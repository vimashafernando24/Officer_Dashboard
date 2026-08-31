# Controlled Second API Experiment — Three-Way Comparison Report

**Question this experiment answers:** was the gpt-4o-mini run's under-recommendation problem
caused by weak retrieval, or by the model/prompt being excessively conservative? **Answer: the
model/prompt.** Retrieval, the 84-course corpus, respondent evidence, and profile evidence were
all held **byte-for-byte identical** to the first API run (the retrieval bundle was loaded from
disk and reused, not recomputed). Only two things changed: the governance prompt was rebalanced,
and the model was upgraded from `gpt-4o-mini` to `gpt-5-mini`. With retrieval held constant,
recommendation coverage went from 2/10 respondents to 10/10 respondents, and every course the
gpt-4o-mini run had inaccurately declined despite it being directly retrieved is now recommended.

---

## 1. What changed (LLM decision layer only)

| Component | Unchanged | Changed |
|---|---|---|
| 84-course V2 corpus | ✓ (re-verified via SHA-256, identical) | |
| BM25 retrieval / retrieved candidate sets | ✓ (loaded from the first run's saved `_v2_respondent_bundle.json`, not recomputed) | |
| Respondent evidence, profile evidence | ✓ | |
| Grounding audit | | **Extended** to also audit `NO_DEFENSIBLE_RECOMMENDATION` reasons (previously only actual recommendations were audited) |
| Governance prompt (`context_pack_v2.GOVERNANCE_INSTRUCTIONS`) | | **Rebalanced**: added an explicit decision standard ("recommend what appears suitable, not what is provably eligible"; missing info = uncertainty, not negative evidence; reserve decline for genuine non-matches; don't reject over unconfirmed fee/location/schedule/eligibility), strengthened the no-unsupported-eligibility rule to cover both positive and negative claims, added a new explicit prohibition against declining a well-matched course solely over an undocumented attribute |
| Model | | `gpt-4o-mini` → **`gpt-5-mini`** (reasoning-tier, cost-conscious; `reasoning={"effort":"low"}` for speed/cost; no `temperature` override, since reasoning models reject a custom value) |
| Client robustness | | Added a 120s explicit request timeout (the SDK default is 600s, which combined with retries could otherwise block ~40 min on a single hanging respondent) and skip-retry-on-non-transient-errors (auth/bad-request failures no longer burn 3 pointless retries) |

## 2. Headline numbers

| Metric | Manual (Claude reasoning) | gpt-4o-mini (run 1) | **gpt-5-mini (run 2)** |
|---|---:|---:|---:|
| Total recommendations (10 respondents) | 19 | 4 | **35** |
| Respondents with ≥1 recommendation | 8/10 | 2/10 | **10/10** |
| `NO_DEFENSIBLE_RECOMMENDATION` count | 2/10 | 8/10 | **0/10** |
| Grounding audit — real FAIL count | n/a (not API-audited) | 1 (00e2c251 unsupported eligibility claim, confirmed real) | **0** (after fixing a false-positive in the audit itself — see §4) |
| Grounding audit — PASS WITH CAUTION | n/a | 0 | 3 (all low-severity paraphrase/word-overlap flags, reviewed below) |
| API cost (this 10-respondent run) | $0 (no API) | $0.036 | **$0.075** |
| Projected cost for 362 respondents | — | ~$1.29 | **~$2.72** (both ESTIMATED from published list pricing, not live-billed) |
| Avg. call duration | — | ~fast (gpt-4o-mini) | 41s avg, 74s max (reasoning model; noticeably slower) |

## 3. Did the previously-missed matches come back?

Every course this project's own report identified as an inaccurate gpt-4o-mini decline is now
recommended:

| Respondent | Previously missed (gpt-4o-mini declined despite retrieval) | gpt-5-mini result |
|---|---|---|
| `acaf63b5` | `COURSE-049` Business Managemant | ✅ recommended (+ `COURSE-006`, `COURSE-071`) |
| `00e2c251` | `COURSE-019` Quantity Surveying Assistant, `COURSE-023` Construction Site Supervisor | ✅ both recommended (+2 more) |
| `55bdfdcc` | `COURSE-007` Professional Cookery, `COURSE-011` Baker, `COURSE-050` Cake & Cake Structure, `COURSE-049` Business Managemant | ✅ all 4 recommended |
| `33aaf2f7` | `COURSE-008` Computer Hardware Technician | ✅ recommended (+4 more) |
| `346623df` | `COURSE-006` ICT Diploma (declined for "start own business" framing) | ✅ recommended (+3 more) |

Full detail in `three_way_comparison.csv`.

## 4. A finding about the audit itself, not the model

The first extended-audit pass on the gpt-5-mini output showed 2 "FAIL"s (`a04f7d96`, `465701ee`),
both flagged for containing the phrase "guaranteed employment." Reading the actual text: both
instances read *"Recommendation does not imply guaranteed employment..."* and *"No explicit
statement about career placement or guaranteed employment outcomes..."* — the model was
**correctly disclaiming** exactly the prohibited claim, not making it. The mechanical audit's
naive substring match didn't check for negation. This was fixed
(`grounding_audit_v2._banned_phrase_issues` now checks a 60-character window before each banned
phrase for negation cues like "does not imply," "no explicit," "not guarantee") and both runs were
re-audited (pure re-analysis of already-saved text, no new API calls). **Result after the fix: 0
real FAILs in the gpt-5-mini run.** The gpt-4o-mini run's one real FAIL (`00e2c251`'s
self-contradicting eligibility claim, "not explicitly stated but can be inferred") is unaffected
by this fix and remains confirmed as a genuine issue — that check doesn't depend on phrase
negation.

This is disclosed because it's a real limitation of a still-imperfect mechanical audit, not
because it changes the bottom line: gpt-5-mini's actual behaviour on both flagged items was
already correct before the audit was fixed.

## 5. The 3 remaining PASS WITH CAUTION items

All three are the approximate word-overlap check on `course_evidence_used` text, which is
deliberately lenient-but-flagging (not a fail) because paraphrase is expected:

- `3a86d117` and `346623df`, both re: `COURSE-001` (Freelancer of Web Design & Development) —
  the model's summary ("teaches web development, hosting, domain management, and how to earn via
  [freelance platforms]") is a legitimate paraphrase of the source text, just with different
  wording than the raw document; manually confirmed accurate, not fabricated.
- `0c6c34a2` re: `COURSE-034` — the model's course_fact text references "one retrieved variant
  (COURSE-012)" while discussing `COURSE-034`, comparing two near-duplicate Refrigeration & AC
  Technician course records in the corpus. Legitimate cross-referencing, not a fabrication, but
  worth a human glance since it's citing a fact from a *different* course_id than the one being
  recommended.

None of these three are unsupported-fact violations on manual review.

## 6. Scrutiny of the two weak-evidence respondents (the key risk this experiment needed to check)

Both `a04f7d96` and `465701ee` correctly returned `NO_DEFENSIBLE_RECOMMENDATION` under
gpt-4o-mini. Under the rebalanced prompt + gpt-5-mini, both now get a recommendation. Is this
evidence-supported or an over-correction?

- **`a04f7d96`**: 1 recommendation (`COURSE-006`, ICT Diploma), rated **MODERATE** (not STRONG).
  Cited evidence: `already_job_searching=Yes`, `job_search_method_d=Online job ads`,
  `plans_after_education=Look for a job`, `study_field_preference=Other field`. The model's own
  `uncertainties` field states outright: *"The respondent did not explicitly state an interest in
  ICT or computing; the recommendation relies on the respondent's job-seeking behaviour and
  openness to 'Other field' rather than a direct declared ICT preference."* This is honest,
  appropriately hedged, and does not overstate the evidence — a defensible call given the new
  instruction to recommend when *any* reasonable connection exists, but it is genuinely a thin
  connection and a reviewer should treat MODERATE-strength recommendations like this one as
  needing more scrutiny than STRONG ones.

- **`465701ee`**: 2 recommendations. The first (`COURSE-006`, rated **STRONG**) cites
  `most_useful_quality_for_job = "IT and digital skills"` as its lead justification. This is a
  genuine problem worth flagging: `most_useful_quality_for_job` is a general OPINION question
  ("which quality do you think is most useful for finding a good job") that this project's own
  evidence-policy audit classified as `INDIVIDUAL_CONTEXT_ONLY` specifically because it is a
  belief about the job market in general, not a personal preference statement about what the
  respondent wants to study — and the prompt does present it under the "INDIVIDUAL CONTEXT ONLY
  (...must not independently drive ranking)" section header. The model used it anyway as primary
  justification for a STRONG rating. This is **not caught by the current mechanical audit**
  (which only checks that a cited variable exists and its value isn't contradicted, not which
  evidence-category section it was drawn from) and is a concrete gap worth closing before scaling
  (see §8).

**Verdict on this section:** the rebalanced prompt did not cause fabrication or protected-field
misuse in either weak-evidence case, but it did surface one real category-discipline gap
(opinion-as-preference) that the audit should be extended to catch.

## 7. Reproducibility & cost

- Deterministic retrieval (BM25) was reused unchanged; the LLM call itself is not bit-for-bit
  reproducible (reasoning-model sampling), but architecture and inputs are fully reproducible.
- `gpt-5-mini` calls averaged 41s (max 74s) versus gpt-4o-mini's sub-second-to-few-second
  latency — a real operational cost of the stronger model, worth planning for at 362-respondent
  scale (362 × ~41s sequential ≈ 4.1 hours; parallelising calls would be needed for a practical
  full run).
- Cost: **ESTIMATED** $0.075 for this 10-respondent run and **ESTIMATED** ~$2.72 for 362
  respondents, computed from actual recorded token usage (234,232 input / 29,570 output tokens,
  including 2,688 reasoning tokens) against `gpt-5-mini`'s published list pricing ($0.25/1M input,
  $2.00/1M output, ~$0.025/1M for the 188,928 cached input tokens). This is **not** a live
  OpenAI billing-API figure — labelled ESTIMATED throughout, consistent with the first run's
  reporting convention.

