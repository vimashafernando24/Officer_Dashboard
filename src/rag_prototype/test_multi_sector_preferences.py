"""Offline regression checks for multi-sector and per-sector skill intake."""
import json
from types import SimpleNamespace

from evidence_safeguards import check_explicit_answers_not_fabricated
from new_person_candidate_selection import retrieve_sector_catalogue, select_candidates
from new_person_context_pack import build_new_person_json_payload
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


branch, _, sectors, context = decode_new_person_intake(BODY)
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

print("MULTI-SECTOR CHECKS PASSED — 2 sectors, 3 selected skills, governed union candidate pool")
