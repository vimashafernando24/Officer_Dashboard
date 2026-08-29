# %% [markdown]
# # Branch F — theory-constrained candidate-dimension discovery
#
# This notebook is an exploratory screening tool. It does **not** search all 105
# Branch F variables and declare the best-looking result a new dimension. It:
#
# 1. uses only the 34 variables previously audited as possible clustering inputs;
# 2. groups variables with mixed-type association measures and row bootstraps;
# 3. searches subsets only inside the pre-specified D1–D9 theory pools;
# 4. validates shortlisted respondent partitions out of sample;
# 5. checks single-item dominance and calibrates each theory pool against an
#    independent-column permutation null.
#
# Statistical stability can support a candidate dimension, but theory and an
# independent sample are still required before claiming construct validity.

# %% [markdown]
# ## Methodological basis
#
# Mixed-variable grouping follows the association-matrix strategy used in the
# CluMix/ClustOfVar literature: absolute Spearman association for two ordered or
# quantitative variables, bias-corrected Cramer's V for two nominal variables,
# and the correlation ratio for a nominal–numeric pair. Average-linkage
# clustering is repeated on bootstrap samples of respondents.
#
# Respondents are clustered with equal-weight Gower distance. Candidate subsets
# are compared using K-medoids, spectral clustering, out-of-sample prediction
# strength, minimum profile size, leave-one-feature logic through a single-item
# dominance statistic, and pool-wise permutation calibration. PAC is reported
# comparatively; no universal PAC cutoff is imposed.
#
# Key references:
#
# - Chavent et al. (2012), *ClustOfVar: An R Package for the Clustering of Variables*.
# - Witten & Tibshirani (2010), *A Framework for Feature Selection in Clustering*.
# - Tibshirani & Walther (2005), *Cluster Validation by Prediction Strength*.
# - Raftery & Dean (2006), *Variable Selection for Model-Based Clustering*.

# %%
from pathlib import Path
from itertools import combinations
import json
import warnings

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from IPython.display import display
from scipy.cluster.hierarchy import fcluster, linkage
from scipy.spatial.distance import squareform
from scipy.stats import chi2_contingency, rankdata
from sklearn.cluster import SpectralClustering
from sklearn.metrics import adjusted_rand_score, silhouette_score

warnings.filterwarnings("ignore", category=FutureWarning)
pd.set_option("display.max_columns", 100)
pd.set_option("display.width", 220)

ROOT = Path.cwd()
VALUES_PATH = ROOT / "outputs/nysc_survey_cleaned_values.csv"
LABELS_PATH = ROOT / "outputs/nysc_survey_cleaned_labels.csv"
AUDIT_PATH = ROOT / "outputs/branch_f_variable_dimension_audit/branch_f_all_105_variables.csv"
OUT = ROOT / "outputs/branch_f_candidate_dimension_discovery"
OUT.mkdir(parents=True, exist_ok=True)

RANDOM_STATE = 20260825
MIN_PROFILE_SIZE = 15
SUBSET_MIN_SIZE = 2
SUBSET_MAX_SIZE = 4
VARIABLE_GROUP_BOOTSTRAPS = 60
VARIABLE_GROUP_COUNTS = range(2, 11)
PREDICTION_SPLITS = 30
PREDICTION_TRAIN_FRACTION = 0.67
SHORTLIST_PER_POOL = 3
NULL_REPETITIONS = 30
NULL_FINAL_RECOMMENDATION = 200

# Thirty null repetitions make this notebook runnable as a screening analysis.
# Increase NULL_REPETITIONS to at least 200 before reporting a final empirical p-value.

# %% [markdown]
# ## 1. Rebuild the strict valid Branch F cohort and eligible-variable catalogue

# %%
audit = pd.read_csv(AUDIT_PATH)
eligible_catalogue = audit.loc[
    audit["proposed_role"].eq("proposed clustering input")
].copy()
ELIGIBLE_VARIABLES = eligible_catalogue["variable"].tolist()
assert len(ELIGIBLE_VARIABLES) == 34

