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
matches this particular member. Do not generate follow-up questions, a research
summary, an assignment explanation, or separate generic advice.

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

Compare all retrieved courses before choosing the final list. A course matching a
skill selected under one sector must not be presented as matching a different sector
unless the verified course record supports that bridge. Do not favour a course merely
because it appears earlier in the input. The retrieval pack contains no suitability
score and its order is not a ranking.

Return at most four distinct programmes, ordered from the strongest overall match to
the weakest defensible match. For each programme, write a concise, specific explanation
of two or three sentences. State the relevant member choices and the verified course
features that create the match. When a retained profile finding materially contributes,
phrase it explicitly as a tendency among people in the matched profile, not as a fact
about this member.

Recommend only course_ids in candidate_programmes. Copy course identifiers, course
names, cited member answers, profile keys, variables, retained finding text, and course
facts exactly into their evidence fields. Cite a selected sector and its relevant skill
as separate scalar user-fact citations; never serialize a sector-to-skills object into
an answer citation. Do not invent eligibility, fees, location,
entry requirements, outcomes, or catalogue facts. If no retrieved programme has a
defensible match, return NO_DEFENSIBLE_RECOMMENDATION with a short reason.

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
        "preferred_skills": preferred_skills or ["Not sure"],
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
