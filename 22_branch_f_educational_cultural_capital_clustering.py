# %% [markdown]
# # Branch F — educational and inherited cultural capital
#
# Dedicated validation of D2 on the 81 valid final-Branch-F respondents.
# The four theory-selected original responses are compared with equal-weight,
# missing-aware Gower distance. No cultural-capital score is constructed.
#
# A consensus profile is created only if at least one k=2–4 candidate contains
# at least 15 respondents in every cluster under both K-medoids and spectral
# clustering. Otherwise, the diagnostic partitions are saved but rejected.

from pathlib import Path
import json
import warnings

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.cluster import SpectralClustering
from sklearn.metrics import adjusted_rand_score, silhouette_score

warnings.filterwarnings("ignore", category=FutureWarning)
pd.set_option("display.max_columns", 100)
pd.set_option("display.width", 220)

ROOT = Path.cwd()
VALUES_PATH = ROOT / "outputs/nysc_survey_cleaned_values.csv"
LABELS_PATH = ROOT / "outputs/nysc_survey_cleaned_labels.csv"
OUT = ROOT / "outputs/branch_f_educational_cultural_capital_clusters"
OUT.mkdir(parents=True, exist_ok=True)

SOURCE_VARIABLES = [
    "father_edu", "mother_edu", "edu_status", "worked_while_studying",
]
FEATURE_TYPES = {
    "father_edu": "ordinal",
    "mother_edu": "ordinal",
    "edu_status": "nominal",
    "worked_while_studying": "binary",
}
RANDOM_STATE = 20260825
MIN_PROFILE_SIZE = 15
SUBSAMPLE_REPETITIONS = 100
SUBSAMPLE_FRACTION = 0.80
PERMUTATION_REPETITIONS = 100


# %% [markdown]
# ## 1. Strict cohort and original-response features

values_all = pd.read_csv(VALUES_PATH)
labels_all = pd.read_csv(LABELS_PATH)
strict_mask = (
    values_all["branch"].eq("F")
    & values_all["branch_routing_source"].eq("translated_final_active_branch")
    & ~values_all["branch_integrity_issue"].astype(bool)
    & values_all["employment_status"].notna()
)
admin_columns = [
    "respondent_id", "entry_branch", "branch", "branch_routing_source",
    "branch_path_disagreement", "branch_integrity_issue", "employment_status",
]
values = values_all.loc[strict_mask, admin_columns + SOURCE_VARIABLES].copy()
labels = labels_all.loc[strict_mask, ["respondent_id"] + SOURCE_VARIABLES].copy()
values = values.rename(columns={v: f"{v}__value" for v in SOURCE_VARIABLES})
labels = labels.rename(columns={v: f"{v}__response" for v in SOURCE_VARIABLES})
cohort = values.merge(labels, on="respondent_id", validate="one_to_one")
assert len(cohort) == 81 and cohort["respondent_id"].nunique() == 81

features = pd.DataFrame(index=cohort.index)
for variable in ["father_edu", "mother_edu"]:
    numeric = pd.to_numeric(cohort[f"{variable}__value"], errors="coerce")
    # Codes 0–7 preserve the questionnaire order. Code 99 means unknown/refusal.
    features[variable] = numeric.where(numeric.between(0, 7)) / 7.0
features["edu_status"] = cohort["edu_status__value"].astype("string")
features["worked_while_studying"] = cohort[
    "worked_while_studying__value"
].map({"no": 0.0, "yes": 1.0})

screening_rows = []
for variable in SOURCE_VARIABLES:
    response = cohort[f"{variable}__response"]
    counts = response.value_counts(dropna=False)
    screening_rows.append({
        "variable": variable,
        "type": FEATURE_TYPES[variable],
        "observed_for_distance": int(features[variable].notna().sum()),
        "missing_for_distance": int(features[variable].isna().sum()),
        "unique_observed_responses": int(response.nunique(dropna=True)),
        "dominant_response": str(counts.index[0]),
        "dominant_response_percent": 100 * float(counts.iloc[0] / len(response)),
    })
variable_screening = pd.DataFrame(screening_rows)
assert features.notna().sum(axis=1).min() >= 2


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
        pair_observed = observed[:, None] & observed[None, :]
        numerator += np.where(pair_observed, difference, 0.0)
        denominator += pair_observed
    distance = np.divide(
        numerator, denominator,
        out=np.zeros_like(numerator), where=denominator > 0,
    )
    np.fill_diagonal(distance, 0.0)
    return distance, denominator


