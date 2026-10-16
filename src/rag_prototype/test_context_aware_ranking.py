"""Offline integration check for the context-aware ranking-only officer flow."""
from types import SimpleNamespace

import officer_recommendation_service as service
from new_person_candidate_selection import retrieve_sector_catalogue
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


CLAIM_CONTEXT = {
    "internal_skill_areas": [
        "ICT & Computing",
        "Automotive & Mechanical Engineering",
        "Electrical & Electronics",
    ],
    "selected_sectors": sectors,
    "selected_skills": officer_context["selected_skills"],
}

# A course's timetable remains valid catalogue information, but direct or
# inferred schedule preferences are unsupported when the intake says there is
# no preference (including when that answer is omitted).
unsupported_schedule_claims = [
    "Its part-time weekend delivery fits the member's weekend study preference.",
    "The member wants weekend classes.",
    "The weekend format works well for them.",
    "Part-time study is ideal for the participant.",
    "The participant requested weekday delivery.",
    "The member prefers weekend classes.",
    "The participant is preferring part-time study.",
    "The member chooses weekend classes.",
    "The participant needs part-time study.",
    "Weekend delivery suits the member.",
    "Full-time attendance matches their schedule preference.",
    "The member's preferred weekday format is available.",
    "The member’s preferred weekend format is available.",
    "The member did not request weekdays but wants weekend classes.",
]
for unsupported_claim in unsupported_schedule_claims:
    assert service._explanation_claim_violations(
        unsupported_claim,
        schedule_preference="No strong preference",
        **CLAIM_CONTEXT,
    ) == ["unsupported schedule-preference attribution"]
for missing_schedule in (None, "", "   "):
    assert service._explanation_claim_violations(
        "The member wants weekend classes.",
        schedule_preference=missing_schedule,
        **CLAIM_CONTEXT,
    ) == ["unsupported schedule-preference attribution"]
assert not service._explanation_claim_violations(
    "Its part-time weekend delivery fits the member's weekend study preference.",
    schedule_preference="Part-time, weekends",
    **CLAIM_CONTEXT,
)
for neutral_or_negated_claim in (
    "The course is offered on weekends.",
    "Part-time attendance is available.",
    "Weekend classes may be available.",
    "The member did not request weekend classes.",
    "The member didn't request weekend classes.",
    "The participant has no preference for weekend delivery.",
):
    assert not service._explanation_claim_violations(
        neutral_or_negated_claim,
        schedule_preference="No strong preference",
        **CLAIM_CONTEXT,
    )

# Internal catalogue areas are not user choices, while exact intake sectors
# and skills remain safe to attribute. An exact overlap is also respected.
assert service._explanation_claim_violations(
    "The member selected the Automotive & Mechanical Engineering area.",
    schedule_preference="No strong preference",
    **CLAIM_CONTEXT,
) == ["internal catalogue skill area attributed as a participant selection"]
for unsupported_area_claim in (
    "The member selected ICT & Computing.",
    "The participant requested Automotive & Mechanical Engineering.",
    "ICT & Computing is the category the member chose.",
    'The member selected "ICT & Computing".',
    "The participant requested ‘Automotive & Mechanical Engineering’.",
    "The member’s selected area is ICT & Computing.",
    "The member chose courses in ICT & Computing.",
    "The member selected an interest in ICT & Computing.",
):
    assert service._explanation_claim_violations(
        unsupported_area_claim,
        schedule_preference="No strong preference",
        **CLAIM_CONTEXT,
    ) == ["internal catalogue skill area attributed as a participant selection"]
assert not service._explanation_claim_violations(
    "The course is in the Automotive & Mechanical Engineering area.",
    schedule_preference="No strong preference",
    **CLAIM_CONTEXT,
)
for valid_compound_claim in (
    "The member selected Machinist, and the course is in Automotive & Mechanical Engineering.",
    "The member selected Computing, and the course is in ICT & Computing.",
    "The member selected the Machinist skill, which relates to the Automotive & Mechanical Engineering category.",
):
    assert not service._explanation_claim_violations(
        valid_compound_claim,
        schedule_preference="No strong preference",
        **CLAIM_CONTEXT,
    )
assert not service._explanation_claim_violations(
    "The member selected the Manufacturing or production sector.",
    schedule_preference="No strong preference",
    **CLAIM_CONTEXT,
)
assert not service._explanation_claim_violations(
    "The member selected the Machinist skill.",
    schedule_preference="No strong preference",
    **CLAIM_CONTEXT,
)
assert not service._explanation_claim_violations(
    "The member selected the ICT & Computing skill.",
    schedule_preference="No strong preference",
    internal_skill_areas=["ICT & Computing"],
    selected_sectors=sectors,
    selected_skills=[*officer_context["selected_skills"], "ICT & Computing"],
)
for cross_sentence_claim in (
    "The course is in ICT & Computing. This is what the member selected.",
    "The course belongs to ICT & Computing. That is the area the participant chose.",
    "The course is in ICT & Computing. This was requested by the member.",
):
    assert service._explanation_claim_violations(
        cross_sentence_claim,
        schedule_preference="No strong preference",
        **CLAIM_CONTEXT,
    ) == ["internal catalogue skill area attributed as a participant selection"]
assert not service._explanation_claim_violations(
    "The course is in ICT & Computing. This may provide useful context.",
    schedule_preference="No strong preference",
    **CLAIM_CONTEXT,
)
assert service._explanation_claim_violations(
    "Weekend delivery fits the member's study preference. "
    "The member selected ICT & Computing.",
    schedule_preference="No strong preference",
    **CLAIM_CONTEXT,
) == [
    "unsupported schedule-preference attribution",
    "internal catalogue skill area attributed as a participant selection",
]

