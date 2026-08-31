"""Offline regression checks for multi-sector and per-sector skill intake."""
import json
from types import SimpleNamespace

from evidence_safeguards import check_explicit_answers_not_fabricated
from new_person_candidate_selection import (
    NOT_STATED,
    load_matching_layer,
    retrieve_sector_catalogue,
    select_candidates,
)
from new_person_context_pack import build_new_person_json_payload
from new_person_profile_context import build_profile_context
from profile_explorer_app import app, decode_new_person_intake


BODY = {
    "branch": "E",
    "cluster_answers": {
        "past_edu_usefulness": "2",
        "plans_further_edu": "yes",
        "expected_highest_edu_e": "6",
    },
    "ideal_sectors": [
        "information technology and communications",
        "manufacturing or production",
    ],
    "skills_by_sector": {
        "information technology and communications": ["Computer Hardware And Network Technician"],
        "manufacturing or production": ["Machinist", "Electrician"],
    },
    "q2": "Get a job",
    "q3": "No strong preference",
    "q4": "English",
    "q5": "Yes, I want a formal NVQ or qualification",
}


def expect_value_error(body, text):
    try:
        decode_new_person_intake(body)
    except ValueError as exc:
        assert text in str(exc), str(exc)
    else:
        raise AssertionError(f"Expected ValueError containing {text!r}")


branch, decoded_cluster_answers, sectors, context = decode_new_person_intake(BODY)
assert branch == "E"
assert sectors == ["Information technology and communications", "Manufacturing or production"]
assert context["selected_skills"] == [
    "Computer Hardware And Network Technician", "Machinist", "Electrician",
]

selection = select_candidates({
    "ideal_sectors": sectors,
    "selected_skills": context["selected_skills"],
    "q3_schedule": BODY["q3"],
    "q4_language": BODY["q4"],
    "q5_qualification": BODY["q5"],
})
assert set(selection["skill_areas"]) == {
    "ICT & Computing", "Automotive & Mechanical Engineering", "Electrical & Electronics",
}
selected_candidate_names = {candidate["course_name"] for candidate in selection["candidates"]}
assert any("Machinist" in name for name in selected_candidate_names)
assert any("Electrician" in name for name in selected_candidate_names)
assert any("Computer Hardware And Network Technician" in name for name in selected_candidate_names)

rich_retrieval = retrieve_sector_catalogue({
    "ideal_sectors": sectors,
    "preferred_skills_by_sector": context["preferred_skills_by_sector"],
})
assert len(rich_retrieval["candidates"]) > len(selection["candidates"])
assert all("score" not in candidate for candidate in rich_retrieval["candidates"])
assert set(rich_retrieval["sector_skill_areas"]) == set(sectors)
assert any(
    candidate["selected_skills_in_those_sectors"].get(
        "Manufacturing or production"
    ) == ["Machinist", "Electrician"]
    for candidate in rich_retrieval["candidates"]
)
assert {
    item["selected_skill"] for item in rich_retrieval["required_selected_skill_coverage"]
} == {"Computer Hardware And Network Technician", "Machinist", "Electrician"}
assert all(
    item["required_course_id"] in item["available_exact_course_ids"]
    for item in rich_retrieval["required_selected_skill_coverage"]
)

payload = build_new_person_json_payload(
    "multi-sector-test", "E", sectors,
    {
        "selected_skills": context["selected_skills"],
        "preferred_skills_by_sector": context["preferred_skills_by_sector"],
        "q2_reason": BODY["q2"], "q3_schedule": BODY["q3"],
        "q4_language": BODY["q4"], "q5_qualification": BODY["q5"],
    },
    [], {"skill_areas": selection["skill_areas"], "selected_skills": context["selected_skills"],
         "note": "", "candidates": []}, {},
)
assert payload["user"]["questionnaire_answers"]["preferred_sectors"] == sectors
assert payload["user"]["questionnaire_answers"]["preferred_skills_by_sector"] == context["preferred_skills_by_sector"]

