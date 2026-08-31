# Officer Dashboard Flow and Evidence Audit

**Audit date:** 30 August 2026  
**Scope:** The active React officer dashboard, Flask endpoints, frozen nearest-medoid assignment, cluster research evidence, course retrieval, programme-ranking LLM call, and validation.  
**Nature of this audit:** Originally a read-only analysis. The cluster-research teaching panel is now deterministic: one generated model/profile library is built from the frozen retained evidence and read directly by the frontend without an LLM call. Clustering and programme ranking were not changed.

## 1. Plain-language conclusion

The current system is not one simple RAG pipeline. It is three connected systems:

1. a deterministic branch-specific nearest-medoid assignment system;
2. a governed finding-level research corpus and assigned-profile retrieval system for the wizard;
3. a deterministic sector-to-catalogue retrieval system followed by LLM ranking.

The nearest-medoid assignment remains frozen and reproducible. The main confusion is downstream:

- the final research documents contain **89 unique profile-level reported findings** across 17 profiles;
- programme ranking still uses the **59 statements in the `programme_relevant_findings` column**;
- the cluster wizard now uses a separate, versioned corpus containing all **89 final reported profile findings**;
- the wizard filters exactly to assigned profiles, orders every finding using local TF-IDF relevance, and returns saved officer-reviewed wording for one card per finding;
- the active course path does not use BM25 or embeddings either: it retrieves every verified course in the static catalogue areas mapped to the member's selected sectors, then asks the LLM to rank them;
- the repository uses the word `validated` for several different concepts that should be kept separate.

## 2. Current user flow

```text
Officer selects current situation (D / E / F / G)
        |
        v
Frontend requests branch-specific question configuration
        |
        v
Officer completes every cluster-forming question
        |
        v
Officer selects 1-3 sectors, 1-3 skills per sector, and Q2-Q5 preferences
        |
        v
Frontend requests free assignment preview
        |
        +--> frozen nearest-medoid assignment
        +--> branch cluster tree and stored cluster descriptions
        |
        +--> deterministic cluster-research teaching panel
        |       input: assigned profile keys
        |       output: sibling comparison + retained survey evidence; no API/LLM call
        |
        +--> programme-options LLM call
                input: member answers + assigned profiles + same 59-finding subset
                       + all course documents in selected-sector catalogue areas
                output: ranked programmes, explanations, and programme questions
                backend: citation checks, constraint checks, and exact-skill restoration
```

## 3. Step-by-step production flow

### 3.1 Branch selection and question configuration

The frontend asks the officer to select the member's current situation. The backend does not infer the branch from a wider set of answers; the selected option directly becomes branch D, E, F, or G.

The frontend then calls:

```text
GET /api/question_config?branch={branch}
```

The response combines:

- hard-coded cluster-question wording and answer options;
- the branch-to-model mapping;
- a static sector-to-course-area bridge;
- generated selectable course/skill names;
- fixed Q2-Q5 answer options.

### 3.2 Intake decoding

Both paid LLM endpoints and the free preview call the same `decode_new_person_intake()` function. It:

- checks that the branch is D, E, F, or G;
- converts cluster answer codes into display labels;
- accepts one to three sectors;
- accepts up to three valid skills under each sector;
- carries the training reason, schedule, language, and qualification answers into `officer_context`.

The React UI prevents progression until all cluster questions and programme questions are answered. The backend itself does **not** verify that every cluster-forming variable required by the selected branch is present. A direct or malformed API request can therefore reach nearest-medoid assignment with missing features. If every feature for a model were missing, every medoid would receive distance 1 and the lowest profile ID would win the tie. This is a backend validation gap.

### 3.3 Frozen nearest-medoid assignment

`build_profile_context()` calls `assign_all_profiles_for_branch()`.

The branch determines how many independent assignments are made:

| Branch | Retained models assigned |
|---|---|
| D | Motivation, household resources, education background |
| E | Education usefulness and further learning |
| F | Employment security and formality |
| G | Household economic role, future engagement |

For each retained model, the code:

1. loads its frozen medoid CSV;
2. derives the same features documented in the original retained clustering implementation;
3. calculates pairwise-available Gower-style distances;
4. selects the nearest medoid;
5. resolves an exact tie to the lowest profile ID;
6. calculates a distance-margin percentage, which is not classification accuracy.

