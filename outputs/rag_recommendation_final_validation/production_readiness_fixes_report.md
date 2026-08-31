# Production-Readiness Fixes — Report

**No API calls were made in this task.** All fixes are code/prompt/audit changes;
all audit results below are re-analysis of already-saved data (the 10-respondent final
targeted validation, cross-checked for regressions against the 30-person batch and the
frozen 10-person v3 baseline). No validation respondent was re-run.

---

## 1. `.env`/model configuration — FIXED

**Problem confirmed:** `openai_client.call_recommendation_api()` had a silent fallback —
`model = model or get_recommendation_model()` — where `get_recommendation_model()` reads
`.env`'s `OPENAI_RECOMMENDATION_MODEL`. Every script written so far happened to pass
`model=` explicitly, so this fallback was never actually triggered in practice, but it
was a live landmine: any future caller (e.g. a careless edit to the full-cohort runner)
that omitted the `model` argument would have silently used whatever `.env` said —
currently `gpt-4o-mini`, not `gpt-5-mini`.

**Fix — one authoritative mechanism, hardcoded:**
- `env_config.py` now defines `PRODUCTION_RECOMMENDATION_MODEL = "gpt-5-mini"` as a
  hardcoded constant, and `get_production_model()` returns it — **`.env` is never
  consulted for this value.**
- `env_config.verify_production_model(selected_model)` prints the selected model name
  and raises `SystemExit` unless it is exactly `"gpt-5-mini"`. Verified directly (no
  API call): prints `Selected model for this run: gpt-5-mini` and passes for the
  correct model; prints `Selected model for this run: gpt-4o-mini` and aborts with a
  clear message for the wrong one.
- `openai_client.call_recommendation_api()`'s silent fallback is **removed entirely** —
  `model` is now a required positional argument with no default; passing `None`/empty
  raises `ValueError` immediately. There is no code path left that can silently select
  a model.
- `get_recommendation_model()` (the old `.env`-driven getter) is kept, but only for the
  two already-completed historical experimental scripts that used it
  (`run_api_pipeline.py`, `run_experiment_v2.py`); it is documented as deprecated and is
  not called anywhere in the production path.
- The new `run_full_cohort.py` (§6) calls `verify_production_model()` as its literal
  first step, before touching the corpus, retrieval, or API key.

**`.env` itself was left as found** (`OPENAI_RECOMMENDATION_MODEL=gpt-4o-mini`) — not
silently corrected, per the standing instruction not to modify files whose changes look
unexpected without saying so. It no longer matters for production regardless: the
production path never reads it. **You may still want to find out who/what changed it**,
since any *other*, non-production script that still calls the deprecated getter would
be affected.

## 2. Economic-profile-affordability rule — FIXED (governance rule tightened, audit tightened, both verified)

**Problem:** the previous rule allowed profile-level economic context to be "discussed
cautiously, explicitly labelled as group-level" — an escape valve that both the model
and my own audit exploited: `nysc-8ae4a1d8`'s citation added a hedge ("...but this is
group-level context only") and was accordingly downgraded to a caution rather than
flagged as a real problem.

**Fix:**
- `context_pack_v2.py`: the rule is now an **absolute prohibition with no hedging
  exception** — any economic/resource-profile citation touching affordability, fee-
  paying capacity, or ability/inability to pay is prohibited outright, "regardless of
  hedging." The rule explicitly instructs: if there's no reason to mention
  affordability, omit the topic entirely rather than reach for a hedged version of it.
- `evidence_hierarchy_audit.py`'s `check_economic_profile_affordability()`: the
  caution-downgrade path is removed. Any affordability-pattern match in an
  economic/resource-profile citation is now a straight FAIL — no exceptions.

**Re-audited against the saved final-validation output (no new calls):**
`nysc-8ae4a1d8`/COURSE-068 — previously PASS WITH CAUTION — is now correctly **FAIL**
under the tightened rule. `nysc-4e38db03`/COURSE-006 remains **FAIL** (unhedged, was
already failing). **Evidence-hierarchy audit result: 41 PASS, 0 CAUTION, 2 FAIL.**

