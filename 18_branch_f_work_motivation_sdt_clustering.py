# %% [markdown]
# # Branch F — work motivation and psychological need experience
#
# This notebook clusters the 81 valid final-Branch-F employment records using
# four survey indicators corresponding to autonomy, competence, relatedness,
# and autonomous-to-controlled work motivation.

# %% [markdown]
# ## Theory and equation
#
# Self-Determination Theory distinguishes the psychological needs for autonomy,
# competence, and relatedness and distinguishes relatively autonomous from
# controlled motivation (Deci and Ryan, 2000). The four questionnaire items map
# directly to those constructs, but each remains a single item rather than a
# validated multi-item scale.
#
# No total motivation score is invented. Equal-maximum-weight Gower distance is:
#
# $$d(i,j)=\frac{1}{4}\sum_{h=1}^{4}\delta_{ijh}$$
#
# The three need-experience items retain their explicit positive-to-negative
# response order. Motivation type follows the questionnaire's SDT continuum from
# intrinsic/identified toward controlled/little-choice motivation. A nominal
# sensitivity analysis checks whether that ordering materially changes results.

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
OUT = ROOT / "outputs/branch_f_work_motivation_clusters"
OUT.mkdir(parents=True, exist_ok=True)

CLUSTER_FEATURES = [
    "work_autonomy", "competence_growth_at_work", "relatedness_at_work",
    "work_motivation_type",
]
FEATURE_TYPES = {
    "work_autonomy": "ordinal",
    "competence_growth_at_work": "ordinal",
    "relatedness_at_work": "ordinal",
    "work_motivation_type": "ordinal",
}
ORIGINAL_CLUSTER_VARIABLES = [
    "work_autonomy", "competence_growth_at_work", "relatedness_at_work",
    "work_motivation_type",
]
DESCRIPTOR_VARIABLES = [
    "job_satisfaction", "hopes_to_change_job", "job_security_12months",
    "received_training",
]
ALL_SOURCE_VARIABLES = ORIGINAL_CLUSTER_VARIABLES + DESCRIPTOR_VARIABLES

RANDOM_STATE = 20260824
MIN_PROFILE_SIZE = 15
CANDIDATE_SUBSAMPLES = 50
CONSENSUS_SUBSAMPLES = 100
SUBSAMPLE_FRACTION = 0.80
ENSEMBLE_BOOTSTRAPS = 100

# %% [markdown]
# ## 1. Rebuild and audit the strict valid employed cohort

# %%
values_all = pd.read_csv(VALUES_PATH)
labels_all = pd.read_csv(LABELS_PATH)
strict_mask = (
    values_all["branch"].eq("F")
    & values_all["branch_routing_source"].eq("translated_final_active_branch")
    & ~values_all["branch_integrity_issue"].astype(bool)
    & values_all["employment_status"].notna()
)
values = values_all.loc[strict_mask, [
    "respondent_id", "entry_branch", "branch", "branch_routing_source",
    "branch_path_disagreement", "branch_integrity_issue",
] + ALL_SOURCE_VARIABLES].copy()
labels = labels_all.loc[strict_mask, ["respondent_id"] + ALL_SOURCE_VARIABLES].copy()
labels = labels.rename(columns={v: f"{v}__response" for v in ALL_SOURCE_VARIABLES})
values = values.rename(columns={v: f"{v}__value" for v in ALL_SOURCE_VARIABLES})
cohort = values.merge(labels, on="respondent_id", validate="one_to_one")

validation = {
    "records": int(len(cohort)),
    "unique_ids": int(cohort["respondent_id"].nunique()),
    "wrong_branch": int(cohort["branch"].ne("F").sum()),
    "wrong_routing_source": int(
        cohort["branch_routing_source"].ne("translated_final_active_branch").sum()
    ),
    "path_disagreements_remaining": int(cohort["branch_path_disagreement"].sum()),
    "integrity_issues_remaining": int(cohort["branch_integrity_issue"].sum()),
}
assert validation == {
    "records": 81, "unique_ids": 81, "wrong_branch": 0,
    "wrong_routing_source": 0, "path_disagreements_remaining": 0,
    "integrity_issues_remaining": 0,
}
display(pd.Series(validation, name="value").to_frame())

# %% [markdown]
# ## 2. Screen variables and build original-response features

# %%
screening_rows = []
for variable in ALL_SOURCE_VARIABLES:
    response = cohort[f"{variable}__response"]
    counts = response.value_counts(dropna=False)
    screening_rows.append({
        "variable": variable,
        "role": "cluster_input" if variable in ORIGINAL_CLUSTER_VARIABLES else "profile_descriptor",
        "observed": int(response.notna().sum()),
        "missing": int(response.isna().sum()),
        "unique_observed_responses": int(response.nunique(dropna=True)),
        "dominant_response": str(counts.index[0]),
        "dominant_response_percent": 100 * float(counts.iloc[0] / len(response)),
    })
