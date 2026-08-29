# Branch E clustering results report

## Scope and method

All six active Branch E candidate dimensions were tested on the 34 strict final-path respondents. E7 job-search social capital remained skipped under the earlier no-overlapping-social-connectedness decision. With a minimum profile size of 15, only k=2 is mathematically eligible.

Each dimension used equal-weight Gower distance on original mixed survey responses, full K-medoids and spectral clustering, 200 matched consensus base partitions, 100 ensemble bootstraps, single-feature dominance, leave-one-feature-out sensitivity and a 100-repetition independently shuffled-variable null. E2 additionally compared raw and `log1p` application/interview counts. No dimension score or psychometric scale was constructed.

## Final decisions

| Code | Dimension | Profile sizes | Silhouette | Ensemble ARI | K-medoids / spectral ARI | Maximum single-item ARI | Minimum leave-one-out ARI | Permutation p | Final decision |
|---|---|---:|---:|---:|---:|---:|---:|---:|---|
| E1 | Job-search psychological readiness/support | 17 / 17 | 0.381 | 0.939 | 0.668 / 0.403 | 0.483 | 0.261 | 0.050 | Rejected |
| E2 | Search intensity/exposure | 26 / 8 | 0.533 | 1.000 | 1.000 / 1.000 | 1.000 | -0.020 | 0.500 | Rejected |
| E3 | Economic urgency/acceptance constraints | 28 / 6 | 0.620 | 1.000 | 1.000 / 1.000 | 1.000 | 0.001 | Not estimable from a size-eligible null | Rejected |
| E4 | Education-to-work preparedness/learning orientation | 18 / 16 | 0.567 | 0.953 | 0.882 / 1.000 | 0.668 | 0.039 | 0.040 | **Retained cautiously—feature dependent** |
| E5 | Household economic resources/dependency | 22 / 12 | 0.257 | 0.898 | 0.484 / 0.484 | 0.772 | 0.080 | 0.583 | Rejected |
| E6 | Educational/inherited cultural capital | 24 / 10 | 0.585 | 1.000 | 1.000 / 1.000 | 1.000 | -0.002 | Not estimable from a size-eligible null | Rejected |
| E7 | Job-search social capital | — | — | — | — | — | — | — | Skipped under no-overlap decision |

## Retained E4 profiles

E4 uses `past_edu_usefulness`, `plans_further_edu`, and `expected_highest_edu_e`. Past education usefulness and further-education plans remain nominal; expected education retains the questionnaire order.

| Profile | Records | Percent | Response pattern |
|---|---:|---:|---|
| High perceived education utility and strong learning ambition | 18 | 52.9% | 83.3% rated past education very useful; 94.4% planned further education; 66.7% expected postgraduate education. |
| Moderate perceived utility and mixed learning ambition | 16 | 47.1% | 93.8% rated past education somewhat useful; 62.5% planned further education, while 18.8% were unsure and 18.8% said no; 37.5% expected postgraduate education. |

All ten mandatory checks passed for E4. Its Gower silhouette is 0.567, ensemble bootstrap mean ARI is 0.953, full K-medoids/spectral agreement is 0.882/1.000, both profiles exceed 15, ambiguous membership is 2.9%, and the searched permutation result is p=0.040.

The limitation is important: `past_edu_usefulness` is the dominant item (single-item ARI 0.668), and removing it changes the partition almost completely (ARI 0.039). Therefore E4 must not be presented as a validated general human-capital or learning-readiness scale. It is an exploratory **education-usefulness and further-learning orientation** profile system. The result needs replication in more Branch E respondents.

## Why the other dimensions were rejected

- **E1:** The consensus produced balanced 17/17 groups, but the full spectral solution agreed only at ARI 0.403, the smallest full-source profile was 11, and the permutation result was exactly 0.050 rather than below 0.05. The pattern is descriptive only.
- **E2:** The 26/8 split exactly reproduced `active_search_4weeks` (ARI 1.000). Removing it gave ARI -0.020. Raw/log count encoding agreed perfectly, so count preprocessing was not the problem.
- **E3:** The 28/6 split exactly reproduced `has_minimum_wage` (ARI 1.000); removing it gave ARI 0.001. This is a direct yes/no response split, not a multidimensional profile.
- **E5:** The final 22/12 profiles were undersized, weakly separated, poorly aligned with both source algorithms (ARI 0.484), ambiguous for 38.2% of respondents and non-significant under permutation (p=0.583). Household worker share was the strongest driver.
- **E6:** The 24/10 split exactly reproduced `worked_while_studying` (ARI 1.000); removing it gave ARI -0.002. It is not an inherited-cultural-capital segmentation.

## Branch E conclusion

Branch E has one retained exploratory dimension: **E4 education-usefulness and further-learning orientation**, with a strong feature-dependence warning. E1, E2, E3, E5 and E6 are excluded from clustering and remain available only for descriptive analysis or programme mapping. E7 remains skipped.