**Important, honest caveat:** these 2 FAILs are *known, already-reported* instances in
data generated *before* this prompt tightening — they cannot be regenerated without a
new API call, which this task prohibits. The tightened prompt has not yet been tested
against a live call. **This is not a blocker, but it is a genuine open question**: does
the stronger wording actually stop the model from producing *new* instances of this
pattern, or only get correctly flagged after the fact? Recommend watching the
evidence-hierarchy audit's FAIL rate closely in the first batch of the real full-cohort
run rather than assuming this is fully closed.

## 3. Category-discipline audit — updated to understand DIRECT_MATCH/ADJACENT_MATCH — FIXED

**Problem:** the pre-existing audit (correctly left unmodified during the validation
phase, per explicit instruction at the time) predates the `match_relationship` schema
field and cannot distinguish "occupation falsely claimed as a direct preference" from
"occupation legitimately cited as the evidentiary basis for a disclosed, bridge-
explained `ADJACENT_MATCH`." It produced one known false FAIL:
`nysc-4646cb19`/COURSE-035.

**Fix:** `evidence_category_discipline_audit.py`'s `evaluate_citation()` gained a new
parameter, `adjacent_match_disclosed` — True only when a recommendation (a) is
`match_relationship == "ADJACENT_MATCH"`, (b) has a non-empty
`adjacent_match_bridge_explanation`, and (c) also cites at least one genuine
`DIRECT_PREFERENCE_OR_INTENT` variable elsewhere in the same recommendation. When True,
a `FEASIBILITY_OR_CONSTRAINT_CONTEXT` or `EDUCATION_AND_EXPERIENCE_CONTEXT` citation
that would otherwise FAIL for "preference framing at position 1" now correctly PASSes.
**`INDIVIDUAL_CONTEXT_ONLY` (opinion/perception variables) deliberately does NOT get
this exemption** — an opinion question is not legitimate evidence for a content bridge
either way, direct or adjacent.

**Backward compatibility, explicitly verified:** the new parameter defaults to `False`
and is computed as `False` for any record lacking `match_relationship` (all pre-schema
saved data). Re-ran against the 30-person batch and the frozen v3 baseline (neither has
this schema field): results are **byte-identical** to before this change
(30-batch: 243 PASS/3 CAUTION/0 FAIL; v3: 72 PASS/1 CAUTION/0 FAIL) — confirmed no
regression on historical data.

**Re-audited final-validation output:** `nysc-4646cb19`/COURSE-035 now correctly
**PASS**. **Category-discipline audit result: 77 PASS, 2 CAUTION, 0 FAIL** (both
remaining cautions are legitimate: one is an `INDIVIDUAL_CONTEXT_ONLY` secondary
citation, correctly still flagged per the no-exemption rule above; one is the same
variable-name typo from §4, correctly landing as a low-severity "unrecognised variable"
caution rather than a hard failure).

## 4. Grounding variable-name typo — mitigated via deterministic tooling fix

**Assessed:** the `occupation_class`/`occupational_class` mismatch is a genuine model
output slip (a wrong key name in one structured-output field), not a tooling bug — I
cannot "fix" what the model already said in a saved record. What **is**
deterministic/tooling-related is *how the audit handles it*, and that was overly blunt
(hard FAIL for any unrecognised variable name, even one character off with an otherwise
verifiably-correct cited value).

**Fix:** `grounding_audit_v2.py`'s respondent-claim check now uses `difflib` (Python
standard library, deterministic, no new dependency) to find a close spelling match
(cutoff 0.8) among the respondent's real answered variables when the cited name isn't
found verbatim. If a close match exists **and** the cited value also matches that real
variable's actual recorded value, it's downgraded to a caution ("likely typo of X"),
not a fabrication-level FAIL. A genuinely fabricated/unrelated variable name would need
to coincidentally satisfy both the spelling-similarity *and* value-matching conditions
to escape a FAIL, which a random fabrication will not do — this does not weaken
fabrication detection.

**Re-audited:** `nysc-04134b0d`/COURSE-066 — previously the one grounding FAIL — is now
correctly **PASS WITH CAUTION**. **Grounding audit result: 29 PASS, 5 CAUTION, 0 FAIL**
(the other 4 cautions are the same previously-documented low-severity word-overlap/
paraphrase pattern, unaffected by this change).