variable_screening = pd.DataFrame(screening_rows)

autonomy_code = pd.to_numeric(cohort["work_autonomy__value"], errors="coerce")
competence_code = pd.to_numeric(
    cohort["competence_growth_at_work__value"], errors="coerce"
)
relatedness_code = pd.to_numeric(
    cohort["relatedness_at_work__value"], errors="coerce"
)
motivation_code = pd.to_numeric(
    cohort["work_motivation_type__value"], errors="coerce"
)
features = pd.DataFrame(index=cohort.index)
four_level_map = {1: 0.0, 2: 1 / 3, 3: 2 / 3, 4: 1.0}
features["work_autonomy"] = autonomy_code.where(autonomy_code.between(1, 4)).map(four_level_map)
features["competence_growth_at_work"] = competence_code.where(competence_code.between(1, 4)).map(four_level_map)
features["relatedness_at_work"] = relatedness_code.where(relatedness_code.between(1, 4)).map(four_level_map)
features["work_motivation_type"] = motivation_code.where(
    motivation_code.between(1, 5)
).map({1: 0.0, 2: 0.25, 3: 0.50, 4: 0.75, 5: 1.0})

feature_audit = pd.DataFrame({
    "feature": CLUSTER_FEATURES,
    "type": [FEATURE_TYPES[v] for v in CLUSTER_FEATURES],
    "observed": [int(features[v].notna().sum()) for v in CLUSTER_FEATURES],
    "missing": [int(features[v].isna().sum()) for v in CLUSTER_FEATURES],
    "maximum_distance_weight": [1 / len(CLUSTER_FEATURES)] * len(CLUSTER_FEATURES),
})
assert features.notna().all().all()
display(variable_screening.round(2))
display(feature_audit)
display(pd.crosstab(
    cohort["work_autonomy__response"],
    cohort["work_motivation_type__response"],
    dropna=False,
))


def mixed_gower(frame, columns=None):
    columns = list(frame.columns) if columns is None else list(columns)
    n = len(frame)
    numerator = np.zeros((n, n), dtype=float)
    denominator = np.zeros((n, n), dtype=float)
    for column in columns:
        feature_type = FEATURE_TYPES[column]
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
                difference = difference / observed_range if observed_range else np.zeros_like(difference)
        pair_observed = observed[:, None] & observed[None, :]
        numerator += np.where(pair_observed, difference, 0.0)
        denominator += pair_observed
    distance = np.divide(
        numerator, denominator, out=np.zeros_like(numerator), where=denominator > 0
    )
    np.fill_diagonal(distance, 0.0)
    return distance, denominator


D, pair_coverage = mixed_gower(features)
assert np.allclose(D, D.T) and D.min() >= 0 and D.max() <= 1
positive_distances = D[D > 0]
sigma = float(np.median(positive_distances))


def affinity(distance):
    result = np.exp(-(distance ** 2) / (2 * sigma ** 2))
    np.fill_diagonal(result, 1.0)
    return result


print("Gower distance median:", round(float(np.median(positive_distances)), 4))

# %% [markdown]
# ## 3. Compare candidate profile counts and algorithms

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
    sample_size = int(np.floor(SUBSAMPLE_FRACTION * len(D)))
    scores = []
    for repetition in range(CANDIDATE_SUBSAMPLES):
        idx = np.sort(rng.choice(len(D), size=sample_size, replace=False))
        D_sub = D[np.ix_(idx, idx)]
        if algorithm == "kmedoids":
            result = fit_kmedoids(D_sub, k, n_init=50, random_state=RANDOM_STATE + 1000 * k + repetition)
            medoids = idx[result["medoids"]]
        else:
            labels_sub = SpectralClustering(
                n_clusters=k, affinity="precomputed", assign_labels="kmeans",
                n_init=30, random_state=RANDOM_STATE + 2000 * k + repetition,
            ).fit_predict(affinity(D_sub))
            medoids = idx[medoids_from_labels(D_sub, labels_sub)]
        scores.append(adjusted_rand_score(reference_labels, np.argmin(D[:, medoids], axis=1)))
    return np.asarray(scores)


