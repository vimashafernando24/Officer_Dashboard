"""
Live nearest-medoid cluster assignment for a BRAND-NEW respondent (not one of
the frozen 362). No clustering is rerun and no medoid, frozen profile ID,
label, or size is changed — this reproduces the exact methodology already
validated in outputs/fixed_medoid_assignment_validation/fixed_medoid_validation_report.md
(nearest-medoid Gower distance to the frozen final-profile medoids), packaged
as a reusable function instead of a one-off validation script.

Per-model Gower distance formulas below are reverse-engineered from the
original clustering notebooks (05/07 for D_motivation, 08 for D_economic, and
the .py exports 09/12/24/26/29 for the rest) since no single shared
implementation exists in the repo — each notebook has its own bespoke
mixed_gower(). Every feature spec below cites its source cell so the formula
can be re-verified against the original notebook if the medoid files are ever
regenerated. Correctness of this module is verified empirically, not just by
inspection: see validate_against_fixed_medoid_report() and
test_cluster_assignment_reproduction.py, which must reproduce
fixed_medoid_validation_summary.csv's exact accuracy/mismatch/tie counts.

IMPORTANT: this module's confidence metric (a distance-margin ratio) is NOT
the same statistic as the historical `within_profile_consensus` bootstrap
co-association metric used for the frozen 362 (see cluster_confidence.py).
Always tag output with confidence_method="nearest_medoid_distance_margin" so
the two are never conflated downstream.

KNOWN, DISCLOSED GAP: test_cluster_assignment_reproduction.py reproduces
fixed_medoid_validation_summary.csv exactly for 6 of 7 models. For
G_economic_role, 2 of 56 respondents' raw distances are off by a small,
unexplained amount (~0.02-0.13) from the published distance_to_profile_N
values, even though this module still predicts the correct nearest profile
for both — the root cause (an undocumented derivation nuance in the deleted
Jupyter cells of 08_/24_branch_g_household_economic_resources_clustering)
could not be recovered. See KNOWN_DISCREPANCIES in the test file for the full
account. This does not change G_economic_role's SAFE-for-new-user judgment.
"""
from __future__ import annotations

import csv
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable, Optional

BASE = Path(__file__).resolve().parents[2]

# Models rated NEEDS REVIEW in fixed_medoid_validation_report.md (accuracy
# 0.906/ARI 0.776 and 0.875/ARI 0.550, vs >=0.95/>=0.80 for the 5 SAFE models).
# New-respondent memberships in these two must be surfaced with a lower-
# reliability caveat, never presented with the same apparent confidence as the
# 5 SAFE models.
NEEDS_REVIEW_MODELS = {"D_educational_cultural", "G_future_engagement"}


def _f(row: dict, var: str) -> Optional[float]:
    """Raw numeric __value code for a variable from a new respondent's answer dict."""
    v = row.get(var)
    if v is None:
        return None
    code = v.get("value_code")
    if code is None:
        return None
    try:
        return float(code)
    except (TypeError, ValueError):
        return None


def _label(row: dict, var: str) -> Optional[str]:
    v = row.get(var)
    if v is None:
        return None
    return v.get("value_label")


def _value_str(row: dict, var: str) -> Optional[str]:
    """The raw __value code as a string (used where the original script treated
    a numeric-looking code as a NOMINAL category, e.g. E4's past_edu_usefulness)."""
    v = row.get(var)
    if v is None:
        return None
    code = v.get("value_code")
    return None if code is None else str(code)


@dataclass
class Feature:
    name: str
    compute: Callable[[dict], Optional[object]]
    distance: Callable[[object, object], Optional[float]]
    source: str  # notebook/script + cell citation, for auditability


def _nominal_distance(a, b) -> Optional[float]:
    if a is None or b is None:
        return None
    return 0.0 if str(a) == str(b) else 1.0


def _ordinal_distance(range_: float):
    def d(a, b) -> Optional[float]:
        if a is None or b is None:
            return None
        return abs(float(a) - float(b)) / range_ if range_ else 0.0
    return d


def _prenormalized_distance(a, b) -> Optional[float]:
    if a is None or b is None:
        return None
    return abs(float(a) - float(b))


