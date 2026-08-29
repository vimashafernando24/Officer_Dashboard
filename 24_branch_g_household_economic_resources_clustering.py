# %% [markdown]
# # Branch G — household economic resources and dependency
#
# This analysis uses the 56 strict final-Branch-G respondents. Six audited survey
# variables create five equal-weight components. Household size is used to form
# worker and unemployed household shares instead of being counted a second time.
# No economic-capital score is created.
#
# Primary method: missing-aware mixed Gower distance, K-medoids and spectral
# clustering, and an equal-weight consensus of 200 matched base partitions.
# Candidate counts are k=2–4. The analysis also checks leave-one-feature-out
# sensitivity, single-question dominance, a three-component structural-resource
# sensitivity analysis, and a 100-repetition independent-column permutation null.

from pathlib import Path
import json
import warnings

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.cluster import AgglomerativeClustering, SpectralClustering
from sklearn.metrics import adjusted_rand_score, silhouette_samples, silhouette_score

warnings.filterwarnings("ignore", category=FutureWarning)
pd.set_option("display.max_columns", 100)
pd.set_option("display.width", 220)

ROOT = Path.cwd()
VALUES_PATH = ROOT / "outputs/nysc_survey_cleaned_values.csv"
LABELS_PATH = ROOT / "outputs/nysc_survey_cleaned_labels.csv"
OUT = ROOT / "outputs/branch_g_household_economic_resources_clusters"
OUT.mkdir(parents=True, exist_ok=True)

SOURCE_VARIABLES = [
    "household_income",
    "household_size",
    "household_workers",
    "household_unemployed",
    "primary_earner_status",
    "primary_income_source",
]
CLUSTER_FEATURES = [
    "household_income_position",
    "household_worker_share",
    "household_unemployed_share",
    "primary_earner_responsibility",
    "primary_income_source",
]
STRUCTURAL_RESOURCE_FEATURES = [
    "household_income_position",
    "household_worker_share",
    "household_unemployed_share",
]
FEATURE_TYPES = {
    "household_income_position": "ordinal",
    "household_worker_share": "continuous",
    "household_unemployed_share": "continuous",
    "primary_earner_responsibility": "ordinal",
    "primary_income_source": "nominal",
}

RANDOM_STATE = 20260826
MIN_PROFILE_SIZE = 15
CANDIDATE_SUBSAMPLES = 40
CONSENSUS_SUBSAMPLES = 100
SUBSAMPLE_FRACTION = 0.80
ENSEMBLE_BOOTSTRAPS = 100
PERMUTATION_REPETITIONS = 100


# %% [markdown]
# ## 1. Strict final-Branch-G cohort

values_all = pd.read_csv(VALUES_PATH)
labels_all = pd.read_csv(LABELS_PATH)
strict_mask = (
    values_all["branch"].eq("G")
    & values_all["branch_routing_source"].eq("translated_final_active_branch")
    & ~values_all["branch_integrity_issue"].astype(bool)
)

admin_columns = [
    "respondent_id", "entry_branch", "branch", "branch_routing_source",
    "branch_path_disagreement", "branch_integrity_issue",
]
values = values_all.loc[strict_mask, admin_columns + SOURCE_VARIABLES].copy()
labels = labels_all.loc[strict_mask, ["respondent_id"] + SOURCE_VARIABLES].copy()
values = values.rename(columns={v: f"{v}__value" for v in SOURCE_VARIABLES})
labels = labels.rename(columns={v: f"{v}__response" for v in SOURCE_VARIABLES})
cohort = values.merge(labels, on="respondent_id", validate="one_to_one")

assert len(cohort) == 56
assert cohort["respondent_id"].nunique() == 56
assert cohort["branch"].eq("G").all()


# %% [markdown]
# ## 2. Audit and construct five theory-safe components

screening_rows = []
for variable in SOURCE_VARIABLES:
    response = cohort[f"{variable}__response"]
    counts_response = response.value_counts(dropna=False)
    screening_rows.append({
        "variable": variable,
        "observed": int(response.notna().sum()),
        "missing": int(response.isna().sum()),
        "unique_observed_responses": int(response.nunique(dropna=True)),
        "dominant_response": str(counts_response.index[0]),
        "dominant_response_percent": 100 * float(counts_response.iloc[0] / len(response)),
    })