values_all = pd.read_csv(VALUES_PATH)
labels_all = pd.read_csv(LABELS_PATH)
strict_mask = (
    values_all["branch"].eq("F")
    & values_all["branch_routing_source"].eq("translated_final_active_branch")
    & ~values_all["branch_integrity_issue"].astype(bool)
    & values_all["employment_status"].notna()
)
values = values_all.loc[strict_mask, ["respondent_id"] + ELIGIBLE_VARIABLES].copy()
labels = labels_all.loc[strict_mask, ["respondent_id"] + ELIGIBLE_VARIABLES].copy()
labels = labels.rename(columns={v: f"{v}__response" for v in ELIGIBLE_VARIABLES})
values = values.rename(columns={v: f"{v}__value" for v in ELIGIBLE_VARIABLES})
cohort = values.merge(labels, on="respondent_id", validate="one_to_one")
assert len(cohort) == 81 and cohort["respondent_id"].nunique() == 81

THEORY_POOLS = {
    dimension: group["variable"].tolist()
    for dimension, group in eligible_catalogue.groupby("proposed_dimension", sort=True)
}

# D7 remains visible in the variable-group discovery, but is not searched for
# respondent clusters because the user previously excluded overlapping social-
# connectedness clustering.
SKIPPED_RESPONDENT_POOLS = {"D7 — Professional social capital"}

TYPE_SPEC = {
    # D1
    "household_income": "ordinal",
    "household_size": "continuous",
    "household_workers": "continuous",
    "household_unemployed": "continuous",
    "primary_earner_status": "nominal",
    "primary_income_source": "nominal",
    # D2
    "father_edu": "ordinal",
    "mother_edu": "ordinal",
    "edu_status": "nominal",
    "worked_while_studying": "nominal",
    # D3
    "sector_formality": "ordinal",
    "contract_type": "nominal",
    "job_security_12months": "ordinal",
    # D4
    "usual_hours_per_week": "continuous",
    "income_hours_preference": "nominal",
    "monthly_income_band": "ordinal",
    # D5
    "contract_satisfaction": "nominal",
    "job_satisfaction": "ordinal",
    "hopes_to_change_job": "nominal",
    # D6
    "qualification_job_match": "ordinal",
    "received_training": "nominal",
    "past_edu_useful_for_job": "ordinal",
    # D7
    "employment_network_quality": "ordinal",
    "professional_network_growth": "ordinal",
    # D8
    "work_autonomy": "ordinal",
    "competence_growth_at_work": "ordinal",
    "relatedness_at_work": "ordinal",
    "work_motivation_type": "ordinal",
    # D9
    "registered_as_jobseeker": "nominal",
    "employment_service_help_f": "nominal",
    "jobs_applied_before_hire": "continuous",
    "interviews_before_hire": "continuous",
    "search_duration_before_hire": "ordinal",
    "obstacle_finding_this_job": "nominal",
}
assert set(TYPE_SPEC) == set(ELIGIBLE_VARIABLES)

UNKNOWN_PATTERN = r"do not know|don't know|prefer not|not sure"
LOG_COUNT_VARIABLES = {"jobs_applied_before_hire", "interviews_before_hire"}

features = pd.DataFrame(index=cohort.index)
encoding_rows = []
for variable in ELIGIBLE_VARIABLES:
    variable_type = TYPE_SPEC[variable]
    response = cohort[f"{variable}__response"].astype("string")
    raw_value = pd.to_numeric(cohort[f"{variable}__value"], errors="coerce")
    if variable_type == "nominal":
        encoded = response
    elif variable_type == "ordinal":
        encoded = raw_value.mask(response.str.lower().str.contains(UNKNOWN_PATTERN, regex=True, na=False))
        observed = encoded.dropna()
        span = float(observed.max() - observed.min())
        encoded = (encoded - observed.min()) / span if span else encoded * 0
    else:
        encoded = raw_value.where(raw_value.ge(0))
        if variable in LOG_COUNT_VARIABLES:
            encoded = np.log1p(encoded)
    features[variable] = encoded
    encoding_rows.append({
        "variable": variable,
        "theory_pool": eligible_catalogue.set_index("variable").loc[variable, "proposed_dimension"],
        "type": variable_type,
        "transformation": "log1p" if variable in LOG_COUNT_VARIABLES else (
            "questionnaire-order range [0,1]" if variable_type == "ordinal" else "none"
        ),
        "observed": int(encoded.notna().sum()),
        "missing_or_unknown": int(encoded.isna().sum()),
        "unique_encoded": int(encoded.nunique(dropna=True)),
        "dominant_response_percent": 100 * float(response.value_counts(dropna=False).iloc[0] / len(response)),
    })
