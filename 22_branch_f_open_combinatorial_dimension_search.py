# %% [markdown]
# # Branch F — open combinatorial dimension search (atheoretical screen)
#
# `20_branch_f_candidate_dimension_discovery.py` searched subsets **inside**
# the nine pre-specified theory pools (D1–D9). This script removes that
# constraint: it pools every variable that is (a) answerable by essentially
# the whole strict Branch F cohort and (b) not circular with branch/subgroup
# membership, then searches combinations **across pool boundaries** — e.g. a
# household-income variable paired with a job-satisfaction variable, which
# the theory-constrained script would never try.
#
# This is deliberately atheoretical. That is the point (the user asked for
# "any possible dimension using any possible variable combination"), but it
# means the guardrails matter more here than anywhere else in the project:
#
# 1. No result from this script is a "dimension" on its own. It is a lead.
# 2. Every eligible variable pair/subset is tested — including combinations
#    that mix unrelated theoretical mechanisms. A cluster that requires
#    incoherent variables to look stable is not more credible than one that
#    requires only coherent ones; it is just a bigger haystack.
# 3. Because the search space is combinatorially large, subset sizes 2 and 3
#    are enumerated exhaustively, but size 4 is a *budgeted random sample*,
#    not exhaustive — this is disclosed in every output file, not just here.
# 4. The single-item-dominance check that split D4 from D5/D6 in the
#    theory-constrained work is applied identically to every candidate here,
#    with the same threshold, decided before results are seen.
# 5. The null comparison is an *omnibus* permutation null (the best result
#    the same search procedure finds on independently shuffled columns),
#    because pool-wise calibration doesn't mean anything once there are no
#    pools. This is the single most important number this script produces.
#
# Anything shortlisted here still needs: theoretical grounding, a redundancy
# check against retained D3 and the excluded D4 diagnostic, and >=200 omnibus null
# repetitions (this script defaults to a much smaller screening number) before
# it is reported as more than a hypothesis to review with a supervisor.

# %%
from pathlib import Path
from itertools import combinations
import json
import time
import warnings

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
AUDIT_PATH = ROOT / "outputs/branch_f_variable_dimension_audit/branch_f_all_105_variables.csv"
OUT = ROOT / "outputs/branch_f_open_dimension_search"
OUT.mkdir(parents=True, exist_ok=True)

RANDOM_STATE = 20260825
MIN_PROFILE_SIZE = 15          # same floor used throughout the project
COVERAGE_THRESHOLD = 95.0      # % of the 81 respondents that must have an answer
DOMINANCE_ARI_REJECT = 0.90    # same rule that split D4 from D5/D6 — fixed in advance

# --- runtime controls -------------------------------------------------------
# QUICK_MODE runs a small, fast pass so you can confirm the script works end
# to end before committing to the full search (which can run for a while —
# see the printed runtime estimate below). Set QUICK_MODE = False for a real
# screening run, and raise NULL_REPETITIONS toward 200 before treating any
# p-value here as final, exactly as the rest of this project already does.
QUICK_MODE = False

SUBSET_MIN_SIZE = 2
SUBSET_MAX_SIZE = 4
# A subset size is enumerated EXHAUSTIVELY only while the number of possible
# subsets at that size is <= EXHAUSTIVE_SIZE_LIMIT; above that it falls back
# to a random budgeted sample of RANDOM_SUBSETS_PER_LARGER_SIZE. This is
# decided per-size at runtime from the actual pool size (see iter_subsets),
# not from a fixed size cutoff — with ~55-60 eligible variables, C(pool,2)
# stays exhaustive but C(pool,3) (~30,000+) does not unless the limit is
# raised, which is exactly the QUICK_MODE / full-run difference below.
EXHAUSTIVE_SIZE_LIMIT = 2_500 if QUICK_MODE else 45_000
RANDOM_SUBSETS_PER_LARGER_SIZE = 150 if QUICK_MODE else 4000
SCREEN_KMEDOIDS_N_INIT = 6 if QUICK_MODE else 15
CONFIRM_KMEDOIDS_N_INIT = 30 if QUICK_MODE else 70
SHORTLIST_SIZE = 15 if QUICK_MODE else 40
BOOTSTRAP_STABILITY_REPS = 15 if QUICK_MODE else 60
NULL_REPETITIONS = 2 if QUICK_MODE else 8
NULL_FINAL_RECOMMENDATION = 200
REDUNDANCY_ASSOCIATION_FLAG = 0.85

# %% [markdown]
# ## 1. Rebuild the strict Branch F cohort (identical filter to the rest of
# the project — same 81 respondents used throughout).