The reproduction test passed for six models exactly and for `G_economic_role` within its documented known discrepancy. The known discrepancy affects reproduced raw distances/tie counts, although the documented cases still select the correct nearest profile.

### 3.4 Building assigned-profile context

For every assigned profile, `build_profile_context()`:

1. uses `profile_document_index.csv` to load a large compiled profile text document;
2. parses its profile definition, supported findings, statistics, distributions, cautions, and prohibited inferences;
3. asks `retained_cluster_evidence_registry.py` to select the current production evidence subset;
4. calculates a current-context eligible subset and a rejected subset;
5. stores all three forms on `ProfileContextEntry`:
   - `retained_evidence`;
   - `validated_evidence` (the current-context subset);
   - `rejected_evidence`.

For Branch D, it also loads a generated JSON dossier for every assigned profile. That dossier is not used by either active LLM payload, but its absence would still break `build_profile_context()`. It is therefore an unnecessary runtime dependency.

### 3.5 Free assignment preview

The frontend automatically calls:

```text
POST /api/new_person_evidence_preview
```

This repeats assignment and returns:

- branch;
- assigned profile IDs, codes, stored names, and stored descriptions;
- all possible clusters for the selected branch;
- the full branch/model/profile tree used by the visual component.

It does not return research statistics or retained findings to the browser.

### 3.6 Deterministic cluster-research teaching panel

The frontend imports `frontend/src/data/clusterResearchTeachingLibrary.json` directly. There is no research endpoint and no research-content LLM call.

The generated library contains all seven frozen models, all 17 governed profiles and all 89 final retained findings. It is grouped by model so an assigned profile is always explained against its sibling profiles in that same model. The main panel shows a short historical comparison; an evidence modal shows the exact survey question, the response distributions genuinely retained in the research outputs, evidence status, sample sizes and cautions.

The generator rebuilds the retained corpus from the explicit registry and authoritative final analysis tables. It fails unless the result contains exactly 7 models, 17 profiles and 89 unique evidence IDs. Complete categorical distributions are used where available; limited comparisons and median/IQR summaries are explicitly labelled when complete categories were not retained.

### 3.7 Course retrieval

Before programme ranking, the backend verifies the 84 indexable course documents and four exclusions, including SHA-256 hashes.

The active retrieval method is:

```text
selected sector
    -> static SECTOR_BRIDGE mapping
    -> one or more catalogue skill areas
    -> every verified course in those areas
```

There is no active BM25, embedding, vector, or semantic-search stage in this frontend flow. `retrieval_v2.py` contains older BM25 code, but the active path imports only its `SECTOR_BRIDGE` constant.

Examples of the size of a one-sector candidate set are:

- IT and communications: 18 courses;
- manufacturing or production: 22 courses;
- construction and building: 8 courses;
- hospitality: 5 courses.

With up to three sectors, the LLM may receive dozens of full course documents.

For every selected skill whose name exactly matches a governed course name, retrieval chooses one course variant using schedule, language, and qualification preferences. That course ID becomes mandatory coverage.

### 3.8 Programme-ranking LLM call

The recommendation LLM receives one JSON payload containing:

- member branch;
- selected sectors and sector-specific skills;
- reason, schedule, language, and qualification preferences;
- every assigned profile's stored metadata and profile definition;
- actual cluster-forming answers, with survey question text;
- every assigned profile's `retained_evidence` items, including exact finding text, effect/interpretation guard, and provenance;
- the course-retrieval method and mandatory exact-skill coverage list;
- each candidate course's structured attributes and full verified course document;
- explicit boundaries separating user facts, historical cluster context, and course facts.

The LLM is asked to rank at most nine programmes and return evidence citations, a member-specific explanation, optional cluster context, and two or three programme-specific officer questions.

The current-context `validated_evidence` subset is not used. The payload builder explicitly prefers `entry.retained_evidence`.

### 3.9 Programme post-processing and validation

After the LLM responds, the backend:

- removes any course not in the retrieved candidate set;
- removes duplicate course IDs;
- removes a programme if it cites no actual member answer;
- removes a programme if a cited member answer does not match an actual submitted value;
- removes a programme if it cites no governed course fact;
- checks course-fact grounding with token overlap and exact number presence;
- keeps only cluster citations whose profile, variable, and exact finding text match the current 59-finding registry;
- removes an invalid or unsupported cluster summary without deleting an otherwise grounded course;
- removes technical or malformed discussion questions and supplements them with deterministic fallback questions;
- independently calculates visible schedule, language, and qualification conflicts;
- makes one additional LLM repair call if mandatory exact-skill courses were omitted;
- restores an omitted exact-skill course with deterministic catalogue wording if the repair still fails.

Finally, all mandatory exact-skill courses are moved ahead of non-mandatory courses, even if the LLM ranked another course higher. The displayed order is therefore not purely the LLM's ranking.

## 4. Research evidence audit

### 4.1 The four evidence levels currently being mixed together

| Evidence level | What it actually means | Source |
|---|---|---|
| Cluster-defining variables | Variables used in frozen distance calculation and nearest-medoid assignment | Original retained clustering outputs plus `CLUSTER_DEFINING_REGISTRY` and `MODEL_SPECS` |
| Final reported profiling findings | Post-cluster comparisons that passed the final report's reporting screen, including descriptive and conditional findings | Final profiling report, 17-row profile CSV, compiled profile documents |
| Programme-relevant findings | Final reported findings copied specifically into the profile CSV's `programme_relevant_findings` column | 17-row profile CSV |
| Current-context eligible findings | Programme-relevant findings that pass deterministic topic/direction rules for this intake | `filter_retained_evidence_for_context()` |

Only nearest-medoid reproduction accuracy is unambiguously a validated accuracy measure. Many final reported profiling findings are descriptive/exploratory rather than FDR-confirmed. Calling every retained profiling statement `validated` obscures this distinction.

### 4.2 Full reported set versus active production set

Deduplicating the five reported finding categories within each profile produces:

| Retained model | Profiles | Wizard corpus statements | Programme-registry statements | Additional wizard statements |
|---|---:|---:|---:|---:|
| D motivation | 3 | 3 | 3 | 0 |
| D household resources | 2 | 10 | 8 | 2 |
| D education background | 4 | 20 | 16 | 4 |
| E learning orientation | 2 | 14 | 8 | 6 |
| F employment security | 2 | 14 | 8 | 6 |
| G economic role | 2 | 14 | 8 | 6 |
| G future engagement | 2 | 14 | 8 | 6 |
| **Total** | **17** | **89** | **59** | **30** |

The 30 additional statements are now present in the wizard corpus while remaining excluded from programme-ranking evidence. They include programme-access guidance, primary-earner status, household size, application volume, minimum wage expectation, job training and employer payment, Branch F work type while studying, prior paid-work experience, locality, and expected minimum education for a decent job.

### 4.3 Statistical-strength warning

The compiled profile documents explicitly report these model-level FDR outcomes among screened findings:

| Model | Findings remaining significant after model-level FDR correction |
|---|---|
| D motivation | 0 of 1 |
| D household resources | 4 of 5 |
| D education background | 7 of 7 |
| E learning orientation | 0 of 15 |
| F employment security | 3 of 12; the separate work-type conditional finding also reached its targeted/sensitivity adjusted threshold |
| G economic role | 0 of 8 |
| G future engagement | 4 of 9 |

The final analysis intentionally uses effect size as its primary reporting screen, so lack of FDR significance does not mean a finding was fabricated or rejected. It does mean the frontend and prompts should distinguish `FDR-supported`, `reported descriptive`, and `conditional/sparse` rather than presenting all three as one undifferentiated class called validated evidence.

### 4.4 The context filter is calculated but bypassed

`build_profile_context()` calculates `validated_evidence` and `rejected_evidence`. Branch G duplicate topics are also resolved within that context-filtered collection.

For programme ranking:

- the programme payload builder prefers `entry.retained_evidence`;
- the recommendation authorization index is manually rebuilt from `entry.retained_evidence`.

The wizard no longer uses this path. It retrieves its separate 89-item corpus by exact assigned profile and known-answer context. The programme service still deliberately uses its separate programme registry; this change did not alter programme ranking.

### 4.5 What the teaching panel returns

The panel returns a model-specific sibling comparison, one clear conclusion per retained finding, and an evidence modal. The modal preserves exact counts, percentages, denominators, evidence status, effect size, FDR value, conditional flags, sparse-data cautions and provenance from the generated library. There is no runtime generation or statistical interpretation.

