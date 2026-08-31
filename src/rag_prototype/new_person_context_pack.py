"""Build the single governed JSON payload sent to the officer-briefing LLM."""
from __future__ import annotations

import csv
import json

import context_pack_v2
from cluster_catalogue import metadata_for_profile
from corpus_v2 import BASE


FEATURE_MANIFEST_CSV = BASE / "outputs/nysc_survey_feature_manifest.csv"


RANKING_INSTRUCTIONS = """
You are the programme-matching analyst for a Youth Services Officer.

The input is a context-rich retrieval pack containing:
- the member's complete programme questionnaire and actual cluster-forming answers;
- every assigned profile dimension for the member's branch, its validated definition,
  common description, and all profiling findings explicitly retained in the final research;
- every verified catalogue course retrieved from the catalogue areas mapped to all
  sectors selected by the member.

Your only task is to rank the strongest programme options and explain why each one
matches this particular member, then provide the small set of programme-specific
questions requested below. Do not generate a research summary, an assignment
explanation, or separate generic advice.

Analyse the context holistically. Do not use a fixed points formula and do not treat
the order of selected sectors as a priority order. For every course, consider the
interaction between:
- each selected sector and only the skills the member selected under that sector;
- the member's reason for training, schedule, language, and qualification preferences;
- the course's verified subject, delivery, language, duration, and qualification facts;
- the member's actual cluster-forming answers across every assigned dimension; and
- the full set of retained findings for those assigned profiles when they genuinely
  help interpret the programme decision.

Personal answers and verified course facts are the strongest evidence. Cluster
descriptions and retained findings are historical group context: they can deepen or
qualify an explanation, but they cannot replace the member's answers and must never
be written as something the member personally said or experienced.

If skill_preference_unsure_by_sector marks a sector as true, the member supplied no
specific skill preference there. Do not ask them to choose a skill before recommending.
Distinguish the supplied candidate programmes using their other questionnaire answers
and the validated historical profile context, while keeping historical findings as
group context rather than personal facts.

If the member's only preferred sector is "Not sure", candidate_programmes contains the
governed full-catalogue fallback rather than a selected-sector slice. Still recommend
from those supplied candidates without asking the member to choose a sector first. Give
greater weight to their other questionnaire answers and relevant validated historical
profile context; the selected-sector mapping requirement does not apply in this case.

Actively evaluate every retained finding supplied for the assigned profiles against
every candidate programme. Use a finding as secondary recommendation evidence when it
meaningfully strengthens, weakens, differentiates, or adds useful context to a course
match. Relevant cluster evidence may affect the final ordering, including when two
courses fit the member's direct answers similarly. Do not ignore a useful finding just
because a direct sector or skill match already exists, but never force an unrelated
finding into a recommendation.

Whenever a retained finding affects a programme's ranking or explanation, cite it
exactly in profile_findings_used and write cluster_finding_summary. The summary is shown
inside a separate officer-facing "Cluster finding" box, so do not repeat the historical
tendency in why_it_may_suit_this_user. Write one or two short, conversational sentences:
begin with wording such as "People in the matched profile tended to..." and explain how
the tendency supported or qualified this programme decision. Do not include percentages,
sample sizes, statistical language, variable names, profile keys, internal codes, or JSON.
If no retained finding materially contributes, leave profile_findings_used empty, set
cluster_finding_summary to null, and base the explanation only on the member's answers
and verified course facts.

Build the final shortlist in two passes:

1. DIRECT-EVIDENCE PASS — first rank courses strongly supported by the member's selected
   sectors and sector-specific skills, stated goal, preferences, and verified course facts.
2. PROFILE-INFORMED PASS — if the first pass produces fewer than six defensible options,
   review every remaining retrieved course again using the assigned profile definitions,
   actual cluster-forming answers, and validated retained findings. Add a secondary option
   only when that context creates a meaningful, explainable reason to consider it.

A profile-informed option must still come from the catalogue areas mapped to a sector the
member selected and must not conflict with a known schedule, language, or qualification
preference. Cluster context may broaden the shortlist or break a close tie, but it must not
invent a new interest, claim personal circumstances the member did not report, or justify
an unrelated course. In why_it_may_suit_this_user, clearly call such a course a "related
option" rather than implying it directly matches a selected skill. Put the supporting
historical tendency only in cluster_finding_summary with exact citations.

Do not stop after finding a small number of obvious exact-name matches. Complete both
passes before returning the ordered shortlist, while still returning fewer than nine when
the remaining courses cannot be defended by personal facts, verified course facts, and
relevant validated cluster context together.

The catalogue_retrieval.required_selected_skill_coverage list is a mandatory coverage
contract, not a suggestion. Every required_course_id in that list MUST appear exactly once
in suggested_programmes. These are verified catalogue courses whose names exactly match a
skill the member explicitly selected. Keep them visible even when a language, schedule, or
qualification mismatch lowers their rank: explain the conflict honestly instead of silently
omitting the member's stated interest. After covering all required selected skills, use the
remaining places for the strongest related options. Never replace a required exact-skill
course with an unrelated course merely because the unrelated course matches more delivery
preferences.

For every recommended programme, write two or three questions_to_discuss for the officer
to use after opening the back of that programme card. Each question must be specific to
that course and resolve a real decision that remains open after reading the member answers
and verified course facts. Use the questions to:
- explore what work or next step the member wants this specific course to lead to;
- clarify a genuine mismatch between a member preference and a verified course fact;
- clarify missing course information such as entry requirements, location, cost, delivery,
  or qualification details; or
- when profile_findings_used is non-empty, respectfully check whether the historical
  group tendency in cluster_finding_summary actually applies to this member.

Never assume that a cluster tendency is true for the member. Ask rather than assert.
Do not mention clusters, profiles, research findings, percentages, statistics, variable
names, internal codes, or JSON in the questions. Avoid generic questions that could be
attached unchanged to every programme, and do not repeat the same question across all
recommended programmes. Do not ask the member to reconfirm a fact already answered in
the questionnaire when the course fact matches it. For example, if the member prefers
English and the course is taught in English, do not ask whether English works; if the
member wants a formal qualification and the course clearly provides one, do not ask
whether they want that qualification. Ask about language, schedule, or qualification only
when there is a mismatch, uncertainty, or meaningful choice still to resolve.

For an exact selected-skill course, treat the member's interest as known and ask about the
desired work outcome, readiness, or an unresolved practical issue. For a related course
that does not directly match the selected skill, clearly ask whether the member wants to
broaden from their named skill into this particular route. Write questions as natural
sentences the officer can ask in a real conversation, preferably addressing the member
directly rather than speaking about them in the third person.

Compare all retrieved courses before choosing the final list. A course matching a
skill selected under one sector must not be presented as matching a different sector
unless the verified course record supports that bridge. Do not favour a course merely
because it appears earlier in the input. The retrieval pack contains no suitability
score and its order is not a ranking.

Return at most nine distinct programmes, ordered from the strongest overall match to
the weakest defensible match. For each programme, write a concise, specific explanation
of two or three sentences. State the relevant member choices and the verified course
features that create the match. When a retained profile finding materially contributes,
keep its historical group tendency in cluster_finding_summary rather than presenting it
as a fact about this member.

Recommend only course_ids in candidate_programmes. Copy course identifiers, course
names, cited member answers, profile keys, variables, retained finding text, and course
facts exactly into their evidence fields. Cite a selected sector and its relevant skill
as separate scalar user-fact citations; never serialize a sector-to-skills object into
an answer citation. Do not invent eligibility, fees, location, entry requirements,
outcomes, or catalogue facts. If no retrieved programme has a defensible match, return
NO_DEFENSIBLE_RECOMMENDATION with a short reason.

Officer-facing explanations must use plain, natural language. Do not expose JSON field
names, internal variable names, profile keys, statistical methodology, or retrieval
terminology in the explanation.
""".strip()

