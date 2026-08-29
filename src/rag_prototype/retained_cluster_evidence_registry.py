"""Governed registry for officer-facing cluster evidence.

This module separates three things that must never be conflated:

1. cluster-defining variables: the variables used by the retained clustering
   model and by nearest-medoid assignment;
2. retained profile findings: post-cluster findings explicitly kept in the
   final analysis' ``programme_relevant_findings`` field; and
3. context-eligible findings: retained findings that are useful for this
   member's current officer conversation or programme decision.

Raw survey columns, complete profile distributions, and merely available
statistics are not evidence sources here.  The registry is deliberately
explicit for all seven retained models and all 17 retained profiles.
"""
from __future__ import annotations

import csv
import re
from pathlib import Path


BASE = Path(__file__).resolve().parents[2]
FINAL_PROFILE_CSV = BASE / "outputs/final_cluster_programme_relevant_profiles.csv"
FINAL_COMPARISON_CSV = BASE / "outputs/final_cluster_profile_comparison_summary.csv"
FINAL_NOTEBOOK = "30_final_cluster_profile_analysis.ipynb"
FINAL_REPORT = "final_cluster_profiling_report.md"


# Exact raw survey variables that formed each retained model.  These are used
# only to explain assignment, never as post-cluster evidence for a programme.
CLUSTER_DEFINING_REGISTRY = {
    "D_motivation": {
        "variables": (
            "study_motivation_type", "autonomy_in_study",
            "competence_in_study_field", "relatedness_at_institution",
        ),
        "provenance": "05_branch_d_motivation_clustering.ipynb cells 6/8",
    },
    "D_economic": {
        "variables": (
            "household_income", "household_size", "household_workers",
            "household_unemployed", "primary_earner_status",
            "primary_income_source", "edu_funding_source",
        ),
        "provenance": "08_branch_d_economic_resources_clustering.ipynb cells 6/8",
    },
    "D_educational_cultural": {
        "variables": (
            "father_edu", "mother_edu", "expected_highest_edu_d",
            "institution_type", "worked_while_studying", "re_entered_education",
        ),
        "provenance": "09_branch_d_educational_cultural_capital_clustering.py",
    },
    "E_learning_orientation": {
        "variables": (
            "past_edu_usefulness", "plans_further_edu", "expected_highest_edu_e",
        ),
        "provenance": "29_branch_e_all_dimensions_clustering.py, retained E4 model",
    },
    "F_employment_security": {
        "variables": ("contract_type", "job_security_12months", "sector_formality"),
        "provenance": "12_branch_f_employment_security_formality_clustering.py",
    },
    "G_economic_role": {
        "variables": (
            "household_income", "household_size", "household_workers",
            "household_unemployed", "primary_earner_status", "primary_income_source",
        ),
        "provenance": "24_branch_g_household_economic_resources_clustering.py",
    },
    "G_future_engagement": {
        "variables": (
            "reason_not_in_labour_force", "ever_worked",
            "wants_to_work_future", "wants_further_edu",
        ),
        "provenance": "26_branch_g_inactivity_pathway_future_engagement_clustering.py",
    },
}