encoding_audit = pd.DataFrame(encoding_rows)
display(encoding_audit)

# %% [markdown]
# ## 2. Bootstrap mixed-variable grouping

# %%
def corrected_cramers_v(x, y):
    table = pd.crosstab(x, y)
    n = table.to_numpy().sum()
    if n <= 1 or table.shape[0] < 2 or table.shape[1] < 2:
        return 0.0
    chi2 = chi2_contingency(table, correction=False)[0]
    phi2 = chi2 / n
    r, k = table.shape
    phi2_corrected = max(0.0, phi2 - ((k - 1) * (r - 1)) / (n - 1))
    r_corrected = r - ((r - 1) ** 2) / (n - 1)
    k_corrected = k - ((k - 1) ** 2) / (n - 1)
    denominator = min(k_corrected - 1, r_corrected - 1)
    return float(np.sqrt(phi2_corrected / denominator)) if denominator > 0 else 0.0


def correlation_ratio(categories, numeric):
    frame = pd.DataFrame({"category": categories, "numeric": numeric}).dropna()
    if frame.empty or frame["category"].nunique() < 2 or frame["numeric"].nunique() < 2:
        return 0.0
    grand = frame["numeric"].mean()
    between = sum(
        len(group) * (group["numeric"].mean() - grand) ** 2
        for _, group in frame.groupby("category", observed=True)
    )
    total = float(((frame["numeric"] - grand) ** 2).sum())
    return float(np.sqrt(between / total)) if total > 0 else 0.0


def spearman_absolute(x, y):
    frame = pd.DataFrame({"x": pd.to_numeric(x, errors="coerce"), "y": pd.to_numeric(y, errors="coerce")}).dropna()
    if len(frame) < 3 or frame["x"].nunique() < 2 or frame["y"].nunique() < 2:
        return 0.0
    return float(abs(pd.Series(rankdata(frame["x"])).corr(pd.Series(rankdata(frame["y"])))))


def mixed_association(x, y, type_x, type_y):
    valid = x.notna() & y.notna()
    x_valid, y_valid = x.loc[valid], y.loc[valid]
    if type_x == "nominal" and type_y == "nominal":
        return corrected_cramers_v(x_valid.astype(str), y_valid.astype(str))
    if type_x == "nominal":
        return correlation_ratio(x_valid.astype(str), pd.to_numeric(y_valid, errors="coerce"))
    if type_y == "nominal":
        return correlation_ratio(y_valid.astype(str), pd.to_numeric(x_valid, errors="coerce"))
    return spearman_absolute(x_valid, y_valid)


def association_matrix(frame):
    columns = list(frame.columns)
    result = np.eye(len(columns), dtype=float)
    for i, left in enumerate(columns):
        for j in range(i + 1, len(columns)):
            right = columns[j]
            association = mixed_association(
                frame[left], frame[right], TYPE_SPEC[left], TYPE_SPEC[right]
            )
            result[i, j] = result[j, i] = np.clip(association, 0, 1)
    return result


def variable_partition(association, group_count):
    distance = np.clip(1 - association, 0, 1)
    np.fill_diagonal(distance, 0)
    tree = linkage(squareform(distance, checks=False), method="average")
    return fcluster(tree, t=group_count, criterion="maxclust")


full_association = association_matrix(features)
variable_names = np.asarray(features.columns)
theory_labels = pd.Categorical(
    [eligible_catalogue.set_index("variable").loc[v, "proposed_dimension"] for v in variable_names]
).codes
full_partitions = {
    q: variable_partition(full_association, q) for q in VARIABLE_GROUP_COUNTS
}

