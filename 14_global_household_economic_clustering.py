# %% [markdown]
# # Global common dimension 1 — household economic resource structure
#
# This notebook clusters the 363 valid new-structure respondents across Branches
# D, E, F, and G. Branch is never used to calculate distance; it is examined only
# after clustering to describe how the resulting global profiles are distributed.

# %% [markdown]
# ## Theory and measurement decisions
#
# Bourdieu's economic capital supports the use of household economic resources.
# The ILO SWTS household module supplies household composition and income-source
# indicators. Four original responses are compared with equal maximum weight:
# household income, household size, workers, and unemployed jobseekers. Primary-
# earner status and primary income source remain descriptors because screening
# showed that each mainly created a direct categorical split rather than a
# multidimensional household-resource profile.
#
# No respondent-level economic score is invented. Mixed-data Gower distance is:
#
# $$d(i,j)=\frac{\sum_h m_{ijh}\,\delta_{ijh}}{\sum_h m_{ijh}}$$
#
# where $m_{ijh}=1$ only when feature $h$ is valid for both respondents. Income
# and household counts use normalized ordered-category positions, which preserves
# order without allowing two extreme counts to compress all other differences.

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
OUT = ROOT / "outputs/global_household_economic_clusters"
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
    "household_income",
    "household_size",
    "household_workers",
    "household_unemployed",
]
DESCRIPTOR_VARIABLES = ["primary_earner_status", "primary_income_source"]
FEATURE_TYPES = {
    "household_income": "ordinal",
    "household_size": "ordinal",
    "household_workers": "ordinal",
    "household_unemployed": "ordinal",
    "primary_earner_status": "ordinal",
    "primary_income_source": "nominal",
}

RANDOM_STATE = 20260824
MIN_PROFILE_SIZE = 25
CANDIDATE_SUBSAMPLES = 50
CONSENSUS_SUBSAMPLES = 100
SUBSAMPLE_FRACTION = 0.80
ENSEMBLE_BOOTSTRAPS = 100

# %% [markdown]
# ## 1. Construct the strict global cohort

# %%
values_all = pd.read_csv(VALUES_PATH)
labels_all = pd.read_csv(LABELS_PATH)

strict_mask = (
    values_all["branch_routing_source"].eq("translated_final_active_branch")
    & values_all["branch"].isin(list("DEFG"))
)

values = values_all.loc[strict_mask, [
    "respondent_id", "entry_branch", "branch", "branch_routing_source",
    "branch_path_disagreement", "branch_integrity_issue",
] + SOURCE_VARIABLES].copy()
labels = labels_all.loc[strict_mask, ["respondent_id"] + SOURCE_VARIABLES].copy()
labels = labels.rename(columns={v: f"{v}__response" for v in SOURCE_VARIABLES})
values = values.rename(columns={v: f"{v}__value" for v in SOURCE_VARIABLES})
cohort = values.merge(labels, on="respondent_id", validate="one_to_one")

branch_counts = cohort["branch"].value_counts().sort_index()
validation = {
    "records": int(len(cohort)),
    "unique_ids": int(cohort["respondent_id"].nunique()),
    "wrong_routing_source": int(
        cohort["branch_routing_source"].ne("translated_final_active_branch").sum()
    ),
    "branch_D": int(branch_counts.get("D", 0)),
    "branch_E": int(branch_counts.get("E", 0)),
    "branch_F": int(branch_counts.get("F", 0)),
    "branch_G": int(branch_counts.get("G", 0)),
}
assert validation == {
    "records": 363,
    "unique_ids": 363,
    "wrong_routing_source": 0,
    "branch_D": 191,
    "branch_E": 34,
    "branch_F": 82,
    "branch_G": 56,
}
display(pd.Series(validation, name="value").to_frame())

# %% [markdown]
# ## 2. Audit the six source variables

# %%
screening_rows = []
for variable in SOURCE_VARIABLES:
    response = cohort[f"{variable}__response"]
    counts = response.value_counts(dropna=False)
    screening_rows.append({
        "variable": variable,
        "type": FEATURE_TYPES[variable],
        "observed": int(response.notna().sum()),
        "missing": int(response.isna().sum()),
        "unique_observed_responses": int(response.nunique(dropna=True)),
        "dominant_response": str(counts.index[0]),
        "dominant_response_percent": 100 * float(counts.iloc[0] / len(response)),
    })