candidate_rows = []
candidate_stability_rows = []
full_source_solutions = {}
for k in range(2, 5):
    km = fit_kmedoids(D, k, n_init=400, random_state=RANDOM_STATE + k)
    sp = SpectralClustering(
        n_clusters=k, affinity="precomputed", assign_labels="kmeans",
        n_init=100, random_state=RANDOM_STATE + 100 + k,
    ).fit_predict(affinity(D))
    full_source_solutions[("kmedoids", k)] = km["labels"]
    full_source_solutions[("spectral", k)] = sp
    results = {}
    for algorithm, labels_k in [("kmedoids", km["labels"]), ("spectral", sp)]:
        stability = subsample_stability(algorithm, k, labels_k)
        results[algorithm] = {
            "silhouette": silhouette_score(D, labels_k, metric="precomputed"),
            "stability": float(stability.mean()),
            "p10": float(np.quantile(stability, 0.10)),
            "minimum_size": int(pd.Series(labels_k).value_counts().min()),
        }
        candidate_stability_rows.extend({
            "algorithm": algorithm, "k": k, "repetition": i + 1, "ari": score,
        } for i, score in enumerate(stability))
    candidate_rows.append({
        "k": k,
        "kmedoids_silhouette": results["kmedoids"]["silhouette"],
        "spectral_silhouette": results["spectral"]["silhouette"],
        "mean_source_silhouette": np.mean([results["kmedoids"]["silhouette"], results["spectral"]["silhouette"]]),
        "kmedoids_stability_mean": results["kmedoids"]["stability"],
        "spectral_stability_mean": results["spectral"]["stability"],
        "mean_source_stability": np.mean([results["kmedoids"]["stability"], results["spectral"]["stability"]]),
        "minimum_source_p10_stability": min(results["kmedoids"]["p10"], results["spectral"]["p10"]),
        "source_algorithm_ari": adjusted_rand_score(km["labels"], sp),
        "minimum_cluster_size_across_sources": min(results["kmedoids"]["minimum_size"], results["spectral"]["minimum_size"]),
    })

candidate_metrics = pd.DataFrame(candidate_rows)
candidate_stability = pd.DataFrame(candidate_stability_rows)

# PAC is used comparatively across candidate k values, not against an arbitrary
# universal cutoff. Each candidate uses the same number of 80% subsamples and
# the same two algorithms.
def candidate_consensus_pac(k):
    rng = np.random.default_rng(RANDOM_STATE + 25000 + k)
    n_local = len(D)
    sample_size_local = int(np.floor(SUBSAMPLE_FRACTION * n_local))
    cover_total = np.zeros((n_local, n_local), dtype=np.uint16)
    same_total = np.zeros((n_local, n_local), dtype=np.uint16)
    for repetition in range(CANDIDATE_SUBSAMPLES):
        idx = np.sort(rng.choice(n_local, size=sample_size_local, replace=False))
        D_sub = D[np.ix_(idx, idx)]
        cover = np.zeros((n_local, n_local), dtype=np.uint8)
        cover[np.ix_(idx, idx)] = 1
        km_labels = fit_kmedoids(
            D_sub, k, n_init=80,
            random_state=RANDOM_STATE + 26000 + 1000 * k + repetition,
        )["labels"]
        sp_labels = SpectralClustering(
            n_clusters=k, affinity="precomputed", assign_labels="kmeans",
            n_init=30,
            random_state=RANDOM_STATE + 27000 + 1000 * k + repetition,
        ).fit_predict(affinity(D_sub))
        for labels_sub in (km_labels, sp_labels):
            same = np.zeros((n_local, n_local), dtype=np.uint8)
            same[np.ix_(idx, idx)] = (
                labels_sub[:, None] == labels_sub[None, :]
            ).astype(np.uint8)
            cover_total += cover
            same_total += same
    consensus_k = np.divide(
        same_total, cover_total,
        out=np.zeros_like(same_total, dtype=float), where=cover_total > 0,
    )
    upper_k = consensus_k[np.triu_indices(n_local, 1)]
    return float(np.mean((upper_k > 0.10) & (upper_k < 0.90)))

