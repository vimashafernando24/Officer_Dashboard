from pathlib import Path
import json

import pandas as pd


ROOT = Path.cwd()
RAW_PATH = ROOT / "nysc_survey.survey_responses23.json"
QUALITY_PATH = ROOT / "outputs/nysc_survey_quality_audit.csv"
OUT_DIR = ROOT / "outputs/branch_f_variable_dimension_audit"
OUT_DIR.mkdir(parents=True, exist_ok=True)


DIMENSIONS = {
    "D1 — Household economic resources and responsibility": {
        "framework": "Bourdieu economic capital + SWTS household structure",
        "variables": [
            "household_income", "household_size", "household_workers",
            "household_unemployed", "primary_earner_status",
            "primary_income_source",
        ],
        "why": "Separates employed youth by resources available to the household and by the respondent's responsibility for providing them.",
        "caution": "These are raw indicators, not a published scale. Household counts must be checked for internal consistency before clustering.",
    },
    "D2 — Educational and inherited cultural capital": {
        "framework": "Bourdieu institutionalised/inherited cultural capital + SWTS education history",
        "variables": [
            "father_edu", "mother_edu", "edu_status",
            "worked_while_studying",
        ],
        "why": "Captures family educational background, the respondent's recent educational position, and prior exposure to work while studying.",
        "caution": "highest_edu_completed is answered by only 21/81 and must not be interpreted as missing education for the other 60 respondents.",
    },
    "D3 — Employment security and formality": {
        "framework": "ILO SWTS employment quality + Bourdieu field position",
        "variables": [
            "contract_type", "job_security_12months", "sector_formality",
        ],
        "why": "Measures contractual stability, perceived continuity of the job, and formal/informal labour-market position.",
        "caution": "enterprise registration and tax payment are descriptors because sector_formality already summarises related information.",
    },
    "D4 — Earnings and working-time adequacy": {
        "framework": "ILO SWTS employment conditions and under/over-employment",
        "variables": [
            "monthly_income_band", "usual_hours_per_week",
            "income_hours_preference",
        ],
        "why": "Distinguishes low/high earnings and whether respondents want more hours/income, fewer hours/income, or no change.",
        "caution": "Actual hours last week can reflect a temporary event, so it is retained as a descriptor rather than double-weighting hours.",
    },
    "D5 — Subjective job satisfaction and mobility intention": {
        "framework": "ILO SWTS satisfactory-employment/transition concept",
        "variables": [
            "job_satisfaction", "contract_satisfaction",
            "hopes_to_change_job",
        ],
        "why": "Separates respondents who evaluate the job positively and intend to stay from those who are dissatisfied or considering another job.",
        "caution": "contract_satisfaction contains reason categories and must be treated as nominal, not as an invented numeric rank.",
    },
    "D6 — Qualification use and skill development": {
        "framework": "Bourdieu cultural-capital utilisation + ILO SWTS education/training relevance",
        "variables": [
            "qualification_job_match", "past_edu_useful_for_job",
            "received_training",
        ],
        "why": "Captures whether existing qualifications are used, whether prior education is useful, and whether current-job training is occurring.",
        "caution": "Training type, provider, duration, and payer are conditional descriptors for the respondents who received training.",
    },
    "D7 — Professional social capital": {
        "framework": "Bourdieu social capital",
        "variables": [
            "employment_network_quality", "professional_network_growth",
        ],
        "why": "Measures useful employment contacts already available and whether the current job is expanding professional connections.",
        "caution": "With only two direct indicators, clustering should proceed only if validation is adequate; otherwise report a cross-tabulation instead.",
    },
    "D8 — Work motivation and psychological need experience": {
        "framework": "Self-Determination Theory (Deci and Ryan, 2000)",
        "variables": [
            "work_autonomy", "competence_growth_at_work",
            "relatedness_at_work", "work_motivation_type",
        ],
        "why": "Directly represents autonomy, competence, relatedness, and autonomous-to-controlled work motivation.",
        "caution": "The survey uses one question per construct; cluster raw responses and do not claim a validated SDT scale or invent a total score.",
    },
    "D9 — Transition-to-work search pathway and barriers": {
        "framework": "ILO School-to-Work Transition Survey",
        "variables": [
            "registered_as_jobseeker", "employment_service_help_f",
            "jobs_applied_before_hire", "interviews_before_hire",
            "search_duration_before_hire", "obstacle_finding_this_job",
        ],
        "why": "Captures the intensity, duration, institutional support, and main barrier involved in obtaining the current job.",
        "caution": "Application/interview counts require outlier checks. Refusal and reservation conditions remain descriptors because they measure selectivity, not search difficulty itself.",
    },
}