variable_screening = pd.DataFrame(screening_rows)

counts = cohort[[
    "household_size__value", "household_workers__value",
    "household_unemployed__value",
]].apply(pd.to_numeric, errors="coerce")
counts.columns = ["household_size", "household_workers", "household_unemployed"]
invalid_negative = counts.lt(0).any(axis=1)
inconsistent_counts = (
    counts["household_workers"] + counts["household_unemployed"]
    > counts["household_size"]
)
count_issue_audit = cohort.loc[
    invalid_negative | inconsistent_counts,
    ["respondent_id", "branch"],
].copy()
count_issue_audit = pd.concat(
    [count_issue_audit.reset_index(drop=True), counts.loc[invalid_negative | inconsistent_counts].reset_index(drop=True)],
    axis=1,
)
count_issue_audit["issue"] = np.where(
    invalid_negative.loc[invalid_negative | inconsistent_counts].to_numpy(),
    "negative household count",
    "workers plus unemployed exceeds household size",
)

count_outlier_audit = counts.describe(percentiles=[0.01, 0.05, 0.95, 0.99]).T
display(variable_screening.round(2))
display(count_outlier_audit.round(2))
display(count_issue_audit)
print("Household count conflicts:", len(count_issue_audit))

# %% [markdown]
# ## 3. Create theory-safe original-response features
#
# `Prefer not to say` for household income is unavailable, not a low or high
# income category. For the 15 internally inconsistent households, the worker and
# unemployed counts are unavailable; the original values remain in the audit.

# %%
features = pd.DataFrame(index=cohort.index)

income = pd.to_numeric(cohort["household_income__value"], errors="coerce")
features["household_income"] = income.where(income.between(1, 5)).map(
    {1: 0.0, 2: 0.25, 3: 0.50, 4: 0.75, 5: 1.0}
)
raw_valid_counts = pd.DataFrame(index=cohort.index)
raw_valid_counts["household_size"] = counts["household_size"].where(~invalid_negative)
raw_valid_counts["household_workers"] = counts["household_workers"].where(
    ~invalid_negative & ~inconsistent_counts
)
raw_valid_counts["household_unemployed"] = counts["household_unemployed"].where(
    ~invalid_negative & ~inconsistent_counts
)
count_rank_rows = []
for column in raw_valid_counts:
    observed_values = sorted(raw_valid_counts[column].dropna().unique())
    rank_map = {
        value: rank / (len(observed_values) - 1) if len(observed_values) > 1 else 0.0
        for rank, value in enumerate(observed_values)
    }
    features[column] = raw_valid_counts[column].map(rank_map)
    count_rank_rows.extend({
        "feature": column, "reported_count": value,
        "normalized_order_position": position,
    } for value, position in rank_map.items())
count_rank_audit = pd.DataFrame(count_rank_rows)
features["primary_earner_status"] = cohort["primary_earner_status__value"].map(
    {"no": 0.0, "shared": 0.5, "yes": 1.0}
)
feature_audit = pd.DataFrame({
    "feature": CLUSTER_FEATURES,
    "type": [FEATURE_TYPES[v] for v in CLUSTER_FEATURES],
    "observed": [int(features[v].notna().sum()) for v in CLUSTER_FEATURES],
    "missing": [int(features[v].isna().sum()) for v in CLUSTER_FEATURES],
    "maximum_weight_when_observed": [1 / len(CLUSTER_FEATURES)] * len(CLUSTER_FEATURES),
})
assert features.notna().sum(axis=1).min() >= 1
display(feature_audit)


