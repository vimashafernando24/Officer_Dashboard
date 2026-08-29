#!/usr/bin/env python3
"""Build and validate the governed Branch F officer-dashboard payload.

Reads frozen research outputs and writes only the dashboard's generated JSON.
No clustering, profiling, assignment, survey, or catalogue source is modified.
"""

from __future__ import annotations

import json
import math
import re
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
SPEC = ROOT / "outputs/officer_dashboard_specification/dashboard_metric_specification.csv"
PROFILE_SUMMARY = ROOT / "outputs/officer_dashboard_specification/profile_dashboard_summary.csv"
ASSIGNMENTS = ROOT / "outputs/branch_f_employment_security_clusters/employment_security_consensus_assignments.csv"
PROFILE_RESULTS = ROOT / "outputs/final_cluster_profile_comparison_summary.csv"
PROFILE_LABELS = ROOT / "outputs/final_cluster_programme_relevant_profiles.csv"
LABELS = ROOT / "outputs/nysc_survey_cleaned_labels.csv"
VALUES = ROOT / "outputs/nysc_survey_cleaned_values.csv"
COURSES = ROOT / "outputs/nysc_course_matching_dataset.csv"
OUTPUT = ROOT / "officer_dashboard/data/branch_f_dashboard_data.json"

MODEL_ID = "F_employment_security"
PROFILE_META = {
    1: {"dashboard_id": "F-S1", "expected_n": 29},
    2: {"dashboard_id": "F-S2", "expected_n": 52},
}

REQUIRED_METRICS = {
    "ALL_IDENTITY_001",
    "ALL_SIZE_001",
    "ALL_SIZE_002",
    "ALL_QUALITY_001",
    "ALL_QUALITY_002",
    "ALL_QUALITY_003",
    "ALL_QUALITY_004",
    "F_EMPLOYMENT_SECURITY_DEF_01",
    "F_EMPLOYMENT_SECURITY_DEF_02",
    "F_EMPLOYMENT_SECURITY_DEF_03",
    "F_EMPLOYMENT_SECURITY_PROF_01",
    "F_EMPLOYMENT_SECURITY_PROF_02",
    "F_EMPLOYMENT_SECURITY_PROF_03",
    "F_EMPLOYMENT_SECURITY_PROF_04",
    "F_EMPLOYMENT_SECURITY_PROF_05",
    "F_EMPLOYMENT_SECURITY_PROF_06",
    "F_EMPLOYMENT_SECURITY_DIRECT_TRA_01",
    "F_EMPLOYMENT_SECURITY_DIRECT_PRE_01",
    "SUPPLY_001",
}

DEFINITIONS = [
    ("F_EMPLOYMENT_SECURITY_DEF_01", "contract_type__response"),
    ("F_EMPLOYMENT_SECURITY_DEF_02", "job_security_12months__response"),
    ("F_EMPLOYMENT_SECURITY_DEF_03", "sector_formality__response"),
]

PROFILING = [
    ("F_EMPLOYMENT_SECURITY_PROF_01", "monthly_income_band"),
    ("F_EMPLOYMENT_SECURITY_PROF_02", "primary_income_source"),
    ("F_EMPLOYMENT_SECURITY_PROF_03", "hopes_to_change_job"),
    ("F_EMPLOYMENT_SECURITY_PROF_04", "job_satisfaction"),
    ("F_EMPLOYMENT_SECURITY_PROF_05", "received_training"),
    ("F_EMPLOYMENT_SECURITY_PROF_06", "work_while_study_type"),
]


def round_pct(count: int | float, denominator: int) -> float | None:
    return round(100 * count / denominator, 1) if denominator else None


def clean_scalar(value):
    if pd.isna(value):
        return None
    if isinstance(value, bool):
        return value
    if isinstance(value, (int, float)):
        return int(value) if float(value).is_integer() else round(float(value), 4)
    return str(value)


def spec_info(spec_by_id, metric_id):
    row = spec_by_id[metric_id]
    return {
        "metric_id": metric_id,
        "display_name": row["display_name"],
        "section": row["dashboard_section"],
        "source": row["source_variable_file"],
        "denominator_rule": row["denominator_rule"],
        "evidence_type": row["evidence_type"],
        "visualization": row["visualization_type"],
        "caution": row["caution_limitation"],
        "display_priority": row["display_priority"],
    }


