"""Build/load governed JSON research dossiers for all retained Branch D profiles.

Each dossier keeps the two final-analysis layers separate:
1. cluster definition and medoid pattern (why assignment is plausible), and
2. approved post-cluster profiling comparisons (what the research found).

No raw tested-only distribution becomes a finding. The approved comparison
allowlist is recovered from the final analysis' strongest retained profile
characteristics; the programme-relevant subset is labelled separately.
"""
from __future__ import annotations

import csv
import json
from pathlib import Path

import context_pack_v2
import new_respondent_cluster_assignment as nrca
from profile_data_parser import parse_profile_document
from profile_response_distributions import profile_response_distribution
from retained_cluster_evidence_registry import (
    PROFILE_RETAINED_VARIABLES,
    _interpretation_guard,
)


BASE = Path(__file__).resolve().parents[2]
OUTPUT_DIR = BASE / "outputs/rag_branch_d_profile_dossiers"
FINAL_PROFILE_CSV = BASE / "outputs/final_cluster_programme_relevant_profiles.csv"
FEATURE_MANIFEST_CSV = BASE / "outputs/nysc_survey_feature_manifest.csv"

APPROVED_PROFILING_VARIABLES_BY_MODEL = {
    "D_motivation": ("employment_network_quality",),
    "D_economic": (
        "ideal_sector",
        "study_field_preference",
        "institution_type",
        "social_capital_in_edu_access",
        "job_search_method_d",
    ),
    "D_educational_cultural": (
        "already_job_searching",
        "primary_income_source",
        "edu_funding_source",
        "household_income",
        "primary_earner_status",
    ),
}

BRANCH_D_CLUSTER_CODES = {
    "D_economic_p1": "Cluster RES-1",
    "D_economic_p2": "Cluster RES-2",
    "D_educational_cultural_p1": "Cluster EDU-1",
    "D_educational_cultural_p2": "Cluster EDU-2",
    "D_educational_cultural_p3": "Cluster EDU-3",
    "D_educational_cultural_p4": "Cluster EDU-4",
    "D_motivation_p1": "Cluster MOT-1",
    "D_motivation_p2": "Cluster MOT-2",
    "D_motivation_p3": "Cluster MOT-3",
}

SAVED_CLUSTER_NAMES = {
    "D_economic_p1": "Family-supported, government-funded study",
    "D_economic_p2": "Family-funded study with more household earners",
    "D_educational_cultural_p1": "Education re-entry with graduate family background",
    "D_educational_cultural_p2": "State-study postgraduate pathway",
    "D_educational_cultural_p3": "Private-study pathway without work exposure",
    "D_educational_cultural_p4": "Private-study pathway with work exposure",
    "D_motivation_p1": "Qualification-led study",
    "D_motivation_p2": "Goal-led study with developing confidence",
    "D_motivation_p3": "Goal-led, confident and connected study",
}

# Reviewed, stable officer-facing explanations of each frozen medoid pattern.
# These are deliberately stored content, not generated again for each intake.
# Wording says "centred on" because a medoid is one real, representative
# response pattern; it does not prove that every answer was the majority
# response within the cluster.
SAVED_CLUSTER_DESCRIPTIONS = {
    "D_economic_p1": (
        "This cluster is centred on household situations with income between LKR 60,000 and 120,000, "
        "three household members, one wage earner and one person seeking work. It combines family financial "
        "support with government-funded or free education."
    ),
    "D_economic_p2": (
        "This cluster is centred on four-person households with two wage earners and one person seeking "
        "work. It combines a learner who is not the main earner with family-funded education. Household income "
        "is not included because it was not disclosed."
    ),
    "D_educational_cultural_p1": (
        "This cluster is centred on learners who returned to education after stopping to work or seek work. "
        "The educational pattern includes graduate parents, private-institution study and an expected "
        "bachelor’s degree."
    ),
    "D_educational_cultural_p2": (
        "This cluster is centred on state-sector learners expecting postgraduate education, without reported "
        "work while studying or a stop-and-return education pathway. Parental education was not known or "
        "not disclosed."
    ),
    "D_educational_cultural_p3": (
        "This cluster is centred on private-institution learners expecting a bachelor’s degree, without "
        "reported work while studying or a stop-and-return education pathway. Parental education was not "
        "known or not disclosed."
    ),
    "D_educational_cultural_p4": (
        "This cluster is centred on private-institution learners expecting a bachelor’s degree who have "
        "experience working while studying. It does not include a reported stop-and-return education pathway, "
        "and parental education was not known or not disclosed."
    ),
    "D_motivation_p1": (
        "This cluster is centred on learners studying because a qualification is required for work. They show "
        "some choice over study, some confidence gaps and some—but not deep—connection to the institution."
    ),
    "D_motivation_p2": (
        "This cluster is centred on learners studying for personally meaningful goals, with some choice over "
        "study, some confidence gaps and some—but not deep—connection to the institution."
    ),
    "D_motivation_p3": (
        "This cluster is centred on learners studying for personally meaningful goals, with substantial "
        "choice, strong confidence and a strong sense of connection to the institution."
    ),
}