def mixed_gower(frame, columns=None, feature_types=None):
    columns = list(frame.columns) if columns is None else list(columns)
    types = FEATURE_TYPES if feature_types is None else feature_types
    n = len(frame)
    numerator = np.zeros((n, n), dtype=float)
    denominator = np.zeros((n, n), dtype=float)
    for column in columns:
        feature_type = types[column]
        if feature_type == "nominal":
            series = frame[column].astype("string")
            observed = series.notna().to_numpy()
            values = series.fillna("__MISSING__").to_numpy(dtype=str)
            difference = (values[:, None] != values[None, :]).astype(float)
        else:
            series = pd.to_numeric(frame[column], errors="coerce")
            observed = series.notna().to_numpy()
            values = series.fillna(0).to_numpy(dtype=float)
            difference = np.abs(values[:, None] - values[None, :])
            if feature_type == "continuous":
                valid = values[observed]
                observed_range = float(valid.max() - valid.min())
                difference = difference / observed_range if observed_range > 0 else np.zeros_like(difference)
        pair_observed = observed[:, None] & observed[None, :]
        numerator += np.where(pair_observed, difference, 0.0)
        denominator += pair_observed
    distance = np.divide(
        numerator, denominator,
        out=np.zeros_like(numerator), where=denominator > 0,
    )
    np.fill_diagonal(distance, 0.0)
    return distance, denominator


D, pair_feature_coverage = mixed_gower(features, CLUSTER_FEATURES)
assert np.allclose(D, D.T)
assert D.min() >= 0 and D.max() <= 1
assert pair_feature_coverage.min() >= 1
positive_distances = D[D > 0]
sigma = float(np.median(positive_distances))


def affinity(distance):
    result = np.exp(-(distance ** 2) / (2 * sigma ** 2))
    np.fill_diagonal(result, 1.0)
    return result


print("Gower distance median:", round(float(np.median(positive_distances)), 4))
print(
    "Pairwise observed features: min", int(pair_feature_coverage.min()),
    "median", int(np.median(pair_feature_coverage)),
    "max", int(pair_feature_coverage.max()),
)

# %% [markdown]
# ## 4. Compare K-medoids and spectral clustering for candidate `k`

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
                n_clusters=k, affinity="precomputed", assign_labels="kmeans",
                n_init=30, random_state=RANDOM_STATE + 2000 * k + repetition,
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
        n_clusters=k, affinity="precomputed", assign_labels="kmeans",
        n_init=100, random_state=RANDOM_STATE + 100 + k,
    ).fit_predict(affinity(D))
    full_source_solutions[("kmedoids", k)] = kmedoids["labels"]
    full_source_solutions[("spectral", k)] = spectral_labels
    method_values = {}
    for algorithm, labels_k in [
        ("kmedoids", kmedoids["labels"]), ("spectral", spectral_labels)
    ]:
        stability = subsample_stability(algorithm, k, labels_k)
        method_values[algorithm] = {
            "silhouette": silhouette_score(D, labels_k, metric="precomputed"),
            "stability": float(stability.mean()),
            "stability_p10": float(np.quantile(stability, 0.10)),
            "minimum_size": int(pd.Series(labels_k).value_counts().min()),
        }
        candidate_stability_rows.extend({
            "algorithm": algorithm, "k": k, "repetition": repetition + 1,
            "ari": value,
        } for repetition, value in enumerate(stability))
    candidate_rows.append({
        "k": k,
        "kmedoids_silhouette": method_values["kmedoids"]["silhouette"],
        "spectral_silhouette": method_values["spectral"]["silhouette"],
        "mean_source_silhouette": np.mean([
            method_values["kmedoids"]["silhouette"], method_values["spectral"]["silhouette"]
        ]),
        "kmedoids_stability_mean": method_values["kmedoids"]["stability"],
        "spectral_stability_mean": method_values["spectral"]["stability"],
        "mean_source_stability": np.mean([
            method_values["kmedoids"]["stability"], method_values["spectral"]["stability"]
        ]),
        "minimum_source_p10_stability": min(
            method_values["kmedoids"]["stability_p10"], method_values["spectral"]["stability_p10"]
        ),
        "source_algorithm_ari": adjusted_rand_score(kmedoids["labels"], spectral_labels),
        "minimum_cluster_size_across_sources": min(
            method_values["kmedoids"]["minimum_size"], method_values["spectral"]["minimum_size"]
        ),
    })

