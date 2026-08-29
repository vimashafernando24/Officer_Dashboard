from pathlib import Path
import json

import pandas as pd


ROOT = Path.cwd()
RAW_PATH = ROOT / "nysc_survey.survey_responses23.json"
QUALITY_PATH = ROOT / "outputs/nysc_survey_quality_audit.csv"
VALUES_PATH = ROOT / "outputs/nysc_survey_cleaned_values.csv"
LABELS_PATH = ROOT / "outputs/nysc_survey_cleaned_labels.csv"
OUT_DIR = ROOT / "outputs/branch_g_variable_dimension_audit"
OUT_DIR.mkdir(parents=True, exist_ok=True)


DIMENSIONS = {
    "G1 — Household economic resources and dependency": {
        "framework": "Bourdieu economic capital + ILO SWTS household structure",
        "variables": [
            "household_income", "household_size", "household_workers",
            "household_unemployed", "primary_earner_status",
            "primary_income_source",
        ],
        "why": (
            "Captures the household resources available to inactive youth, the "
            "number of working/job-seeking household members, and dependence or "
            "responsibility for current income."
        ),
        "caution": (
            "These are raw indicators, not a validated economic-capital scale. "
            "Household counts require consistency checks, and primary income "
            "source may create a direct family-supported versus own-income split."
        ),
    },
    "G2 — Educational and inherited cultural capital": {
        "framework": "Bourdieu cultural capital + ILO SWTS education history",
        "variables": [
            "father_edu", "mother_edu", "edu_status",
            "worked_while_studying",
        ],
        "why": (
            "Represents family educational background, current/recent education "
            "position, and exposure to work while studying."
        ),
        "caution": (
            "Parental education is a proxy, not a measure of ability or merit. "
            "Highest completed education is conditional and is therefore a "
            "descriptor rather than an all-Branch-G input."
        ),
    },
    "G3 — Inactivity pathway and future engagement intention": {
        "framework": "ILO School-to-Work Transition Survey",
        "variables": [
            "reason_not_in_labour_force", "ever_worked",
            "wants_to_work_future", "wants_further_edu",
        ],
        "why": (
            "Distinguishes current reasons for inactivity, previous labour-market "
            "experience, and stated intentions to enter work or education."
        ),
        "caution": (
            "The inactivity reason is a direct nominal structural category and may "
            "dominate a partition. The intention questions are observed choices, "
            "not a latent readiness scale. Leave-one-feature-out and single-item "
            "dominance tests are mandatory."
        ),
    },
    "G4 — Psychological readiness and support for engagement": {
        "framework": "Self-Determination Theory extension recorded in the survey",
        "variables": [
            "future_orientation_g", "employment_self_efficacy",
            "support_for_engagement",
        ],
        "why": (
            "Combines direction/planning, perceived capability to find work or "
            "training, and anticipated support for re-engagement."
        ),
        "caution": (
            "The survey contains one item for each component. Cluster original "
            "ordered answers; do not construct or claim a validated SDT scale."
        ),
    },
    "G5 — Labour-market social connection": {
        "framework": "Bourdieu social capital",
        "variables": [
            "employment_network_quality", "labour_market_connection",
        ],
        "why": (
            "Measures access to people who could help and the flow of information "
            "about employment or training opportunities."
        ),
        "caution": (
            "Only two closely related indicators are available. They may be better "
            "reported as a cross-tabulation unless clustering is cross-method "
            "stable and adds more than a direct response-pattern table."
        ),
    },
}

SELECTED = {
    variable: dimension
    for dimension, specification in DIMENSIONS.items()
    for variable in specification["variables"]
}

ROUTING_AUDIT = {
    "current_activity_status", "desire_for_work", "active_search_4weeks",
    "search_method_primary", "wanted_to_work", "reason_not_seeking",
    "available_to_start", "has_job_to_return", "looking_while_absent",
}
CONDITIONAL_DESCRIPTORS = {
    "age_first_married", "spouse_activity", "num_children",
    "reason_left_edu", "highest_edu_completed", "edu_end_year",
    "spell1_activity", "spell2_activity", "spell1_is_current",
    "spell2_is_current", "spell1_contract", "spell1_satisfaction",
    "spell1_end_reason",
}
PROFILE_AND_MAPPING = {
    "age_group", "gender", "district", "area_type", "moved_from_origin",
    "move_reason", "marital_status", "has_children", "father_occ",
    "mother_occ", "work_while_study_type", "work_while_study_paid",
    "work_while_study_hours", "work_while_study_motivation",
    "edu_min_for_decent_job", "most_important_life_goal",
    "most_useful_quality_for_job", "ideal_work_type", "ideal_sector",
    "time_use_decision_maker", "expected_highest_edu_g",
}


