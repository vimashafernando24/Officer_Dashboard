# NYSC Officer Dashboard Data-Model Specification

## Scope

This is a dashboard **data specification only**. It creates no frontend, changes no frozen profile, and makes no individual course recommendation. It covers all **17 retained profiles** across the seven frozen dimension-specific models: Branch D n=191, Branch E n=34, Branch F n=81 and Branch G n=56.

The dashboard must keep the seven dimensions separate. A Branch D respondent has three dimension-specific memberships and a Branch G respondent has two; those memberships must never be collapsed into a newly invented overall profile.

## Evidence layers

1. **Cluster-defining:** variables/components that created the retained profile. These explain the definition but cannot independently validate it.
2. **Profiling finding:** only variables retained in the approved profiling report. BH-adjusted support, sparse cells, conditional gateways and valid denominators must display with the chart.
3. **Direct survey evidence:** distributions of respondents’ own answers, calculated within a frozen profile. These are planning context, not inferred individual facts.
4. **Catalogue supply:** documented course counts and attributes. These describe known supply only—not seats, live intake, eligibility, quality or outcomes.

The metric CSV contains **100 governed metric definitions**. Display-priority counts are: context chart=27, headline=6, headline chart=31, secondary=4, secondary/cautious chart=17, strong chart=15.

## Metric coverage by section

| Dashboard section | Specification rows |
|---|---:|
| Barriers and support context | 2 |
| Career direction / job-change / self-employment interest | 8 |
| Cluster-defining characteristics | 31 |
| Demand-versus-supply planning signals | 3 |
| NYSC programme supply by relevant area | 3 |
| Preferred sectors | 7 |
| Profile identity and size | 3 |
| Research cautions | 4 |
| Strong post-cluster profiling findings | 32 |
| Training/further-learning demand | 7 |

## Profile-page summary

