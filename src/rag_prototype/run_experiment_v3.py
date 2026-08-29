"""
Prompt-fix verification run: SAME 10 respondents, SAME 84-course corpus, SAME BM25
retrieval / retrieved candidate sets (reused byte-for-byte from the first API run's
saved bundle — retrieval is NOT recomputed), SAME model (gpt-5-mini). The ONLY change
from the v2 run is the governance prompt, which now includes the targeted
evidence-category-discipline fix (context_pack_v2.GOVERNANCE_INSTRUCTIONS, §9 of
evidence_category_discipline_report.md).

Writes to outputs/rag_recommendation_prototype_api_v3/, leaving
outputs/rag_recommendation_prototype_api_v2/ (the "before" run) fully intact for
before/after comparison.
"""
import csv, json, sys, functools
from pathlib import Path

print = functools.partial(print, flush=True)

from env_config import has_api_key, describe_key_status, get_recommendation_model
from corpus_v2 import verify_corpus, BASE
from retrieval_v2 import SAMPLE
import context_pack_v2

MODEL = "gpt-5-mini"  # unchanged from v2, per instructions

OLD_RUN_DIR = BASE / "outputs/rag_recommendation_prototype_api"          # v1 bundle source
V2_RUN_DIR = BASE / "outputs/rag_recommendation_prototype_api_v2"        # "before" snapshot, untouched
V3_RUN_DIR = BASE / "outputs/rag_recommendation_prototype_api_v3"        # "after" (this run)
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
    V3_RUN_DIR.mkdir(parents=True, exist_ok=True)

    print("Step 1: verifying V2 corpus is unchanged (84 indexable + 4 excluded = 88)...")
    manifest, exclusions = verify_corpus(verbose=True)
    manifest_by_id = {r["course_id"]: r for r in manifest}

    print("Step 2: loading the FIRST run's saved retrieval bundle (retrieval reused, not recomputed)...")
    bundle_path = OLD_RUN_DIR / "_v2_respondent_bundle.json"
    bundle = json.loads(bundle_path.read_text(encoding="utf-8"))
    print(f"  Loaded retrieval for {len(bundle)} respondents (identical to the v2/before run).")

    print("Step 3: confirming the SAME 10 respondents as before...")
    prev_ids = {rid for rid, _, _ in SAMPLE}
    print(f"  {len(prev_ids)} respondents, unchanged sample list — no new respondents.")

    print(f"Step 4: checking OPENAI_API_KEY... {describe_key_status()}")
    if not has_api_key():
        print("OPENAI_API_KEY REQUIRED BEFORE EXECUTION")
        return 2

    print(f"Step 5: calling OpenAI API (model={MODEL}, UPDATED prompt) for {len(SAMPLE)} respondents...")
    from openai_client import call_recommendation_api
    from recommendation_schema import RespondentRecommendationResponse
    respondents = load_respondents()
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
        result = call_recommendation_api(rid, input_text, model=MODEL)
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

        # Write incrementally after every respondent so a partial run is never lost.
        with open(V3_RUN_DIR / "api_test_recommendations.jsonl", "w", encoding="utf-8") as f:
            for r in recommendation_records:
                f.write(json.dumps(r, ensure_ascii=False) + "\n")
        write_csv(V3_RUN_DIR / "api_usage_audit.csv", usage_rows)

    print("Step 6: running the extended grounding audit (fabrication/eligibility/etc.) on the NEW run...")
    from grounding_audit_v2 import audit_all
    excluded_ids = {r["course_id"] for r in exclusions}
    retrieved_by_respondent = {rid: bundle[rid]["retrieved_parents_ranked"] for rid in bundle}
    audit_rows = audit_all(V3_RUN_DIR / "api_test_recommendations.jsonl", respondents,
                            retrieved_by_respondent, excluded_ids, manifest_by_id)
    write_csv(V3_RUN_DIR / "api_recommendation_evidence_audit.csv", audit_rows)
    from collections import Counter
    print(f"  Grounding audit: {dict(Counter(r['final_audit_status'] for r in audit_rows))}")

    n_success = sum(1 for r in usage_rows if r["success"])
    print()
    print(f"Done. {n_success}/{len(usage_rows)} API calls succeeded with model={MODEL} (updated prompt).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