variable_screening = pd.DataFrame(screening_rows)

reported_counts = pd.DataFrame({
    "household_size": pd.to_numeric(cohort["household_size__value"], errors="coerce"),
    "household_workers": pd.to_numeric(cohort["household_workers__value"], errors="coerce"),
    "household_unemployed": pd.to_numeric(cohort["household_unemployed__value"], errors="coerce"),
})
invalid_counts = (
    reported_counts.isna().any(axis=1)
    | reported_counts.lt(0).any(axis=1)
    | reported_counts["household_size"].le(0)
    | reported_counts["household_workers"].gt(reported_counts["household_size"])
    | reported_counts["household_unemployed"].gt(reported_counts["household_size"])
    | (
        reported_counts["household_workers"]
        + reported_counts["household_unemployed"]
        > reported_counts["household_size"]
    )
)
count_issue_audit = pd.concat(
    [
        cohort.loc[invalid_counts, ["respondent_id"]].reset_index(drop=True),
        reported_counts.loc[invalid_counts].reset_index(drop=True),
    ],
    axis=1,
)
count_issue_audit["issue"] = "household counts internally inconsistent"

features = pd.DataFrame(index=cohort.index)
income = pd.to_numeric(cohort["household_income__value"], errors="coerce")
features["household_income_position"] = income.where(income.between(1, 5)).map(
    {1: 0.0, 2: 0.25, 3: 0.50, 4: 0.75, 5: 1.0}
)
features["household_worker_share"] = (
    reported_counts["household_workers"] / reported_counts["household_size"]
).where(~invalid_counts)
features["household_unemployed_share"] = (
    reported_counts["household_unemployed"] / reported_counts["household_size"]
).where(~invalid_counts)
features["primary_earner_responsibility"] = cohort["primary_earner_status__value"].map(
    {"no": 0.0, "shared": 0.5, "yes": 1.0}
)
features["primary_income_source"] = (
    cohort["primary_income_source__value"].astype("string").replace("<NA>", pd.NA)
)

feature_audit = pd.DataFrame({
    "feature": CLUSTER_FEATURES,
    "source_variables": [
        "household_income",
        "household_size + household_workers",
        "household_size + household_unemployed",
        "primary_earner_status",
        "primary_income_source",
    ],
    "type": [FEATURE_TYPES[v] for v in CLUSTER_FEATURES],
    "observed": [int(features[v].notna().sum()) for v in CLUSTER_FEATURES],
    "missing": [int(features[v].isna().sum()) for v in CLUSTER_FEATURES],
    "maximum_distance_weight": [1 / len(CLUSTER_FEATURES)] * len(CLUSTER_FEATURES),
})
respondent_component_coverage = features.notna().sum(axis=1)
# Retain and flag any respondent with fewer than three usable components rather
# than inventing values or deleting the record. Invalid household counts make
# only the two derived share components unavailable.
assert respondent_component_coverage.min() >= 2


def mixed_gower(frame, columns=None):
    columns = list(frame.columns) if columns is None else list(columns)
    n = len(frame)
    numerator = np.zeros((n, n), dtype=float)
    denominator = np.zeros((n, n), dtype=float)
    for column in columns:
        kind = FEATURE_TYPES[column]
        if kind == "nominal":
            series = frame[column].astype("string")
            observed = series.notna().to_numpy()
            values_column = series.fillna("__MISSING__").to_numpy(dtype=str)
            difference = (values_column[:, None] != values_column[None, :]).astype(float)
        else:
            series = pd.to_numeric(frame[column], errors="coerce")
            observed = series.notna().to_numpy()
            values_column = series.fillna(0).to_numpy(dtype=float)
            difference = np.abs(values_column[:, None] - values_column[None, :])
            if kind == "continuous":
                valid = values_column[observed]
                span = float(valid.max() - valid.min())
                difference = difference / span if span > 0 else np.zeros_like(difference)
        pair_observed = observed[:, None] & observed[None, :]
        numerator += np.where(pair_observed, difference, 0.0)
        denominator += pair_observed
    distance = np.divide(
        numerator, denominator,
        out=np.zeros_like(numerator), where=denominator > 0,
    )
    np.fill_diagonal(distance, 0.0)
    return distance, denominator


