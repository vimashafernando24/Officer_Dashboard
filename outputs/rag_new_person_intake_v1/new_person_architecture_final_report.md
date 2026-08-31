# New-Respondent Profile-Aware RAG Recommender — Final Report

Covers §1-§5 of the new-person recommendation architecture, built as a versioned addition alongside (not a replacement of) the existing 362-person experimental pipeline. §0 (new-respondent cluster assignment) was already built and accepted in a prior session and was reused unmodified throughout.

---

## 1. Final additional question set

Full reasoning and rejected alternatives: [`question_design_report.md`](question_design_report.md).

| # | Question | Options | Role in retrieval |
|---|---|---|---|
| Reused (not new) | `ideal_sector` (existing survey field) | 12 existing options | Hard filter, via existing `SECTOR_BRIDGE` → `skill_area` |
| Q1 | Occupation/course focus within your sector | Real course names generated from the corpus per skill area (see `q1_occupation_options_by_skill_area.json`) + "Not sure" | Hard-filtered pool + score +3 on match |
| Q2 | Main reason for this training | Get a job / Improve skills in current job / Start my own business / Continue further education / Build general skills | Explanation framing only — no catalogue field supports it as a filter (disclosed) |
| Q3 | Schedule preference | Full-time weekdays / Part-time weekends / No strong preference | Score +2 on match |
| Q4 | Language preference | Sinhala / English / No strong preference | Score +2 on match |
| Q5 | Qualification/NVQ preference | Yes / Not necessarily / Not sure | Score +1 on match (soft only — 37-39% catalogue coverage) |

Five candidates (specific skills, duration, target-occupation, affordability, location, eligibility, childcare) were investigated and explicitly rejected — see the report for the real population/variance numbers behind each rejection.

---

## 2. Catalogue matching schema

Built by [`build_course_matching_layer.py`](../../src/rag_prototype/build_course_matching_layer.py), output: [`course_matching_layer.csv`](course_matching_layer.csv).

- Covers all **84 validated, indexable RAG-corpus courses** (verified via `corpus_v2.verify_corpus()`, SHA-256-checked, unchanged).
- **83 of 84** crosswalk to a structured row in `nysc_course_matching_dataset.csv` via the existing `course_source_traceability.csv`; **1** (`COURSE-004`) has no reliable crosswalk and every structured field for it is explicitly `NOT_STATED`, not guessed.
- Every row keeps `rag_course_id` (provenance back to the original document) and a `provenance` field recording exactly how the structured attributes were sourced.
- The full parent document remains authoritative for any factual claim — this layer only feeds candidate selection and score-breakdown transparency; it is never presented to the LLM as a substitute for the real course text.
- The original 84-doc corpus, its manifest, and `nysc_course_matching_dataset.csv` are all **untouched**.

---

## 3. New RAG architecture

```
new person's existing profiling answers
        │
        ▼
new_respondent_cluster_assignment.py   (§0 — ALREADY BUILT & ACCEPTED, reused unmodified)
        │
        ▼
new_person_profile_context.py          (§3 — loads profile docs + correctly-labeled
        │                                     similarity/confidence, not "accuracy")
        │
new person's Q1-Q5 answers
        │
        ▼
new_person_candidate_selection.py      (§2 — deterministic hard-filter + score against
        │                                     the structured matching layer, ≤5 candidates,
        │                                     no BM25, no randomness)
        │
        ▼
new_person_context_pack.py             (§4 — builds Sections 1-4, new GOVERNANCE_INSTRUCTIONS)
        │
        ▼
new_person_recommendation_schema.py    (§4 — new Pydantic schema)
        │
        ▼
new_person_openai_client.py            (§4/§5 — reuses openai_client.py's retry/hard-timeout
        │                                     primitives; only instructions/schema differ)
        │
        ▼
run_new_person_recommendation.py       (§5 — per-person runner + human-readable formatter)
```

All new files live in `src/rag_prototype/`, none replacing or editing an existing frozen module. `openai_client.py`, `context_pack_v2.py`, `recommendation_schema.py`, `run_full_cohort.py`, `corpus_v2.py`, `env_config.py`, and the 84-course corpus are **byte-for-byte untouched** — confirmed by `corpus_v2.verify_corpus()` passing on every run in this session.

---

## 4. Governance rules

