# Locked validation: D educational/cultural assignment

## Decision

**SAFE TO FREEZE**

No clustering was rerun. No medoids, frozen assignments, variables, weights, profile IDs, labels, memberships, or questionnaires were changed.

## Validation design

- 500 repeated stratified 5-fold cross-validation runs.
- Every repeat generated one out-of-fold prediction for all 191 respondents.
- The respondent and the rest of their held-out fold were excluded from all profile means.
- This is stricter than operational new-user assignment, where the full frozen reference cohort will be available.
- Exact mean-distance ties used the lowest profile ID and were recorded.
- Confirmation required at least 95% of repeats to pass all five SAFE thresholds jointly.

## Overall metric distributions

| Metric | Mean | Median | Empirical 95% interval | Worst case | Repeats passing |
|---|---:|---:|---:|---:|---:|
| accuracy | 0.9788 | 0.9791 | 0.9686–0.9843 | 0.9634 | 500/500 (100.0%) |
| balanced_accuracy | 0.9793 | 0.9830 | 0.9497–0.9877 | 0.9368 | 500/500 (100.0%) |
| macro_f1 | 0.9708 | 0.9714 | 0.9495–0.9809 | 0.9403 | 500/500 (100.0%) |
| ari | 0.9492 | 0.9495 | 0.9309–0.9640 | 0.9166 | 500/500 (100.0%) |
| mismatch_percent | 2.1204 | 2.0942 | 1.5707–3.1414 | 3.6649 | 500/500 (100.0%) |

All five thresholds were passed jointly in **500/500 repeats (100.0%)**.

## Profile-specific performance

| Profile | n | Precision mean (95% interval; worst) | Recall mean (95% interval; worst) | F1 mean (95% interval; worst) |
|---|---:|---:|---:|---:|
| 1 — Re-entered students, often with degree-educated parents | 15 | 0.896 (0.849–0.938; 0.812) | 0.982 (0.867–1.000; 0.800) | 0.936 (0.867–0.968; 0.839) |
| 2 — State-institution students without work exposure | 53 | 0.999 (0.981–1.000; 0.980) | 0.961 (0.943–0.981; 0.925) | 0.980 (0.971–0.990; 0.961) |
| 3 — Private-institution students without work exposure | 57 | 0.962 (0.934–0.983; 0.919) | 0.999 (0.982–1.000; 0.982) | 0.980 (0.966–0.991; 0.957) |
| 4 — Work-experienced students, mainly in private institutions | 66 | 1.000 (1.000–1.000; 0.985) | 0.974 (0.970–0.985; 0.970) | 0.987 (0.985–0.992; 0.977) |

Profile 1 contained 15 respondents. Its mean recall was 0.982, median recall was 1.000, empirical 95% interval was 0.867–1.000, and worst observed recall was 0.800. It did not collapse in any repeat.

Across 95,500 out-of-fold predictions there were 1 exact mean-distance ties. 178 of 191 respondents were correct in every repeat; no respondent was incorrect in every repeat.

## Stability judgment

The mean, median, empirical 95% interval and worst observed result remained inside every SAFE threshold. Performance was stable across fold membership and reference-profile composition.

**Final decision: SAFE TO FREEZE.**

## Output files

- `locked_validation_design.json`
- `locked_validation_repeat_metrics.csv`
- `locked_validation_metric_distribution.csv`
- `locked_validation_profile_repeat_metrics.csv`
- `locked_validation_profile_summary.csv`
- `locked_validation_respondent_stability.csv`
