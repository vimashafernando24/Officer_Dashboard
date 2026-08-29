"""
§3 — Wraps the ALREADY-BUILT, already-accepted new_respondent_cluster_assignment.py
(untouched — not redesigned, not reopened here) to produce the profile context
handed to the LLM and shown to the person: which profile(s) they were
assigned to, the profile interpretation, relevant frozen findings with real
percentages, and a correctly-labeled similarity/confidence figure.

Terminology note (per governance): the assignment module's confidence_percent
is a DISTANCE-MARGIN RATIO (how much closer the respondent is to their
nearest-medoid profile than to the next-closest one), not a validated
classification accuracy. It is always presented as "membership similarity"
or "assignment confidence (distance-based)", never as "accuracy" — the word
"accuracy" is reserved for the genuinely validated per-model accuracy figures
already published in fixed_medoid_validation_summary.csv (SAFE for 5 models,
NEEDS REVIEW for 2), which are reported separately and explicitly labeled.
"""
import sys
from dataclasses import dataclass
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import new_respondent_cluster_assignment as nrca
import context_pack_v2
from profile_data_parser import parse_profile_document
from retained_cluster_evidence_registry import (
    CLUSTER_DEFINING_REGISTRY,
    select_retained_evidence,
    filter_retained_evidence_for_context,
)
from branch_d_profile_dossiers import load_branch_d_dossier

# Published, genuinely validated per-model reliability from
# outputs/fixed_medoid_assignment_validation/fixed_medoid_validation_summary.csv.
# This IS legitimately called "accuracy" because it is a validated statistic
# (reproduction of the frozen 362's known assignments), unlike the per-person
# distance-margin confidence above.
PUBLISHED_MODEL_ACCURACY = {
    "D_motivation": {"accuracy": 0.958, "judgment": "SAFE for new-user nearest-medoid assignment"},
    "D_economic": {"accuracy": 0.990, "judgment": "SAFE for new-user nearest-medoid assignment"},
    "D_educational_cultural": {"accuracy": 0.906, "judgment": "NEEDS REVIEW"},
    "E_learning_orientation": {"accuracy": 0.971, "judgment": "SAFE for new-user nearest-medoid assignment"},
    "F_employment_security": {"accuracy": 0.988, "judgment": "SAFE for new-user nearest-medoid assignment"},
    "G_economic_role": {"accuracy": 0.964, "judgment": "SAFE for new-user nearest-medoid assignment"},
    "G_future_engagement": {"accuracy": 0.875, "judgment": "NEEDS REVIEW"},
}

# Canonical raw-survey-variable list per model — the exact cluster-forming
# items §0 uses (see new_respondent_cluster_assignment.MODEL_SPECS for the
# derivation formulas). Kept here, not duplicated, so both the LLM context
# builder and any UI consuming this module use the same source.
RAW_VARIABLES_BY_MODEL = {
    model_id: list(entry["variables"])
    for model_id, entry in CLUSTER_DEFINING_REGISTRY.items()
}


@dataclass
class ProfileContextEntry:
    model_id: str
    profile_id: int
    profile_label: str
    profile_key: str  # e.g. "G_economic_role_p1"
    membership_similarity_percent: int  # distance-margin ratio, NOT accuracy
    distance_to_nearest: float
    distance_to_second_nearest: float | None
    distance_tie: bool
    model_published_accuracy: float  # genuinely validated, from fixed_medoid_validation
    model_judgment: str  # "SAFE for new-user nearest-medoid assignment" or "NEEDS REVIEW"
    profile_document_text: str
    cluster_forming_answers: dict  # {variable: value_label} — the raw answers §0 actually assigned on
    profile_definition_text: str  # PROFILE_DEFINITION section only — needed to explain the assignment itself
    retained_evidence: list  # exact final-analysis allowlist before current-context filtering
    validated_evidence: list  # retained AND meaningful for this current officer/programme context
    rejected_evidence: list  # retained but not useful now, with explicit reason
    research_dossier: dict | None  # reviewed per-profile JSON, Branch D prototype only


def build_profile_context(
    branch: str, respondent_answers: dict, officer_context: dict | None = None,
) -> list[ProfileContextEntry]:
    profile_index = context_pack_v2.load_profile_index()
    results = nrca.assign_all_profiles_for_branch(branch, respondent_answers)
    entries = []
    for r in results:
        profile_key = f"{r.model_id}_p{r.profile_id}"
        doc_text = context_pack_v2.load_profile_doc(profile_key, profile_index)
        parsed = parse_profile_document(doc_text)
        retained = select_retained_evidence(parsed)
        eligible, rejected = filter_retained_evidence_for_context(
            profile_key, retained, officer_context or {},
        )
        pub = PUBLISHED_MODEL_ACCURACY[r.model_id]
        cluster_answers = {
            var: respondent_answers[var]["value_label"]
            for var in RAW_VARIABLES_BY_MODEL[r.model_id]
            if var in respondent_answers
        }
        entries.append(ProfileContextEntry(
            model_id=r.model_id,
            profile_id=r.profile_id,
            profile_label=r.profile_label,
            profile_key=profile_key,
            membership_similarity_percent=r.confidence_percent,
            distance_to_nearest=r.distance_to_nearest,
            distance_to_second_nearest=r.distance_to_second_nearest,
            distance_tie=r.distance_tie,
            model_published_accuracy=pub["accuracy"],
            model_judgment=pub["judgment"],
            profile_document_text=doc_text,
            cluster_forming_answers=cluster_answers,
            profile_definition_text=parsed["profile_definition_text"],
            retained_evidence=retained,
            validated_evidence=eligible,
            rejected_evidence=rejected,
            research_dossier=(load_branch_d_dossier(profile_key) if branch == "D" else None),
        ))

    # Branch G assigns two retained models which share some profiling
    # variables.  Showing both copies adds volume, not information.  Keep the
    # stronger retained comparison and record the other as context-rejected.
    occurrences = {}
    for entry in entries:
        for evidence in entry.validated_evidence:
            occurrences.setdefault(evidence["variable"], []).append((entry, evidence))
    for variable, candidates in occurrences.items():
        if len(candidates) < 2:
            continue
        winner_entry, winner = max(candidates, key=lambda pair: pair[1]["effect_size"])
        for entry, evidence in candidates:
            if entry is winner_entry and evidence is winner:
                continue
            entry.validated_evidence.remove(evidence)
            entry.rejected_evidence.append({
                **evidence,
                "decision": "rejected_current_context",
                "reason": (
                    f"Redundant with the same retained variable in {winner_entry.profile_key}; "
                    "the stronger final-analysis comparison was kept."
                ),
            })
    return entries
