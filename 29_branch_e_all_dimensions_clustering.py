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
OUT = ROOT / "outputs/branch_e_all_dimensions_clusters"
OUT.mkdir(parents=True, exist_ok=True)

RANDOM_STATE = 20260826
MIN_PROFILE_SIZE = 15
SUBSAMPLE_FRACTION = 0.80
CANDIDATE_SUBSAMPLES = 50
CONSENSUS_SUBSAMPLES = 100
ENSEMBLE_BOOTSTRAPS = 100
PERMUTATION_REPETITIONS = 100

DIMENSIONS = {
    "E1": {
        "name": "Job-search psychological readiness and support",
        "sources": [
            "job_search_self_efficacy", "job_search_autonomy_orientation",
            "social_support_job_search", "future_planning_orientation",
        ],
    },
    "E2": {
        "name": "Search intensity and accumulated exposure",
        "sources": [
            "active_search_4weeks", "job_search_duration",
            "num_applications", "num_interviews",
        ],
    },
    "E3": {
        "name": "Economic urgency and job-acceptance constraints",
        "sources": [
            "income_urgency", "job_acceptance_conditions", "has_minimum_wage",
        ],
    },
    "E4": {
        "name": "Education-to-work preparedness and learning orientation",
        "sources": [
            "past_edu_usefulness", "plans_further_edu", "expected_highest_edu_e",
        ],
    },
    "E5": {
        "name": "Household economic resources and dependency",
        "sources": [
            "household_income", "household_size", "household_workers",
            "household_unemployed", "primary_earner_status", "primary_income_source",
        ],
    },
    "E6": {
        "name": "Educational and inherited cultural capital",
        "sources": [
            "father_edu", "mother_edu", "edu_status", "worked_while_studying",
        ],
    },
}

PROFILE_LABELS = {
    "E1": {
        1: "Diagnostic: general-direction and flexible-search pattern",
        2: "Diagnostic: clear-plan and specific-search pattern",
    },
    "E2": {
        1: "Diagnostic: active search in the past four weeks",
        2: "Diagnostic: no active search in the past four weeks",
    },
    "E3": {
        1: "Diagnostic: stated minimum-wage boundary",
        2: "Diagnostic: no stated minimum-wage boundary",
    },
    "E4": {
        1: "High perceived education utility and strong learning ambition",
        2: "Moderate perceived utility and mixed learning ambition",
    },
    "E5": {
        1: "Diagnostic household-economic response profile 1",
        2: "Diagnostic household-economic response profile 2",
    },
    "E6": {
        1: "Diagnostic: did not work while studying",
        2: "Diagnostic: worked while studying",
    },
}

all_sources = sorted({v for spec in DIMENSIONS.values() for v in spec["sources"]})
admin_columns = [
    "respondent_id", "entry_branch", "branch", "branch_routing_source",
    "branch_path_disagreement", "branch_integrity_issue",
]
values_all = pd.read_csv(VALUES_PATH)
labels_all = pd.read_csv(LABELS_PATH)
strict_mask = (
    values_all["branch"].eq("E")
    & values_all["branch_routing_source"].eq("translated_final_active_branch")
    & ~values_all["branch_integrity_issue"].astype(bool)
)
values = values_all.loc[strict_mask, admin_columns + all_sources].copy()
labels = labels_all.loc[strict_mask, ["respondent_id"] + all_sources].copy()
values = values.rename(columns={v: f"{v}__value" for v in all_sources})
labels = labels.rename(columns={v: f"{v}__response" for v in all_sources})
cohort = values.merge(labels, on="respondent_id", validate="one_to_one")
assert len(cohort) == 34 and cohort["respondent_id"].nunique() == 34
assert cohort["branch"].eq("E").all()


def ordered(column, low, high):
    code = pd.to_numeric(cohort[f"{column}__value"], errors="coerce")
    return code.where(code.between(low, high)).sub(low).div(high - low)


def nominal(column):
    return cohort[f"{column}__value"].astype("string").replace("<NA>", pd.NA)