## 5. Active runtime files

### 5.1 Frontend

| File | Active role |
|---|---|
| `src/rag_prototype/frontend/src/App.tsx` | Intake state and programme submission |
| `frontend/src/steps/Step0Branch.tsx` | Direct branch selection |
| `frontend/src/steps/Step1ClusterQuestions.tsx` | Cluster-forming questionnaire and frontend completeness check |
| `frontend/src/steps/Step2Sector.tsx` | Multiple-sector selection |
| `frontend/src/steps/Step3ProgrammeQuestions.tsx` | Sector skills and Q2-Q5 |
| `frontend/src/steps/Step4Review.tsx` | Preview, assignment tree, teaching panel, and result tabs |
| `frontend/src/components/ClusterResearchTeachingPanel.tsx` | Assigned-profile sibling comparison and survey-evidence modal |
| `frontend/src/data/clusterResearchTeachingLibrary.json` | Generated 7-model/17-profile/89-finding teaching source |
| `frontend/src/components/ResultView.tsx` | Programme cards, cluster box, and card-back questions |
| `frontend/src/components/research-tree/*` | Branch/profile graph and click popovers |
| `frontend/src/api.ts` | Calls question-config, preview, and programme endpoints |
| `frontend/src/types.ts` | Active response types mixed with several older unused response structures |

### 5.2 Research-wizard retrieval

| File | Active role |
|---|---|
| `research_wizard_evidence_registry.py` | Explicit all-model wizard finding allowlist |
| `build_research_wizard_corpus.py` | Reproducibly validates and builds the 89-item corpus |
| `outputs/rag_cluster_research_wizard/findings.jsonl` | Finding-level governed retrieval documents |
| `outputs/rag_cluster_research_wizard/manifest.json` | Corpus/source hashes and evidence counts |
| `build_cluster_research_teaching_library.py` | Joins the authoritative sources and generates the one frontend teaching library |
| `frontend/src/data/clusterResearchTeachingLibrary.json` | Active model/profile teaching library with distributions, status and provenance |

### 5.3 Backend orchestration and LLMs

| File | Active role |
|---|---|
| `profile_explorer_app.py` | Flask app, question configuration, intake decoding, preview and paid programme endpoint |
| `new_respondent_cluster_assignment.py` | Frozen nearest-medoid assignment formulas and medoid loading |
| `new_person_profile_context.py` | Assignment-to-profile-document and evidence assembly |
| `retained_cluster_evidence_registry.py` | Cluster-variable registry, 59-statement allowlist, interpretation guards, and currently bypassed context filter |
| `profile_data_parser.py` | Parses the compiled profile documents |
| `cluster_catalogue.py` | Stored cluster codes, names, common descriptions, and tree metadata |
| `branch_d_profile_dossiers.py` | Branch D names/descriptions and an unnecessary runtime load of nine generated dossiers |
| `new_person_candidate_selection.py` | Active sector-scoped catalogue retrieval and exact-skill coverage |
| `new_person_context_pack.py` | Programme JSON payload and current ranking prompt |
| `officer_recommendation_service.py` | Recommendation orchestration, repair, validation, constraints, and fallbacks |
| `new_person_recommendation_schema.py` | Recommendation structured-output schema |
| `evidence_safeguards.py` | Exact member-answer and research-citation checks |
| `corpus_v2.py` | Course corpus count/hash verification |
| `context_pack_v2.py` | Active only for loading profile and course documents; its large older governance prompt is not the current programme prompt |
| `new_person_openai_client.py` | OpenAI structured Responses API wrapper |
| `env_config.py` | Hard-coded production model (`gpt-5-mini`) and API-key loading |
| `retrieval_v2.py` | Active path imports only `SECTOR_BRIDGE`; its BM25 retrieval code is legacy for this frontend |

### 5.4 Runtime research and assignment data

