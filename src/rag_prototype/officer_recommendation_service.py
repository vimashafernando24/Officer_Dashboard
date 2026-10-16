"""End-to-end service for the simplified officer briefing response."""
from __future__ import annotations

import json
import logging
import re
import time

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

APPLICATION_DEADLINE_SECONDS = 270.0
PRIMARY_OPENAI_TIMEOUT_SECONDS = 90.0
REPAIR_OPENAI_TIMEOUT_SECONDS = 60.0
MIN_POST_PROCESSING_RESERVE_SECONDS = 20.0
REPAIR_MINIMUM_REMAINING_SECONDS = (
    REPAIR_OPENAI_TIMEOUT_SECONDS + MIN_POST_PROCESSING_RESERVE_SECONDS
)

_ERROR_HTTP_STATUS = {
    "missing_configuration": 503,
    "authentication_failure": 503,
    "provider_unavailable": 503,
    "upstream_timeout": 504,
    "invalid_provider_output": 502,
}
_ERROR_PUBLIC_CODE = {
    "missing_configuration": "recommendation_unavailable",
    "authentication_failure": "recommendation_unavailable",
    "provider_unavailable": "recommendation_unavailable",
    "upstream_timeout": "recommendation_timeout",
    "invalid_provider_output": "invalid_recommendation_response",
}
_ERROR_PUBLIC_MESSAGE = {
    "missing_configuration": "Programme recommendation service is temporarily unavailable.",
    "authentication_failure": "Programme recommendation service is temporarily unavailable.",
    "provider_unavailable": "Programme recommendation service is temporarily unavailable.",
    "upstream_timeout": "Programme recommendation service timed out. Please try again.",
    "invalid_provider_output": "Programme recommendation service returned an invalid response.",
}


def _controlled_failure(base_response: dict, category: str) -> tuple[dict, int]:
    safe_category = category if category in _ERROR_HTTP_STATUS else "provider_unavailable"
    return {
        **base_response,
        "error": _ERROR_PUBLIC_MESSAGE[safe_category],
        "error_code": _ERROR_PUBLIC_CODE[safe_category],
        "suggested_programmes": [],
    }, _ERROR_HTTP_STATUS[safe_category]


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


def _claim_label(value: str) -> str:
    """Normalize an exact displayed label without treating related concepts as equal."""
    normalized = _normalise_text(value).replace("&", " and ")
    return " ".join(re.findall(r"[\w+-]+", normalized))


