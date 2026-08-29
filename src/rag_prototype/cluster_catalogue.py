"""Stable officer-facing metadata for all 17 frozen retained profiles.

Codes, names, and common descriptions are display metadata only. They never
participate in branch routing, nearest-medoid assignment, evidence selection,
or course ranking.
"""
from __future__ import annotations

from branch_d_profile_dossiers import (
    BRANCH_D_CLUSTER_CODES,
    SAVED_CLUSTER_DESCRIPTIONS,
    SAVED_CLUSTER_NAMES,
)
from new_respondent_cluster_assignment import BRANCH_MODELS
from retained_cluster_evidence_registry import CLUSTER_DEFINING_REGISTRY


MODEL_DIMENSIONS = {
    "D_motivation": "Study motivation",
    "D_economic": "Household resources",
    "D_educational_cultural": "Education background",
    "E_learning_orientation": "Education and further learning",
    "F_employment_security": "Employment security",
    "G_economic_role": "Household economic role",
    "G_future_engagement": "Future work and education",
}

BRANCH_LABELS = {
    "D": "In education or training",
    "E": "Looking for work",
    "F": "Currently employed",
    "G": "Outside work and education",
}


PROFILE_METADATA = {
    **{
        key: {
            "cluster_code": BRANCH_D_CLUSTER_CODES[key],
            "cluster_name": SAVED_CLUSTER_NAMES[key],
            "common_description": SAVED_CLUSTER_DESCRIPTIONS[key],
        }
        for key in BRANCH_D_CLUSTER_CODES
    },
    "E_learning_orientation_p1": {
        "cluster_code": "Cluster E-LEARN-1",
        "cluster_name": "High education value and strong learning ambition",
        "common_description": (
            "This cluster is centred on job-seeking youth who found their previous education highly useful "
            "and showed strong plans for further and postgraduate study."
        ),
    },
    "E_learning_orientation_p2": {
        "cluster_code": "Cluster E-LEARN-2",
        "cluster_name": "Moderate education value and mixed learning plans",
        "common_description": (
            "This cluster is centred on job-seeking youth who found their previous education somewhat useful "
            "and had a mixture of firm, uncertain, or limited plans for further study."
        ),
    },
    "F_employment_security_p1": {
        "cluster_code": "Cluster F-SEC-1",
        "cluster_name": "Temporary work with uncertain security",
        "common_description": (
            "This cluster is centred on employed youth whose contract, formality, and near-term security "
            "answers indicated temporary or absent contracts and less certain employment."
        ),
    },
    "F_employment_security_p2": {
        "cluster_code": "Cluster F-SEC-2",
        "cluster_name": "Permanent work with stronger security",
        "common_description": (
            "This cluster is centred on employed youth whose contract, formality, and near-term security "
            "answers indicated more permanent and secure employment."
        ),
    },
    "G_economic_role_p1": {
        "cluster_code": "Cluster G-ROLE-1",
        "cluster_name": "Family-supported non-provider",
        "common_description": (
            "This cluster is centred on youth outside work and education who were not the main household "
            "provider and relied mainly on family or a partner for income."
        ),
    },
    "G_economic_role_p2": {
        "cluster_code": "Cluster G-ROLE-2",
        "cluster_name": "Self-income provider or contributor",
        "common_description": (
            "This cluster is centred on youth outside work and education who were main or shared earners and "
            "reported their own work or business as an important income source."
        ),
    },
    "G_future_engagement_p1": {
        "cluster_code": "Cluster G-FUTURE-1",
        "cluster_name": "Work-and-education engaged",
        "common_description": (
            "This cluster is centred on youth with previous work experience who expressed interest in future "
            "work and further education."
        ),
    },
    "G_future_engagement_p2": {
        "cluster_code": "Cluster G-FUTURE-2",
        "cluster_name": "Low or uncertain future engagement",
        "common_description": (
            "This cluster is centred on youth with little or no previous work experience and lower or uncertain "
            "interest in future work and further education."
        ),
    },
}


def metadata_for_profile(profile_key: str) -> dict:
    if profile_key not in PROFILE_METADATA:
        raise ValueError(f"No governed cluster catalogue entry for {profile_key}")
    model_id = profile_key.rsplit("_p", 1)[0]
    return {
        "profile_key": profile_key,
        "model_id": model_id,
        "dimension": MODEL_DIMENSIONS[model_id],
        **PROFILE_METADATA[profile_key],
    }


def catalogue_for_branch(branch: str, question_map: dict | None = None) -> list[dict]:
    catalogue = []
    for model_id in BRANCH_MODELS.get(branch, []):
        keys = sorted(
            key for key in PROFILE_METADATA
            if key.startswith(f"{model_id}_p")
        )
        for key in keys:
            item = metadata_for_profile(key)
            item["cluster_defining_variables"] = [
                {
                    "variable": variable,
                    "question_id": (question_map or {}).get(variable, {}).get("question_id"),
                    "question": (question_map or {}).get(variable, {}).get("question_text"),
                }
                for variable in CLUSTER_DEFINING_REGISTRY[model_id]["variables"]
            ]
            catalogue.append(item)
    return catalogue


def full_research_tree(question_map: dict | None = None) -> list[dict]:
    """Canonical read-only hierarchy for the complete retained research tree."""
    tree = []
    for branch_id, model_ids in BRANCH_MODELS.items():
        branch_catalogue = catalogue_for_branch(branch_id, question_map)
        tree.append({
            "branch_id": branch_id,
            "branch_label": BRANCH_LABELS[branch_id],
            "models": [
                {
                    "model_id": model_id,
                    "model_label": MODEL_DIMENSIONS[model_id],
                    "profiles": [
                        profile for profile in branch_catalogue
                        if profile["model_id"] == model_id
                    ],
                }
                for model_id in model_ids
            ],
        })
    return tree


def validate_catalogue() -> None:
    expected = {
        f"{model_id}_p{profile_id}"
        for model_id, count in {
            "D_motivation": 3,
            "D_economic": 2,
            "D_educational_cultural": 4,
            "E_learning_orientation": 2,
            "F_employment_security": 2,
            "G_economic_role": 2,
            "G_future_engagement": 2,
        }.items()
        for profile_id in range(1, count + 1)
    }
    if set(PROFILE_METADATA) != expected:
        raise ValueError("Cluster catalogue does not exactly cover all 17 frozen retained profiles")


validate_catalogue()