candidate_metrics["pac_10_90"] = [
    candidate_consensus_pac(int(k)) for k in candidate_metrics["k"]
]
candidate_metrics["pac_rank_all_candidates"] = candidate_metrics[
    "pac_10_90"
].rank(ascending=True, method="min")
eligible = candidate_metrics.loc[
    candidate_metrics["minimum_cluster_size_across_sources"].ge(MIN_PROFILE_SIZE)
].copy()
candidate_size_eligible = not eligible.empty
ranking_pool = eligible.copy() if candidate_size_eligible else candidate_metrics.copy()
ranking_pool["rank_silhouette"] = ranking_pool["mean_source_silhouette"].rank(ascending=False, method="min")
ranking_pool["rank_stability"] = ranking_pool["mean_source_stability"].rank(ascending=False, method="min")
ranking_pool["rank_pac"] = ranking_pool["pac_10_90"].rank(ascending=True, method="min")
ranking_pool["primary_mean_rank"] = ranking_pool[[
    "rank_silhouette", "rank_stability", "rank_pac"
]].mean(axis=1)
best_rank = ranking_pool["primary_mean_rank"].min()
selected_k = int(ranking_pool.loc[
    ranking_pool["primary_mean_rank"].eq(best_rank)
].sort_values("k").iloc[0]["k"])
candidate_metrics = candidate_metrics.merge(
    ranking_pool[["k", "primary_mean_rank"]], on="k", how="left"
)
candidate_metrics["selected"] = candidate_metrics["k"].eq(selected_k)
display(candidate_metrics.round(4))
if candidate_size_eligible:
    print("Selected k:", selected_k)
else:
    print("No candidate met the minimum-size rule; k=", selected_k, "is fitted for rejection diagnostics only.")

# %% [markdown]
# ## 4. Build and profile the consensus solution

# %%
rng = np.random.default_rng(RANDOM_STATE + 30000)
n = len(D)
sample_size = int(np.floor(SUBSAMPLE_FRACTION * n))
cover_matrices, same_matrices, base_rows = [], [], []
for repetition in range(CONSENSUS_SUBSAMPLES):
    idx = np.sort(rng.choice(n, size=sample_size, replace=False))
    D_sub = D[np.ix_(idx, idx)]
    cover = np.zeros((n, n), dtype=np.uint8)
    cover[np.ix_(idx, idx)] = 1
    km = fit_kmedoids(D_sub, selected_k, n_init=100, random_state=RANDOM_STATE + 40000 + repetition)["labels"]
    sp = SpectralClustering(
        n_clusters=selected_k, affinity="precomputed", assign_labels="kmeans",
        n_init=30, random_state=RANDOM_STATE + 50000 + repetition,
    ).fit_predict(affinity(D_sub))
    for algorithm, labels_sub in [("kmedoids", km), ("spectral", sp)]:
        same = np.zeros((n, n), dtype=np.uint8)
        same[np.ix_(idx, idx)] = (labels_sub[:, None] == labels_sub[None, :]).astype(np.uint8)
        cover_matrices.append(cover.copy())
        same_matrices.append(same)
        base_rows.append({
            "partition_id": len(base_rows) + 1, "algorithm": algorithm,
            "repetition": repetition + 1,
            "silhouette_in_subsample": silhouette_score(D_sub, labels_sub, metric="precomputed"),
            "minimum_cluster_size": int(pd.Series(labels_sub).value_counts().min()),
        })

cover_stack = np.stack(cover_matrices)
same_stack = np.stack(same_matrices)
coverage = cover_stack.sum(axis=0)
consensus = same_stack.sum(axis=0) / coverage
np.fill_diagonal(consensus, 1.0)
consensus_distance = 1 - consensus
np.fill_diagonal(consensus_distance, 0.0)
base_partition_diagnostics = pd.DataFrame(base_rows)
final_fit = fit_kmedoids(consensus_distance, selected_k, n_init=500, random_state=RANDOM_STATE + 60000)
raw_labels = final_fit["labels"]

raw_medoids = {}
for raw in sorted(np.unique(raw_labels)):
    members = np.flatnonzero(raw_labels == raw)
    within = consensus_distance[np.ix_(members, members)]
    raw_medoids[int(raw)] = members[np.argmin(within.sum(axis=1))]
# Give profile IDs a reproducible substantive order: stronger need satisfaction
# and more autonomous motivation first. This changes names only; it does not
# affect clustering.
raw_order = sorted(raw_medoids, key=lambda raw: (
    features.loc[raw_labels == raw, "work_autonomy"].median(),
    features.loc[raw_labels == raw, "competence_growth_at_work"].median(),
    features.loc[raw_labels == raw, "relatedness_at_work"].median(),
    features.loc[raw_labels == raw, "work_motivation_type"].median(),
))
raw_to_profile = {raw: i + 1 for i, raw in enumerate(raw_order)}
profile_id = np.asarray([raw_to_profile[int(raw)] for raw in raw_labels])
profile_names = {
    profile: f"Rejected diagnostic profile {profile}"
    for profile in sorted(np.unique(profile_id))
}

assignments = cohort[["respondent_id", "entry_branch", "branch", "branch_routing_source"]].copy()
for variable in ALL_SOURCE_VARIABLES:
    assignments[f"{variable}__value"] = cohort[f"{variable}__value"]
    assignments[f"{variable}__response"] = cohort[f"{variable}__response"]