# %%
values_all = pd.read_csv(VALUES_PATH)
labels_all = pd.read_csv(LABELS_PATH)
strict_mask = (
    values_all["branch"].eq("F")
    & values_all["branch_routing_source"].eq("translated_final_active_branch")
    & ~values_all["branch_integrity_issue"].astype(bool)
    & values_all["employment_status"].notna()
)
n_cohort = int(strict_mask.sum())
assert n_cohort == 81, f"expected 81 strict Branch F respondents, found {n_cohort}"

# %% [markdown]
# ## 2. Build the eligible variable pool from scratch — not just the 34
# theory-approved inputs. Eligibility is a data-quality/circularity gate,
# not a theory gate: that is what makes this an *open* search.
#
# Included roles: `proposed clustering input` (the 34 already audited),
# `profile/programme-mapping descriptor`, and `validation/profile descriptor`
# — but only when >=95% of the 81 respondents actually answered the question.
# That threshold alone excludes every conditional descriptor and both
# subgroup-only pools (wage-worker: 86.4% coverage; self-employed: 13.6%),
# because none of them clear 95% in this cohort. It's a data-driven exclusion,
# not a hand-picked one.
#
# Two variables are excluded by name despite high coverage, both for
# documented circularity reasons already established in the project:
# - `employment_status` ("how do you usually work") *is* the question that
#   defines the wage-worker/self-employed split the report already found
#   couldn't be pooled (70 vs 11). Clustering on it just reproduces that
#   split under a new name.
# - `current_activity_status` / `has_job_to_return` are routing/audit
#   fields, not substantive answers.

# %%
audit = pd.read_csv(AUDIT_PATH)
OPEN_SEARCH_ROLES = {
    "proposed clustering input",
    "profile/programme-mapping descriptor",
    "validation/profile descriptor",
}
CIRCULAR_EXCLUSIONS = {"employment_status", "current_activity_status", "has_job_to_return"}

role_eligible = audit.loc[
    audit["proposed_role"].isin(OPEN_SEARCH_ROLES)
    & audit["coverage_percent"].ge(COVERAGE_THRESHOLD)
    & ~audit["variable"].isin(CIRCULAR_EXCLUSIONS)
].copy()

# Ordinal variables whose numeric code needs a variable-specific fix before
# it can be treated as a distance. Both cases were checked directly against
# the labelled response text — never assumed from the raw code alone.
LABEL_ORDER_OVERRIDES = {
    # age_group's stored value is a text band ("18-21", ...), not a number.
    "age_group": {"18-21": 1, "22-25": 2, "26-29": 3, "30-35": 4},
}
# edu_min_for_decent_job uses 99 as a "doesn't matter" catch-all, not the top
# of the education scale — including it as 99 would wreck the [0,1] rescale.
SENTINEL_AS_MISSING = {
    "edu_min_for_decent_job": {99, 99.0},
}

# Explicit type calls for every non-theory-pool variable added to the pool.
# willing_to_relocate_f looks ordinal (1-4 = increasing distance) but option
# 5 is "no strong preference", which is not further along that scale — it's
# a different kind of answer. Coding it as ordinal 1-5 would misrepresent it,
# so it is treated as nominal instead. occupational_class and
# enterprise_location_type have no natural order and are nominal too.
EXTRA_TYPE_SPEC = {
    "age_group": "ordinal",
    "gender": "nominal",
    "district": "nominal",
    "area_type": "nominal",
    "moved_from_origin": "nominal",
    "marital_status": "nominal",
    "has_children": "nominal",
    "father_occ": "nominal",
    "mother_occ": "nominal",
    "edu_min_for_decent_job": "ordinal",
    "most_important_life_goal": "nominal",
    "most_useful_quality_for_job": "nominal",
    "ideal_work_type": "nominal",
    "ideal_sector": "nominal",
    "enterprise_location_type": "nominal",
    "enterprise_registered": "nominal",
    "paid_taxes": "nominal",
    "occupational_class": "nominal",
    "has_second_job": "nominal",
    "actual_hours_last_week": "continuous",
    "hours_below_normal": "nominal",
    "willing_to_relocate_f": "nominal",
    "plans_further_edu_f": "nominal",
    "union_member": "nominal",
    "ever_refused_job_f": "nominal",
    "acceptance_conditions_search": "ordinal",
    "had_min_wage_during_search": "nominal",
}
THEORY_TYPE_SPEC = {
    "household_income": "ordinal", "household_size": "continuous",
    "household_workers": "continuous", "household_unemployed": "continuous",
    "primary_earner_status": "nominal", "primary_income_source": "nominal",
    "father_edu": "ordinal", "mother_edu": "ordinal", "edu_status": "nominal",
    "worked_while_studying": "nominal", "sector_formality": "ordinal",
    "contract_type": "nominal", "job_security_12months": "ordinal",
    "usual_hours_per_week": "continuous", "income_hours_preference": "nominal",
    "monthly_income_band": "ordinal", "contract_satisfaction": "nominal",
    "job_satisfaction": "ordinal", "hopes_to_change_job": "nominal",
    "qualification_job_match": "ordinal", "received_training": "nominal",
    "past_edu_useful_for_job": "ordinal", "employment_network_quality": "ordinal",
    "professional_network_growth": "ordinal", "work_autonomy": "ordinal",
    "competence_growth_at_work": "ordinal", "relatedness_at_work": "ordinal",
    "work_motivation_type": "ordinal", "registered_as_jobseeker": "nominal",
    "employment_service_help_f": "nominal", "jobs_applied_before_hire": "continuous",
    "interviews_before_hire": "continuous", "search_duration_before_hire": "ordinal",
    "obstacle_finding_this_job": "nominal",
}
TYPE_SPEC = {**THEORY_TYPE_SPEC, **EXTRA_TYPE_SPEC}

