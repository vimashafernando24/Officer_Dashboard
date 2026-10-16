"""Regression: minimum of three options, best-fitting course variants and
course-level sector additions.

Offline: the recommendation API is replaced by a fake that returns scripted
model output, so every case runs through the real post-processing, evidence
checks, repair decision, exact-skill restoration and catalogue top-up.
"""
from types import SimpleNamespace

import officer_recommendation_service as service
from new_person_recommendation_schema import (
    CourseFactCitation,
    NewPersonRecommendationResponse,
    SuggestedProgramme,
    UserFactCitation,
)
from profile_explorer_app import decode_new_person_intake, load_survey_question_map

CLUSTER_ANSWERS = {"contract_type": "1", "job_security_12months": "3", "sector_formality": "5"}
results = []


def check(name, condition, detail=""):
    results.append((name, bool(condition), detail))


def ai_programme(rank, course_id, course_name, fact, sector_label):
    """A model programme that passes the existing evidence checks."""
    return SuggestedProgramme(
        rank=rank,
        course_id=course_id,
        course_name=course_name,
        why_it_may_suit_this_user="This course could be a practical option to discuss with the member.",
        user_facts_used=[UserFactCitation(question="Preferred sector", answer=sector_label)],
        course_facts_used=[CourseFactCitation(fact=fact, source_reference=course_id)],
        profile_findings_used=[],
        cluster_finding_summary=None,
        questions_to_discuss=[
            f"What kind of work would you like {course_name} to lead to?",
            f"Is there anything that could make it hard for you to start {course_name}?",
        ],
    )


def run(body, programmes, status="RECOMMENDATIONS_AVAILABLE", reason=None):
    calls = []

    def fake_api(*_args, **_kwargs):
        calls.append(1)
        return SimpleNamespace(
            success=True, total_tokens=1, input_tokens=1, output_tokens=0,
            parsed=NewPersonRecommendationResponse(
                recommendation_status=status, suggested_programmes=programmes,
                no_recommendation_reason=reason,
            ),
        )

    branch, cluster_answers, sectors, context = decode_new_person_intake(body)
    original = service.call_new_person_recommendation_api
    service.call_new_person_recommendation_api = fake_api
    try:
        response, status_code = service.generate_officer_briefing(
            person_id="minimum-options-regression", branch=branch, cluster_answers=cluster_answers,
            ideal_sector_label=sectors, officer_context=context, raw_body=body,
            question_map=load_survey_question_map(),
        )
    finally:
        service.call_new_person_recommendation_api = original
    return response, status_code, len(calls)


def body(sector, skills, q3="No strong preference", q4="English", q5="Not sure"):
    return {"branch": "F", "cluster_answers": CLUSTER_ANSWERS, "ideal_sectors": [sector],
            "skills_by_sector": {sector: skills}, "q2": "Get a job", "q3": q3, "q4": q4, "q5": q5}


def names(response):
    return [p["course_name"] for p in response["suggested_programmes"]]


def basis(response):
    return [p.get("selection_basis") for p in response["suggested_programmes"]]


# 1. The reported case: model returns only the Sinhala Secretary variant for an
#    English-preferring member who selected Human Resources Management.
FIN = "finance, banking, and insurance"
FIN_LABEL = "Finance, banking, and insurance"
resp, code, n_calls = run(body(FIN, ["Human Resources Management"], q5="Not necessarily — I mainly want the practical skills"),
                          [ai_programme(1, "COURSE-035", "Secretary – Secretarial Practices", "Sinhala", FIN_LABEL)])
programmes = resp["suggested_programmes"]
ids = [p["course_id"] for p in programmes]
check("reported case returns at least three options", len(programmes) >= 3, names(resp))
check("selected skill (Human Resources Management) is shown first", programmes[0]["course_id"] == "COURSE-071", ids)
check("Sinhala Secretary variant replaced by the English variant", "COURSE-082" in ids and "COURSE-035" not in ids, ids)
check("no course appears twice", len({n.casefold() for n in names(resp)}) == len(programmes), names(resp))
check("variant swap and top-up are labelled", "variant_adjusted" in basis(resp) and "catalogue_top_up" in basis(resp), basis(resp))

# 2. Hospitality has no English-taught course: the top-up still adds options,
#    each with a visible language-mismatch warning.
HOS = "hotels, restaurants, and hospitality"
HOS_LABEL = "Hotels, restaurants, and hospitality"
hos_candidates = {c["course_id"]: c for c in service.candidate_selection.retrieve_sector_catalogue(
    {"ideal_sectors": [HOS], "preferred_skills_by_sector": {}, "q4_language": "English"})["candidates"]}
first_id = sorted(hos_candidates)[0]
resp, code, n_calls = run(body(HOS, ["Not sure yet"]),
                          [ai_programme(1, first_id, hos_candidates[first_id]["course_name"],
                                        hos_candidates[first_id]["structured_attributes"]["attendance_type"], HOS_LABEL)])