def role_for(variable):
    if variable in SELECTED:
        return "proposed clustering input", SELECTED[variable]
    if variable in ROUTING_AUDIT:
        return "routing/audit only", "Not a clustering dimension"
    if variable in CONDITIONAL_DESCRIPTORS:
        return "conditional descriptor", "Not used in all-Branch-G distance"
    if variable in PROFILE_AND_MAPPING:
        return "profile/programme-mapping descriptor", "Not a clustering dimension"
    raise KeyError(f"Unclassified Branch G variable: {variable}")


# Select the strict new-structure final Branch G cohort.
quality = pd.read_csv(QUALITY_PATH)
selected_quality = quality.loc[
    quality["keep_final"].astype(bool)
    & quality["branch"].eq("G")
    & quality["branch_routing_source"].eq("translated_final_active_branch")
    & ~quality["branch_integrity_issue"].astype(bool)
].copy()
assert len(selected_quality) == 56

values_all = pd.read_csv(VALUES_PATH)
labels_all = pd.read_csv(LABELS_PATH)
selected_ids = selected_quality["respondent_id"].astype(str).tolist()
values = values_all.loc[
    values_all["respondent_id"].astype(str).isin(selected_ids)
].copy()
labels = labels_all.loc[
    labels_all["respondent_id"].astype(str).isin(selected_ids)
].copy()
assert len(values) == 56 and len(labels) == 56
assert values["respondent_id"].nunique() == 56

# Recover the full set of questions that appeared on an active path and their
# survey metadata. Coverage is calculated from the canonical cleaned tables so
# intermediate export layouts are not undercounted.
with open(RAW_PATH, encoding="utf-8") as handle:
    raw_records = json.load(handle)
metadata = {}
response_options = {}
for raw_index in selected_quality["raw_row"].astype(int):
    record = raw_records[raw_index]
    for question_id, item in record.get("answers", {}).items():
        if not isinstance(item, dict) or item.get("is_active_path") is False:
            continue
        variable = item.get("variable")
        if not variable:
            continue
        metadata.setdefault(variable, {
            "question_id": question_id,
            "survey_section": item.get("section"),
            "framework": item.get("framework"),
            "question_text": item.get("question_text"),
        })
        if item.get("label") is not None:
            response_options.setdefault(variable, set()).add(str(item["label"]))

answerable_variables = sorted(metadata)
assert len(answerable_variables) == 62
assert set(SELECTED).issubset(answerable_variables)

rows = []
response_rows = []
for variable in answerable_variables:
    role, dimension = role_for(variable)
    value_series = values[variable] if variable in values else pd.Series(dtype=object)
    label_series = labels[variable] if variable in labels else pd.Series(dtype=object)
    observed = int(value_series.notna().sum())
    for response, count in label_series.value_counts(dropna=False).items():
        response_rows.append({
            "variable": variable,
            "response": "[missing]" if pd.isna(response) else str(response),
            "records": int(count),
            "percent_of_56": round(100 * count / len(values), 1),
        })
    item = metadata[variable]
    rows.append({
        "question_id": item["question_id"],
        "survey_section": item["survey_section"],
        "variable": variable,
        "framework_recorded_in_survey": item["framework"],
        "question_text": item["question_text"],
        "observed_records": observed,
        "coverage_percent": round(100 * observed / len(values), 1),
        "unique_observed_responses": int(label_series.nunique(dropna=True)),
        "proposed_role": role,
        "proposed_dimension": dimension,
    })

variable_audit = pd.DataFrame(rows)
section_order = {"A": 0, "B": 1, "D": 2, "E": 3, "F": 4}
variable_audit["_section_order"] = variable_audit["survey_section"].map(
    section_order
).fillna(9)
variable_audit["_question_number"] = pd.to_numeric(
    variable_audit["question_id"].str.extract(r"(\d+)", expand=False),
    errors="coerce",
)
variable_audit = variable_audit.sort_values(
    ["_section_order", "_question_number", "question_id", "variable"]
).drop(columns=["_section_order", "_question_number"])
variable_audit.to_csv(OUT_DIR / "branch_g_all_62_variables.csv", index=False)
pd.DataFrame(response_rows).to_csv(
    OUT_DIR / "branch_g_variable_response_distributions.csv", index=False
)