candidate_pool = [v for v in role_eligible["variable"] if v in TYPE_SPEC]
missing_type = sorted(set(role_eligible["variable"]) - set(TYPE_SPEC))
if missing_type:
    raise ValueError(f"No type assigned for eligible variables: {missing_type}")

excluded_log = pd.concat([
    audit.loc[~audit["proposed_role"].isin(OPEN_SEARCH_ROLES), ["variable", "proposed_role", "coverage_percent"]]
    .assign(exclusion_reason="role not in scope of this open search"),
    audit.loc[
        audit["proposed_role"].isin(OPEN_SEARCH_ROLES)
        & audit["coverage_percent"].lt(COVERAGE_THRESHOLD),
        ["variable", "proposed_role", "coverage_percent"],
    ].assign(exclusion_reason=f"coverage below {COVERAGE_THRESHOLD}% of the strict cohort"),
    audit.loc[audit["variable"].isin(CIRCULAR_EXCLUSIONS), ["variable", "proposed_role", "coverage_percent"]]
    .assign(exclusion_reason="circular with branch/subgroup membership"),
], ignore_index=True).drop_duplicates(subset="variable")

# %%
values = values_all.loc[strict_mask, ["respondent_id"] + candidate_pool].reset_index(drop=True)
labels = labels_all.loc[strict_mask, ["respondent_id"] + candidate_pool].reset_index(drop=True)

features = pd.DataFrame(index=values.index)
encoding_rows = []
for variable in candidate_pool:
    vtype = TYPE_SPEC[variable]
    response = labels[variable].astype("string")
    raw = values[variable]

    if variable in LABEL_ORDER_OVERRIDES:
        encoded = raw.map(LABEL_ORDER_OVERRIDES[variable]).astype(float)
    else:
        encoded = pd.to_numeric(raw, errors="coerce")

    if variable in SENTINEL_AS_MISSING:
        encoded = encoded.mask(encoded.isin(SENTINEL_AS_MISSING[variable]))

    if vtype == "nominal":
        encoded = response  # nominal distance compares the raw category label
    elif vtype == "ordinal":
        unknown = response.str.lower().str.contains(
            r"do not know|don't know|prefer not|not sure", regex=True, na=False
        )
        encoded = encoded.mask(unknown)
        observed = encoded.dropna()
        span = float(observed.max() - observed.min()) if len(observed) else 0.0
        encoded = (encoded - observed.min()) / span if span else encoded * 0
    else:  # continuous
        encoded = encoded.where(encoded.ge(0))

    features[variable] = encoded
    encoding_rows.append({
        "variable": variable,
        "type": vtype,
        "observed": int(encoded.notna().sum()),
        "unique_encoded": int(encoded.nunique(dropna=True)),
    })

encoding_audit = pd.DataFrame(encoding_rows)
# drop anything that turns out constant/near-empty once encoded on this exact
# cohort, even though the audit file said it was fine — belt and braces.
usable = encoding_audit.loc[
    (encoding_audit["unique_encoded"] >= 2) & (encoding_audit["observed"] >= MIN_PROFILE_SIZE * 2)
]
dropped_after_encoding = sorted(set(candidate_pool) - set(usable["variable"]))
candidate_pool = usable["variable"].tolist()
features = features[candidate_pool]

print(f"Strict Branch F cohort: {n_cohort} respondents")
print(f"Open-search eligible variable pool: {len(candidate_pool)} variables "
      f"(vs. 34 in the theory-constrained script)")
if dropped_after_encoding:
    print(f"Dropped after direct encoding check (constant/too sparse in this cohort): {dropped_after_encoding}")

# %% [markdown]
# ## 3. Distance, clustering and diagnostic primitives
# (Same equal-weight Gower distance, K-medoids and spectral implementations
# already used and reviewed elsewhere in this project — kept identical on
# purpose so results are comparable across scripts.)