# Compatibility alias for older local runners. The production officer flow uses the
# new ranking-only instructions above.
GOVERNANCE_INSTRUCTIONS = RANKING_INSTRUCTIONS


def _question_map() -> dict:
    with open(FEATURE_MANIFEST_CSV, newline="", encoding="utf-8-sig") as handle:
        return {row["variable"]: row for row in csv.DictReader(handle)}


def _as_distinct_strings(value) -> list[str]:
    if value is None:
        return []
    values = value if isinstance(value, (list, tuple, set)) else [value]
    result = []
    for item in values:
        text = str(item).strip()
        if text and text not in result:
            result.append(text)
    return result


def _profile_payload(entry, questions: dict) -> dict:
    metadata = metadata_for_profile(entry.profile_key)
    defining_answers = [
        {
            "variable": variable,
            "question_id": questions.get(variable, {}).get("question_id"),
            "question": questions.get(variable, {}).get("question_text") or variable,
            "user_answer": answer,
        }
        for variable, answer in entry.cluster_forming_answers.items()
    ]
    # The richer research pack receives the complete final-retained set for the
    # assigned profile. It still cannot see arbitrary survey statistics or any
    # explored/rejected profiling variable.
    retained_findings = (
        getattr(entry, "retained_evidence", None)
        or getattr(entry, "validated_evidence", [])
    )
    findings = [
        {
            "profile_key": entry.profile_key,
            "variable": finding["variable"],
            "label": finding["label"],
            "finding": finding["finding"],
            "interpretation_guard": finding["interpretation_guard"],
            "research_role": (
                "Final-retained profiling finding available for holistic programme interpretation."
            ),
            "provenance": finding["provenance"],
        }
        for finding in retained_findings
    ]
    return {
        **metadata,
        "validated_profile_definition": entry.profile_definition_text,
        "validated_cluster_defining_variables": defining_answers,
        "validated_profile_findings": findings,
    }


