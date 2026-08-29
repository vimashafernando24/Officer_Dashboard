"""
Validation batch: 30 NEW respondents (never used in the frozen 10-person v3 baseline),
run through the UNCHANGED scripted pipeline — same 84-course V2 corpus, same BM25
retrieval architecture and query-construction logic (imported directly from
retrieval_v2.py, not reimplemented), same evidence-category-disciplined governance
prompt, same gpt-5-mini model, same recommendation schema, same two audits, same
hard-timeout/retry/incremental-save safeguards.

Only the ORCHESTRATION differs from retrieval_v2.py/run_experiment_v3.py: it iterates
a new 30-respondent sample instead of the frozen 10, because retrieval has never been
computed for these 30 (there is no prior bundle to reuse, unlike the v2->v3 comparison
which intentionally reused the same 10 respondents' retrieval). The retrieval
ALGORITHM itself (BM25 class, build_query, retrieve_parents) is imported unchanged from
retrieval_v2.py and bm25.py.
"""
import csv, json, sys, functools

print = functools.partial(print, flush=True)

from env_config import has_api_key, describe_key_status, get_recommendation_model
from corpus_v2 import verify_corpus, BASE
from chunking_v2 import build_chunks_and_index
from bm25 import BM25
import retrieval_v2  # reused unchanged: build_query, retrieve_parents, load_respondents, load_skill_area_keywords
import context_pack_v2

MODEL = "gpt-5-mini"  # unchanged, per instructions
OUT_DIR = BASE / "outputs/rag_recommendation_validation_30"