def build_features(code, raw_counts=False):
    frame = pd.DataFrame(index=cohort.index)
    if code == "E1":
        for column in DIMENSIONS[code]["sources"]:
            frame[column] = ordered(column, 1, 4)
        types = {column: "ordinal" for column in frame}
    elif code == "E2":
        frame["active_search_4weeks"] = cohort[
            "active_search_4weeks__value"
        ].map({"no": 0.0, "yes": 1.0})
        frame["job_search_duration"] = ordered("job_search_duration", 1, 6)
        for column in ["num_applications", "num_interviews"]:
            count = pd.to_numeric(cohort[f"{column}__value"], errors="coerce")
            frame[column] = count if raw_counts else np.log1p(count)
        types = {
            "active_search_4weeks": "binary",
            "job_search_duration": "ordinal",
            "num_applications": "continuous",
            "num_interviews": "continuous",
        }
    elif code == "E3":
        frame["income_urgency"] = ordered("income_urgency", 1, 4)
        frame["job_acceptance_conditions"] = ordered(
            "job_acceptance_conditions", 1, 5
        )
        frame["has_minimum_wage"] = cohort[
            "has_minimum_wage__value"
        ].map({"no": 0.0, "yes": 1.0})
        types = {column: "ordinal" for column in frame}
        types["has_minimum_wage"] = "binary"
    elif code == "E4":
        frame["past_edu_usefulness"] = nominal("past_edu_usefulness")
        frame["plans_further_edu"] = nominal("plans_further_edu")
        frame["expected_highest_edu_e"] = ordered("expected_highest_edu_e", 0, 7)
        types = {
            "past_edu_usefulness": "nominal",
            "plans_further_edu": "nominal",
            "expected_highest_edu_e": "ordinal",
        }
    elif code == "E5":
        size = pd.to_numeric(cohort["household_size__value"], errors="coerce")
        workers = pd.to_numeric(cohort["household_workers__value"], errors="coerce")
        unemployed = pd.to_numeric(
            cohort["household_unemployed__value"], errors="coerce"
        )
        invalid = (
            size.isna() | workers.isna() | unemployed.isna() | size.le(0)
            | workers.lt(0) | unemployed.lt(0) | workers.gt(size)
            | unemployed.gt(size) | (workers + unemployed).gt(size)
        )
        income = pd.to_numeric(cohort["household_income__value"], errors="coerce")
        frame["household_income_position"] = income.where(
            income.between(1, 5)
        ).map({1: 0.0, 2: 0.25, 3: 0.5, 4: 0.75, 5: 1.0})
        frame["household_worker_share"] = (workers / size).where(~invalid)
        frame["household_unemployed_share"] = (unemployed / size).where(~invalid)
        frame["primary_earner_responsibility"] = cohort[
            "primary_earner_status__value"
        ].map({"no": 0.0, "shared": 0.5, "yes": 1.0})
        frame["primary_income_source"] = nominal("primary_income_source")
        types = {
            "household_income_position": "ordinal",
            "household_worker_share": "continuous",
            "household_unemployed_share": "continuous",
            "primary_earner_responsibility": "ordinal",
            "primary_income_source": "nominal",
        }
    elif code == "E6":
        for column in ["father_edu", "mother_edu"]:
            frame[column] = ordered(column, 0, 7)
        frame["edu_status"] = nominal("edu_status")
        frame["worked_while_studying"] = cohort[
            "worked_while_studying__value"
        ].map({"no": 0.0, "yes": 1.0})
        types = {
            "father_edu": "ordinal", "mother_edu": "ordinal",
            "edu_status": "nominal", "worked_while_studying": "binary",
        }
    else:
        raise KeyError(code)
    return frame, types


def mixed_gower(frame, feature_types, columns=None):
    columns = list(frame.columns) if columns is None else list(columns)
    n = len(frame)
    numerator = np.zeros((n, n), dtype=float)
    denominator = np.zeros((n, n), dtype=float)
    for column in columns:
        kind = feature_types[column]
        if kind == "nominal":
            series = frame[column].astype("string")
            observed = series.notna().to_numpy()
            vals = series.fillna("__MISSING__").to_numpy(dtype=str)
            difference = (vals[:, None] != vals[None, :]).astype(float)
        else:
            series = pd.to_numeric(frame[column], errors="coerce")
            observed = series.notna().to_numpy()
            vals = series.fillna(0).to_numpy(dtype=float)
            difference = np.abs(vals[:, None] - vals[None, :])
            if kind == "continuous":
                valid = vals[observed]
                span = float(valid.max() - valid.min()) if len(valid) else 0.0
                difference = difference / span if span else np.zeros_like(difference)
        pair_observed = observed[:, None] & observed[None, :]
        numerator += np.where(pair_observed, difference, 0.0)
        denominator += pair_observed
    distance = np.divide(
        numerator, denominator, out=np.zeros_like(numerator), where=denominator > 0
    )
    np.fill_diagonal(distance, 0.0)
    return distance, denominator