SELECTED = {
    variable: dimension
    for dimension, specification in DIMENSIONS.items()
    for variable in specification["variables"]
}

ROUTING_AUDIT = {"current_activity_status", "has_job_to_return"}
SPARSE_CONDITIONAL = {
    "age_first_married", "spouse_activity", "num_children", "reason_left_edu",
    "highest_edu_completed", "edu_end_year", "spell1_activity",
    "spell1_is_current", "spell1_contract", "spell1_satisfaction",
    "spell1_end_reason", "spell2_activity", "spell2_is_current",
    "spell2_contract", "spell2_satisfaction", "spell2_end_reason",
    "spell3_activity", "reason_temp_absence", "insecurity_bothers",
    "reason_below_normal_hours", "reason_wants_to_change",
    "reason_not_union", "training_type_received", "training_provider",
    "training_duration", "who_paid_training", "reason_refused_job_f",
}
SELF_EMPLOYED_SUBGROUP = {
    "reason_self_employed", "business_helpers", "business_funding_source",
    "business_profitability", "main_business_obstacle",
}
WAGE_WORKER_SUBGROUP = {
    "job_recruitment_method", "enterprise_size", "gender_equality_at_work",
}
REDUNDANT_OR_VOLATILE = {
    "enterprise_registered", "paid_taxes", "actual_hours_last_week",
    "hours_below_normal",
}
CONTEXT_AND_MAPPING = {
    "age_group", "gender", "district", "area_type", "moved_from_origin",
    "move_reason", "marital_status", "has_children", "father_occ",
    "mother_occ", "edu_min_for_decent_job", "most_important_life_goal",
    "most_useful_quality_for_job", "ideal_work_type", "ideal_sector",
    "work_while_study_type", "work_while_study_paid",
    "work_while_study_hours", "work_while_study_motivation",
    "enterprise_location_type", "occupational_class", "has_second_job",
    "willing_to_relocate_f", "plans_further_edu_f", "expected_highest_edu_f",
    "union_member", "ever_refused_job_f", "acceptance_conditions_search",
    "had_min_wage_during_search", "employment_status",
}


def role_for(variable):
    if variable in SELECTED:
        return "proposed clustering input", SELECTED[variable]
    if variable in ROUTING_AUDIT:
        return "routing/audit only", "Not a clustering dimension"
    if variable in SELF_EMPLOYED_SUBGROUP:
        return "self-employed subgroup description", "Separate n=11 subgroup"
    if variable in WAGE_WORKER_SUBGROUP:
        return "wage-worker subgroup description", "Separate n=70 subgroup"
    if variable in SPARSE_CONDITIONAL:
        return "conditional descriptor", "Not used in all-Branch-F distance"
    if variable in REDUNDANT_OR_VOLATILE:
        return "validation/profile descriptor", "Avoid duplicate or temporary-event weighting"
    if variable in CONTEXT_AND_MAPPING:
        return "profile/programme-mapping descriptor", "Not a clustering dimension"
    raise KeyError(f"Unclassified Branch F variable: {variable}")


quality = pd.read_csv(QUALITY_PATH)
selected_rows = quality.loc[
    quality["keep_final"]
    & quality["branch"].eq("F")
    & quality["branch_routing_source"].eq("translated_final_active_branch")
    & ~quality["branch_integrity_issue"]
]
raw_indices = selected_rows["raw_row"].astype(int).tolist()

with open(RAW_PATH, encoding="utf-8") as handle:
    raw_records = json.load(handle)
records = [raw_records[index] for index in raw_indices]
assert len(records) == 81

audit = {}
for record in records:
    for question_id, item in record.get("answers", {}).items():
        if not isinstance(item, dict) or item.get("is_active_path") is False:
            continue
        variable = item.get("variable")
        if not variable:
            continue
        row = audit.setdefault(variable, {
            "question_id": question_id,
            "survey_section": item.get("section"),
            "framework": item.get("framework"),
            "question_text": item.get("question_text"),
            "observed_records": 0,
            "responses": set(),
        })
        if item.get("value") is not None:
            row["observed_records"] += 1
            if item.get("label") is not None:
                row["responses"].add(str(item["label"]))

rows = []
for variable, item in audit.items():
    role, dimension = role_for(variable)
    rows.append({
        "question_id": item["question_id"],
        "survey_section": item["survey_section"],
        "variable": variable,
        "framework_recorded_in_survey": item["framework"],
        "question_text": item["question_text"],
        "observed_records": item["observed_records"],
        "coverage_percent": round(100 * item["observed_records"] / len(records), 1),
        "unique_observed_responses": len(item["responses"]),
        "proposed_role": role,
        "proposed_dimension": dimension,
    })