D, pair_coverage = mixed_gower(features, CLUSTER_FEATURES)
assert np.allclose(D, D.T)
assert D.min() >= 0 and D.max() <= 1
positive_distances = D[D > 0]
sigma = float(np.median(positive_distances))


def affinity(distance):
    positive = distance[distance > 0]
    local_sigma = float(np.median(positive)) if len(positive) else 1.0
    result = np.exp(-(distance ** 2) / (2 * local_sigma ** 2))
    np.fill_diagonal(result, 1.0)
    return result


def fit_kmedoids(distance, k, n_init=150, max_iter=150, random_state=RANDOM_STATE):
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
    medoids = []
    for cluster in sorted(np.unique(labels_k)):
        members = np.flatnonzero(labels_k == cluster)
        within = distance[np.ix_(members, members)]
        medoids.append(members[np.argmin(within.sum(axis=1))])
    return np.asarray(medoids, dtype=int)


# %% [markdown]
# ## 3. Candidate k comparison

def subsample_stability(distance, algorithm, k, reference_labels):
    offset = 0 if algorithm == "kmedoids" else 10000
    rng = np.random.default_rng(RANDOM_STATE + 100 * k + offset)
    rows = []
    sample_size = int(np.floor(SUBSAMPLE_FRACTION * len(distance)))
    for repetition in range(CANDIDATE_SUBSAMPLES):
        idx = np.sort(rng.choice(len(distance), size=sample_size, replace=False))
        D_sub = distance[np.ix_(idx, idx)]
        if algorithm == "kmedoids":
            result = fit_kmedoids(
                D_sub, k, n_init=60,
                random_state=RANDOM_STATE + 1000 * k + repetition,
            )
            medoids = idx[result["medoids"]]
        else:
            labels_sub = SpectralClustering(
                n_clusters=k, affinity="precomputed", assign_labels="kmeans",
                n_init=30, random_state=RANDOM_STATE + 2000 * k + repetition,
            ).fit_predict(affinity(D_sub))
            medoids = idx[medoids_from_labels(D_sub, labels_sub)]
        predicted = np.argmin(distance[:, medoids], axis=1)
        rows.append(adjusted_rand_score(reference_labels, predicted))
    return np.asarray(rows)


candidate_rows = []
candidate_stability_rows = []
full_source_solutions = {}
for k in range(2, 5):
    kmedoids = fit_kmedoids(D, k, n_init=400, random_state=RANDOM_STATE + k)
    spectral_labels = SpectralClustering(
        n_clusters=k, affinity="precomputed", assign_labels="kmeans",
        n_init=100, random_state=RANDOM_STATE + 100 + k,
    ).fit_predict(affinity(D))
    full_source_solutions[("kmedoids", k)] = kmedoids["labels"]
    full_source_solutions[("spectral", k)] = spectral_labels
    method_metrics = {}
    for algorithm, labels_k in [
        ("kmedoids", kmedoids["labels"]), ("spectral", spectral_labels)
    ]:
        stability = subsample_stability(D, algorithm, k, labels_k)
        method_metrics[algorithm] = {
            "silhouette": float(silhouette_score(D, labels_k, metric="precomputed")),
            "stability_mean": float(stability.mean()),
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
        "kmedoids_silhouette": method_metrics["kmedoids"]["silhouette"],
        "spectral_silhouette": method_metrics["spectral"]["silhouette"],
        "mean_source_silhouette": np.mean([
            method_metrics["kmedoids"]["silhouette"],
            method_metrics["spectral"]["silhouette"],
        ]),
        "kmedoids_stability_mean": method_metrics["kmedoids"]["stability_mean"],
        "spectral_stability_mean": method_metrics["spectral"]["stability_mean"],
        "mean_source_stability": np.mean([
            method_metrics["kmedoids"]["stability_mean"],
            method_metrics["spectral"]["stability_mean"],
        ]),
        "minimum_source_p10_stability": min(
            method_metrics["kmedoids"]["stability_p10"],
            method_metrics["spectral"]["stability_p10"],
        ),
        "source_algorithm_ari": adjusted_rand_score(
            kmedoids["labels"], spectral_labels
        ),
        "minimum_cluster_size_across_sources": min(
            method_metrics["kmedoids"]["minimum_size"],
            method_metrics["spectral"]["minimum_size"],
        ),
    })