assignments["work_motivation_profile_id"] = profile_id
assignments["work_motivation_profile_label"] = assignments["work_motivation_profile_id"].map(profile_names)
gower_sil = silhouette_samples(D, profile_id, metric="precomputed")
consensus_sil = silhouette_samples(consensus_distance, profile_id, metric="precomputed")
assignments["gower_individual_silhouette"] = gower_sil
assignments["consensus_individual_silhouette"] = consensus_sil

profile_sizes = assignments.groupby([
    "work_motivation_profile_id", "work_motivation_profile_label"
], as_index=False).agg(
    records=("respondent_id", "size"),
    low_gower_confidence_records=("gower_individual_silhouette", lambda x: int((x < 0.10).sum())),
    mean_gower_silhouette=("gower_individual_silhouette", "mean"),
    mean_consensus_silhouette=("consensus_individual_silhouette", "mean"),
)
profile_sizes["percent"] = 100 * profile_sizes["records"] / len(assignments)

response_rows = []
for variable in ALL_SOURCE_VARIABLES:
    col = f"{variable}__response"
    temp = assignments.groupby(["work_motivation_profile_id", col], dropna=False).size().rename("records").reset_index()
    temp["within_profile_percent"] = 100 * temp["records"] / temp.groupby("work_motivation_profile_id")["records"].transform("sum")
    temp = temp.rename(columns={col: "response"})
    temp.insert(1, "variable", variable)
    response_rows.append(temp)
profile_response_distributions = pd.concat(response_rows, ignore_index=True)
profile_modes = profile_response_distributions.sort_values(
    ["work_motivation_profile_id", "variable", "within_profile_percent"],
    ascending=[True, True, False],
).groupby(["work_motivation_profile_id", "variable"], as_index=False, dropna=False).head(1)
profile_numeric_medians = pd.DataFrame({
    "work_motivation_profile_id": profile_id,
    "autonomy_code": autonomy_code,
    "competence_code": competence_code,
    "relatedness_code": relatedness_code,
    "motivation_type_code": motivation_code,
    "received_training": cohort["received_training__response"].eq("Yes").astype(int),
    "wants_to_change_job": cohort["hopes_to_change_job__response"].eq(
        "Yes — I want to change"
    ).astype(int),
}).groupby("work_motivation_profile_id").agg(
    median_autonomy_code=("autonomy_code", "median"),
    median_competence_code=("competence_code", "median"),
    median_relatedness_code=("relatedness_code", "median"),
    median_motivation_type_code=("motivation_type_code", "median"),
    percent_received_training=("received_training", lambda x: 100 * x.mean()),
    percent_wants_to_change_job=("wants_to_change_job", lambda x: 100 * x.mean()),
)
display(profile_sizes.round(3))
display(profile_modes.round(2))
display(profile_numeric_medians)

# %% [markdown]
# ## 5. Validation and sensitivity

# %%
confidence_rows = []
for i in range(n):
    own = profile_id[i]
    own_members = np.flatnonzero(profile_id == own)
    own_members = own_members[own_members != i]
    within = float(consensus[i, own_members].mean()) if len(own_members) else 1.0
    other = max(float(consensus[i, np.flatnonzero(profile_id == p)].mean()) for p in set(profile_id) - {own})
    confidence_rows.append({
        "respondent_id": cohort.iloc[i]["respondent_id"],
        "work_motivation_profile_id": int(own),
        "within_profile_consensus": within,
        "strongest_other_profile_consensus": other,
        "consensus_margin": within - other,
        "ambiguous_consensus_membership": (within < 0.70) or ((within - other) < 0.20),
    })
respondent_confidence = pd.DataFrame(confidence_rows)
assignments = assignments.merge(respondent_confidence.drop(columns="work_motivation_profile_id"), on="respondent_id", validate="one_to_one")

bootstrap_rng = np.random.default_rng(RANDOM_STATE + 70000)
bootstrap_rows = []
for repetition in range(ENSEMBLE_BOOTSTRAPS):
    selected = bootstrap_rng.choice(len(cover_stack), size=len(cover_stack), replace=True)
    boot_cover = cover_stack[selected].sum(axis=0)
    boot_same = same_stack[selected].sum(axis=0)
    boot_consensus = np.divide(boot_same, boot_cover, out=np.zeros_like(boot_same, dtype=float), where=boot_cover > 0)
    np.fill_diagonal(boot_consensus, 1.0)
    boot_distance = 1 - boot_consensus
    np.fill_diagonal(boot_distance, 0.0)
    boot_labels = fit_kmedoids(boot_distance, selected_k, n_init=80, random_state=RANDOM_STATE + 80000 + repetition)["labels"]
    bootstrap_rows.append({"repetition": repetition + 1, "ari_vs_full_consensus": adjusted_rand_score(profile_id, boot_labels)})
