"""End-to-end service for the simplified officer briefing response."""
from __future__ import annotations

import json
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
    selected_skills = officer_context.get("selected_skills") or [raw_body.get("q1")]
    selected_skills = [skill for skill in selected_skills if skill]
    selection = candidate_selection.retrieve_sector_catalogue({
        "ideal_sectors": ideal_sectors,
        "preferred_skills_by_sector": skills_by_sector,
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

    assignments = []
    for entry in entries:
        metadata = metadata_for_profile(entry.profile_key)
        assignments.append({
            "profile_key": entry.profile_key,
            "model_id": entry.model_id,
            "cluster_code": metadata["cluster_code"],
            "cluster_name": metadata["cluster_name"],
            "common_description": metadata["common_description"],
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
        _, finding_violations = filter_authorized_findings(
            programme.profile_findings_used,
            allowed_evidence,
            f"programme {course_id}",
        )
        violations.extend(finding_violations)
        if finding_violations:
            continue

        candidate = candidates_by_id[course_id]
        programmes.append({
            "rank": len(programmes) + 1,
            "course_id": course_id,
            "course_name": candidate["course_name"],
            "why_it_may_suit_this_user": programme.why_it_may_suit_this_user,
        })

    if parsed.recommendation_status == "NO_DEFENSIBLE_RECOMMENDATION":
        programmes = []

    effective_status = parsed.recommendation_status
    no_recommendation_reason = parsed.no_recommendation_reason
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
            "total_tokens": api_result.total_tokens,
            "input_tokens": api_result.input_tokens,
            "output_tokens": api_result.output_tokens,
        },
    }, 200
