"""
Controlled second API experiment: SAME 10 respondents, SAME 84-course corpus, SAME
BM25 retrieval / retrieved candidate sets (reused byte-for-byte from the first API
run's saved bundle — retrieval is NOT recomputed), only the LLM decision layer
changes: a rebalanced governance prompt (context_pack_v2.GOVERNANCE_INSTRUCTIONS,
revised in place) and a stronger model.

Also re-runs the extended grounding audit (now covering NO_DEFENSIBLE_RECOMMENDATION
decline reasons too) against the ORIGINAL gpt-4o-mini run's already-saved output, for
a fair apples-to-apples comparison under the same audit methodology — this is pure
re-analysis of saved text, not a new API call.

Writes everything to outputs/rag_recommendation_prototype_api_v2/, leaving
outputs/rag_recommendation_prototype_api/ (the first, gpt-4o-mini run) untouched.
"""
import csv, json, sys, functools
from pathlib import Path

print = functools.partial(print, flush=True)  # unbuffered so progress is visible in real time

from env_config import has_api_key, describe_key_status, get_recommendation_model
from corpus_v2 import verify_corpus, BASE
from retrieval_v2 import SAMPLE
import context_pack_v2
from grounding_audit_v2 import audit_all

STRONGER_MODEL = "gpt-5-mini"  # cost-conscious reasoning-tier model, documented choice — see report

OLD_RUN_DIR = BASE / "outputs/rag_recommendation_prototype_api"
NEW_RUN_DIR = BASE / "outputs/rag_recommendation_prototype_api_v2"
RESPONDENT_EVIDENCE_JSONL = BASE / "outputs/rag_respondent_evidence/respondent_evidence.jsonl"


def load_respondents():
    out = {}
    with open(RESPONDENT_EVIDENCE_JSONL, encoding="utf-8") as f:
        for line in f:
            rec = json.loads(line)
            out[rec["respondent_id"]] = rec
    return out


def write_csv(path, rows):
    if not rows:
        return
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        for r in rows:
            w.writerow(r)


def main():
    NEW_RUN_DIR.mkdir(parents=True, exist_ok=True)

    print("Step 1: verifying V2 corpus is unchanged (84 indexable + 4 excluded = 88)...")
    manifest, exclusions = verify_corpus(verbose=True)
    manifest_by_id = {r["course_id"]: r for r in manifest}
    excluded_ids = {r["course_id"] for r in exclusions}

    print("Step 2: loading the FIRST run's saved retrieval bundle (retrieval is reused, not recomputed)...")
    bundle_path = OLD_RUN_DIR / "_v2_respondent_bundle.json"
    if not bundle_path.exists():
        raise SystemExit(f"{bundle_path} not found — run the first API experiment before this one.")
    bundle = json.loads(bundle_path.read_text(encoding="utf-8"))
    retrieved_by_respondent = {rid: bundle[rid]["retrieved_parents_ranked"] for rid in bundle}
    print(f"  Loaded retrieval for {len(bundle)} respondents (unchanged from the first run).")

    print("Step 3: re-auditing the ORIGINAL gpt-4o-mini run's saved output with the EXTENDED audit "
          "(no new API calls — pure re-analysis of already-saved text)...")
    respondents = load_respondents()
    old_jsonl = OLD_RUN_DIR / "api_test_recommendations.jsonl"
    old_audit_rows = audit_all(old_jsonl, respondents, retrieved_by_respondent, excluded_ids, manifest_by_id)
    write_csv(NEW_RUN_DIR / "gpt4o_mini_extended_reaudit.csv", old_audit_rows)
    from collections import Counter
    print(f"  Extended audit of the original gpt-4o-mini run: "
          f"{dict(Counter(r['final_audit_status'] for r in old_audit_rows))}")

    print(f"Step 4: checking OPENAI_API_KEY... {describe_key_status()}")
    if not has_api_key():
        print()
        print("=" * 70)
        print("SCRIPTED RAG PIPELINE (EXPERIMENT 2) PREPARED")
        print("OPENAI_API_KEY REQUIRED BEFORE EXECUTION")
        print("=" * 70)
        return 2

    print(f"Step 5: calling OpenAI API (model={STRONGER_MODEL}) for {len(SAMPLE)} respondents...")
    from openai_client import call_recommendation_api
    from recommendation_schema import RespondentRecommendationResponse
    profile_index = context_pack_v2.load_profile_index()

    usage_rows, recommendation_records = [], []
    for i, (rid, branch, case_tag) in enumerate(SAMPLE, start=1):
        print(f"  [{i}/{len(SAMPLE)}] calling for {rid} ({branch}, {len(bundle[rid]['retrieved_parents_ranked'])} retrieved parents)...")
        respondent = respondents[rid]
        b = bundle[rid]
        input_text = context_pack_v2.build_input_text(
            respondent, b["retrieved_parents_ranked"], b["retrieved_parent_scores"],
            manifest_by_id, profile_index,
        )
        result = call_recommendation_api(rid, input_text, model=STRONGER_MODEL)
        usage_rows.append({
            "respondent_id": rid, "model": result.model, "success": result.success,
            "input_tokens": result.input_tokens, "output_tokens": result.output_tokens,
            "total_tokens": result.total_tokens, "cached_input_tokens": result.cached_input_tokens,
            "reasoning_tokens": result.reasoning_tokens, "duration_seconds": result.duration_seconds,
            "retry_count": result.retry_count, "response_id": result.response_id,
            "error_message": result.error_message,
        })
        if result.success:
            parsed: RespondentRecommendationResponse = result.parsed
            recommendation_records.append({
                "respondent_id": rid, "branch": branch,
                "profile_memberships": respondent["frozen_profile_memberships"],
                "retrieval": {
                    "query_summary": b["query_summary"],
                    "retrieved_course_ids": b["retrieved_parents_ranked"],
                    "retrieval_scores": b["retrieved_parent_scores"],
                },
                "recommendation_status": parsed.recommendation_status,
                "recommendations": [r.model_dump() for r in parsed.recommendations],
                "no_defensible_recommendation_reason": parsed.no_defensible_recommendation_reason,
            })
            print(f"  {rid}: OK ({parsed.recommendation_status}, {len(parsed.recommendations)} recs, "
                  f"{result.total_tokens} tokens, {result.reasoning_tokens} reasoning tokens)")
        else:
            print(f"  {rid}: FAILED after {result.retry_count} retries — {result.error_message}")

    with open(NEW_RUN_DIR / "api_test_recommendations.jsonl", "w", encoding="utf-8") as f:
        for r in recommendation_records:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    write_csv(NEW_RUN_DIR / "api_usage_audit.csv", usage_rows)

    print("Step 6: running the extended grounding audit on the NEW run...")
    new_audit_rows = audit_all(NEW_RUN_DIR / "api_test_recommendations.jsonl", respondents,
                                retrieved_by_respondent, excluded_ids, manifest_by_id)
    write_csv(NEW_RUN_DIR / "api_recommendation_evidence_audit.csv", new_audit_rows)
    print(f"  New run audit: {dict(Counter(r['final_audit_status'] for r in new_audit_rows))}")

    n_success = sum(1 for r in usage_rows if r["success"])
    print()
    print(f"Done. {n_success}/{len(usage_rows)} API calls succeeded with model={STRONGER_MODEL}.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
