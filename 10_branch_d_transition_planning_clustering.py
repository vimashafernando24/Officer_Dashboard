# %% [markdown]
# # Branch D — education-to-work transition planning and direction
#
# This notebook clusters all 191 respondents whose validated final active branch
# is D. It uses four original aspiration responses supported by the ILO
# school-to-work transition framework. Search status and search method are kept
# as descriptors so the algorithm cannot merely rediscover a known routing split.
# No readiness score, aspiration score, or study-to-sector alignment formula is
# created.

# %% [markdown]
# ## Method and guardrails
#
# - Four original nominal answers are compared using equal-weight,
#   missing-aware Gower distance.
# - K-medoids and spectral clustering are compared for `k=2–5`.
# - One hundred matched 80% subsamples per algorithm form a 200-partition
#   consensus ensemble.
# - Final profiles come from K-medoids on `1 - co-association`.
# - Job-search status and conditional job-search method describe the resulting
#   profiles; neither determines the clustering distance.

# %%
from pathlib import Path
import json
import warnings

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from IPython.display import display
from sklearn.cluster import AgglomerativeClustering, SpectralClustering
from sklearn.metrics import adjusted_rand_score, silhouette_samples, silhouette_score

warnings.filterwarnings("ignore", category=FutureWarning)
pd.set_option("display.max_columns", 100)
pd.set_option("display.width", 180)

ROOT = Path.cwd()
VALUES_PATH = ROOT / "outputs/nysc_survey_cleaned_values.csv"
LABELS_PATH = ROOT / "outputs/nysc_survey_cleaned_labels.csv"
OUT = ROOT / "outputs/branch_d_transition_planning_clusters"
OUT.mkdir(parents=True, exist_ok=True)

CLUSTER_FEATURES = [
    "plans_after_education",
    "ideal_work_type",
    "ideal_sector",
    "study_field_preference",
]
DESCRIPTOR_VARIABLES = ["already_job_searching", "job_search_method_d"]
DESCRIPTOR_ROLES = {
    "already_job_searching": "transition_engagement_descriptor",
    "job_search_method_d": "conditional_descriptor",
}
ALL_SOURCE_VARIABLES = CLUSTER_FEATURES + DESCRIPTOR_VARIABLES

RANDOM_STATE = 20260825
MIN_PROFILE_SIZE = 15
CANDIDATE_SUBSAMPLES = 50
CONSENSUS_SUBSAMPLES = 100
SUBSAMPLE_FRACTION = 0.80
ENSEMBLE_BOOTSTRAPS = 100

# %% [markdown]
# ## 1. Rebuild and audit the strict final-Branch-D cohort

# %%
values_all = pd.read_csv(VALUES_PATH)
labels_all = pd.read_csv(LABELS_PATH)

strict_mask = (
    values_all["branch"].eq("D")
    & values_all["branch_routing_source"].eq("translated_final_active_branch")
)

values = values_all.loc[strict_mask, [
    "respondent_id",
    "entry_branch",
    "branch",
    "branch_routing_source",
    "current_activity_status",
] + ALL_SOURCE_VARIABLES].copy()

labels = labels_all[[
    "respondent_id", "current_activity_status"
] + ALL_SOURCE_VARIABLES].copy()

cohort = values.merge(
    labels,
    on="respondent_id",
    suffixes=("__value", "__label"),
    validate="one_to_one",
)

validation = {
    "records": int(len(cohort)),
    "unique_ids": int(cohort["respondent_id"].nunique()),
    "wrong_branch": int(cohort["branch"].ne("D").sum()),
    "wrong_routing_source": int(
        cohort["branch_routing_source"].ne("translated_final_active_branch").sum()
    ),
    "not_currently_attending_by_final_status": int(
        cohort["current_activity_status__label"].ne(
            "Attending school, university, or a training programme"
        ).sum()
    ),
}

assert validation["records"] == 191
assert validation["unique_ids"] == 191
assert validation["wrong_branch"] == 0
assert validation["wrong_routing_source"] == 0
assert validation["not_currently_attending_by_final_status"] == 0

display(pd.Series(validation, name="value").to_frame())

# %% [markdown]
# ## 2. Screen variables and verify conditional routing
#
# Plans, preferred work type, preferred sector, and study field are nominal: no
# category is ranked as better than another. Job-search status is a directly
# observed transition-engagement descriptor, not a discovered latent profile.
# The job-search-method question is structurally applicable only to the 111
# students already searching.