ensemble_stability = pd.DataFrame(bootstrap_rows)

full_km = full_source_solutions[("kmedoids", selected_k)]
full_sp = full_source_solutions[("spectral", selected_k)]
hac_average = AgglomerativeClustering(n_clusters=selected_k, metric="precomputed", linkage="average").fit_predict(consensus_distance)
hac_complete = AgglomerativeClustering(n_clusters=selected_k, metric="precomputed", linkage="complete").fit_predict(consensus_distance)

sensitivity_rows = []
for omitted in CLUSTER_FEATURES:
    retained = [v for v in CLUSTER_FEATURES if v != omitted]
    complete_for_retained = features[retained].notna().all(axis=1).to_numpy()
    reduced_frame = features.loc[complete_for_retained].reset_index(drop=True)
    D_reduced, reduced_coverage = mixed_gower(reduced_frame, retained)
    reduced = fit_kmedoids(D_reduced, selected_k, n_init=400, random_state=RANDOM_STATE + 90000 + CLUSTER_FEATURES.index(omitted))["labels"]
    sensitivity_rows.append({
        "omitted_feature": omitted, "retained_features": len(retained),
        "respondents_compared": int(complete_for_retained.sum()),
        "minimum_pair_coverage": int(reduced_coverage.min()),
        "gower_silhouette_reduced_kmedoids": silhouette_score(D_reduced, reduced, metric="precomputed"),
        "ari_reduced_kmedoids_vs_final_consensus": adjusted_rand_score(
            profile_id[complete_for_retained], reduced
        ),
    })
feature_sensitivity = pd.DataFrame(sensitivity_rows)

# Test the only contestable scale decision: treat motivation type as five
# unrelated categories rather than as the SDT continuum used above.
motivation_ordinal_type = FEATURE_TYPES["work_motivation_type"]
FEATURE_TYPES["work_motivation_type"] = "nominal"
nominal_motivation_features = features.copy()
nominal_motivation_features["work_motivation_type"] = cohort[
    "work_motivation_type__response"
].astype("string")
D_nominal_motivation, _ = mixed_gower(nominal_motivation_features)
nominal_motivation_labels = fit_kmedoids(
    D_nominal_motivation, selected_k, n_init=400,
    random_state=RANDOM_STATE + 95000,
)["labels"]
FEATURE_TYPES["work_motivation_type"] = motivation_ordinal_type
encoding_sensitivity = pd.DataFrame([{
    "alternative_encoding": "work_motivation_type treated as nominal",
    "gower_silhouette": silhouette_score(
        D_nominal_motivation, nominal_motivation_labels, metric="precomputed"
    ),
    "ari_vs_final_consensus": adjusted_rand_score(
        profile_id, nominal_motivation_labels
    ),
}])

