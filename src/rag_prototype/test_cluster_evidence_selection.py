"""Offline and live regression tests for governed cluster evidence.

The offline suite validates all seven retained models / 17 profiles against
the final analysis and proves both gates:

    shown = explicitly retained in final analysis + useful current context

The optional live section makes one Branch E / Machinist API call.
"""
import glob
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import new_respondent_cluster_assignment as nrca
from evidence_safeguards import (
    build_allowed_evidence_index,
    check_explicit_answers_not_fabricated,
    filter_authorized_findings,
)
from new_person_profile_context import RAW_VARIABLES_BY_MODEL, build_profile_context
from profile_data_parser import parse_profile_document
from retained_cluster_evidence_registry import (
    CLUSTER_DEFINING_REGISTRY,
    PROFILE_RETAINED_VARIABLES,
    audit_profile_evidence,
    filter_retained_evidence_for_context,
    select_retained_evidence,
    validate_registry,
)
from branch_d_profile_dossiers import (
    APPROVED_PROFILING_VARIABLES_BY_MODEL,
    BRANCH_D_CLUSTER_CODES,
    SAVED_CLUSTER_NAMES,
    SAVED_CLUSTER_DESCRIPTIONS,
    OUTPUT_DIR as BRANCH_D_DOSSIER_DIR,
    build_branch_d_dossiers,
)


DOCS_DIR = Path(__file__).resolve().parents[2] / "outputs/rag_profile_knowledge/documents"
FAILURES = []

BRANCH_E_CONTEXT = {
    "ideal_sector": "Manufacturing or production",
    "q1_occupation_focus": "Machinist",
    "q2_reason": "Get a job",
    "q3_schedule": "No strong preference",
    "q4_language": "No strong preference",
    "q5_qualification": "Not sure",
}
BRANCH_E_CLUSTER_ANSWERS = {
    "past_edu_usefulness": {
        "value_code": "2",
        "value_label": "Somewhat useful — helps to some extent",
    },
    "plans_further_edu": {"value_code": "yes", "value_label": "Yes"},
    "expected_highest_edu_e": {"value_code": "6", "value_label": "Bachelor's degree"},
}


def check(condition, message):
    if not condition:
        FAILURES.append(message)
        print(f"  FAIL: {message}")


