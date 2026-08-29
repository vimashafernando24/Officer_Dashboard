"""
PRODUCTION full-cohort runner — the finalized pipeline for all 362 respondents.

NOT executed as part of the production-readiness fix task that created this file
(that task explicitly prohibited new API calls). This script is prepared, verified
structurally (imports, model-abort check, resume-skip logic), and frozen, ready to be
invoked separately when the full run is authorized.

Guarantees, each satisfying one item of the production-readiness checklist:
  - uses gpt-5-mini: the ONLY model ever used is env_config.get_production_model(),
    verified at startup via env_config.verify_production_model(), which prints the
    selected model and aborts (SystemExit) unless it is exactly "gpt-5-mini". This
    module never reads OPENAI_RECOMMENDATION_MODEL from .env at all.
  - uses the frozen 84-course corpus: corpus_v2.verify_corpus() (SHA-256-checked
    against the manifest) runs before anything else and raises if it doesn't match.
  - uses the finalized governance prompt: context_pack_v2.GOVERNANCE_INSTRUCTIONS,
    imported directly, not duplicated or reconstructed.
  - preserves profile context as group-level supporting evidence: unchanged from
    context_pack_v2.build_input_text(), which labels Section 2 as
    "GROUP-LEVEL RESEARCH CONTEXT — DO NOT ASSUME THESE CHARACTERISTICS APPLY TO THIS
    INDIVIDUAL" and is not modified by this script.
  - saves the literal input/context snapshot for every call: see call_snapshots/.
  - saves model/prompt/corpus hashes and token usage: see each snapshot's fields.
  - writes results incrementally: each respondent's snapshot and JSONL line are
    written immediately after that respondent's call completes, before moving to the
    next respondent.
  - resumable without duplicating completed respondents: on startup, reads the
    existing output JSONL (if any) and skips any respondent_id already present,
    appending only new results — see load_already_completed().
"""
import csv, hashlib, json, sys, functools, time
from pathlib import Path

print = functools.partial(print, flush=True)

from env_config import has_api_key, describe_key_status, get_production_model, verify_production_model
from corpus_v2 import verify_corpus, BASE
import context_pack_v2

OUT_DIR = BASE / "outputs/rag_recommendation_full_cohort"
RESPONDENT_EVIDENCE_JSONL = BASE / "outputs/rag_respondent_evidence/respondent_evidence.jsonl"
RESULTS_JSONL = OUT_DIR / "api_recommendations_full_cohort.jsonl"
USAGE_CSV = OUT_DIR / "api_usage_full_cohort.csv"
SNAPSHOT_DIR = OUT_DIR / "call_snapshots"


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def load_respondents():
    out = {}
    with open(RESPONDENT_EVIDENCE_JSONL, encoding="utf-8") as f:
        for line in f:
            rec = json.loads(line)
            out[rec["respondent_id"]] = rec
    return out


