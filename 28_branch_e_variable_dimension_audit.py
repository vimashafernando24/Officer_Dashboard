from pathlib import Path
import json

import pandas as pd


ROOT = Path.cwd()
RAW_PATH = ROOT / "nysc_survey.survey_responses23.json"
QUALITY_PATH = ROOT / "outputs/nysc_survey_quality_audit.csv"
VALUES_PATH = ROOT / "outputs/nysc_survey_cleaned_values.csv"
LABELS_PATH = ROOT / "outputs/nysc_survey_cleaned_labels.csv"
OUT_DIR = ROOT / "outputs/branch_e_variable_dimension_audit"
OUT_DIR.mkdir(parents=True, exist_ok=True)


DIMENSIONS = {
    "E1 — Job-search psychological readiness and support": {
        "framework": "Self-Determination Theory extension recorded in the survey",
        "variables": ["job_search_self_efficacy", "job_search_autonomy_orientation", "social_support_job_search", "future_planning_orientation"],
        "why": "Captures perceived search capability, autonomous versus pressured search orientation, social support, and future direction while seeking work.",
        "caution": "Each construct has one ordered item. Use original responses and do not claim a validated SDT or employability-readiness scale.",
    },
    "E2 — Search intensity and accumulated exposure": {
        "framework": "ILO School-to-Work Transition Survey",
        "variables": ["active_search_4weeks", "job_search_duration", "num_applications", "num_interviews"],
        "why": "Represents recent search activation, time exposed to unemployment/search, and accumulated applications and interviews.",
        "caution": "Application/interview counts are exposure-dependent and contain large values. Raw-range versus robust/log-count sensitivity is mandatory; this is not a job-seeker effort score.",
    },
    "E3 — Economic urgency and job-acceptance constraints": {
        "framework": "Bourdieu field/economic position + ILO SWTS job acceptance",
        "variables": ["income_urgency", "job_acceptance_conditions", "has_minimum_wage"],
        "why": "Combines urgency to earn with the conditions and minimum-income boundary affecting which job offers respondents would accept.",
        "caution": "These are stated constraints/preferences, not an economic-capital scale. The binary minimum-wage answer or the highly concentrated urgency item may dominate.",
    },
    "E4 — Education-to-work preparedness and learning orientation": {
        "framework": "ILO School-to-Work Transition Survey human-capital transition",
        "variables": ["past_edu_usefulness", "plans_further_edu", "expected_highest_edu_e"],
        "why": "Captures perceived usefulness of past education and stated orientation toward additional education or training.",
        "caution": "Perceived usefulness and future educational plans are related but not one validated latent construct. Keep nominal responses nominal and require leave-one-item-out validation.",
    },
    "E5 — Household economic resources and dependency": {
        "framework": "Bourdieu economic capital + ILO SWTS household structure",
        "variables": ["household_income", "household_size", "household_workers", "household_unemployed", "primary_earner_status", "primary_income_source"],
        "why": "Captures household resource position, worker/job-seeker composition, and the respondent's dependence or responsibility for income.",
        "caution": "Household counts require consistency checks and income source may produce a direct dependency split. Interpret economic role separately from resource level.",
    },
    "E6 — Educational and inherited cultural capital": {
        "framework": "Bourdieu cultural capital + ILO SWTS education history",
        "variables": ["father_edu", "mother_edu", "edu_status", "worked_while_studying"],
        "why": "Represents parental educational background, current/recent education position, and work exposure while studying.",
        "caution": "Parental education is a proxy, not merit or ability. Prior branches produced work-while-studying-dominated results, so test last if at all.",
    },
    "E7 — Job-search social capital": {
        "framework": "Bourdieu social capital",
        "variables": ["employment_network_quality", "knows_people_in_target_sector", "network_helpfulness"],
        "why": "Measures general employment contacts, sector-specific contacts, and whether those contacts have actually helped the search.",
        "caution": "This overlaps the previously excluded social-connectedness dimensions and is marked skipped unless the research scope changes.",
    },
}

SELECTED = {
    variable: dimension
    for dimension, specification in DIMENSIONS.items()
    for variable in specification["variables"]
}