variable_audit = pd.DataFrame(rows)
section_order = {"A": 0, "B": 1, "E": 2}
variable_audit["_section_order"] = variable_audit["survey_section"].map(section_order).fillna(9)
variable_audit["_question_number"] = (
    variable_audit["question_id"].str.extract(r"(\d+)", expand=False).astype(int)
)
variable_audit = variable_audit.sort_values(
    ["_section_order", "_question_number", "question_id", "variable"]
).drop(columns=["_section_order", "_question_number"])

assert len(variable_audit) == 105
assert set(SELECTED).issubset(set(variable_audit["variable"]))
variable_audit.to_csv(OUT_DIR / "branch_f_all_105_variables.csv", index=False)

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
    })
dimension_plan = pd.DataFrame(dimension_rows)
dimension_plan.to_csv(OUT_DIR / "branch_f_proposed_dimensions.csv", index=False)

role_summary = (
    variable_audit.groupby(["proposed_role", "proposed_dimension"], as_index=False)
    .agg(
        variables=("variable", lambda values: ", ".join(values)),
        variable_count=("variable", "size"),
        minimum_coverage_percent=("coverage_percent", "min"),
    )
)
role_summary.to_csv(OUT_DIR / "branch_f_variable_role_summary.csv", index=False)


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
    "# Branch F variable and dimension selection report",
    "",
    "## Cohort and scope",
    "",
    "This report covers the corrected new-survey-structure employed branch. There are 82 strict final-Branch-F records; one routing-corrupted record is retained in the cleaned master data but excluded here, leaving 81 valid records.",
    "",
    "The raw active survey path contains 105 collectively answerable variables. The earlier 84-variable figure described only the modelling manifest (39 universal + 45 retained Branch-F variables) and omitted conditional follow-ups. This report uses all 105.",
    "",
    "The live application calls the employed section `E`, while the research document calls the analytical employed branch `F`. Variables are matched by stable variable name and final path, not by assuming that the section letter is identical.",
    "",
    "## Proposed Level-1 clustering dimensions",
    "",
    markdown_table(
        dimension_plan,
        ["dimension", "framework", "variables", "number_of_inputs", "minimum_coverage_percent", "why_grouped", "caution"],
    ),
    "",
    "No dimension score or formula is proposed here. Each analysis should compare respondents on the original answers using a mixed-data distance such as Gower distance. Theory determines which variables belong together; it does not justify inventing a total score.",
    "",
    "## Complete variable-role summary",
    "",
    markdown_table(
        role_summary,
        ["proposed_role", "proposed_dimension", "variable_count", "minimum_coverage_percent", "variables"],
    ),
    "",
    "## Complete 105-variable audit",
    "",
    markdown_table(
        variable_audit,
        ["question_id", "survey_section", "variable", "framework_recorded_in_survey", "observed_records", "coverage_percent", "proposed_role", "proposed_dimension", "question_text"],
    ),
    "",
    "## Theory sources used",
    "",
    "- ILO School-to-Work Transition Survey: structural position, employment conditions, stable/satisfactory employment, job-search pathway, and barriers.",
    "- Bourdieu (1986), *The Forms of Capital*: economic, cultural, and social capital and position within a field.",
    "- Deci and Ryan (2000), *The What and Why of Goal Pursuits*: autonomy, competence, relatedness, and regulatory/motivation style.",
    "- The local `nysc_supervisor_prep.docx`: maps the survey variables to the three frameworks and specifies branch-specific clustering.",
    "",
    "## Decision required before modelling",
    "",
    "Approve, remove, or revise the nine proposed dimensions first. The existing employment-security notebook is preliminary and should not be treated as the final Branch-F analysis until this variable plan is agreed.",
]
(ROOT / "branch_f_variable_dimension_selection_report.md").write_text(
    "\n".join(report), encoding="utf-8"
)

print("Valid Branch F records:", len(records))
print("Collectively answerable variables:", len(variable_audit))
print("Proposed dimensions:", len(dimension_plan))
print(dimension_plan[["dimension", "number_of_inputs", "minimum_coverage_percent"]].to_string(index=False))
print("\nVariable roles:")
print(variable_audit["proposed_role"].value_counts().to_string())
print("\nSaved:")
print(" - branch_f_variable_dimension_selection_report.md")
for path in sorted(OUT_DIR.iterdir()):
    print(" -", path.relative_to(ROOT))