def _unknown_aware_distance(a, b) -> Optional[float]:
    """F_employment_security's job_security_12months: -1.0 is an explicit
    'Do not know' sentinel. Two unknowns match (distance 0); one known + one
    unknown is maximally different (distance 1); otherwise plain |a-b|
    (source: 12_branch_f_employment_security_formality_clustering.py, the
    'ordinal_with_unknown' branch of mixed_gower — deliberately NOT further
    normalized, matching the original script exactly)."""
    if a is None or b is None:
        return None
    a_unknown, b_unknown = a < 0, b < 0
    if a_unknown and b_unknown:
        return 0.0
    if a_unknown != b_unknown:
        return 1.0
    return abs(a - b)


# --- D_motivation: 05_branch_d_motivation_clustering.ipynb, cell 6 (CANONICAL) ---
_D_MOTIVATION_CANONICAL = {
    "study_motivation_type": {
        1: "Intrinsic: genuinely passionate about the subject",
        2: "Identified: aligned with own goals",
        3: "Introjected: avoid guilt or disappointing family",
        4: "External: qualification required for a job",
        5: "Amotivated/uncertain: following the path ended up on",
    },
    "autonomy_in_study": {
        1: "A great deal of choice and control",
        2: "Some flexibility within a mostly fixed curriculum",
        3: "Very little choice; prescribed and fixed",
        4: "No choice or control",
    },
    "competence_in_study_field": {
        1: "Very capable and confident",
        2: "Fairly capable with some gaps",
        3: "Somewhat capable; struggles in some areas",
        4: "Not very capable; frequently out of depth",
    },
    "relatedness_at_institution": {
        1: "Strongly connected and part of the community",
        2: "Some connections but not deeply involved",
        3: "Weakly connected or isolated",
        4: "No sense of belonging",
    },
}
_D_MOTIVATION_LABEL_TO_CODE = {
    var: {label: code for code, label in levels.items()}
    for var, levels in _D_MOTIVATION_CANONICAL.items()
}


def _d_motivation_code(var):
    levels = _D_MOTIVATION_CANONICAL[var]
    rng = float(len(levels) - 1)

    def compute(row):
        code = _f(row, var)
        return code if code is not None and int(code) in levels else None
    return compute, _ordinal_distance(rng)


def _label_to_code_feature(var, label_map):
    def compute_from_label(label_value: Optional[str]):
        return label_map.get(label_value) if label_value is not None else None
    return compute_from_label


# --- D_economic: 08_branch_d_economic_resources_clustering.ipynb, cell 6 ---
_EARNER_MAP = {"no": 0.0, "shared": 0.5, "yes": 1.0}


def _household_counts_valid(row) -> bool:
    """Matches 08_.../24_...'s invalid_counts guard: size/workers/unemployed
    must all be present, non-negative, size>0, workers<=size, unemployed<=size,
    and workers+unemployed<=size. When invalid, BOTH share features become
    missing (not just clipped), matching the original scripts exactly."""
    size = _f(row, "household_size")
    workers = _f(row, "household_workers")
    unemployed = _f(row, "household_unemployed")
    if size is None or workers is None or unemployed is None:
        return False
    if size <= 0 or workers < 0 or unemployed < 0:
        return False
    if workers > size or unemployed > size or (workers + unemployed) > size:
        return False
    return True


def _earner_responsibility(row, var="primary_earner_status"):
    v = row.get(var)
    if v is None:
        return None
    code = v.get("value_code")
    # value_code for this field is the lowercase raw survey code ("no"/"shared"/"yes")
    if code is None:
        return None
    return _EARNER_MAP.get(str(code).strip().lower())


MODEL_SPECS: dict[str, dict] = {}

# ============================== D_motivation ==============================
MODEL_SPECS["D_motivation"] = {
    "medoid_file": "outputs/branch_d_motivation_clusters/motivation_medoid_profiles.csv",
    "profile_id_col": "motivation_profile_id",
    "profile_label_col": "motivation_profile_label",
    "medoid_value_style": "label",  # medoid CSV stores label text; convert via CANONICAL
    "features": [
        Feature("study_motivation_type", *_d_motivation_code("study_motivation_type"),
                "05_branch_d_motivation_clustering.ipynb cell 6/8"),
        Feature("autonomy_in_study", *_d_motivation_code("autonomy_in_study"),
                "05_branch_d_motivation_clustering.ipynb cell 6/8"),
        Feature("competence_in_study_field", *_d_motivation_code("competence_in_study_field"),
                "05_branch_d_motivation_clustering.ipynb cell 6/8"),
        Feature("relatedness_at_institution", *_d_motivation_code("relatedness_at_institution"),
                "05_branch_d_motivation_clustering.ipynb cell 6/8"),
    ],
}