def _explanation_claim_violations(
    explanation: str,
    *,
    schedule_preference: str | None,
    internal_skill_areas: list[str],
    selected_sectors: list[str],
    selected_skills: list[str],
) -> list[str]:
    """Detect only unsupported participant attributions in explanation sentences."""
    violations = []
    matching_text = str(explanation).replace("’", "'")
    sentences = [
        sentence.strip()
        for sentence in re.split(r"(?<=[.!?])[\"'”]?\s+|\n+", matching_text)
        if sentence.strip()
    ]

    effective_schedule = _normalise_text(schedule_preference or "") or "no strong preference"
    if "no strong preference" in effective_schedule:
        schedule = r"(?:weekends?|weekdays?|part[ -]?time|full[ -]?time)"
        participant = r"(?:the\s+)?(?:member|participant|user|they|you|them)"
        preference_owner = (
            r"(?:the\s+)?(?:member|participant|user|them|they|you)|"
            r"(?:their|your|the\s+member's|the\s+participant's)|"
            r"(?:schedule|study)\s+preference"
        )
        direct_choice = (
            r"(?:want(?:s|ed|ing)?|request(?:s|ed|ing)?|"
            r"cho(?:ose|oses|se|sen|osing)|prefer(?:s|red|ring)?|need(?:s|ed|ing)?)"
        )
        suitability = (
            r"(?:suit(?:s|ed|ing)?|fit(?:s|ted|ting)?|match(?:es|ed|ing)?|"
            r"meet(?:s|ing)?|align(?:s|ed|ing)?|accommodat(?:e|es|ed|ing)|"
            r"satisf(?:y|ies|ied|ying)|"
            r"work(?:s|ed|ing)?\s+well\s+for|(?:is|was|would\s+be)\s+ideal\s+for|"
            r"ideal\s+for)"
        )
        schedule_claim_patterns = [
            re.compile(
                rf"\b{participant}\b(?:\s+\w+){{0,3}}\s+{direct_choice}\b"
                rf"(?:\W+\w+){{0,4}}\W+\b{schedule}\b",
                re.IGNORECASE,
            ),
            re.compile(
                rf"\b{schedule}\b(?:\W+\w+){{0,6}}\W+\b{suitability}\b"
                rf"(?:\W+\w+){{0,5}}\W+\b(?:{preference_owner})\b",
                re.IGNORECASE,
            ),
            re.compile(
                rf"\b{suitability}\b(?:\W+\w+){{0,5}}\W+\b(?:{preference_owner})\b"
                rf"(?:\W+\w+){{0,5}}\W+\b{schedule}\b",
                re.IGNORECASE,
            ),
            re.compile(
                rf"\b(?:the\s+member's|the\s+participant's|their|your)\s+"
                rf"(?:preferred|chosen|requested|needed)\s+\b{schedule}\b",
                re.IGNORECASE,
            ),
        ]
        negation = re.compile(
            r"\b(?:not|never|without)\b|"
            r"\b(?:doesn|didn|isn|aren|wasn|weren|hasn|haven|hadn|wouldn|couldn|shouldn)['’]t\b|"
            r"\bno\s+(?:stated\s+|strong\s+|schedule\s+|study\s+)?preference\b",
            re.IGNORECASE,
        )
        participant_reference = re.compile(
            r"\b(?:member|participant|user|they|you|them)\b",
            re.IGNORECASE,
        )
        schedule_claim_found = False
        for sentence in sentences:
            clauses = [
                clause.strip()
                for clause in re.split(
                    r"\s*;\s*|\s+\b(?:but|yet|however)\b\s+",
                    sentence,
                    flags=re.IGNORECASE,
                )
                if clause.strip()
            ]
            inherited_participant = bool(participant_reference.search(sentence))
            for clause_index, clause in enumerate(clauses):
                matching_clause = clause
                if (
                    clause_index > 0
                    and inherited_participant
                    and not participant_reference.search(clause)
                    and re.match(rf"^{direct_choice}\b", clause, re.IGNORECASE)
                ):
                    matching_clause = "the member " + clause
                for pattern in schedule_claim_patterns:
                    if any(
                        not negation.search(match.group(0))
                        for match in pattern.finditer(matching_clause)
                    ):
                        schedule_claim_found = True
                        break
                if schedule_claim_found:
                    break
            if schedule_claim_found:
                break
        if schedule_claim_found:
            violations.append("unsupported schedule-preference attribution")

    explicit_labels = {
        _claim_label(label)
        for label in [*selected_sectors, *selected_skills]
        if _claim_label(label)
    }
    internal_labels = {
        _claim_label(label)
        for label in internal_skill_areas
        if _claim_label(label) and _claim_label(label) not in explicit_labels
    }
    participant = r"(?:the\s+)?(?:member|participant|user|they|you)"
    selection = (
        r"(?:select(?:s|ed|ing)?|cho(?:ose|oses|se|sen|osing)|"
        r"request(?:s|ed|ing)?|prefer(?:s|red|ring)?)"
    )

    def directly_attributes_label(clause: str, label: str) -> bool:
        patterns = (
            # "The member explicitly selected the ICT & Computing category."
            rf"\b{participant}\b(?:\s+\w+){{0,3}}\s+\b{selection}\b"
            rf"(?:\s+(?:the|an?|internal|catalogue|course|skill|area|category|classification))*"
            rf"\s+\b{re.escape(label)}\b",
            # "ICT & Computing is the category the member chose."
            rf"\b{re.escape(label)}\b\s+(?:is|was)\s+(?:the\s+)?"
            rf"(?:area|category|classification)?\s*(?:that\s+|which\s+)?"
            rf"\b{participant}\b(?:\s+\w+){{0,2}}\s+\b{selection}\b",
            # "ICT & Computing was requested by the participant."
            rf"\b{re.escape(label)}\b(?:\s+\w+){{0,2}}\s+(?:is|was)\s+"
            rf"\b(?:selected|chosen|requested|preferred)\b\s+by\s+\b{participant}\b",
            # "The member's selected area is ICT & Computing."
            rf"\b(?:(?:the\s+)?(?:member|participant|user)\s+s|their|your)\b\s+"
            rf"\b(?:selected|preferred|chosen|requested)\b\s+"
            rf"\b(?:area|category|classification)\b\s+(?:is|was)\s+"
            rf"\b{re.escape(label)}\b",
            # "The member chose courses/an interest in ICT & Computing."
            rf"\b{participant}\b(?:\s+\w+){{0,3}}\s+\b{selection}\b\s+"
            rf"(?:(?:the|an?)\s+)?\b(?:course|courses|option|options|interest|pathway|route)\b"
            rf"\s+\b(?:in|within|from)\b\s+(?:the\s+)?\b{re.escape(label)}\b",
        )
        return any(re.search(pattern, clause, re.IGNORECASE) for pattern in patterns)

    category_reference = re.compile(
        r"\b(?:course|area|category|classification|belongs|mapped|in)\b",
        re.IGNORECASE,
    )
    cross_sentence_attribution = re.compile(
        rf"^(?:this|that)\s+(?:is|was)\s+(?:(?:the|an?)\s+)?"
        rf"(?:(?:area|category|classification)\s+)?(?:what\s+|that\s+)?"
        rf"\b{participant}\b(?:\s+\w+){{0,2}}\s+\b{selection}\b|"
        rf"^(?:this|that)\s+(?:is|was)\s+\b(?:selected|chosen|requested|preferred)\b"
        rf"\s+by\s+\b{participant}\b",
        re.IGNORECASE,
    )
    normalized_sentences = [_claim_label(sentence) for sentence in sentences]
    for sentence_index, sentence in enumerate(sentences):
        clauses = [
            _claim_label(clause)
            for clause in re.split(
                r"\s*(?:,|;|:|—|–)\s*(?:(?:and|but|while|which)\s+)?|"
                r"\s+and\s+(?=(?:the\s+)?course\b)",
                sentence,
                flags=re.IGNORECASE,
            )
            if clause.strip()
        ]
        for label in internal_labels:
            if any(directly_attributes_label(clause, label) for clause in clauses):
                violations.append(
                    "internal catalogue skill area attributed as a participant selection"
                )
                return violations
            if sentence_index + 1 >= len(sentences):
                continue
            if (
                f" {label} " in f" {normalized_sentences[sentence_index]} "
                and category_reference.search(sentence)
                and cross_sentence_attribution.search(normalized_sentences[sentence_index + 1])
            ):
                violations.append(
                    "internal catalogue skill area attributed as a participant selection"
                )
                return violations
    return violations