def affinity(distance):
    positive = distance[distance > 0]
    sigma = float(np.median(positive)) if len(positive) else 1.0
    result = np.exp(-(distance ** 2) / (2 * sigma ** 2))
    np.fill_diagonal(result, 1.0)
    return result


def fit_kmedoids(distance, k, n_init=200, max_iter=150, random_state=RANDOM_STATE):
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


D, pair_coverage = mixed_gower(features)
assert np.allclose(D, D.T) and D.min() >= 0 and D.max() <= 1


# %% [markdown]
# ## 2. K-medoids/spectral candidate and resampling comparison

def subsample_stability(algorithm, k, reference_labels):
    offset = 0 if algorithm == "kmedoids" else 10000
    rng = np.random.default_rng(RANDOM_STATE + 100 * k + offset)
    sample_size = int(np.floor(SUBSAMPLE_FRACTION * len(D)))
    results = []
    for repetition in range(SUBSAMPLE_REPETITIONS):
        idx = np.sort(rng.choice(len(D), size=sample_size, replace=False))
        D_sub = D[np.ix_(idx, idx)]
        if algorithm == "kmedoids":
            fit = fit_kmedoids(
                D_sub, k, n_init=60,
                random_state=RANDOM_STATE + 1000 * k + repetition,
            )
            medoids = idx[fit["medoids"]]
        else:
            labels_sub = SpectralClustering(
                n_clusters=k, affinity="precomputed", assign_labels="kmeans",
                n_init=30, random_state=RANDOM_STATE + 2000 * k + repetition,
            ).fit_predict(affinity(D_sub))
            medoids = idx[medoids_from_labels(D_sub, labels_sub)]
        predicted = np.argmin(D[:, medoids], axis=1)
        results.append(adjusted_rand_score(reference_labels, predicted))
    return np.asarray(results)


candidate_rows = []
stability_rows = []
solutions = {}
for k in range(2, 5):
    kmedoids = fit_kmedoids(D, k, n_init=500, random_state=RANDOM_STATE + k)
    spectral = SpectralClustering(
        n_clusters=k, affinity="precomputed", assign_labels="kmeans",
        n_init=100, random_state=RANDOM_STATE + 100 + k,
    ).fit_predict(affinity(D))
    solutions[("kmedoids", k)] = kmedoids["labels"]
    solutions[("spectral", k)] = spectral
    k_stability = subsample_stability("kmedoids", k, kmedoids["labels"])
    s_stability = subsample_stability("spectral", k, spectral)
    stability_rows.extend(
        {"algorithm": algorithm, "k": k, "repetition": i + 1, "ari": value}
        for algorithm, values_array in [
            ("kmedoids", k_stability), ("spectral", s_stability)
        ]
        for i, value in enumerate(values_array)
    )
    candidate_rows.append({
        "k": k,
        "kmedoids_silhouette": silhouette_score(D, kmedoids["labels"], metric="precomputed"),
        "spectral_silhouette": silhouette_score(D, spectral, metric="precomputed"),
        "kmedoids_stability_mean": k_stability.mean(),
        "kmedoids_stability_p10": np.quantile(k_stability, 0.10),
        "spectral_stability_mean": s_stability.mean(),
        "spectral_stability_p10": np.quantile(s_stability, 0.10),
        "cross_algorithm_ari": adjusted_rand_score(kmedoids["labels"], spectral),
        "kmedoids_minimum_cluster_size": int(pd.Series(kmedoids["labels"]).value_counts().min()),
        "spectral_minimum_cluster_size": int(pd.Series(spectral).value_counts().min()),
        "minimum_cluster_size_across_algorithms": min(
            int(pd.Series(kmedoids["labels"]).value_counts().min()),
            int(pd.Series(spectral).value_counts().min()),
        ),
    })

candidate_metrics = pd.DataFrame(candidate_rows)
candidate_stability = pd.DataFrame(stability_rows)
candidate_metrics["size_eligible"] = candidate_metrics[
    "minimum_cluster_size_across_algorithms"
].ge(MIN_PROFILE_SIZE)
eligible = candidate_metrics.loc[candidate_metrics["size_eligible"]].copy()