candidate_metrics = pd.DataFrame(candidate_rows)
candidate_stability = pd.DataFrame(candidate_stability_rows)
eligible = candidate_metrics.loc[
    candidate_metrics["minimum_cluster_size_across_sources"].ge(MIN_PROFILE_SIZE)
].copy()
if eligible.empty:
    display(candidate_metrics.round(4))
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
print("Selected global k:", selected_k)

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

raw_medoids = {}
for raw_cluster in sorted(np.unique(raw_labels)):
    members = np.flatnonzero(raw_labels == raw_cluster)
    within = consensus_distance[np.ix_(members, members)]
    raw_medoids[int(raw_cluster)] = members[np.argmin(within.sum(axis=1))]

# Order profile IDs from lower to higher median observed household income, with
# medoid respondent ID as deterministic tie-breaker. Names remain descriptive.
raw_order = sorted(
    raw_medoids,
    key=lambda cluster: (
        features.loc[raw_labels == cluster, "household_income"].median(),
        str(cohort.iloc[raw_medoids[cluster]]["respondent_id"]),
    ),
)
raw_to_profile = {raw: profile + 1 for profile, raw in enumerate(raw_order)}
profile_id = np.asarray([raw_to_profile[int(label)] for label in raw_labels])
profile_names = {
    1: "Exploratory lower-income/fewer-worker household pattern",
    2: "Exploratory higher-income/more-worker household pattern",
}
assert set(np.unique(profile_id)) == set(profile_names), "Update descriptive names if selected k changes."

print("Base partitions:", len(base_partition_diagnostics))
print(
    "Pair coverage: min", int(coverage.min()),
    "median", int(np.median(coverage)), "max", int(coverage.max()),
)

# %% [markdown]
# ## 6. Profile the global clusters and examine branch composition

# %%
assignments = cohort[[
    "respondent_id", "entry_branch", "branch", "branch_routing_source",
    "branch_integrity_issue",
]].copy()
for variable in SOURCE_VARIABLES:
    assignments[f"{variable}__value"] = cohort[f"{variable}__value"]
    assignments[f"{variable}__response"] = cohort[f"{variable}__response"]
assignments["global_economic_profile_id"] = profile_id
assignments["global_economic_profile_label"] = assignments[
    "global_economic_profile_id"
].map(profile_names)

gower_individual_silhouette = silhouette_samples(D, profile_id, metric="precomputed")
consensus_individual_silhouette = silhouette_samples(
    consensus_distance, profile_id, metric="precomputed"
)
assignments["gower_individual_silhouette"] = gower_individual_silhouette
assignments["consensus_individual_silhouette"] = consensus_individual_silhouette

profile_sizes = (
    assignments.groupby([
        "global_economic_profile_id", "global_economic_profile_label"
    ], as_index=False)
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
for variable in SOURCE_VARIABLES:
    response_col = f"{variable}__response"
    temp = (
        assignments.groupby(
            ["global_economic_profile_id", response_col], dropna=False
        ).size().rename("records").reset_index()
    )
    temp["within_profile_percent"] = (
        100 * temp["records"]
        / temp.groupby("global_economic_profile_id")["records"].transform("sum")
    )
    temp = temp.rename(columns={response_col: "response"})
    temp.insert(1, "variable", variable)
    response_rows.append(temp)
profile_response_distributions = pd.concat(response_rows, ignore_index=True)
profile_modes = (
    profile_response_distributions.sort_values(
        ["global_economic_profile_id", "variable", "within_profile_percent"],
        ascending=[True, True, False],
    ).groupby(["global_economic_profile_id", "variable"], as_index=False).first()
)

numeric_profile_source = pd.DataFrame({
    "household_income_order": features["household_income"],
    "household_size_reported": raw_valid_counts["household_size"],
    "household_workers_reported": raw_valid_counts["household_workers"],
    "household_unemployed_reported": raw_valid_counts["household_unemployed"],
    "primary_earner_responsibility": features["primary_earner_status"],
})
numeric_profile_medians = numeric_profile_source.assign(
    global_economic_profile_id=profile_id
).groupby("global_economic_profile_id").median()

branch_profile_counts = pd.crosstab(
    assignments["branch"], assignments["global_economic_profile_id"]
)
branch_profile_percent = 100 * branch_profile_counts.div(
    branch_profile_counts.sum(axis=1), axis=0
)

display(profile_sizes.round(3))
display(profile_modes.round(2))
display(numeric_profile_medians.round(3))
display(branch_profile_counts)
display(branch_profile_percent.round(1))

# %% [markdown]
# ## 7. Validate stability, ambiguity, and sensitivity

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
        "global_economic_profile_id": int(own),
        "within_profile_consensus": within,
        "strongest_other_profile_consensus": strongest_other,
        "consensus_margin": within - strongest_other,
        "ambiguous_consensus_membership": (
            (within < 0.70) or ((within - strongest_other) < 0.20)
        ),
    })
