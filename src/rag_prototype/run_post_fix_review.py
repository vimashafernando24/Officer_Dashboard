"""
FINAL post-fix live review: the SAME 10 targeted respondents used in
run_final_validation.py, re-run through the NOW-FULLY-FIXED pipeline —
this is the first LIVE test of the tightened, no-hedging-exception economic-
affordability governance rule (added after run_final_validation.py's run, with no
live call to confirm it actually changes model behaviour, not just audit behaviour),
and the first LIVE end-to-end exercise of the new get_production_model() /
verify_production_model() config mechanism.

Unchanged: gpt-5-mini (now sourced via env_config.get_production_model(), verified at
startup), the 84-course V2 corpus, BM25 retrieval (reused byte-for-byte from the
original saved bundle — not recomputed), the same 10 respondents (no new ones), frozen
clustering/profile assignments, respondent evidence source.

Writes to outputs/rag_recommendation_post_fix_review/, leaving
outputs/rag_recommendation_final_validation/ (the prior "before" run) untouched.
"""
import csv, hashlib, json, sys, functools
from pathlib import Path

print = functools.partial(print, flush=True)

from env_config import has_api_key, describe_key_status, get_production_model, verify_production_model
from corpus_v2 import verify_corpus, BASE
import context_pack_v2
from run_final_validation import TARGETED_10  # same 10 respondents, same selection rationale

OLD_BATCH_JSONL = BASE / "outputs/rag_recommendation_validation_30/api_recommendations_30.jsonl"
BEFORE_JSONL = BASE / "outputs/rag_recommendation_final_validation/api_recommendations_final.jsonl"
RESPONDENT_EVIDENCE_JSONL = BASE / "outputs/rag_respondent_evidence/respondent_evidence.jsonl"
OUT_DIR = BASE / "outputs/rag_recommendation_post_fix_review"


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def load_respondents():
    out = {}
    with open(RESPONDENT_EVIDENCE_JSONL, encoding="utf-8") as f:
        for line in f:
            rec = json.loads(line)
            out[rec["respondent_id"]] = rec
    return out


def load_retrieval_bundle():
    """Retrieval is reused byte-for-byte from the 30-person batch's saved bundle
    (the same source run_final_validation.py used) — not recomputed."""
    bundle = {}
    with open(OLD_BATCH_JSONL, encoding="utf-8") as f:
        for line in f:
            rec = json.loads(line)
            if rec["respondent_id"] in {rid for rid, _, _ in TARGETED_10}:
                bundle[rec["respondent_id"]] = rec["retrieval"]
    return bundle


