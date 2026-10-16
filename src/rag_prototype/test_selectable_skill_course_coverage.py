"""Regression: every selectable skill must exact-match at least one catalogue course.

The exact-skill guarantee (a member's selected skill always appears in the
programme options) depends on the skill name matching a course name in
course_matching_layer.csv. A misspelled catalogue name silently disables that
guarantee, as happened for "Human Recources Management". Note that
build_course_matching_layer.py copies source-document spellings, so
regenerating the layer without the corrections makes this test fail.
"""
import json

import new_person_candidate_selection as cs
from corpus_v2 import BASE
from profile_explorer_app import decode_new_person_intake

skills_by_area = json.loads(
    (BASE / "outputs/rag_new_person_intake_v1/q1_occupation_options_by_skill_area.json").read_text(encoding="utf-8")
)
course_names = {
    cs._strip_variant_suffix(row["rag_course_name"]).casefold() for row in cs.load_matching_layer()
}
unmatched = sorted(
    skill for skills in skills_by_area.values() for skill in skills if skill.casefold() not in course_names
)
assert not unmatched, f"Selectable skills with no exact-name catalogue course: {unmatched}"

# Every course-level sector addition must name a real catalogue course.
missing_extras = sorted(
    name for names in cs.SECTOR_EXTRA_COURSES.values() for name in names
    if cs.course_name_key(name) not in course_names
)
assert not missing_extras, f"SECTOR_EXTRA_COURSES entries not in the catalogue: {missing_extras}"

# The reported case: Finance sector + Human Resources Management must now make
# the HRM course a required (guaranteed) programme option.
BODY = {
    "branch": "E",
    "cluster_answers": {"past_edu_usefulness": "1", "plans_further_edu": "yes", "expected_highest_edu_e": "6"},
    "ideal_sectors": ["finance, banking, and insurance"],
    "skills_by_sector": {"finance, banking, and insurance": ["Human Resources Management"]},
    "q2": "Start my own business",
    "q3": "No strong preference",
    "q4": "English",
    "q5": "Not necessarily — I mainly want the practical skills",
}
_, _, sectors, context = decode_new_person_intake(BODY)
selection = cs.retrieve_sector_catalogue({
    "ideal_sectors": sectors,
    "preferred_skills_by_sector": context["preferred_skills_by_sector"],
    "q3_schedule": BODY["q3"],
    "q4_language": BODY["q4"],
    "q5_qualification": BODY["q5"],
})
required = {item["required_course_id"] for item in selection["required_selected_skill_coverage"]}
assert "COURSE-071" in required, f"HRM course not guaranteed: {selection['required_selected_skill_coverage']}"

total = sum(len(skills) for skills in skills_by_area.values())
print(f"SELECTABLE SKILL COVERAGE CHECK PASSED — {total}/{total} skills exact-match a course; HRM intake requires COURSE-071")
