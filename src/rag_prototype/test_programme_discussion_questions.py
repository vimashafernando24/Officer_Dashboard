"""Regression checks for purposeful programme discussion questions."""

import officer_recommendation_service as service


def candidate(
    *,
    name="Survey Field Assistant",
    attendance="Full Time",
    days="Weekdays",
    languages=None,
    qualification="National Vocational Qualification (NVQ)",
    exact_matches=None,
    selected_skills=None,
):
    return {
        "course_id": "COURSE-036",
        "course_name": name,
        "exact_selected_skill_matches": exact_matches or [],
        "selected_skills_in_those_sectors": {
            "Construction and building": selected_skills or ["Quantity Surveying"]
        },
        "structured_attributes": {
            "attendance_type": attendance,
            "attendance_days": days,
            "instruction_languages": languages or ["English"],
            "qualification_type": qualification,
        },
    }


assert service._programme_question_is_plain_language(
    "What kind of surveying work would you like this course to lead to?"
)
assert not service._programme_question_is_plain_language(
    "Does the retained cluster variable apply to you?"
)

matching_answers = {
    "q3": "Full-time, weekdays",
    "q4": "English",
    "q5": "Yes, I want a formal NVQ or qualification",
}
matching_questions = service._fallback_questions(candidate(), matching_answers)
matching_text = " ".join(matching_questions).lower()
assert len(matching_questions) == 2
assert "english" not in matching_text
assert "timetable" not in matching_text
assert "formal qualification" not in matching_text
assert "quantity surveying" in matching_text
assert "survey field assistant" in matching_text

mismatch_questions = service._fallback_questions(
    candidate(
        languages=["Sinhala"],
        qualification=service.candidate_selection.NOT_STATED,
    ),
    {
        "q3": "Part-time, weekends",
        "q4": "English",
        "q5": "Yes, I want a formal NVQ or qualification",
    },
)
mismatch_text = " ".join(mismatch_questions).lower()
assert len(mismatch_questions) == 3
assert "timetable" in mismatch_text
assert "taught in sinhala" in mismatch_text
assert "does not confirm a formal qualification" in mismatch_text

exact_questions = service._fallback_questions(
    candidate(
        exact_matches=[{
            "sector": "Construction and building",
            "skill": "Survey Field Assistant",
        }],
        selected_skills=["Survey Field Assistant"],
    ),
    matching_answers,
)
assert any("what kind of work" in question.lower() for question in exact_questions)
assert not any("would you also want to explore" in question.lower() for question in exact_questions)

print(
    "PROGRAMME QUESTION CHECK PASSED — valid LLM questions survive and fallbacks target "
    "real mismatches or programme-specific decisions"
)