def load_already_completed() -> set:
    """Resume support: respondent_ids already present in the output JSONL are never
    re-called. Safe to run this script repeatedly after any interruption."""
    if not RESULTS_JSONL.exists():
        return set()
    done = set()
    with open(RESULTS_JSONL, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                done.add(json.loads(line)["respondent_id"])
            except (json.JSONDecodeError, KeyError):
                continue  # ignore a possibly-truncated final line from a prior interruption
    return done


def build_retrieval_for_respondent(rid, respondent, bm25, chunks, skill_area_keywords):
    """Uses the UNCHANGED retrieval architecture (retrieval_v2.build_query /
    retrieve_parents), imported directly rather than reimplemented."""
    import retrieval_v2
    query_text, query_summary = retrieval_v2.build_query(respondent, skill_area_keywords)
    chunk_hits, parent_scores = retrieval_v2.retrieve_parents(bm25, chunks, query_text)
    ranked_parents = sorted(parent_scores.items(), key=lambda kv: kv[1], reverse=True)
    return {
        "query_summary": query_summary,
        "retrieved_course_ids": [pid for pid, _ in ranked_parents],
        "retrieval_scores": {pid: round(s, 4) for pid, s in ranked_parents},
    }


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    SNAPSHOT_DIR.mkdir(exist_ok=True)

    print("Step 1: verifying production model configuration...")
    model = get_production_model()
    verify_production_model(model)  # prints selected model; raises SystemExit if wrong

    print("Step 2: verifying V2 corpus is unchanged (84 indexable + 4 excluded = 88)...")
    manifest, exclusions = verify_corpus(verbose=True)
    manifest_by_id = {r["course_id"]: r for r in manifest}
    excluded_ids = {r["course_id"] for r in exclusions}
    corpus_manifest_hash = sha256_text(json.dumps(manifest, sort_keys=True))

    print("Step 3: checking for already-completed respondents (resume support)...")
    already_done = load_already_completed()
    print(f"  {len(already_done)} respondents already completed in a prior run — will be skipped.")

    print(f"Step 4: checking OPENAI_API_KEY... {describe_key_status()}")
    if not has_api_key():
        print("OPENAI_API_KEY REQUIRED BEFORE EXECUTION")
        return 2

    print("Step 5: building retrieval index (unchanged BM25 architecture)...")
    from chunking_v2 import build_chunks_and_index
    from bm25 import BM25
    import retrieval_v2
    chunks, _ = build_chunks_and_index()
    bm25 = BM25([c["text"] for c in chunks])
    skill_area_keywords = retrieval_v2.load_skill_area_keywords()

    respondents = load_respondents()
    all_ids = list(respondents.keys())
    remaining = [rid for rid in all_ids if rid not in already_done]
    print(f"  {len(all_ids)} total respondents in the frozen evidence file; {len(remaining)} remaining to process.")

    instructions_hash = sha256_text(context_pack_v2.GOVERNANCE_INSTRUCTIONS)
    print(f"Governance instructions hash: {instructions_hash[:16]}...")

    from openai_client import call_recommendation_api
    from recommendation_schema import RespondentRecommendationResponse
    profile_index = context_pack_v2.load_profile_index()

    print(f"Step 6: processing {len(remaining)} respondents (model={model})...")
    for i, rid in enumerate(remaining, start=1):
        t0 = time.monotonic()
        respondent = respondents[rid]
        retrieval = build_retrieval_for_respondent(rid, respondent, bm25, chunks, skill_area_keywords)

        input_text = context_pack_v2.build_input_text(
            respondent, retrieval["retrieved_course_ids"], retrieval["retrieval_scores"],
            manifest_by_id, profile_index,
        )
        result = call_recommendation_api(rid, input_text, model=model)

        # --- Auditability snapshot: written BEFORE the aggregate files, so even an
        # interruption immediately after this line leaves a complete, self-contained
        # record of exactly what was sent and (if successful) what came back. ---
        profile_doc_refs = [f"{m['model_id']}_p{m['profile_id']}" for m in respondent["frozen_profile_memberships"]]
        snapshot = {
            "respondent_id": rid,
            "model": model,
            "governance_instructions_sha256": instructions_hash,
            "constructed_input_text": input_text,
            "retrieved_course_ids": retrieval["retrieved_course_ids"],
            "retrieved_course_scores": retrieval["retrieval_scores"],
            "profile_document_refs": profile_doc_refs,
            "course_corpus_manifest_sha256": corpus_manifest_hash,
            "response_id": result.response_id,
            "token_usage": {
                "input_tokens": result.input_tokens, "output_tokens": result.output_tokens,
                "total_tokens": result.total_tokens, "cached_input_tokens": result.cached_input_tokens,
                "reasoning_tokens": result.reasoning_tokens,
            },
            "success": result.success,
            "error_message": result.error_message,
        }
        with open(SNAPSHOT_DIR / f"{rid}.json", "w", encoding="utf-8") as f:
            json.dump(snapshot, f, indent=2, ensure_ascii=False)

        # --- Usage row: appended, not rewritten from scratch, so this scales cleanly
        # to 362 respondents and is safe to resume. ---
        usage_row = {
            "respondent_id": rid, "model": result.model, "success": result.success,
            "input_tokens": result.input_tokens, "output_tokens": result.output_tokens,
            "total_tokens": result.total_tokens, "cached_input_tokens": result.cached_input_tokens,
            "reasoning_tokens": result.reasoning_tokens, "duration_seconds": result.duration_seconds,
            "retry_count": result.retry_count, "response_id": result.response_id,
            "error_message": result.error_message,
        }
        usage_file_exists = USAGE_CSV.exists()
        with open(USAGE_CSV, "a", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=list(usage_row.keys()))
            if not usage_file_exists:
                w.writeheader()
            w.writerow(usage_row)

        if result.success:
            parsed: RespondentRecommendationResponse = result.parsed
            record = {
                "respondent_id": rid, "branch": respondent["branch"],
                "profile_memberships": respondent["frozen_profile_memberships"],
                "retrieval": retrieval,
                "recommendation_status": parsed.recommendation_status,
                "catalogue_coverage_note": parsed.catalogue_coverage_note,
                "recommendations": [r.model_dump() for r in parsed.recommendations],
                "no_defensible_recommendation_reason": parsed.no_defensible_recommendation_reason,
            }
            # --- Append-only results write: this is what makes resume-without-
            # duplication safe. A fresh process re-reads this file at startup
            # (load_already_completed) and only ever appends new lines. ---
            with open(RESULTS_JSONL, "a", encoding="utf-8") as f:
                f.write(json.dumps(record, ensure_ascii=False) + "\n")
            print(f"  [{i}/{len(remaining)}] {rid}: OK ({parsed.recommendation_status}, "
                  f"{len(parsed.recommendations)} recs, {result.total_tokens} tokens, "
                  f"{time.monotonic()-t0:.1f}s)")
        else:
            print(f"  [{i}/{len(remaining)}] {rid}: FAILED after {result.retry_count} retries — "
                  f"{result.error_message} — NOT written to results (will retry on next resume)")

    print()
    print(f"Done. {len(load_already_completed())}/{len(all_ids)} respondents completed overall.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
