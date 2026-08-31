"""Offline integration check for the context-aware ranking-only officer flow."""
from types import SimpleNamespace

import officer_recommendation_service as service
from new_person_recommendation_schema import (
    CourseFactCitation,
    NewPersonRecommendationResponse,
    ProfileFindingCitation,
    SuggestedProgramme,
    UserFactCitation,
)
from new_person_profile_context import build_profile_context
from profile_explorer_app import decode_new_person_intake, load_survey_question_map


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
        "information technology and communications": [
            "Computer Hardware And Network Technician",
        ],
        "manufacturing or production": ["Machinist", "Electrician"],
    },
    "q2": "Get a job",
    "q3": "No strong preference",
    "q4": "Sinhala",
    "q5": "Yes, I want a formal NVQ or qualification",
}


branch, cluster_answers, sectors, officer_context = decode_new_person_intake(BODY)
profile_entries = build_profile_context(branch, cluster_answers, officer_context)
retained_finding = profile_entries[0].retained_evidence[0]
cluster_finding_summary = (
    "People in the matched profile tended to have varied conditions for accepting work. "
    "This supports reviewing a practical programme with a clear route towards employment."
)
questions_to_discuss = [
    "Would a full-time weekday course fit your current responsibilities?",
    "Would Sinhala instruction help you participate confidently in the practical training?",
    "What conditions would make this route into employment workable for you?",
]

parsed = NewPersonRecommendationResponse(
    recommendation_status="RECOMMENDATIONS_AVAILABLE",
    suggested_programmes=[
        SuggestedProgramme(
            rank=1,
            course_id="COURSE-044",
            course_name="Machinist",
            why_it_may_suit_this_user=(
                "The member selected Manufacturing or production and Machinist, and wants "
                "a formal qualification. This course is a Machinist programme leading to an NVQ."
            ),
            user_facts_used=[
                UserFactCitation(
                    question="Selected skill",
                    answer="Machinist",
                ),
                UserFactCitation(
                    question="Qualification preference",
                    answer="Yes, I want a formal NVQ or qualification",
                ),
            ],
            course_facts_used=[
                CourseFactCitation(
                    fact="National Vocational Qualification (NVQ)",
                    source_reference="COURSE-044",
                ),
            ],
            profile_findings_used=[ProfileFindingCitation(
                profile_key=profile_entries[0].profile_key,
                variable=retained_finding["variable"],
                finding=retained_finding["finding"],
            )],
            cluster_finding_summary=cluster_finding_summary,
            questions_to_discuss=questions_to_discuss,
        ),
    ],
)


def fake_api(*_args, **_kwargs):
    return SimpleNamespace(
        success=True,
        parsed=parsed,
        total_tokens=100,
        input_tokens=80,
        output_tokens=20,
    )


original_api = service.call_new_person_recommendation_api
service.call_new_person_recommendation_api = fake_api
try:
    response, status = service.generate_officer_briefing(
        person_id="offline-context-aware-check",
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
assert response["candidate_programme_count"] == 40
programmes_by_id = {
    programme["course_id"]: programme for programme in response["suggested_programmes"]
}
assert {"COURSE-044", "COURSE-056", "COURSE-064"} <= set(programmes_by_id)
assert programmes_by_id["COURSE-044"]["why_it_may_suit_this_user"] == (
    parsed.suggested_programmes[0].why_it_may_suit_this_user
)
assert programmes_by_id["COURSE-044"]["cluster_finding_summary"] == cluster_finding_summary
assert programmes_by_id["COURSE-044"]["questions_to_discuss"] == questions_to_discuss
assert all(
    question.endswith("?")
    for question in programmes_by_id["COURSE-044"]["questions_to_discuss"]
)
assert "important_mismatches" in programmes_by_id["COURSE-044"]
assert "questions_to_discuss" not in response
assert any(
    "COURSE-056" in violation and "restored from governed catalogue facts" in violation
    for violation in response["evidence_safeguard_violations"]
)
assert any(
    "COURSE-064" in violation and "restored from governed catalogue facts" in violation
    for violation in response["evidence_safeguard_violations"]
)

print(
    "CONTEXT-AWARE RANKING CHECK PASSED — complete 40-course sector slice, "
    "mandatory exact-skill coverage, separate governed cluster-finding summary"
)