## 5. All audits re-run against saved data — summary

| Audit | Before this fix session | After (same saved data, re-analyzed) |
|---|---|---|
| Grounding | 29 PASS / 4 CAUTION / **1 FAIL** | 29 PASS / 5 CAUTION / **0 FAIL** |
| Category-discipline | 76 PASS / 2 CAUTION / **1 FAIL** | 77 PASS / 2 CAUTION / **0 FAIL** |
| Evidence-hierarchy | 41 PASS / 1 CAUTION / **1 FAIL** | 41 PASS / 0 CAUTION / **2 FAIL** |

The evidence-hierarchy FAIL count going *up* (1→2) is correct and expected, not a
regression — it reflects the rule getting strictly *more* demanding (§2), correctly
catching a case that used to slip through via a hedging loophole. Every other change is
a genuine reduction in false positives, cross-checked for backward-compatible behavior
on two other historical datasets.

## 6. Full-cohort runner — built, NOT executed, structurally verified

`src/rag_prototype/run_full_cohort.py` is new. It was **not run** — Steps 1-5 (model
verification, corpus verification, resume-scan, API-key presence check, BM25 index
build) touch no network at all; Step 6 (the only step that calls the API) was never
invoked in this task.

Verified without any API call:

| Requirement | How it's satisfied | Verified |
|---|---|---|
| Uses gpt-5-mini | `get_production_model()` (hardcoded, no `.env`) + `verify_production_model()` abort check as literal Step 1 | ✅ tested in isolation — prints correct model, passes; prints wrong model, raises `SystemExit` |
| Uses the frozen 84-course corpus | `corpus_v2.verify_corpus()` (SHA-256-checked) as Step 2, raises on mismatch | ✅ (already exercised dozens of times this session, always passing) |
| Uses the finalized governance prompt | Imports `context_pack_v2.GOVERNANCE_INSTRUCTIONS` directly, not duplicated | ✅ by construction |
| Preserves profile context as group-level supporting evidence | Unchanged `build_input_text()` Section 2 labelling ("GROUP-LEVEL RESEARCH CONTEXT — DO NOT ASSUME...") | ✅ unmodified in this fix session |
| Saves literal input/context snapshot per call | `call_snapshots/{respondent_id}.json`: full `constructed_input_text`, instructions hash, retrieved course IDs/scores, profile refs, corpus manifest hash, response ID, token usage | ✅ by construction (same pattern already used and verified in the 10-respondent final validation run) |
| Saves model/prompt/corpus hashes and token usage | Same snapshot fields as above | ✅ |
| Writes results incrementally | Snapshot + usage CSV row + results JSONL line all written immediately after each respondent's call, before the next one starts | ✅ by construction |
| Resumable without duplicating completed respondents | `load_already_completed()` reads the existing results JSONL at startup and the main loop only processes `[rid for rid in all_ids if rid not in already_done]`; results file is opened in **append** mode, never rewritten from scratch | ✅ tested directly with a simulated file containing 2 complete records and 1 deliberately truncated record (imitating a mid-write interruption) — correctly recovered the 2 complete respondent_ids and safely ignored the truncated line |

## Nothing was hidden or silently worked around

- `.env`'s incorrect model setting was left as found, not corrected, and explicitly
  flagged again here.
- The 2 evidence-hierarchy FAILs are reported, not deleted or reclassified away — the
  rule is *supposed* to be strict now, and these are real, known instances in
  already-saved data.
- The `nysc-04134b0d` typo is disclosed as a genuine (if minor) model slip, not erased
  — only the audit's classification of it (FAIL → caution) changed, and the reasoning
  for that change is fully documented.

## Genuine unresolved production blocker?

**None identified.** The one open item is the caveat in §2: whether the tightened
economic-affordability prompt wording actually prevents *new* instances in a live call
is unconfirmed (by design — no API calls were permitted in this task). This is a
monitoring item for the first batch of the real full-cohort run, not a blocker to
starting it — the audit that would catch a recurrence is itself now correctly strict
(§2, §5), so any recurrence will be visible immediately rather than silently passing.

---

## FULL COHORT PIPELINE FROZEN AND READY