fake_citations = [
    SimpleNamespace(question="Preferred sector", answer=sectors[0]),
    SimpleNamespace(question="Preferred skill", answer="Machinist"),
]
assert not check_explicit_answers_not_fabricated(
    fake_citations, payload["user"]["questionnaire_answers"], "multi-sector test",
)
nested_sector_skill_citation = [SimpleNamespace(
    question="preferred_skills_by_sector",
    answer=json.dumps({
        "Manufacturing or production": ["Machinist", "Electrician"],
    }),
)]
assert not check_explicit_answers_not_fabricated(
    nested_sector_skill_citation,
    payload["user"]["questionnaire_answers"],
    "nested multi-sector test",
)
invented_nested_citation = [SimpleNamespace(
    question="preferred_skills_by_sector",
    answer=json.dumps({"Manufacturing or production": ["Invented skill"]}),
)]
assert check_explicit_answers_not_fabricated(
    invented_nested_citation,
    payload["user"]["questionnaire_answers"],
    "invented nested multi-sector test",
)

with app.test_client() as client:
    preview_response = client.post("/api/new_person_evidence_preview", json=BODY)
    preview = preview_response.get_json()
assert preview_response.status_code == 200, preview
assert preview["branch"] == "E" and len(preview["assigned_profiles"]) == 1

expect_value_error({**BODY, "ideal_sectors": ["not sure", "manufacturing or production"]}, "cannot be combined")
expect_value_error({**BODY, "ideal_sectors": [
    "information technology and communications", "manufacturing or production",
    "construction and building", "creative, media, and arts",
]}, "no more than three sectors")
expect_value_error({**BODY, "skills_by_sector": {
    **BODY["skills_by_sector"],
    "manufacturing or production": [
        "Machinist", "Electrician", "Automobile Mechanic", "Mobile Phone Repair Technician",
    ],
}}, "no more than three skills")

unsure_body = {
    **BODY,
    "skills_by_sector": {
        "information technology and communications": ["Not sure yet"],
        "manufacturing or production": ["Not sure yet"],
    },
}
_, _, unsure_sectors, unsure_context = decode_new_person_intake(unsure_body)
assert unsure_context["preferred_skills_by_sector"] == {
    "Information technology and communications": [],
    "Manufacturing or production": [],
}
assert unsure_context["skill_preference_unsure_by_sector"] == {
    "Information technology and communications": True,
    "Manufacturing or production": True,
}
assert unsure_context["selected_skills"] == []
assert "Not sure yet" not in json.dumps(unsure_context["preferred_skills_by_sector"])
normal_profile_keys = [
    entry.profile_key
    for entry in build_profile_context(branch, decoded_cluster_answers, context)
]
unsure_profile_keys = [
    entry.profile_key
    for entry in build_profile_context(branch, decoded_cluster_answers, unsure_context)
]
assert unsure_profile_keys == normal_profile_keys

manufacturing_unsure_body = {
    **BODY,
    "ideal_sectors": ["manufacturing or production"],
    "skills_by_sector": {"manufacturing or production": ["Not sure yet"]},
}
with app.test_client() as client:
    unsure_preview_response = client.post(
        "/api/new_person_evidence_preview", json=manufacturing_unsure_body
    )
    unsure_preview = unsure_preview_response.get_json()
assert unsure_preview_response.status_code == 200, unsure_preview
assert unsure_preview["assigned_profiles"]
unsure_retrieval = retrieve_sector_catalogue({
    "ideal_sectors": unsure_sectors,
    "preferred_skills_by_sector": unsure_context["preferred_skills_by_sector"],
    "q3_schedule": unsure_body["q3"],
    "q4_language": unsure_body["q4"],
    "q5_qualification": unsure_body["q5"],
})
assert unsure_retrieval["candidates"]
assert not unsure_retrieval["required_selected_skill_coverage"]
assert all(
    candidate["course_id"] in {
        item["course_id"] for item in rich_retrieval["candidates"]
    }
    for candidate in unsure_retrieval["candidates"]
)
unsure_scored_selection = select_candidates({
    "ideal_sectors": unsure_sectors,
    "selected_skills": ["Not sure yet"],
    "q3_schedule": unsure_body["q3"],
    "q4_language": unsure_body["q4"],
    "q5_qualification": unsure_body["q5"],
})
assert unsure_scored_selection["candidates"]
assert all(
    "course-name match (+3)" not in candidate["score_breakdown"]
    for candidate in unsure_scored_selection["candidates"]
)