dimension_rows = []
for dimension, specification in DIMENSIONS.items():
    selected = variable_audit.loc[
        variable_audit["variable"].isin(specification["variables"])
    ]
    dimension_rows.append({
        "dimension": dimension,
        "framework": specification["framework"],
        "variables": ", ".join(specification["variables"]),
        "number_of_inputs": len(specification["variables"]),
        "minimum_coverage_percent": selected["coverage_percent"].min(),
        "why_grouped": specification["why"],
        "caution": specification["caution"],
        "clustering_status": "candidate — requires approval and empirical validation",
    })
dimension_plan = pd.DataFrame(dimension_rows)
dimension_plan.to_csv(OUT_DIR / "branch_g_proposed_dimensions.csv", index=False)

role_summary = (
    variable_audit.groupby(["proposed_role", "proposed_dimension"], as_index=False)
    .agg(
        variables=("variable", lambda items: ", ".join(items)),
        variable_count=("variable", "size"),
        minimum_coverage_percent=("coverage_percent", "min"),
    )
)
role_summary.to_csv(OUT_DIR / "branch_g_variable_role_summary.csv", index=False)

# Explicit audit of possible household count conflicts for G1.
counts = values[[
    "household_size", "household_workers", "household_unemployed"
]].apply(pd.to_numeric, errors="coerce")
count_conflict = (
    counts.isna().any(axis=1)
    | counts["household_size"].le(0)
    | counts["household_workers"].lt(0)
    | counts["household_unemployed"].lt(0)
    | counts["household_workers"].gt(counts["household_size"])
    | counts["household_unemployed"].gt(counts["household_size"])
    | (
        counts["household_workers"] + counts["household_unemployed"]
        > counts["household_size"]
    )
)
count_issues = pd.concat(
    [
        values.loc[count_conflict, ["respondent_id"]].reset_index(drop=True),
        counts.loc[count_conflict].reset_index(drop=True),
    ],
    axis=1,
)
count_issues["issue"] = "household counts missing or internally inconsistent"
count_issues.to_csv(OUT_DIR / "branch_g_household_count_issues.csv", index=False)


def markdown_table(frame, columns):
    shown = frame[columns].fillna("").astype(str)
    header = "| " + " | ".join(columns) + " |"
    rule = "|" + "|".join(["---"] * len(columns)) + "|"
    body = [
        "| " + " | ".join(value.replace("|", "/") for value in row) + " |"
        for row in shown.itertuples(index=False, name=None)
    ]
    return "\n".join([header, rule] + body)


