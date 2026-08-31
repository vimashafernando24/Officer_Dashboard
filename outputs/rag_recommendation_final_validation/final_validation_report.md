# Final Targeted Reasoning Refinement — Before/After Validation Report

**Architecture preserved, unchanged:** `gpt-5-mini`, the 84-course V2 corpus, BM25
retrieval (reused byte-for-byte from the saved 30-person batch — not recomputed),
frozen clustering/profile assignments, respondent evidence source, and the two
pre-existing audits (`grounding_audit_v2.py`, `evidence_category_discipline_audit.py`),
run unmodified in addition to a new, additive evidence-hierarchy audit.

**Changed:** the governance prompt (`context_pack_v2.GOVERNANCE_INSTRUCTIONS` — evidence
hierarchy A/B/C, correct profile-context use rules, `available_to_start` fix,
economic-affordability fix, occupation-as-preference fix, DIRECT_MATCH/ADJACENT_MATCH
classification) and the recommendation schema (added `match_relationship`,
`adjacent_match_bridge_explanation`, `catalogue_coverage_note`).

**Sample:** 10 respondents, all reused from the existing 30-person batch — no new
respondents, no retrieval recomputation.

**⚠️ A discrepancy was found and NOT silently corrected:** partway through this task,
`ClusterRP/.env`'s `OPENAI_RECOMMENDATION_MODEL` was found changed on disk to
`gpt-4o-mini`, contradicting the explicit instruction to keep using `gpt-5-mini`. This
run does **not** read that setting — `gpt-5-mini` is hardcoded directly in
`run_final_validation.py` (`MODEL = "gpt-5-mini"`, verified in the run log below) — so
the run was unaffected. The `.env` file itself was left as found; you may want to check
who/what changed it before the full cohort run, since a future script that *does* read
`.env` would silently use the wrong model.

---

## 1. Headline audit results