def section1_offline_tests():
    print("=== Section 1: offline governed-evidence tests ===")
    counts = validate_registry()
    check(counts == {"models": 7, "profiles": 17}, f"unexpected registry counts: {counts}")
    check(set(CLUSTER_DEFINING_REGISTRY) == set(nrca.MODEL_SPECS),
          "cluster-defining registry must cover exactly the seven assignment models")
    check(
        RAW_VARIABLES_BY_MODEL == {
            model: list(entry["variables"]) for model, entry in CLUSTER_DEFINING_REGISTRY.items()
        },
        "profile-context cluster-forming variables must come from the governed registry",
    )

    files = sorted(glob.glob(str(DOCS_DIR / "*.txt")))
    check(len(files) == 17, f"expected 17 profile documents, found {len(files)}")
    total_retained = 0
    for filepath in files:
        profile_key = Path(filepath).stem
        model_id = profile_key.rsplit("_p", 1)[0]
        parsed = parse_profile_document(Path(filepath).read_text(encoding="utf-8"))
        retained = select_retained_evidence(parsed)
        total_retained += len(retained)
        check(
            tuple(item["variable"] for item in retained) == PROFILE_RETAINED_VARIABLES[profile_key],
            f"{profile_key}: runtime retained list differs from explicit allowlist",
        )
        for item in retained:
            check(item["variable"] not in RAW_VARIABLES_BY_MODEL[model_id],
                  f"{profile_key}: own cluster-forming variable leaked as profile evidence")
            check("programme_relevant_findings" in item["provenance"]["retention_source"],
                  f"{profile_key}/{item['variable']}: missing final retention provenance")
    check(total_retained == 59, f"expected 59 profile-specific retained findings, found {total_retained}")
    print(f"  OK — {counts['models']} models, {counts['profiles']} profiles, {total_retained} exact retained findings.")

    print("\n  Branch E / Machinist eligibility audit")
    parsed_e = parse_profile_document(
        (DOCS_DIR / "E_learning_orientation_p2.txt").read_text(encoding="utf-8")
    )
    audit = audit_profile_evidence(parsed_e, BRANCH_E_CONTEXT)
    eligible_vars = [item["variable"] for item in audit["eligible"]]
    check(
        eligible_vars == [
            "job_acceptance_conditions", "network_helpfulness",
            "search_method_primary", "social_support_job_search",
        ],
        f"unexpected Branch E eligible findings: {eligible_vars}",
    )
    not_retained = {
        item["variable"] for item in audit["decisions"]
        if item["decision"] == "rejected_not_retained"
    }
    check(
        not_retained == {"household_size", "num_applications", "minimum_wage_band"},
        f"unexpected reported-but-not-retained Branch E set: {not_retained}",
    )
    for item in audit["eligible"]:
        print(f"    ELIGIBLE {item['variable']}: {item['context_reason']}")
    for item in audit["decisions"]:
        if item["decision"].startswith("rejected"):
            print(f"    REJECTED {item['variable']}: {item['reason']}")

    print("\n  Second gate: retained does not mean always shown")
    retained_e = select_retained_evidence(parsed_e)
    unrelated_context = {**BRANCH_E_CONTEXT, "q2_reason": "Improve skills in my current job"}
    eligible, rejected = filter_retained_evidence_for_context(
        "E_learning_orientation_p2", retained_e, unrelated_context,
    )
    check(eligible == [], "Branch E job-search findings should not survive an unrelated current-job context")
    check(len(rejected) == 4 and all(x["decision"] == "rejected_current_context" for x in rejected),
          "all four retained E findings should be explicitly context-rejected")
    print("    OK — all four retained findings were withheld when the current purpose did not match.")

    print("\n  Ordered-question display distributions")
    from profile_response_distributions import profile_response_distribution
    support_distribution = profile_response_distribution(
        "E_learning_orientation_p2", "social_support_job_search",
    )
    support_percentages = {
        item["value"]: item["percent"] for item in support_distribution["distribution"]
    }
    check(support_distribution["eligible_n"] == 16, "social-support chart denominator must be 16")
    check(
        support_percentages["Somewhat supported — I have some encouragement"] == 43.8,
        "social-support chart must expose the real labelled answer percentages",
    )
    acceptance_distribution = profile_response_distribution(
        "E_learning_orientation_p2", "job_acceptance_conditions",
    )
    check(
        len(acceptance_distribution["distribution"]) == 5
        and acceptance_distribution["eligible_n"] == 16,
        "job-acceptance chart must show all five real answer options",
    )
    print("    OK — ordered findings expose real answer labels and percentages, not median/IQR.")

    print("\n  Pre-briefing evidence preview")
    from profile_explorer_app import app
    client = app.test_client()
    preview_response = client.post("/api/new_person_evidence_preview", json={
        "branch": "E",
        "cluster_answers": {
            variable: answer["value_code"] for variable, answer in BRANCH_E_CLUSTER_ANSWERS.items()
        },
        "ideal_sector": "manufacturing or production",
        "q1": "Machinist",
        "q2": "Get a job",
        "q3": "No strong preference",
        "q4": "No strong preference",
        "q5": "Not sure",
    })
    preview = preview_response.get_json()
    check(preview_response.status_code == 200, f"evidence preview failed: {preview}")
    check(
        [profile["profile_key"] for profile in preview["assigned_profiles"]] == ["E_learning_orientation_p2"],
        "evidence preview must use the same retained profile assignment path",
    )
    check(
        all("common_description" in profile for profile in preview["assigned_profiles"]),
        "every assigned profile must expose its short governed description",
    )
    check(
        "eligible_findings" not in preview and "retained_findings" not in preview,
        "research findings must stay out of the frontend preview contract",
    )
    check(
        [branch["branch_id"] for branch in preview["research_tree"]] == list("DEFG"),
        "full research tree must expose all four retained branches for every respondent",
    )
    check(
        sum(
            len(model["profiles"])
            for branch in preview["research_tree"] for model in branch["models"]
        ) == 17,
        "full research tree must expose exactly all 17 retained profiles",
    )
    print("    OK — no-cost preview returns the assignment map without research-statistic payloads.")

    f_preview_response = client.post("/api/new_person_evidence_preview", json={
        "branch": "F",
        "cluster_answers": {
            "contract_type": "6",
            "job_security_12months": "2",
            "sector_formality": "3",
        },
        "ideal_sector": "wholesale, retail, or repair",
        "q1": "Secretary – Secretarial Practices",
        "q2": "Start my own business",
        "q3": "Part-time, weekends",
        "q4": "English",
        "q5": "Yes, I want a formal NVQ or qualification",
    })
    f_preview = f_preview_response.get_json()
    f_profile = f_preview["assigned_profiles"][0]
    check(f_profile["profile_key"] == "F_employment_security_p1", "expected temporary-employment profile")
    check(
        "retained_findings" not in f_profile and "eligible_findings" not in f_profile,
        "frontend profile tiles must not become evidence dumps",
    )
    print("    OK — profile assignment remains visible while its research evidence stays behind the scenes.")

    print("\n  Branch D governed JSON profile dossiers")
    from profile_explorer_app import VAR_LISTS, build_answers_for_model, load_all_rows
    values, labels = load_all_rows()
    branch_d_id = next(
        rid for rid, row in values.items()
        if row.get("branch") == "D"
        and row.get("branch_routing_source") == "translated_final_active_branch"
    )
    branch_d_answers = {}
    for model_id in nrca.BRANCH_MODELS["D"]:
        branch_d_answers.update(build_answers_for_model(branch_d_id, model_id, values, labels))
    branch_d_context = {
        "ideal_sector": labels[branch_d_id].get("ideal_sector") or "Not sure",
        "q1_occupation_focus": "Not sure / open to more than one",
        "q2_reason": "Get a job",
        "q3_schedule": "No strong preference",
        "q4_language": "No strong preference",
        "q5_qualification": "Not sure",
    }
    branch_d_entries = build_profile_context("D", branch_d_answers, branch_d_context)
    dossiers = build_branch_d_dossiers()
    check(len(branch_d_entries) == 3, "Branch D must assign one profile in each of three dimensions")
    check(len(dossiers) == 9, "expected one governed JSON dossier for each Branch D profile")
    check(len(list(BRANCH_D_DOSSIER_DIR.glob("D_*.json"))) == 9,
          "all nine generated Branch D dossier files must exist")
    total_approved = 0
    for profile_key, dossier in dossiers.items():
        model_id = dossier["profile"]["model_id"]
        approved = dossier["approved_post_cluster_findings"]
        total_approved += len(approved)
        check(
            dossier["profile"]["cluster_code"] == BRANCH_D_CLUSTER_CODES[profile_key]
            and dossier["profile"]["cluster_name"] == SAVED_CLUSTER_NAMES[profile_key]
            and "officer_display_name" not in dossier["profile"],
            f"{profile_key}: dossier must expose its stable cluster code and saved name",
        )
        check(
            dossier["cluster_definition"]["saved_officer_description"]
            == SAVED_CLUSTER_DESCRIPTIONS[profile_key],
            f"{profile_key}: dossier must contain its reviewed saved explanation",
        )
        check(
            tuple(item["variable"] for item in approved)
            == APPROVED_PROFILING_VARIABLES_BY_MODEL[model_id],
            f"{profile_key}: dossier approved findings differ from reviewed registry",
        )
        check(
            all(item["provenance"]["retention_source"].endswith(
                "column=strongest_non_clustering_characteristics"
            ) for item in approved),
            f"{profile_key}: every dossier finding must cite final approved profiling output",
        )
        check(
            {item["variable"] for item in approved if item["is_programme_relevant_subset"]}
            == set(PROFILE_RETAINED_VARIABLES[profile_key]),
            f"{profile_key}: broader approved findings and programme subset were conflated",
        )
    check(total_approved == 33, f"expected 33 approved Branch D profile findings, got {total_approved}")
    check(all(entry.research_dossier for entry in branch_d_entries),
          "each runtime Branch D assignment must load its exact JSON dossier")
    from new_person_context_pack import build_new_person_json_payload
    dossier_payload = build_new_person_json_payload(
        "branch-d-test", "D", branch_d_context["ideal_sector"], branch_d_context,
        branch_d_entries, {"skill_areas": [], "note": "", "candidates": []}, {},
    )
    dossier_prompt = json.dumps(dossier_payload)
    payload_assignments = {
        item["profile_key"]: item
        for item in dossier_payload["assigned_branch_research_context"]
    }
    for entry in branch_d_entries:
        check(entry.profile_key in dossier_prompt, "assigned dossier must reach the GPT context")
        payload_assignment = payload_assignments[entry.profile_key]
        check(bool(payload_assignment["validated_cluster_defining_variables"]),
              "runtime assignment answers must accompany the dossier")
        check(
            {
                (finding["variable"], finding["finding"])
                for finding in payload_assignment["validated_profile_findings"]
            }
            == {
                (finding["variable"], finding["finding"])
                for finding in entry.retained_evidence
            },
            "every final-retained finding for each assigned branch profile must reach the ranking LLM",
        )

    # Regression case for the UI problem that motivated neutral codes: this
    # response reports a government vocational institute but is still closest
    # overall to EDU-3 after all six education variables are considered.
    mismatch_id = "nysc-a8734961-39e9-42dc-87f3-5939365f535d"
    mismatch_answers = {}
    for model_id in nrca.BRANCH_MODELS["D"]:
        mismatch_answers.update(build_answers_for_model(
            mismatch_id, model_id, values, labels
        ))
    mismatch_answers["institution_type"] = {
        "value_code": "2",
        "value_label": "Government vocational/technical institute (NYSC, NAITA, VTA, etc.)",
    }
    mismatch_entries = build_profile_context("D", mismatch_answers, branch_d_context)
    mismatch_edu = next(
        entry for entry in mismatch_entries
        if entry.model_id == "D_educational_cultural"
    )
    check(mismatch_edu.profile_key == "D_educational_cultural_p3",
          "government-institute regression case should remain closest overall to EDU-3")
    mismatch_reference = next(
        item for item in mismatch_edu.research_dossier["cluster_definition"]["medoid_pattern"]
        if item["variable"] == "institution_type"
    )
    check(
        mismatch_reference["medoid_answer"]
        == "Private school or private degree-awarding institute",
        "EDU-3 dossier must preserve the conflicting private-institution medoid answer",
    )
    check(mismatch_edu.research_dossier["profile"]["cluster_code"] == "Cluster EDU-3",
          "the regression case must display a neutral code instead of a private-sector label")

    preview_body = {
        "branch": "D",
        "cluster_answers": {
            variable: str(answer["value_code"])
            for variable, answer in mismatch_answers.items()
        },
        "ideal_sector": "4",
        "q1": "Not sure / open to more than one",
        "q2": "Get a job",
        "q3": "No strong preference",
        "q4": "English",
        "q5": "Not sure",
    }
    from profile_explorer_app import app
    with app.test_client() as client:
        response = client.post("/api/new_person_evidence_preview", json=preview_body)
        preview = response.get_json()
    check(response.status_code == 200, "Branch D preview must succeed")
    check(len(preview["cluster_catalogue"]) == 9,
          "preview must expose saved explanations for assigned and unassigned Branch D clusters")
    check(all(item["common_description"] for item in preview["cluster_catalogue"]),
          "every Branch D cluster tile must have a saved explanation")
    check(all(item["cluster_name"] for item in preview["cluster_catalogue"]),
          "every Branch D cluster tile must have a saved descriptive name")
    check(all("reference_pattern" not in item for item in preview["cluster_catalogue"]),
          "technical reference-pattern details must stay out of the officer UI payload")
    check(all("assignment_comparison" not in profile for profile in preview["assigned_profiles"]),
          "confusing youth-versus-reference comparison must not return to the UI")
    branch_e_entries = build_profile_context("E", BRANCH_E_CLUSTER_ANSWERS, BRANCH_E_CONTEXT)
    check(all(entry.research_dossier is None for entry in branch_e_entries),
          "unreviewed branches must not receive Branch D dossiers")
    print(
        "    OK — 9 dossiers preserve 33 approved findings, their programme subset, assignment "
        "evidence, and exact provenance."
    )

    print("\n  Research retrieval isolation: GPT receives the complete final-retained registry set")
    entries = build_profile_context("E", BRANCH_E_CLUSTER_ANSWERS, BRANCH_E_CONTEXT)
    check([e.profile_key for e in entries] == ["E_learning_orientation_p2"],
          f"expected Branch E profile 2, got {[e.profile_key for e in entries]}")
    from new_person_context_pack import build_new_person_json_payload
    profile_payload = build_new_person_json_payload(
        "branch-e-test", "E", BRANCH_E_CONTEXT["ideal_sector"], BRANCH_E_CONTEXT,
        entries, {"skill_areas": [], "note": "", "candidates": []}, {},
    )
    profile_prompt = json.dumps(profile_payload)
    for variable in PROFILE_RETAINED_VARIABLES[entries[0].profile_key]:
        check(f'"variable": "{variable}"' in profile_prompt, f"retained variable {variable} missing from prompt")
    check(
        "joint-highest tie at 36.4%" in profile_prompt
        and "Attending job fairs; Online job ads" in profile_prompt,
        "Branch E search-method evidence must carry its within-profile tie guard into the GPT prompt",
    )
    for variable in ("household_size", "num_applications", "minimum_wage_band"):
        check(variable not in profile_prompt, f"rejected variable {variable} leaked into GPT prompt")
    check("DIRECT_GROUP_DISTRIBUTIONS" not in profile_prompt,
          "full distribution section must never be included in the GPT profile context")
    print("    OK — all final-retained findings are present; over-admitted variables and raw distributions are absent.")

    print("\n  Exact-text authorization safeguard")

    class FakeFinding:
        def __init__(self, profile_key, variable, finding):
            self.profile_key, self.variable, self.finding = profile_key, variable, finding

    allowed_index = build_allowed_evidence_index(entries)
    allowed = entries[0].validated_evidence[0]
    exact = FakeFinding(entries[0].profile_key, allowed["variable"], allowed["finding"])
    invented = FakeFinding(entries[0].profile_key, allowed["variable"], "Invented statistic")
    kept, violations = filter_authorized_findings([exact, invented], allowed_index, "test")
    check(kept == [exact], "exact retained finding should be kept")
    check(len(violations) == 1 and "exact finding text" in violations[0],
          "same variable with invented text must be rejected")
    print("    OK — authorization requires profile + variable + exact final finding text.")

    print("\n  Intake-answer/history separation safeguard")

    class FakeAnswerCitation:
        def __init__(self, question, answer):
            self.question, self.answer = question, answer

    collected = {
        "ideal_sector": "Manufacturing or production", "q1": "Machinist", "q2": "Get a job",
        "q3": "No strong preference", "q4": "No strong preference", "q5": "Not sure",
    }
    real = FakeAnswerCitation("Q1", "Machinist")
    fabricated = FakeAnswerCitation("Household size", "4")
    violations = check_explicit_answers_not_fabricated([real, fabricated], collected, "test")
    check(len(violations) == 1 and "Household size" in violations[0],
          "historical profile statistic must not become a member intake answer")
    print("    OK — a historical cluster characteristic cannot be cited as this member's answer.")


