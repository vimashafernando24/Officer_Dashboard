# %% [markdown]
# # Branch F — earnings and working-time preference patterns
#
# This notebook clusters the 81 valid final-Branch-F employment records using
# three original SWTS employment-condition responses. Employment security and
# formality remain a separate dimension.

# %% [markdown]
# ## Theory and equation
#
# The ILO School-to-Work Transition Survey treats earnings, working hours, and
# the respondent's preference for changing hours and income as employment-quality
# conditions. We compare monthly income band, usual weekly hours, and whether the
# respondent wants more hours/income, no change, or fewer hours/income.
#
# No adequacy score is invented. Equal-maximum-weight Gower distance is:
#
# $$d(i,j)=\frac{1}{3}\sum_{h=1}^{3}\delta_{ijh}$$
#
# Income retains questionnaire order, usual hours use normalized absolute
# difference, and hours/income preference is nominal because its three categories
# represent different situations rather than a validated interval scale.

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
OUT = ROOT / "outputs/branch_f_earnings_working_time_clusters"
OUT.mkdir(parents=True, exist_ok=True)

CLUSTER_FEATURES = [
    "monthly_income_band", "usual_hours_per_week", "income_hours_preference",
]
FEATURE_TYPES = {
    "monthly_income_band": "ordinal",
    "usual_hours_per_week": "continuous",
    "income_hours_preference": "nominal",
}
DESCRIPTOR_VARIABLES = [
    "actual_hours_last_week", "hours_below_normal", "job_satisfaction",
    "has_second_job",
]
ALL_SOURCE_VARIABLES = CLUSTER_FEATURES + DESCRIPTOR_VARIABLES

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
        "role": "cluster_input" if variable in CLUSTER_FEATURES else "profile_descriptor",
        "observed": int(response.notna().sum()),
        "missing": int(response.isna().sum()),
        "unique_observed_responses": int(response.nunique(dropna=True)),
        "dominant_response": str(counts.index[0]),
        "dominant_response_percent": 100 * float(counts.iloc[0] / len(response)),
    })
variable_screening = pd.DataFrame(screening_rows)

income_code = pd.to_numeric(cohort["monthly_income_band__value"], errors="coerce")
usual_hours = pd.to_numeric(cohort["usual_hours_per_week__value"], errors="coerce")
features = pd.DataFrame(index=cohort.index)
features["monthly_income_band"] = income_code.where(income_code.between(1, 6)).map(
    {1: 0.0, 2: 0.2, 3: 0.4, 4: 0.6, 5: 0.8, 6: 1.0}
)
features["usual_hours_per_week"] = usual_hours.where(usual_hours.between(0, 112))
features["income_hours_preference"] = cohort[
    "income_hours_preference__response"
].astype("string")

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
display(usual_hours.describe(percentiles=[0.01, 0.05, 0.95, 0.99]).to_frame("usual_hours"))


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
eligible = candidate_metrics.loc[
    candidate_metrics["minimum_cluster_size_across_sources"].ge(MIN_PROFILE_SIZE)
].copy()
if eligible.empty:
    display(candidate_metrics.round(4))
    raise RuntimeError("No k=2–4 candidate meets the minimum profile-size rule.")
eligible["rank_silhouette"] = eligible["mean_source_silhouette"].rank(ascending=False, method="min")
eligible["rank_stability"] = eligible["mean_source_stability"].rank(ascending=False, method="min")
eligible["primary_mean_rank"] = eligible[["rank_silhouette", "rank_stability"]].mean(axis=1)
best_rank = eligible["primary_mean_rank"].min()
selected_k = int(eligible.loc[eligible["primary_mean_rank"].eq(best_rank)].sort_values("k").iloc[0]["k"])
candidate_metrics = candidate_metrics.merge(eligible[["k", "primary_mean_rank"]], on="k", how="left")
candidate_metrics["selected"] = candidate_metrics["k"].eq(selected_k)
display(candidate_metrics.round(4))
print("Selected k:", selected_k)

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
# Give the profile IDs a reproducible substantive order: the group with the
# smaller share wanting more hours/income is Profile 1. Income and hours break
# an unlikely tie. This changes names only; it does not affect clustering.
raw_order = sorted(raw_medoids, key=lambda raw: (
    features.loc[raw_labels == raw, "income_hours_preference"].eq(
        "More hours and correspondingly more income"
    ).mean(),
    features.loc[raw_labels == raw, "monthly_income_band"].median(),
    features.loc[raw_labels == raw, "usual_hours_per_week"].median(),
))
raw_to_profile = {raw: i + 1 for i, raw in enumerate(raw_order)}
profile_id = np.asarray([raw_to_profile[int(raw)] for raw in raw_labels])
profile_names = {
    1: "Mostly current-hours preference",
    2: "More-hours/more-income preference",
}