# Select a diagnostic k for transparent failure analysis, never as a retained
# typology when the eligibility gate is empty.
candidate_metrics["mean_source_silhouette"] = candidate_metrics[[
    "kmedoids_silhouette", "spectral_silhouette"
]].mean(axis=1)
diagnostic_k = int(
    candidate_metrics.sort_values(
        ["mean_source_silhouette", "cross_algorithm_ari", "k"],
        ascending=[False, False, True],
    ).iloc[0]["k"]
)
diagnostic_labels = solutions[("kmedoids", diagnostic_k)]


# %% [markdown]
# ## 3. Dominance, leave-one-feature-out and permutation calibration

single_feature_rows = []
leave_one_rows = []
for feature in SOURCE_VARIABLES:
    D_single, _ = mixed_gower(features, [feature])
    single = fit_kmedoids(
        D_single, diagnostic_k, n_init=400,
        random_state=RANDOM_STATE + 30000 + SOURCE_VARIABLES.index(feature),
    )["labels"]
    single_feature_rows.append({
        "single_feature": feature,
        "ari_single_feature_vs_diagnostic_kmedoids": adjusted_rand_score(
            diagnostic_labels, single
        ),
    })
    retained = [column for column in SOURCE_VARIABLES if column != feature]
    D_reduced, coverage_reduced = mixed_gower(features, retained)
    reduced = fit_kmedoids(
        D_reduced, diagnostic_k, n_init=400,
        random_state=RANDOM_STATE + 31000 + SOURCE_VARIABLES.index(feature),
    )["labels"]
    leave_one_rows.append({
        "omitted_feature": feature,
        "minimum_pair_coverage": int(coverage_reduced.min()),
        "ari_reduced_vs_diagnostic_kmedoids": adjusted_rand_score(
            diagnostic_labels, reduced
        ),
        "reduced_minimum_cluster_size": int(pd.Series(reduced).value_counts().min()),
    })
single_feature_dominance = pd.DataFrame(single_feature_rows)
leave_one_feature_out = pd.DataFrame(leave_one_rows)

observed_valid_kmedoids = candidate_metrics.loc[
    candidate_metrics["kmedoids_minimum_cluster_size"].ge(MIN_PROFILE_SIZE),
    "kmedoids_silhouette",
]
observed_maximum_silhouette = float(observed_valid_kmedoids.max())
permutation_rng = np.random.default_rng(RANDOM_STATE + 40000)
permutation_rows = []
for repetition in range(PERMUTATION_REPETITIONS):
    shuffled = features.copy()
    for column in SOURCE_VARIABLES:
        shuffled[column] = permutation_rng.permutation(shuffled[column].to_numpy())
    D_null, _ = mixed_gower(shuffled)
    valid_silhouettes = []
    for k in range(2, 5):
        null_labels = fit_kmedoids(
            D_null, k, n_init=80,
            random_state=RANDOM_STATE + 41000 + 10 * repetition + k,
        )["labels"]
        if pd.Series(null_labels).value_counts().min() >= MIN_PROFILE_SIZE:
            valid_silhouettes.append(silhouette_score(
                D_null, null_labels, metric="precomputed"
            ))
    permutation_rows.append({
        "repetition": repetition + 1,
        "maximum_valid_kmedoids_silhouette": (
            max(valid_silhouettes) if valid_silhouettes else np.nan
        ),
    })
permutation_null = pd.DataFrame(permutation_rows)
valid_null = permutation_null["maximum_valid_kmedoids_silhouette"].dropna()
empirical_p = float(
    (1 + (valid_null >= observed_maximum_silhouette).sum())
    / (1 + len(valid_null))
)

diagnostic_assignments = cohort[admin_columns].copy()
for variable in SOURCE_VARIABLES:
    diagnostic_assignments[f"{variable}__value"] = cohort[f"{variable}__value"]
    diagnostic_assignments[f"{variable}__response"] = cohort[f"{variable}__response"]
diagnostic_assignments["diagnostic_k"] = diagnostic_k
diagnostic_assignments["rejected_diagnostic_cluster"] = diagnostic_labels + 1