| Profile | Recommended dashboard KPIs | Recommended charts | Key officer insight | Main caution |
|---|---|---|---|---|
| D_economic:Profile 1 — Economic profile 1: relatively lower household economic position (n=44) | Profile size; model-cohort share | Cluster-component table; preferred-sector stacked bar; study-field and institution bars | Lower relative household economic position; sector, study-field and institution patterns are more diverse and less ICT/private-institution concentrated. | Relative position is not poverty status; sparse categories and household-count inconsistencies must remain visible. |
| D_economic:Profile 2 — Economic profile 2: relatively higher household economic position (n=147) | Profile size; model-cohort share | Cluster-component table; preferred-sector stacked bar; study-field and institution bars | Higher relative household economic position; stronger concentration in ICT study/sector and private institutions. | Do not infer affordability or individual course suitability; several categorical tables are sparse. |
| D_educational_cultural:Profile 1 — Re-entered students, often with degree-educated parents (n=15) | Profile size; model-cohort share | Educational-characteristic table; job-search, income-source and funding bars | Small re-entry group with high active-search prevalence and more varied personal/funding sources. | n=15; parental education is a proxy and several related economic tables are sparse. |
| D_educational_cultural:Profile 2 — State-institution students without work exposure (n=53) | Profile size; model-cohort share | Educational-characteristic table; job-search and funding stacked bars | State-institution students without work exposure, commonly family-supported and often government-funded/free. | Cross-dimensional financial variables are related to the separate economic model; do not imply causation. |
| D_educational_cultural:Profile 3 — Private-institution students without work exposure (n=57) | Profile size; model-cohort share | Educational-characteristic table; income-source and funding stacked bars | Private-institution students without work exposure, with very high family income/funding reliance. | Sparse categories; family support is a group prevalence, not true of every member. |
| D_educational_cultural:Profile 4 — Work-experienced students, mainly in private institutions (n=66) | Profile size; model-cohort share | Educational-characteristic table; job-search, income-source and income-band bars | Work-experienced students, mainly in private institutions, with more mixed personal income sources. | Economic characteristics overlap another retained dimension and must be labelled cross-dimensional. |
| D_motivation:Profile 1 — Consensus motivation profile 1: externally or uncertainly motivated, with moderate study support (n=47) | Profile size; model-cohort share | Four defining-item stacked bars; employment-contact bar | Externally/uncertainly motivated group with a larger descriptive share reporting no useful contacts. | Contact difference did not survive FDR; membership uncertainty and single-item constructs must be shown. |
| D_motivation:Profile 2 — Consensus motivation profile 2: goal-aligned motivation with mixed study confidence and support (n=75) | Profile size; model-cohort share | Four defining-item stacked bars; employment-contact bar | Goal-aligned motivation with mixed confidence/support and comparatively fewer reporting several useful connections. | Contact evidence is descriptive, not a headline statistical finding. |
| D_motivation:Profile 3 — Consensus motivation profile 3: highly self-directed, capable and connected (n=69) | Profile size; model-cohort share | Four defining-item stacked bars; employment-contact bar | Highly self-directed/capable/connected study profile with more respondents reporting several useful contacts. | Do not interpret the profile as a guaranteed individual trait; contact evidence is descriptive. |
| E_learning_orientation:Profile 1 — High perceived education utility and strong learning ambition (n=18) | Profile size; model-cohort share; small-profile warning | Three defining-item bars; job-acceptance, network-helpfulness and support bars | Higher perceived education usefulness and learning ambition, with descriptive evidence of stricter job conditions and more helpful contacts/support. | n=18; no selected profiling comparison survived FDR and several tables are sparse. |
| E_learning_orientation:Profile 2 — Moderate perceived utility and mixed learning ambition (n=16) | Profile size; model-cohort share; small-profile warning | Three defining-item bars; job-acceptance, network-helpfulness and support bars | Moderate perceived usefulness/mixed ambition, with descriptively less helpful contacts/support and more job-fair searching among eligible searchers. | n=16; conditional search denominator is 11 and no selected comparison survived FDR. |
| F_employment_security:Profile 1 — Temporary/no-contract employment with uncertain security (n=29) | Profile size; model-cohort share; median income-band display | Security-defining stacked bars; income, job-change, satisfaction and training bars | Temporary/no-contract and less secure employment, with lower income and less reliance on the job/business as primary personal income. | Employment arrangement and satisfaction are related outcomes; conditional work-while-study finding is sparse and non-causal. |
| F_employment_security:Profile 2 — Predominantly permanent employment with stronger security (n=52) | Profile size; model-cohort share; median income-band display | Security-defining stacked bars; income, job-change, satisfaction and training bars | Predominantly permanent/stronger-security work, with higher income and greater reliance on regular job/business income. | Stronger security does not imply that every member is satisfied or should remain in the job. |
| G_economic_role:Profile 1 — Predominantly family/partner-supported non-provider (n=41) | Profile size; model-cohort share; small-profile-model warning | Economic-component table; contacts, connection and self-efficacy median bars | Predominantly family/partner-supported non-providers, descriptively less connected to employment contacts and labour-market information. | The comparison model includes n=15 in its other profile; no selected profiling finding survived FDR. |
| G_economic_role:Profile 2 — Predominantly self-income provider/contributor (n=15) | Profile size; model-cohort share; small-profile warning | Economic-component table; contacts, connection and self-efficacy median bars | Self-income providers/contributors, descriptively more connected to employment contacts and labour-market information. | n=15; results are descriptive and must not be generalized as individual capacities. |
| G_future_engagement:Profile 1 — Work-and-education engaged, mostly prior work experience (n=35) | Profile size; model-cohort share; self-efficacy median | Four defining-item bars; self-efficacy/support/connection/future-orientation median bars | Work/education-engaged group with stronger self-efficacy, support and labour-market connection and less future uncertainty. | Associations are non-causal; the profile does not guarantee readiness for every individual. |
| G_future_engagement:Profile 2 — Low/uncertain engagement, mostly no prior work experience (n=21) | Profile size; model-cohort share; self-efficacy median | Four defining-item bars; self-efficacy/support/connection/future-orientation median bars | Low/uncertain engagement group with lower self-efficacy, support and connection and greater future uncertainty. | n=21; do not label individuals as deficient or infer unmeasured needs. |