report = [
    "# Branch G variable and dimension selection report",
    "",
    "## Cohort and scope",
    "",
    "This report covers the 56 strict new-survey-structure respondents whose corrected final analytical branch is G — inactive/not currently seeking work. The live application calls the inactive section `F`; the research document calls it Branch `G`. The final translated path, not the entry branch, controls inclusion.",
    "",
    "The active paths contain 62 collectively answerable variables. Most core universal and inactive-branch questions have 100% canonical coverage. Questions from implementation Sections D or E were gateway questions answered before some respondents were re-routed to final Branch G; they remain routing evidence and do not enter all-Branch-G clustering.",
    "",
    "## Recommended candidate Level-1 dimensions",
    "",
    markdown_table(
        dimension_plan,
        [
            "dimension", "framework", "variables", "number_of_inputs",
            "minimum_coverage_percent", "why_grouped", "caution",
            "clustering_status",
        ],
    ),
    "",
    "No dimension is automatically approved by this audit. No total score or formula is proposed. If a dimension is approved, respondents should be compared on their original mixed responses using equal-weight, missing-aware Gower distance, followed by K-medoids/spectral comparison, resampling, dominance and permutation checks.",
    "",
    "## Variables deliberately kept outside clustering distances",
    "",
    "- `time_use_decision_maker` is substantively important but is one nominal constraint/autonomy question. It should describe inactivity profiles rather than create a standalone capital or autonomy dimension.",
    "- `expected_highest_edu_g` is applicable only to respondents wanting further education and has 57.1% coverage; it is a programme-mapping descriptor.",
    "- Parental occupations remain descriptors until a defensible occupational-class crosswalk is adopted.",
    "- Demographics are used to describe profiles and assess equity, not to create need profiles.",
    "- Conditional education/spell histories are not supplied to an all-Branch-G distance.",
    "- Pre-rerouting unemployment/temporary-absence gateway questions are routing/audit fields.",
    "",
    "## Complete variable-role summary",
    "",
    markdown_table(
        role_summary,
        [
            "proposed_role", "proposed_dimension", "variable_count",
            "minimum_coverage_percent", "variables",
        ],
    ),
    "",
    "## Complete 62-variable audit",
    "",
    markdown_table(
        variable_audit,
        [
            "question_id", "survey_section", "variable",
            "framework_recorded_in_survey", "observed_records",
            "coverage_percent", "proposed_role", "proposed_dimension",
            "question_text",
        ],
    ),
    "",
    "## Initial data-quality findings",
    "",
    f"- Strict valid final-Branch-G records: {len(values)}.",
    f"- Collectively answerable active-path variables: {len(variable_audit)}.",
    f"- Household count conflicts requiring pairwise unavailability rather than correction: {len(count_issues)}.",
    f"- Household-income refusals: {int(pd.to_numeric(values['household_income'], errors='coerce').eq(99).sum())}.",
    "- `reason_not_in_labour_force` has 13 observed categories; it must remain nominal and may dominate G3.",
    "- The three G4 psychological-readiness items and the two G5 social-connection items have full coverage and all four ordered response levels represented.",
    "",
    "## Theory sources",
    "",
    "- ILO School-to-Work Transition Survey: inactivity reason, previous employment, and future work/education engagement.",
    "- Bourdieu (1986), *The Forms of Capital*: household economic resources, family educational background, and employment-network resources.",
    "- Deci and Ryan (2000) and the local survey extension: perceived direction, competence/self-efficacy, and relatedness/support for engagement.",
    "- Local `nysc_supervisor_prep.docx`: Branch G was intended to distinguish temporarily constrained, discouraged, and voluntarily inactive youth while retaining motivational and capital context.",
    "",
    "## Recommended modelling order",
    "",
    "1. G4 psychological readiness and support — three coherent full-coverage branch-specific indicators.",
    "2. G3 inactivity pathway and future engagement — highly actionable, but requires a strong dominance test for inactivity reason.",
    "3. G5 labour-market social connection — theoretically clear but only two indicators; use a cross-tab if clustering adds no value.",
    "4. G1 household economic resources/dependency — test carefully for income-source dominance and count consistency.",
    "5. G2 educational/inherited cultural capital — test last because prior branches showed weak or work-exposure-led solutions.",
    "",
    "The recommended first clustering attempt is G4, subject to approval of this dimension plan.",
]
(ROOT / "branch_g_variable_dimension_selection_report.md").write_text(
    "\n".join(report), encoding="utf-8"
)

summary = {
    "cohort": {
        "branch": "G",
        "records": int(len(values)),
        "routing_source": "translated_final_active_branch",
    },
    "inventory": {
        "collectively_answerable_variables": int(len(variable_audit)),
        "proposed_clustering_inputs": int(
            variable_audit["proposed_role"].eq("proposed clustering input").sum()
        ),
        "profile_programme_mapping_descriptors": int(
            variable_audit["proposed_role"].eq(
                "profile/programme-mapping descriptor"
            ).sum()
        ),
        "conditional_descriptors": int(
            variable_audit["proposed_role"].eq("conditional descriptor").sum()
        ),
        "routing_audit_variables": int(
            variable_audit["proposed_role"].eq("routing/audit only").sum()
        ),
    },
    "candidate_dimensions": {
        row.dimension: {
            "variables": row.variables.split(", "),
            "number_of_inputs": int(row.number_of_inputs),
            "minimum_coverage_percent": float(row.minimum_coverage_percent),
        }
        for row in dimension_plan.itertuples()
    },
    "quality": {
        "household_count_conflicts": int(len(count_issues)),
        "household_income_refusals": int(
            pd.to_numeric(values["household_income"], errors="coerce").eq(99).sum()
        ),
    },
    "decision": {
        "clustering_run": False,
        "reason": "variable/dimension audit must be reviewed before clustering",
        "recommended_first_dimension": (
            "G4 — Psychological readiness and support for engagement"
        ),
    },
}
with open(OUT_DIR / "branch_g_variable_dimension_audit_summary.json", "w", encoding="utf-8") as handle:
    json.dump(summary, handle, indent=2)

print(json.dumps(summary, indent=2))
print("\nRole counts:\n", variable_audit["proposed_role"].value_counts().to_string())
print("\nSaved report:", ROOT / "branch_g_variable_dimension_selection_report.md")
print("Saved outputs:")
for path in sorted(OUT_DIR.iterdir()):
    print(" -", path)