# Explicit profile-level allowlist recovered from the final analysis output,
# specifically its programme_relevant_findings column.  Do not replace this
# with "every screened variable" or infer it from the distribution section.
PROFILE_RETAINED_VARIABLES = {
    "D_motivation_p1": ("employment_network_quality",),
    "D_motivation_p2": ("employment_network_quality",),
    "D_motivation_p3": ("employment_network_quality",),
    "D_economic_p1": (
        "ideal_sector", "study_field_preference", "institution_type", "job_search_method_d",
    ),
    "D_economic_p2": (
        "ideal_sector", "study_field_preference", "institution_type", "job_search_method_d",
    ),
    "D_educational_cultural_p1": (
        "already_job_searching", "primary_income_source", "edu_funding_source", "household_income",
    ),
    "D_educational_cultural_p2": (
        "already_job_searching", "primary_income_source", "edu_funding_source", "household_income",
    ),
    "D_educational_cultural_p3": (
        "already_job_searching", "primary_income_source", "edu_funding_source", "household_income",
    ),
    "D_educational_cultural_p4": (
        "already_job_searching", "primary_income_source", "edu_funding_source", "household_income",
    ),
    "E_learning_orientation_p1": (
        "job_acceptance_conditions", "network_helpfulness",
        "search_method_primary", "social_support_job_search",
    ),
    "E_learning_orientation_p2": (
        "job_acceptance_conditions", "network_helpfulness",
        "search_method_primary", "social_support_job_search",
    ),
    "F_employment_security_p1": (
        "monthly_income_band", "primary_income_source", "hopes_to_change_job", "job_satisfaction",
    ),
    "F_employment_security_p2": (
        "monthly_income_band", "primary_income_source", "hopes_to_change_job", "job_satisfaction",
    ),
    "G_economic_role_p1": (
        "employment_network_quality", "labour_market_connection",
        "employment_self_efficacy", "most_important_life_goal",
    ),
    "G_economic_role_p2": (
        "employment_network_quality", "labour_market_connection",
        "employment_self_efficacy", "most_important_life_goal",
    ),
    "G_future_engagement_p1": (
        "employment_self_efficacy", "support_for_engagement",
        "labour_market_connection", "future_orientation_g",
    ),
    "G_future_engagement_p2": (
        "employment_self_efficacy", "support_for_engagement",
        "labour_market_connection", "future_orientation_g",
    ),
}


# Context policies are intentionally deterministic and applied before prompt
# construction.  GPT never gets a non-matching retained finding and is never
# asked to decide which of all available statistics "sounds relevant".
CONTEXT_POLICY = {
    ("D_motivation", "employment_network_quality"): {"topics": {"job_search", "self_employment", "further_education", "exploration"}},
    ("D_economic", "ideal_sector"): {"mode": "matching_current_direction"},
    ("D_economic", "study_field_preference"): {"mode": "matching_current_direction"},
    ("D_economic", "institution_type"): {"mode": "missing_corresponding_intake_fact"},
    ("D_economic", "job_search_method_d"): {"topics": {"job_search"}},
    ("D_educational_cultural", "already_job_searching"): {"topics": {"job_search"}},
    ("D_educational_cultural", "primary_income_source"): {"mode": "missing_corresponding_intake_fact"},
    ("D_educational_cultural", "edu_funding_source"): {"mode": "missing_corresponding_intake_fact"},
    ("D_educational_cultural", "household_income"): {"mode": "missing_corresponding_intake_fact"},
    ("E_learning_orientation", "job_acceptance_conditions"): {"topics": {"job_entry"}},
    ("E_learning_orientation", "network_helpfulness"): {"topics": {"job_search"}},
    ("E_learning_orientation", "search_method_primary"): {"topics": {"job_search"}},
    ("E_learning_orientation", "social_support_job_search"): {"topics": {"job_search"}},
    ("F_employment_security", "monthly_income_band"): {"mode": "missing_corresponding_intake_fact"},
    ("F_employment_security", "primary_income_source"): {"mode": "missing_corresponding_intake_fact"},
    ("F_employment_security", "hopes_to_change_job"): {"topics": {"job_entry", "job_retention"}},
    ("F_employment_security", "job_satisfaction"): {"topics": {"job_entry", "job_retention"}},
    ("G_economic_role", "employment_network_quality"): {"topics": {"job_search", "self_employment", "further_education", "exploration"}},
    ("G_economic_role", "labour_market_connection"): {"topics": {"job_search", "self_employment", "exploration"}},
    ("G_economic_role", "employment_self_efficacy"): {"topics": {"job_search", "self_employment", "further_education", "exploration"}},
    ("G_economic_role", "most_important_life_goal"): {"topics": {"exploration"}},
    ("G_future_engagement", "employment_self_efficacy"): {"topics": {"job_search", "self_employment", "further_education", "exploration"}},
    ("G_future_engagement", "support_for_engagement"): {"topics": {"job_search", "self_employment", "further_education", "exploration"}},
    ("G_future_engagement", "labour_market_connection"): {"topics": {"job_search", "self_employment", "exploration"}},
    ("G_future_engagement", "future_orientation_g"): {"topics": {"job_search", "self_employment", "further_education", "exploration"}},
}