bootstrap_rng = np.random.default_rng(RANDOM_STATE)
variable_group_stability_rows = []
variable_coclustering = {
    q: np.zeros_like(full_association) for q in VARIABLE_GROUP_COUNTS
}
for repetition in range(VARIABLE_GROUP_BOOTSTRAPS):
    idx = bootstrap_rng.choice(len(features), size=len(features), replace=True)
    boot_association = association_matrix(features.iloc[idx].reset_index(drop=True))
    for q in VARIABLE_GROUP_COUNTS:
        boot_partition = variable_partition(boot_association, q)
        variable_group_stability_rows.append({
            "repetition": repetition + 1,
            "variable_group_count": q,
            "ari_vs_full_variable_partition": adjusted_rand_score(
                full_partitions[q], boot_partition
            ),
        })
        variable_coclustering[q] += (
            boot_partition[:, None] == boot_partition[None, :]
        ).astype(float)

variable_group_stability = pd.DataFrame(variable_group_stability_rows)
variable_group_summary = variable_group_stability.groupby(
    "variable_group_count", as_index=False
).agg(
    bootstrap_ari_mean=("ari_vs_full_variable_partition", "mean"),
    bootstrap_ari_median=("ari_vs_full_variable_partition", "median"),
    bootstrap_ari_p10=("ari_vs_full_variable_partition", lambda x: x.quantile(0.10)),
)
variable_group_summary["ari_with_original_theory_pools"] = [
    adjusted_rand_score(theory_labels, full_partitions[q])
    for q in variable_group_summary["variable_group_count"]
]
selected_variable_group_count = int(
    variable_group_summary.sort_values(
        ["bootstrap_ari_median", "bootstrap_ari_mean", "variable_group_count"],
        ascending=[False, False, True],
    ).iloc[0]["variable_group_count"]
)
selected_variable_partition = full_partitions[selected_variable_group_count]
selected_consensus = variable_coclustering[selected_variable_group_count] / VARIABLE_GROUP_BOOTSTRAPS

variable_group_assignments = pd.DataFrame({
    "variable": variable_names,
    "data_driven_variable_group": selected_variable_partition,
    "theory_pool": [eligible_catalogue.set_index("variable").loc[v, "proposed_dimension"] for v in variable_names],
    "type": [TYPE_SPEC[v] for v in variable_names],
})
variable_group_assignments["mean_within_group_bootstrap_coclustering"] = [
    float(selected_consensus[i, selected_variable_partition == selected_variable_partition[i]].mean())
    for i in range(len(variable_names))
]
display(variable_group_summary.round(3))
display(variable_group_assignments.sort_values(["data_driven_variable_group", "variable"]))

# %% [markdown]
# ## 3. Theory-constrained subset search for respondent clustering

# %%
def mixed_gower(frame, columns):
    columns = list(columns)
    n = len(frame)
    numerator = np.zeros((n, n), dtype=float)
    denominator = np.zeros((n, n), dtype=float)
    for column in columns:
        variable_type = TYPE_SPEC[column]
        if variable_type == "nominal":
            series = frame[column].astype("string")
            observed = series.notna().to_numpy()
            values_array = series.fillna("__MISSING__").to_numpy(dtype=str)
            difference = (values_array[:, None] != values_array[None, :]).astype(float)
        else:
            series = pd.to_numeric(frame[column], errors="coerce")
            observed = series.notna().to_numpy()
            values_array = series.fillna(0).to_numpy(dtype=float)
            difference = np.abs(values_array[:, None] - values_array[None, :])
            if variable_type == "continuous":
                valid_values = values_array[observed]
                observed_range = float(valid_values.max() - valid_values.min())
                difference = difference / observed_range if observed_range else np.zeros_like(difference)
        pair_observed = observed[:, None] & observed[None, :]
        numerator += np.where(pair_observed, difference, 0.0)
        denominator += pair_observed
    distance = np.divide(numerator, denominator, out=np.zeros_like(numerator), where=denominator > 0)
    np.fill_diagonal(distance, 0.0)
    return distance, denominator