missing_metadata_explanation = service._deterministic_grounded_explanation({
    "exact_selected_skill_matches": [],
    "matched_selected_sectors": [],
    "structured_attributes": {},
})
assert "governed catalogue option" in missing_metadata_explanation
assert "verified catalogue record" in missing_metadata_explanation
assert "preference" not in missing_metadata_explanation.lower()


# Exercise the full recommendation service with every required exact-skill
# course present. Explanation replacement must not change IDs, order, evidence,
# questions, mismatches, or initiate a coverage-repair call.
selection = retrieve_sector_catalogue({
    "ideal_sectors": sectors,
    "preferred_skills_by_sector": officer_context["preferred_skills_by_sector"],
    "q3_schedule": BODY["q3"],
    "q4_language": BODY["q4"],
    "q5_qualification": BODY["q5"],
})
candidates_by_id = {
    candidate["course_id"]: candidate for candidate in selection["candidates"]
}
required_coverage = selection["required_selected_skill_coverage"]
guarded_programmes = []
for index, coverage in enumerate(required_coverage, start=1):
    candidate = candidates_by_id[coverage["required_course_id"]]
    if index == 1:
        explanation = (
            "Its part-time weekend delivery fits the member's weekend study preference."
        )
    elif index == 2:
        explanation = (
            f"The member selected the {candidate['structured_attributes']['skill_area']} area."
        )
    else:
        explanation = (
            f"The member selected the {coverage['selected_skill']} skill under the "
            f"{coverage['sector']} sector."
        )
    guarded_programmes.append(SuggestedProgramme(
        rank=index,
        course_id=candidate["course_id"],
        course_name=candidate["course_name"],
        why_it_may_suit_this_user=explanation,
        user_facts_used=[UserFactCitation(
            question="Selected skill",
            answer=coverage["selected_skill"],
        )],
        course_facts_used=[CourseFactCitation(
            fact=candidate["course_name"],
            source_reference=candidate["course_id"],
        )],
        questions_to_discuss=[
            f"What work would you want {candidate['course_name']} training to lead to?",
            f"What preparation would help you begin {candidate['course_name']}?",
        ],
    ))

guarded_parsed = NewPersonRecommendationResponse(
    recommendation_status="RECOMMENDATIONS_AVAILABLE",
    suggested_programmes=guarded_programmes,
)
original_ids = [programme.course_id for programme in guarded_programmes]
original_evidence = [
    (
        programme.user_facts_used[0].model_dump(),
        programme.course_facts_used[0].model_dump(),
    )
    for programme in guarded_programmes
]
original_questions = [list(programme.questions_to_discuss) for programme in guarded_programmes]
guarded_call_count = 0


def guarded_fake_api(*_args, **_kwargs):
    global guarded_call_count
    guarded_call_count += 1
    return SimpleNamespace(
        success=True,
        parsed=guarded_parsed,
        total_tokens=100,
        input_tokens=80,
        output_tokens=20,
    )


service.call_new_person_recommendation_api = guarded_fake_api
try:
    guarded_response, guarded_status = service.generate_officer_briefing(
        person_id="offline-explanation-guard-check",
        branch=branch,
        cluster_answers=cluster_answers,
        ideal_sector_label=sectors,
        officer_context=officer_context,
        raw_body=BODY,
        question_map=load_survey_question_map(),
    )
finally:
    service.call_new_person_recommendation_api = original_api

assert guarded_status == 200, guarded_response
assert guarded_call_count == 1
guarded_output = guarded_response["suggested_programmes"]
assert [programme["course_id"] for programme in guarded_output] == original_ids
assert [programme["rank"] for programme in guarded_output] == list(
    range(1, len(original_ids) + 1)
)
assert {programme["course_id"] for programme in guarded_output} == {
    coverage["required_course_id"] for coverage in required_coverage
}
assert guarded_output[0]["why_it_may_suit_this_user"] != guarded_programmes[0].why_it_may_suit_this_user
assert guarded_output[1]["why_it_may_suit_this_user"] != guarded_programmes[1].why_it_may_suit_this_user
assert guarded_output[2]["why_it_may_suit_this_user"] == guarded_programmes[2].why_it_may_suit_this_user
for programme in guarded_output[:2]:
    assert not service._explanation_claim_violations(
        programme["why_it_may_suit_this_user"],
        schedule_preference=BODY["q3"],
        **CLAIM_CONTEXT,
    )
assert [programme["questions_to_discuss"] for programme in guarded_output] == original_questions
assert [
    programme["important_mismatches"] for programme in guarded_output
] == [
    service._candidate_constraints(candidates_by_id[course_id], BODY)
    for course_id in original_ids
]
assert original_evidence == [
    (
        programme.user_facts_used[0].model_dump(),
        programme.course_facts_used[0].model_dump(),
    )
    for programme in guarded_programmes
]
replacement_violations = [
    violation for violation in guarded_response["evidence_safeguard_violations"]
    if "replaced explanation" in violation
]
assert len(replacement_violations) == 2, replacement_violations
assert "unsupported schedule-preference attribution" in replacement_violations[0]
assert "internal catalogue skill area attributed as a participant selection" in replacement_violations[1]

print(
    "CONTEXT-AWARE RANKING CHECK PASSED — complete 40-course sector slice, "
    "mandatory exact-skill coverage, separate governed cluster-finding summary"
)