respondent_confidence = pd.DataFrame(confidence_rows)
assignments = assignments.merge(
    respondent_confidence.drop(columns="global_economic_profile_id"),
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

# Count-scaling sensitivity: restore raw count magnitudes and continuous Gower
# ranges, then refit K-medoids at the selected k.
raw_count_features = features.copy()
for column in ["household_size", "household_workers", "household_unemployed"]:
    raw_count_features[column] = raw_valid_counts[column]
raw_count_types = FEATURE_TYPES | {
    "household_size": "continuous",
    "household_workers": "continuous",
    "household_unemployed": "continuous",
}
D_raw_count, _ = mixed_gower(
    raw_count_features, CLUSTER_FEATURES, feature_types=raw_count_types
)
raw_count_fit = fit_kmedoids(
    D_raw_count, selected_k, n_init=500, random_state=RANDOM_STATE + 90000
)
raw_count_sensitivity_ari = float(
    adjusted_rand_score(profile_id, raw_count_fit["labels"])
)

feature_sensitivity_rows = []
for omitted in CLUSTER_FEATURES:
    retained = [feature for feature in CLUSTER_FEATURES if feature != omitted]
    D_reduced, coverage_reduced = mixed_gower(features, retained)
    reduced_fit = fit_kmedoids(
        D_reduced, selected_k, n_init=300,
        random_state=RANDOM_STATE + 91000 + CLUSTER_FEATURES.index(omitted),
    )
    reduced_labels = reduced_fit["labels"]
    reduced_unique = np.unique(reduced_labels).size
    feature_sensitivity_rows.append({
        "omitted_feature": omitted,
        "retained_features": len(retained),
        "minimum_pair_coverage": int(coverage_reduced.min()),
        "clusters_recovered": int(reduced_unique),
        "gower_silhouette_reduced_kmedoids": (
            float(silhouette_score(D_reduced, reduced_labels, metric="precomputed"))
            if 1 < reduced_unique < len(reduced_labels) else np.nan
        ),
        "ari_reduced_kmedoids_vs_final_consensus": float(
            adjusted_rand_score(profile_id, reduced_labels)
        ),
    })
feature_sensitivity = pd.DataFrame(feature_sensitivity_rows)

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
    "raw_count_sensitivity_ari": raw_count_sensitivity_ari,
    "minimum_profile_size": int(pd.Series(profile_id).value_counts().min()),
    "low_gower_confidence_percent": 100 * float(
        np.mean(gower_individual_silhouette < 0.10)
    ),
    "ambiguous_consensus_percent": 100 * float(
        assignments["ambiguous_consensus_membership"].mean()
    ),
    "pac_10_90": float(np.mean((upper > 0.10) & (upper < 0.90))),
}