# %%
screening_rows = []
for variable in ALL_SOURCE_VARIABLES:
    label_col = f"{variable}__label"
    observed = cohort[label_col].notna()
    counts = cohort.loc[observed, label_col].value_counts(dropna=False)
    screening_rows.append({
        "variable": variable,
        "role": "cluster_input" if variable in CLUSTER_FEATURES else DESCRIPTOR_ROLES[variable],
        "observed": int(observed.sum()),
        "missing": int((~observed).sum()),
        "coverage_percent": 100 * float(observed.mean()),
        "unique_observed_responses": int(counts.size),
        "dominant_response": str(counts.index[0]) if len(counts) else None,
        "dominant_response_percent": 100 * float(counts.iloc[0] / counts.sum()) if len(counts) else np.nan,
    })

variable_screening = pd.DataFrame(screening_rows)

searching = cohort["already_job_searching__value"].eq("yes")
method_observed = cohort["job_search_method_d__label"].notna()
validation.update({
    "already_searching": int(searching.sum()),
    "not_yet_searching": int((~searching).sum()),
    "search_method_observed": int(method_observed.sum()),
    "search_method_present_for_non_searcher": int((method_observed & ~searching).sum()),
    "search_method_missing_for_searcher": int((~method_observed & searching).sum()),
})
assert validation["search_method_present_for_non_searcher"] == 0
assert validation["search_method_missing_for_searcher"] == 0

display(variable_screening.round(2))
display(pd.Series(validation, name="value").to_frame())

# %% [markdown]
# ## 3. Build original-response features and Gower distance

# %%
features = pd.DataFrame(index=cohort.index)
for feature in CLUSTER_FEATURES:
    features[feature] = cohort[f"{feature}__label"].astype("string")

feature_audit = pd.DataFrame({
    "feature": CLUSTER_FEATURES,
    "type": ["nominal"] * len(CLUSTER_FEATURES),
    "observed": [int(features[c].notna().sum()) for c in CLUSTER_FEATURES],
    "missing": [int(features[c].isna().sum()) for c in CLUSTER_FEATURES],
    "maximum_distance_weight": [1 / len(CLUSTER_FEATURES)] * len(CLUSTER_FEATURES),
})
assert features.notna().sum(axis=1).min() >= 3
display(feature_audit)


def nominal_gower(frame, columns=None):
    if columns is None:
        columns = list(frame.columns)
    n = len(frame)
    numerator = np.zeros((n, n), dtype=float)
    denominator = np.zeros((n, n), dtype=float)
    for column in columns:
        strings = frame[column].astype("string")
        observed = strings.notna().to_numpy()
        values_k = strings.fillna("__MISSING__").to_numpy(dtype=str)
        pair_observed = observed[:, None] & observed[None, :]
        difference = (values_k[:, None] != values_k[None, :]).astype(float)
        numerator += np.where(pair_observed, difference, 0.0)
        denominator += pair_observed
    distance = np.divide(
        numerator,
        denominator,
        out=np.zeros_like(numerator),
        where=denominator > 0,
    )
    np.fill_diagonal(distance, 0.0)
    return distance, denominator


D, pair_feature_coverage = nominal_gower(features)
assert np.allclose(D, D.T)
assert D.min() >= 0 and D.max() <= 1
assert pair_feature_coverage.min() >= 3

positive_distances = D[D > 0]
sigma = float(np.median(positive_distances))


def affinity(distance):
    result = np.exp(-(distance ** 2) / (2 * sigma ** 2))
    np.fill_diagonal(result, 1.0)
    return result


print("Gower distance median:", round(float(np.median(positive_distances)), 4))
print(
    "Pairwise observed features: min",
    int(pair_feature_coverage.min()),
    "median",
    int(np.median(pair_feature_coverage)),
    "max",
    int(pair_feature_coverage.max()),
)

# %% [markdown]
# ## 4. Compare candidate profile counts

# %%
def fit_kmedoids(distance, k, n_init=200, max_iter=200, random_state=RANDOM_STATE):
    rng = np.random.default_rng(random_state)
    n = len(distance)
    best = None
    for _ in range(n_init):
        medoids = np.sort(rng.choice(n, size=k, replace=False))
        for _ in range(max_iter):
            labels_k = np.argmin(distance[:, medoids], axis=1)
            updated = medoids.copy()
            for cluster in range(k):
                members = np.flatnonzero(labels_k == cluster)
                if len(members) == 0:
                    nearest = distance[:, medoids].min(axis=1)
                    available = np.setdiff1d(np.argsort(nearest)[::-1], updated)
                    updated[cluster] = available[0]
                else:
                    within = distance[np.ix_(members, members)]
                    updated[cluster] = members[np.argmin(within.sum(axis=1))]
            if np.array_equal(updated, medoids):
                break
            medoids = updated
        labels_k = np.argmin(distance[:, medoids], axis=1)
        loss = float(distance[np.arange(n), medoids[labels_k]].sum())
        candidate = (loss, tuple(medoids.tolist()), medoids.copy(), labels_k.copy())
        if best is None or candidate[:2] < best[:2]:
            best = candidate
    return {"labels": best[3], "medoids": best[2], "loss": best[0]}