# %%
def mixed_gower(frame, columns):
    columns = list(columns)
    n = len(frame)
    numerator = np.zeros((n, n), dtype=float)
    denominator = np.zeros((n, n), dtype=float)
    for column in columns:
        vtype = TYPE_SPEC[column]
        if vtype == "nominal":
            series = frame[column].astype("string")
            observed = series.notna().to_numpy()
            arr = series.fillna("__MISSING__").to_numpy(dtype=str)
            difference = (arr[:, None] != arr[None, :]).astype(float)
        else:
            series = pd.to_numeric(frame[column], errors="coerce")
            observed = series.notna().to_numpy()
            arr = series.fillna(0).to_numpy(dtype=float)
            difference = np.abs(arr[:, None] - arr[None, :])
            if vtype == "continuous":
                valid = arr[observed]
                rng = float(valid.max() - valid.min()) if len(valid) else 0.0
                difference = difference / rng if rng else np.zeros_like(difference)
        pair_observed = observed[:, None] & observed[None, :]
        numerator += np.where(pair_observed, difference, 0.0)
        denominator += pair_observed
    distance = np.divide(numerator, denominator, out=np.zeros_like(numerator), where=denominator > 0)
    np.fill_diagonal(distance, 0.0)
    return distance, denominator


def fit_kmedoids(distance, k, n_init, max_iter=60, random_state=RANDOM_STATE):
    rng = np.random.default_rng(random_state)
    n = len(distance)
    best = None
    for _ in range(n_init):
        medoids = np.sort(rng.choice(n, size=k, replace=False))
        for _ in range(max_iter):
            lab = np.argmin(distance[:, medoids], axis=1)
            updated = medoids.copy()
            for cluster in range(k):
                members = np.flatnonzero(lab == cluster)
                if not len(members):
                    nearest = distance[:, medoids].min(axis=1)
                    avail = np.setdiff1d(np.argsort(nearest)[::-1], updated)
                    updated[cluster] = avail[0]
                else:
                    within = distance[np.ix_(members, members)]
                    updated[cluster] = members[np.argmin(within.sum(axis=1))]
            if np.array_equal(updated, medoids):
                break
            medoids = updated
        lab = np.argmin(distance[:, medoids], axis=1)
        loss = float(distance[np.arange(n), medoids[lab]].sum())
        candidate = (loss, tuple(medoids.tolist()), medoids.copy(), lab.copy())
        if best is None or candidate[:2] < best[:2]:
            best = candidate
    return {"labels": best[3], "medoids": best[2], "loss": best[0]}


def spectral_labels(distance, k, seed):
    positive = distance[distance > 0]
    sigma = float(np.median(positive)) if len(positive) else 1.0
    affinity = np.exp(-(distance ** 2) / (2 * sigma ** 2))
    np.fill_diagonal(affinity, 1.0)
    return SpectralClustering(
        n_clusters=k, affinity="precomputed", assign_labels="kmeans",
        n_init=20, random_state=seed,
    ).fit_predict(affinity)


def safe_silhouette(distance, lab):
    unique = np.unique(lab)
    if len(unique) < 2 or len(unique) >= len(lab):
        return np.nan
    return float(silhouette_score(distance, lab, metric="precomputed"))


def min_cluster_size(lab):
    return int(pd.Series(lab).value_counts().min())

# %% [markdown]
# ## 4. Association matrix (for the redundancy diagnostic only — this does
# not gate what gets searched, it just explains afterward why a candidate
# might look artificially strong).

# %%
from scipy.stats import chi2_contingency, rankdata


def corrected_cramers_v(x, y):
    table = pd.crosstab(x, y)
    n = table.to_numpy().sum()
    if n <= 1 or table.shape[0] < 2 or table.shape[1] < 2:
        return 0.0
    chi2 = chi2_contingency(table, correction=False)[0]
    phi2 = chi2 / n
    r, k = table.shape
    phi2c = max(0.0, phi2 - ((k - 1) * (r - 1)) / (n - 1))
    rc = r - ((r - 1) ** 2) / (n - 1)
    kc = k - ((k - 1) ** 2) / (n - 1)
    denom = min(kc - 1, rc - 1)
    return float(np.sqrt(phi2c / denom)) if denom > 0 else 0.0


def correlation_ratio(categories, numeric):
    frame = pd.DataFrame({"c": categories, "n": numeric}).dropna()
    if frame.empty or frame["c"].nunique() < 2 or frame["n"].nunique() < 2:
        return 0.0
    grand = frame["n"].mean()
    between = sum(len(g) * (g["n"].mean() - grand) ** 2 for _, g in frame.groupby("c", observed=True))
    total = float(((frame["n"] - grand) ** 2).sum())
    return float(np.sqrt(between / total)) if total > 0 else 0.0


