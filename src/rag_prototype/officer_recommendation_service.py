"""End-to-end service for the simplified officer briefing response."""
from __future__ import annotations

import json
import logging
import re

from cluster_catalogue import catalogue_for_branch, metadata_for_profile
import context_pack_v2
from corpus_v2 import verify_corpus
from env_config import get_production_model, verify_production_model
from evidence_safeguards import (
    check_explicit_answers_not_fabricated,
    filter_authorized_findings,
)
import new_person_candidate_selection as candidate_selection
import new_person_context_pack as context_pack
import new_person_profile_context as profile_context
from new_person_openai_client import call_new_person_recommendation_api
from new_person_recommendation_schema import NewPersonRecommendationResponse


LOGGER = logging.getLogger(__name__)


def _finding_json(finding) -> dict:
    return {
        "profile_key": finding.profile_key,
        "variable": finding.variable,
        "finding": finding.finding,
    }


def _normalise_text(value: str) -> str:
    return " ".join(str(value).lower().split())


_FACT_FILLER_WORDS = {
    "a", "an", "and", "are", "as", "at", "be", "by", "course", "for", "from",
    "has", "in", "is", "it", "its", "of", "on", "or", "programme", "that", "the",
    "this", "to", "with",
}


def _fact_is_grounded(fact: str, allowed_text: str) -> bool:
    fact_tokens = {
        token for token in re.findall(r"[\w&+-]+", _normalise_text(fact))
        if token not in _FACT_FILLER_WORDS
    }
    allowed_tokens = set(re.findall(r"[\w&+-]+", allowed_text))
    if not fact_tokens:
        return False
    numbers = re.findall(r"\d+(?:[.,]\d+)?", fact)
    if any(number not in allowed_text for number in numbers):
        return False
    return len(fact_tokens & allowed_tokens) / len(fact_tokens) >= 0.65


def _course_citations_are_exact(programme, candidate: dict, course_document: str) -> list[str]:
    """Require every cited course claim to be traceable to its governed candidate record."""
    violations = []
    allowed_text = _normalise_text(json.dumps(candidate, ensure_ascii=False) + " " + course_document)
    for citation in programme.course_facts_used:
        if citation.source_reference != programme.course_id:
            violations.append(
                f"programme {programme.course_id}: course fact used a different source_reference."
            )
        if not _fact_is_grounded(citation.fact, allowed_text):
            violations.append(
                f"programme {programme.course_id}: course fact was not grounded in the governed course record."
            )
    if not programme.course_facts_used:
        violations.append(
            f"programme {programme.course_id}: removed because it cited no governed course fact."
        )
    return violations


def _has_clear_group_context_wording(value: str) -> bool:
    lowered = value.lower()
    return bool(
        re.search(r"\b(people|members|young people|youth)\b", lowered)
        and re.search(r"\b(matched profile|profile|group)\b", lowered)
    )


def _cluster_summary_is_plain_language(value: str) -> bool:
    lowered = value.lower()
    forbidden = (
        "profile_key", "variable", "effect size", "p-value", "p value",
        "median", "iqr", "sample size", "statistically", "significance",
        "retained finding", "validated finding", "json",
    )
    return bool(
        value.strip()
        and len(value) <= 420
        and _has_clear_group_context_wording(value)
        and not re.search(r"[%{}\[\]_]|\b\d+(?:[.,]\d+)?\b", value)
        and not re.search(r"\b(you|your|yours)\b", lowered)
        and not any(marker in lowered for marker in forbidden)
    )


def _programme_question_is_plain_language(value: str) -> bool:
    lowered = value.lower()
    forbidden = (
        "cluster", "profile", "profile_key", "variable", "effect size",
        "p-value", "p value", "median", "iqr", "statistically",
        "retained finding", "validated finding", "json",
    )
    return bool(
        value.strip()
        and len(value) <= 260
        and value.rstrip().endswith("?")
        and not re.search(r"[%{}\[\]_]", value)
        and not any(marker in lowered for marker in forbidden)
    )


def _as_language_list(value) -> list[str]:
    if value in (None, "", candidate_selection.NOT_STATED):
        return []
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]
    try:
        parsed = json.loads(str(value))
    except (TypeError, json.JSONDecodeError):
        parsed = None
    if isinstance(parsed, list):
        return [str(item).strip() for item in parsed if str(item).strip()]
    return [item.strip() for item in re.split(r"[/,]", str(value)) if item.strip()]