candidate_metrics = pd.DataFrame(candidate_rows)
candidate_stability = pd.DataFrame(candidate_stability_rows)
eligible = candidate_metrics.loc[
    candidate_metrics["minimum_cluster_size_across_sources"].ge(MIN_PROFILE_SIZE)
].copy()
if eligible.empty:
    raise RuntimeError("No k=2–4 candidate meets the minimum profile-size rule.")
eligible["rank_mean_silhouette"] = eligible["mean_source_silhouette"].rank(
    ascending=False, method="min"
)
eligible["rank_mean_stability"] = eligible["mean_source_stability"].rank(
    ascending=False, method="min"
)
eligible["primary_mean_rank"] = eligible[[
    "rank_mean_silhouette", "rank_mean_stability"
]].mean(axis=1)
selected_k = int(
    eligible.sort_values(["primary_mean_rank", "k"]).iloc[0]["k"]
)
candidate_metrics = candidate_metrics.merge(
    eligible[["k", "primary_mean_rank"]], on="k", how="left"
)
candidate_metrics["selected"] = candidate_metrics["k"].eq(selected_k)


# %% [markdown]
# ## 4. Equal-weight K-medoids + spectral consensus

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
        n_clusters=selected_k, affinity="precomputed", assign_labels="kmeans",
        n_init=30, random_state=RANDOM_STATE + 50000 + repetition,
    ).fit_predict(affinity(D_sub))
    for algorithm, labels_sub in [
        ("kmedoids", kmedoids_sub), ("spectral", spectral_sub)
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

# Reorder profiles from lower to higher median household-income position, then
# worker share. The order is descriptive and does not imply respondent worth.
raw_order = sorted(
    np.unique(raw_labels),
    key=lambda cluster: (
        features.loc[raw_labels == cluster, "household_income_position"].median(),
        features.loc[raw_labels == cluster, "household_worker_share"].median(),
        int(cluster),
    ),
)
raw_to_profile = {int(raw): i + 1 for i, raw in enumerate(raw_order)}
profile_id = np.asarray([raw_to_profile[int(label)] for label in raw_labels])
profile_names = {
    1: "Predominantly family/partner-supported non-provider",
    2: "Predominantly self-income provider/contributor",
}


# %% [markdown]
# ## 5. Profile and validate the solution

assignments = cohort[admin_columns].copy()
for variable in SOURCE_VARIABLES:
    assignments[f"{variable}__value"] = cohort[f"{variable}__value"]
    assignments[f"{variable}__response"] = cohort[f"{variable}__response"]
for feature in CLUSTER_FEATURES:
    assignments[feature] = features[feature]
assignments["economic_profile_id"] = profile_id
assignments["economic_profile_label"] = assignments["economic_profile_id"].map(profile_names)
assignments["observed_economic_components"] = respondent_component_coverage.to_numpy()
assignments["low_component_coverage"] = assignments["observed_economic_components"].lt(3)
assignments["gower_individual_silhouette"] = silhouette_samples(
    D, profile_id, metric="precomputed"
)
assignments["consensus_individual_silhouette"] = silhouette_samples(
    consensus_distance, profile_id, metric="precomputed"
)

profile_sizes = (
    assignments.groupby(["economic_profile_id", "economic_profile_label"], as_index=False)
    .agg(
        records=("respondent_id", "size"),
        low_gower_confidence_records=(
            "gower_individual_silhouette", lambda x: int((x < 0.10).sum())
        ),
        mean_gower_silhouette=("gower_individual_silhouette", "mean"),
        mean_consensus_silhouette=("consensus_individual_silhouette", "mean"),
    )
)
profile_sizes["percent"] = 100 * profile_sizes["records"] / len(assignments)

response_rows = []
for variable in SOURCE_VARIABLES:
    response_col = f"{variable}__response"
    temp = (
        assignments.groupby(["economic_profile_id", response_col], dropna=False)
        .size().rename("records").reset_index()
    )
    temp["within_profile_percent"] = (
        100 * temp["records"]
        / temp.groupby("economic_profile_id")["records"].transform("sum")
    )
    temp = temp.rename(columns={response_col: "response"})
    temp.insert(1, "variable", variable)
    response_rows.append(temp)
profile_response_distributions = pd.concat(response_rows, ignore_index=True)
profile_modes = (
    profile_response_distributions.sort_values(
        ["economic_profile_id", "variable", "within_profile_percent"],
        ascending=[True, True, False],
    ).groupby(["economic_profile_id", "variable"], as_index=False).first()
)
numeric_profile_medians = (
    assignments.groupby("economic_profile_id")[
        [
            "household_income_position", "household_worker_share",
            "household_unemployed_share", "primary_earner_responsibility",
        ]
    ].median()
)

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
        "economic_profile_id": int(own),
        "within_profile_consensus": within,
        "strongest_other_profile_consensus": strongest_other,
        "consensus_margin": within - strongest_other,
        "ambiguous_consensus_membership": (
            (within < 0.70) or ((within - strongest_other) < 0.20)
        ),
    })