def distribution(series: pd.Series, categories=None):
    valid = series.dropna().astype(str)
    counts = valid.value_counts().to_dict()
    ordered = categories or list(counts)
    result = []
    for category in ordered:
        count = int(counts.get(category, 0))
        result.append({"category": category, "count": count, "percent": round_pct(count, len(valid))})
    return {"valid_n": int(len(valid)), "missing_n": int(series.isna().sum()), "categories": result}


def parse_profile_descriptives(text, categorical):
    parsed = {}
    for block in text.split(" || "):
        if categorical:
            match = re.match(r"Profile (\d+) eligible n=(\d+): (.*)", block)
            if not match:
                raise AssertionError(f"Cannot parse categorical descriptive: {block}")
            profile_id, eligible_n, categories_text = match.groups()
            categories = []
            for entry in categories_text.split("; "):
                category, count, percent = re.match(r"(.*): (\d+) \(([0-9.]+)%\)$", entry).groups()
                categories.append({"category": category, "count": int(count), "percent": float(percent)})
            parsed[int(profile_id)] = {"valid_n": int(eligible_n), "categories": categories}
        else:
            match = re.match(r"Profile (\d+) n=(\d+): median=([0-9.]+), IQR=([0-9.]+)–([0-9.]+)", block)
            if not match:
                raise AssertionError(f"Cannot parse ordered descriptive: {block}")
            profile_id, valid_n, median, q1, q3 = match.groups()
            parsed[int(profile_id)] = {
                "valid_n": int(valid_n),
                "median": float(median),
                "q1": float(q1),
                "q3": float(q3),
            }
    return parsed


def validate_categorical(raw_series, stored, variable, profile_id):
    raw = distribution(raw_series, [item["category"] for item in stored["categories"]])
    assert raw["valid_n"] == stored["valid_n"], (variable, profile_id, raw["valid_n"], stored["valid_n"])
    for actual, expected in zip(raw["categories"], stored["categories"]):
        assert actual["category"] == expected["category"]
        assert actual["count"] == expected["count"], (variable, profile_id, actual, expected)
        assert abs(actual["percent"] - expected["percent"]) <= 0.1


def validate_ordered(raw_series, stored, variable, profile_id):
    valid = pd.to_numeric(raw_series, errors="coerce").dropna()
    assert len(valid) == stored["valid_n"], (variable, profile_id, len(valid), stored["valid_n"])
    assert math.isclose(float(valid.median()), stored["median"], abs_tol=0.005)
    assert math.isclose(float(valid.quantile(0.25)), stored["q1"], abs_tol=0.005)
    assert math.isclose(float(valid.quantile(0.75)), stored["q3"], abs_tol=0.005)