def _candidate_constraints(candidate: dict, raw_body: dict) -> list[str]:
    """Return user-visible, mechanically verified mismatches and uncertainties."""
    attributes = candidate["structured_attributes"]
    constraints = []

    preferred_schedule = str(raw_body.get("q3") or "").lower()
    attendance = str(attributes.get("attendance_type") or "")
    days = str(attributes.get("attendance_days") or "")
    if preferred_schedule and "no strong preference" not in preferred_schedule:
        wants_part_time = "part-time" in preferred_schedule or "weekend" in preferred_schedule
        actual_part_time = "part time" in attendance.lower() or "weekend" in days.lower()
        attendance_known = attendance not in ("", candidate_selection.NOT_STATED)
        if attendance_known and wants_part_time != actual_part_time:
            constraints.append(
                f"Schedule mismatch: the catalogue lists {attendance.lower()}"
                + (f" on {days.lower()}" if days not in ("", candidate_selection.NOT_STATED) else "")
                + "."
            )

    preferred_language = str(raw_body.get("q4") or "").strip()
    languages = _as_language_list(attributes.get("instruction_languages"))
    if preferred_language and "no strong preference" not in preferred_language.lower() and languages:
        if preferred_language.casefold() not in {language.casefold() for language in languages}:
            constraints.append(
                f"Language mismatch: the member prefers {preferred_language}, but the catalogue lists "
                + " / ".join(languages) + "."
            )

    qualification_preference = str(raw_body.get("q5") or "").strip().lower()
    qualification = attributes.get("qualification_type")
    if qualification_preference.startswith("yes") and qualification in (
        None, "", candidate_selection.NOT_STATED,
    ):
        constraints.append(
            "Qualification to confirm: the catalogue does not state an NVQ or other formal qualification for this course."
        )
    return constraints


def _fallback_questions(candidate: dict, raw_body: dict) -> list[str]:
    """Build decision questions from unresolved fit, never from matched facts alone."""
    attributes = candidate["structured_attributes"]
    course_name = candidate["course_name"]
    questions = []

    preferred_schedule = str(raw_body.get("q3") or "").strip()
    attendance = str(attributes.get("attendance_type") or "").strip()
    days = str(attributes.get("attendance_days") or "").strip()
    attendance_known = attendance not in ("", candidate_selection.NOT_STATED)
    if (
        preferred_schedule
        and "no strong preference" not in preferred_schedule.lower()
        and attendance_known
    ):
        wants_part_time = (
            "part-time" in preferred_schedule.lower()
            or "weekend" in preferred_schedule.lower()
        )
        actual_part_time = (
            "part time" in attendance.lower()
            or "weekend" in days.lower()
        )
        if wants_part_time != actual_part_time:
            schedule_text = attendance.lower()
            if days not in ("", candidate_selection.NOT_STATED):
                schedule_text += f" on {days.lower()}"
            questions.append(
                f"{course_name} runs {schedule_text}, while you prefer "
                f"{preferred_schedule.lower()}. Could you realistically attend this timetable?"
            )

    preferred_language = str(raw_body.get("q4") or "").strip()
    languages = _as_language_list(attributes.get("instruction_languages"))
    if (
        preferred_language
        and "no strong preference" not in preferred_language.lower()
        and languages
        and preferred_language.casefold() not in {
            language.casefold() for language in languages
        }
    ):
        questions.append(
            f"{course_name} is taught in {' / '.join(languages)}, while you prefer "
            f"{preferred_language}. Would you be comfortable learning in the listed language?"
        )

    qualification_preference = str(raw_body.get("q5") or "").strip()
    qualification = attributes.get("qualification_type")
    if (
        qualification_preference.lower().startswith("yes")
        and qualification in (None, "", candidate_selection.NOT_STATED)
    ):
        questions.append(
            f"The catalogue does not confirm a formal qualification for {course_name}. "
            "Would you only consider it if the provider confirms one?"
        )

    exact_matches = candidate.get("exact_selected_skill_matches") or []
    selected_skills = []
    for skills in (candidate.get("selected_skills_in_those_sectors") or {}).values():
        for skill in skills:
            if skill and skill.casefold() not in {item.casefold() for item in selected_skills}:
                selected_skills.append(str(skill))
    if exact_matches:
        questions.append(
            f"What kind of work would you want {course_name} training to help you move into?"
        )
    elif selected_skills:
        selected_text = " or ".join(selected_skills[:2])
        questions.append(
            f"You selected {selected_text}. Would you also want to explore the related "
            f"{course_name} route, or stay focused on your original choice?"
        )
    else:
        questions.append(
            f"What specific work goal would make {course_name} worth considering for you?"
        )

    questions.append(
        f"What relevant experience or prior learning do you have that could help you start "
        f"{course_name}?"
    )

    unique_questions = []
    for question in questions:
        if question.casefold() not in {item.casefold() for item in unique_questions}:
            unique_questions.append(question)
    return unique_questions[:3]


