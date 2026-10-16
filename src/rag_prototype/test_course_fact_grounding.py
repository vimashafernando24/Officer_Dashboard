"""Regression: course-fact grounding accepts copied catalogue field labels but
still rejects any value that the governed course record does not support.

Uses real catalogue records and course documents; no OpenAI calls.
"""
import corpus_v2
import context_pack_v2
import new_person_candidate_selection as cs
import officer_recommendation_service as service
from new_person_recommendation_schema import CourseFactCitation, SuggestedProgramme, UserFactCitation

manifest, _ = corpus_v2.verify_corpus(verbose=False)
manifest_by_id = {row["course_id"]: row for row in manifest}
candidates = {
    c["course_id"]: c
    for c in cs.retrieve_sector_catalogue({"ideal_sectors": ["not sure"], "preferred_skills_by_sector": {}})["candidates"]
}
results = []


def grounded(course_id, fact):
    programme = SuggestedProgramme(
        rank=1, course_id=course_id, course_name=candidates[course_id]["course_name"],
        why_it_may_suit_this_user="Placeholder.", user_facts_used=[UserFactCitation(question="q", answer="a")],
        course_facts_used=[CourseFactCitation(fact=fact, source_reference=course_id)],
        profile_findings_used=[], cluster_finding_summary=None, questions_to_discuss=["First question?", "Second question?"],
    )
    violations = service._course_citations_are_exact(
        programme, candidates[course_id], context_pack_v2.load_course_doc(course_id, manifest_by_id),
    )
    return not violations


def check(name, condition):
    results.append((name, bool(condition)))


# The live failure: Preschool Teacher (COURSE-041) is taught in English.
attrs = candidates["COURSE-041"]["structured_attributes"]
assert "English" in attrs["instruction_languages"], attrs
check("labelled fact 'Instruction languages: [\"English\"]' is accepted", grounded("COURSE-041", 'Instruction languages: ["English"]'))
check("snake_case label 'instruction_languages: English' is accepted", grounded("COURSE-041", "instruction_languages: English"))
check("labelled attendance fact is accepted", grounded("COURSE-041", f"Attendance type: {attrs['attendance_type']}"))
check("unlabelled value is still accepted", grounded("COURSE-041", attrs["attendance_type"]))

# Values the record does not support are still rejected, label or not.
check("wrong language behind a label is rejected", not grounded("COURSE-041", 'Instruction languages: ["Tamil"]'))
check("wrong duration number behind a label is rejected", not grounded("COURSE-041", "Duration months: 99"))
check("a bare label with no value is rejected", not grounded("COURSE-041", "Instruction languages:"))
unstated = next(
    cid for cid, c in sorted(candidates.items())
    if c["structured_attributes"]["qualification_type"] == cs.NOT_STATED
    and "nvq" not in context_pack_v2.load_course_doc(cid, manifest_by_id).lower()
)
check(f"unsupported NVQ claim behind a label is rejected ({unstated})", not grounded(unstated, "Qualification type: NVQ Level 4"))

failed = [name for name, ok in results if not ok]
for name, ok in results:
    print(f"{'PASS' if ok else 'FAIL'}  {name}")
if failed:
    raise SystemExit(f"COURSE FACT GROUNDING CHECK FAILED — {len(failed)} of {len(results)}")
print(f"COURSE FACT GROUNDING CHECK PASSED — {len(results)} checks")