def _question_map() -> dict:
    with open(FEATURE_MANIFEST_CSV, newline="", encoding="utf-8-sig") as handle:
        return {row["variable"]: row for row in csv.DictReader(handle)}


def _final_rows() -> dict:
    with open(FINAL_PROFILE_CSV, newline="", encoding="utf-8-sig") as handle:
        rows = list(csv.DictReader(handle))
    return {
        f"{row['model_id']}_p{row['profile_id']}": row
        for row in rows if row["branch"] == "D"
    }


def _medoid_answers(model_id: str, profile_id: int, variables: tuple[str, ...]) -> list[dict]:
    spec = nrca.MODEL_SPECS[model_id]
    path = BASE / spec["medoid_file"]
    with open(path, newline="", encoding="utf-8-sig") as handle:
        rows = list(csv.DictReader(handle))
    row = next(
        item for item in rows
        if int(float(item[spec["profile_id_col"]])) == profile_id
    )
    questions = _question_map()
    answers = []
    for variable in variables:
        answer = row.get(f"{variable}__response")
        if answer in (None, ""):
            answer = row.get(variable)
        question = questions.get(variable, {})
        answers.append({
            "variable": variable,
            "question_id": question.get("question_id"),
            "question": question.get("question_text"),
            "medoid_answer": answer or None,
        })
    return answers