def medoids_from_labels(distance, labels_k):
    result = []
    for cluster in sorted(np.unique(labels_k)):
        members = np.flatnonzero(labels_k == cluster)
        within = distance[np.ix_(members, members)]
        result.append(members[np.argmin(within.sum(axis=1))])
    return np.asarray(result, dtype=int)


def subsample_stability(algorithm, k, reference_labels):
    offset = 0 if algorithm == "kmedoids" else 10000
    rng = np.random.default_rng(RANDOM_STATE + 100 * k + offset)
    rows = []
    sample_size = int(np.floor(SUBSAMPLE_FRACTION * len(D)))
    for repetition in range(CANDIDATE_SUBSAMPLES):
        idx = np.sort(rng.choice(len(D), size=sample_size, replace=False))
        D_sub = D[np.ix_(idx, idx)]
        if algorithm == "kmedoids":
            result = fit_kmedoids(
                D_sub, k, n_init=50,
                random_state=RANDOM_STATE + 1000 * k + repetition,
            )
            medoids = idx[result["medoids"]]
        else:
            labels_sub = SpectralClustering(
                n_clusters=k,
                affinity="precomputed",
                assign_labels="kmeans",
                n_init=30,
                random_state=RANDOM_STATE + 2000 * k + repetition,
            ).fit_predict(affinity(D_sub))
            medoids = idx[medoids_from_labels(D_sub, labels_sub)]
        predicted = np.argmin(D[:, medoids], axis=1)
        rows.append(adjusted_rand_score(reference_labels, predicted))
    return np.asarray(rows)


candidate_rows = []
candidate_stability_rows = []
full_source_solutions = {}

for k in range(2, 6):
    kmedoids = fit_kmedoids(D, k, n_init=400, random_state=RANDOM_STATE + k)
    spectral_labels = SpectralClustering(
        n_clusters=k,
        affinity="precomputed",
        assign_labels="kmeans",
        n_init=100,
        random_state=RANDOM_STATE + 100 + k,
    ).fit_predict(affinity(D))
    full_source_solutions[("kmedoids", k)] = kmedoids["labels"]
    full_source_solutions[("spectral", k)] = spectral_labels
    method_values = {}

    for algorithm, labels_k in [
        ("kmedoids", kmedoids["labels"]),
        ("spectral", spectral_labels),
    ]:
        stability = subsample_stability(algorithm, k, labels_k)
        method_values[algorithm] = {
            "silhouette": silhouette_score(D, labels_k, metric="precomputed"),
            "stability": float(stability.mean()),
            "stability_p10": float(np.quantile(stability, 0.10)),
            "minimum_size": int(pd.Series(labels_k).value_counts().min()),
        }
        candidate_stability_rows.extend({
            "algorithm": algorithm,
            "k": k,
            "repetition": repetition + 1,
            "ari": value,
        } for repetition, value in enumerate(stability))

    candidate_rows.append({
        "k": k,
        "kmedoids_silhouette": method_values["kmedoids"]["silhouette"],
        "spectral_silhouette": method_values["spectral"]["silhouette"],
        "mean_source_silhouette": np.mean([
            method_values["kmedoids"]["silhouette"],
            method_values["spectral"]["silhouette"],
        ]),
        "kmedoids_stability_mean": method_values["kmedoids"]["stability"],
        "spectral_stability_mean": method_values["spectral"]["stability"],
        "mean_source_stability": np.mean([
            method_values["kmedoids"]["stability"],
            method_values["spectral"]["stability"],
        ]),
        "minimum_source_p10_stability": min(
            method_values["kmedoids"]["stability_p10"],
            method_values["spectral"]["stability_p10"],
        ),
        "source_algorithm_ari": adjusted_rand_score(kmedoids["labels"], spectral_labels),
        "minimum_cluster_size_across_sources": min(
            method_values["kmedoids"]["minimum_size"],
            method_values["spectral"]["minimum_size"],
        ),
    })