quality_checks = pd.DataFrame([
    {"check": "original Gower silhouette >= 0.25", "value": metrics["gower_silhouette"], "passed": metrics["gower_silhouette"] >= 0.25},
    {"check": "ensemble bootstrap mean ARI >= 0.80", "value": metrics["ensemble_bootstrap_ari_mean"], "passed": metrics["ensemble_bootstrap_ari_mean"] >= 0.80},
    {"check": f"minimum profile size >= {MIN_PROFILE_SIZE}", "value": metrics["minimum_profile_size"], "passed": metrics["minimum_profile_size"] >= MIN_PROFILE_SIZE},
    {"check": "ARI with full K-medoids >= 0.60", "value": metrics["ari_vs_full_kmedoids"], "passed": metrics["ari_vs_full_kmedoids"] >= 0.60},
    {"check": "ARI with full spectral >= 0.60", "value": metrics["ari_vs_full_spectral"], "passed": metrics["ari_vs_full_spectral"] >= 0.60},
    {"check": "raw-count sensitivity ARI >= 0.60", "value": metrics["raw_count_sensitivity_ari"], "passed": metrics["raw_count_sensitivity_ari"] >= 0.60},
    {"check": "PAC (0.10, 0.90) <= 0.20", "value": metrics["pac_10_90"], "passed": metrics["pac_10_90"] <= 0.20},
    {"check": "ambiguous consensus respondents <= 20%", "value": metrics["ambiguous_consensus_percent"], "passed": metrics["ambiguous_consensus_percent"] <= 20},
    {"check": "low-confidence respondents in original Gower space <= 20%", "value": metrics["low_gower_confidence_percent"], "passed": metrics["low_gower_confidence_percent"] <= 20},
])

primary_pass = bool(quality_checks.iloc[:6]["passed"].all())
if primary_pass and quality_checks.iloc[6:]["passed"].all():
    status = "Stable, cross-method-supported global household-economic segmentation"
elif primary_pass:
    status = "Passes primary stability rules but retains ambiguity cautions"
else:
    status = "No sufficiently robust global household-economic segmentation found"

display(pd.Series(metrics, name="value").to_frame().round(3))
display(quality_checks.round(3))
display(feature_sensitivity.round(3))
print("Statistical result:", status)

# %% [markdown]
# ## 8. Visualise candidates, profiles, and branch distribution

# %%
fig, axes = plt.subplots(1, 2, figsize=(12, 4.5))
axes[0].plot(candidate_metrics["k"], candidate_metrics["mean_source_silhouette"], marker="o")
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
fig.savefig(OUT / "global_economic_candidate_diagnostics.png", dpi=180, bbox_inches="tight")
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
    ax.scatter(
        coordinates[mask, 0], coordinates[mask, 1], s=28, alpha=0.65,
        edgecolor="white", linewidth=0.4, label=profile_names[int(pid)],
    )
ax.set(
    title="Global household-economic response patterns in Gower space",
    xlabel="Classical MDS axis 1 (display coordinate only)",
    ylabel="Classical MDS axis 2 (display coordinate only)",
)
ax.legend()
fig.tight_layout()
fig.savefig(OUT / "global_economic_profile_scatterplot.png", dpi=180, bbox_inches="tight")
plt.show()

fig, ax = plt.subplots(figsize=(9, 5))
branch_profile_percent.plot(kind="bar", stacked=True, ax=ax, colormap="tab10")
ax.set(
    title="Global household-economic profiles within each final branch",
    xlabel="Final branch", ylabel="Percent within branch", ylim=(0, 100),
)
ax.legend(title="Global profile", bbox_to_anchor=(1.02, 1), loc="upper left")
fig.tight_layout()
fig.savefig(OUT / "global_economic_branch_distribution.png", dpi=180, bbox_inches="tight")
plt.show()

# %% [markdown]
# ## 9. Save reproducible outputs