diagnostic_sizes = (
    diagnostic_assignments["rejected_diagnostic_cluster"]
    .value_counts().sort_index().rename_axis("cluster").reset_index(name="records")
)
diagnostic_sizes["percent"] = 100 * diagnostic_sizes["records"] / len(cohort)

dominance_max = float(
    single_feature_dominance["ari_single_feature_vs_diagnostic_kmedoids"].max()
)
dominance_feature = str(
    single_feature_dominance.sort_values(
        "ari_single_feature_vs_diagnostic_kmedoids", ascending=False
    ).iloc[0]["single_feature"]
)
diagnostic_row = candidate_metrics.loc[
    candidate_metrics["k"].eq(diagnostic_k)
].iloc[0]
quality_checks = pd.DataFrame([
    {"check": "at least one k passes the cross-algorithm minimum-size rule", "value": int(len(eligible)), "passed": not eligible.empty},
    {"check": "diagnostic mean source silhouette >= 0.25", "value": diagnostic_row["mean_source_silhouette"], "passed": diagnostic_row["mean_source_silhouette"] >= 0.25},
    {"check": "diagnostic cross-algorithm ARI >= 0.60", "value": diagnostic_row["cross_algorithm_ari"], "passed": diagnostic_row["cross_algorithm_ari"] >= 0.60},
    {"check": "diagnostic K-medoids stability mean >= 0.80", "value": diagnostic_row["kmedoids_stability_mean"], "passed": diagnostic_row["kmedoids_stability_mean"] >= 0.80},
    {"check": "diagnostic spectral stability mean >= 0.80", "value": diagnostic_row["spectral_stability_mean"], "passed": diagnostic_row["spectral_stability_mean"] >= 0.80},
    {"check": "not near-exactly reproduced by one feature (ARI < 0.90)", "value": dominance_max, "passed": dominance_max < 0.90},
    {"check": "permutation screening p < 0.05", "value": empirical_p, "passed": empirical_p < 0.05},
])

# The predeclared minimum-size gate is mandatory. No consensus is constructed
# when it fails, even if a diagnostic silhouette appears attractive.
retained = False
status = "No sufficiently robust Branch F educational/cultural-capital segmentation found"


# %% [markdown]
# ## 4. Diagnostic plots and reproducible outputs

fig, axes = plt.subplots(1, 2, figsize=(12, 4.5))
axes[0].plot(candidate_metrics["k"], candidate_metrics["mean_source_silhouette"], marker="o")
axes[0].axvline(diagnostic_k, color="tab:red", linestyle="--", label=f"diagnostic k={diagnostic_k}")
axes[0].set(title="Candidate separation", xlabel="Number of clusters", ylabel="Mean Gower silhouette")
axes[0].legend()
axes[1].plot(candidate_metrics["k"], candidate_metrics["kmedoids_stability_mean"], marker="o", label="K-medoids stability")
axes[1].plot(candidate_metrics["k"], candidate_metrics["spectral_stability_mean"], marker="o", label="Spectral stability")
axes[1].plot(candidate_metrics["k"], candidate_metrics["cross_algorithm_ari"], marker="s", label="Cross-algorithm ARI")
axes[1].axvline(diagnostic_k, color="tab:red", linestyle="--")
axes[1].set(title="Stability and algorithm agreement", xlabel="Number of clusters", ylabel="ARI", ylim=(-0.05, 1.05))
axes[1].legend()
fig.tight_layout()
fig.savefig(OUT / "educational_cultural_candidate_diagnostics.png", dpi=180, bbox_inches="tight")
plt.close(fig)

J = np.eye(len(D)) - np.ones_like(D) / len(D)
B = -0.5 * J @ (D ** 2) @ J
eigenvalues, eigenvectors = np.linalg.eigh(B)
order = np.argsort(eigenvalues)[::-1]
positive = order[eigenvalues[order] > 0][:2]
coordinates = eigenvectors[:, positive] * np.sqrt(eigenvalues[positive])
fig, ax = plt.subplots(figsize=(8, 6))
for cluster in sorted(np.unique(diagnostic_labels)):
    mask = diagnostic_labels == cluster
    ax.scatter(
        coordinates[mask, 0], coordinates[mask, 1], s=36, alpha=0.72,
        edgecolor="white", linewidth=0.4,
        label=f"Rejected diagnostic cluster {cluster + 1}",
    )