candidate_metrics = pd.DataFrame(candidate_rows)
candidate_stability = pd.DataFrame(candidate_stability_rows)
eligible = candidate_metrics.loc[
    candidate_metrics["minimum_cluster_size_across_sources"].ge(MIN_PROFILE_SIZE)
].copy()
if eligible.empty:
    raise RuntimeError("No k=2–5 candidate meets the minimum profile-size rule.")

eligible["rank_mean_silhouette"] = eligible["mean_source_silhouette"].rank(
    ascending=False, method="min"
)
eligible["rank_mean_stability"] = eligible["mean_source_stability"].rank(
    ascending=False, method="min"
)
eligible["primary_mean_rank"] = eligible[[
    "rank_mean_silhouette", "rank_mean_stability"
]].mean(axis=1)
best_rank = eligible["primary_mean_rank"].min()
selected_k = int(
    eligible.loc[eligible["primary_mean_rank"].eq(best_rank)]
    .sort_values("k").iloc[0]["k"]
)
candidate_metrics = candidate_metrics.merge(
    eligible[["k", "primary_mean_rank"]], on="k", how="left"
)
candidate_metrics["selected"] = candidate_metrics["k"].eq(selected_k)

display(candidate_metrics.round(4))
print("Selected common k:", selected_k)

# %% [markdown]
# ## 5. Build the K-medoids + spectral consensus ensemble

# %%
ensemble_rng = np.random.default_rng(RANDOM_STATE + 30000)
n = len(D)
sample_size = int(np.floor(SUBSAMPLE_FRACTION * n))
cover_matrices = []
same_matrices = []
base_rows = []

for repetition in range(CONSENSUS_SUBSAMPLES):
    idx = np.sort(ensemble_rng.choice(n, size=sample_size, replace=False))
    D_sub = D[np.ix_(idx, idx)]
    cover = np.zeros((n, n), dtype=np.uint8)
    cover[np.ix_(idx, idx)] = 1

    kmedoids_sub = fit_kmedoids(
        D_sub, selected_k, n_init=100,
        random_state=RANDOM_STATE + 40000 + repetition,
    )["labels"]
    spectral_sub = SpectralClustering(
        n_clusters=selected_k,
        affinity="precomputed",
        assign_labels="kmeans",
        n_init=30,
        random_state=RANDOM_STATE + 50000 + repetition,
    ).fit_predict(affinity(D_sub))

    for algorithm, labels_sub in [
        ("kmedoids", kmedoids_sub),
        ("spectral", spectral_sub),
    ]:
        same = np.zeros((n, n), dtype=np.uint8)
        same[np.ix_(idx, idx)] = (
            labels_sub[:, None] == labels_sub[None, :]
        ).astype(np.uint8)
        cover_matrices.append(cover.copy())
        same_matrices.append(same)
        base_rows.append({
            "partition_id": len(base_rows) + 1,
            "algorithm": algorithm,
            "repetition": repetition + 1,
            "silhouette_in_subsample": silhouette_score(
                D_sub, labels_sub, metric="precomputed"
            ),
            "minimum_cluster_size": int(pd.Series(labels_sub).value_counts().min()),
        })

cover_stack = np.stack(cover_matrices)
same_stack = np.stack(same_matrices)
coverage = cover_stack.sum(axis=0)
together = same_stack.sum(axis=0)
consensus = together / coverage
np.fill_diagonal(consensus, 1.0)
consensus_distance = 1 - consensus
np.fill_diagonal(consensus_distance, 0.0)
base_partition_diagnostics = pd.DataFrame(base_rows)

final_fit = fit_kmedoids(
    consensus_distance, selected_k, n_init=500,
    random_state=RANDOM_STATE + 60000,
)
raw_labels = final_fit["labels"]

raw_medoids = {}
for raw_cluster in sorted(np.unique(raw_labels)):
    members = np.flatnonzero(raw_labels == raw_cluster)
    within = consensus_distance[np.ix_(members, members)]
    raw_medoids[int(raw_cluster)] = members[np.argmin(within.sum(axis=1))]

raw_order = sorted(
    raw_medoids,
    key=lambda label: str(cohort.iloc[raw_medoids[label]]["respondent_id"]),
)
raw_to_profile = {raw: profile + 1 for profile, raw in enumerate(raw_order)}
profile_id = np.asarray([raw_to_profile[int(label)] for label in raw_labels])
profile_names = {
    profile: f"Transition profile {profile}"
    for profile in sorted(np.unique(profile_id))
}