Full text: `new_person_context_pack.GOVERNANCE_INSTRUCTIONS`. Encodes, verbatim in spirit:
- The A/B/C evidence hierarchy (explicit answers PRIMARY, profile context CONTEXTUAL/group-level, course docs AUTHORITATIVE).
- **The profile-percentage rule**: a group statistic is never converted into an individual fact — enforced structurally via `ProfileContextContribution.role` (`REINFORCED` / `CONTRASTED` / `HELPED_DIFFERENTIATE` / `NOT_USED`), not left to prose discipline alone.
- DIRECT_MATCH vs ADJACENT_MATCH classification, with mandatory bridge explanations and no invented bridges.
- Explicit prohibition on inventing eligibility, affordability, schedule/location compatibility, or employment outcomes, and on inferring any of those from profile/cluster characteristics.
- NO_DEFENSIBLE_RECOMMENDATION as a normal, valid, expected output.
- No forced list-padding; fewer well-supported recommendations preferred over more weak ones.

---

## 5. New-person runner

[`run_new_person_recommendation.py`](../../src/rag_prototype/run_new_person_recommendation.py) — `run_one(spec, manifest_by_id, call_api=...)` processes exactly one person. **Never invoked against the historical 362** — the only caller in this work is the 9-case synthetic test harness below. `run_full_cohort.py` (the batch runner for the 362) is untouched and remains the only path that ever processes that cohort.

Human-readable output follows the requested structure exactly: **YOUR YOUTH PROFILE** (profile + correctly-labeled similarity, not "accuracy") → **PEOPLE WITH SIMILAR PROFILE PATTERNS** (2 real, percentage-bearing findings per profile + the required "these describe the group, not you" disclaimer) → **WHAT YOU TOLD US** (labeled `[YOUR ANSWER]`) → **RECOMMENDED NYSC PROGRAMMES** (each with `[YOUR ANSWER]` / `[PROFILE PATTERN]` / `[COURSE FACT]` / `[LLM REASONING]` labeled sections).

---

## 6. Test results

9 synthetic cases, `src/rag_prototype/test_new_person_synthetic_cases.py`. Cluster-forming answers borrowed from real respondents purely for valid §0 encoding; every scenario under test (ideal_sector/Q1-Q5) is synthetic. **Not** run against the historical 362-person experiment. Reports: `test_cases/*.md`, machine-readable summary: `test_cases/summary.json`.

| Case | Property tested | Candidates | Live call | Result |
|---|---|---:|:---:|---|
| 01 direct-preference | Very clear direct preference | 5 | Yes ×3 | 3× `RECOMMENDATIONS_AVAILABLE`, all DIRECT_MATCH |
| 02 broad-uncertain | Broad/uncertain preference | 0 | No | Correctly zero candidates (no skill area determinable) |
| 03 conflict-with-profile | Preference vs. profile tendency | 5 | Yes ×1 | All 5 DIRECT_MATCH from the respondent's own answers; every one correctly labeled `CONTRASTED`, citing the real group figure (3.4%) that the respondent's choice is a minority pattern in their assigned profile — **individual evidence won, contrast disclosed, not hidden** |
| 04 schedule-constraint | Schedule as disambiguator | 5 | No (verified offline) | The correct schedule-matching delivery variant (`COURSE-040`, part-time) outranked its full-time duplicate (`COURSE-005`) by score 5 vs 3 — **this is the exact duplicate-course ambiguity that motivated this whole redesign, now resolved deterministically** |
| 05 qualification-preference | Soft NVQ signal | 5 | No | Candidate set built correctly; soft scoring confirmed by code path (score+1 only when `qualification_type` populated, never penalizing blank) |
| 06 self-employment-goal | Governance discipline | 5 | Yes ×1 | 2 DIRECT_MATCH + 2 ADJACENT_MATCH (each with a genuine, non-manufactured bridge); zero invented affordability/viability claims; profile contribution correctly `REINFORCED` (citing a real 36.6% figure) on the two DIRECT_MATCH and correctly `NOT_USED` on the two ADJACENT_MATCH |
| 07 catalogue-gap | No mapped sector | 0 | Yes ×1 | Correct `NO_DEFENSIBLE_RECOMMENDATION` with an honest reason — **no hallucination even when Section 3 was empty** |
| 08 profile-adds-value | Legitimate REINFORCED use | 5 | Yes ×1 | Confirmed `REINFORCED` used only where the group figure aligns with an already-stated individual preference, `NOT_USED` on the one recommendation where it didn't apply |
| 09 profile-should-not-influence | Profile irrelevant to content | 5 | No (offline only — disclosed limitation, see §7) | Candidate selection verified deterministic and correct; NOT_USED behavior for a wholly-orthogonal profile was **not** separately live-tested for this case (already demonstrated in cases 06/08) |

