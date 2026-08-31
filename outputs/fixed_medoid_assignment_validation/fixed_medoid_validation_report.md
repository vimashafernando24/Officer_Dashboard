# Fixed-medoid assignment validation

No clustering was rerun. No medoid, frozen assignment, profile ID, profile label, or profile size was changed.

Each respondent was represented using only the retained model variables and the original preprocessing/Gower definition. Distances were calculated to the already frozen final-profile medoids. Exact equal-distance ties were assigned to the lowest profile ID.

For this operational validation, **SAFE** requires all of: accuracy ≥ 0.95, balanced accuracy ≥ 0.90, macro F1 ≥ 0.90, ARI ≥ 0.80, and no more than 5% mismatches. This assesses reproduction of the frozen cohort only; it is not independent external validation.

## Summary

| Model | n | Accuracy | Balanced accuracy | Macro F1 | ARI | Mismatches | Distance ties | Judgment |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| D_motivation | 191 | 0.958 | 0.964 | 0.955 | 0.886 | 8 (4.2%) | 9 (4.7%) | SAFE for new-user nearest-medoid assignment |
| D_economic | 191 | 0.990 | 0.985 | 0.985 | 0.955 | 2 (1.0%) | 1 (0.5%) | SAFE for new-user nearest-medoid assignment |
| D_educational_cultural | 191 | 0.906 | 0.925 | 0.886 | 0.776 | 18 (9.4%) | 1 (0.5%) | NEEDS REVIEW |
| E_learning_orientation | 34 | 0.971 | 0.972 | 0.971 | 0.882 | 1 (2.9%) | 0 (0.0%) | SAFE for new-user nearest-medoid assignment |
| F_employment_security | 81 | 0.988 | 0.990 | 0.987 | 0.950 | 1 (1.2%) | 4 (4.9%) | SAFE for new-user nearest-medoid assignment |
| G_economic_role | 56 | 0.964 | 0.954 | 0.954 | 0.854 | 2 (3.6%) | 0 (0.0%) | SAFE for new-user nearest-medoid assignment |
| G_future_engagement | 56 | 0.875 | 0.833 | 0.855 | 0.550 | 7 (12.5%) | 8 (14.3%) | NEEDS REVIEW |

## D_motivation

Frozen profile sizes: 1:47 | 2:75 | 3:69.

Confusion matrix (rows = frozen profile; columns = nearest-medoid prediction):

| Frozen \ Predicted | 1 | 2 | 3 |
|---|---:|---:|---:|
| 1 | 47 | 0 | 0 |
| 2 | 7 | 68 | 0 |
| 3 | 1 | 0 | 68 |

Mismatches: 8/191 (4.2%). Distance ties: 9/191 (4.7%).

Judgment: **SAFE for new-user nearest-medoid assignment**.

## D_economic

Frozen profile sizes: 1:44 | 2:147.

Confusion matrix (rows = frozen profile; columns = nearest-medoid prediction):

| Frozen \ Predicted | 1 | 2 |
|---|---:|---:|
| 1 | 43 | 1 |
| 2 | 1 | 146 |

Mismatches: 2/191 (1.0%). Distance ties: 1/191 (0.5%).

Judgment: **SAFE for new-user nearest-medoid assignment**.

## D_educational_cultural

Frozen profile sizes: 1:15 | 2:53 | 3:57 | 4:66.

Confusion matrix (rows = frozen profile; columns = nearest-medoid prediction):

| Frozen \ Predicted | 1 | 2 | 3 | 4 |
|---|---:|---:|---:|---:|
| 1 | 15 | 0 | 0 | 0 |
| 2 | 1 | 50 | 2 | 0 |
| 3 | 5 | 1 | 51 | 0 |
| 4 | 2 | 7 | 0 | 57 |

Mismatches: 18/191 (9.4%). Distance ties: 1/191 (0.5%).

Judgment: **NEEDS REVIEW**.

## E_learning_orientation

Frozen profile sizes: 1:18 | 2:16.

Confusion matrix (rows = frozen profile; columns = nearest-medoid prediction):

| Frozen \ Predicted | 1 | 2 |
|---|---:|---:|
| 1 | 17 | 1 |
| 2 | 0 | 16 |

Mismatches: 1/34 (2.9%). Distance ties: 0/34 (0.0%).

Judgment: **SAFE for new-user nearest-medoid assignment**.

## F_employment_security

Frozen profile sizes: 1:29 | 2:52.

Confusion matrix (rows = frozen profile; columns = nearest-medoid prediction):

| Frozen \ Predicted | 1 | 2 |
|---|---:|---:|
| 1 | 29 | 0 |
| 2 | 1 | 51 |

Mismatches: 1/81 (1.2%). Distance ties: 4/81 (4.9%).

Judgment: **SAFE for new-user nearest-medoid assignment**.

## G_economic_role

Frozen profile sizes: 1:41 | 2:15.

Confusion matrix (rows = frozen profile; columns = nearest-medoid prediction):

| Frozen \ Predicted | 1 | 2 |
|---|---:|---:|
| 1 | 40 | 1 |
| 2 | 1 | 14 |

Mismatches: 2/56 (3.6%). Distance ties: 0/56 (0.0%).

Judgment: **SAFE for new-user nearest-medoid assignment**.

## G_future_engagement

Frozen profile sizes: 1:35 | 2:21.

Confusion matrix (rows = frozen profile; columns = nearest-medoid prediction):

| Frozen \ Predicted | 1 | 2 |
|---|---:|---:|
| 1 | 35 | 0 |
| 2 | 7 | 14 |

Mismatches: 7/56 (12.5%). Distance ties: 8/56 (14.3%).

Judgment: **NEEDS REVIEW**.

## Output files

- `fixed_medoid_validation_summary.csv`: one row per retained model.
- `fixed_medoid_validation_confusion_matrices.csv`: long-form confusion-matrix cells.
- `fixed_medoid_validation_mismatches.csv`: every mismatch with distances to every profile medoid.
- `fixed_medoid_validation_distance_ties.csv`: every exact distance tie and the deterministic tie-break result.