def _fallback_exact_skill_programme(coverage: dict, candidate: dict, raw_body: dict) -> dict:
    attributes = candidate["structured_attributes"]
    facts = []
    attendance = attributes.get("attendance_type")
    days = attributes.get("attendance_days")
    if attendance not in (None, "", candidate_selection.NOT_STATED):
        facts.append(str(attendance).lower())
    if days not in (None, "", candidate_selection.NOT_STATED):
        facts.append(str(days).lower())
    languages = _as_language_list(attributes.get("instruction_languages"))
    if languages:
        facts.append("instruction in " + " / ".join(languages))
    verified_details = ", ".join(facts) if facts else "limited delivery information"
    return {
        "rank": 0,
        "course_id": candidate["course_id"],
        "course_name": candidate["course_name"],
        "why_it_may_suit_this_user": (
            f"This programme directly matches the member's selected {coverage['selected_skill']} skill "
            f"in {coverage['sector']}. The verified catalogue currently provides {verified_details}; "
            "review the important constraints before deciding together."
        ),
        "cluster_finding_summary": None,
        "questions_to_discuss": _fallback_questions(candidate, raw_body),
        "important_mismatches": _candidate_constraints(candidate, raw_body),
    }


def generate_officer_briefing(
    *,
    person_id: str,
    branch: str,
    cluster_answers: dict,
    ideal_sector_label: str | list[str],
    officer_context: dict,
    raw_body: dict,
    question_map: dict,
) -> tuple[dict, int]:
    manifest, _ = verify_corpus(verbose=False)
    manifest_by_id = {row["course_id"]: row for row in manifest}
    entries = profile_context.build_profile_context(branch, cluster_answers, officer_context)
    # Authorize the complete final-retained research set for each assigned
    # profile. Arbitrary survey statistics and explored/rejected variables are
    # still excluded mechanically.
    allowed_evidence = {
        entry.profile_key: {
            finding["variable"]: finding for finding in entry.retained_evidence
        }
        for entry in entries
    }

    ideal_sectors = ideal_sector_label if isinstance(ideal_sector_label, list) else [ideal_sector_label]
    skills_by_sector = officer_context.get("preferred_skills_by_sector") or {}
    skill_preference_unsure_by_sector = (
        officer_context.get("skill_preference_unsure_by_sector") or {}
    )
    selected_skills = officer_context.get("selected_skills")
    if selected_skills is None:
        selected_skills = [raw_body.get("q1")]
    selected_skills = [skill for skill in selected_skills if skill]
    selection = candidate_selection.retrieve_sector_catalogue({
        "ideal_sectors": ideal_sectors,
        "preferred_skills_by_sector": skills_by_sector,
        "q3_schedule": raw_body.get("q3"),
        "q4_language": raw_body.get("q4"),
        "q5_qualification": raw_body.get("q5"),
    })
    candidates_by_id = {
        candidate["course_id"]: candidate for candidate in selection["candidates"]
    }
    input_text = context_pack.build_new_person_input_text(
        person_id,
        branch,
        ideal_sector_label,
        {
            "selected_skills": selected_skills,
            "preferred_skills_by_sector": skills_by_sector,
            "skill_preference_unsure_by_sector": skill_preference_unsure_by_sector,
            "q2_reason": raw_body.get("q2"),
            "q3_schedule": raw_body.get("q3"),
            "q4_language": raw_body.get("q4"),
            "q5_qualification": raw_body.get("q5"),
        },
        entries,
        selection,
        manifest_by_id,
    )

    model = get_production_model()
    verify_production_model(model)
    api_result = call_new_person_recommendation_api(
        person_id,
        input_text,
        model,
        context_pack.RANKING_INSTRUCTIONS,
        NewPersonRecommendationResponse,
    )
    api_results = [api_result]
    required_coverage = selection.get("required_selected_skill_coverage", [])
    required_course_ids = {
        item["required_course_id"] for item in required_coverage
    }
    if api_result.success:
        returned_ids = {
            programme.course_id for programme in api_result.parsed.suggested_programmes
        }
        missing_required_ids = sorted(required_course_ids - returned_ids)
        if missing_required_ids:
            LOGGER.warning(
                "Ranking output omitted mandatory exact selected-skill courses; requesting one repair: %s",
                ", ".join(missing_required_ids),
            )
            repair_instructions = (
                context_pack.RANKING_INSTRUCTIONS
                + "\n\nCORRECTION REQUIRED: The previous response omitted mandatory exact selected-skill "
                + "course IDs: " + ", ".join(missing_required_ids) + ". Return a fresh complete ranking "
                "that includes every required_course_id in required_selected_skill_coverage exactly once. "
                "Keep conflicting preferences as explicit cautions; do not omit these courses."
            )
            repaired = call_new_person_recommendation_api(
                person_id + "-coverage-repair",
                input_text,
                model,
                repair_instructions,
                NewPersonRecommendationResponse,
            )
            api_results.append(repaired)
            if repaired.success:
                api_result = repaired

    assignments = []
    for entry in entries:
        metadata = metadata_for_profile(entry.profile_key)
        assignments.append({
            "profile_key": entry.profile_key,
            "model_id": entry.model_id,
            "cluster_code": metadata["cluster_code"],
            "cluster_name": metadata["cluster_name"],
            "common_description": metadata["common_description"],
            "model_published_accuracy": entry.model_published_accuracy,
            "model_judgment": entry.model_judgment,
            "needs_review_model": entry.model_judgment == "NEEDS REVIEW",
        })

    base_response = {
        "person_id": person_id,
        "branch": branch,
        "assigned_profiles": assignments,
        "cluster_catalogue": catalogue_for_branch(branch, question_map),
    }
    if not api_result.success:
        return {
            **base_response,
            "error": api_result.error_message,
            "suggested_programmes": [],
        }, 502

    parsed = api_result.parsed
    violations = []
    user_answers = {
        "preferred_sectors": ideal_sectors,
        "preferred_skills_by_sector": skills_by_sector,
        "preferred_skills": selected_skills,
        "q2": raw_body.get("q2"),
        "q3": raw_body.get("q3"),
        "q4": raw_body.get("q4"),
        "q5": raw_body.get("q5"),
        **{
            variable: answer.get("value_label")
            for variable, answer in cluster_answers.items()
        },
    }

    programmes = []
    seen_course_ids = set()
    ranked_output = sorted(
        parsed.suggested_programmes,
        key=lambda programme: (programme.rank, programme.course_id),
    )
    for programme in ranked_output:
        course_id = programme.course_id
        if course_id not in candidates_by_id:
            violations.append(
                f"programme {course_id}: removed because it was not in the retrieved selected-sector catalogue."
            )
            continue
        if course_id in seen_course_ids:
            violations.append(f"programme {course_id}: removed duplicate recommendation.")
            continue
        seen_course_ids.add(course_id)
        programme_violations = check_explicit_answers_not_fabricated(
            programme.user_facts_used,
            user_answers,
            f"programme {course_id}",
        )
        programme_violations.extend(_course_citations_are_exact(
            programme,
            candidates_by_id[course_id],
            context_pack_v2.load_course_doc(course_id, manifest_by_id),
        ))
        if not programme.user_facts_used:
            programme_violations.append(
                f"programme {course_id}: removed because it cited no actual user answer."
            )
        violations.extend(programme_violations)
        if programme_violations:
            continue
        kept_findings, finding_violations = filter_authorized_findings(
            programme.profile_findings_used,
            allowed_evidence,
            f"programme {course_id}",
        )
        cluster_summary = (programme.cluster_finding_summary or "").strip() or None
        # Cluster context and discussion prompts enrich a recommendation, but
        # are not allowed to delete a course that is otherwise grounded in an
        # exact member answer and verified catalogue facts.
        if kept_findings and not cluster_summary:
            finding_violations.append(
                f"programme {course_id}: ignored cluster citations because no plain-language summary was supplied."
            )
            kept_findings = []
        if cluster_summary and not kept_findings:
            finding_violations.append(
                f"programme {course_id}: removed the cluster summary because it had no authorized retained finding."
            )
            cluster_summary = None
        if cluster_summary and not _cluster_summary_is_plain_language(cluster_summary):
            finding_violations.append(
                f"programme {course_id}: removed a technical, statistical, or person-level cluster summary."
            )
            cluster_summary = None
            kept_findings = []
        if _has_clear_group_context_wording(programme.why_it_may_suit_this_user):
            finding_violations.append(
                f"programme {course_id}: cluster context was repeated outside the separate cluster-finding summary."
            )
        questions_to_discuss = []
        for question in programme.questions_to_discuss:
            question_text = question.strip()
            if not _programme_question_is_plain_language(question_text):
                finding_violations.append(
                    f"programme {course_id}: removed an invalid or technical discussion question."
                )
                continue
            if question_text.lower() not in {item.lower() for item in questions_to_discuss}:
                questions_to_discuss.append(question_text)
        if len(questions_to_discuss) < 2:
            finding_violations.append(
                f"programme {course_id}: supplemented insufficient discussion questions with governed course questions."
            )
            for fallback_question in _fallback_questions(
                candidates_by_id[course_id], raw_body,
            ):
                if fallback_question.casefold() not in {
                    item.casefold() for item in questions_to_discuss
                }:
                    questions_to_discuss.append(fallback_question)
                if len(questions_to_discuss) == 3:
                    break
        violations.extend(finding_violations)

        candidate = candidates_by_id[course_id]
        programmes.append({
            "rank": len(programmes) + 1,
            "course_id": course_id,
            "course_name": candidate["course_name"],
            "why_it_may_suit_this_user": programme.why_it_may_suit_this_user,
            "cluster_finding_summary": cluster_summary,
            "questions_to_discuss": questions_to_discuss,
            "important_mismatches": _candidate_constraints(candidate, raw_body),
        })

    # A selected skill with an exact governed course match is a hard coverage
    # requirement. If the LLM or a core citation check still omitted it after
    # the single repair call, restore a conservative catalogue-grounded card.
    programmes_by_id = {programme["course_id"]: programme for programme in programmes}
    for coverage_index, coverage in enumerate(required_coverage):
        required_id = coverage["required_course_id"]
        if required_id in programmes_by_id:
            continue
        fallback = _fallback_exact_skill_programme(
            coverage, candidates_by_id[required_id], raw_body,
        )
        fallback["rank"] = 1000 + coverage_index
        programmes.append(fallback)
        programmes_by_id[required_id] = fallback
        violations.append(
            f"programme {required_id}: restored from governed catalogue facts because an exact selected-skill match was omitted."
        )

    required_order = {
        coverage["required_course_id"] for coverage in required_coverage
    }
    programmes.sort(key=lambda programme: (
        0 if programme["course_id"] in required_order else 1,
        programme["rank"],
    ))
    for rank, programme in enumerate(programmes[:9], start=1):
        programme["rank"] = rank
    programmes = programmes[:9]

    if parsed.recommendation_status == "NO_DEFENSIBLE_RECOMMENDATION" and not required_coverage:
        programmes = []

    effective_status = parsed.recommendation_status
    no_recommendation_reason = parsed.no_recommendation_reason
    if programmes:
        effective_status = "RECOMMENDATIONS_AVAILABLE"
        no_recommendation_reason = None
    if effective_status == "RECOMMENDATIONS_AVAILABLE" and not programmes:
        effective_status = "NO_DEFENSIBLE_RECOMMENDATION"
        no_recommendation_reason = (
            "No programme remained after checking the model output against the member's answers "
            "and governed course evidence."
        )

    return {
        **base_response,
        "recommendation_status": effective_status,
        "suggested_programmes": programmes,
        "no_recommendation_reason": no_recommendation_reason,
        "candidate_programme_count": len(candidates_by_id),
        "evidence_safeguard_violations": violations,
        "token_usage": {
            "total_tokens": sum(result.total_tokens or 0 for result in api_results),
            "input_tokens": sum(result.input_tokens or 0 for result in api_results),
            "output_tokens": sum(result.output_tokens or 0 for result in api_results),
        },
    }, 200