def main():
    spec = pd.read_csv(SPEC).fillna("")
    profile_summary = pd.read_csv(PROFILE_SUMMARY).fillna("")
    assignments = pd.read_csv(ASSIGNMENTS)
    profile_results = pd.read_csv(PROFILE_RESULTS).fillna("")
    profile_labels = pd.read_csv(PROFILE_LABELS).fillna("")
    labels = pd.read_csv(LABELS, low_memory=False)
    values = pd.read_csv(VALUES, low_memory=False)
    courses = pd.read_csv(COURSES).fillna("")

    spec_by_id = {row["metric_id"]: row for _, row in spec.iterrows()}
    missing_metrics = REQUIRED_METRICS - set(spec_by_id)
    assert not missing_metrics, f"Missing governed metrics: {sorted(missing_metrics)}"
    for metric_id in REQUIRED_METRICS:
        assert "F_employment_security" in spec_by_id[metric_id]["applicable_profiles"]

    assert len(assignments) == 81
    assert assignments["respondent_id"].nunique() == 81
    counts = assignments.groupby("employment_security_profile_id")["respondent_id"].nunique().to_dict()
    assert counts == {1: 29, 2: 52}, counts
    assert len(courses) == 87 and courses["course_id"].nunique() == 87

    ids = set(assignments["respondent_id"])
    labels_f = labels[labels["respondent_id"].isin(ids)].copy()
    values_f = values[values["respondent_id"].isin(ids)].copy()
    assert len(labels_f) == 81 and labels_f["respondent_id"].nunique() == 81
    assert len(values_f) == 81 and values_f["respondent_id"].nunique() == 81

    joined = (
        assignments.merge(labels_f, on="respondent_id", how="left", validate="one_to_one", suffixes=("", "__label"))
        .merge(values_f[["respondent_id", "monthly_income_band", "job_satisfaction"]], on="respondent_id", how="left", validate="one_to_one", suffixes=("", "__value"))
    )
    # Because assignment already contains job_satisfaction, force cleaned numeric source names explicitly.
    income_value_col = "monthly_income_band__value"
    satisfaction_value_col = "job_satisfaction__value" if "job_satisfaction__value" in joined else "job_satisfaction"

    label_rows = profile_labels[profile_labels["model_id"] == MODEL_ID]
    assert set(label_rows["profile_id"].astype(int)) == {1, 2}
    summary_rows = profile_summary[profile_summary["profile"].str.startswith("F_employment_security:")]
    assert len(summary_rows) == 2

    validation_checks = [
        "All required governed metric IDs were found and are applicable to F profiles.",
        "Frozen assignment cohort contains 81 unique respondents.",
        "Frozen profile sizes reproduce F-S1 n=29 and F-S2 n=52.",
        "Cleaned readable-label and internal-value joins are one-to-one on respondent_id.",
        "Course V2 contains 87 unique course records.",
    ]

    profiles = {}
    for profile_id, meta in PROFILE_META.items():
        members = joined[joined["employment_security_profile_id"] == profile_id].copy()
        label_row = label_rows[label_rows["profile_id"].astype(int) == profile_id].iloc[0]
        assert int(label_row["cluster_size"]) == meta["expected_n"]
        ambiguous = int(members["ambiguous_consensus_membership"].fillna(False).astype(bool).sum())
        profiles[meta["dashboard_id"]] = {
            "profile_id": meta["dashboard_id"],
            "frozen_profile_id": profile_id,
            "label": label_row["profile_label"],
            "dimension": label_row["dimension"],
            "size": meta["expected_n"],
            "cohort_n": 81,
            "cohort_share": round_pct(meta["expected_n"], 81),
            "ambiguous_n": ambiguous,
            "ambiguous_percent": round_pct(ambiguous, meta["expected_n"]),
        }

    # Defining distributions come directly from the frozen assignment file.
    defining_metrics = []
    for metric_id, variable in DEFINITIONS:
        item = {**spec_info(spec_by_id, metric_id), "variable": variable, "profiles": {}}
        for profile_id, meta in PROFILE_META.items():
            members = assignments[assignments["employment_security_profile_id"] == profile_id]
            item["profiles"][meta["dashboard_id"]] = distribution(members[variable])
            assert item["profiles"][meta["dashboard_id"]]["valid_n"] == meta["expected_n"]
        defining_metrics.append(item)
    validation_checks.append("All defining distributions use frozen assignment values and full profile denominators.")

    # Approved profiling values are read from the frozen profiling output and independently validated.
    profiling_metrics = []
    for metric_id, variable in PROFILING:
        governed = spec_info(spec_by_id, metric_id)
        result = profile_results[(profile_results["model_id"] == MODEL_ID) & (profile_results["variable"] == variable)]
        assert len(result) == 1
        result = result.iloc[0]
        categorical = result["variable_type"] == "categorical"
        stored = parse_profile_descriptives(result["profile_descriptives"], categorical)
        item = {
            **governed,
            "variable": variable,
            "variable_type": result["variable_type"],
            "effect_size_name": result["effect_size_name"],
            "effect_size": round(float(result["effect_size"]), 3),
            "raw_p_value": round(float(result["p_value"]), 6),
            "adjusted_p_value": round(float(result["p_adjusted_bh"]), 6),
            "conditional": str(result["conditional"]).lower() == "true",
            "gateway": result["gateway"] or None,
            "sparse": str(result["sparse_cells"]).lower() == "true",
            "sparse_expected_share": clean_scalar(result["sparse_expected_share"]),
            "profiles": {},
        }
        for profile_id, meta in PROFILE_META.items():
            members = joined[joined["employment_security_profile_id"] == profile_id]
            if categorical:
                raw_col = variable
                validate_categorical(members[raw_col], stored[profile_id], variable, profile_id)
                item["profiles"][meta["dashboard_id"]] = {
                    **stored[profile_id],
                    "missing_or_not_applicable_n": meta["expected_n"] - stored[profile_id]["valid_n"],
                }
            else:
                raw_col = income_value_col if variable == "monthly_income_band" else satisfaction_value_col
                validate_ordered(members[raw_col], stored[profile_id], variable, profile_id)
                item["profiles"][meta["dashboard_id"]] = {
                    **stored[profile_id],
                    "missing_n": meta["expected_n"] - stored[profile_id]["valid_n"],
                }
        profiling_metrics.append(item)
    validation_checks.append("All six approved profiling metrics reproduce stored valid n, counts/percentages or median/IQR values.")

    # Label maps make ordered codes understandable without changing stored analysis.
    value_label_maps = {}
    for variable in ("monthly_income_band", "job_satisfaction"):
        map_frame = labels_f[["respondent_id", variable]].merge(
            values_f[["respondent_id", variable]], on="respondent_id", suffixes=("_label", "_value")
        ).dropna()
        pairs = map_frame[[f"{variable}_value", f"{variable}_label"]].drop_duplicates().sort_values(f"{variable}_value")
        value_label_maps[variable] = [
            {"value": clean_scalar(row[f"{variable}_value"]), "label": row[f"{variable}_label"]}
            for _, row in pairs.iterrows()
        ]

    # Direct survey demand/context metrics from the cleaned readable-label file.
    direct_metrics = []
    for metric_id, variable in (
        ("F_EMPLOYMENT_SECURITY_DIRECT_PRE_01", "ideal_sector"),
        ("F_EMPLOYMENT_SECURITY_DIRECT_TRA_01", "plans_further_edu_f"),
    ):
        item = {**spec_info(spec_by_id, metric_id), "variable": variable, "profiles": {}}
        for profile_id, meta in PROFILE_META.items():
            members = joined[joined["employment_security_profile_id"] == profile_id]
            item["profiles"][meta["dashboard_id"]] = distribution(members[variable])
            assert item["profiles"][meta["dashboard_id"]]["valid_n"] == meta["expected_n"]
        direct_metrics.append(item)
    validation_checks.append("Preferred-sector and further-training distributions use respondents’ own cleaned readable-label answers.")

    supply_metric = spec_info(spec_by_id, "SUPPLY_001")
    area_counts = courses.groupby("skill_area")["course_id"].nunique().sort_values(ascending=False)
    catalogue_supply = {
        **supply_metric,
        "total_courses": int(courses["course_id"].nunique()),
        "areas": [{"area": area, "course_count": int(count)} for area, count in area_counts.items()],
    }
    assert sum(item["course_count"] for item in catalogue_supply["areas"]) == 87
    validation_checks.append("Catalogue broad-area counts sum to all 87 unique V2 course records.")

    payload = {
        "dashboard": {
            "title": "NYSC Officer Dashboard",
            "subtitle": "Officer decision-support · profile intelligence",
            "scope": "Branch F — employed youth",
            "model_id": MODEL_ID,
            "model_cohort_n": 81,
        },
        "governance": {
            "specification_file": str(SPEC.relative_to(ROOT)),
            "profile_summary_file": str(PROFILE_SUMMARY.relative_to(ROOT)),
            "group_warning": "These are group patterns. Profile membership does not mean every member has each characteristic.",
            "supply_warning": "Catalogue counts describe documented programme supply only. They are not course recommendations, capacity estimates, live intake information, or individual eligibility decisions.",
            "comparison_warning": "Compare F-S1 and F-S2 only. Do not compare these sample shares with other branches as population prevalence.",
        },
        "profiles": profiles,
        "defining_metrics": defining_metrics,
        "profiling_metrics": profiling_metrics,
        "direct_metrics": direct_metrics,
        "value_label_maps": value_label_maps,
        "catalogue_supply": catalogue_supply,
        "validation": {"passed": True, "checks": validation_checks},
    }

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Wrote {OUTPUT.relative_to(ROOT)}")
    print(f"Validated {len(validation_checks)} source checks; F-S1=29, F-S2=52, courses=87")


if __name__ == "__main__":
    main()