PERCENT_MARGIN_RE = re.compile(r"\(\d+/\d+, ([\d.]+)% vs ([\d.]+)% in other profile")
MEDIAN_MARGIN_RE = re.compile(r"had (?:lower|higher) median .+? \(([\d.]+) vs ([\d.]+)\)")
QUOTED_VALUE_RE = re.compile(r"[‘\"]([^’\"]+)[’\"]")


def _model_id(profile_key: str) -> str:
    return profile_key.rsplit("_p", 1)[0]


def _finding_margin_points(text: str):
    match = PERCENT_MARGIN_RE.search(text)
    if match:
        return abs(float(match.group(1)) - float(match.group(2)))
    if MEDIAN_MARGIN_RE.search(text):
        return None
    return None


def _load_final_retained_rows() -> dict:
    rows = {}
    with open(FINAL_PROFILE_CSV, newline="", encoding="utf-8-sig") as handle:
        for row in csv.DictReader(handle):
            key = f"{row['model_id']}_p{row['profile_id']}"
            findings = tuple(
                item.strip() for item in row["programme_relevant_findings"].split(" | ")
                if item.strip() and not item.startswith("No clear additional difference")
            )
            rows[key] = {"row": row, "findings": findings}
    return rows


def _finding_text_by_label(parsed: dict) -> dict:
    result = {}
    for category in parsed["supported_findings"]["categories"]:
        for bullet in category["findings"]:
            result.setdefault(bullet.split(":", 1)[0].strip(), bullet)
    return result


def _stat_by_variable(parsed: dict) -> dict:
    return {stat["variable"]: stat for stat in parsed["supported_findings"]["statistical_detail"]}


def _interpretation_guard(variable: str, finding: str, parsed: dict) -> str:
    """Keep a retained between-profile difference from becoming a false mode claim.

    This does not widen the evidence registry: it inspects only the already
    allowlisted variable's own display distribution and supplies a constraint
    on how the retained finding may be worded. It is especially important when
    the category named by the final analysis is tied with another response, or
    is differentiating without being the within-profile mode.
    """
    distribution = next(
        (item for item in parsed["distributions"] if item.get("variable") == variable),
        None,
    )
    items = (distribution or {}).get("distribution") or []
    if not items:
        return (
            "Treat this only as the retained between-profile comparison stated above; "
            "do not turn it into a claim that one response was the profile's most common answer."
        )

    highest = max(item["percent"] for item in items)
    leaders = [item for item in items if abs(item["percent"] - highest) < 0.05]
    quoted = QUOTED_VALUE_RE.search(finding)
    quoted_value = quoted.group(1) if quoted else None
    if len(leaders) > 1:
        leader_names = "; ".join(item["value"] for item in leaders)
        return (
            f"Within this profile there is a joint-highest tie at {highest:.1f}% between: "
            f"{leader_names}. The retained statement about {quoted_value or variable} is a "
            "between-profile difference, not evidence that it is the sole primary, dominant, "
            "top, or most common response. Mention the tie whenever summarising this finding."
        )

    leader = leaders[0]
    if quoted_value and quoted_value != leader["value"]:
        return (
            f"The most common answer within this profile was {leader['value']} ({highest:.1f}%). "
            f"The retained statement highlights {quoted_value} only because it differed between "
            "profiles. Do not call the highlighted category primary, dominant, top, or most common."
        )
    return (
        f"The most common answer within this profile was {leader['value']} ({highest:.1f}%). "
        "Keep any wording proportional and distinguish this within-profile pattern from the "
        "retained between-profile comparison."
    )


def _provenance(profile_key: str, variable: str) -> dict:
    model_id = _model_id(profile_key)
    profile_id = profile_key.rsplit("_p", 1)[1]
    return {
        "retention_source": (
            f"outputs/final_cluster_programme_relevant_profiles.csv row "
            f"model_id={model_id}, profile_id={profile_id}, column=programme_relevant_findings"
        ),
        "analysis_source": f"{FINAL_NOTEBOOK} -> {FINAL_REPORT}",
        "statistical_source": (
            f"{FINAL_COMPARISON_CSV.relative_to(BASE)} row "
            f"model_id={model_id}, variable={variable}"
        ),
    }