def fit_kmedoids(distance, k, n_init=50, max_iter=100, random_state=RANDOM_STATE):
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
                if not len(members):
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


def spectral_labels(distance, k, seed):
    positive = distance[distance > 0]
    sigma = float(np.median(positive)) if len(positive) else 1.0
    affinity = np.exp(-(distance ** 2) / (2 * sigma ** 2))
    np.fill_diagonal(affinity, 1.0)
    return SpectralClustering(
        n_clusters=k,
        affinity="precomputed",
        assign_labels="kmeans",
        n_init=30,
        random_state=seed,
    ).fit_predict(affinity)


def safe_silhouette(distance, labels_k):
    unique = np.unique(labels_k)
    if len(unique) < 2 or len(unique) >= len(labels_k):
        return np.nan
    return float(silhouette_score(distance, labels_k, metric="precomputed"))


def single_feature_dominance(columns, k, reference_labels):
    scores = []
    for column in columns:
        D_one, _ = mixed_gower(features, [column])
        one_labels = fit_kmedoids(
            D_one, k, n_init=40,
            random_state=RANDOM_STATE + 3000 + ELIGIBLE_VARIABLES.index(column) + 100 * k,
        )["labels"]
        scores.append((column, adjusted_rand_score(reference_labels, one_labels)))
    return max(scores, key=lambda item: item[1])


candidate_rows = []
candidate_cache = {}
candidate_id = 0
for theory_pool, pool_variables in THEORY_POOLS.items():
    if theory_pool in SKIPPED_RESPONDENT_POOLS:
        continue
    maximum_size = min(SUBSET_MAX_SIZE, len(pool_variables))
    for subset_size in range(SUBSET_MIN_SIZE, maximum_size + 1):
        for subset in combinations(pool_variables, subset_size):
            D_subset, coverage = mixed_gower(features, subset)
            for k in range(2, 5):
                candidate_id += 1
                km = fit_kmedoids(
                    D_subset, k, n_init=70,
                    random_state=RANDOM_STATE + 10000 + candidate_id,
                )
                sp = spectral_labels(D_subset, k, RANDOM_STATE + 20000 + candidate_id)
                dominant_variable, dominance_ari = single_feature_dominance(
                    subset, k, km["labels"]
                )
                km_min = int(pd.Series(km["labels"]).value_counts().min())
                sp_min = int(pd.Series(sp).value_counts().min())
                row = {
                    "candidate_id": candidate_id,
                    "theory_pool": theory_pool,
                    "variables": " | ".join(subset),
                    "variable_count": len(subset),
                    "k": k,
                    "minimum_pair_coverage": int(coverage.min()),
                    "kmedoids_silhouette": safe_silhouette(D_subset, km["labels"]),
                    "spectral_silhouette": safe_silhouette(D_subset, sp),
                    "cross_algorithm_ari": adjusted_rand_score(km["labels"], sp),
                    "kmedoids_minimum_cluster_size": km_min,
                    "spectral_minimum_cluster_size": sp_min,
                    "minimum_cluster_size_across_algorithms": min(km_min, sp_min),
                    "dominant_single_variable": dominant_variable,
                    "maximum_single_variable_ari": dominance_ari,
                }
                row["mean_source_silhouette"] = np.nanmean([
                    row["kmedoids_silhouette"], row["spectral_silhouette"]
                ])
                row["size_eligible"] = row["minimum_cluster_size_across_algorithms"] >= MIN_PROFILE_SIZE
                row["priority_for_resampling"] = bool(
                    row["size_eligible"]
                    and row["cross_algorithm_ari"] >= 0.60
                    and row["mean_source_silhouette"] >= 0.25
                    and row["maximum_single_variable_ari"] < 0.90
                )
                candidate_rows.append(row)
                candidate_cache[candidate_id] = {
                    "variables": subset,
                    "k": k,
                    "distance": D_subset,
                    "labels": km["labels"],
                }