def section2_live_integration_test():
    print("\n=== Section 2: live integration test (1 API call) — Branch E, Machinist ===")
    from corpus_v2 import verify_corpus
    from run_new_person_recommendation import run_one

    manifest, _ = verify_corpus(verbose=False)
    manifest_by_id = {row["course_id"]: row for row in manifest}
    spec = {
        "person_id": "test-branch-e-machinist",
        "branch": "E",
        "cluster_answers": BRANCH_E_CLUSTER_ANSWERS,
        **BRANCH_E_CONTEXT,
        "case_description": "Branch E / Machinist governed-evidence regression test.",
    }
    result = run_one(spec, manifest_by_id, call_api=True)
    api_result = result["api_result"]
    check(api_result.success, f"API call failed: {api_result.error_message if api_result else 'no result'}")
    if not api_result.success:
        return

    entries = result["profile_entries"]
    allowed_index = build_allowed_evidence_index(entries)
    for entry in entries:
        print(
            f"  {entry.profile_key}: retained={len(entry.retained_evidence)}, "
            f"eligible_now={len(entry.validated_evidence)}, rejected_now={len(entry.rejected_evidence)}"
        )

    parsed = api_result.parsed
    all_findings = []
    if parsed.about_people_like_you:
        all_findings.extend(parsed.about_people_like_you.supporting_findings)
    for recommendation in parsed.recommendations:
        all_findings.extend(recommendation.profile_context_contribution.contributing_findings)
    for prompt in parsed.officer_discussion_prompts:
        all_findings.extend(prompt.supporting_findings)

    kept, violations = filter_authorized_findings(all_findings, allowed_index, "live test")
    check(len(violations) == 0, f"unauthorized cluster citations in live response: {violations}")
    check(len(kept) == len(all_findings), "every live citation must be exactly authorized")
    forbidden = {"household_size", "num_applications", "minimum_wage_band"}
    leaked = [finding.variable for finding in all_findings if finding.variable in forbidden]
    check(not leaked, f"reported-but-not-retained Branch E variables leaked into live output: {leaked}")

    misattributed = [
        finding for finding in all_findings
        if " you " in f" {finding.finding.lower()} "
        or finding.finding.lower().startswith("you ")
        or "your " in finding.finding.lower()
    ]
    check(not misattributed, "historical cluster findings used individual you/your framing")
    print(f"  OK — {len(all_findings)} cited finding(s), all exact registry matches; no rejected variable leaked.")


if __name__ == "__main__":
    section1_offline_tests()
    if "--offline" not in sys.argv:
        section2_live_integration_test()

    print()
    if FAILURES:
        print(f"{len(FAILURES)} FAILURE(S):")
        for failure in FAILURES:
            print(f"  - {failure}")
        sys.exit(1)
    print("ALL CHECKS PASSED")