def select_retained_evidence(parsed: dict) -> list[dict]:
    """Return only findings explicitly retained in the final profile analysis.

    The explicit code registry and the frozen final CSV must agree exactly.
    Any disagreement fails loudly instead of widening the evidence base.
    """
    profile_key = parsed.get("header", {}).get("profile_key")
    if profile_key not in PROFILE_RETAINED_VARIABLES:
        raise ValueError(f"No retained-evidence registry entry for profile '{profile_key}'")

    final_rows = _load_final_retained_rows()
    if profile_key not in final_rows:
        raise ValueError(f"No final retained profile row for '{profile_key}'")

    allowed_variables = PROFILE_RETAINED_VARIABLES[profile_key]
    final_texts = set(final_rows[profile_key]["findings"])
    text_by_label = _finding_text_by_label(parsed)
    stats = _stat_by_variable(parsed)
    retained = []

    for variable in allowed_variables:
        stat = stats.get(variable)
        if not stat:
            raise ValueError(f"{profile_key}: retained variable '{variable}' has no statistical-detail row")
        text = text_by_label.get(stat["label"])
        if not text:
            raise ValueError(f"{profile_key}: retained variable '{variable}' has no reported profile finding")
        if text not in final_texts:
            raise ValueError(
                f"{profile_key}: '{variable}' is allowlisted but its finding is absent from the final "
                "programme_relevant_findings field"
            )
        retained.append({
            "variable": variable,
            "label": stat["label"],
            "finding": text,
            "interpretation_guard": _interpretation_guard(variable, text, parsed),
            "programme_relevance": stat["programme_relevance"],
            "effect_size": stat["effect_size"],
            "effect_size_name": stat["effect_size_name"],
            "margin_percentage_points": _finding_margin_points(text),
            "provenance": _provenance(profile_key, variable),
        })

    unexpected_final = final_texts - {item["finding"] for item in retained}
    if unexpected_final:
        raise ValueError(
            f"{profile_key}: final programme_relevant_findings contains unregistered finding(s): "
            f"{sorted(unexpected_final)}"
        )
    return retained


def _context_topics(context: dict) -> set[str]:
    reason = str(context.get("q2_reason") or "").strip().lower()
    topics = set()
    if "get a job" in reason:
        topics.update({"job_entry", "job_search"})
    elif "current job" in reason:
        topics.update({"job_retention", "skill_development"})
    elif "business" in reason:
        topics.update({"self_employment"})
    elif "further education" in reason:
        topics.update({"further_education"})
    elif "general skills" in reason or "not sure" in reason:
        topics.update({"exploration"})
    if context.get("ideal_sector") or context.get("q1_occupation_focus"):
        topics.add("course_direction")
    if str(context.get("q5_qualification") or "").lower().startswith("yes"):
        topics.add("qualification")
    return topics


def _direction_matches(finding: str, context: dict) -> bool:
    match = QUOTED_VALUE_RE.search(finding)
    if not match:
        return False
    finding_value = match.group(1).lower()
    current = " ".join(str(context.get(k) or "") for k in ("ideal_sector", "q1_occupation_focus")).lower()
    concept_groups = (
        {"information technology", "communications", "ict", "computing", "software", "computer"},
        {"manufacturing", "production", "industrial", "technical", "machinist", "mechanic"},
        {"education", "teaching", "teacher"},
        {"commerce", "business", "management", "finance", "banking"},
        {"health", "nursing", "wellbeing", "care"},
        {"construction", "building"},
        {"hospitality", "hotel", "restaurant"},
        {"agriculture", "forestry", "fishing"},
        {"creative", "media", "arts"},
    )
    for group in concept_groups:
        if any(term in finding_value for term in group) and any(term in current for term in group):
            return True
    return finding_value in current or any(token in current for token in finding_value.split() if len(token) > 4)


