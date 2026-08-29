"""Mechanical, testable safeguards for the youth-services-officer briefing.

Prompt instructions alone are not trusted to keep the model inside the
retained + current-context cluster-evidence bar (see
retained_cluster_evidence_registry.py and new_person_context_pack.py's
"ALLOWED CLUSTER-EVIDENCE BASE" rule) — this
module re-checks the model's actual output against the same allow-list that
was given to it, and strips anything that doesn't belong, the same way
new_person_context_pack.py already flags (rather than silently accepts)
duplicate course_ids. Findings are DROPPED, not merely flagged, because an
unauthorized claim reaching the officer's screen is exactly the failure mode
this exists to prevent — but every drop is recorded and returned so nothing
disappears silently.
"""

import json


def build_allowed_evidence_index(profile_entries) -> dict:
    """profile_key -> {variable: evidence_dict} for every ProfileContextEntry's
    pre-selected validated_evidence. This is the single source of truth a
    ProfileFinding is checked against."""
    index = {}
    for e in profile_entries:
        index[e.profile_key] = {ev["variable"]: ev for ev in e.validated_evidence}
    return index


def is_finding_authorized(
    profile_key: str, variable: str, finding_text: str, allowed_index: dict,
) -> bool:
    """Authorize the profile, variable, and exact retained finding text.

    Variable-only checks are insufficient: a model could cite an allowlisted
    variable while inventing or copying a different statistic for it.
    """
    allowed = allowed_index.get(profile_key, {}).get(variable)
    return bool(allowed and finding_text.strip() == allowed["finding"].strip())


def filter_authorized_findings(findings: list, allowed_index: dict, context_label: str):
    """findings: list of objects/dicts with .profile_key/.variable (or dict keys).
    Returns (kept, violations) — violations is a list of human-readable strings
    for anything dropped, so it can be surfaced (e.g. in an API response) rather
    than vanish without a trace."""
    kept, violations = [], []
    for f in findings:
        profile_key = f.profile_key if hasattr(f, "profile_key") else f["profile_key"]
        variable = f.variable if hasattr(f, "variable") else f["variable"]
        finding_text = f.finding if hasattr(f, "finding") else f["finding"]
        if is_finding_authorized(profile_key, variable, finding_text, allowed_index):
            kept.append(f)
        else:
            violations.append(
                f"{context_label}: dropped unauthorized cluster citation "
                f"variable='{variable}' profile_key='{profile_key}' — the profile, variable, "
                f"and exact finding text did not match the retained + current-context registry."
            )
    return kept, violations


def check_explicit_answers_not_fabricated(explicit_answers_used: list, collected_answers: dict,
                                           context_label: str) -> list:
    """collected_answers: {question_label_lowercase_fragment: actual_answer_value} — the
    real Section 1 values this member actually gave (ideal_sector, Q1-Q5). Flags any
    explicit_answers_used entry whose stated answer doesn't match anything the member
    actually said, which would mean the model invented (or altered) an answer."""
    violations = []
    def scalar_values(value):
        if isinstance(value, dict):
            for nested in value.values():
                yield from scalar_values(nested)
        elif isinstance(value, (list, tuple, set)):
            for nested in value:
                yield from scalar_values(nested)
        elif value not in (None, ""):
            yield str(value)

    collected_values_lower = {
        value.strip().lower()
        for collected in collected_answers.values()
        for value in scalar_values(collected)
    }

    def is_exact_nested_subset(candidate, actual) -> bool:
        """Allow an exact sector -> selected-skills subset, but no invented value."""
        if isinstance(candidate, dict) and isinstance(actual, dict):
            return bool(candidate) and all(
                key in actual and is_exact_nested_subset(value, actual[key])
                for key, value in candidate.items()
            )
        if isinstance(candidate, list) and isinstance(actual, (list, tuple, set)):
            actual_values = {str(value).strip().lower() for value in actual}
            return bool(candidate) and all(
                str(value).strip().lower() in actual_values for value in candidate
            )
        return str(candidate).strip().lower() == str(actual).strip().lower()

    for a in explicit_answers_used:
        answer = a.answer if hasattr(a, "answer") else a["answer"]
        question = a.question if hasattr(a, "question") else a["question"]
        nested_match = False
        try:
            parsed_answer = json.loads(answer)
        except (TypeError, json.JSONDecodeError):
            parsed_answer = None
        if isinstance(parsed_answer, (dict, list)):
            nested_match = any(
                is_exact_nested_subset(parsed_answer, collected)
                for collected in collected_answers.values()
            )
        if answer.strip().lower() not in collected_values_lower and not nested_match:
            violations.append(
                f"{context_label}: explicit_answers_used cites question='{question}' "
                f"answer='{answer}' which does not match any value this member actually "
                f"gave — possible fabrication of an intake answer."
            )
    return violations