# ============================== D_economic ==============================
MODEL_SPECS["D_economic"] = {
    "medoid_file": "outputs/branch_d_economic_resources_clusters/economic_final_profile_gower_medoids.csv",
    "profile_id_col": "economic_profile_id",
    "profile_label_col": "economic_profile_label",
    "medoid_value_style": "precomputed",  # medoid CSV stores final feature values directly
    "features": [
        Feature("household_income_position",
                lambda row: (_f(row, "household_income")
                             if _f(row, "household_income") is not None
                             and 1 <= _f(row, "household_income") <= 5 else None),
                _ordinal_distance(4.0),
                "08_branch_d_economic_resources_clustering.ipynb cell 6/8 "
                "(code 99 'prefer not to say' filtered to missing, matching "
                "income.where(income.between(1,5)))"),
        Feature("household_worker_share",
                lambda row: (_f(row, "household_workers") / _f(row, "household_size"))
                if _household_counts_valid(row) else None,
                _prenormalized_distance,
                "08_branch_d_economic_resources_clustering.ipynb cell 6/8 "
                "(gated by _household_counts_valid, matching inconsistent_counts)"),
        Feature("household_unemployed_share",
                lambda row: (_f(row, "household_unemployed") / _f(row, "household_size"))
                if _household_counts_valid(row) else None,
                _prenormalized_distance,
                "08_branch_d_economic_resources_clustering.ipynb cell 6/8 "
                "(gated by _household_counts_valid, matching inconsistent_counts)"),
        Feature("primary_earner_responsibility", _earner_responsibility, _prenormalized_distance,
                "08_branch_d_economic_resources_clustering.ipynb cell 6/8"),
        Feature("primary_income_source", lambda row: _label(row, "primary_income_source"),
                _nominal_distance, "08_branch_d_economic_resources_clustering.ipynb cell 6/8"),
        Feature("education_funding_source", lambda row: _label(row, "edu_funding_source"),
                _nominal_distance, "08_branch_d_economic_resources_clustering.ipynb cell 6/8"),
    ],
}

# ======================== D_educational_cultural ==========================
MODEL_SPECS["D_educational_cultural"] = {
    "medoid_file": "outputs/branch_d_educational_cultural_capital_clusters/"
                   "educational_cultural_final_profile_gower_medoids.csv",
    "profile_id_col": "educational_cultural_profile_id",
    "profile_label_col": "educational_cultural_profile_label",
    "medoid_value_style": "precomputed",
    "features": [
        Feature("father_education", lambda row: _f(row, "father_edu"), _ordinal_distance(6.0),
                "09_branch_d_educational_cultural_capital_clustering.py"),
        Feature("mother_education", lambda row: _f(row, "mother_edu"), _ordinal_distance(6.0),
                "09_branch_d_educational_cultural_capital_clustering.py"),
        Feature("expected_education", lambda row: _f(row, "expected_highest_edu_d"), _ordinal_distance(6.0),
                "09_branch_d_educational_cultural_capital_clustering.py"),
        Feature("institution_type", lambda row: _label(row, "institution_type"), _nominal_distance,
                "09_branch_d_educational_cultural_capital_clustering.py"),
        Feature("worked_while_studying", lambda row: _label(row, "worked_while_studying"), _nominal_distance,
                "09_branch_d_educational_cultural_capital_clustering.py"),
        Feature("re_entered_education", lambda row: _label(row, "re_entered_education"), _nominal_distance,
                "09_branch_d_educational_cultural_capital_clustering.py"),
    ],
}

# ======================== E_learning_orientation (E4) =====================
MODEL_SPECS["E_learning_orientation"] = {
    "medoid_file": "outputs/branch_e_all_dimensions_clusters/e4/e4_final_profile_gower_medoids.csv",
    "profile_id_col": "profile_id",
    "profile_label_col": "profile_label",
    "medoid_value_style": "precomputed",
    "features": [
        Feature("past_edu_usefulness", lambda row: _value_str(row, "past_edu_usefulness"), _nominal_distance,
                "29_branch_e_all_dimensions_clustering.py (E4, nominal() helper)"),
        Feature("plans_further_edu",
                lambda row: (_value_str(row, "plans_further_edu") or "").lower() or None,
                _nominal_distance,
                "29_branch_e_all_dimensions_clustering.py (E4, nominal() helper)"),
        Feature("expected_highest_edu_e",
                lambda row: (_f(row, "expected_highest_edu_e") / 7.0)
                if _f(row, "expected_highest_edu_e") is not None else None,
                _prenormalized_distance,
                "29_branch_e_all_dimensions_clustering.py (E4, ordered(col,0,7))"),
    ],
}