assignments = cohort[["respondent_id", "entry_branch", "branch", "branch_routing_source"]].copy()
for variable in ALL_SOURCE_VARIABLES:
    assignments[f"{variable}__value"] = cohort[f"{variable}__value"]
    assignments[f"{variable}__response"] = cohort[f"{variable}__response"]
assignments["earnings_time_profile_id"] = profile_id
assignments["earnings_time_profile_label"] = assignments["earnings_time_profile_id"].map(profile_names)
gower_sil = silhouette_samples(D, profile_id, metric="precomputed")
consensus_sil = silhouette_samples(consensus_distance, profile_id, metric="precomputed")
assignments["gower_individual_silhouette"] = gower_sil
assignments["consensus_individual_silhouette"] = consensus_sil

profile_sizes = assignments.groupby([
    "earnings_time_profile_id", "earnings_time_profile_label"
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
    temp = assignments.groupby(["earnings_time_profile_id", col], dropna=False).size().rename("records").reset_index()
    temp["within_profile_percent"] = 100 * temp["records"] / temp.groupby("earnings_time_profile_id")["records"].transform("sum")
    temp = temp.rename(columns={col: "response"})
    temp.insert(1, "variable", variable)
    response_rows.append(temp)
profile_response_distributions = pd.concat(response_rows, ignore_index=True)
profile_modes = profile_response_distributions.sort_values(
    ["earnings_time_profile_id", "variable", "within_profile_percent"],
    ascending=[True, True, False],
).groupby(["earnings_time_profile_id", "variable"], as_index=False).first()
profile_numeric_medians = pd.DataFrame({
    "earnings_time_profile_id": profile_id,
    "monthly_income_code": income_code,
    "usual_hours_per_week": usual_hours,
}).groupby("earnings_time_profile_id").median()
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
        "earnings_time_profile_id": int(own),
        "within_profile_consensus": within,
        "strongest_other_profile_consensus": other,
        "consensus_margin": within - other,
        "ambiguous_consensus_membership": (within < 0.70) or ((within - other) < 0.20),
    })
respondent_confidence = pd.DataFrame(confidence_rows)
assignments = assignments.merge(respondent_confidence.drop(columns="earnings_time_profile_id"), on="respondent_id", validate="one_to_one")

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
    D_reduced, reduced_coverage = mixed_gower(features, retained)
    reduced = fit_kmedoids(D_reduced, selected_k, n_init=400, random_state=RANDOM_STATE + 90000 + CLUSTER_FEATURES.index(omitted))["labels"]
    sensitivity_rows.append({
        "omitted_feature": omitted, "retained_features": len(retained),
        "minimum_pair_coverage": int(reduced_coverage.min()),
        "gower_silhouette_reduced_kmedoids": silhouette_score(D_reduced, reduced, metric="precomputed"),
        "ari_reduced_kmedoids_vs_final_consensus": adjusted_rand_score(profile_id, reduced),
    })
feature_sensitivity = pd.DataFrame(sensitivity_rows)

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
}
quality_checks = pd.DataFrame([
    {"check": "original Gower silhouette >= 0.25", "value": metrics["gower_silhouette"], "passed": metrics["gower_silhouette"] >= 0.25},
    {"check": "ensemble bootstrap mean ARI >= 0.80", "value": metrics["ensemble_bootstrap_ari_mean"], "passed": metrics["ensemble_bootstrap_ari_mean"] >= 0.80},
    {"check": f"minimum profile size >= {MIN_PROFILE_SIZE}", "value": metrics["minimum_profile_size"], "passed": metrics["minimum_profile_size"] >= MIN_PROFILE_SIZE},
    {"check": "ARI with full K-medoids >= 0.60", "value": metrics["ari_vs_full_kmedoids"], "passed": metrics["ari_vs_full_kmedoids"] >= 0.60},
    {"check": "ARI with full spectral >= 0.60", "value": metrics["ari_vs_full_spectral"], "passed": metrics["ari_vs_full_spectral"] >= 0.60},
    {"check": "PAC <= 0.20", "value": metrics["pac_10_90"], "passed": metrics["pac_10_90"] <= 0.20},
    {"check": "ambiguous respondents <= 20%", "value": metrics["ambiguous_consensus_percent"], "passed": metrics["ambiguous_consensus_percent"] <= 20},
    {"check": "low-confidence respondents <= 20%", "value": metrics["low_gower_confidence_percent"], "passed": metrics["low_gower_confidence_percent"] <= 20},
])
primary_pass = bool(quality_checks.iloc[:5]["passed"].all())
if primary_pass and quality_checks.iloc[5:]["passed"].all():
    status = "Stable, cross-method-supported but preference-led segmentation"
elif primary_pass:
    status = "Passes primary stability rules but retains ambiguity cautions"
else:
    status = "No sufficiently robust earnings/working-time segmentation found"
display(pd.Series(metrics, name="value").to_frame().round(3))
display(quality_checks.round(3))
display(feature_sensitivity.round(3))
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
fig.savefig(OUT / "earnings_time_candidate_diagnostics.png", dpi=180, bbox_inches="tight")
plt.show()