respondent_confidence = pd.DataFrame(confidence_rows)
assignments = assignments.merge(
    respondent_confidence.drop(columns="economic_profile_id"),
    on="respondent_id", validate="one_to_one",
)

bootstrap_rng = np.random.default_rng(RANDOM_STATE + 70000)
ensemble_stability_rows = []
for repetition in range(ENSEMBLE_BOOTSTRAPS):
    chosen = bootstrap_rng.choice(len(cover_stack), size=len(cover_stack), replace=True)
    boot_cover = cover_stack[chosen].sum(axis=0)
    boot_same = same_stack[chosen].sum(axis=0)
    boot_consensus = np.divide(
        boot_same, boot_cover,
        out=np.zeros_like(boot_same, dtype=float), where=boot_cover > 0,
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

# Leave-one-feature-out and single-feature dominance checks.
feature_sensitivity_rows = []
single_feature_rows = []
for feature in CLUSTER_FEATURES:
    retained = [column for column in CLUSTER_FEATURES if column != feature]
    D_reduced, coverage_reduced = mixed_gower(features, retained)
    reduced_fit = fit_kmedoids(
        D_reduced, selected_k, n_init=300,
        random_state=RANDOM_STATE + 90000 + CLUSTER_FEATURES.index(feature),
    )
    feature_sensitivity_rows.append({
        "omitted_feature": feature,
        "minimum_pair_coverage": int(coverage_reduced.min()),
        "gower_silhouette_reduced": silhouette_score(
            D_reduced, reduced_fit["labels"], metric="precomputed"
        ),
        "ari_reduced_kmedoids_vs_final_consensus": adjusted_rand_score(
            profile_id, reduced_fit["labels"]
        ),
    })
    D_single, _ = mixed_gower(features, [feature])
    single_fit = fit_kmedoids(
        D_single, selected_k, n_init=300,
        random_state=RANDOM_STATE + 91000 + CLUSTER_FEATURES.index(feature),
    )
    single_feature_rows.append({
        "single_feature": feature,
        "ari_single_feature_vs_final_consensus": adjusted_rand_score(
            profile_id, single_fit["labels"]
        ),
    })
feature_sensitivity = pd.DataFrame(feature_sensitivity_rows)
single_feature_dominance = pd.DataFrame(single_feature_rows)

D_structural, _ = mixed_gower(features, STRUCTURAL_RESOURCE_FEATURES)
structural_fit = fit_kmedoids(
    D_structural, selected_k, n_init=500,
    random_state=RANDOM_STATE + 92000,
)
structural_resource_sensitivity_ari = float(adjusted_rand_score(
    profile_id, structural_fit["labels"]
))

# Independent-column permutation null. The search over k=2–4 is repeated in
# every permutation to calibrate the best observed K-medoids silhouette.
observed_eligible = candidate_metrics.loc[
    candidate_metrics["minimum_cluster_size_across_sources"].ge(MIN_PROFILE_SIZE)
]
observed_max_kmedoids_silhouette = float(
    observed_eligible["kmedoids_silhouette"].max()
)
permutation_rng = np.random.default_rng(RANDOM_STATE + 100000)
permutation_rows = []
for repetition in range(PERMUTATION_REPETITIONS):
    shuffled = features.copy()
    for column in CLUSTER_FEATURES:
        shuffled[column] = permutation_rng.permutation(shuffled[column].to_numpy())
    D_null, _ = mixed_gower(shuffled, CLUSTER_FEATURES)
    null_solutions = []
    for k in range(2, 5):
        null_fit = fit_kmedoids(
            D_null, k, n_init=80,
            random_state=RANDOM_STATE + 101000 + 10 * repetition + k,
        )
        minimum_size = int(pd.Series(null_fit["labels"]).value_counts().min())
        if minimum_size >= MIN_PROFILE_SIZE:
            null_solutions.append(silhouette_score(
                D_null, null_fit["labels"], metric="precomputed"
            ))
    permutation_rows.append({
        "repetition": repetition + 1,
        "maximum_valid_kmedoids_silhouette": (
            max(null_solutions) if null_solutions else np.nan
        ),
    })
permutation_null = pd.DataFrame(permutation_rows)
valid_null = permutation_null["maximum_valid_kmedoids_silhouette"].dropna()
empirical_permutation_p = float(
    (1 + (valid_null >= observed_max_kmedoids_silhouette).sum())
    / (1 + len(valid_null))
)

upper = consensus[np.triu_indices(n, 1)]
maximum_single_feature_ari = float(
    single_feature_dominance["ari_single_feature_vs_final_consensus"].max()
)
dominant_single_feature = str(
    single_feature_dominance.sort_values(
        "ari_single_feature_vs_final_consensus", ascending=False
    ).iloc[0]["single_feature"]
)
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
    "ari_vs_consensus_hac_average": float(
        adjusted_rand_score(profile_id, consensus_hac_average)
    ),
    "ari_vs_consensus_hac_complete": float(
        adjusted_rand_score(profile_id, consensus_hac_complete)
    ),
    "structural_resource_only_sensitivity_ari": structural_resource_sensitivity_ari,
    "minimum_leave_one_feature_out_ari": float(
        feature_sensitivity["ari_reduced_kmedoids_vs_final_consensus"].min()
    ),
    "maximum_single_feature_ari": maximum_single_feature_ari,
    "dominant_single_feature": dominant_single_feature,
    "minimum_profile_size": int(pd.Series(profile_id).value_counts().min()),
    "low_gower_confidence_percent": 100 * float(
        np.mean(assignments["gower_individual_silhouette"] < 0.10)
    ),
    "ambiguous_consensus_percent": 100 * float(
        assignments["ambiguous_consensus_membership"].mean()
    ),
    "pac_10_90": float(np.mean((upper > 0.10) & (upper < 0.90))),
    "observed_maximum_kmedoids_silhouette": observed_max_kmedoids_silhouette,
    "permutation_null_maximum_silhouette_median": float(valid_null.median()),
    "permutation_null_maximum_silhouette_p95": float(valid_null.quantile(0.95)),
    "empirical_permutation_p": empirical_permutation_p,
}

