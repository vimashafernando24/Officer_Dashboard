# NYSC Youth Profile Knowledge Base — Build Report

**Purpose of this build:** Construct the research/profile knowledge source for a later RAG
(retrieval-augmented generation) recommendation layer. This stage only compiles and structures
already-frozen, already-audited research findings into one comprehensive full-text knowledge
document per retained profile. **No frozen clustering, profiling, survey, assignment, or course
file was modified.** No programme recommendation, scoring, or matching logic was created.

---

## 1. What was built

| Deliverable | Location | Count |
|---|---|---|
| Per-profile knowledge documents | `outputs/rag_profile_knowledge/documents/*.txt` | 17 |
| Document index | `outputs/rag_profile_knowledge/profile_document_index.csv` | 17 rows + header |
| This report | `outputs/rag_profile_knowledge/profile_knowledge_report.md` | — |

Each document is named `{model_id}_p{profile_id}.txt` (e.g. `D_economic_p1.txt`) and follows the
same five-section structure, exactly as required:

1. **PROFILE_DEFINITION** — facts that define the cluster (branch, retained dimension/model,
   profile id/label, exact frozen size, exact cluster-forming variables, theoretical basis,
   clustering method, validation diagnostics, decision status, and the profile's own frozen
   interpretation text).
2. **SUPPORTED_PROFILE_FINDINGS** — only the post-cluster comparisons that passed the model's
   pre-registered effect-size/coverage reporting screen (i.e. explicitly approved/retained
   findings), organised into the same five evidence categories used in the source report
   (strongest characteristics; barriers/support/financial; aspirations/preferences;
   education/training/employment; programme-relevant evidence), plus a statistical-support table
   (effect size, raw p, BH-adjusted p, FDR-significance flag) for every variable named.
3. **DIRECT_GROUP_DISTRIBUTIONS** — the complete observed distribution of this profile's answers
   for **every** non-cluster-forming variable tested against that model (not only the highlighted
   findings), each tagged `[SCREENED FINDING]` or `[tested, not highlighted]` so a reader can tell
   an approved finding from raw descriptive data.
4. **CAUTIONS** — model-level and profile-specific cautions verbatim from the frozen source, plus
   systematically generated cautions for conditional denominators, sparse cells, cross-dimensional
   overlap, small-sample size, and FDR-correction context.