candidate_screen = pd.DataFrame(candidate_rows)
display(candidate_screen.sort_values(
    ["priority_for_resampling", "cross_algorithm_ari", "mean_source_silhouette"],
    ascending=[False, False, False],
).head(30).round(3))

# %% [markdown]
# ## 4. Shortlist validation with out-of-sample prediction strength

# %%
shortlist_parts = []
for theory_pool, group in candidate_screen.loc[candidate_screen["size_eligible"]].groupby("theory_pool"):
    priority = group.loc[group["priority_for_resampling"]]
    source = priority if not priority.empty else group
    shortlist_parts.append(source.sort_values(
        ["cross_algorithm_ari", "mean_source_silhouette", "maximum_single_variable_ari"],
        ascending=[False, False, True],
    ).head(SHORTLIST_PER_POOL))
shortlist = pd.concat(shortlist_parts, ignore_index=True) if shortlist_parts else pd.DataFrame()


def prediction_strength(candidate, repetitions=PREDICTION_SPLITS):
    distance = candidate["distance"]
    k = candidate["k"]
    n = len(distance)
    train_size = int(np.floor(PREDICTION_TRAIN_FRACTION * n))
    rng = np.random.default_rng(RANDOM_STATE + 40000 + k + len(candidate["variables"]))
    rows = []
    for repetition in range(repetitions):
        train = np.sort(rng.choice(n, size=train_size, replace=False))
        test = np.setdiff1d(np.arange(n), train)
        D_train = distance[np.ix_(train, train)]
        train_fit = fit_kmedoids(
            D_train, k, n_init=50,
            random_state=RANDOM_STATE + 41000 + repetition + 100 * k,
        )
        train_medoids_global = train[train_fit["medoids"]]
        predicted_test = np.argmin(distance[np.ix_(test, train_medoids_global)], axis=1)
        D_test = distance[np.ix_(test, test)]
        independent_test = fit_kmedoids(
            D_test, k, n_init=50,
            random_state=RANDOM_STATE + 42000 + repetition + 100 * k,
        )["labels"]
        cluster_strengths = []
        for cluster in range(k):
            members = np.flatnonzero(predicted_test == cluster)
            if len(members) < 2:
                cluster_strengths.append(0.0)
                continue
            pairs = np.triu_indices(len(members), 1)
            same_independent = (
                independent_test[members][:, None]
                == independent_test[members][None, :]
            )[pairs]
            cluster_strengths.append(float(same_independent.mean()))
        rows.append(min(cluster_strengths))
    return np.asarray(rows)


prediction_rows = []
for row in shortlist.itertuples(index=False):
    strengths = prediction_strength(candidate_cache[int(row.candidate_id)])
    prediction_rows.append({
        "candidate_id": int(row.candidate_id),
        "prediction_strength_mean": float(strengths.mean()),
        "prediction_strength_median": float(np.median(strengths)),
        "prediction_strength_p10": float(np.quantile(strengths, 0.10)),
        "prediction_strength_ge_0_80_percent": 100 * float(np.mean(strengths >= 0.80)),
    })
prediction_results = pd.DataFrame(prediction_rows)
shortlist = shortlist.merge(prediction_results, on="candidate_id", how="left")
display(shortlist.sort_values(
    ["prediction_strength_median", "cross_algorithm_ari", "mean_source_silhouette"],
    ascending=False,
).round(3))

# %% [markdown]
# ## 5. Pool-wise independent-column permutation calibration
#
# For each theory pool, the complete subset-and-k search is repeated after each
# variable is independently permuted. The null statistic is the maximum
# K-medoids silhouette among solutions meeting the same minimum-size rule. This
# accounts for selecting the best result from many combinations within that pool.
# It does not prove construct validity.

# %%
observed_pool_max = candidate_screen.loc[
    candidate_screen["kmedoids_minimum_cluster_size"].ge(MIN_PROFILE_SIZE)
].groupby("theory_pool")["kmedoids_silhouette"].max().to_dict()