def build_new_person_json_payload(
    respondent_id: str,
    branch: str,
    ideal_sector: str | list[str],
    answers: dict,
    profile_entries: list,
    selection: dict,
    manifest_by_id: dict,
) -> dict:
    questions = _question_map()
    preferred_sectors = _as_distinct_strings(ideal_sector) or ["Not sure"]
    skills_by_sector = answers.get("preferred_skills_by_sector") or {}
    skill_preference_unsure_by_sector = (
        answers.get("skill_preference_unsure_by_sector") or {}
    )
    preferred_skills = _as_distinct_strings(
        answers.get("selected_skills") or answers.get("q1_occupation_focus")
    )
    if not preferred_skills and isinstance(skills_by_sector, dict):
        preferred_skills = _as_distinct_strings([
            skill for skills in skills_by_sector.values()
            for skill in (skills if isinstance(skills, list) else [skills])
        ])
    programme_answers = {
        "preferred_sectors": preferred_sectors,
        "preferred_skills_by_sector": skills_by_sector,
        "skill_preference_unsure_by_sector": skill_preference_unsure_by_sector,
        "preferred_skills": (
            preferred_skills
            if preferred_skills or skill_preference_unsure_by_sector
            else ["Not sure"]
        ),
        "reason_for_training": answers.get("q2_reason") or "Not stated",
        "schedule_preference": answers.get("q3_schedule") or "No strong preference",
        "language_preference": answers.get("q4_language") or "No strong preference",
        "qualification_preference": answers.get("q5_qualification") or "Not sure",
    }

    candidates = []
    for candidate in selection["candidates"]:
        candidates.append({
            "course_id": candidate["course_id"],
            "course_name": candidate["course_name"],
            "matched_selected_sectors": candidate.get("matched_selected_sectors", []),
            "selected_skills_in_those_sectors": candidate.get(
                "selected_skills_in_those_sectors", skills_by_sector,
            ),
            "exact_selected_skill_matches": candidate.get(
                "exact_selected_skill_matches", [],
            ),
            "structured_course_facts": candidate["structured_attributes"],
            "verified_course_document": context_pack_v2.load_course_doc(
                candidate["course_id"], manifest_by_id
            ),
        })

    return {
        "schema_version": "context_aware_programme_ranking_v3",
        "user": {
            "respondent_id": respondent_id,
            "assigned_branch": branch,
            "questionnaire_answers": programme_answers,
        },
        "constraints": {
            "sectors": programme_answers["preferred_sectors"],
            "skills": programme_answers["preferred_skills_by_sector"],
            "reason": programme_answers["reason_for_training"],
            "schedule": programme_answers["schedule_preference"],
            "language": programme_answers["language_preference"],
            "qualification": programme_answers["qualification_preference"],
        },
        "assigned_branch_research_context": [
            _profile_payload(entry, questions) for entry in profile_entries
        ],
        "catalogue_retrieval": {
            "method": selection.get(
                "retrieval_method", "complete selected-sector catalogue slice"
            ),
            "sector_skill_areas": selection.get("sector_skill_areas", {}),
            "skill_areas": selection["skill_areas"],
            "selected_skills_by_sector": skills_by_sector,
            "required_selected_skill_coverage": selection.get(
                "required_selected_skill_coverage", [],
            ),
            "note": selection["note"],
        },
        "candidate_programmes": candidates,
        "evidence_boundaries": {
            "user_fact": "Only values in user.questionnaire_answers and validated_cluster_defining_variables.",
            "cluster_context": (
                "Only the assigned profiles' final-retained findings are included. They are "
                "historical group context, never personal facts about the user."
            ),
            "course_fact": "Only facts inside the corresponding candidate programme record.",
        },
    }


def build_new_person_input_text(
    respondent_id: str,
    branch: str,
    ideal_sector: str | list[str],
    answers: dict,
    profile_entries: list,
    selection: dict,
    manifest_by_id: dict,
) -> str:
    payload = build_new_person_json_payload(
        respondent_id, branch, ideal_sector, answers,
        profile_entries, selection, manifest_by_id,
    )
    return json.dumps(payload, ensure_ascii=False, indent=2)