programmes = resp["suggested_programmes"]
check("one AI option is topped up to three", len(programmes) == 3 and basis(resp) == ["ai_ranked", "catalogue_top_up", "catalogue_top_up"], basis(resp))
check("AI option stays first and its explanation is unchanged",
      programmes[0]["course_id"] == first_id
      and programmes[0]["why_it_may_suit_this_user"] == "This course could be a practical option to discuss with the member.")
check("added options in a no-English sector show the language-mismatch warning",
      all(any(m.startswith("Language mismatch") for m in p["important_mismatches"]) for p in programmes[1:]),
      [p["important_mismatches"] for p in programmes[1:]])
check("added options use rule-based text and plain discussion questions",
      all(p["why_it_may_suit_this_user"] and len(p["questions_to_discuss"]) >= 1 and p["cluster_finding_summary"] is None
          for p in programmes[1:]))

# 3. Model says nothing is defensible (no selected skill): three catalogue options.
resp, code, n_calls = run(body(HOS, ["Not sure yet"]), [], status="NO_DEFENSIBLE_RECOMMENDATION",
                          reason="No course fits the stated preferences.")
check("'no defensible recommendation' still yields three labelled catalogue options",
      resp["recommendation_status"] == "RECOMMENDATIONS_AVAILABLE" and basis(resp) == ["catalogue_top_up"] * 3, basis(resp))

# 4. Four valid AI options: nothing is added or reordered.
IT = "information technology and communications"
IT_LABEL = "Information technology and communications"
it_candidates = service.candidate_selection.retrieve_sector_catalogue(
    {"ideal_sectors": [IT], "preferred_skills_by_sector": {}})["candidates"]
seen, picks = set(), []
for c in sorted(it_candidates, key=lambda c: c["course_id"]):
    key = service.candidate_selection.course_name_key(c["course_name"])
    if key in seen or "english" not in c["structured_attributes"]["instruction_languages"].lower():
        continue
    seen.add(key); picks.append(c)
    if len(picks) == 4:
        break
model = [ai_programme(i + 1, c["course_id"], c["course_name"], "English", IT_LABEL) for i, c in enumerate(picks)]
resp, code, n_calls = run(body(IT, ["Not sure yet"]), model)
check("four valid AI options are returned unchanged, in order, with no additions",
      [p["course_id"] for p in resp["suggested_programmes"]] == [c["course_id"] for c in picks]
      and set(basis(resp)) == {"ai_ranked"}, basis(resp))

# 5. Wrong variant of a required exact-skill course: corrected without a paid repair call.
MAN = "manufacturing or production"
MAN_LABEL = "Manufacturing or production"
man = service.candidate_selection.retrieve_sector_catalogue(
    {"ideal_sectors": [MAN], "preferred_skills_by_sector": {MAN: ["Automobile Mechanic"]},
     "q3_schedule": "Part-time, weekends", "q4_language": "English"})
required_id = man["required_selected_skill_coverage"][0]["required_course_id"]  # English, part-time variant
other = next(c for c in man["candidates"]
             if service.candidate_selection.course_name_key(c["course_name"]) == "automobile mechanic"
             and c["course_id"] != required_id)  # Sinhala, full-time variant
resp, code, n_calls = run(body(MAN, ["Automobile Mechanic"], q3="Part-time, weekends"),
                          [ai_programme(1, other["course_id"], other["course_name"],
                                        other["structured_attributes"]["attendance_type"], MAN_LABEL)])
ids = [p["course_id"] for p in resp["suggested_programmes"]]
check("wrong variant of the selected course is swapped for the required variant",
      ids[0] == required_id == "COURSE-040" and other["course_id"] not in ids, ids)
check("no paid repair call when the model only chose the wrong variant", n_calls == 1, n_calls)
ENG = "education and teaching"

# 6. Course-level sector additions.
_, _, _, ctx = decode_new_person_intake(body(ENG, ["Preschool Teacher (Early Childhood Development)"]))
# The pipeline passes sector labels (as decode_new_person_intake returns them).
pre = service.candidate_selection.retrieve_sector_catalogue(
    {"ideal_sectors": ctx["preferred_sectors"], "preferred_skills_by_sector": ctx["preferred_skills_by_sector"]})
check("Preschool Teacher is selectable under Education and is a guaranteed option",
      any("Preschool" in c["course_name"] for c in pre["candidates"]) and pre["required_selected_skill_coverage"])
transport = service.candidate_selection.retrieve_sector_catalogue(
    {"ideal_sectors": ["transport, storage, and logistics"], "preferred_skills_by_sector": {}})
check("Store Management is a candidate for Transport, storage and logistics",
      any(c["course_name"] == "Store Management" for c in transport["candidates"]))

failed = [r for r in results if not r[1]]
for name, ok, detail in results:
    print(f"{'PASS' if ok else 'FAIL'}  {name}" + (f" — {detail}" if not ok else ""))
if failed:
    raise SystemExit(f"MINIMUM OPTIONS CHECK FAILED — {len(failed)} of {len(results)}")
print(f"MINIMUM OPTIONS CHECK PASSED — {len(results)} checks")