def write_csv(path, rows):
    if not rows:
        return
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        for r in rows:
            w.writerow(r)


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUT_DIR / "call_snapshots").mkdir(exist_ok=True)

    print("Step 1: verifying production model configuration (new authoritative mechanism)...")
    model = get_production_model()
    verify_production_model(model)

    print("Step 2: verifying V2 corpus is unchanged (84 indexable + 4 excluded = 88)...")
    manifest, exclusions = verify_corpus(verbose=True)
    manifest_by_id = {r["course_id"]: r for r in manifest}
    excluded_ids = {r["course_id"] for r in exclusions}
    corpus_manifest_hash = sha256_text(json.dumps(manifest, sort_keys=True))

    print("Step 3: loading SAVED retrieval (reused, not recomputed) for the same 10 respondents...")
    bundle = load_retrieval_bundle()
    missing = [rid for rid, _, _ in TARGETED_10 if rid not in bundle]
    if missing:
        raise SystemExit(f"Missing retrieval for: {missing}")
    print(f"  Loaded retrieval for {len(bundle)} respondents.")

    print(f"Step 4: checking OPENAI_API_KEY... {describe_key_status()}")
    if not has_api_key():
        print("OPENAI_API_KEY REQUIRED BEFORE EXECUTION")
        return 2

    instructions_hash = sha256_text(context_pack_v2.GOVERNANCE_INSTRUCTIONS)
    print(f"Governance instructions hash (post-fix, this run): {instructions_hash[:16]}...")

    print(f"Step 5: calling OpenAI API (model={model}, FINAL fixed prompt+schema) for {len(TARGETED_10)} respondents...")
    from openai_client import call_recommendation_api
    from recommendation_schema import RespondentRecommendationResponse
    respondents = load_respondents()
    profile_index = context_pack_v2.load_profile_index()

    usage_rows, after_records = [], []
    for i, (rid, branch, reason) in enumerate(TARGETED_10, start=1):
        print(f"  [{i}/{len(TARGETED_10)}] calling for {rid} ({branch})...")
        respondent = respondents[rid]
        b = bundle[rid]
        retrieved_ids = b["retrieved_course_ids"]
        retrieved_scores = b["retrieval_scores"]

        input_text = context_pack_v2.build_input_text(
            respondent, retrieved_ids, retrieved_scores, manifest_by_id, profile_index,
        )
        result = call_recommendation_api(rid, input_text, model=model)

        usage_rows.append({
            "respondent_id": rid, "model": result.model, "success": result.success,
            "input_tokens": result.input_tokens, "output_tokens": result.output_tokens,
            "total_tokens": result.total_tokens, "cached_input_tokens": result.cached_input_tokens,
            "reasoning_tokens": result.reasoning_tokens, "duration_seconds": result.duration_seconds,
            "retry_count": result.retry_count, "response_id": result.response_id,
            "error_message": result.error_message,
        })

        profile_doc_refs = [f"{m['model_id']}_p{m['profile_id']}" for m in respondent["frozen_profile_memberships"]]
        snapshot = {
            "respondent_id": rid, "model": model,
            "governance_instructions_sha256": instructions_hash,
            "constructed_input_text": input_text,
            "retrieved_course_ids": retrieved_ids, "retrieved_course_scores": retrieved_scores,
            "profile_document_refs": profile_doc_refs,
            "course_corpus_manifest_sha256": corpus_manifest_hash,
            "response_id": result.response_id,
            "token_usage": {
                "input_tokens": result.input_tokens, "output_tokens": result.output_tokens,
                "total_tokens": result.total_tokens, "cached_input_tokens": result.cached_input_tokens,
                "reasoning_tokens": result.reasoning_tokens,
            },
            "success": result.success, "error_message": result.error_message,
        }
        with open(OUT_DIR / "call_snapshots" / f"{rid}.json", "w", encoding="utf-8") as f:
            json.dump(snapshot, f, indent=2, ensure_ascii=False)

        if result.success:
            parsed: RespondentRecommendationResponse = result.parsed
            after_records.append({
                "respondent_id": rid, "branch": branch, "selection_reason": reason,
                "profile_memberships": respondent["frozen_profile_memberships"],
                "retrieval": {"retrieved_course_ids": retrieved_ids, "retrieval_scores": retrieved_scores},
                "recommendation_status": parsed.recommendation_status,
                "catalogue_coverage_note": parsed.catalogue_coverage_note,
                "recommendations": [r.model_dump() for r in parsed.recommendations],
                "no_defensible_recommendation_reason": parsed.no_defensible_recommendation_reason,
            })
            print(f"  {rid}: OK ({parsed.recommendation_status}, {len(parsed.recommendations)} recs, "
                  f"{result.total_tokens} tokens)")
        else:
            print(f"  {rid}: FAILED after {result.retry_count} retries — {result.error_message}")

        with open(OUT_DIR / "api_recommendations_post_fix.jsonl", "w", encoding="utf-8") as f:
            for r in after_records:
                f.write(json.dumps(r, ensure_ascii=False) + "\n")
        write_csv(OUT_DIR / "api_usage_post_fix.csv", usage_rows)

    print("Step 6: running ALL THREE audits (grounding, category-discipline, evidence-hierarchy)...")
    from grounding_audit_v2 import audit_all as grounding_audit_all
    retrieved_by_respondent = {rid: bundle[rid]["retrieved_course_ids"] for rid, _, _ in TARGETED_10}
    grounding_rows = grounding_audit_all(OUT_DIR / "api_recommendations_post_fix.jsonl", respondents,
                                          retrieved_by_respondent, excluded_ids, manifest_by_id)
    write_csv(OUT_DIR / "grounding_audit_post_fix.csv", grounding_rows)

    from evidence_category_discipline_audit import load_policy, audit_recommendations, audit_declines
    policy = load_policy()
    cat_rows = audit_recommendations(OUT_DIR / "api_recommendations_post_fix.jsonl", policy, "gpt-5-mini-post-fix")
    cat_rows += audit_declines(OUT_DIR / "api_recommendations_post_fix.jsonl", policy, respondents, "gpt-5-mini-post-fix")
    write_csv(OUT_DIR / "evidence_category_audit_post_fix.csv", cat_rows)

    import evidence_hierarchy_audit as eha
    hierarchy_rows = eha.audit_all(OUT_DIR / "api_recommendations_post_fix.jsonl", policy)
    write_csv(OUT_DIR / "evidence_hierarchy_audit_post_fix.csv", hierarchy_rows)

    from collections import Counter
    print(f"  Grounding audit: {dict(Counter(r['final_audit_status'] for r in grounding_rows))}")
    print(f"  Category-discipline audit: {dict(Counter(r['status'] for r in cat_rows))}")
    print(f"  Evidence-hierarchy audit: {dict(Counter(r['status'] for r in hierarchy_rows))}")

    n_success = sum(1 for r in usage_rows if r["success"])
    print()
    print(f"Done. {n_success}/{len(usage_rows)} API calls succeeded with model={model}.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