quality_checks = pd.DataFrame([
    {"check": "original Gower silhouette >= 0.25", "value": metrics["gower_silhouette"], "passed": metrics["gower_silhouette"] >= 0.25},
    {"check": "ensemble bootstrap mean ARI >= 0.80", "value": metrics["ensemble_bootstrap_ari_mean"], "passed": metrics["ensemble_bootstrap_ari_mean"] >= 0.80},
    {"check": f"minimum profile size >= {MIN_PROFILE_SIZE}", "value": metrics["minimum_profile_size"], "passed": metrics["minimum_profile_size"] >= MIN_PROFILE_SIZE},
    {"check": "ARI with full K-medoids >= 0.60", "value": metrics["ari_vs_full_kmedoids"], "passed": metrics["ari_vs_full_kmedoids"] >= 0.60},
    {"check": "ARI with full spectral >= 0.60", "value": metrics["ari_vs_full_spectral"], "passed": metrics["ari_vs_full_spectral"] >= 0.60},
    {"check": "not near-exactly reproduced by one feature (ARI < 0.90)", "value": metrics["maximum_single_feature_ari"], "passed": metrics["maximum_single_feature_ari"] < 0.90},
    {"check": "permutation screening p < 0.05", "value": metrics["empirical_permutation_p"], "passed": metrics["empirical_permutation_p"] < 0.05},
    {"check": "ambiguous consensus respondents <= 20%", "value": metrics["ambiguous_consensus_percent"], "passed": metrics["ambiguous_consensus_percent"] <= 20},
    {"check": "low-confidence respondents in original Gower space <= 20%", "value": metrics["low_gower_confidence_percent"], "passed": metrics["low_gower_confidence_percent"] <= 20},
])
primary_pass = bool(quality_checks.iloc[:7]["passed"].all())
if primary_pass:
    status = (
        "Retained as an exploratory household economic role/dependency "
        "segmentation; not interpreted as resource level alone"
    )
