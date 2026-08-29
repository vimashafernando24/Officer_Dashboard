# Branch-by-branch clustering progress

This file records which exploratory clustering results are retained and which
are excluded. A statistically stable partition is not treated as a validated
psychometric scale.

| Scope | Dimension | Valid records | Decision | Main result or reason |
|---|---|---:|---|---|
| Global (all strict branches) | Household economic resources | 363 | Excluded | No sufficiently robust solution; K-medoids agreement and raw-count sensitivity were both 0.011 ARI, and PAC was 0.609. |
| Branch F | Household economic resources and responsibility | 81 | Excluded from clustering; retain for descriptive analysis | The k=2 split (21 and 60) was stable internally but was primarily an income-source split: the single `primary_income_source` partition had ARI 0.845 with the consensus, removing that item changed the partition to ARI -0.036, structural-resource-only agreement was ARI 0.000, and the 100-repetition searched-null p-value was 0.059. |
| Branch F | Educational and inherited cultural capital | 81 | Excluded from clustering; retain for descriptive analysis | No k=2–4 candidate kept at least 15 respondents per cluster under both algorithms. Diagnostic k=2 had K-medoids sizes 21/60 but spectral minimum size 14, spectral stability mean ARI 0.713, and permutation p=0.683. The diagnostic split was influenced most by `worked_while_studying` (single-item ARI 0.571; leave-out ARI 0.243). |
| Branch F | Employment security and formality | 81 | Retained with PAC caution | Two profiles (29 and 52); seven of eight checks passed. |
| Branch F | Earnings and working-time preference patterns | 81 | Excluded from final dimension set by researcher decision; retain as descriptive diagnostic | Two profiles (51 and 30) and eight of eight statistical checks passed, but removing the hours/income-preference item changed the partition substantially (ARI -0.013). The result is a direct preference segmentation rather than a multidimensional employed-youth profile. |
| Branch F | Job satisfaction and mobility intention | 81 | Excluded from clustering; retain for descriptive analysis | The apparent profiles nearly reproduced `hopes_to_change_job`: removing that item gave ARI -0.007. Both groups remained predominantly job-satisfied, PAC was 0.519, and detailed-versus-binary contract encoding agreement was only ARI 0.488. |
| Branch F | Qualification utilisation and skill development | 81 | Excluded from clustering; retain for descriptive analysis | The three-input result exactly reproduced training receipt (leave-one-out ARI 0.014). With training moved to a descriptor, no k=2–4 solution met the minimum-size rule across both algorithms; K-medoids/spectral ARI was only 0.097–0.212. |
| Branch F | Professional social capital | 81 | Skipped under the prior no-overlapping-social-connectedness decision | The proposed indicators are `employment_network_quality` and `professional_network_growth`; retain them as descriptors unless that earlier scope decision is changed. |
| Branch F | Work motivation and psychological need experience | 81 | Excluded from clustering; retain for descriptive analysis | No k=2–4 candidate met the cross-algorithm minimum-size rule. At diagnostic k=3, spectral agreement was ARI 0.330, and nominal-versus-ordinal motivation-type encoding agreement was only ARI 0.248. |
| Branch F | Transition-to-work search pathway and barriers | 81 | Excluded from clustering; retain for descriptive analysis | Diagnostic k=2 had silhouette 0.165, bootstrap mean ARI 0.532, and spectral agreement ARI 0.038. Raw-versus-log count agreement was ARI 0.902, so count preprocessing did not explain the instability. |
| Branch G | Variable and candidate-dimension audit | 56 | Completed | Sixty-two answerable variables were audited: 19 candidate clustering inputs, 21 programme/profile descriptors, 13 conditional descriptors, and 9 routing/audit fields. Five candidate dimensions were proposed. |
| Branch G | Household economic resources and dependency (G1) | 56 | Retained with narrowed interpretation and caution | Two profiles (41 and 15) passed all 9 screening checks: Gower silhouette 0.372, consensus bootstrap mean ARI 1.000, K-medoids/spectral agreement 0.854/0.718, and permutation p=0.012. However, structural-resource-only agreement was ARI -0.016 and removing income source reduced agreement to ARI 0.356. Therefore this is a household economic role/dependency segmentation, not a low-versus-high resource classification. |
| Branch G | Psychological readiness and support for engagement (G4) | 56 | Excluded from clustering; retain as descriptive cross-tabulation | No k=2–4 candidate met the minimum-profile-size rule across both algorithms. Diagnostic k=2 produced groups of 45 and 11; K-medoids agreement was ARI 0.590 and removing self-efficacy changed the partition to ARI -0.017. Although silhouette (0.539), ensemble bootstrap ARI (0.984) and permutation p=0.010 looked strong, the small constrained group and feature sensitivity prevent retention. |
| Branch G | Inactivity pathway and future engagement intention (G3) | 56 | Retained with narrowed interpretation | Two profiles (35 and 21) passed all 10 checks: Gower silhouette 0.413, ensemble bootstrap ARI 1.000, K-medoids/spectral agreement 0.928/1.000, and permutation p=0.011. The 13-category inactivity reason did not dominate; removing it reproduced the final partition (ARI 1.000). Therefore interpret the result as future-engagement/prior-work-experience profiles, with inactivity reason only descriptive. |
| Branch G | Educational and inherited cultural capital (G2) | 56 | Excluded from clustering; retain for descriptive analysis | Diagnostic k=2 formed groups of 38 and 18 but exactly reproduced `worked_while_studying` (single-item ARI 1.000); removing that item changed the partition to ARI 0.004. Both profiles had the same median parental-education position, and the searched permutation p-value was 0.230. |
| Branch E | Variable and candidate-dimension audit | 34 | Completed | Seventy-five answerable variables were audited: 24 active candidate inputs across six dimensions, 3 social-capital inputs skipped under the no-overlap decision, 26 programme/profile descriptors, 16 conditional descriptors and 6 routing/audit fields. Only k=2 can meet the minimum profile size of 15. |
| Branch E | Job-search psychological readiness/support (E1) | 34 | Excluded; descriptive only | Consensus groups were 17/17, but the smallest full-source group was 11, spectral agreement was ARI 0.403 and the permutation result was exactly p=0.050 rather than below 0.05. |
| Branch E | Search intensity/accumulated exposure (E2) | 34 | Excluded; descriptive only | Diagnostic groups of 26/8 exactly reproduced `active_search_4weeks` (single-item ARI 1.000; leave-out ARI -0.020); permutation p=0.500. Raw-versus-log count agreement was ARI 1.000, so count encoding was not the cause. |
| Branch E | Economic urgency/job-acceptance constraints (E3) | 34 | Excluded; descriptive only | Diagnostic groups of 28/6 exactly reproduced `has_minimum_wage` (single-item ARI 1.000; leave-out ARI 0.001). |
| Branch E | Education-to-work preparedness/learning orientation (E4) | 34 | Retained cautiously—feature dependent | Two profiles (18/16) passed all 10 mandatory checks: silhouette 0.567, ensemble ARI 0.953, K-medoids/spectral agreement 0.882/1.000 and permutation p=0.040. However, removing `past_edu_usefulness` reduced agreement to ARI 0.039, so interpret narrowly as education-usefulness/further-learning orientation. |
| Branch E | Household economic resources/dependency (E5) | 34 | Excluded; descriptive only | Final groups were 22/12, source-algorithm agreement was only ARI 0.484, ambiguous membership was 38.2%, and permutation p=0.583. |
| Branch E | Educational/inherited cultural capital (E6) | 34 | Excluded; descriptive only | Diagnostic groups of 24/10 exactly reproduced `worked_while_studying` (single-item ARI 1.000; leave-out ARI -0.002). |
| Branch E | Job-search social capital (E7) | 34 | Skipped under no-overlap decision | The three inputs remain descriptors unless the earlier social-connectedness scope decision changes. |

## Excluded D4 diagnostic result

- Profile 1: **Mostly current-hours preference** — 51 respondents (63.0%);
  47 preferred to keep things the same and 4 preferred fewer hours/income.
- Profile 2: **More-hours/more-income preference** — 30 respondents (37.0%);
  28 preferred more hours/income and 2 preferred fewer hours/income.
- Both profiles have median monthly-income-band code 4 and median usual weekly
  hours of 40. Therefore, this result must not be described as a low-income
  versus high-income split.

All proposed Branch F dimensions D1–D9 have now been tested or explicitly
skipped. The only retained Branch F clustering is D3 employment security and
formality, with caution. D4 remains available for descriptive analysis but is
not part of the final clustering set.