def affinity(distance):
    positive = distance[distance > 0]
    sigma = float(np.median(positive)) if len(positive) else 1.0
    result = np.exp(-(distance ** 2) / (2 * sigma ** 2))
    np.fill_diagonal(result, 1.0)
    return result


def fit_kmedoids(distance, k=2, n_init=150, max_iter=150, random_state=RANDOM_STATE):
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


def medoids_from_labels(distance, labels_k):
    medoids = []
    for cluster in sorted(np.unique(labels_k)):
        members = np.flatnonzero(labels_k == cluster)
        within = distance[np.ix_(members, members)]
        medoids.append(members[np.argmin(within.sum(axis=1))])
    return np.asarray(medoids, dtype=int)


def full_source_solutions(distance, seed):
    km = fit_kmedoids(distance, n_init=400, random_state=seed + 1)
    sp = SpectralClustering(
        n_clusters=2, affinity="precomputed", assign_labels="kmeans",
        n_init=100, random_state=seed + 2,
    ).fit_predict(affinity(distance))
    return km, sp


def subsample_stability(distance, algorithm, reference_labels, seed):
    rng = np.random.default_rng(seed)
    sample_size = int(np.floor(SUBSAMPLE_FRACTION * len(distance)))
    scores = []
    for repetition in range(CANDIDATE_SUBSAMPLES):
        idx = np.sort(rng.choice(len(distance), size=sample_size, replace=False))
        sub = distance[np.ix_(idx, idx)]
        if algorithm == "kmedoids":
            fit = fit_kmedoids(sub, n_init=60, random_state=seed + 1000 + repetition)
            medoids = idx[fit["medoids"]]
        else:
            labels_sub = SpectralClustering(
                n_clusters=2, affinity="precomputed", assign_labels="kmeans",
                n_init=30, random_state=seed + 2000 + repetition,
            ).fit_predict(affinity(sub))
            medoids = idx[medoids_from_labels(sub, labels_sub)]
        predicted = np.argmin(distance[:, medoids], axis=1)
        scores.append(adjusted_rand_score(reference_labels, predicted))
    return np.asarray(scores)