else:
    status = "No sufficiently robust Branch G household-economic segmentation found"


# %% [markdown]
# ## 6. Visual outputs

fig, axes = plt.subplots(1, 2, figsize=(12, 4.5))
axes[0].plot(candidate_metrics["k"], candidate_metrics["mean_source_silhouette"], marker="o")
axes[0].axvline(selected_k, color="tab:red", linestyle="--", label=f"selected k={selected_k}")
axes[0].set(title="Candidate separation", xlabel="Number of profiles", ylabel="Mean Gower silhouette")
axes[0].legend()
axes[1].plot(candidate_metrics["k"], candidate_metrics["mean_source_stability"], marker="o", label="mean source stability")
axes[1].plot(candidate_metrics["k"], candidate_metrics["source_algorithm_ari"], marker="s", label="K-medoids vs spectral ARI")
axes[1].axvline(selected_k, color="tab:red", linestyle="--")
axes[1].set(title="Stability and source agreement", xlabel="Number of profiles", ylabel="ARI", ylim=(-0.05, 1.05))
axes[1].legend()
fig.tight_layout()
fig.savefig(OUT / "household_economic_candidate_diagnostics.png", dpi=180, bbox_inches="tight")
plt.close(fig)

J = np.eye(n) - np.ones((n, n)) / n
B = -0.5 * J @ (D ** 2) @ J
eigenvalues, eigenvectors = np.linalg.eigh(B)
order = np.argsort(eigenvalues)[::-1]
positive = order[eigenvalues[order] > 0][:2]
coordinates = eigenvectors[:, positive] * np.sqrt(eigenvalues[positive])
fig, ax = plt.subplots(figsize=(8, 6))
for pid in sorted(np.unique(profile_id)):
    mask = profile_id == pid
    ax.scatter(
        coordinates[mask, 0], coordinates[mask, 1], s=36, alpha=0.72,
        edgecolor="white", linewidth=0.4, label=profile_names[int(pid)],
    )
ax.set(
    title="Branch G household-economic response patterns",
    xlabel="Classical MDS axis 1 (display coordinate only)",
    ylabel="Classical MDS axis 2 (display coordinate only)",
)
ax.legend()
fig.tight_layout()
fig.savefig(OUT / "household_economic_profile_scatterplot.png", dpi=180, bbox_inches="tight")
plt.close(fig)


# %% [markdown]
# ## 7. Save reproducible outputs and decision