ROUTING_AUDIT = {
    "current_activity_status", "desire_for_work", "wanted_to_work",
    "available_to_start", "has_job_to_return", "looking_while_absent",
}
CONDITIONAL_DESCRIPTORS = {
    "age_first_married", "spouse_activity", "num_children",
    "reason_left_edu", "highest_edu_completed", "edu_end_year",
    "spell1_activity", "spell2_activity", "spell1_is_current",
    "spell2_is_current", "spell1_contract", "spell1_satisfaction",
    "spell1_end_reason", "search_method_primary", "reason_not_seeking",
    "reason_refused_job", "minimum_wage_band",
}
PROFILE_AND_MAPPING = {
    "age_group", "gender", "district", "area_type", "moved_from_origin",
    "move_reason", "marital_status", "has_children", "father_occ",
    "mother_occ", "work_while_study_type", "work_while_study_paid",
    "work_while_study_hours", "work_while_study_motivation",
    "edu_min_for_decent_job", "most_important_life_goal",
    "most_useful_quality_for_job", "ideal_work_type", "ideal_sector",
    "job_type_sought", "ever_refused_job", "employment_service_help",
    "activity_while_searching", "willing_to_relocate",
    "main_obstacle_finding_work", "training_type_would_help",
}


def role_for(variable):
    if variable in SELECTED:
        if SELECTED[variable].startswith("E7"):
            return "skipped clustering input", SELECTED[variable]
        return "proposed clustering input", SELECTED[variable]
    if variable in ROUTING_AUDIT:
        return "routing/audit only", "Not a clustering dimension"
    if variable in CONDITIONAL_DESCRIPTORS:
        return "conditional descriptor", "Not used in all-Branch-E distance"
    if variable in PROFILE_AND_MAPPING:
        return "profile/programme-mapping descriptor", "Not a clustering dimension"
    raise KeyError(f"Unclassified Branch E variable: {variable}")


# Select the strict new-structure final Branch E cohort.
quality = pd.read_csv(QUALITY_PATH)
selected_quality = quality.loc[
    quality["keep_final"].astype(bool)
    & quality["branch"].eq("E")
    & quality["branch_routing_source"].eq("translated_final_active_branch")
    & ~quality["branch_integrity_issue"].astype(bool)
].copy()
assert len(selected_quality) == 34

values_all = pd.read_csv(VALUES_PATH)
labels_all = pd.read_csv(LABELS_PATH)
selected_ids = selected_quality["respondent_id"].astype(str).tolist()
values = values_all.loc[
    values_all["respondent_id"].astype(str).isin(selected_ids)
].copy()
labels = labels_all.loc[
    labels_all["respondent_id"].astype(str).isin(selected_ids)
].copy()
assert len(values) == 34 and len(labels) == 34
assert values["respondent_id"].nunique() == 34

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
assert len(answerable_variables) == 75
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
            "percent_of_34": round(100 * count / len(values), 1),
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
variable_audit.to_csv(OUT_DIR / "branch_e_all_75_variables.csv", index=False)
pd.DataFrame(response_rows).to_csv(
    OUT_DIR / "branch_e_variable_response_distributions.csv", index=False
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
        "clustering_status": (
            "skipped under no-overlapping-social-connectedness decision"
            if dimension.startswith("E7")
            else "candidate — requires approval and empirical validation"
        ),
    })
dimension_plan = pd.DataFrame(dimension_rows)
dimension_plan.to_csv(OUT_DIR / "branch_e_proposed_dimensions.csv", index=False)