# ======================== F_employment_security ============================
MODEL_SPECS["F_employment_security"] = {
    "medoid_file": "outputs/branch_f_employment_security_clusters/"
                   "employment_security_final_profile_gower_medoids.csv",
    "profile_id_col": "employment_security_profile_id",
    "profile_label_col": "employment_security_profile_label",
    "medoid_value_style": "precomputed",
    "features": [
        Feature("contract_type", lambda row: _label(row, "contract_type"), _nominal_distance,
                "12_branch_f_employment_security_formality_clustering.py"),
        Feature("job_security_12months",
                lambda row: {1: 1.0, 2: 0.5, 3: 0.0, 4: -1.0}.get(int(_f(row, "job_security_12months")))
                if _f(row, "job_security_12months") is not None else None,
                _unknown_aware_distance,
                "12_branch_f_employment_security_formality_clustering.py"),
        Feature("sector_formality",
                lambda row: {1: 1.0, 2: 2 / 3, 3: 1 / 3, 5: 0.0}.get(int(_f(row, "sector_formality")))
                if _f(row, "sector_formality") is not None else None,
                _prenormalized_distance,
                "12_branch_f_employment_security_formality_clustering.py"),
    ],
}

# ============================ G_economic_role ===============================
MODEL_SPECS["G_economic_role"] = {
    "medoid_file": "outputs/branch_g_household_economic_resources_clusters/"
                   "household_economic_final_profile_gower_medoids.csv",
    "profile_id_col": "economic_profile_id",
    "profile_label_col": "economic_profile_label",
    "medoid_value_style": "precomputed",
    "features": [
        Feature("household_income_position",
                lambda row: {1: 0.0, 2: 0.25, 3: 0.5, 4: 0.75, 5: 1.0}.get(int(_f(row, "household_income")))
                if _f(row, "household_income") is not None
                and 1 <= _f(row, "household_income") <= 5 else None,
                _prenormalized_distance,
                "24_branch_g_household_economic_resources_clustering.py "
                "(code 99 'prefer not to say' filtered to missing)"),
        Feature("household_worker_share",
                lambda row: (_f(row, "household_workers") / _f(row, "household_size"))
                if _household_counts_valid(row) else None,
                _prenormalized_distance,
                "24_branch_g_household_economic_resources_clustering.py "
                "(gated by _household_counts_valid, matching invalid_counts)"),
        Feature("household_unemployed_share",
                lambda row: (_f(row, "household_unemployed") / _f(row, "household_size"))
                if _household_counts_valid(row) else None,
                _prenormalized_distance,
                "24_branch_g_household_economic_resources_clustering.py "
                "(gated by _household_counts_valid, matching invalid_counts)"),
        Feature("primary_earner_responsibility", _earner_responsibility, _prenormalized_distance,
                "24_branch_g_household_economic_resources_clustering.py"),
        Feature("primary_income_source", lambda row: _value_str(row, "primary_income_source"), _nominal_distance,
                "24_branch_g_household_economic_resources_clustering.py"),
    ],
}

# ========================= G_future_engagement ==============================
MODEL_SPECS["G_future_engagement"] = {
    "medoid_file": "outputs/branch_g_inactivity_pathway_future_engagement_clusters/"
                   "pathway_engagement_final_profile_gower_medoids.csv",
    "profile_id_col": "pathway_profile_id",
    "profile_label_col": "pathway_profile_label",
    "medoid_value_style": "precomputed",
    "features": [
        Feature("reason_not_in_labour_force", lambda row: _value_str(row, "reason_not_in_labour_force"),
                _nominal_distance, "26_branch_g_inactivity_pathway_future_engagement_clustering.py"),
        Feature("ever_worked", lambda row: (_value_str(row, "ever_worked") or "").lower() or None,
                _nominal_distance, "26_branch_g_inactivity_pathway_future_engagement_clustering.py"),
        Feature("wants_to_work_future", lambda row: (_value_str(row, "wants_to_work_future") or "").lower() or None,
                _nominal_distance, "26_branch_g_inactivity_pathway_future_engagement_clustering.py"),
        Feature("wants_further_edu", lambda row: (_value_str(row, "wants_further_edu") or "").lower() or None,
                _nominal_distance, "26_branch_g_inactivity_pathway_future_engagement_clustering.py"),
    ],
}