def _deterministic_grounded_explanation(candidate: dict) -> str:
    """Build a conservative replacement from explicit selections and catalogue facts."""
    exact_matches = candidate.get("exact_selected_skill_matches") or []
    matched_sectors = list(dict.fromkeys(candidate.get("matched_selected_sectors") or []))
    if exact_matches:
        selected_pairs = list(dict.fromkeys(
            (str(match["skill"]), str(match["sector"])) for match in exact_matches
        ))
        if len(selected_pairs) == 1:
            skill, sector = selected_pairs[0]
            match_sentence = (
                f"This programme directly matches the member's selected {skill} skill "
                f"under the {sector} sector."
            )
        else:
            choices = ", ".join(f"{skill} ({sector})" for skill, sector in selected_pairs)
            match_sentence = f"This programme directly matches the member's selected skills: {choices}."
    elif matched_sectors:
        sectors = ", ".join(matched_sectors)
        match_sentence = (
            "This programme is a related catalogue option mapped from the member's selected "
            f"sector{'s' if len(matched_sectors) > 1 else ''}: {sectors}."
        )
    else:
        match_sentence = (
            "This is a governed catalogue option that the officer can review with the member."
        )

    attributes = candidate.get("structured_attributes") or {}
    catalogue_facts = []
    attendance = str(attributes.get("attendance_type") or "").strip()
    days = str(attributes.get("attendance_days") or "").strip()
    if attendance not in ("", candidate_selection.NOT_STATED):
        schedule = attendance
        if days not in ("", candidate_selection.NOT_STATED):
            schedule += f" on {days}"
        catalogue_facts.append(schedule)
    languages = _as_language_list(attributes.get("instruction_languages"))
    if languages:
        catalogue_facts.append("instruction in " + " / ".join(languages))
    qualification = str(attributes.get("qualification_type") or "").strip()
    if qualification not in ("", candidate_selection.NOT_STATED):
        catalogue_facts.append(qualification)

    if catalogue_facts:
        fact_sentence = "The catalogue lists " + ", and ".join(catalogue_facts[:2]) + "."
    else:
        fact_sentence = "The verified catalogue record should be reviewed before deciding together."
    return f"{match_sentence} {fact_sentence}"


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
    deadline_at = time.monotonic() + APPLICATION_DEADLINE_SECONDS
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

    remaining_before_primary = deadline_at - time.monotonic()
    if remaining_before_primary < (
        PRIMARY_OPENAI_TIMEOUT_SECONDS + MIN_POST_PROCESSING_RESERVE_SECONDS
    ):
        LOGGER.warning("Primary recommendation skipped: insufficient execution budget.")
        return _controlled_failure(base_response, "upstream_timeout")

    model = get_production_model()
    verify_production_model(model)
    api_result = call_new_person_recommendation_api(
        person_id,
        input_text,
        model,
        context_pack.RANKING_INSTRUCTIONS,
        NewPersonRecommendationResponse,
        timeout_seconds=PRIMARY_OPENAI_TIMEOUT_SECONDS,
    )
    api_results = [api_result]
    if not api_result.success:
        return _controlled_failure(
            base_response,
            api_result.error_category or "provider_unavailable",
        )

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
            if deadline_at - time.monotonic() >= REPAIR_MINIMUM_REMAINING_SECONDS:
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
                    timeout_seconds=REPAIR_OPENAI_TIMEOUT_SECONDS,
                )
                api_results.append(repaired)
                if repaired.success:
                    api_result = repaired
                else:
                    LOGGER.warning(
                        "Coverage repair failed; preserving the primary response (category=%s).",
                        repaired.error_category or "provider_unavailable",
                    )
            else:
                LOGGER.warning(
                    "Coverage repair skipped: insufficient execution budget; preserving primary response."
                )

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
        explanation = programme.why_it_may_suit_this_user
        explanation_violations = _explanation_claim_violations(
            explanation,
            schedule_preference=raw_body.get("q3"),
            internal_skill_areas=selection.get("skill_areas") or [],
            selected_sectors=ideal_sectors,
            selected_skills=selected_skills,
        )
        if explanation_violations:
            explanation = _deterministic_grounded_explanation(candidate)
            violations.append(
                f"programme {course_id}: replaced explanation because it contained "
                + " and ".join(explanation_violations) + "."
            )
        programmes.append({
            "rank": len(programmes) + 1,
            "course_id": course_id,
            "course_name": candidate["course_name"],
            "why_it_may_suit_this_user": explanation,
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