def filter_retained_evidence_for_context(
    profile_key: str, retained_evidence: list[dict], context: dict,
) -> tuple[list[dict], list[dict]]:
    """Apply the second gate: retained finding + useful current context."""
    model_id = _model_id(profile_key)
    topics = _context_topics(context)
    eligible, rejected = [], []
    for evidence in retained_evidence:
        policy = CONTEXT_POLICY[(model_id, evidence["variable"])]
        mode = policy.get("mode")
        if mode == "missing_corresponding_intake_fact":
            rejected.append({
                **evidence,
                "decision": "rejected_current_context",
                "reason": (
                    "Retained historically, but the intake collected no corresponding individual fact; "
                    "using it here could manufacture a personal constraint or need."
                ),
            })
        elif mode == "matching_current_direction":
            if _direction_matches(evidence["finding"], context):
                eligible.append({
                    **evidence,
                    "context_reason": "The retained field/sector pattern matches the member's stated direction.",
                })
            else:
                rejected.append({
                    **evidence,
                    "decision": "rejected_current_context",
                    "reason": "The retained field/sector pattern does not match the member's stated direction.",
                })
        else:
            matched_topics = topics & set(policy.get("topics", ()))
            if matched_topics:
                eligible.append({
                    **evidence,
                    "context_reason": (
                        "Useful to the current officer context because the intake established: "
                        + ", ".join(sorted(matched_topics)) + "."
                    ),
                })
            else:
                rejected.append({
                    **evidence,
                    "decision": "rejected_current_context",
                    "reason": "Retained historically, but unrelated to the member's current intake purpose.",
                })
    return eligible, rejected


def audit_profile_evidence(parsed: dict, context: dict) -> dict:
    """Return a complete eligibility audit, including explored/rejected rows."""
    profile_key = parsed["header"]["profile_key"]
    allowlist = set(PROFILE_RETAINED_VARIABLES[profile_key])
    retained = select_retained_evidence(parsed)
    eligible, context_rejected = filter_retained_evidence_for_context(profile_key, retained, context)
    eligible_vars = {item["variable"] for item in eligible}
    context_rejected_by_var = {item["variable"]: item for item in context_rejected}
    text_by_label = _finding_text_by_label(parsed)

    decisions = []
    for stat in parsed["supported_findings"]["statistical_detail"]:
        variable = stat["variable"]
        text = text_by_label.get(stat["label"])
        base = {
            "profile_key": profile_key,
            "variable": variable,
            "label": stat["label"],
            "finding": text,
        }
        if variable in eligible_vars:
            item = next(item for item in eligible if item["variable"] == variable)
            decisions.append({**base, "decision": "eligible", "reason": item["context_reason"],
                              "provenance": item["provenance"]})
        elif variable in context_rejected_by_var:
            item = context_rejected_by_var[variable]
            decisions.append({**base, "decision": item["decision"], "reason": item["reason"],
                              "provenance": item["provenance"]})
        elif variable in allowlist:
            decisions.append({**base, "decision": "registry_error",
                              "reason": "Allowlisted variable failed registry validation."})
        elif text:
            decisions.append({
                **base,
                "decision": "rejected_not_retained",
                "reason": "Reported/explored in profiling, but not kept in the final programme_relevant_findings field.",
            })
        else:
            decisions.append({
                **base,
                "decision": "rejected_not_reported",
                "reason": "Statistically tested, but not retained as a reported profile finding in the final analysis.",
            })
    return {"profile_key": profile_key, "eligible": eligible, "rejected": context_rejected,
            "decisions": decisions}


def validate_registry() -> dict:
    """Validate seven models, 17 profiles, and exact final finding membership."""
    model_ids = set(CLUSTER_DEFINING_REGISTRY)
    profile_models = {_model_id(key) for key in PROFILE_RETAINED_VARIABLES}
    if model_ids != profile_models:
        raise ValueError(f"Registry model mismatch: models={model_ids}, profile_models={profile_models}")
    if len(PROFILE_RETAINED_VARIABLES) != 17:
        raise ValueError(f"Expected 17 profile allowlists, found {len(PROFILE_RETAINED_VARIABLES)}")
    for profile_key, variables in PROFILE_RETAINED_VARIABLES.items():
        model_id = _model_id(profile_key)
        missing_policy = [v for v in variables if (model_id, v) not in CONTEXT_POLICY]
        if missing_policy:
            raise ValueError(f"{profile_key}: missing context policy for {missing_policy}")
    return {"models": len(model_ids), "profiles": len(PROFILE_RETAINED_VARIABLES)}