upper = consensus[np.triu_indices(n, 1)]
metrics = {
    "gower_silhouette": float(silhouette_score(D, profile_id, metric="precomputed")),
    "consensus_distance_silhouette": float(silhouette_score(consensus_distance, profile_id, metric="precomputed")),
    "ensemble_bootstrap_ari_mean": float(ensemble_stability["ari_vs_full_consensus"].mean()),
    "ensemble_bootstrap_ari_p10": float(ensemble_stability["ari_vs_full_consensus"].quantile(0.10)),
    "ari_vs_full_kmedoids": float(adjusted_rand_score(profile_id, full_km)),
    "ari_vs_full_spectral": float(adjusted_rand_score(profile_id, full_sp)),
    "ari_vs_hac_average": float(adjusted_rand_score(profile_id, hac_average)),
    "ari_vs_hac_complete": float(adjusted_rand_score(profile_id, hac_complete)),
    "minimum_profile_size": int(pd.Series(profile_id).value_counts().min()),
    "low_gower_confidence_percent": 100 * float(np.mean(gower_sil < 0.10)),
    "ambiguous_consensus_percent": 100 * float(assignments["ambiguous_consensus_membership"].mean()),
    "pac_10_90": float(np.mean((upper > 0.10) & (upper < 0.90))),
    "candidate_pac_rank_all": float(candidate_metrics.loc[
        candidate_metrics["k"].eq(selected_k), "pac_rank_all_candidates"
    ].iloc[0]),
    "ari_nominal_motivation_encoding": float(
        adjusted_rand_score(profile_id, nominal_motivation_labels)
    ),
}
quality_checks = pd.DataFrame([
    {"check": "original Gower silhouette >= 0.25", "value": metrics["gower_silhouette"], "passed": metrics["gower_silhouette"] >= 0.25},
    {"check": "ensemble bootstrap mean ARI >= 0.80", "value": metrics["ensemble_bootstrap_ari_mean"], "passed": metrics["ensemble_bootstrap_ari_mean"] >= 0.80},
    {"check": f"minimum profile size >= {MIN_PROFILE_SIZE}", "value": metrics["minimum_profile_size"], "passed": metrics["minimum_profile_size"] >= MIN_PROFILE_SIZE},
    {"check": f"minimum source-algorithm profile size >= {MIN_PROFILE_SIZE}", "value": float(candidate_metrics.loc[candidate_metrics["k"].eq(selected_k), "minimum_cluster_size_across_sources"].iloc[0]), "passed": candidate_size_eligible},
    {"check": "ARI with full K-medoids >= 0.60", "value": metrics["ari_vs_full_kmedoids"], "passed": metrics["ari_vs_full_kmedoids"] >= 0.60},
    {"check": "ARI with full spectral >= 0.60", "value": metrics["ari_vs_full_spectral"], "passed": metrics["ari_vs_full_spectral"] >= 0.60},
    {"check": "ambiguous respondents <= 20% (analyst caution rule)", "value": metrics["ambiguous_consensus_percent"], "passed": metrics["ambiguous_consensus_percent"] <= 20},
    {"check": "low-confidence respondents <= 20% (analyst caution rule)", "value": metrics["low_gower_confidence_percent"], "passed": metrics["low_gower_confidence_percent"] <= 20},
])
primary_pass = bool(quality_checks.iloc[:6]["passed"].all())
if primary_pass and quality_checks.iloc[6:]["passed"].all():
    status = "Stable, cross-method-supported work-motivation/psychological-needs segmentation"
elif primary_pass:
    status = "Cross-method-supported with respondent-level ambiguity caution"
else:
    status = "No sufficiently robust work-motivation/psychological-needs segmentation found"
display(pd.Series(metrics, name="value").to_frame().round(3))
display(quality_checks.round(3))
display(feature_sensitivity.round(3))
display(encoding_sensitivity.round(3))
display(candidate_metrics[["k", "pac_10_90", "pac_rank_all_candidates", "selected"]].round(3))
print("Statistical result:", status)

# %% [markdown]
# ## 6. Visualise and save outputs

# %%
fig, axes = plt.subplots(1, 2, figsize=(12, 4.5))
axes[0].plot(candidate_metrics["k"], candidate_metrics["mean_source_silhouette"], marker="o")
axes[0].axvline(selected_k, color="tab:red", linestyle="--", label=f"selected k={selected_k}")
axes[0].axhline(0.25, color="grey", linestyle=":")
axes[0].set(title="Candidate separation", xlabel="Profiles", ylabel="Mean Gower silhouette")
axes[0].legend()
axes[1].plot(candidate_metrics["k"], candidate_metrics["mean_source_stability"], marker="o", label="mean stability")
axes[1].plot(candidate_metrics["k"], candidate_metrics["source_algorithm_ari"], marker="s", label="algorithm agreement")
axes[1].axvline(selected_k, color="tab:red", linestyle="--")
axes[1].set(title="Stability and agreement", xlabel="Profiles", ylabel="ARI", ylim=(-0.05, 1.05))
axes[1].legend()
fig.tight_layout()
fig.savefig(OUT / "work_motivation_candidate_diagnostics.png", dpi=180, bbox_inches="tight")
plt.show()

J = np.eye(n) - np.ones((n, n)) / n
B = -0.5 * J @ (D ** 2) @ J
eigenvalues, eigenvectors = np.linalg.eigh(B)
order = np.argsort(eigenvalues)[::-1]
positive = order[eigenvalues[order] > 0][:2]
coordinates = eigenvectors[:, positive] * np.sqrt(eigenvalues[positive])
# Respondents with identical categorical response patterns have identical MDS
# coordinates. A small deterministic display-only jitter makes all records
# visible without changing clustering, distances, or validation.
plot_rng = np.random.default_rng(RANDOM_STATE + 99000)
plot_coordinates = coordinates + plot_rng.normal(0, 0.012, size=coordinates.shape)
fig, ax = plt.subplots(figsize=(8, 6))
for pid in sorted(np.unique(profile_id)):
    mask = profile_id == pid
    ax.scatter(plot_coordinates[mask, 0], plot_coordinates[mask, 1], s=42, alpha=0.7, edgecolor="white", linewidth=0.5, label=profile_names[int(pid)])
