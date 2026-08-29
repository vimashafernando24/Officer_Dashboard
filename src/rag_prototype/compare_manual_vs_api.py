"""
Builds manual_vs_api_comparison.csv (Section R) once real API recommendations exist.

Computes the mechanically-answerable comparison points automatically (course_id
overlap, recommendation counts, NO_DEFENSIBLE_RECOMMENDATION agreement, whether any of
the 5 newly-recovered V2 courses appear) and leaves clearly-marked fields for the
qualitative judgement questions (unsupported assumptions, inference quality, profile
usage quality) that require reading both outputs side by side — this script does NOT
guess at those to avoid fabricating a comparison. Run this only after
api_test_recommendations.jsonl exists.

NOT run automatically by this task because no API key was available; provided ready
to execute once outputs/rag_recommendation_prototype_api/api_test_recommendations.jsonl
exists.
"""
import csv, json
from pathlib import Path
from corpus_v2 import BASE

MANUAL_JSONL = BASE / "outputs/rag_recommendation_prototype/test_recommendations.jsonl"
API_JSONL = BASE / "outputs/rag_recommendation_prototype_api/api_test_recommendations.jsonl"
OUT_CSV = BASE / "outputs/rag_recommendation_prototype_api/manual_vs_api_comparison.csv"

RECOVERED_COURSES = {"COURSE-002", "COURSE-004", "COURSE-005", "COURSE-046", "COURSE-068"}


def load_jsonl(path):
    out = {}
    with open(path, encoding="utf-8") as f:
        for line in f:
            rec = json.loads(line)
            out[rec["respondent_id"]] = rec
    return out


def main():
    if not API_JSONL.exists():
        raise SystemExit(
            f"{API_JSONL} does not exist yet — this script only runs after the "
            f"scripted OpenAI pipeline has produced real recommendations. Run "
            f"run_api_pipeline.py first (requires OPENAI_API_KEY)."
        )

    manual = load_jsonl(MANUAL_JSONL)
    api = load_jsonl(API_JSONL)

    rows = []
    for rid in manual:
        m = manual[rid]
        a = api.get(rid)
        if a is None:
            rows.append({"respondent_id": rid, "note": "no API record found — API call may have failed for this respondent"})
            continue

        manual_ids = {r["course_id"] for r in m.get("recommendations", [])}
        api_ids = {r["course_id"] for r in a.get("recommendations", [])}
        manual_no_def = m.get("no_defensible_recommendation", len(manual_ids) == 0)
        api_no_def = a.get("recommendation_status") == "NO_DEFENSIBLE_RECOMMENDATION"

        rows.append({
            "respondent_id": rid,
            "branch": m.get("branch"),
            "manual_course_ids": ";".join(sorted(manual_ids)),
            "api_course_ids": ";".join(sorted(api_ids)),
            "n_manual_recs": len(manual_ids),
            "n_api_recs": len(api_ids),
            "overlap_course_ids": ";".join(sorted(manual_ids & api_ids)),
            "n_overlap": len(manual_ids & api_ids),
            "api_only_course_ids": ";".join(sorted(api_ids - manual_ids)),
            "manual_only_course_ids": ";".join(sorted(manual_ids - api_ids)),
            "both_returned_no_defensible_recommendation": manual_no_def and api_no_def,
            "manual_no_defensible_recommendation": manual_no_def,
            "api_no_defensible_recommendation": api_no_def,
            "recovered_v2_course_recommended_by_api": ";".join(sorted(api_ids & RECOVERED_COURSES)) or "(none)",
            # Fields intentionally left for manual/qualitative completion — not guessed here:
            "q5_which_made_more_unsupported_assumptions": "REQUIRES MANUAL REVIEW OF BOTH OUTPUTS",
            "q6_which_used_inference_more_effectively": "REQUIRES MANUAL REVIEW OF BOTH OUTPUTS",
            "q7_which_used_profile_context_more_appropriately": "REQUIRES MANUAL REVIEW OF BOTH OUTPUTS",
            "q10_api_value_beyond_sector_filtering": "REQUIRES MANUAL REVIEW — see api_llm_added_value_analysis.csv",
        })

    with open(OUT_CSV, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        for r in rows:
            w.writerow(r)
    print(f"Wrote {len(rows)} comparison rows -> {OUT_CSV}")


if __name__ == "__main__":
    main()