print("Base partitions:", len(base_partition_diagnostics))
print(
    "Pair coverage: min", int(coverage.min()),
    "median", int(np.median(coverage)),
    "max", int(coverage.max()),
)

# %% [markdown]
# ## 6. Profile the final transition clusters

# %%
assignments = cohort[[
    "respondent_id", "entry_branch", "branch", "branch_routing_source"
]].copy()
for variable in ALL_SOURCE_VARIABLES:
    assignments[f"{variable}__value"] = cohort[f"{variable}__value"]
    assignments[f"{variable}__response"] = cohort[f"{variable}__label"]

assignments["transition_profile_id"] = profile_id
assignments["transition_profile_label"] = assignments["transition_profile_id"].map(profile_names)
gower_individual_silhouette = silhouette_samples(D, profile_id, metric="precomputed")
consensus_individual_silhouette = silhouette_samples(
    consensus_distance, profile_id, metric="precomputed"
)
assignments["gower_individual_silhouette"] = gower_individual_silhouette
assignments["consensus_individual_silhouette"] = consensus_individual_silhouette

profile_sizes = (
    assignments.groupby(["transition_profile_id", "transition_profile_label"], as_index=False)
    .agg(
        records=("respondent_id", "size"),
        low_gower_confidence_records=(
            "gower_individual_silhouette", lambda values: int((values < 0.10).sum())
        ),
        mean_gower_silhouette=("gower_individual_silhouette", "mean"),
        mean_consensus_silhouette=("consensus_individual_silhouette", "mean"),
    )
)
profile_sizes["percent"] = 100 * profile_sizes["records"] / len(assignments)

response_rows = []
for variable in ALL_SOURCE_VARIABLES:
    response_col = f"{variable}__response"
    temp = (
        assignments.groupby(["transition_profile_id", response_col], dropna=False)
        .size().rename("records").reset_index()
    )
    temp["within_profile_percent"] = (
        100 * temp["records"]
        / temp.groupby("transition_profile_id")["records"].transform("sum")
    )
    temp = temp.rename(columns={response_col: "response"})
    temp.insert(1, "variable", variable)
    temp.insert(
        2,
        "role",
        "cluster_input" if variable in CLUSTER_FEATURES else DESCRIPTOR_ROLES[variable],
    )
    response_rows.append(temp)

profile_response_distributions = pd.concat(response_rows, ignore_index=True)
profile_modes = (
    profile_response_distributions.sort_values(
        ["transition_profile_id", "variable", "within_profile_percent"],
        ascending=[True, True, False],
    ).groupby(["transition_profile_id", "variable"], as_index=False).first()
)

medoid_rows = []
for raw_cluster, medoid_idx in raw_medoids.items():
    pid = raw_to_profile[raw_cluster]
    row = {
        "transition_profile_id": pid,
        "respondent_id": cohort.iloc[medoid_idx]["respondent_id"],
    }
    for feature in CLUSTER_FEATURES:
        row[f"{feature}__response"] = cohort.iloc[medoid_idx][f"{feature}__label"]
    medoid_rows.append(row)
medoid_profiles = pd.DataFrame(medoid_rows).sort_values("transition_profile_id")

field_sector_crosstab = pd.crosstab(
    cohort["study_field_preference__label"],
    cohort["ideal_sector__label"],
    dropna=False,
)

display(profile_sizes.round(3))
display(profile_modes.round(2))
display(medoid_profiles)

# %% [markdown]
# ## 7. Validate stability, ambiguity, and feature sensitivity

# %%
confidence_rows = []
for i in range(n):
    own = profile_id[i]
    own_members = np.flatnonzero(profile_id == own)
    own_members = own_members[own_members != i]
    within = float(consensus[i, own_members].mean()) if len(own_members) else 1.0
    strongest_other = max(
        float(consensus[i, np.flatnonzero(profile_id == other)].mean())
        for other in sorted(set(profile_id) - {own})
    )
    confidence_rows.append({
        "respondent_id": cohort.iloc[i]["respondent_id"],
        "transition_profile_id": int(own),
        "within_profile_consensus": within,
        "strongest_other_profile_consensus": strongest_other,
        "consensus_margin": within - strongest_other,
        "ambiguous_consensus_membership": (
            (within < 0.70) or ((within - strongest_other) < 0.20)
        ),
    })

respondent_confidence = pd.DataFrame(confidence_rows)
assignments = assignments.merge(
    respondent_confidence.drop(columns="transition_profile_id"),
    on="respondent_id", validate="one_to_one",
)