ax.set(title="Rejected diagnostic: Branch F work motivation and psychological needs", xlabel="Classical MDS axis 1 (jittered for display only)", ylabel="Classical MDS axis 2 (jittered for display only)")
ax.legend()
fig.text(0.5, 0.01, "Small jitter separates respondents with identical answer patterns; clustering uses the original Gower distances.", ha="center", fontsize=8)
fig.tight_layout()
fig.savefig(OUT / "work_motivation_profile_scatterplot.png", dpi=180, bbox_inches="tight")
plt.show()

variable_screening.to_csv(OUT / "work_motivation_variable_screening.csv", index=False)
feature_audit.to_csv(OUT / "work_motivation_feature_audit.csv", index=False)
candidate_metrics.to_csv(OUT / "work_motivation_candidate_metrics.csv", index=False)
candidate_stability.to_csv(OUT / "work_motivation_candidate_subsample_stability.csv", index=False)
base_partition_diagnostics.to_csv(OUT / "work_motivation_consensus_base_partitions.csv", index=False)
assignments.to_csv(OUT / "work_motivation_consensus_assignments.csv", index=False)
profile_sizes.to_csv(OUT / "work_motivation_profile_sizes.csv", index=False)
profile_response_distributions.to_csv(OUT / "work_motivation_profile_response_distributions.csv", index=False)
profile_modes.to_csv(OUT / "work_motivation_profile_modes.csv", index=False)
profile_numeric_medians.to_csv(OUT / "work_motivation_profile_numeric_medians.csv")
respondent_confidence.to_csv(OUT / "work_motivation_respondent_confidence.csv", index=False)
ensemble_stability.to_csv(OUT / "work_motivation_consensus_ensemble_stability.csv", index=False)
feature_sensitivity.to_csv(OUT / "work_motivation_leave_one_feature_out.csv", index=False)
encoding_sensitivity.to_csv(OUT / "work_motivation_encoding_sensitivity.csv", index=False)
quality_checks.to_csv(OUT / "work_motivation_quality_checks.csv", index=False)

summary = {
    "cohort": {"records": 81, "branch": "F", "strict_final_branch_records": 82, "excluded_routing_integrity_records": 1},
    "dimension": "work motivation and psychological need experience",
    "clustering_features": CLUSTER_FEATURES,
    "descriptors": DESCRIPTOR_VARIABLES,
    "method": {"distance": "equal-weight mixed Gower on four questionnaire indicators", "selected_k": selected_k, "ensemble": "K-medoids plus spectral consensus", "base_partitions": 200},
    "profiles": {"sizes": {str(int(r.work_motivation_profile_id)): int(r.records) for r in profile_sizes.itertuples()}, "names": {str(k): v for k, v in profile_names.items()}},
    "metrics": metrics,
    "decision": {"retained_for_clustering": False, "diagnostic_partition_only": True, "primary_checks_passed": primary_pass, "checks_passed": int(quality_checks["passed"].sum()), "checks_total": int(len(quality_checks)), "status": status},
    "limitations": [
        "These are exploratory work-motivation/psychological-needs response profiles, not validated SDT subscales.",
        "Each SDT construct is represented by one survey item, so no reliability coefficient or total SDT score is claimed.",
        "The motivation-type continuum is theoretically ordered; a nominal-encoding sensitivity result is reported separately.",
        "High need-experience responses are strongly dominant in this sample, which can leave small contrasting groups.",
        "No k=2 to k=4 candidate met the minimum-profile-size rule across both source algorithms.",
        "For diagnostic k=3, K-medoids and spectral agreement was ARI 0.330, below the cross-method requirement.",
        "Treating motivation type as nominal produced only ARI 0.248 agreement with the ordinal-continuum result, so the apparent profiles are encoding-sensitive.",
        "PAC is reported comparatively across k=2 to k=4; no universal absolute PAC pass/fail cutoff is imposed.",
        "The one routing-corrupted final-Branch-F record is excluded from this employment analysis.",
    ],
}
with open(OUT / "work_motivation_clustering_summary.json", "w", encoding="utf-8") as handle:
    json.dump(summary, handle, indent=2)
print(json.dumps(summary, indent=2))

# %% [markdown]
# ## Interpretation guardrails
#
# - These profiles describe response patterns across four single-item SDT
#   indicators; they are not validated psychological diagnoses or scales.
# - Controlled motivation must not automatically be labelled poor performance.
# - They do not measure personal worth, productivity, or programme eligibility.
# - Profile names are descriptive and assigned only after examining distributions.
