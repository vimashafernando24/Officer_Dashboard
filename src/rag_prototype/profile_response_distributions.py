"""Exact labelled response percentages for officer-facing evidence charts.

The frozen profile documents intentionally summarise ordered variables with a
median and IQR. Those statistics are suitable for the analysis report but not
for a Youth Services Officer trying to understand what people actually
answered. This module reconstructs the display distribution from the frozen
profile assignments and cleaned labelled survey responses.

It is display-only: it does not form clusters, assign a new respondent, select
evidence, rank courses, or enter the GPT prompt.
"""
from __future__ import annotations

import csv
from collections import Counter
from functools import lru_cache
from pathlib import Path


BASE = Path(__file__).resolve().parents[2]
LABELS_CSV = BASE / "outputs/nysc_survey_cleaned_labels.csv"
VALUES_CSV = BASE / "outputs/nysc_survey_cleaned_values.csv"


ASSIGNMENT_SPECS = {
    "D_motivation": (
        BASE / "outputs/branch_d_motivation_consensus/motivation_consensus_assignments.csv",
        "consensus_profile_id",
    ),
    "D_economic": (
        BASE / "outputs/branch_d_economic_resources_clusters/economic_consensus_assignments.csv",
        "economic_profile_id",
    ),
    "D_educational_cultural": (
        BASE / "outputs/branch_d_educational_cultural_capital_clusters/educational_cultural_consensus_assignments.csv",
        "educational_cultural_profile_id",
    ),
    "E_learning_orientation": (
        BASE / "outputs/branch_e_all_dimensions_clusters/e4/consensus_assignments.csv",
        "profile_id",
    ),
    "F_employment_security": (
        BASE / "outputs/branch_f_employment_security_clusters/employment_security_consensus_assignments.csv",
        "employment_security_profile_id",
    ),
    "G_economic_role": (
        BASE / "outputs/branch_g_household_economic_resources_clusters/household_economic_consensus_assignments.csv",
        "economic_profile_id",
    ),
    "G_future_engagement": (
        BASE / "outputs/branch_g_inactivity_pathway_future_engagement_clusters/pathway_engagement_consensus_assignments.csv",
        "pathway_profile_id",
    ),
}


def _normalise_profile_id(value: str) -> int:
    return int(float(value.strip()))


@lru_cache(maxsize=1)
def _survey_rows() -> tuple[dict[str, dict], dict[str, dict]]:
    with open(LABELS_CSV, newline="", encoding="utf-8-sig") as handle:
        labels = {row["respondent_id"]: row for row in csv.DictReader(handle)}
    with open(VALUES_CSV, newline="", encoding="utf-8-sig") as handle:
        values = {row["respondent_id"]: row for row in csv.DictReader(handle)}
    if labels.keys() != values.keys():
        raise ValueError("Cleaned label/value survey files do not contain the same respondents")
    return labels, values


@lru_cache(maxsize=None)
def _profile_member_ids(model_id: str, profile_id: int) -> frozenset[str]:
    if model_id not in ASSIGNMENT_SPECS:
        raise ValueError(f"No frozen assignment source configured for retained model '{model_id}'")
    path, profile_column = ASSIGNMENT_SPECS[model_id]
    with open(path, newline="", encoding="utf-8-sig") as handle:
        members = {
            row["respondent_id"]
            for row in csv.DictReader(handle)
            if row.get(profile_column, "").strip()
            and _normalise_profile_id(row[profile_column]) == profile_id
        }
    if not members:
        raise ValueError(f"No frozen members found for {model_id} profile {profile_id}")
    return frozenset(members)


def _sort_code(raw: str) -> tuple[int, float | str]:
    try:
        return (0, float(raw))
    except (TypeError, ValueError):
        return (1, str(raw).lower())


def _is_eligible_label(label: str) -> bool:
    """Match the final profiling analysis' explicit non-response exclusions."""
    normalised = label.strip().lower().replace("’", "'")
    return normalised not in {
        "prefer not to say",
        "not applicable",
        "don't know",
        "do not know",
        "missing",
    }


@lru_cache(maxsize=None)
def _answer_scale(variable: str) -> tuple[str, ...]:
    """Return all known labelled answers in their original survey-code order."""
    labels, values = _survey_rows()
    answer_codes: dict[str, list[str]] = {}
    for respondent_id, label_row in labels.items():
        label = label_row.get(variable, "").strip()
        if not label or not _is_eligible_label(label):
            continue
        answer_codes.setdefault(label, []).append(values[respondent_id].get(variable, ""))

    def label_order(label: str):
        codes = [code for code in answer_codes[label] if str(code).strip()]
        return min((_sort_code(code) for code in codes), default=(1, label.lower()))

    return tuple(sorted(answer_codes, key=lambda label: (label_order(label), label.lower())))


@lru_cache(maxsize=None)
def profile_response_distribution(profile_key: str, variable: str) -> dict:
    """Return exact counts/% for answer labels within one frozen profile."""
    try:
        model_id, profile_text = profile_key.rsplit("_p", 1)
        profile_id = int(profile_text)
    except (ValueError, TypeError) as exc:
        raise ValueError(f"Invalid retained profile key '{profile_key}'") from exc

    labels, _ = _survey_rows()
    member_ids = _profile_member_ids(model_id, profile_id)
    observed = Counter(
        labels[respondent_id].get(variable, "").strip()
        for respondent_id in member_ids
        if respondent_id in labels
        and labels[respondent_id].get(variable, "").strip()
        and _is_eligible_label(labels[respondent_id].get(variable, ""))
    )
    eligible_n = sum(observed.values())
    if not eligible_n:
        return {"eligible_n": 0, "distribution": []}

    scale = list(_answer_scale(variable))
    # Include a label even if it was somehow absent from the global scale;
    # this is defensive and never silently drops an observed response.
    scale.extend(sorted(set(observed) - set(scale)))
    distribution = [
        {
            "value": answer,
            "count": observed.get(answer, 0),
            "percent": round(observed.get(answer, 0) * 100 / eligible_n, 1),
        }
        for answer in scale
    ]
    return {"eligible_n": eligible_n, "distribution": distribution}