## Catalogue supply reference

The V2 file contains **87 unique courses**. Known field coverage is: NVQ level 32/87, qualification type 34/87, attendance type 87/87, normalized duration 87/87 and instruction languages 87/87.

| Broad skill area | Documented course records |
|---|---:|
| Agriculture & Environment | 5 |
| Automotive & Mechanical Engineering | 15 |
| Beauty, Fashion & Personal Care | 9 |
| Business, Management & Administration | 5 |
| Construction & Surveying | 8 |
| Creative Arts, Design & Media | 5 |
| Electrical & Electronics | 8 |
| Hospitality & Culinary Arts | 6 |
| ICT & Computing | 18 |
| Languages & Communication | 8 |

Course counts must not be interpreted as capacity. The catalogue does not establish current seats, centre availability, fees, entry eligibility, application dates or employment outcomes.

## 1. Metrics on every profile page

- Stored profile label and retained dimension.
- Profile size and its share of the same frozen model cohort.
- Defining-variable distributions with valid n.
- Assignment-uncertainty and small-sample warning where applicable.
- Evidence/denominator note and permanent group-not-individual warning.
- Broad preferred-sector distribution and a clearly separated catalogue-supply reference.

Only profile size/share is a universal headline KPI. Weak or exploratory survey differences are never headline KPIs.

## 2. Branch-specific metrics

- **D:** study motivation/autonomy/competence/belonging; relative household economic components; educational/cultural trajectory; plans after education; study field, institution, programme-access and job-search context where approved.
- **E:** education usefulness/further-learning orientation; training type believed helpful; job type sought; job-acceptance conditions and search/support context. All E profiling differences are descriptive because none survived BH adjustment.
- **F:** contract/security/formality; income, primary income source, job-change intention, satisfaction and training exposure. Work-while-study type is an approved secondary conditional chart only (63 eligible; severe sparsity).
- **G:** household economic role or future engagement; employment contacts, labour-market connection, self-efficacy and support. The four strongest future-engagement comparisons have adjusted support; G-economic comparisons remain descriptive.

## 3. Scientifically safe charts

- Stacked bars for complete categorical distributions, always with n/denominator.
- Median/IQR bars or compact tables for ordered/numeric variables; axes must describe the coding direction.
- Tables for conditional or sparse results, with the gateway and eligible profile n shown.
- Side-by-side **separate** demand percentages and catalogue course counts by broad area.
- Text cautions for small samples, ambiguity, structural N/A, sparsity and cross-dimensional overlap.

Cross-profile comparison is safe only within the same retained model and under the same denominator rule. No statistical comparison across D/E/F/G is authorized.

## 4. Metrics that must not be shown

- Unscreened weak/exploratory profiling variables as prominent findings.
- Respondent identifiers, timestamps, routing metadata or individual survey records.
- Profiling probabilities or profile percentages presented as an individual’s facts.
- Structural N/A converted to No, or conditional follow-ups divided by the full profile.
- Composite need scores, causal language, poverty labels or deficit labels not in the frozen research.
- Individual course recommendations, eligibility predictions or claims that every profile member wants a course.
- Demand/supply ratios, capacity gaps or underserved-area claims without seats, current intake and location data.
- Course rankings based only on a profile label.

## 5. Implementation readiness

**The data model is ready for a dashboard implementation, with governance conditions.** The frontend must consume the metric specification rather than improvising calculations, enforce model-specific comparisons, display valid denominators and warnings, and keep catalogue supply separate from youth demand. A later implementation should validate each rendered metric against its named frozen source before release.

## Output files

- `dashboard_metric_specification.csv` — governed formulas, sources, denominators, evidence type, visualization and cautions.
- `profile_dashboard_summary.csv` — one implementation summary row for every retained profile.
- `officer_dashboard_specification_report.md` — this human-readable design specification.