SELECTED_30 = {
    "D": [
        ("nysc-0cba8a68-ebf6-47cb-bd45-e2a1d78ad74b", "Education and teaching; distinct D profile combo"),
        ("nysc-0d099a8b-7f90-43c3-8b8d-6eb1c4c23e88", "Manufacturing or production"),
        ("nysc-4eae9a51-70b3-48ae-ae06-6fe372ac0230", "Finance, banking, and insurance"),
        ("nysc-4e38db03-e477-420e-9afd-d3f92b53995d", "Health, social work, and wellbeing"),
        ("nysc-8ae4a1d8-97c7-4bc4-9dc9-cb7eea0c897f", "Creative, media, and arts"),
        ("nysc-4401e631-9304-4f41-9ba4-6f84d659f7c8", "Agriculture, forestry, and fishing"),
        ("nysc-515dbda4-d209-46f1-b1cd-a9f996f9cebd", "Hotels, restaurants, and hospitality"),
        ("nysc-b556590a-0e0d-4d6f-8b9e-f148e18ca930", "Weak/unsure sector AND field — NO_DEFENSIBLE stress test"),
        ("nysc-25c345ec-5f45-4616-adb8-c96e31f3511c", "has_children=Yes, never studied, conflicting intent signals"),
        ("nysc-0566257f-e441-4134-9a0f-ebedde047f88", "ICT + worked_while_studying — experience-building test"),
        ("nysc-15a74ec0-011b-4f61-804e-72de37c73705", "Public administration/government sector, new combo"),
    ],
    "E": [
        ("nysc-0a4832c0-3e8a-47e9-ac41-22252b0ceb06", "E profile 1, ICT, entrepreneurship-training interest"),
        ("nysc-136c3ecd-09d4-4238-8a63-64c8636724df", "E profile 2, ICT, self-employment intent"),
        ("nysc-2e8a4c77-f611-4fff-9da8-9161a3f0f368", "E profile 1, Personal services/beauty sector"),
        ("nysc-3258dc18-84da-4092-82af-cfb84352536e", "E profile 2, Manufacturing, wage barrier"),
        ("nysc-cab6cf5f-13dc-4f50-9d5a-b24f266dc279", "E profile 2, sector unsure but job_type/training signals present — partial-weak test"),
    ],
    "F": [
        ("nysc-04134b0d-f3fe-4a25-916c-ee106362e150", "F profile 1 (insecure), weak/unsure sector, professional occupational_class"),
        ("nysc-4646cb19-0ac0-49ca-a00b-e2d8cb16b65e", "F profile 2 (secure), weak/unsure sector"),
        ("nysc-03b655c2-0162-44b7-a418-e4d9ac99ccbb", "F profile 1, Retail/repair, job-change-for-pay intent"),
        ("nysc-1a42a4ad-7444-4e03-8b9c-7ce184f7850c", "F profile 1, Creative arts, no-experience barrier"),
        ("nysc-0a92b28f-94dc-44ce-9e9e-2d25b35c0b04", "F profile 2, Manufacturing, satisfied/stable"),
        ("nysc-14ffa0bd-0d24-4a0e-b75d-516771a7fbbb", "F profile 1, ICT, qualification mismatch signal"),
        ("nysc-079cc6c0-68dd-4ae3-b5e3-9ffd99d463f3", "F profile 2, ICT, wants to change job"),
        ("nysc-34933c14-655f-4189-800f-2419775963fe", "F profile 2, ICT self-employed, financing obstacle"),
    ],
    "G": [
        ("nysc-27b17da2-64b7-4031-b4ac-3205b9b2a735", "G economic_role p1 / future_engagement p1, ICT, caregiving time-constraint"),
        ("nysc-31cab333-afc9-48c5-baec-8ba48e14defb", "G p1/p2, Personal services/beauty, seasonal-worker, low engagement"),
        ("nysc-0717027e-65cc-4b29-9b44-17593f66aaf5", "G p2/p1, ICT, 'no suitable work in area' barrier"),
        ("nysc-27c2ff48-e39c-4db3-aa11-a149d76be479", "G p2/p1, ICT, caregiving + shared provider"),
        ("nysc-49b62c9a-e647-4f21-9742-305d52c6b5a9", "G p2/p2 (rare combo), Education sector, provider+children, conflicting work-intent signals"),
        ("nysc-5242257e-4708-442a-a41f-1081109194a9", "G p2/p2, weak/unsure sector, does not wish to work — strong NO_DEFENSIBLE test"),
    ],
}


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

    print("Step 1: verifying V2 corpus is unchanged (84 indexable + 4 excluded = 88)...")
    manifest, exclusions = verify_corpus(verbose=True)
    manifest_by_id = {r["course_id"]: r for r in manifest}
    excluded_ids = {r["course_id"] for r in exclusions}

    print("Step 2: building V2 child chunks (same chunking code as before, corpus unchanged)...")
    chunks, _ = build_chunks_and_index()
    print(f"  {len(chunks)} child chunks.")

    print("Step 3: running BM25 retrieval (same architecture/query logic, new respondents)...")
    respondents = retrieval_v2.load_respondents()
    skill_area_keywords = retrieval_v2.load_skill_area_keywords()
    bm25 = BM25([c["text"] for c in chunks])

    flat_sample = [(rid, branch, note) for branch, lst in SELECTED_30.items() for rid, note in lst]
    assert len(flat_sample) == 30

    sample_rows, retrieval_audit_rows, bundle = [], [], {}
    for rid, branch, note in flat_sample:
        rec = respondents[rid]
        assert rec["branch"] == branch, f"{rid} branch mismatch"
        query_text, query_summary = retrieval_v2.build_query(rec, skill_area_keywords)
        chunk_hits, parent_scores = retrieval_v2.retrieve_parents(bm25, chunks, query_text)
        ranked_parents = sorted(parent_scores.items(), key=lambda kv: kv[1], reverse=True)

        sample_rows.append({
            "respondent_id": rid, "branch": branch, "selection_rationale": note,
            "n_profile_memberships": len(rec["frozen_profile_memberships"]),
            "profile_memberships": ";".join(f"{m['model_id']}:p{m['profile_id']}" for m in rec["frozen_profile_memberships"]),
            "n_retrieved_parents": len(ranked_parents),
        })
        for rank, (chunk_id, pid, cname, section, score) in enumerate(chunk_hits, start=1):
            retrieval_audit_rows.append({
                "respondent_id": rid, "chunk_rank": rank, "child_chunk_id": chunk_id,
                "parent_course_id": pid, "course_name": cname, "section": section,
                "bm25_score": round(score, 4),
            })
        bundle[rid] = {
            "query_text": query_text, "query_summary": query_summary,
            "retrieved_parents_ranked": [pid for pid, _ in ranked_parents],
            "retrieved_parent_scores": {pid: round(s, 4) for pid, s in ranked_parents},
        }

    write_csv(OUT_DIR / "validation_sample_30.csv", sample_rows)
    with open(OUT_DIR / "validation_30_retrieval_audit.csv", "w", newline="", encoding="utf-8") as f:
        if retrieval_audit_rows:
            w = csv.DictWriter(f, fieldnames=list(retrieval_audit_rows[0].keys()))
            w.writeheader()
            for r in retrieval_audit_rows:
                w.writerow(r)
    print(f"  Retrieval complete for {len(flat_sample)} respondents.")

    print(f"Step 4: checking OPENAI_API_KEY... {describe_key_status()}")
    if not has_api_key():
        print("OPENAI_API_KEY REQUIRED BEFORE EXECUTION")
        return 2

    print(f"Step 5: calling OpenAI API (model={MODEL}) for {len(flat_sample)} respondents...")
    from openai_client import call_recommendation_api
    from recommendation_schema import RespondentRecommendationResponse
    profile_index = context_pack_v2.load_profile_index()

    usage_rows, recommendation_records = [], []
    for i, (rid, branch, note) in enumerate(flat_sample, start=1):
        print(f"  [{i}/{len(flat_sample)}] calling for {rid} ({branch}, {len(bundle[rid]['retrieved_parents_ranked'])} retrieved parents)...")
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

        # Incremental save after every respondent.
        with open(OUT_DIR / "api_recommendations_30.jsonl", "w", encoding="utf-8") as f:
            for r in recommendation_records:
                f.write(json.dumps(r, ensure_ascii=False) + "\n")
        write_csv(OUT_DIR / "api_usage_30.csv", usage_rows)

    print("Step 6: running BOTH audits (standard grounding + evidence-category discipline)...")
    from grounding_audit_v2 import audit_all
    retrieved_by_respondent = {rid: bundle[rid]["retrieved_parents_ranked"] for rid, _, _ in flat_sample}
    grounding_rows = audit_all(OUT_DIR / "api_recommendations_30.jsonl", respondents,
                                retrieved_by_respondent, excluded_ids, manifest_by_id)
    write_csv(OUT_DIR / "grounding_audit_30.csv", grounding_rows)
    from collections import Counter
    print(f"  Grounding audit: {dict(Counter(r['final_audit_status'] for r in grounding_rows))}")

    from evidence_category_discipline_audit import (load_policy, audit_recommendations, audit_declines)
    policy = load_policy()
    ecd_rows = audit_recommendations(OUT_DIR / "api_recommendations_30.jsonl", policy, "gpt-5-mini-validation-30")
    ecd_rows += audit_declines(OUT_DIR / "api_recommendations_30.jsonl", policy, respondents, "gpt-5-mini-validation-30")
    write_csv(OUT_DIR / "evidence_category_audit_30.csv", ecd_rows)
    print(f"  Category-discipline audit: {dict(Counter(r['status'] for r in ecd_rows))}")

    n_success = sum(1 for r in usage_rows if r["success"])
    print()
    print(f"Done. {n_success}/{len(usage_rows)} API calls succeeded with model={MODEL}.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