expect_value_error({**BODY, "skills_by_sector": {
    **BODY["skills_by_sector"],
    "manufacturing or production": ["Not sure yet", "Machinist"],
}}, "cannot be combined with specific skills")

whole_sector_unsure_body = {
    **BODY,
    "ideal_sectors": ["not sure"],
    "skills_by_sector": {},
    "q2": "Continue on to further education",
    "q3": "Part-time, weekends",
    "q4": "English",
    "q5": "Not necessarily — I mainly want the practical skills",
}
_, whole_unsure_cluster_answers, whole_unsure_sectors, whole_unsure_context = (
    decode_new_person_intake(whole_sector_unsure_body)
)
assert whole_unsure_context["preferred_skills_by_sector"] == {"Not sure": []}
assert whole_unsure_context["skill_preference_unsure_by_sector"] == {
    "Not sure": True,
}
whole_unsure_entries = build_profile_context(
    branch, whole_unsure_cluster_answers, whole_unsure_context
)
whole_unsure_profile_keys = [entry.profile_key for entry in whole_unsure_entries]
assert whole_unsure_profile_keys == normal_profile_keys
whole_unsure_retrieval = retrieve_sector_catalogue({
    "ideal_sectors": whole_unsure_sectors,
    "preferred_skills_by_sector": whole_unsure_context["preferred_skills_by_sector"],
    "q3_schedule": whole_sector_unsure_body["q3"],
    "q4_language": whole_sector_unsure_body["q4"],
    "q5_qualification": whole_sector_unsure_body["q5"],
})
expected_governed_ids = {
    row["rag_course_id"]
    for row in load_matching_layer()
    if row["skill_area"] != NOT_STATED
}
assert whole_unsure_retrieval["candidates"]
assert whole_unsure_retrieval["retrieval_method"] == (
    "complete verified catalogue fallback for unspecified sector"
)
assert not whole_unsure_retrieval["required_selected_skill_coverage"]
assert {
    candidate["course_id"] for candidate in whole_unsure_retrieval["candidates"]
} == expected_governed_ids
assert all(
    candidate["matched_selected_sectors"] == []
    for candidate in whole_unsure_retrieval["candidates"]
)
whole_unsure_payload = build_new_person_json_payload(
    "whole-sector-unsure-test",
    branch,
    whole_unsure_sectors,
    {
        "selected_skills": whole_unsure_context["selected_skills"],
        "preferred_skills_by_sector": whole_unsure_context["preferred_skills_by_sector"],
        "skill_preference_unsure_by_sector": (
            whole_unsure_context["skill_preference_unsure_by_sector"]
        ),
        "q2_reason": whole_sector_unsure_body["q2"],
        "q3_schedule": whole_sector_unsure_body["q3"],
        "q4_language": whole_sector_unsure_body["q4"],
        "q5_qualification": whole_sector_unsure_body["q5"],
    },
    whole_unsure_entries,
    {**whole_unsure_retrieval, "candidates": []},
    {},
)
assert whole_unsure_payload["user"]["questionnaire_answers"] == {
    "preferred_sectors": ["Not sure"],
    "preferred_skills_by_sector": {"Not sure": []},
    "skill_preference_unsure_by_sector": {"Not sure": True},
    "preferred_skills": [],
    "reason_for_training": "Continue on to further education",
    "schedule_preference": "Part-time, weekends",
    "language_preference": "English",
    "qualification_preference": "Not necessarily — I mainly want the practical skills",
}
assert whole_unsure_payload["assigned_branch_research_context"]

print("MULTI-SECTOR CHECKS PASSED — 2 sectors, 3 selected skills, governed union candidate pool")