null_rng = np.random.default_rng(RANDOM_STATE + 50000)
null_rows = []
for repetition in range(NULL_REPETITIONS):
    permuted = features.copy()
    for column in permuted.columns:
        permuted[column] = permuted[column].iloc[
            null_rng.permutation(len(permuted))
        ].reset_index(drop=True)
    for theory_pool, pool_variables in THEORY_POOLS.items():
        if theory_pool in SKIPPED_RESPONDENT_POOLS:
            continue
        best_null = np.nan
        maximum_size = min(SUBSET_MAX_SIZE, len(pool_variables))
        null_candidate_counter = 0
        for subset_size in range(SUBSET_MIN_SIZE, maximum_size + 1):
            for subset in combinations(pool_variables, subset_size):
                D_null, _ = mixed_gower(permuted, subset)
                for k in range(2, 5):
                    null_candidate_counter += 1
                    null_fit = fit_kmedoids(
                        D_null, k, n_init=12,
                        random_state=RANDOM_STATE + 60000 + 1000 * repetition + null_candidate_counter,
                    )
                    minimum_size = int(pd.Series(null_fit["labels"]).value_counts().min())
                    if minimum_size < MIN_PROFILE_SIZE:
                        continue
                    score = safe_silhouette(D_null, null_fit["labels"])
                    best_null = score if np.isnan(best_null) else max(best_null, score)
        null_rows.append({
            "repetition": repetition + 1,
            "theory_pool": theory_pool,
            "maximum_null_kmedoids_silhouette": best_null,
        })

null_search_results = pd.DataFrame(null_rows)
null_calibration_rows = []
for theory_pool, observed in observed_pool_max.items():
    null_scores = null_search_results.loc[
        null_search_results["theory_pool"].eq(theory_pool),
        "maximum_null_kmedoids_silhouette",
    ].dropna()
    empirical_p = (1 + int((null_scores >= observed).sum())) / (1 + len(null_scores))
    null_calibration_rows.append({
        "theory_pool": theory_pool,
        "observed_maximum_kmedoids_silhouette": observed,
        "null_repetitions_with_valid_solution": len(null_scores),
        "null_maximum_silhouette_median": float(null_scores.median()) if len(null_scores) else np.nan,
        "null_maximum_silhouette_p95": float(null_scores.quantile(0.95)) if len(null_scores) else np.nan,
        "empirical_poolwise_p_value": empirical_p,
        "screening_only_because_null_repetitions_below_200": NULL_REPETITIONS < NULL_FINAL_RECOMMENDATION,
    })
null_calibration = pd.DataFrame(null_calibration_rows)
display(null_calibration.sort_values("empirical_poolwise_p_value").round(4))

shortlist = shortlist.merge(
    null_calibration[[
        "theory_pool", "observed_maximum_kmedoids_silhouette",
        "null_maximum_silhouette_median", "null_maximum_silhouette_p95",
        "empirical_poolwise_p_value",
        "screening_only_because_null_repetitions_below_200",
    ]],
    on="theory_pool", how="left",
)
shortlist["single_item_dominated_at_ari_0_90"] = (
    shortlist["maximum_single_variable_ari"] >= 0.90
)
shortlist["automatic_dimension_confirmation"] = False
shortlist["required_next_gate"] = np.where(
    shortlist["single_item_dominated_at_ari_0_90"],
    "reject single-item-dominated candidate",
    "theory review plus >=200 null repetitions and independent confirmation",
)

# %% [markdown]
# ## 6. Save transparent screening outputs

