"""
Orchestrator for the scripted OpenAI recommendation pipeline (Section A-W of the task).

Pipeline:
  respondent evidence + frozen profile context
    -> BM25 retrieval over the V2 (84-parent) course corpus
    -> deduplicated parent courses
    -> full parent course documents assembled into a structured LLM input
    -> OpenAI Responses API (structured output, RespondentRecommendationResponse)
    -> mechanical + approximate-text grounding audit
    -> outputs/rag_recommendation_prototype_api/*

STOP CONDITION: if OPENAI_API_KEY is not configured, this script verifies/builds
everything that does not require the API, prints a clear status, and exits WITHOUT
calling the API and WITHOUT fabricating any recommendation content.
"""
import csv, json, sys, time
from pathlib import Path

from env_config import has_api_key, describe_key_status, env_file_path, get_recommendation_model
from corpus_v2 import verify_corpus, BASE
from chunking_v2 import build_chunks_and_index
from retrieval_v2 import run as run_retrieval, SAMPLE
import context_pack_v2

OUT_DIR = BASE / "outputs/rag_recommendation_prototype_api"
RESPONDENT_EVIDENCE_JSONL = BASE / "outputs/rag_respondent_evidence/respondent_evidence.jsonl"


def load_respondents():
    out = {}
    with open(RESPONDENT_EVIDENCE_JSONL, encoding="utf-8") as f:
        for line in f:
            rec = json.loads(line)
            out[rec["respondent_id"]] = rec
    return out


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    print("Step 1/6: verifying V2 course corpus (84 indexable + 4 excluded = 88)...")
    manifest, exclusions = verify_corpus(verbose=True)
    manifest_by_id = {r["course_id"]: r for r in manifest}
    excluded_ids = {r["course_id"] for r in exclusions}

    print("Step 2/6: building V2 child chunks + retrieval index metadata...")
    chunks, index_rows = build_chunks_and_index()
    with open(OUT_DIR / "v2_course_child_chunks.jsonl", "w", encoding="utf-8") as f:
        for c in chunks:
            f.write(json.dumps(c, ensure_ascii=False) + "\n")
    with open(OUT_DIR / "v2_course_retrieval_index_metadata.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(index_rows[0].keys()))
        w.writeheader()
        for r in index_rows:
            w.writerow(r)
    print(f"  {len(chunks)} child chunks for {len(index_rows)} parents.")

    print("Step 3/6: running BM25 retrieval for the 10 test respondents...")
    sample_rows, retrieval_audit_rows, bundle = run_retrieval(chunks)
    with open(OUT_DIR / "test_sample.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(sample_rows[0].keys()))
        w.writeheader()
        for r in sample_rows:
            w.writerow(r)
    with open(OUT_DIR / "v2_retrieval_audit.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(retrieval_audit_rows[0].keys()))
        w.writeheader()
        for r in retrieval_audit_rows:
            w.writerow(r)
    with open(OUT_DIR / "_v2_respondent_bundle.json", "w", encoding="utf-8") as f:
        json.dump(bundle, f, indent=2, ensure_ascii=False)
    print(f"  Retrieval complete for {len(sample_rows)} respondents.")

    print("Step 4/6: checking OPENAI_API_KEY...")
    print(f"  {describe_key_status()}")
    if not has_api_key():
        print()
        print("=" * 70)
        print("SCRIPTED RAG PIPELINE PREPARED")
        print("OPENAI_API_KEY REQUIRED BEFORE EXECUTION")
        print("=" * 70)
        print(f"Add your key to: {env_file_path()}")
        print("(copy .env.example to .env in the ClusterRP project root, then set OPENAI_API_KEY=...)")
        print("No API call was made. No recommendation content was fabricated or manually written.")
        return 2

    # -------------------------------------------------------------------
    # Steps 5-6 only run once a key is present.
    # -------------------------------------------------------------------
    from openai_client import call_recommendation_api
    from recommendation_schema import RespondentRecommendationResponse
    respondents = load_respondents()
    profile_index = context_pack_v2.load_profile_index()
    model = get_recommendation_model()

    print(f"Step 5/6: calling OpenAI API (model={model}) for {len(SAMPLE)} respondents...")
    usage_rows = []
    recommendation_records = []

    for rid, branch, case_tag in SAMPLE:
        respondent = respondents[rid]
        b = bundle[rid]
        input_text = context_pack_v2.build_input_text(
            respondent, b["retrieved_parents_ranked"], b["retrieved_parent_scores"],
            manifest_by_id, profile_index,
        )
        result = call_recommendation_api(rid, input_text, model=model)
        usage_rows.append({
            "respondent_id": rid,
            "model": result.model,
            "success": result.success,
            "input_tokens": result.input_tokens,
            "output_tokens": result.output_tokens,
            "total_tokens": result.total_tokens,
            "cached_input_tokens": result.cached_input_tokens,
            "reasoning_tokens": result.reasoning_tokens,
            "duration_seconds": result.duration_seconds,
            "retry_count": result.retry_count,
            "response_id": result.response_id,
            "error_message": result.error_message,
        })
        if result.success:
            parsed: RespondentRecommendationResponse = result.parsed
            recommendation_records.append({
                "respondent_id": rid,
                "branch": branch,
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
            print(f"  {rid}: OK ({parsed.recommendation_status}, "
                  f"{len(parsed.recommendations)} recs, {result.total_tokens} tokens)")
        else:
            print(f"  {rid}: FAILED after {result.retry_count} retries — {result.error_message}")

    with open(OUT_DIR / "api_test_recommendations.jsonl", "w", encoding="utf-8") as f:
        for r in recommendation_records:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

    with open(OUT_DIR / "api_usage_audit.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(usage_rows[0].keys()))
        w.writeheader()
        for r in usage_rows:
            w.writerow(r)

    print("Step 6/6: running automated grounding audit...")
    from grounding_audit_v2 import audit_all
    retrieved_by_respondent = {rid: bundle[rid]["retrieved_parents_ranked"] for rid, _, _ in SAMPLE}
    audit_rows = audit_all(
        OUT_DIR / "api_test_recommendations.jsonl", respondents, retrieved_by_respondent,
        excluded_ids, manifest_by_id,
    )
    with open(OUT_DIR / "api_recommendation_evidence_audit.csv", "w", newline="", encoding="utf-8") as f:
        if audit_rows:
            w = csv.DictWriter(f, fieldnames=list(audit_rows[0].keys()))
            w.writeheader()
            for r in audit_rows:
                w.writerow(r)

    print()
    print(f"Done. {sum(1 for r in usage_rows if r['success'])}/{len(usage_rows)} API calls succeeded.")
    print(f"{len(audit_rows)} recommendations audited.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