## 8. Fixes still worth making before a full-scale run

1. **Extend the mechanical audit to check evidence-category discipline**: verify that a
   `direct_respondent_evidence_used` citation actually comes from a variable classified
   `DIRECT_PREFERENCE_OR_INTENT` (or at least flag citations drawn from
   `INDIVIDUAL_CONTEXT_ONLY`/`EDUCATION_AND_EXPERIENCE_CONTEXT` variables presented as if they
   were a stated preference) — directly motivated by the `465701ee` finding in §6.
2. **Watch total recommendation volume**: 35 recommendations across 10 respondents (avg. 3.5) is
   noticeably higher than the manual baseline's 19 (avg. 2.4 among the 8 who got any). Nothing in
   this run's audit suggests genuine over-recommendation, but this is worth monitoring in a larger
   sample — the fix for under-recommendation should not silently become a new bias toward
   recommending too liberally.
3. **Plan for latency/parallelism** if scaling to 362 respondents — sequential gpt-5-mini calls at
   this rate would take several hours; batching or concurrent calls (with rate-limit-aware
   retries) would be needed.
4. Continue monitoring the negation-aware banned-phrase check and the eligibility-claim check on
   a larger sample to confirm the audit fix generalises.

---

## Verdict

The evidence in this experiment directly answers the assigned question:
**the under-recommendation problem in the first run was caused by the gpt-4o-mini
model/prompt combination, not by BM25 retrieval or the course corpus** — retrieval and corpus
were held constant and coverage went from 2/10 to 10/10, recovering every specific course this
project had documented as an inaccurate miss.

The rebalanced prompt + `gpt-5-mini` combination is a substantial, evidence-backed improvement.
It is not yet flawless (one real audit-catchable category-discipline gap found in §6, one
mechanical-audit bug found and fixed in §4, recommendation volume running somewhat higher than the
manual baseline) — but none of these are fabrication, protected-field misuse, or excluded-course
risks. This run is **materially closer to ready for a controlled full-scale run** than the first
API run was, pending the audit extension in §8.1 and a latency/cost plan for 362 respondents.