bootstrap_rng = np.random.default_rng(RANDOM_STATE + 70000)
ensemble_stability_rows = []
for repetition in range(ENSEMBLE_BOOTSTRAPS):
    selected = bootstrap_rng.choice(len(cover_stack), size=len(cover_stack), replace=True)
    boot_cover = cover_stack[selected].sum(axis=0)
    boot_same = same_stack[selected].sum(axis=0)
    boot_consensus = np.divide(
        boot_same, boot_cover,
        out=np.zeros_like(boot_same, dtype=float),
        where=boot_cover > 0,
    )
    np.fill_diagonal(boot_consensus, 1.0)
    boot_distance = 1 - boot_consensus
    np.fill_diagonal(boot_distance, 0.0)
    boot_labels = fit_kmedoids(
        boot_distance, selected_k, n_init=80,
        random_state=RANDOM_STATE + 80000 + repetition,
    )["labels"]
    ensemble_stability_rows.append({
        "repetition": repetition + 1,
        "ari_vs_full_consensus": adjusted_rand_score(profile_id, boot_labels),
    })

ensemble_stability = pd.DataFrame(ensemble_stability_rows)
full_kmedoids = full_source_solutions[("kmedoids", selected_k)]
full_spectral = full_source_solutions[("spectral", selected_k)]
consensus_hac_average = AgglomerativeClustering(
    n_clusters=selected_k, metric="precomputed", linkage="average"
).fit_predict(consensus_distance)
consensus_hac_complete = AgglomerativeClustering(
    n_clusters=selected_k, metric="precomputed", linkage="complete"
).fit_predict(consensus_distance)

upper = consensus[np.triu_indices(n, 1)]
metrics = {
    "gower_silhouette": float(silhouette_score(D, profile_id, metric="precomputed")),
    "consensus_distance_silhouette": float(
        silhouette_score(consensus_distance, profile_id, metric="precomputed")
    ),
    "ensemble_bootstrap_ari_mean": float(
        ensemble_stability["ari_vs_full_consensus"].mean()
    ),
    "ensemble_bootstrap_ari_p10": float(
        ensemble_stability["ari_vs_full_consensus"].quantile(0.10)
    ),
    "ari_vs_full_kmedoids": float(adjusted_rand_score(profile_id, full_kmedoids)),
    "ari_vs_full_spectral": float(adjusted_rand_score(profile_id, full_spectral)),
    "ari_consensus_kmedoids_vs_hac_average": float(
        adjusted_rand_score(profile_id, consensus_hac_average)
    ),
    "ari_consensus_kmedoids_vs_hac_complete": float(
        adjusted_rand_score(profile_id, consensus_hac_complete)
    ),
    "minimum_profile_size": int(pd.Series(profile_id).value_counts().min()),
    "low_gower_confidence_percent": 100 * float(
        np.mean(gower_individual_silhouette < 0.10)
    ),
    "ambiguous_consensus_percent": 100 * float(
        assignments["ambiguous_consensus_membership"].mean()
    ),
    "pac_10_90": float(np.mean((upper > 0.10) & (upper < 0.90))),
}

feature_sensitivity_rows = []
for omitted in CLUSTER_FEATURES:
    retained = [feature for feature in CLUSTER_FEATURES if feature != omitted]
    D_reduced, coverage_reduced = nominal_gower(features, retained)
    reduced_fit = fit_kmedoids(
        D_reduced, selected_k, n_init=400,
        random_state=RANDOM_STATE + 90000 + CLUSTER_FEATURES.index(omitted),
    )
    feature_sensitivity_rows.append({
        "omitted_feature": omitted,
        "retained_features": len(retained),
        "minimum_pair_coverage": int(coverage_reduced.min()),
        "gower_silhouette_reduced_kmedoids": float(
            silhouette_score(D_reduced, reduced_fit["labels"], metric="precomputed")
        ),
        "ari_reduced_kmedoids_vs_final_consensus": float(
            adjusted_rand_score(profile_id, reduced_fit["labels"])
        ),
    })
feature_sensitivity = pd.DataFrame(feature_sensitivity_rows)