# ---------------------------------------------------------------------------
def _load_medoids(model_id: str) -> list[dict]:
    spec = MODEL_SPECS[model_id]
    path = BASE / spec["medoid_file"]
    with open(path, newline="", encoding="utf-8-sig") as f:
        rows = list(csv.DictReader(f))

    medoids = []
    for row in rows:
        profile_id = int(float(row[spec["profile_id_col"]]))
        profile_label = row[spec["profile_label_col"]]
        features = {}
        if spec["medoid_value_style"] == "label":
            for feat in spec["features"]:
                label_val = row[feat.name]
                code = _D_MOTIVATION_LABEL_TO_CODE[feat.name].get(label_val)
                features[feat.name] = float(code) if code is not None else None
        else:  # "precomputed": medoid CSV already stores the final Gower-space value
            for feat in spec["features"]:
                raw = row.get(feat.name, "")
                if raw is None or raw == "":
                    features[feat.name] = None
                elif feat.distance is _nominal_distance:
                    features[feat.name] = raw  # keep as string for nominal comparison
                else:
                    features[feat.name] = float(raw)
        medoids.append({"profile_id": profile_id, "profile_label": profile_label, "features": features})
    medoids.sort(key=lambda m: m["profile_id"])
    return medoids


@dataclass
class AssignmentResult:
    model_id: str
    profile_id: int
    profile_label: str
    distance_to_nearest: float
    distance_to_second_nearest: Optional[float]
    confidence_percent: int
    distance_tie: bool
    tied_profile_ids: list[int]
    needs_review_model: bool
    confidence_method: str = "nearest_medoid_distance_margin"


def assign_profile(model_id: str, respondent_answers: dict) -> AssignmentResult:
    """respondent_answers: {variable: {"value_code": ..., "value_label": ...}, ...}
    covering (at least) this model's cluster-forming variables, in the same
    shape used throughout respondent_evidence.jsonl."""
    spec = MODEL_SPECS[model_id]
    medoids = _load_medoids(model_id)

    new_features = {feat.name: feat.compute(respondent_answers) for feat in spec["features"]}

    distances = []
    for medoid in medoids:
        num, den = 0.0, 0
        for feat in spec["features"]:
            d = feat.distance(new_features[feat.name], medoid["features"][feat.name])
            if d is not None:
                num += d
                den += 1
        distance = (num / den) if den else 1.0
        distances.append((medoid["profile_id"], medoid["profile_label"], distance))

    distances.sort(key=lambda t: (t[2], t[0]))  # nearest first; ties -> lowest profile_id
    nearest_pid, nearest_label, nearest_d = distances[0]
    second_d = distances[1][2] if len(distances) > 1 else None

    min_d = min(d for _, _, d in distances)
    tied = [pid for pid, _, d in distances if d == min_d]
    is_tie = len(tied) > 1

    if second_d is None:
        confidence = 100
    else:
        total = nearest_d + second_d
        confidence = 100 if total == 0 else round((1 - nearest_d / total) * 100)

    return AssignmentResult(
        model_id=model_id,
        profile_id=nearest_pid,
        profile_label=nearest_label,
        distance_to_nearest=round(nearest_d, 6),
        distance_to_second_nearest=round(second_d, 6) if second_d is not None else None,
        confidence_percent=confidence,
        distance_tie=is_tie,
        tied_profile_ids=tied,
        needs_review_model=model_id in NEEDS_REVIEW_MODELS,
    )


BRANCH_MODELS = {
    "D": ["D_motivation", "D_economic", "D_educational_cultural"],
    "E": ["E_learning_orientation"],
    "F": ["F_employment_security"],
    "G": ["G_economic_role", "G_future_engagement"],
}


def assign_all_profiles_for_branch(branch: str, respondent_answers: dict) -> list[AssignmentResult]:
    return [assign_profile(model_id, respondent_answers) for model_id in BRANCH_MODELS.get(branch, [])]