| File or directory | Active role |
|---|---|
| Seven medoid CSVs under `outputs/*_clusters/` | Frozen assignment reference patterns |
| `outputs/rag_profile_knowledge/profile_document_index.csv` | Maps all 17 profile keys to documents |
| `outputs/rag_profile_knowledge/documents/*.txt` | Compiled full research documents read and parsed at runtime |
| `outputs/final_cluster_programme_relevant_profiles.csv` | Exact source for the active 59 finding texts |
| `outputs/final_cluster_profile_comparison_summary.csv` | Statistical-detail/provenance source used through compiled documents and registry metadata |
| `outputs/nysc_survey_feature_manifest.csv` | Survey question IDs and wording |
| `outputs/rag_branch_d_profile_dossiers/*.json` | Loaded for Branch D even though not used by active LLM payloads |

The seven exact frozen medoid files read during assignment are:

1. `outputs/branch_d_motivation_clusters/motivation_medoid_profiles.csv`
2. `outputs/branch_d_economic_resources_clusters/economic_final_profile_gower_medoids.csv`
3. `outputs/branch_d_educational_cultural_capital_clusters/educational_cultural_final_profile_gower_medoids.csv`
4. `outputs/branch_e_all_dimensions_clusters/e4/e4_final_profile_gower_medoids.csv`
5. `outputs/branch_f_employment_security_clusters/employment_security_final_profile_gower_medoids.csv`
6. `outputs/branch_g_household_economic_resources_clusters/household_economic_final_profile_gower_medoids.csv`
7. `outputs/branch_g_inactivity_pathway_future_engagement_clusters/pathway_engagement_final_profile_gower_medoids.csv`

### 5.5 Runtime course data

| File or directory | Active role |
|---|---|
| `outputs/rag_new_person_intake_v1/course_matching_layer.csv` | Course-to-skill-area and structured delivery fields |
| `outputs/rag_new_person_intake_v1/q1_occupation_options_by_skill_area.json` | Selectable skills/course names |
| `outputs/rag_course_knowledge/final_rag_corpus_v2_manifest.csv` | 84-course manifest and document hashes |
| `outputs/rag_course_knowledge/final_rag_corpus_v2_exclusions.csv` | Four excluded course records |
| `outputs/rag_course_knowledge/final_rag_corpus_v2/*.txt` | Full course documents sent to the ranking LLM |

## 6. Research source and generated-copy files

These files explain provenance but are not all read directly during each request:

| File | Role |
|---|---|
| `30_final_cluster_profile_analysis.ipynb` | Generates the final comparison CSV, profile CSV, and markdown report |
| `final_cluster_profiling_report.md` | Human-readable final post-cluster profiling report |
| `NYSC_all_branches_clustering_final_report.md` | Final retained-model definitions and validation decisions |
| `NYSC_Final_Clustering_and_Post_Cluster_Profiling_Report.docx` | Combined clustering/profiling report and Branch F conditional finding |
| `outputs/rag_profile_knowledge/profile_knowledge_report.md` | Documents how the 17 profile text files were compiled |
| `outputs/fixed_medoid_assignment_validation/*` | Published assignment-reproduction evidence; runtime accuracy values are duplicated in Python rather than loaded from this CSV |

No source script that rebuilds `outputs/rag_profile_knowledge/documents/*.txt` and `profile_document_index.csv` was found in the repository. The generated documents and build report exist, but their generating implementation is missing. This is a reproducibility risk.

## 7. Legacy and confusing paths

- `context_pack_v2.py` contains a much older, very long recommendation prompt. The active officer ranking prompt is `RANKING_INSTRUCTIONS` in `new_person_context_pack.py`.
- `retrieval_v2.py` contains BM25 retrieval for an earlier respondent experiment. The active officer flow does not call it.
- `new_person_candidate_selection.py` still contains the older `select_candidates()` points-based top-eight method below the active `retrieve_sector_catalogue()` method. The active officer service calls only `retrieve_sector_catalogue()`.
- `profile_explorer_app.py` still contains the old explorer endpoints and a `_legacy_api_new_person_recommend()` serializer alongside the active API.
- `frontend/src/types.ts` retains old recommendation, finding, distribution, and briefing interfaces that are no longer returned by the active React flow.
- compiled `__pycache__` files refer to `research_insight_retrieval.py`, but that source file is absent and is not part of the active flow.

These files do not necessarily change current results, but they make it difficult to identify the source of truth.

## 8. LLM-call count and persistence

For one initial respondent flow:

- free assignment preview: no LLM call;
- teaching panel: no API or LLM call;
- programme ranking: normally one call;
- programme ranking repair: one additional call when exact selected-skill coverage is omitted.