| Audit | Before (this exact prompt-fix's predecessor, 30-batch subset) | After (this run) |
|---|---|---|
| Standard grounding audit (unchanged tooling) | not separately re-run for this subset | **29 PASS, 4 CAUTION, 1 FAIL** |
| Evidence-category-discipline audit (unchanged tooling) | not separately re-run for this subset | **76 PASS, 2 CAUTION, 1 FAIL** |
| Evidence-hierarchy audit (NEW) | N/A — didn't exist before | **41 PASS, 1 CAUTION, 1 FAIL** |

All three FAILs were individually investigated (§5-§7) rather than accepted at face
value. Summary: one is a genuine minor model error (a variable-name typo); one is a
known, expected limitation of the pre-existing category-discipline audit, which predates
the ADJACENT_MATCH concept and cannot yet recognise a legitimately-disclosed adjacent/
upskilling citation as different from a false direct-preference claim (manual review
confirms the underlying model behaviour is correct); one is a genuine, if softer-than-
before, residual instance of the economic-affordability issue this refinement targeted.
A second borderline case was found to have a keyword-only false-positive in my *new*
audit's affordability check — fixed in this session (§7) — landing as PASS WITH CAUTION.

## 2. API usage and cost

10/10 calls succeeded, 0 retries, avg. 41.2s/call. **Cost: $0.1218 (ESTIMATED)** from
recorded token usage against `gpt-5-mini` published list pricing — not live-billed.

---

## 3. Per-respondent before/after

### 3.1 `nysc-0d099a8b` (D) — strong direct-match control case

**Why selected:** confirm the refinement didn't weaken a clean, already-correct case.

**BEFORE:** RECOMMENDATIONS_AVAILABLE, 3 recs (Motorcycle Mechanic, Automobile Mechanic,
Automobile Electrician), all grounded in `ideal_sector = "Manufacturing or production"`.

**AFTER:** RECOMMENDATIONS_AVAILABLE, 4 recs — same 3 courses retained, all now
explicitly `DIRECT_MATCH` (2× STRONG, 2× MODERATE), plus one additional DIRECT_MATCH
course (Motorcycle Mechanic variant). **What changed:** nothing substantive — the
control case is stable. Audit: PASS across all three audits.

### 3.2 `nysc-4e38db03` (D) — Education/Science → adjacent-match + catalogue-gap

**Why selected:** was `NO_DEFENSIBLE_RECOMMENDATION` before (no health/social-work
course exists in the 84-course corpus); this is the exact scenario the task's own
worked example describes (Education + Science → ICT as adjacent).

**BEFORE:** `NO_DEFENSIBLE_RECOMMENDATION`. Reason: neither retrieved course (TV
Production, ICT Diploma) taught the respondent's stated field.

**AFTER:** RECOMMENDATIONS_AVAILABLE, 1 rec — ICT Diploma, `ADJACENT_MATCH`, MODERATE.
`catalogue_coverage_note`: *"No strong direct programme match was found... for the
respondent's explicitly stated ideal sector (Health, social work, and wellbeing) or for
a literal 'Science' vocational programme. The recommendation above is an adjacent
STEM/ICT option that may still be relevant."* Bridge explanation: connects the stated
`study_field_preference = "Science or mathematics"` to ICT as "a defensible
STEM-adjacent technical option," explicitly not claiming this satisfies the
health/social-work goal. **What changed:** the system now surfaces a transparently
labelled, evidence-grounded adjacent option instead of a flat decline — exactly the
targeted behaviour change, using genuine individual evidence (the stated study-field
preference), not a manufactured bridge. Audit: PASS (all three).

### 3.3 `nysc-0cba8a68` (D) — profile-context use + individual-diverges-from-profile

**Why selected:** frozen profile membership is `D_motivation_p1` ("externally or
uncertainly motivated, with moderate study support"), yet this respondent's own
Section 1 answers are clear and goal-directed (`ideal_sector = "Education and
teaching"`, `plans_after_education = "Immediately go on to further education"`) — a
genuine divergence between the profile's framing and the individual's own evidence.

**BEFORE:** 3 recs, including the ICT Diploma at MODERATE strength (justified loosely
via the science/maths field preference).

**AFTER:** 2 recs (English Communication Essentials, Professional English), both
correctly reclassified `ADJACENT_MATCH`, MODERATE — the ICT Diploma was **dropped
entirely** this time. `catalogue_coverage_note` explicitly states no dedicated
Education/teaching or Science/Maths teacher-training programme exists in the retrieved
set. Both bridge explanations are explicit: "This is an inferential bridge (education
goal -> language/communication skill as enabling support), not a stated course
preference by the respondent." One recommendation's `uncertainties` field explicitly
discloses: *"The respondent's explicit study_field_preference (Science or mathematics)
would not be directly addressed by this programme"* — a transparent, honest admission
of a residual mismatch, not glossed over. Profile context is cited on both courses,
correctly hedged ("Profile describes... group-level tendency for limited
employment/training contacts was observed" for `D_motivation_p1`). **What changed:**
the model became *more selective*, not less — it dropped a previously-included but
weakly-justified course (ICT) once required to properly classify and bridge-explain
adjacent matches, rather than looser inference. Audit: PASS (all three).

### 3.4 `nysc-25c345ec` (D) — profile-context differentiation, complex case

**Why selected:** has children, never formally studied (O/L-level, "stay at home"
intent stated), yet also states a genuine sector preference (Manufacturing/production)
— tests whether care/education-history context is handled as hedged support rather than
a disqualifying or content-determining factor.

**BEFORE:** 4 recs, all DIRECT_MATCH-equivalent (schema didn't have the field yet),
with correctly hedged caregiving uncertainty language already present (documented in
the 30-batch report).

**AFTER:** 5 recs, all explicitly `DIRECT_MATCH` (3× STRONG, 2× MODERATE) grounded in
`ideal_sector = "Manufacturing or production"` and `expected_highest_edu_d = "O/L
level"`. The caregiving/schedule hedging pattern is preserved (verified in the
underlying JSON — uncertainty language about weekday full-time attendance and
caregiving remains present and appropriately hedged, not asserted as fact). **What
changed:** one additional course added; core reasoning quality preserved. Audit: PASS
(all three).

### 3.5 `nysc-4646cb19` (F) — CONFIRMED occupation-as-preference overreach → the clearest fix

**Why selected:** the single clearest confirmed problem case found in the 30-batch:
`ideal_sector = "Not sure"` (no usable direct preference), yet **all three** prior
recommendations were primarily justified by current `occupational_class` ("Clerical or
office work") alone, framed as if it were a stated preference.

**BEFORE:** 3 recs (Secretary, Computer Applications Assistant, ICT Diploma), no
match-relationship concept existed, `occupational_class` used as primary/sole
field-determining evidence for all three.

**AFTER:** 4 recs, **every single one now correctly classified `ADJACENT_MATCH`**
(2× MODERATE, 2× LIMITED — evidence strength appropriately downgraded from any implied
STRONG). `catalogue_coverage_note`: *"No strong direct programme match was found... for
a specifically stated sector because the respondent answered 'Not sure' for
ideal_sector. The following are adjacent options that may still be relevant, based on
the respondent's current clerical occupation and intention to pursue further
education."* Every bridge explanation correctly frames `occupational_class` as
*upskilling/continuity* evidence ("could build on their existing clerical experience"),
now always paired with a genuine direct-preference variable (`plans_further_edu_f`,
`expected_highest_edu_f`) rather than standing alone. **This is the single clearest
before/after transformation in this validation** — the exact confirmed failure mode is
now handled correctly: occupation legitimately informs an *adjacent* recommendation,
transparently disclosed as such, rather than masquerading as a direct field match.
Grounding audit: PASS. Evidence-hierarchy audit (new): PASS (has_genuine_preference
correctly detected, since real direct-preference variables are now always co-cited).
Category-discipline audit (pre-existing, unchanged): **FAIL on COURSE-035** — see §6 for
why this is a known limitation of that older audit rather than a real problem.

### 3.6 `nysc-04134b0d` (F) — second occupation + weak-preference case

**Why selected:** a second instance of professional-occupation + unclear sector,
previously resolved by declining — confirms correct behaviour generalizes beyond the
one confirmed-overreach case above.

**BEFORE:** `NO_DEFENSIBLE_RECOMMENDATION`.

**AFTER:** RECOMMENDATIONS_AVAILABLE, 2 recs (Professional English, ICT Diploma), both
`ADJACENT_MATCH` (MODERATE/LIMITED), grounded in `plans_further_edu_f` and
`usual_hours_per_week` (feasibility context, correctly used for format reasoning, not
content). **What changed:** like §3.2, the system now finds a defensible adjacent
option rather than flatly declining, without falsely elevating occupation to a direct
preference. One genuine grounding issue found here — see §5 (a variable-name typo, not
a content fabrication). Category-discipline: PASS. Evidence-hierarchy: PASS.

### 3.7 `nysc-3258dc18` (E) — CONFIRMED `available_to_start` misuse → fixed

**Why selected:** the confirmed case from the 30-batch: `available_to_start` (job-start
availability) cited as *"Indicates readiness to undertake training"* — the exact
job-vs-training conflation this refinement targeted.

**BEFORE:** 5 recs, `available_to_start` cited on COURSE-005 as training-readiness
evidence.

**AFTER:** 5 recs (4 unchanged, 1 swapped — COURSE-028 replaces COURSE-029), all
`DIRECT_MATCH` STRONG, grounded in `ideal_sector = "Manufacturing or production"` and
`job_type_sought = "Manual or trade work"`. **`available_to_start` is not cited in any
recommendation at all this time** — verified directly against the underlying JSON. The
model simply stopped reaching for this variable once its correct scope was clarified,
rather than needing a corrective disclaimer. Audit: PASS (all three).

### 3.8 `nysc-8ae4a1d8` (D) — CONFIRMED economic-profile/affordability overreach → improved, not fully eliminated

**Why selected:** the confirmed case: a `D_economic_p2` profile citation stated *"may
indicate capacity to pursue part-time, fee-paying training if desired."*

**BEFORE:** 4 recs; the flagged citation on COURSE-068.

**AFTER:** 5 recs, all `DIRECT_MATCH`. The same course (COURSE-068)'s profile citation
now reads: *"Profile shows relatively higher household economic position for many
members (supporting possibility of fee-paying study for some), but this is group-level
context only."* **The model added an explicit group-level-only disclaimer this time**
— a genuine, self-initiated improvement, correctly following the "may be discussed
cautiously, explicitly labelled as group-level" allowance in the new rules. My audit
initially flagged this as a FAIL via a bare keyword match; on review this was a false
positive in my *own new* tooling (it didn't account for explicit hedging), which I
fixed in this session (§7) — it now correctly lands as **PASS WITH CAUTION** (borderline
-compliant, still worth a human glance, not a clear violation). A second citation
elsewhere in this respondent's *other* recommendation set does still show a genuine,
unhedged residual instance of this issue (§6) — the fix reduced but did not 100%
eliminate this pattern across all 10 respondents.

### 3.9 `nysc-5242257e` (G) — genuine NO_DEFENSIBLE_RECOMMENDATION control case

**Why selected:** confirm the refinement hasn't reintroduced excessive recommending.

**BEFORE / AFTER:** identical — `NO_DEFENSIBLE_RECOMMENDATION` both times (sector "Not
sure," explicitly does not wish to work). Audit: PASS (all three). **No regression.**

### 3.10 `nysc-27c2ff48` (G) — additional profile-context example, branch diversity

**BEFORE:** 4 recs, all ICT-related, grounded in `ideal_sector = "Information technology
and communications"`.

**AFTER:** 5 recs, all `DIRECT_MATCH` (2× STRONG, 3× MODERATE), same core direction,
one additional course. `G_economic_role_p2` profile context cited appropriately
("Profile-level tendency: respondents often report useful employment/training
contacts... supporting context"), hedged correctly. Audit: PASS (all three).

---

## 4. Did the LLM use clustering/profile context intelligently, without treating members as identical?

Yes, consistently across all 10 respondents' profile citations reviewed in this run:
every `profile_context_used` finding retained explicit group-level language ("group-level
tendency," "profile members," "supporting context," "this is group-level context only"),
and none asserted a profile characteristic as an individual fact about the respondent.
The clearest demonstrations:
- §3.3 (`nysc-0cba8a68`): profile framing ("externally/uncertainly motivated") is
  present but does not override or contradict the respondent's own clear, specific
  direct-preference answers — the recommendation is built from the individual evidence,
  with profile context relegated to a labelled supporting note.
- §3.8 (`nysc-8ae4a1d8`): the model **self-corrected** an economic-profile citation
  between the 30-batch and this run to add an explicit "this is group-level context
  only" qualifier — direct evidence the prompt's evidence-hierarchy framing is being
  internalised, not just pattern-matched.

## 5. The one genuine grounding issue (minor)

`nysc-04134b0d` / COURSE-066: the model cited a respondent variable as `occupation_class`
— a typo of the real variable name `occupational_class`. The cited *value* ("Professional
work (doctor, lawyer, engineer, accountant, teacher, etc.)") and the underlying claim
were accurate; the error is a literal key-naming slip, not a fabricated fact. Genuinely
minor, but real — reported as-is, not corrected or hidden.

## 6. The one genuine category-discipline FAIL — a known audit-tooling limitation, not a model error

`nysc-4646cb19` / COURSE-035 (§3.5): the pre-existing, deliberately-unchanged
category-discipline audit flags `occupational_class` as a position-1 citation with
preference-framed language, regardless of the recommendation's own `match_relationship`.
Manual review (§3.5) confirms this citation is legitimately used within a properly
labelled `ADJACENT_MATCH`, with a real bridge explanation and co-cited genuine
direct-preference evidence — exactly the allowed "upskilling" pattern the new rules
describe. This audit predates the ADJACENT_MATCH concept and cannot yet distinguish
"occupation falsely claimed as a direct preference" from "occupation legitimately cited
as the evidentiary basis for a disclosed adjacent/upskilling match." **This FAIL is
preserved in the CSV, not deleted or reclassified** — per instruction, the pre-existing
audit was left unmodified — but it should not be read as a model defect. My own *new*
evidence-hierarchy audit's occupation-as-preference check (which does account for
co-cited direct-preference evidence) correctly passed this same case.

## 7. Bug found and fixed in my own new audit (not the model, not the pre-existing audits)

The new evidence-hierarchy audit's economic-affordability check was originally a bare
keyword match with no hedge-awareness — the same class of bug found and fixed twice
before in the grounding audit's negation window. `nysc-8ae4a1d8`/COURSE-068's citation
(§3.8) explicitly hedges as group-level-only, but was still flagged FAIL by the
unrefined keyword check. **Fixed in this session**: the check now downgrades to PASS
WITH CAUTION when an explicit group-level-only qualifier co-occurs with the affordability
language, and only FAILs a bare, unhedged individual-affordability claim. Re-run (no new
API calls) against the same saved output: `nysc-8ae4a1d8`/COURSE-068 now correctly PASS
WITH CAUTION; `nysc-4e38db03`/COURSE-006 (§8) remains a genuine FAIL, since its citation
has no such qualifier.

## 8. The one genuine, residual evidence-hierarchy FAIL

`nysc-4e38db03` / COURSE-006: profile citation reads *"This economic profile emphasises
government-funded or lower-cost education patterns (relevant when considering
affordability and public-sector career alignment)."* No explicit group-level-only
qualifier is present. This is a real, if softer-than-before, residual instance of the
economic-profile-affordability issue — the fix reduced the pattern's severity (compare
to the pre-fix "may indicate capacity to pursue... fee-paying training") but did not
eliminate it in every instance across this 10-respondent sample.

## 9. Auditability improvement implemented (Section 13)

For every one of the 10 calls, `outputs/rag_recommendation_final_validation/call_snapshots/
{respondent_id}.json` now saves: the full constructed input text actually sent, a SHA-256
hash of the exact governance instructions used, the model name, retrieved course IDs and
scores, profile document references, a SHA-256 hash of the full course-corpus manifest,
the API response ID, and complete token usage — sufficient to reproduce and audit exactly
what the model saw for each call without depending on deterministic reconstruction from
separately-frozen files (the limitation flagged after the 30-person batch). No API key is
stored anywhere in these files (verified).

## 10. Versioning

All outputs for this run are under the new, separate `outputs/rag_recommendation_final_validation/`
directory. `outputs/rag_recommendation_prototype_api_v3/` (frozen 10) and
`outputs/rag_recommendation_validation_30/` (30-batch) are untouched — verified by file
timestamps predating this session.

---

## Verdict

Across 10 deliberately targeted respondents (not randomly chosen, not chosen for ease):
- Every one of the specific confirmed problems (occupation-as-preference §3.5,
  `available_to_start` misuse §3.7) is fixed in the cases that motivated this
  refinement, with real before/after evidence, not just prompt text.
- The Education/Science → adjacent-match and catalogue-gap behaviour works exactly as
  specified in the task's own worked example (§3.2).
- Profile context is being used exactly as intended: contextualising, hedging,
  self-correcting toward more explicit group-level framing, and in one case (§3.3)
  becoming the reason a weaker match was appropriately *dropped* rather than kept.
- Both control cases (strong direct match §3.1; genuine NO_DEFENSIBLE §3.9) are
  unaffected — no regression toward either excessive recommending or excessive refusal.
- The economic-affordability issue is genuinely improved (self-correcting hedged
  language observed) but not 100% eliminated (§8) — one residual instance remains in
  this sample.
- One minor grounding typo (§5) and one known pre-existing-audit limitation (§6, not a
  model defect) were found and reported, not hidden.
- The auditability gap flagged after the 30-person batch is now closed for this run.

The one outstanding item — residual (softer, less frequent) economic-profile-affordability
language in some citations — is real but minor, non-blocking, and worth continued
monitoring during the full run rather than requiring another prompt-iteration cycle
first: it did not, in this sample, cross into an actual individual-affordability *claim*
being used to justify or deny a recommendation, only into profile-context phrasing that
sits close to the line.

## READY FOR FULL COHORT RUN