role_summary = (
    variable_audit.groupby(["proposed_role", "proposed_dimension"], as_index=False)
    .agg(
        variables=("variable", lambda items: ", ".join(items)),
        variable_count=("variable", "size"),
        minimum_coverage_percent=("coverage_percent", "min"),
    )
)
role_summary.to_csv(OUT_DIR / "branch_e_variable_role_summary.csv", index=False)

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
count_issues.to_csv(OUT_DIR / "branch_e_household_count_issues.csv", index=False)


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
    "# Branch E variable and dimension selection report",
    "",
    "## Cohort and scope",
    "",
    "This report covers the 34 strict new-survey-structure respondents whose corrected final analytical branch is E — unemployed/available and seeking or wanting work. The live application records these questions in implementation Section `D`; the research document calls the analytical group Branch `E`. The final translated path, not the entry branch, controls inclusion.",
    "",
    "The active paths contain 75 collectively answerable variables. Core common questions and most Branch-E search questions have complete canonical coverage. Conditional questions such as search method, refusal reason and minimum-wage band remain descriptors rather than universal clustering inputs.",
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
    "- `main_obstacle_finding_work`, `training_type_would_help`, `employment_service_help` and `job_type_sought` are direct programme-mapping descriptors; using them to create clusters would risk merely reproducing the answer categories that should later guide intervention matching.",
    "- Search method, non-search reason, refusal reason and minimum-wage band are conditional and cannot enter an all-Branch-E distance without inventing values for inapplicable respondents.",
    "- Parental occupations remain descriptors until a defensible occupational-class crosswalk is adopted.",
    "- Demographics are used to describe profiles and assess equity, not to create need profiles.",
    "- Conditional education/spell histories are not supplied to an all-Branch-E distance.",
    "- Constant eligibility/routing questions validate Branch E membership rather than recreate it.",
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
    "## Complete 75-variable audit",
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
    f"- Strict valid final-Branch-E records: {len(values)}.",
    f"- Collectively answerable active-path variables: {len(variable_audit)}.",
    f"- Household count conflicts requiring pairwise unavailability rather than correction: {len(count_issues)}.",
    f"- Household-income refusals: {int(pd.to_numeric(values['household_income'], errors='coerce').eq(99).sum())}.",
    f"- Maximum reported applications: {int(pd.to_numeric(values['num_applications'], errors='coerce').max())}; maximum interviews: {int(pd.to_numeric(values['num_interviews'], errors='coerce').max())}. Robust/log-count sensitivity is required for E2.",
    "- `desire_for_work` and `available_to_start` are constant eligibility answers; `active_search_4weeks` varies (26 yes, 8 no) and is retained only in the search-process dimension.",
    "- With n=34 and a minimum profile size of 15, only k=2 can be eligible; three profiles would require at least 45 respondents.",
    "",
    "## Theory sources",
    "",
    "- ILO School-to-Work Transition Survey: search activity, duration, applications/interviews, acceptance conditions, obstacles, services and education-to-work transition.",
    "- Bourdieu (1986), *The Forms of Capital*: household economic position, inherited educational background, search networks and labour-market field constraints.",
    "- Deci and Ryan (2000) and the local survey extension: autonomy, perceived competence, relatedness/support and future direction during job search.",
    "- Local `nysc_supervisor_prep.docx`: Branch E concerns unemployed youth navigating search activity, barriers, motivation, networks and programme-relevant support needs.",
    "",
    "## Recommended modelling order",
    "",
    "1. E1 job-search psychological readiness/support — the most coherent full-coverage branch-specific set.",
    "2. E2 search intensity/exposure — highly actionable, but requires raw-versus-log count sensitivity.",
    "3. E3 economic urgency/acceptance constraints — test for binary-item and urgency dominance.",
    "4. E4 education-to-work preparedness/learning orientation — keep nominal items nominal and test coherence.",
    "5. E5 household economic resources/dependency — test carefully for income-source dominance and count consistency.",
    "6. E6 educational/inherited cultural capital — test last because previous branches produced work-exposure-led results.",
    "7. E7 job-search social capital — skipped under the earlier no-overlapping-social-connectedness decision.",
    "",
    "The recommended first clustering attempt is E1. Because n=34 is small, every result remains exploratory and must use k=2 only under the existing minimum-size rule.",
]
(ROOT / "branch_e_variable_dimension_selection_report.md").write_text(
    "\n".join(report), encoding="utf-8"
)

summary = {
    "cohort": {
        "branch": "E",
        "records": int(len(values)),
        "routing_source": "translated_final_active_branch",
    },
    "inventory": {
        "collectively_answerable_variables": int(len(variable_audit)),
        "proposed_clustering_inputs": int(
            variable_audit["proposed_role"].eq("proposed clustering input").sum()
        ),
        "skipped_clustering_inputs": int(
            variable_audit["proposed_role"].eq("skipped clustering input").sum()
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
            "E1 — Job-search psychological readiness and support"
        ),
    },
}
with open(OUT_DIR / "branch_e_variable_dimension_audit_summary.json", "w", encoding="utf-8") as handle:
    json.dump(summary, handle, indent=2)

print(json.dumps(summary, indent=2))
print("\nRole counts:\n", variable_audit["proposed_role"].value_counts().to_string())
print("\nSaved report:", ROOT / "branch_e_variable_dimension_selection_report.md")
print("Saved outputs:")
for path in sorted(OUT_DIR.iterdir()):
    print(" -", path)