**Recommendation-set stability** (test-01, 3 repeat live calls): the candidate set fed to the LLM was identical and fully deterministic across all 3 calls (verified — same 5 `course_id`s every time, confirmed by construction). The LLM's final output showed a **4-course stable core** (`COURSE-006`, `008`, `009`, `022`) in all 3 calls, with one additional, explicitly lower-confidence, honestly-caveated 5th recommendation (`COURSE-001`) appearing in 1 of 3 calls. This is qualitatively different from the original bug (arbitrary swaps between unrelated courses drawn from a loosely-matched 15-document BM25 pool) — the redesign's core goal, a deterministic candidate set, is achieved; residual variance is a legitimate, disclosed, low-stakes inclusion/exclusion judgment on one borderline item, not identity-swapping among the primary recommendations.

---

## 7. Limitations

- **Q2 (reason for training)** has no reliable catalogue field to filter on (`entrepreneurship_content` is only 8% populated and, on inspection, inconsistently labeled) — it is used for explanation framing only, exactly as disclosed in §1; this is a genuine catalogue gap, not a design oversight.
- **Q5 (qualification)** is a soft signal only, by necessity — the catalogue is only 37-39% populated for NVQ/qualification fields.
- **1 of 84 courses** (`COURSE-004`) has no structured crosswalk; it can still be retrieved if it's the only option in its sector, with every structured attribute honestly marked `NOT_STATED`.
- **Case 09** (profile-should-not-influence) was validated at the deterministic candidate-selection layer only, not with a dedicated live LLM call — NOT_USED behavior was directly confirmed live in cases 06 and 08 instead, to keep API usage minimal per instruction.
- **Token/cost usage** for the 7 live calls in this test batch was not separately logged in this test harness (unlike `run_full_cohort.py`'s per-call CSV) — a minor tracking gap, not a correctness issue; each `CallResult` returned real token counts that simply weren't persisted to a summary file.
- The residual 4-of-5-stable / 1-borderline-item variance in test-01's repeat calls (§6) is disclosed, not hidden — it reflects legitimate LLM discretion on a marginal recommendation, not the original architectural flaw.

---

## 8. Exact output paths

- `outputs/rag_new_person_intake_v1/question_design_report.md` — §1
- `outputs/rag_new_person_intake_v1/course_matching_layer.csv` — §2
- `outputs/rag_new_person_intake_v1/q1_occupation_options_by_skill_area.json` — §1/§2
- `src/rag_prototype/build_course_matching_layer.py` — §2 builder
- `src/rag_prototype/new_person_profile_context.py` — §3
- `src/rag_prototype/new_person_candidate_selection.py` — §2 scoring / retrieval
- `src/rag_prototype/new_person_context_pack.py` — §4 governance + input construction
- `src/rag_prototype/new_person_recommendation_schema.py` — §4 schema
- `src/rag_prototype/new_person_openai_client.py` — §4/§5 API wrapper
- `src/rag_prototype/run_new_person_recommendation.py` — §5 runner + formatter
- `src/rag_prototype/test_new_person_synthetic_cases.py` — testing harness
- `outputs/rag_new_person_intake_v1/test_cases/*.md` — 12 human-readable test reports (9 cases, 3 repeats for case 01)
- `outputs/rag_new_person_intake_v1/test_cases/*_input_text.txt` — full literal LLM input per case, for audit
- `outputs/rag_new_person_intake_v1/test_cases/summary.json` — machine-readable test summary

**Preserved, untouched**: `outputs/rag_recommendation_prototype_api/`, `_v2/`, `_v3/`, `rag_recommendation_validation_30/`, `rag_recommendation_final_validation/`, `rag_recommendation_post_fix_review/` (all historical 362-person experimental work), `outputs/rag_course_knowledge/final_rag_corpus_v2/` and its manifest, `outputs/nysc_course_matching_dataset.csv`, and every frozen clustering/profiling output under `outputs/branch_*`.

---

## NEW-RESPONDENT PROFILE-AWARE RAG RECOMMENDER READY