def spearman_absolute(x, y):
    frame = pd.DataFrame({"x": pd.to_numeric(x, errors="coerce"), "y": pd.to_numeric(y, errors="coerce")}).dropna()
    if len(frame) < 3 or frame["x"].nunique() < 2 or frame["y"].nunique() < 2:
        return 0.0
    return float(abs(pd.Series(rankdata(frame["x"])).corr(pd.Series(rankdata(frame["y"])))))


def mixed_association(x, y, tx, ty):
    valid = x.notna() & y.notna()
    xv, yv = x.loc[valid], y.loc[valid]
    if tx == "nominal" and ty == "nominal":
        return corrected_cramers_v(xv.astype(str), yv.astype(str))
    if tx == "nominal":
        return correlation_ratio(xv.astype(str), pd.to_numeric(yv, errors="coerce"))
    if ty == "nominal":
        return correlation_ratio(yv.astype(str), pd.to_numeric(xv, errors="coerce"))
    return spearman_absolute(xv, yv)


assoc_cols = list(features.columns)
association = np.eye(len(assoc_cols))
for i, a in enumerate(assoc_cols):
    for j in range(i + 1, len(assoc_cols)):
        b = assoc_cols[j]
        val = mixed_association(features[a], features[b], TYPE_SPEC[a], TYPE_SPEC[b])
        association[i, j] = association[j, i] = np.clip(val, 0, 1)
association_df = pd.DataFrame(association, index=assoc_cols, columns=assoc_cols)

high_assoc_pairs = [
    (assoc_cols[i], assoc_cols[j], round(float(association[i, j]), 3))
    for i in range(len(assoc_cols)) for j in range(i + 1, len(assoc_cols))
    if association[i, j] >= REDUNDANCY_ASSOCIATION_FLAG
]
if high_assoc_pairs:
    print(f"{len(high_assoc_pairs)} variable pair(s) with association >= {REDUNDANCY_ASSOCIATION_FLAG} "
          f"(any candidate using both is likely double-counting one fact):")
    for a, b, v in sorted(high_assoc_pairs, key=lambda r: -r[2])[:20]:
        print(f"  {a} <-> {b}: {v}")

# %% [markdown]
# ## 5. Screening pass — subset sizes 2 and 3 enumerated exhaustively across
# the WHOLE pool (not per theory pool); size 4 is a budgeted random sample.
# This is the "any possible combination" step. It uses a fast, low-n_init
# K-medoids fit only — no spectral clustering yet, no dominance test yet —
# because it has to run once per candidate and the candidate count is large.
# Full validation happens only for the shortlist in the next section.

# %%
from math import comb as n_choose_k


def iter_subsets(pool, min_size, max_size, exhaustive_limit, random_budget, seed):
    rng = np.random.default_rng(seed)
    for size in range(min_size, max_size + 1):
        total_possible = n_choose_k(len(pool), size)
        if total_possible <= exhaustive_limit:
            for subset in combinations(pool, size):
                yield subset
        else:
            seen = set()
            attempts = 0
            target = min(random_budget, total_possible)
            while len(seen) < target and attempts < target * 20:
                attempts += 1
                subset = tuple(sorted(rng.choice(pool, size=size, replace=False).tolist()))
                if subset not in seen:
                    seen.add(subset)
                    yield subset


def subset_size_plan(pool, min_size, max_size, exhaustive_limit, random_budget):
    plan = {}
    for size in range(min_size, max_size + 1):
        total_possible = n_choose_k(len(pool), size)
        if total_possible <= exhaustive_limit:
            plan[size] = ("exhaustive", total_possible)
        else:
            plan[size] = ("random-budgeted", min(random_budget, total_possible))
    return plan


pool_array = np.array(candidate_pool)
size_plan = subset_size_plan(
    candidate_pool, SUBSET_MIN_SIZE, SUBSET_MAX_SIZE, EXHAUSTIVE_SIZE_LIMIT, RANDOM_SUBSETS_PER_LARGER_SIZE
)
est_total = sum(count for _, count in size_plan.values()) * 3  # x3 for k in {2,3,4}
print(f"Eligible variables: {len(candidate_pool)}")
for size, (mode, count) in size_plan.items():
    print(f"  size {size}: {mode} — {count:,} subsets")
print(f"Total screening fits (subset x k): ~{est_total:,} "
      f"(QUICK_MODE={QUICK_MODE}; set QUICK_MODE=False and raise the budgets for a full run)")