def build_branch_d_dossiers() -> dict[str, dict]:
    profile_index = context_pack_v2.load_profile_index()
    final_rows = _final_rows()
    questions = _question_map()
    dossiers = {}

    for profile_key in sorted(BRANCH_D_CLUSTER_CODES):
        model_id, profile_id_text = profile_key.rsplit("_p", 1)
        profile_id = int(profile_id_text)
        parsed = parse_profile_document(
            context_pack_v2.load_profile_doc(profile_key, profile_index)
        )
        final_row = final_rows[profile_key]
        approved_variables = APPROVED_PROFILING_VARIABLES_BY_MODEL[model_id]
        approved_texts = final_row["strongest_non_clustering_characteristics"].split(" | ")
        if len(approved_texts) != len(approved_variables):
            raise ValueError(
                f"{profile_key}: approved finding count does not match explicit variable registry"
            )
        stats = {
            item["variable"]: item
            for item in parsed["supported_findings"]["statistical_detail"]
        }
        findings = []
        for variable, finding_text in zip(approved_variables, approved_texts):
            stat = stats.get(variable)
            if not stat:
                raise ValueError(f"{profile_key}: no final statistical detail for {variable}")
            if not finding_text.startswith(f"{stat['label']}:"):
                raise ValueError(
                    f"{profile_key}: finding order/label mismatch for {variable}"
                )
            question = questions.get(variable, {})
            findings.append({
                "evidence_id": f"{profile_key}:{variable}",
                "variable": variable,
                "label": stat["label"],
                "finding": finding_text,
                "interpretation_guard": _interpretation_guard(
                    variable, finding_text, parsed
                ),
                "is_programme_relevant_subset": (
                    variable in PROFILE_RETAINED_VARIABLES[profile_key]
                ),
                "statistical_support": stat,
                "survey_question": {
                    "question_id": question.get("question_id"),
                    "section": question.get("section"),
                    "framework": question.get("framework"),
                    "question_text": question.get("question_text"),
                },
                "profile_distribution": profile_response_distribution(
                    profile_key, variable
                ),
                "provenance": {
                    "retention_source": (
                        "outputs/final_cluster_programme_relevant_profiles.csv row "
                        f"model_id={model_id}, profile_id={profile_id}, "
                        "column=strongest_non_clustering_characteristics"
                    ),
                    "analysis_source": (
                        "30_final_cluster_profile_analysis.ipynb -> "
                        "final_cluster_profiling_report.md"
                    ),
                    "statistical_source": (
                        "outputs/final_cluster_profile_comparison_summary.csv row "
                        f"model_id={model_id}, variable={variable}"
                    ),
                },
            })

        cluster_variables = tuple(
            item.name for item in nrca.MODEL_SPECS[model_id]["features"]
        )
        raw_variables = tuple(
            {
                "D_motivation": (
                    "study_motivation_type", "autonomy_in_study",
                    "competence_in_study_field", "relatedness_at_institution",
                ),
                "D_economic": (
                    "household_income", "household_size", "household_workers",
                    "household_unemployed", "primary_earner_status",
                    "primary_income_source", "edu_funding_source",
                ),
                "D_educational_cultural": (
                    "father_edu", "mother_edu", "expected_highest_edu_d",
                    "institution_type", "worked_while_studying",
                    "re_entered_education",
                ),
            }[model_id]
        )
        dossiers[profile_key] = {
            "schema_version": "branch_d_profile_dossier_v2",
            "profile": {
                "profile_key": profile_key,
                "branch": "D",
                "model_id": model_id,
                "dimension": parsed["header"]["retained_dimension"],
                "profile_id": profile_id,
                "analysis_label": parsed["header"]["profile_label"],
                "cluster_code": BRANCH_D_CLUSTER_CODES[profile_key],
                "cluster_name": SAVED_CLUSTER_NAMES[profile_key],
                "historical_profile_size": int(parsed["header"]["profile_size_n"]),
            },
            "cluster_definition": {
                "raw_cluster_forming_variables": list(raw_variables),
                "derived_distance_features": list(cluster_variables),
                "medoid_pattern": _medoid_answers(model_id, profile_id, raw_variables),
                "saved_officer_description": SAVED_CLUSTER_DESCRIPTIONS[profile_key],
                "final_definition_text": parsed["profile_definition_text"],
            },
            "approved_post_cluster_findings": findings,
            "cautions": parsed["cautions_text"],
            "prohibited_inferences": parsed["prohibited_inferences_text"],
            "sources": [
                "NYSC_all_branches_clustering_final_report.md",
                "final_cluster_profiling_report.md",
                "outputs/final_cluster_programme_relevant_profiles.csv",
                "outputs/final_cluster_profile_comparison_summary.csv",
                nrca.MODEL_SPECS[model_id]["medoid_file"],
            ],
        }
    return dossiers


def write_branch_d_dossiers() -> list[Path]:
    dossiers = build_branch_d_dossiers()
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    paths = []
    for profile_key, dossier in dossiers.items():
        path = OUTPUT_DIR / f"{profile_key}.json"
        path.write_text(
            json.dumps(dossier, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        paths.append(path)
    return paths


def load_branch_d_dossier(profile_key: str) -> dict:
    if profile_key not in BRANCH_D_CLUSTER_CODES:
        raise ValueError(f"No reviewed Branch D dossier for {profile_key}")
    path = OUTPUT_DIR / f"{profile_key}.json"
    if not path.exists():
        raise FileNotFoundError(
            f"Missing generated dossier {path}; run branch_d_profile_dossiers.py"
        )
    return json.loads(path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    written = write_branch_d_dossiers()
    print(f"Wrote {len(written)} Branch D profile dossiers to {OUTPUT_DIR}")