5. **PROHIBITED_INFERENCES** — nine universal prohibitions applying to all 17 profiles (do not
   convert a group percentage into an individual fact, do not treat membership as a diagnosis or
   eligibility gate, do not treat untested/unscreened data as a finding, do not generalise beyond
   the 362-respondent cohort, do not invent needs, do not use this document alone to select a
   course, etc.), plus model-specific reinterpretation warnings (e.g. "not poverty status," "not a
   validated SDT type," "not low-vs-high household resources," "not respondent worth or
   employability"), plus one worked right/wrong counter-example specific to that profile's own
   top finding.

---

## 2. Verification of the 17 frozen profiles and exact frozen sizes

The 17 retained profiles and their sizes were cross-verified across **three independent points**
in the frozen source material, all of which agree exactly:

1. `outputs/final_cluster_programme_relevant_profiles.csv` (17 data rows).
2. `NYSC_all_branches_clustering_final_report.md`, §4.1 "Retained profile systems" (k and sizes
   column).
3. `NYSC_Final_Clustering_and_Post_Cluster_Profiling_Report.docx` / `final_cluster_profiling_report.md`,
   Part III "Final verification" freeze table (the report's own audit re-check of frozen assignment
   counts).

| Branch | Model | Profile sizes | Sum |
|---|---|---|---|
| D | Motivation and study experience | 47 / 75 / 69 | 191 |
| D | Economic resources and household pressure | 44 / 147 | 191 |
| D | Educational trajectory and cultural capital | 15 / 53 / 57 / 66 | 191 |
| E | Education usefulness and further-learning orientation | 18 / 16 | 34 |
| F | Employment security and formality | 29 / 52 | 81 |
| G | Household economic role and dependency | 41 / 15 | 56 |
| G | Future engagement and prior work experience | 35 / 21 | 56 |

**17 profiles total** (9 in Branch D across 3 dimensions, 2 in Branch E, 2 in Branch F, 4 in
Branch G across 2 dimensions). Because a Branch D respondent is profiled independently in all
three retained D dimensions, the per-branch sum of profile sizes is a multiple of the branch
cohort: D sums to 573 = 191×3, E to 34 = 34×1, F to 81 = 81×1, G to 112 = 56×2 — all of which match
exactly, confirming internal consistency between the profile CSV, the two report documents, and
the branch cohort totals stated in the frozen report (strict cohort = 362: D=191, E=34, F=81,
G=56).

No discrepancy was found between any of the three sources.

---

## 3. Source files used (read-only)

| File | Role |
|---|---|
| `outputs/final_cluster_programme_relevant_profiles.csv` | Primary source for PROFILE_DEFINITION identifiers and the five SUPPORTED_PROFILE_FINDINGS evidence-category texts, and the profile-specific CAUTIONS paragraph. |
| `outputs/final_cluster_profile_comparison_summary.csv` | Primary source for DIRECT_GROUP_DISTRIBUTIONS (270 variable-level rows across the 7 models) and the statistical-support table in SUPPORTED_PROFILE_FINDINGS (effect size, coverage, p-values, FDR flags, sparse/conditional/cross-dimensional flags). |
| `NYSC_all_branches_clustering_final_report.md` | Source for cluster-forming variables, k/sizes, validation diagnostics (silhouette, bootstrap ARI, source-method ARIs, PAC, permutation p, checks passed), theoretical basis, and final decision text per model. |
| `NYSC_Final_Clustering_and_Post_Cluster_Profiling_Report.docx` (Part II and Part III) | Cross-verification source for all of the above, plus the Branch F approved secondary conditional finding and the Part III freeze-verification table. Extracted via direct OOXML parsing (no external converter available in this environment). |
| `final_cluster_profiling_report.md` | Clean-markdown restatement of the docx's Part II content; used to confirm the extraction above was accurate. |

All five sources were cross-checked against each other; every profile-level number, effect size,
and quoted caution in the generated documents was found to be word-for-word or numerically
identical across sources. No number in the generated documents was computed, estimated, or
extrapolated — every figure is a direct transcription from one of the files above.

**Files explicitly NOT modified:** all files listed above, plus every other frozen clustering,
profiling, survey, assignment, and course dataset in the repository (`outputs/*_clusters/`,
`outputs/*_assignment_validation/`, `nysc_survey_*`, `nysc_course_*`, etc.).

---

## 4. What was deliberately excluded, and why

Per the task instructions, the following were **not** used and **not** invented:

- **Cluster membership as a course score / recommendation input** — this build only compiles
  descriptive profile knowledge; no scoring or matching logic exists here.
- **Demographic or household variables as defining facts** — where a demographic/household
  variable (e.g. gender, age group, household income) appears, it appears only inside
  DIRECT_GROUP_DISTRIBUTIONS as one of the many *tested, non-cluster-forming* comparison
  variables from the frozen post-cluster profiling table — never as a PROFILE_DEFINITION fact,
  and never elevated to SUPPORTED_PROFILE_FINDINGS unless it independently passed the model's own
  effect-size/coverage screen in the frozen source.
- **Invented needs** — every SUPPORTED_PROFILE_FINDINGS bullet is a verbatim transcription of the
  frozen evidence-summary text; nothing was paraphrased into a stronger or more specific claim.
- **Group percentages converted into individual facts** — explicitly forbidden in every document's
  PROHIBITED_INFERENCES section, with a profile-specific worked counter-example.
- **Programme recommendations** — none of the 17 documents names, ranks, or suggests any NYSC
  course; several PROHIBITED_INFERENCES entries explicitly state that course matching requires a
  separate stage.

---

## 5. Known limitations of this knowledge base (inherited from the frozen source, not introduced here)

- Branch E (n=34) and several individual profiles (n=15, n=16) are small; the source report and
  every corresponding document flag this explicitly.
- Most models have few or zero SUPPORTED_PROFILE_FINDINGS that remain significant after
  Benjamini–Hochberg FDR correction — D_educational_cultural (7/7) is the strongest; D_motivation,
  E_learning_orientation and G_economic_role have **zero** FDR-significant findings among their
  screened findings. This is stated per-document in the `fdr_note` and CAUTIONS section, not
  hidden.
- A large share of tested variables in every model contain sparse cells, conditional
  eligible-subgroup denominators, or cross-dimensional overlap with another retained model; every
  instance is flagged inline in DIRECT_GROUP_DISTRIBUTIONS rather than smoothed over.
- These documents describe **dimension-specific** profiles only. No respondent-level, whole-person,
  or cross-branch integrated profile exists in the frozen source (an earlier integrated-score
  attempt was withdrawn), and none is implied here.

---

## 6. Next step (not part of this task)

This knowledge base is a read/retrieval source only. Building the actual RAG retrieval index,
embeddings, or any course-recommendation logic that consumes these documents is explicitly a
separate, later task.
