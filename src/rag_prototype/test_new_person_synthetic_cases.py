"""
TESTING — 9 synthetic new-person test cases for the new-person recommendation
architecture. Cluster-forming answers (§0's inputs — ordinary, already-existing
profiling-survey items) are borrowed from real respondents purely for valid
encoding; the actual scenario under test in each case is the ideal_sector/
Q1-Q5 override, which is fully synthetic. This is NOT the historical 362-person
experiment and does not touch it.

All 9 cases are run OFFLINE first (deterministic candidate selection + full
input-text construction — no API call, verifiable without spending anything).
A small subset is then run LIVE against gpt-5-mini, per the "use gpt-5-mini
only for the small final live test where actually necessary" instruction.
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from corpus_v2 import verify_corpus, BASE
from run_new_person_recommendation import load_donor_cluster_answers, run_one, format_human_readable

OUT_DIR = BASE / "outputs/rag_new_person_intake_v1"
CASES_DIR = OUT_DIR / "test_cases"

D_VARS = ["study_motivation_type", "autonomy_in_study", "competence_in_study_field",
          "relatedness_at_institution", "household_income", "household_size",
          "household_workers", "household_unemployed", "primary_earner_status",
          "primary_income_source", "edu_funding_source", "father_edu", "mother_edu",
          "expected_highest_edu_d", "institution_type", "worked_while_studying",
          "re_entered_education"]
F_VARS = ["contract_type", "job_security_12months", "sector_formality"]
G_VARS = ["household_income", "household_size", "household_workers", "household_unemployed",
          "primary_earner_status", "primary_income_source", "reason_not_in_labour_force",
          "ever_worked", "wants_to_work_future", "wants_further_edu"]

D_DONOR = "nysc-7f7d7d2a-1592-4a24-8512-5986c27ddd28"
D_DONOR_2 = "nysc-edaf37b2-0534-4518-affa-b7a02a23d465"
F_DONOR = "nysc-a8a47401-005b-42ef-b494-19fadefdd779"
G_DONOR = "nysc-31cab333-afc9-48c5-baec-8ba48e14defb"

CASES = [
    {
        "person_id": "test-01-direct-preference", "branch": "D",
        "cluster_answers": load_donor_cluster_answers(D_DONOR, D_VARS),
        "ideal_sector": "Information technology and communications",
        "q1_occupation_focus": "Information & Communication Technology Technician",
        "q2_reason": "Get a job", "q3_schedule": "Full-time, weekdays",
        "q4_language": "English", "q5_qualification": "Not necessarily",
        "case_description": "Very clear direct programme preference — expect a strong DIRECT_MATCH.",
        "live_test": True, "repeat": 3,
    },
    {
        "person_id": "test-02-broad-uncertain", "branch": "D",
        "cluster_answers": load_donor_cluster_answers(D_DONOR, D_VARS),
        "ideal_sector": "Not sure",
        "q1_occupation_focus": "Not sure", "q2_reason": "Build general skills, not sure about the next step yet",
        "q3_schedule": "No strong preference", "q4_language": "No strong preference",
        "q5_qualification": "Not sure",
        "case_description": "Broad/uncertain programme preference — no skill area determinable, "
                             "expect zero candidates / NO_DEFENSIBLE_RECOMMENDATION.",
        "live_test": False,
    },
    {
        "person_id": "test-03-conflict-with-profile", "branch": "F",
        "cluster_answers": load_donor_cluster_answers(F_DONOR, F_VARS),
        "ideal_sector": "Personal services (beauty, fitness, wellness)",
        "q1_occupation_focus": "Not sure",
        "q2_reason": "Start my own business",
        "q3_schedule": "Part-time, weekends", "q4_language": "Sinhala",
        "q5_qualification": "Not sure",
        "case_description": "Explicit self-employment/beauty-sector preference set against an "
                             "F_employment_security profile whose common tendency is toward stable, "
                             "formal permanent employment — tests that individual evidence wins, not the "
                             "group tendency.",
        "live_test": True,
    },
    {
        "person_id": "test-04-schedule-constraint", "branch": "D",
        "cluster_answers": load_donor_cluster_answers(D_DONOR_2, D_VARS),
        "ideal_sector": "Manufacturing or production",
        "q1_occupation_focus": "Automobile Mechanic",
        "q2_reason": "Get a job", "q3_schedule": "Part-time, weekends",
        "q4_language": "No strong preference", "q5_qualification": "Not sure",
        "case_description": "Schedule constraint — expect scoring to favor the part-time/weekend "
                             "delivery variant.",
        "live_test": False,
    },
    {
        "person_id": "test-05-qualification-preference", "branch": "D",
        "cluster_answers": load_donor_cluster_answers(D_DONOR, D_VARS),
        "ideal_sector": "Manufacturing or production",
        "q1_occupation_focus": "Not sure",
        "q2_reason": "Improve skills in my current job", "q3_schedule": "No strong preference",
        "q4_language": "No strong preference", "q5_qualification": "Yes, I want a formal NVQ or qualification",
        "case_description": "Qualification/NVQ preference — expect a soft score boost toward "
                             "NVQ-bearing courses, no hard filter.",
        "live_test": False,
    },
    {
        "person_id": "test-06-self-employment-goal", "branch": "G",
        "cluster_answers": load_donor_cluster_answers(G_DONOR, G_VARS),
        "ideal_sector": "Wholesale, retail, or repair",
        "q1_occupation_focus": "Not sure",
        "q2_reason": "Start my own business", "q3_schedule": "No strong preference",
        "q4_language": "No strong preference", "q5_qualification": "Not sure",
        "case_description": "Self-employment goal — governance discipline test: model must not invent "
                             "business-viability/affordability claims.",
        "live_test": True,
    },
    {
        "person_id": "test-07-catalogue-gap", "branch": "D",
        "cluster_answers": load_donor_cluster_answers(D_DONOR, D_VARS),
        "ideal_sector": "Public administration, government, and defence",
        "q1_occupation_focus": "Not sure",
        "q2_reason": "Get a job", "q3_schedule": "No strong preference",
        "q4_language": "No strong preference", "q5_qualification": "Not sure",
        "case_description": "Catalogue gap — ideal_sector has no SECTOR_BRIDGE mapping to any "
                             "skill_area; expect NO_DEFENSIBLE_RECOMMENDATION.",
        "live_test": True,
    },
    {
        "person_id": "test-08-profile-adds-value", "branch": "G",
        "cluster_answers": load_donor_cluster_answers(G_DONOR, G_VARS),
        "ideal_sector": "Wholesale, retail, or repair",
        "q1_occupation_focus": "Business Management",
        "q2_reason": "Start my own business", "q3_schedule": "No strong preference",
        "q4_language": "No strong preference", "q5_qualification": "Not sure",
        "case_description": "Profile context should genuinely add value: G_economic_role's "
                             "'predominantly self-income provider' pattern, if assigned, is consistent "
                             "with (reinforces) an explicit self-employment goal.",
        "live_test": True,
    },
    {
        "person_id": "test-09-profile-should-not-influence", "branch": "D",
        "cluster_answers": load_donor_cluster_answers(D_DONOR_2, D_VARS),
        "ideal_sector": "Information technology and communications",
        "q1_occupation_focus": "Computer Hardware Technician",
        "q2_reason": "Get a job", "q3_schedule": "Full-time, weekdays",
        "q4_language": "English", "q5_qualification": "Not sure",
        "case_description": "Crystal-clear direct preference where profile context (study "
                             "motivation/economic background) is orthogonal to course content — "
                             "expect profile_context_contribution.role = NOT_USED for most/all recs, "
                             "not forced in.",
        "live_test": False,
    },
]


def run_all(live: bool = True):
    CASES_DIR.mkdir(parents=True, exist_ok=True)
    manifest, _ = verify_corpus(verbose=False)
    manifest_by_id = {r["course_id"]: r for r in manifest}

    summary = []
    for case in CASES:
        n_calls = case.get("repeat", 1) if (live and case["live_test"]) else 1
        call_api = live and case["live_test"]
        results_for_case = []
        for i in range(n_calls):
            person_id = case["person_id"] if n_calls == 1 else f"{case['person_id']}-rep{i+1}"
            spec = {**case, "person_id": person_id}
            result = run_one(spec, manifest_by_id, call_api=call_api)
            results_for_case.append(result)

            report = format_human_readable(result)
            with open(CASES_DIR / f"{person_id}.md", "w", encoding="utf-8") as f:
                f.write(report)

            with open(CASES_DIR / f"{person_id}_input_text.txt", "w", encoding="utf-8") as f:
                f.write(result["input_text"])

        rec_sets = []
        for r in results_for_case:
            if r["api_result"] and r["api_result"].success:
                rec_sets.append(tuple(sorted(rc.course_id for rc in r["api_result"].parsed.recommendations)))
            elif r["api_result"] and not r["api_result"].success:
                rec_sets.append(("API_ERROR",))

        summary.append({
            "case": case["person_id"],
            "description": case["case_description"],
            "candidate_count": len(results_for_case[0]["selection"]["candidates"]),
            "skill_areas": results_for_case[0]["selection"]["skill_areas"],
            "called_api": call_api,
            "n_calls": n_calls,
            "recommendation_sets": rec_sets,
            "stable_across_repeats": len(set(rec_sets)) <= 1 if rec_sets else None,
            "status": (results_for_case[0]["api_result"].parsed.recommendation_status
                       if results_for_case[0]["api_result"] and results_for_case[0]["api_result"].success
                       else None),
        })
        print(f"[{case['person_id']}] candidates={summary[-1]['candidate_count']} "
              f"skill_areas={summary[-1]['skill_areas']} called_api={call_api} "
              f"status={summary[-1]['status']} stable={summary[-1]['stable_across_repeats']}")

    with open(CASES_DIR / "summary.json", "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False, default=str)
    print(f"\nWrote {len(CASES)} case reports to {CASES_DIR}")
    return summary


if __name__ == "__main__":
    live = "--offline" not in sys.argv
    run_all(live=live)
