"""Explicit evidence scope for the assigned-cluster research wizard.

The programme recommendation registry intentionally contains only the final
``programme_relevant_findings`` subset.  The research wizard has a different
purpose: it teaches an officer about every profiling comparison retained in
the final report.  This registry therefore maps the complete, deduplicated
set reported across the final profile columns to exact survey variables.

Nothing in this file is inferred from every available statistic.  The corpus
builder verifies these variables against the frozen final CSV, the generated
profile document, and the final comparison summary before any item can reach
retrieval or an LLM.
"""
from __future__ import annotations


FINAL_WIZARD_SOURCE_COLUMNS = (
    "strongest_non_clustering_characteristics",
    "barriers_and_support_needs",
    "aspirations_and_preferences",
    "education_training_employment_characteristics",
)


# The final notebook selected the same comparison variables for every profile
# within a model; only the direction/profile-specific wording changes.
WIZARD_PROFILING_VARIABLES_BY_MODEL = {
    "D_motivation": (
        "employment_network_quality",
    ),
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
    "E_learning_orientation": (
        "job_acceptance_conditions",
        "network_helpfulness",
        "household_size",
        "search_method_primary",
        "social_support_job_search",
        "minimum_wage_band",
        "num_applications",
    ),
    "F_employment_security": (
        "monthly_income_band",
        "primary_income_source",
        "hopes_to_change_job",
        "job_satisfaction",
        "received_training",
        "who_paid_training",
        "work_while_study_type",
    ),
    "G_economic_role": (
        "employment_network_quality",
        "labour_market_connection",
        "employment_self_efficacy",
        "most_important_life_goal",
        "support_for_engagement",
        "edu_status",
        "ever_worked",
    ),
    "G_future_engagement": (
        "employment_self_efficacy",
        "support_for_engagement",
        "labour_market_connection",
        "future_orientation_g",
        "employment_network_quality",
        "moved_from_origin",
        "edu_min_for_decent_job",
    ),
}


THEME_LABELS = {
    "aspiration": "Aspirations and preferences",
    "barrier": "Barriers and practical needs",
    "education": "Education and learning",
    "employment": "Employment experience",
    "feasibility": "Practical feasibility",
    "financial": "Financial context",
    "mobility": "Mobility and place",
    "service": "Services and participation",
    "support": "Support and networks",
    "training": "Training experience",
}


EXPECTED_PROFILE_COUNT = 17
EXPECTED_FINDING_COUNT = 89


# These two retained conditional descriptors are present in the cleaned survey
# and branch audits but not in the 131-variable feature manifest.  Keep their
# governed survey wording explicit instead of falling back to an invented
# question at generation time.
SUPPLEMENTAL_SURVEY_QUESTIONS = {
    "work_while_study_type": {
        "question_id": "B10",
        "section": "B",
        "framework": "SWTS",
        "question_text": "How would you describe that work experience while studying?",
    },
    "who_paid_training": {
        "question_id": "E31",
        "section": "E",
        "framework": "SWTS",
        "question_text": "Who mainly paid for that training?",
    },
}
