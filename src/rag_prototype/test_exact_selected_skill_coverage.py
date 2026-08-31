"""Regression: exact selected skills cannot disappear from programme options."""
from types import SimpleNamespace

import officer_recommendation_service as service
from new_person_recommendation_schema import (
    CourseFactCitation,
    NewPersonRecommendationResponse,
    SuggestedProgramme,
    UserFactCitation,
)
from profile_explorer_app import decode_new_person_intake, load_survey_question_map


BODY = {
    "branch": "F",
    "cluster_answers": {
        "contract_type": "1",
        "job_security_12months": "3",
        "sector_formality": "5",
    },
    "ideal_sectors": [
        "hotels, restaurants, and hospitality",
        "manufacturing or production",
    ],
    "skills_by_sector": {
        "hotels, restaurants, and hospitality": ["Cake Decorator"],
        "manufacturing or production": ["Automobile Mechanic", "Aluminium Fabricator"],
    },
    "q2": "Build general skills, not sure about the next step yet",
    "q3": "Part-time, weekends",
    "q4": "English",
    "q5": "Yes, I want a formal NVQ or qualification",
}


# Simulate the failure that reached the UI: the model returns only an unrelated
# delivery-preference match and omits all three exact selected skills, even on repair.
parsed = NewPersonRecommendationResponse(
    recommendation_status="RECOMMENDATIONS_AVAILABLE",
    suggested_programmes=[SuggestedProgramme(
        rank=1,
        course_id="COURSE-081",
        course_name="Radio, TV & Allied Equipment Repairer",
        why_it_may_suit_this_user=(
            "This is a part-time weekend course taught in English, matching the member's "
            "delivery preferences as a related manufacturing option."
        ),
        user_facts_used=[UserFactCitation(question="Language preference", answer="English")],
        course_facts_used=[CourseFactCitation(fact="English", source_reference="COURSE-081")],
        profile_findings_used=[],
        cluster_finding_summary=None,
        questions_to_discuss=[
            "Would electronics repair interest the member despite not being a selected skill?",
            "Should the officer confirm whether this course awards a formal qualification?",
        ],
    )],
)


def fake_api(*_args, **_kwargs):
    return SimpleNamespace(
        success=True,
        parsed=parsed,
        total_tokens=100,
        input_tokens=80,
        output_tokens=20,
    )


branch, cluster_answers, sectors, officer_context = decode_new_person_intake(BODY)
original_api = service.call_new_person_recommendation_api
service.call_new_person_recommendation_api = fake_api
try:
    response, status = service.generate_officer_briefing(
        person_id="exact-selected-skill-regression",
        branch=branch,
        cluster_answers=cluster_answers,
        ideal_sector_label=sectors,
        officer_context=officer_context,
        raw_body=BODY,
        question_map=load_survey_question_map(),
    )
finally:
    service.call_new_person_recommendation_api = original_api

assert status == 200, response
names = [programme["course_name"] for programme in response["suggested_programmes"]]
assert names[:3] == ["Cake Decorator", "Automobile Mechanic", "Aluminium Fabricator"], names
assert "Radio, TV & Allied Equipment Repairer" in names

by_name = {programme["course_name"]: programme for programme in response["suggested_programmes"]}
assert any("Language mismatch" in item for item in by_name["Cake Decorator"]["important_mismatches"])
assert any("Qualification to confirm" in item for item in by_name["Cake Decorator"]["important_mismatches"])
assert any("Schedule mismatch" in item for item in by_name["Aluminium Fabricator"]["important_mismatches"])
assert all(len(programme["questions_to_discuss"]) >= 2 for programme in response["suggested_programmes"])

print("EXACT-SKILL COVERAGE CHECK PASSED — selected courses survive LLM omission with visible constraints")