ax.set(
    title="Rejected diagnostic educational/cultural-capital partition",
    xlabel="Classical MDS axis 1 (display only)",
    ylabel="Classical MDS axis 2 (display only)",
)
ax.legend()
fig.tight_layout()
fig.savefig(OUT / "educational_cultural_rejected_diagnostic_scatterplot.png", dpi=180, bbox_inches="tight")
plt.close(fig)

variable_screening.to_csv(OUT / "educational_cultural_variable_screening.csv", index=False)
candidate_metrics.to_csv(OUT / "educational_cultural_candidate_metrics.csv", index=False)
candidate_stability.to_csv(OUT / "educational_cultural_candidate_subsample_stability.csv", index=False)
single_feature_dominance.to_csv(OUT / "educational_cultural_single_feature_dominance.csv", index=False)
leave_one_feature_out.to_csv(OUT / "educational_cultural_leave_one_feature_out.csv", index=False)
permutation_null.to_csv(OUT / "educational_cultural_permutation_null.csv", index=False)
diagnostic_assignments.to_csv(OUT / "educational_cultural_rejected_diagnostic_assignments.csv", index=False)
diagnostic_sizes.to_csv(OUT / "educational_cultural_rejected_diagnostic_sizes.csv", index=False)
quality_checks.to_csv(OUT / "educational_cultural_quality_checks.csv", index=False)

summary = {
    "cohort": {
        "records": int(len(cohort)),
        "branch": "F",
        "strict_final_branch_records": 82,
        "excluded_routing_integrity_records": 1,
    },
    "dimension": "educational and inherited cultural capital",
    "clustering_features": SOURCE_VARIABLES,
    "measurement": {
        "father_edu": "ordered questionnaire response; unknown/refusal unavailable",
        "mother_edu": "ordered questionnaire response; unknown/refusal unavailable",
        "edu_status": "nominal current education position",
        "worked_while_studying": "binary work-exposure indicator",
    },
    "method": {
        "distance": "equal-weight missing-aware mixed Gower on four original responses",
        "candidate_k": [2, 3, 4],
        "subsample_repetitions_per_algorithm": SUBSAMPLE_REPETITIONS,
        "permutation_repetitions": PERMUTATION_REPETITIONS,
        "consensus_constructed": False,
        "consensus_reason": "no candidate passed the minimum-size rule across both source algorithms",
    },
    "diagnostic_only": {
        "k": diagnostic_k,
        "kmedoids_sizes": {
            str(int(row.cluster)): int(row.records)
            for row in diagnostic_sizes.itertuples()
        },
        "mean_source_silhouette": float(diagnostic_row["mean_source_silhouette"]),
        "cross_algorithm_ari": float(diagnostic_row["cross_algorithm_ari"]),
        "kmedoids_stability_mean": float(diagnostic_row["kmedoids_stability_mean"]),
        "spectral_stability_mean": float(diagnostic_row["spectral_stability_mean"]),
        "dominant_single_feature": dominance_feature,
        "maximum_single_feature_ari": dominance_max,
        "observed_maximum_kmedoids_silhouette": observed_maximum_silhouette,
        "permutation_null_median": float(valid_null.median()),
        "permutation_null_p95": float(valid_null.quantile(0.95)),
        "empirical_permutation_p": empirical_p,
    },
    "decision": {
        "retained_for_clustering": retained,
        "checks_passed": int(quality_checks["passed"].sum()),
        "checks_total": int(len(quality_checks)),
        "status": status,
    },
    "limitations": [
        "These are original-response similarities, not a validated cultural-capital scale.",
        "Parental education is a proxy for family cultural capital and must not be interpreted as respondent merit or ability.",
        "Education status describes current educational position and is nominal; categories are not ranked.",
        "Worked while studying measures exposure, not the quality or relevance of the work.",
        "The diagnostic assignments are saved only to explain failure and must not be used as final profiles.",
        "The Branch F sample contains only 81 valid respondents.",
    ],
}
with open(OUT / "educational_cultural_clustering_summary.json", "w", encoding="utf-8") as handle:
    json.dump(summary, handle, indent=2)

print(json.dumps(summary, indent=2))
print("\nCandidate metrics:\n", candidate_metrics.to_string(index=False))
print("\nQuality checks:\n", quality_checks.to_string(index=False))
print("\nSaved outputs to", OUT)