# %%
fig, axes = plt.subplots(1, 2, figsize=(14, 5.5))
im = axes[0].imshow(full_association, vmin=0, vmax=1, cmap="viridis")
axes[0].set_xticks(range(len(variable_names)), variable_names, rotation=90, fontsize=6)
axes[0].set_yticks(range(len(variable_names)), variable_names, fontsize=6)
axes[0].set_title("Mixed-variable association matrix")
fig.colorbar(im, ax=axes[0], fraction=0.046)
axes[1].plot(
    variable_group_summary["variable_group_count"],
    variable_group_summary["bootstrap_ari_median"], marker="o", label="bootstrap median ARI",
)
axes[1].plot(
    variable_group_summary["variable_group_count"],
    variable_group_summary["ari_with_original_theory_pools"], marker="s", label="ARI with original theory pools",
)
axes[1].axvline(selected_variable_group_count, color="tab:red", linestyle="--", label="descriptive selected q")
axes[1].set(xlabel="Number of variable groups", ylabel="ARI", ylim=(-0.05, 1.05), title="Variable-group stability")
axes[1].legend()
fig.tight_layout()
fig.savefig(OUT / "variable_group_discovery_diagnostics.png", dpi=180, bbox_inches="tight")
plt.show()

encoding_audit.to_csv(OUT / "eligible_variable_encoding_audit.csv", index=False)
pd.DataFrame(full_association, index=variable_names, columns=variable_names).to_csv(
    OUT / "mixed_variable_association_matrix.csv"
)
variable_group_summary.to_csv(OUT / "variable_group_count_stability.csv", index=False)
variable_group_stability.to_csv(OUT / "variable_group_bootstrap_ari.csv", index=False)
variable_group_assignments.to_csv(OUT / "data_driven_variable_group_assignments.csv", index=False)
pd.DataFrame(selected_consensus, index=variable_names, columns=variable_names).to_csv(
    OUT / "selected_variable_group_consensus_matrix.csv"
)
candidate_screen.to_csv(OUT / "all_theory_constrained_subset_candidates.csv", index=False)
shortlist.to_csv(OUT / "shortlisted_candidates_with_all_screening_evidence.csv", index=False)
shortlist.to_csv(OUT / "shortlisted_candidates_with_prediction_strength.csv", index=False)
null_search_results.to_csv(OUT / "poolwise_permutation_null_results.csv", index=False)
null_calibration.to_csv(OUT / "poolwise_null_calibration_summary.csv", index=False)

summary = {
    "cohort": {
        "branch": "F",
        "records": len(cohort),
        "eligible_variables": len(ELIGIBLE_VARIABLES),
        "excluded_non_clustering_variables": int(len(audit) - len(eligible_catalogue)),
    },
    "variable_group_discovery": {
        "bootstrap_repetitions": VARIABLE_GROUP_BOOTSTRAPS,
        "descriptive_selected_group_count": selected_variable_group_count,
        "selection_rule": "highest bootstrap median ARI; descriptive only",
    },
    "respondent_subset_search": {
        "candidate_rows": len(candidate_screen),
        "shortlisted_rows": len(shortlist),
        "subset_sizes": [SUBSET_MIN_SIZE, SUBSET_MAX_SIZE],
        "k_values": [2, 3, 4],
        "skipped_pools": sorted(SKIPPED_RESPONDENT_POOLS),
    },
    "validation": {
        "prediction_splits": PREDICTION_SPLITS,
        "null_repetitions": NULL_REPETITIONS,
        "recommended_null_repetitions_before_thesis_reporting": NULL_FINAL_RECOMMENDATION,
        "pac_policy": "comparative only; no absolute cutoff",
    },
    "interpretation": {
        "automatically_confirmed_dimensions": 0,
        "reason": "statistical screening cannot establish theoretical construct validity",
        "required_next_gate": "review shortlisted variable groups for theoretical coherence before any final clustering",
    },
}
with open(OUT / "candidate_dimension_discovery_summary.json", "w", encoding="utf-8") as handle:
    json.dump(summary, handle, indent=2)
print(json.dumps(summary, indent=2))

# %% [markdown]
# ## Interpretation guardrails
#
# - A high silhouette after searching many combinations is not sufficient.
# - A candidate dominated by one variable is a recoded survey answer, not a
#   multidimensional respondent profile.
# - Permutation calibration addresses chance selection within each theory pool,
#   but does not create theoretical meaning.
# - This screening run uses 30 null repetitions for runtime. Use at least 200
#   before reporting empirical p-values in the thesis.
# - Final dimensions require theory review and ideally confirmation in additional
#   respondents or an independent sample.