variable_screening.to_csv(OUT / "household_economic_variable_screening.csv", index=False)
count_issue_audit.to_csv(OUT / "household_economic_count_issues.csv", index=False)
feature_audit.to_csv(OUT / "household_economic_feature_audit.csv", index=False)
candidate_metrics.to_csv(OUT / "household_economic_candidate_metrics.csv", index=False)
candidate_stability.to_csv(OUT / "household_economic_candidate_subsample_stability.csv", index=False)
base_partition_diagnostics.to_csv(OUT / "household_economic_consensus_base_partitions.csv", index=False)
assignments.to_csv(OUT / "household_economic_consensus_assignments.csv", index=False)
profile_sizes.to_csv(OUT / "household_economic_profile_sizes.csv", index=False)
profile_response_distributions.to_csv(OUT / "household_economic_profile_response_distributions.csv", index=False)
profile_modes.to_csv(OUT / "household_economic_profile_modes.csv", index=False)
numeric_profile_medians.to_csv(OUT / "household_economic_profile_numeric_medians.csv")
respondent_confidence.to_csv(OUT / "household_economic_respondent_confidence.csv", index=False)
ensemble_stability.to_csv(OUT / "household_economic_consensus_ensemble_stability.csv", index=False)
feature_sensitivity.to_csv(OUT / "household_economic_leave_one_feature_out.csv", index=False)
single_feature_dominance.to_csv(OUT / "household_economic_single_feature_dominance.csv", index=False)
permutation_null.to_csv(OUT / "household_economic_permutation_null.csv", index=False)
quality_checks.to_csv(OUT / "household_economic_quality_checks.csv", index=False)

consensus_export = pd.DataFrame(consensus, columns=cohort["respondent_id"])
consensus_export.insert(0, "respondent_id", cohort["respondent_id"].to_numpy())
consensus_export.to_csv(OUT / "household_economic_consensus_matrix.csv", index=False)

summary = {
    "cohort": {
        "records": int(len(cohort)),
        "branch": "G",
        "routing_source": "translated_final_active_branch",
        "strict_final_branch_records": 56,
        "excluded_routing_integrity_records": 0,
    },
    "dimension": "household economic resources and dependency",
    "source_variables": SOURCE_VARIABLES,
    "clustering_components": CLUSTER_FEATURES,
    "data_quality": {
        "income_prefer_not_to_say": int(income.eq(99).sum()),
        "household_count_conflicts": int(invalid_counts.sum()),
        "respondents_with_fewer_than_three_observed_components": int(
            (respondent_component_coverage < 3).sum()
        ),
        "minimum_pair_feature_coverage": int(pair_coverage.min()),
    },
    "method": {
        "distance": "equal-weight missing-aware mixed Gower on five components derived from six original survey variables",
        "candidate_k": [2, 3, 4],
        "selected_k": selected_k,
        "ensemble": "equal-weight K-medoids plus spectral consensus",
        "base_partitions": 2 * CONSENSUS_SUBSAMPLES,
        "permutation_repetitions": PERMUTATION_REPETITIONS,
        "pac_policy": "comparative only; no universal absolute cutoff",
    },
    "profiles": {
        "sizes": {
            str(int(row.economic_profile_id)): int(row.records)
            for row in profile_sizes.itertuples()
        },
        "names": {str(key): value for key, value in profile_names.items()},
    },
    "metrics": metrics,
    "decision": {
        "retained_for_clustering": primary_pass,
        "checks_passed": int(quality_checks["passed"].sum()),
        "checks_total": int(len(quality_checks)),
        "status": status,
    },
    "limitations": [
        "These are exploratory household-economic response profiles, not validated economic-capital classes.",
        "Household size is used as a denominator for worker/unemployed shares rather than receiving an additional distance weight.",
        "Income prefer-not-to-say is pairwise unavailable rather than ranked as an income level.",
        "Respondents with fewer than three usable components after income refusal/count checks are retained and explicitly flagged rather than imputed or deleted.",
        "Primary income source is nominal and may create a direct job-versus-family-support split; single-feature and structural-only sensitivity are reported.",
        "The structural-resource-only partition has ARI near zero with the final profiles, so the result must be interpreted mainly as household economic role/dependency, not as low-versus-high household resources.",
        "Permutation calibration tests whether the selected structure exceeds independently shuffled variables, but it does not establish theoretical construct validity.",
        "The Branch G sample contains only 56 valid respondents; confirmation in additional data is required.",
    ],
}
with open(OUT / "household_economic_clustering_summary.json", "w", encoding="utf-8") as handle:
    json.dump(summary, handle, indent=2)

print(json.dumps(summary, indent=2))
print("\nProfile modes:\n", profile_modes.to_string(index=False))
print("\nQuality checks:\n", quality_checks.to_string(index=False))
print("\nSaved outputs to", OUT)