Therefore an initial completed flow makes one paid call normally, or two when programme-ranking repair is required. Reopening or reloading the teaching panel reads the same bundled source and has no model cost.

## 9. Audit findings by priority

### High priority

1. **Resolved for the wizard: the evidence name and scope were misleading.** The wizard now has a separate 89-item corpus with `fdr_supported` versus `retained_descriptive` status. The programme registry remains a narrower 59-item subset by design.
2. **The context filter is dead in production.** It is calculated and tested independently, then bypassed by both active LLM payloads and the recommendation authorization index.
3. **Resolved: the wizard used the wrong evidence scope.** It now receives every final reported finding for the assigned profiles from a hashed corpus.
4. **Backend assignment input is incomplete-validation dependent.** UI completeness is enforced, but the API does not require every model variable before assigning.
5. **The generated profile knowledge base is not reproducibly buildable from a checked-in source script.**
6. **Runtime depends on the untracked `outputs/` tree.** Git currently reports the whole directory as untracked; a clean checkout would not contain required medoids, research documents, or course documents unless they are supplied separately.
7. **The current teaching-panel implementation is also untracked.** Git reports the generated teaching library, generator, component and tests as working-tree additions, while several active recommendation and frontend files are modified. The behaviour audited here therefore exists in the working tree but is not reproducible from the current committed revision alone.

### Medium priority

8. **Resolved for the teaching panel: no runtime RAG is required.** The research set is frozen and small, so the panel performs an exact assigned-profile lookup in the generated model/profile library and preserves every retained finding.
9. **The course side is deterministic scope retrieval, not BM25/vector RAG.** The LLM receives every course in mapped areas, potentially dozens of full documents.
10. **Final displayed programme order is hybrid.** Mandatory exact-skill courses are moved above other LLM-ranked courses, and deterministic fallback cards may be inserted.
11. **Resolved: research results do not require caching.** The complete teaching library is bundled with the frontend, so tab changes and full reloads do not make a research-content request.
12. **Branch D has an unused generated-dossier runtime dependency.**
13. **Several active constants duplicate frozen files.** Question lists, published accuracies, profile names, and descriptions can drift from their source artefacts.
14. **Legacy code and active code coexist in the same modules.** This is the main reason multiple prompts and retrieval descriptions appear to be current when they are not.

### Strengths that should be preserved

- frozen medoids are not retrained;
- assignment reproduction is tested;
- course corpus count and hashes are mechanically verified;
- arbitrary raw survey distributions are not sent to the active LLMs;
- member facts, group findings, and course facts are represented separately in the programme payload;
- exact member-answer and exact research-citation checks exist;
- exact selected course interests cannot silently disappear;
- schedule, language, and qualification conflicts are calculated outside the LLM;
- the frontend build and current offline regression checks pass.

## 10. Safe correction order

The wizard-specific evidence registry, corpus, retrieval, prompt, validation, and same-session caching steps below are now implemented. Remaining work should follow this order:

1. freeze and label the current behaviour with regression snapshots;
2. add backend completeness validation for branch/model assignment inputs;
3. keep the new wizard inventory and generated corpus reproducible as research inputs evolve;
4. preserve the wizard/programme evidence separation unless a reviewed research decision changes it;
5. decide deliberately whether programme ranking should use all programme-retained findings or the already-implemented current-context filter;
6. remove the unused Branch D dossier load and separate legacy modules from production modules;
7. decide whether the new privacy-preserving session-memory wizard cache should later become server-side persistent caching; tab changes and same-session revisits are already covered;
8. only after those are stable, consider changing catalogue retrieval or recommendation ranking.

## 11. Verification performed during this audit

The following checks completed successfully:

- nearest-medoid assignment reproduction test;
- governed evidence-selection offline test: 7 models, 17 profiles, 59 active statements;
- cluster-wizard mocked service test;
- context-aware ranking mocked service test;
- exact selected-skill coverage test;
- multiple-sector validation test;
- programme discussion-question test;
- React/TypeScript production build;
- frontend lint completed with one existing React warning in `Step4Review.tsx` about setting tab state synchronously inside an effect.

Passing these tests means the code behaves as currently specified. It does not remove the architectural findings above; several tests explicitly expect the narrower 59-finding registry and full-registry delivery to the LLM.