def analyse_dimension(code, specification):
    seed = RANDOM_STATE + 100000 * int(code[1:])
    dimension_out = OUT / code.lower()
    dimension_out.mkdir(parents=True, exist_ok=True)
    features, feature_types = build_features(code)
    distance, pair_coverage = mixed_gower(features, feature_types)
    km, sp = full_source_solutions(distance, seed)
    km_stability = subsample_stability(distance, "kmedoids", km["labels"], seed + 10)
    sp_stability = subsample_stability(distance, "spectral", sp, seed + 20)
    source_minimum_size = min(
        int(pd.Series(km["labels"]).value_counts().min()),
        int(pd.Series(sp).value_counts().min()),
    )
    source_size_eligible = source_minimum_size >= MIN_PROFILE_SIZE

    rng = np.random.default_rng(seed + 30000)
    n = len(distance)
    sample_size = int(np.floor(SUBSAMPLE_FRACTION * n))
    covers, sames, base_rows = [], [], []
    for repetition in range(CONSENSUS_SUBSAMPLES):
        idx = np.sort(rng.choice(n, size=sample_size, replace=False))
        sub = distance[np.ix_(idx, idx)]
        cover = np.zeros((n, n), dtype=np.uint8)
        cover[np.ix_(idx, idx)] = 1
        km_sub = fit_kmedoids(
            sub, n_init=80, random_state=seed + 40000 + repetition
        )["labels"]
        sp_sub = SpectralClustering(
            n_clusters=2, affinity="precomputed", assign_labels="kmeans",
            n_init=30, random_state=seed + 50000 + repetition,
        ).fit_predict(affinity(sub))
        for algorithm, labels_sub in [("kmedoids", km_sub), ("spectral", sp_sub)]:
            same = np.zeros((n, n), dtype=np.uint8)
            same[np.ix_(idx, idx)] = (
                labels_sub[:, None] == labels_sub[None, :]
            ).astype(np.uint8)
            covers.append(cover.copy())
            sames.append(same)
            base_rows.append({
                "partition_id": len(base_rows) + 1,
                "algorithm": algorithm,
                "repetition": repetition + 1,
                "silhouette": silhouette_score(sub, labels_sub, metric="precomputed"),
                "minimum_cluster_size": int(pd.Series(labels_sub).value_counts().min()),
            })
    cover_stack = np.stack(covers)
    same_stack = np.stack(sames)
    consensus = np.divide(
        same_stack.sum(axis=0), cover_stack.sum(axis=0),
        out=np.zeros((n, n), dtype=float), where=cover_stack.sum(axis=0) > 0,
    )
    np.fill_diagonal(consensus, 1.0)
    consensus_distance = 1 - consensus
    np.fill_diagonal(consensus_distance, 0.0)
    final_raw = fit_kmedoids(
        consensus_distance, n_init=500, random_state=seed + 60000
    )["labels"]
    order = sorted(
        np.unique(final_raw),
        key=lambda cluster: (-int(np.sum(final_raw == cluster)), int(cluster)),
    )
    mapping = {int(raw): i + 1 for i, raw in enumerate(order)}
    profile_id = np.asarray([mapping[int(raw)] for raw in final_raw])

    assignments = cohort[admin_columns].copy()
    for variable in specification["sources"]:
        assignments[f"{variable}__value"] = cohort[f"{variable}__value"]
        assignments[f"{variable}__response"] = cohort[f"{variable}__response"]
    for feature in features:
        assignments[feature] = features[feature]
    assignments["profile_id"] = profile_id
    assignments["profile_label"] = assignments["profile_id"].map(
        PROFILE_LABELS[code]
    )
    assignments["gower_individual_silhouette"] = silhouette_samples(
        distance, profile_id, metric="precomputed"
    )
    assignments["consensus_individual_silhouette"] = silhouette_samples(
        consensus_distance, profile_id, metric="precomputed"
    )

    confidence_rows = []
    for i in range(n):
        own = profile_id[i]
        own_members = np.flatnonzero(profile_id == own)
        own_members = own_members[own_members != i]
        within = float(consensus[i, own_members].mean()) if len(own_members) else 1.0
        other_members = np.flatnonzero(profile_id != own)
        other = float(consensus[i, other_members].mean())
        confidence_rows.append({
            "respondent_id": cohort.iloc[i]["respondent_id"],
            "within_profile_consensus": within,
            "strongest_other_profile_consensus": other,
            "consensus_margin": within - other,
            "ambiguous_consensus_membership": (
                within < 0.70 or (within - other) < 0.20
            ),
        })
    confidence = pd.DataFrame(confidence_rows)
    assignments = assignments.merge(confidence, on="respondent_id", validate="one_to_one")

    response_rows = []
    for variable in specification["sources"]:
        response_col = f"{variable}__response"
        table = (
            assignments.groupby(["profile_id", response_col], dropna=False)
            .size().rename("records").reset_index()
        )
        table["within_profile_percent"] = (
            100 * table["records"]
            / table.groupby("profile_id")["records"].transform("sum")
        )
        table = table.rename(columns={response_col: "response"})
        table.insert(1, "variable", variable)
        response_rows.append(table)
    response_distributions = pd.concat(response_rows, ignore_index=True)
    profile_modes = (
        response_distributions.sort_values(
            ["profile_id", "variable", "within_profile_percent"],
            ascending=[True, True, False],
        ).groupby(["profile_id", "variable"], as_index=False).first()
    )
    profile_sizes = (
        assignments.groupby(["profile_id", "profile_label"], as_index=False)
        .agg(
            records=("respondent_id", "size"),
            mean_gower_silhouette=("gower_individual_silhouette", "mean"),
            mean_consensus_silhouette=("consensus_individual_silhouette", "mean"),
        )
    )
    profile_sizes["percent"] = 100 * profile_sizes["records"] / n

    sensitivity_rows, dominance_rows = [], []
    for feature in features:
        retained = [column for column in features if column != feature]
        reduced, reduced_coverage = mixed_gower(features, feature_types, retained)
        reduced_labels = fit_kmedoids(
            reduced, n_init=300, random_state=seed + 70000 + list(features).index(feature)
        )["labels"]
        sensitivity_rows.append({
            "omitted_feature": feature,
            "minimum_pair_coverage": int(reduced_coverage.min()),
            "silhouette_reduced": silhouette_score(
                reduced, reduced_labels, metric="precomputed"
            ),
            "ari_reduced_vs_final": adjusted_rand_score(profile_id, reduced_labels),
        })
        single, _ = mixed_gower(features, feature_types, [feature])
        single_labels = fit_kmedoids(
            single, n_init=300, random_state=seed + 71000 + list(features).index(feature)
        )["labels"]
        dominance_rows.append({
            "single_feature": feature,
            "ari_single_feature_vs_final": adjusted_rand_score(
                profile_id, single_labels
            ),
        })
    sensitivity = pd.DataFrame(sensitivity_rows)
    dominance = pd.DataFrame(dominance_rows)

    bootstrap_rng = np.random.default_rng(seed + 72000)
    bootstrap_rows = []
    for repetition in range(ENSEMBLE_BOOTSTRAPS):
        chosen = bootstrap_rng.choice(len(cover_stack), size=len(cover_stack), replace=True)
        boot_cover = cover_stack[chosen].sum(axis=0)
        boot_same = same_stack[chosen].sum(axis=0)
        boot_consensus = np.divide(
            boot_same, boot_cover, out=np.zeros_like(boot_same, dtype=float),
            where=boot_cover > 0,
        )
        np.fill_diagonal(boot_consensus, 1.0)
        boot_distance = 1 - boot_consensus
        np.fill_diagonal(boot_distance, 0.0)
        boot_labels = fit_kmedoids(
            boot_distance, n_init=80, random_state=seed + 73000 + repetition
        )["labels"]
        bootstrap_rows.append({
            "repetition": repetition + 1,
            "ari_vs_final": adjusted_rand_score(profile_id, boot_labels),
        })
    bootstrap = pd.DataFrame(bootstrap_rows)

    permutation_rng = np.random.default_rng(seed + 80000)
    permutation_rows = []
    for repetition in range(PERMUTATION_REPETITIONS):
        shuffled = features.copy()
        for feature in features:
            shuffled[feature] = permutation_rng.permutation(
                shuffled[feature].to_numpy()
            )
        null_distance, _ = mixed_gower(shuffled, feature_types)
        null_labels = fit_kmedoids(
            null_distance, n_init=100, random_state=seed + 81000 + repetition
        )["labels"]
        minimum_size = int(pd.Series(null_labels).value_counts().min())
        permutation_rows.append({
            "repetition": repetition + 1,
            "minimum_cluster_size": minimum_size,
            "silhouette_if_size_eligible": (
                silhouette_score(null_distance, null_labels, metric="precomputed")
                if minimum_size >= MIN_PROFILE_SIZE else np.nan
            ),
        })
    permutation = pd.DataFrame(permutation_rows)
    valid_null = permutation["silhouette_if_size_eligible"].dropna()
    observed_km_silhouette = silhouette_score(
        distance, km["labels"], metric="precomputed"
    )
    empirical_p = (
        float((1 + (valid_null >= observed_km_silhouette).sum()) / (1 + len(valid_null)))
        if len(valid_null) else np.nan
    )

    encoding_sensitivity_ari = None
    if code == "E2":
        raw_features, raw_types = build_features("E2", raw_counts=True)
        raw_distance, _ = mixed_gower(raw_features, raw_types)
        raw_km, raw_sp = full_source_solutions(raw_distance, seed + 90000)
        encoding_sensitivity_ari = min(
            adjusted_rand_score(profile_id, raw_km["labels"]),
            adjusted_rand_score(profile_id, raw_sp),
        )

    structural_sensitivity_ari = None
    if code == "E5":
        structural = [
            "household_income_position", "household_worker_share",
            "household_unemployed_share",
        ]
        structural_distance, _ = mixed_gower(features, feature_types, structural)
        structural_labels = fit_kmedoids(
            structural_distance, n_init=400, random_state=seed + 91000
        )["labels"]
        structural_sensitivity_ari = adjusted_rand_score(
            profile_id, structural_labels
        )

    upper = consensus[np.triu_indices(n, 1)]
    metrics = {
        "gower_silhouette": float(silhouette_score(distance, profile_id, metric="precomputed")),
        "consensus_silhouette": float(silhouette_score(consensus_distance, profile_id, metric="precomputed")),
        "source_minimum_cluster_size": source_minimum_size,
        "final_minimum_cluster_size": int(pd.Series(profile_id).value_counts().min()),
        "kmedoids_subsample_stability_mean": float(km_stability.mean()),
        "spectral_subsample_stability_mean": float(sp_stability.mean()),
        "ensemble_bootstrap_ari_mean": float(bootstrap["ari_vs_final"].mean()),
        "ensemble_bootstrap_ari_p10": float(bootstrap["ari_vs_final"].quantile(0.10)),
        "ari_vs_full_kmedoids": float(adjusted_rand_score(profile_id, km["labels"])),
        "ari_vs_full_spectral": float(adjusted_rand_score(profile_id, sp)),
        "maximum_single_feature_ari": float(dominance["ari_single_feature_vs_final"].max()),
        "dominant_single_feature": str(dominance.sort_values("ari_single_feature_vs_final", ascending=False).iloc[0]["single_feature"]),
        "minimum_leave_one_feature_out_ari": float(sensitivity["ari_reduced_vs_final"].min()),
        "ambiguous_consensus_percent": 100 * float(assignments["ambiguous_consensus_membership"].mean()),
        "low_gower_confidence_percent": 100 * float(np.mean(assignments["gower_individual_silhouette"] < 0.10)),
        "pac_10_90": float(np.mean((upper > 0.10) & (upper < 0.90))),
        "permutation_valid_repetitions": int(len(valid_null)),
        "permutation_null_p95": float(valid_null.quantile(0.95)) if len(valid_null) else None,
        "empirical_permutation_p": empirical_p,
        "raw_vs_log_count_encoding_minimum_ari": encoding_sensitivity_ari,
        "structural_resource_only_ari": structural_sensitivity_ari,
    }
    checks = [
        ("cross-algorithm source minimum size >= 15", source_size_eligible),
        ("Gower silhouette >= 0.25", metrics["gower_silhouette"] >= 0.25),
        ("ensemble bootstrap mean ARI >= 0.80", metrics["ensemble_bootstrap_ari_mean"] >= 0.80),
        ("final minimum profile size >= 15", metrics["final_minimum_cluster_size"] >= 15),
        ("ARI with full K-medoids >= 0.60", metrics["ari_vs_full_kmedoids"] >= 0.60),
        ("ARI with full spectral >= 0.60", metrics["ari_vs_full_spectral"] >= 0.60),
        ("maximum single-feature ARI < 0.90", metrics["maximum_single_feature_ari"] < 0.90),
        ("permutation p < 0.05", pd.notna(empirical_p) and empirical_p < 0.05),
        ("ambiguous consensus <= 20%", metrics["ambiguous_consensus_percent"] <= 20),
        ("low Gower confidence <= 20%", metrics["low_gower_confidence_percent"] <= 20),
    ]
    if code == "E2":
        checks.append(("raw-vs-log count encoding ARI >= 0.60", encoding_sensitivity_ari >= 0.60))
    quality = pd.DataFrame([
        {"check": name, "passed": bool(passed)} for name, passed in checks
    ])
    automatic_pass = bool(quality["passed"].all())
    if automatic_pass and metrics["minimum_leave_one_feature_out_ari"] < 0.10:
        final_decision = "retain_cautiously_feature_dependent"
    elif automatic_pass:
        final_decision = "retain_cautiously"
    else:
        final_decision = "reject"

    # Two-dimensional classical MDS is for display only.
    J = np.eye(n) - np.ones((n, n)) / n
    B = -0.5 * J @ (distance ** 2) @ J
    eigenvalues, eigenvectors = np.linalg.eigh(B)
    order_eigen = np.argsort(eigenvalues)[::-1]
    positive = order_eigen[eigenvalues[order_eigen] > 0][:2]
    coordinates = eigenvectors[:, positive] * np.sqrt(eigenvalues[positive])
    fig, ax = plt.subplots(figsize=(8, 6))
    for profile in sorted(np.unique(profile_id)):
        mask = profile_id == profile
        ax.scatter(
            coordinates[mask, 0], coordinates[mask, 1], s=42, alpha=0.75,
            edgecolor="white", linewidth=0.4, label=PROFILE_LABELS[code][int(profile)],
        )
    ax.set(
        title=f"Branch E {code}: {specification['name']}",
        xlabel="Classical MDS axis 1 (display coordinate only)",
        ylabel="Classical MDS axis 2 (display coordinate only)",
    )
    ax.legend()
    fig.tight_layout()
    fig.savefig(dimension_out / "profile_scatterplot.png", dpi=180, bbox_inches="tight")
    plt.close(fig)

    assignments.to_csv(dimension_out / "consensus_assignments.csv", index=False)
    profile_sizes.to_csv(dimension_out / "profile_sizes.csv", index=False)
    response_distributions.to_csv(dimension_out / "profile_response_distributions.csv", index=False)
    profile_modes.to_csv(dimension_out / "profile_modes.csv", index=False)
    sensitivity.to_csv(dimension_out / "leave_one_feature_out.csv", index=False)
    dominance.to_csv(dimension_out / "single_feature_dominance.csv", index=False)
    bootstrap.to_csv(dimension_out / "ensemble_bootstrap_stability.csv", index=False)
    permutation.to_csv(dimension_out / "permutation_null.csv", index=False)
    pd.DataFrame(base_rows).to_csv(dimension_out / "consensus_base_partitions.csv", index=False)
    quality.to_csv(dimension_out / "quality_checks.csv", index=False)

    summary = {
        "dimension_code": code,
        "dimension_name": specification["name"],
        "records": n,
        "source_variables": specification["sources"],
        "clustering_features": list(features),
        "feature_types": feature_types,
        "profile_sizes": {
            str(int(row.profile_id)): int(row.records) for row in profile_sizes.itertuples()
        },
        "profile_labels": {str(key): value for key, value in PROFILE_LABELS[code].items()},
        "profile_modes": profile_modes.to_dict(orient="records"),
        "metrics": metrics,
        "automatic_screen_pass": automatic_pass,
        "checks_passed": int(quality["passed"].sum()),
        "checks_total": int(len(quality)),
        "decision": final_decision,
        "limitations": [
            "Branch E contains only 34 strict respondents, so only k=2 can satisfy the minimum profile size of 15.",
            "No dimension score or psychometric scale is constructed.",
            "PAC is reported descriptively because there is only one eligible candidate k.",
            "Automatic screening does not replace single-feature and leave-one-feature-out substantive review.",
            "A retained result with leave-one-feature-out ARI below 0.10 is explicitly marked feature-dependent and must be interpreted around its central indicator rather than as a broad latent scale.",
        ],
    }
    with open(dimension_out / "clustering_summary.json", "w", encoding="utf-8") as handle:
        json.dump(summary, handle, indent=2)
    return summary