quality_checks = pd.DataFrame([
    {"check": "original Gower silhouette >= 0.25", "value": metrics["gower_silhouette"], "passed": metrics["gower_silhouette"] >= 0.25},
    {"check": "ensemble bootstrap mean ARI >= 0.80", "value": metrics["ensemble_bootstrap_ari_mean"], "passed": metrics["ensemble_bootstrap_ari_mean"] >= 0.80},
    {"check": f"minimum profile size >= {MIN_PROFILE_SIZE}", "value": metrics["minimum_profile_size"], "passed": metrics["minimum_profile_size"] >= MIN_PROFILE_SIZE},
    {"check": "ARI with full K-medoids >= 0.60", "value": metrics["ari_vs_full_kmedoids"], "passed": metrics["ari_vs_full_kmedoids"] >= 0.60},
    {"check": "ARI with full spectral >= 0.60", "value": metrics["ari_vs_full_spectral"], "passed": metrics["ari_vs_full_spectral"] >= 0.60},
    {"check": "PAC (0.10, 0.90) <= 0.20", "value": metrics["pac_10_90"], "passed": metrics["pac_10_90"] <= 0.20},
    {"check": "ambiguous consensus respondents <= 20%", "value": metrics["ambiguous_consensus_percent"], "passed": metrics["ambiguous_consensus_percent"] <= 20},
    {"check": "low-confidence respondents in original Gower space <= 20%", "value": metrics["low_gower_confidence_percent"], "passed": metrics["low_gower_confidence_percent"] <= 20},
])

primary_pass = bool(quality_checks.iloc[:5]["passed"].all())
if primary_pass and quality_checks.iloc[5:]["passed"].all():
    status = "Stable, cross-method-supported transition-planning segmentation"
elif primary_pass:
    status = "Passes primary stability rules but retains ambiguity cautions"
else:
    status = "No sufficiently robust transition-planning segmentation found"

display(pd.Series(metrics, name="value").to_frame().round(3))
display(quality_checks.round(3))
display(feature_sensitivity.round(3))
print("Decision:", status)

# %% [markdown]
# ## 8. Visualise candidate evidence, consensus, and profiles

# %%
fig, axes = plt.subplots(1, 2, figsize=(12, 4.5))
axes[0].plot(candidate_metrics["k"], candidate_metrics["mean_source_silhouette"], marker="o", label="mean source silhouette")
axes[0].axvline(selected_k, color="tab:red", linestyle="--", label=f"selected k={selected_k}")
axes[0].axhline(0.25, color="grey", linestyle=":")
axes[0].set(title="Candidate separation", xlabel="Number of profiles", ylabel="Mean Gower silhouette")
axes[0].legend()
axes[1].plot(candidate_metrics["k"], candidate_metrics["mean_source_stability"], marker="o", label="mean source stability")
axes[1].plot(candidate_metrics["k"], candidate_metrics["source_algorithm_ari"], marker="s", label="K-medoids vs spectral ARI")
axes[1].axvline(selected_k, color="tab:red", linestyle="--")
axes[1].axhline(0.70, color="grey", linestyle=":")
axes[1].set(title="Stability and source agreement", xlabel="Number of profiles", ylabel="ARI", ylim=(-0.05, 1.05))
axes[1].legend()
fig.tight_layout()
fig.savefig(OUT / "transition_candidate_diagnostics.png", dpi=180, bbox_inches="tight")
plt.show()

order = np.argsort(profile_id, kind="stable")
fig, ax = plt.subplots(figsize=(8, 7))
heat = ax.imshow(consensus[np.ix_(order, order)], cmap="viridis", vmin=0, vmax=1, aspect="auto")
boundaries = np.cumsum(pd.Series(profile_id[order]).value_counts(sort=False).sort_index().to_numpy())[:-1]
for boundary in boundaries:
    ax.axhline(boundary - 0.5, color="white", linewidth=1.2)
    ax.axvline(boundary - 0.5, color="white", linewidth=1.2)
ax.set(title="Transition-planning consensus matrix", xlabel="Respondents ordered by profile", ylabel="Respondents")
fig.colorbar(heat, ax=ax, label="Proportion clustered together")
fig.tight_layout()
fig.savefig(OUT / "transition_consensus_matrix_heatmap.png", dpi=180, bbox_inches="tight")
plt.show()

J = np.eye(n) - np.ones((n, n)) / n
B = -0.5 * J @ (D ** 2) @ J
eigenvalues, eigenvectors = np.linalg.eigh(B)
eigen_order = np.argsort(eigenvalues)[::-1]
positive = eigen_order[eigenvalues[eigen_order] > 0][:2]
coordinates = eigenvectors[:, positive] * np.sqrt(eigenvalues[positive])

fig, ax = plt.subplots(figsize=(8, 6))
for pid in sorted(np.unique(profile_id)):
    mask = profile_id == pid
    ax.scatter(coordinates[mask, 0], coordinates[mask, 1], s=40, alpha=0.75, label=profile_names[int(pid)])