J = np.eye(n) - np.ones((n, n)) / n
B = -0.5 * J @ (D ** 2) @ J
eigenvalues, eigenvectors = np.linalg.eigh(B)
order = np.argsort(eigenvalues)[::-1]
positive = order[eigenvalues[order] > 0][:2]
coordinates = eigenvectors[:, positive] * np.sqrt(eigenvalues[positive])
fig, ax = plt.subplots(figsize=(8, 6))
for pid in sorted(np.unique(profile_id)):
    mask = profile_id == pid
    ax.scatter(coordinates[mask, 0], coordinates[mask, 1], s=42, alpha=0.7, edgecolor="white", linewidth=0.5, label=profile_names[int(pid)])
ax.set(title="Branch F earnings/working-time preference patterns", xlabel="Classical MDS axis 1 (display only)", ylabel="Classical MDS axis 2 (display only)")
ax.legend()
fig.tight_layout()
fig.savefig(OUT / "earnings_time_profile_scatterplot.png", dpi=180, bbox_inches="tight")
plt.show()

variable_screening.to_csv(OUT / "earnings_time_variable_screening.csv", index=False)
feature_audit.to_csv(OUT / "earnings_time_feature_audit.csv", index=False)
candidate_metrics.to_csv(OUT / "earnings_time_candidate_metrics.csv", index=False)
candidate_stability.to_csv(OUT / "earnings_time_candidate_subsample_stability.csv", index=False)
base_partition_diagnostics.to_csv(OUT / "earnings_time_consensus_base_partitions.csv", index=False)
assignments.to_csv(OUT / "earnings_time_consensus_assignments.csv", index=False)
profile_sizes.to_csv(OUT / "earnings_time_profile_sizes.csv", index=False)
profile_response_distributions.to_csv(OUT / "earnings_time_profile_response_distributions.csv", index=False)
profile_modes.to_csv(OUT / "earnings_time_profile_modes.csv", index=False)
profile_numeric_medians.to_csv(OUT / "earnings_time_profile_numeric_medians.csv")
respondent_confidence.to_csv(OUT / "earnings_time_respondent_confidence.csv", index=False)
ensemble_stability.to_csv(OUT / "earnings_time_consensus_ensemble_stability.csv", index=False)
feature_sensitivity.to_csv(OUT / "earnings_time_leave_one_feature_out.csv", index=False)
quality_checks.to_csv(OUT / "earnings_time_quality_checks.csv", index=False)

summary = {
    "cohort": {"records": 81, "branch": "F", "strict_final_branch_records": 82, "excluded_routing_integrity_records": 1},
    "dimension": "earnings and working-time preference patterns",
    "clustering_features": CLUSTER_FEATURES,
    "descriptors": DESCRIPTOR_VARIABLES,
    "method": {"distance": "equal-weight mixed Gower on three original responses", "selected_k": selected_k, "ensemble": "K-medoids plus spectral consensus", "base_partitions": 200},
    "profiles": {"sizes": {str(int(r.earnings_time_profile_id)): int(r.records) for r in profile_sizes.itertuples()}, "names": {str(k): v for k, v in profile_names.items()}},
    "metrics": metrics,
    "decision": {
        "primary_checks_passed": primary_pass,
        "checks_passed": int(quality_checks["passed"].sum()),
        "checks_total": int(len(quality_checks)),
        "statistical_status": status,
        "included_in_final_dimension_set": False,
        "exclusion_reason": "Final researcher scope decision: retain only the multidimensional employment-security/formality clustering; this solution is primarily a direct hours/income-preference segmentation.",
        "status": "Excluded from the final Branch F dimension set despite statistical stability",
    },
    "limitations": [
        "These are exploratory earnings/working-time response profiles, not a validated employment-adequacy scale.",
        "Hours/income preference is nominal; no numeric desirability order is imposed.",
        "Usual weekly hours are self-reported and do not by themselves identify overwork or underemployment.",
        "Job satisfaction and actual hours describe profiles but do not determine distance.",
        "The result is driven mainly by hours/income preference: omitting that feature changes the partition substantially, so this is not evidence of two broad earnings levels.",
        "The one routing-corrupted final-Branch-F record is excluded from this employment analysis.",
    ],
}
with open(OUT / "earnings_time_clustering_summary.json", "w", encoding="utf-8") as handle:
    json.dump(summary, handle, indent=2)
print(json.dumps(summary, indent=2))

# %% [markdown]
# ## Interpretation guardrails
#
# - These profiles describe earnings and working-time response patterns only.
# - The split is preference-led; both profiles have the same median income-band
#   code and the same median usual weekly hours in this sample.
# - Final framework decision: keep this result only as a descriptive diagnostic;
#   it is not part of the retained Branch F clustering set.
# - They do not measure personal worth, productivity, or programme eligibility.
# - Profile names are descriptive and assigned only after examining distributions.