screen_rows = []
t0 = time.time()
for idx, subset in enumerate(iter_subsets(
    pool_array, SUBSET_MIN_SIZE, SUBSET_MAX_SIZE, EXHAUSTIVE_SIZE_LIMIT,
    RANDOM_SUBSETS_PER_LARGER_SIZE, RANDOM_STATE + 1,
)):
    D, coverage = mixed_gower(features, subset)
    max_pair_assoc = 0.0
    if len(subset) >= 2:
        idxs = [assoc_cols.index(v) for v in subset]
        max_pair_assoc = float(max(
            association[a, b] for a, b in combinations(idxs, 2)
        ))
    for k in (2, 3, 4):
        km = fit_kmedoids(D, k, n_init=SCREEN_KMEDOIDS_N_INIT,
                           random_state=RANDOM_STATE + 100 * idx + k)
        m_size = min_cluster_size(km["labels"])
        sil = safe_silhouette(D, km["labels"]) if m_size >= 2 else np.nan
        screen_rows.append({
            "variables": " | ".join(subset),
            "variable_count": len(subset),
            "k": k,
            "min_pair_coverage": int(coverage.min()),
            "screen_kmedoids_silhouette": sil,
            "screen_min_cluster_size": m_size,
            "max_pairwise_association_in_subset": round(max_pair_assoc, 3),
            "size_eligible": m_size >= MIN_PROFILE_SIZE,
        })
    if (idx + 1) % 2000 == 0:
        elapsed = time.time() - t0
        print(f"  screened {idx + 1:,} subsets in {elapsed:,.0f}s...")

screen = pd.DataFrame(screen_rows)
print(f"Screening pass complete: {len(screen):,} subset x k combinations "
      f"in {time.time() - t0:,.0f}s")

# %% [markdown]
# ## 6. Shortlist for full validation
#
# Ranked by screening silhouette among size-eligible fits, but candidates
# whose subset is dominated by one near-duplicate pair (max pairwise
# association >= REDUNDANCY_ASSOCIATION_FLAG) are pushed down rather than
# dropped — they are flagged, not hidden, since the confirmation stage's
# leave-one-out test will characterize them properly either way.

# %%
eligible_screen = screen.loc[screen["size_eligible"] & screen["screen_kmedoids_silhouette"].notna()].copy()
eligible_screen = eligible_screen.sort_values(
    ["screen_kmedoids_silhouette", "max_pairwise_association_in_subset"],
    ascending=[False, True],
)
# de-duplicate near-identical variable sets before taking the top N, so the
# shortlist isn't just the same three variables with k swapped five times
seen_variable_sets = set()
shortlist_rows = []
for row in eligible_screen.itertuples(index=False):
    key = row.variables
    if key in seen_variable_sets and len(shortlist_rows) >= SHORTLIST_SIZE:
        continue
    seen_variable_sets.add(key)
    shortlist_rows.append(row._asdict())
    if len(shortlist_rows) >= SHORTLIST_SIZE:
        break
shortlist = pd.DataFrame(shortlist_rows)
print(f"Shortlisted {len(shortlist)} candidates for full validation")

# %% [markdown]
# ## 7. Full validation of the shortlist: high-n_init K-medoids, spectral
# clustering, cross-algorithm ARI, bootstrap subsample stability, and the
# leave-one-feature-out dominance test — the same test, same threshold, that
# distinguished D3/D4 from D5/D6 in the theory-constrained work.

# %%
def single_feature_dominance(subset, k, reference_labels, seed_base):
    scores = []
    for i, column in enumerate(subset):
        D_one, _ = mixed_gower(features, [column])
        one_labels = fit_kmedoids(D_one, k, n_init=25, random_state=seed_base + i)["labels"]
        scores.append((column, adjusted_rand_score(reference_labels, one_labels)))
    return max(scores, key=lambda item: item[1])


def bootstrap_stability(D, subset, k, reps, seed_base):
    n = len(D)
    ref = fit_kmedoids(D, k, n_init=CONFIRM_KMEDOIDS_N_INIT, random_state=seed_base)["labels"]
    rng = np.random.default_rng(seed_base + 777)
    aris = []
    for r in range(reps):
        idx = rng.choice(n, size=int(0.8 * n), replace=False)
        D_sub = D[np.ix_(idx, idx)]
        boot_labels = fit_kmedoids(D_sub, k, n_init=20, random_state=seed_base + 1000 + r)["labels"]
        aris.append(adjusted_rand_score(ref[idx], boot_labels))
    return ref, float(np.mean(aris)), float(np.quantile(aris, 0.10))