ax.set(title="Transition profiles in two-dimensional Gower space", xlabel="Classical MDS axis 1", ylabel="Classical MDS axis 2")
ax.legend()
fig.tight_layout()
fig.savefig(OUT / "transition_profile_scatterplot.png", dpi=180, bbox_inches="tight")
plt.show()

# %% [markdown]
# ## 9. Save reproducible outputs

# %%
variable_screening.to_csv(OUT / "transition_variable_screening.csv", index=False)
feature_audit.to_csv(OUT / "transition_feature_audit.csv", index=False)
candidate_metrics.to_csv(OUT / "transition_candidate_metrics.csv", index=False)
candidate_stability.to_csv(OUT / "transition_candidate_subsample_stability.csv", index=False)
base_partition_diagnostics.to_csv(OUT / "transition_consensus_base_partitions.csv", index=False)
assignments.to_csv(OUT / "transition_consensus_assignments.csv", index=False)
profile_sizes.to_csv(OUT / "transition_profile_sizes.csv", index=False)
profile_response_distributions.to_csv(OUT / "transition_profile_response_distributions.csv", index=False)
profile_modes.to_csv(OUT / "transition_profile_modes.csv", index=False)
medoid_profiles.to_csv(OUT / "transition_medoid_profiles.csv", index=False)
field_sector_crosstab.to_csv(OUT / "transition_study_field_by_ideal_sector.csv")
respondent_confidence.to_csv(OUT / "transition_respondent_confidence.csv", index=False)
ensemble_stability.to_csv(OUT / "transition_consensus_ensemble_stability.csv", index=False)
feature_sensitivity.to_csv(OUT / "transition_leave_one_feature_out.csv", index=False)
quality_checks.to_csv(OUT / "transition_quality_checks.csv", index=False)

consensus_export = pd.DataFrame(consensus, columns=cohort["respondent_id"])
consensus_export.insert(0, "respondent_id", cohort["respondent_id"].to_numpy())
consensus_export.to_csv(OUT / "transition_consensus_matrix.csv", index=False)

summary = {
    "cohort": {
        "records": int(len(cohort)),
        "branch": "D",
        "routing_source": "translated_final_active_branch",
    },
    "dimension": "education-to-work transition planning and direction",
    "clustering_features": CLUSTER_FEATURES,
    "descriptors": DESCRIPTOR_VARIABLES,
    "data_quality": validation,
    "method": {
        "distance": "equal-weight nominal, missing-aware Gower on four original aspiration responses",
        "candidate_k": [2, 3, 4, 5],
        "selected_k": selected_k,
        "ensemble": "equal-weight K-medoids plus spectral consensus",
        "base_partitions": 2 * CONSENSUS_SUBSAMPLES,
        "final_method": "K-medoids on one minus co-association",
    },
    "profiles": {
        "sizes": {
            str(int(row.transition_profile_id)): int(row.records)
            for row in profile_sizes.itertuples()
        },
        "names": {str(key): value for key, value in profile_names.items()},
    },
    "metrics": metrics,
    "decision": {
        "primary_checks_passed": primary_pass,
        "checks_passed": int(quality_checks["passed"].sum()),
        "checks_total": int(len(quality_checks)),
        "status": status,
    },
    "limitations": [
        "These profiles are exploratory response patterns, not a validated transition-readiness scale.",
        "All four inputs are categorical, so distances are based on exact category matches and contain ties.",
        "ICT study field and IT sector preference are common and may strongly influence grouping; leave-one-feature-out results must be reported.",
        "Search status is kept as a descriptor because including it produced a trivial already-searching versus not-yet-searching split.",
        "Job-search method is conditional and describes only the 111 respondents already searching.",
        "No study-field-to-sector alignment crosswalk or score is invented.",
    ],
}

with open(OUT / "transition_clustering_summary.json", "w", encoding="utf-8") as handle:
    json.dump(summary, handle, indent=2)

print(json.dumps(summary, indent=2))
print("\nSaved files:")
for path in sorted(OUT.iterdir()):
    print(" -", path.name)

# %% [markdown]
# ## Interpretation guardrails
#
# - These profiles describe plans, current job-search action, preferred work
#   arrangement, preferred sector, and study field.
# - They do not measure employability, ability, programme suitability, or the
#   probability of obtaining a job.
# - Profile names are descriptive summaries assigned after examining complete
#   response distributions.
# - A stable clustering solution does not prove causal or permanent youth types.