# %%
variable_screening.to_csv(OUT / "global_economic_variable_screening.csv", index=False)
count_issue_audit.to_csv(OUT / "global_economic_household_count_issues.csv", index=False)
count_outlier_audit.to_csv(OUT / "global_economic_count_diagnostics.csv")
feature_audit.to_csv(OUT / "global_economic_feature_audit.csv", index=False)
count_rank_audit.to_csv(OUT / "global_economic_count_rank_audit.csv", index=False)
candidate_metrics.to_csv(OUT / "global_economic_candidate_metrics.csv", index=False)
candidate_stability.to_csv(OUT / "global_economic_candidate_subsample_stability.csv", index=False)
base_partition_diagnostics.to_csv(OUT / "global_economic_consensus_base_partitions.csv", index=False)
assignments.to_csv(OUT / "global_economic_consensus_assignments.csv", index=False)
profile_sizes.to_csv(OUT / "global_economic_profile_sizes.csv", index=False)
profile_response_distributions.to_csv(OUT / "global_economic_profile_response_distributions.csv", index=False)
profile_modes.to_csv(OUT / "global_economic_profile_modes.csv", index=False)
numeric_profile_medians.to_csv(OUT / "global_economic_profile_numeric_medians.csv")
branch_profile_counts.to_csv(OUT / "global_economic_branch_counts.csv")
branch_profile_percent.to_csv(OUT / "global_economic_branch_percent.csv")
respondent_confidence.to_csv(OUT / "global_economic_respondent_confidence.csv", index=False)
ensemble_stability.to_csv(OUT / "global_economic_consensus_ensemble_stability.csv", index=False)
feature_sensitivity.to_csv(OUT / "global_economic_leave_one_feature_out.csv", index=False)
quality_checks.to_csv(OUT / "global_economic_quality_checks.csv", index=False)

consensus_export = pd.DataFrame(consensus, columns=cohort["respondent_id"])
consensus_export.insert(0, "respondent_id", cohort["respondent_id"].to_numpy())
consensus_export.to_csv(OUT / "global_economic_consensus_matrix.csv", index=False)

summary = {
    "cohort": {
        "records": int(len(cohort)),
        "routing_source": "translated_final_active_branch",
        "branch_counts": {key: int(value) for key, value in branch_counts.items()},
        "branch_used_as_clustering_input": False,
    },
    "dimension": "global household economic resource structure",
    "source_variables": SOURCE_VARIABLES,
    "clustering_features": CLUSTER_FEATURES,
    "descriptors": DESCRIPTOR_VARIABLES,
    "data_quality": {
        **validation,
        "household_count_conflicts": int(len(count_issue_audit)),
        "income_prefer_not_to_say": int(income.eq(99).sum()),
    },
    "method": {
        "distance": "equal-maximum-weight, missing-aware mixed Gower on four original household-resource responses",
        "candidate_k": [2, 3, 4, 5],
        "selected_k": selected_k,
        "ensemble": "equal-weight K-medoids plus spectral consensus",
        "base_partitions": 2 * CONSENSUS_SUBSAMPLES,
        "final_method": "K-medoids on one minus co-association",
    },
    "profiles": {
        "sizes": {
            str(int(row.global_economic_profile_id)): int(row.records)
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
        "These are exploratory household-economic response profiles, not a validated economic-capital scale.",
        "Household income 'prefer not to say' is unavailable in pairwise distance rather than forced into the income ordering.",
        "Worker and unemployed counts are unavailable for 15 internally inconsistent households; original values remain in the audit.",
        "Two unusually large households are retained because the survey contains no evidence that they are impossible; ordered count positions are primary and raw-count sensitivity is reported.",
        "Household worker count asks about salary/wage workers and may not capture every form of household work.",
        "Primary income source is a descriptor because using it in distance mainly reproduced current activity/branch status in the initial screening run.",
        "Primary-earner status is a descriptor because using it in distance produced the direct no-versus-shared/yes questionnaire split rather than a multidimensional resource profile.",
        "K-medoids and spectral clustering disagree strongly on the four-feature solution; the displayed profiles are exploratory and must not be used as a validated global classification.",
        "Branch is used only after clustering for composition analysis and never determines global profile membership.",
    ],
}
with open(OUT / "global_economic_clustering_summary.json", "w", encoding="utf-8") as handle:
    json.dump(summary, handle, indent=2)

print(json.dumps(summary, indent=2))
print("\nSaved files:")
for path in sorted(OUT.iterdir()):
    print(" -", path.name)

# %% [markdown]
# ## Interpretation guardrails
#
# - These are household-economic response patterns, not fixed social classes.
# - Cluster membership does not imply personal merit, need, or programme eligibility.
# - Branch composition is descriptive; it does not show that branch status causes
#   household-economic position.
# - Profile names are assigned only after examining complete response distributions.