confirm_rows = []
for i, row in enumerate(shortlist.itertuples(index=False)):
    subset = row.variables.split(" | ")
    k = int(row.k)
    D, _ = mixed_gower(features, subset)
    seed_base = RANDOM_STATE + 300000 + 97 * i

    km = fit_kmedoids(D, k, n_init=CONFIRM_KMEDOIDS_N_INIT, random_state=seed_base)
    sp = spectral_labels(D, k, seed_base + 1)
    km_min, sp_min = min_cluster_size(km["labels"]), min_cluster_size(sp)
    dom_var, dom_ari = single_feature_dominance(subset, k, km["labels"], seed_base + 2)
    ref_labels, boot_ari_mean, boot_ari_p10 = bootstrap_stability(
        D, subset, k, BOOTSTRAP_STABILITY_REPS, seed_base
    )

    confirm_rows.append({
        "variables": row.variables,
        "variable_count": len(subset),
        "k": k,
        "kmedoids_silhouette": safe_silhouette(D, km["labels"]),
        "spectral_silhouette": safe_silhouette(D, sp),
        "cross_algorithm_ari": adjusted_rand_score(km["labels"], sp),
        "kmedoids_minimum_cluster_size": km_min,
        "spectral_minimum_cluster_size": sp_min,
        "bootstrap_ari_mean": boot_ari_mean,
        "bootstrap_ari_p10": boot_ari_p10,
        "dominant_single_variable": dom_var,
        "single_variable_max_ari": dom_ari,
        "single_item_dominated": dom_ari >= DOMINANCE_ARI_REJECT,
        "max_pairwise_association_in_subset": row.max_pairwise_association_in_subset,
        "near_duplicate_variables_flagged": row.max_pairwise_association_in_subset >= REDUNDANCY_ASSOCIATION_FLAG,
    })

confirmed = pd.DataFrame(confirm_rows)
confirmed["passes_basic_gates"] = (
    (confirmed[["kmedoids_minimum_cluster_size", "spectral_minimum_cluster_size"]].min(axis=1) >= MIN_PROFILE_SIZE)
    & (confirmed["cross_algorithm_ari"] >= 0.60)
    & (confirmed["bootstrap_ari_mean"] >= 0.70)
    & ~confirmed["single_item_dominated"]
)
confirmed = confirmed.sort_values(
    ["passes_basic_gates", "cross_algorithm_ari", "bootstrap_ari_mean"], ascending=False
)
print(confirmed.round(3).to_string(index=False))

# %% [markdown]
# ## 8. Omnibus permutation null
#
# All columns are shuffled independently (destroying every real association
# while preserving each variable's own distribution), then the *entire*
# screening procedure above is repeated on the shuffled data. The best
# size-eligible silhouette found by that repeat is one draw from the null
# distribution of "best result an open search like this finds by construction,
# even with no real structure." The observed best screening silhouette is
# compared against that distribution — this is the number that actually
# answers "did I find something, or did I just search hard enough to find
# noise." NULL_REPETITIONS defaults low here because repeating the full
# screen is expensive; raise it toward 200 (and expect a long run) before
# reporting a p-value from this section anywhere formal.

# %%
observed_best = float(eligible_screen["screen_kmedoids_silhouette"].max()) if len(eligible_screen) else np.nan