summaries = []
for dimension_code, dimension_specification in DIMENSIONS.items():
    print(f"Running {dimension_code}: {dimension_specification['name']}")
    summaries.append(analyse_dimension(dimension_code, dimension_specification))

decision_table = pd.DataFrame([
    {
        "dimension_code": item["dimension_code"],
        "dimension_name": item["dimension_name"],
        "profile_sizes": "/".join(str(v) for v in item["profile_sizes"].values()),
        "gower_silhouette": item["metrics"]["gower_silhouette"],
        "ensemble_bootstrap_ari_mean": item["metrics"]["ensemble_bootstrap_ari_mean"],
        "ari_vs_full_kmedoids": item["metrics"]["ari_vs_full_kmedoids"],
        "ari_vs_full_spectral": item["metrics"]["ari_vs_full_spectral"],
        "maximum_single_feature_ari": item["metrics"]["maximum_single_feature_ari"],
        "minimum_leave_one_feature_out_ari": item["metrics"]["minimum_leave_one_feature_out_ari"],
        "permutation_p": item["metrics"]["empirical_permutation_p"],
        "checks_passed": item["checks_passed"],
        "checks_total": item["checks_total"],
        "automatic_screen_pass": item["automatic_screen_pass"],
        "final_decision": item["decision"],
    }
    for item in summaries
])
decision_table.to_csv(OUT / "branch_e_all_dimension_screening_summary.csv", index=False)
with open(OUT / "branch_e_all_dimension_summaries.json", "w", encoding="utf-8") as handle:
    json.dump(summaries, handle, indent=2)

print("\nBranch E dimension screening summary:\n")
print(decision_table.round(3).to_string(index=False))
print("\nSaved outputs to", OUT)
