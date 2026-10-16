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

# --- Card-level assessment: keep a card when most of its facts verify ---
def card(course_id, facts):
    return SuggestedProgramme(
        rank=1, course_id=course_id, course_name=candidates[course_id]["course_name"],
        why_it_may_suit_this_user="Placeholder.", user_facts_used=[UserFactCitation(question="q", answer="a")],
        course_facts_used=[CourseFactCitation(fact=f, source_reference=course_id) for f in facts],
        profile_findings_used=[], cluster_finding_summary=None, questions_to_discuss=["First?", "Second?"],
    )


def assess(course_id, facts):
    return service._assess_course_citations(
        card(course_id, facts), candidates[course_id], context_pack_v2.load_course_doc(course_id, manifest_by_id),
    )


cake = candidates["COURSE-051"]["structured_attributes"]
real_paraphrase = "Course focus: cake decoration practical training"   # captured from a live run
removal, verified, unverified = assess("COURSE-051", [
    f"attendance_type: {cake['attendance_type']}", f"attendance_days: {cake['attendance_days']}",
    f"duration_months: {cake['duration_months']}", real_paraphrase])
check("card with 3 verified facts and 1 real paraphrase is kept (3 verified, 1 unused)",
      not removal and (verified, unverified) == (3, 1))
removal, _, _ = assess("COURSE-051", [f"attendance_type: {cake['attendance_type']}", real_paraphrase, "Taught by celebrity chefs abroad"])
check("card with more unverified than verified facts is still removed", bool(removal))
removal, _, _ = assess("COURSE-051", [real_paraphrase])
check("card with no verified fact is still removed", bool(removal))
removal, _, _ = assess("COURSE-051", [f"attendance_type: {cake['attendance_type']}", f"attendance_days: {cake['attendance_days']}",
                                      "duration_months: 99"])
check("a wrong number removes the card even when other facts verify", any("number" in r for r in removal))
cookery_doc = context_pack_v2.load_course_doc("COURSE-007", manifest_by_id).lower()
near_verbatim = "Course content includes sweets and desserts, fairnaceous dishes, stock, sauces, soups and salad"  # live run
check("near-verbatim fact with plural differences now verifies",
      service._fact_is_grounded(near_verbatim, service._normalise_text(cookery_doc)))
check("explanation number check flags a number absent from the record",
      service._explanation_has_unverified_number("Runs for 99 months.", candidates["COURSE-051"],
                                                 context_pack_v2.load_course_doc("COURSE-051", manifest_by_id)))

failed = [name for name, ok in results if not ok]
for name, ok in results:
    print(f"{'PASS' if ok else 'FAIL'}  {name}")
if failed:
    raise SystemExit(f"COURSE FACT GROUNDING CHECK FAILED — {len(failed)} of {len(results)}")
print(f"COURSE FACT GROUNDING CHECK PASSED — {len(results)} checks")