null_best_values = []
null_rng = np.random.default_rng(RANDOM_STATE + 900000)
for rep in range(NULL_REPETITIONS):
    permuted = features.copy()
    for col in permuted.columns:
        permuted[col] = permuted[col].iloc[null_rng.permutation(len(permuted))].reset_index(drop=True)

    rep_best = np.nan
    for subset in iter_subsets(
        pool_array, SUBSET_MIN_SIZE, SUBSET_MAX_SIZE, EXHAUSTIVE_SIZE_LIMIT,
        RANDOM_SUBSETS_PER_LARGER_SIZE, RANDOM_STATE + 2000 + rep,
    ):
        D_null, _ = mixed_gower(permuted, subset)
        for k in (2, 3, 4):
            km_null = fit_kmedoids(D_null, k, n_init=max(3, SCREEN_KMEDOIDS_N_INIT // 2),
                                    random_state=RANDOM_STATE + 500000 + rep * 97 + k)
            if min_cluster_size(km_null["labels"]) < MIN_PROFILE_SIZE:
                continue
            s = safe_silhouette(D_null, km_null["labels"])
            rep_best = s if np.isnan(rep_best) else max(rep_best, s)
    null_best_values.append(rep_best)
    print(f"  null repetition {rep + 1}/{NULL_REPETITIONS}: best size-eligible silhouette = {rep_best:.3f}")

null_best_values = pd.Series(null_best_values).dropna()
empirical_p = (
    (1 + int((null_best_values >= observed_best).sum())) / (1 + len(null_best_values))
    if len(null_best_values) else np.nan
)
print(f"\nObserved best-of-search K-medoids silhouette: {observed_best:.3f}")
print(f"Omnibus null (n={len(null_best_values)} reps): median={null_best_values.median():.3f}, "
      f"p95={null_best_values.quantile(0.95):.3f}" if len(null_best_values) else "Omnibus null: no valid reps")
print(f"Empirical omnibus p-value: {empirical_p:.3f} "
      f"(screening-only estimate; NULL_REPETITIONS={NULL_REPETITIONS} << {NULL_FINAL_RECOMMENDATION} recommended)")

# %% [markdown]
# ## 9. Save everything

# %%
excluded_log.to_csv(OUT / "excluded_variables_log.csv", index=False)
encoding_audit.to_csv(OUT / "eligible_variable_encoding_audit.csv", index=False)
association_df.to_csv(OUT / "open_pool_association_matrix.csv")
screen.to_csv(OUT / "all_screened_candidates.csv", index=False)
confirmed.to_csv(OUT / "shortlist_full_validation.csv", index=False)
pd.Series(null_best_values, name="best_size_eligible_silhouette").to_csv(
    OUT / "omnibus_permutation_null_results.csv", index=False
)

summary = {
    "cohort": {"branch": "F", "records": n_cohort},
    "open_search_pool": {
        "eligible_variables": len(candidate_pool),
        "theory_pool_variables_included": 34,
        "descriptor_variables_added": len(candidate_pool) - 34,
        "excluded_variables": len(excluded_log),
    },
    "search": {
        "quick_mode": QUICK_MODE,
        "subset_sizes_searched": [SUBSET_MIN_SIZE, SUBSET_MAX_SIZE],
        "exhaustive_size_limit": EXHAUSTIVE_SIZE_LIMIT,
        "random_budget_for_larger_sizes": RANDOM_SUBSETS_PER_LARGER_SIZE,
        "k_values": [2, 3, 4],
        "total_screened_fits": len(screen),
    },
    "confirmation": {
        "shortlist_size": len(shortlist),
        "passing_all_basic_gates": int(confirmed["passes_basic_gates"].sum()) if len(confirmed) else 0,
        "single_item_dominated_at_ari": DOMINANCE_ARI_REJECT,
        "near_duplicate_flag_threshold": REDUNDANCY_ASSOCIATION_FLAG,
    },
    "omnibus_null": {
        "repetitions_run": int(len(null_best_values)),
        "recommended_before_reporting": NULL_FINAL_RECOMMENDATION,
        "observed_best_silhouette": None if np.isnan(observed_best) else round(observed_best, 4),
        "empirical_p_value": None if np.isnan(empirical_p) else round(float(empirical_p), 4),
    },
    "interpretation": {
        "automatically_confirmed_dimensions": 0,
        "reason": "an atheoretical open search cannot establish construct validity by itself",
        "required_before_reporting_any_result": [
            "theory review: does the surviving variable set map to SWTS/Bourdieu/SDT, "
            "or articulate a coherent new construct that isn't just several unrelated items?",
            "redundancy check against retained D3 (security/formality) and the "
            "excluded D4 (earnings/hours preference) diagnostic",
            "single-item-dominance gate at the same threshold used for D4/D5/D6",
            f"omnibus null repetitions raised from {NULL_REPETITIONS} to >= {NULL_FINAL_RECOMMENDATION}",
            "independent-sample or future-wave confirmation before any thesis claim",
        ],
    },
}
with open(OUT / "open_dimension_search_summary.json", "w", encoding="utf-8") as fh:
    json.dump(summary, fh, indent=2)
print(json.dumps(summary, indent=2))

# %% [markdown]
# ## Interpretation guardrails — read before using any output above
#
# - This script tests far more combinations than the theory-constrained
#   script (tens of thousands vs. 414). More tests means a higher chance
#   that *something* clears any fixed silhouette/ARI bar by chance alone,
#   at n=81. The omnibus null in Section 8 is the only number here that
#   actually accounts for that — silhouette or ARI values in isolation do
#   not, no matter how large they look.
# - A shortlisted subset that mixes variables from unrelated theoretical
#   mechanisms (e.g. household income + job satisfaction) is not
#   automatically wrong, but it needs a substantive story for *why* those
#   two things covary in this population before it is worth a name. If no
#   such story exists, report it as an observation, not a dimension.
# - `near_duplicate_variables_flagged = True` means the "cluster" may just
#   be two proxies for one fact (the way `enterprise_registered`/`paid_taxes`
#   and `sector_formality` were already flagged in the theory-driven work as
#   likely to duplicate each other).
# - Nothing here should be used to build individual assignments or reported
#   as a validated profile. It is a hypothesis-generation pass over the data
#   you already have permission to use — the confirmatory work (more null
#   repetitions, theory review, ideally new respondents) still has to happen
#   before any of it is trustworthy.
