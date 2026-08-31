# RAG + LLM NYSC Programme Recommendation Prototype — Step 4 Report

**Status: small, auditable prototype only.** 10 of 362 respondents. No frozen research
output was modified. No embedding API or external LLM API was called — retrieval is a
transparent, dependency-free lexical method (documented below), and all recommendation
reasoning in this prototype was performed directly by Claude (this session), reading
each respondent's full context pack and reasoning over it, with no hidden chain-of-thought
stored — only the auditable evidence+inference+recommendation record itself.

---

## 1-3. Course corpus: validated, excluded, indexed

| Count | Value |
|---|---|
| Validated screenshot-derived course parents (from the course-knowledge audit) | **88** |
| Excluded from indexing (`NEEDS_MANUAL_REVIEW_DO_NOT_INDEX`) | **9** |
| **Actually indexed (safe course parents)** | **79** |

The 9 excluded documents (verified against `course_source_traceability.csv`, not assumed):
`COURSE-002` PYTHON, `COURSE-004` Professional English, `COURSE-005` Automobile Mechanic,
`COURSE-015` Quantity Surveying Assistant, `COURSE-027` Landscaping Technician, `COURSE-039`
Cook (title/content mismatch — automobile content under a "Cook" title), `COURSE-045B`
Welder, `COURSE-046` Beautician, `COURSE-068` Graphics Designer. None of these appears
anywhere in `course_child_chunks.jsonl`, in any retrieval result, or in any recommendation —
verified both by construction (the chunking script filters on `validation_status` before
creating any chunk) and by the automated evidence audit's document-safety check (0 failures
on this check across all 19 recommendations). The 8 `SUPPORTING_SOURCE` catalogue-listing
pages were never part of `validated_documents/` in the first place and were not touched.

---

## 4-6. Architecture, chunking, retrieval method

**Parent-child retrieval**, per the course-knowledge audit's own recommendation
(`rag_chunking_strategy.md`): each safe validated document is the authoritative parent;
retrieval happens over section-aware child chunks; final reasoning always receives the
**complete parent document**, never an isolated chunk.

**Chunking** (`src/rag_prototype/build_course_chunks.py`): every parent gets a
`whole_document` child (safety net, since most documents are short — matches the audit's
own finding that whole-document retrieval is a reasonable baseline for this corpus).
Where the corpus's consistent structural pattern is detected (`Course Overview` heading →
numbered module/overview list → narrative paragraph starting `The National Youth Service
Council...`), additional `identity_and_schedule_snippet`, `modules_or_overview_list`, and
`narrative_description` children are also created — 51 of 79 parents got this additional
section-aware split; the remaining 28 fall back to whole-document only. **193 total child
chunks**, each carrying `parent_course_id`, `course_name`, `section`, `source_document`,
`source_screenshots`, and an `uncertainty_flag`. No chunk ever loses its parent link.

**Retrieval method**: a from-scratch, dependency-free **BM25** implementation
(`src/rag_prototype/bm25.py`) — chosen because it is fully available in this environment
without any external embedding API or credentials, fully deterministic, and fully
auditable (no external service, no fabricated "an embedding model was used" claim). This
is the lexical fallback the task explicitly asked for; no semantic/embedding retrieval was
implemented in this prototype (see Limitations).

Two documented, generic (not respondent-tuned) refinements were required to make BM25
usable on this specific corpus and are disclosed here rather than hidden:
- A stopword list including both standard English stopwords and this corpus's own
  repeated NYSC boilerplate phrasing (e.g. "National Youth Service Council has initiated
  several course programs...", present in nearly every document) — without this, every
  document scored similarly on boilerplate alone.
- A **sector-vocabulary expansion** step: the respondent's stated `ideal_sector` is
  bridged to the V2 structured dataset's `skill_area` categories and that category's
  `skill_keywords` vocabulary is added to the retrieval query. This is a legitimate,
  fully-documented hybrid step using only the already-validated structured dataset (not
  historical cluster/profile data, not an embedding model) to close the vocabulary gap
  between survey sector phrasing ("Hotels, restaurants, and hospitality") and course text
  phrasing ("cookery," "cake"). Its necessity, and one case where it made a decisive
  difference, is documented in §12 below.

**LLM used**: Claude (this session), reading each respondent's assembled context pack
directly — no separate API call, no hidden reasoning step, output limited to the
structured, auditable fields specified in the task.

---

## 7. Test respondent selection (10 of 362)

Selected by scanning all 362 respondents' direct-preference and context evidence and
deliberately choosing a diverse, non-cherry-picked set — see `test_sample.csv` for the
exact list with rationale tags. Composition: **3 Branch D** (all three retained profile
memberships preserved for each), **1 Branch E**, **3 Branch F**, **3 Branch G** (both
retained profile memberships preserved for each). Deliberately includes two respondents
with **no usable direct field preference** (to test that the system declines rather than
invents), not just "easy" cases. Each respondent is tagged against the task's Section V
case types:

| Respondent (short id) | Branch | Case type(s) tested |
|---|---|---|
| acaf63b5 | D | 2 (provider+care, clear field preference) |
| 3a86d117 | D | 1 (strong ICT preference + self-employment intent) |
| a04f7d96 | D | 6 (weak/no direct preference) |
| 131a2b60 | E | 1+3 (strong ICT preference + training-access barrier) |
| 346623df | F | 3 (employment insecurity + job-change intent + skills barrier) |
| 0c6c34a2 | F | 4 (secure employment, prior employer training to build on) |
| 33aaf2f7 | F | 3 (insecure, self-employed, overqualification + barrier) |
| 00e2c251 | G | 5 (dual G membership, construction interest, barrier) |
| 465701ee | G | 5+6 (dual G membership, weak preference, care/home-duties context) |
| 55bdfdcc | G | 2+4 (provider+care, dual G membership, hospitality + prior work) |

---

## 8-9. Recommendations produced and audit outcome

| Metric | Value |
|---|---|
| Respondents with ≥1 recommendation | 8 / 10 |
| Respondents returning `NO_DEFENSIBLE_RECOMMENDATION` | 2 / 10 |
| Total individual recommendations | 19 |
| Recommendations per respondent (where produced) | 2-3 (never forced to 5) |
| **Final audit: PASS** | **10 / 19** |
| **Final audit: PASS WITH CAUTION** | **9 / 19** |
| **Final audit: FAIL (in the delivered output)** | **0 / 19** |

No recommendation was silently deleted or hidden to reach this result — see §10-11 for a
FAIL that was caught, corrected, and is disclosed here rather than erased.

---

## 10. Retrieval failures (disclosed, not hidden)

**A genuine bug was caught by the automated audit and is reported transparently.** While
iteratively improving BM25 retrieval quality (adding stopword filtering and the
sector-vocabulary expansion step described above), the retrieval index for respondent
`nysc-0c6c34a2` changed between when its recommendation was first drafted (against an
earlier retrieval run, before the expansion step existed) and when the corpus's final
retrieval was generated. The mechanical evidence audit's document-safety check correctly
flagged both of that respondent's originally-drafted recommendations (`COURSE-043`
AutoCAD, `COURSE-018` Aluminium Fabricator) as **not present in the respondent's actual
final retrieved set** — i.e. a genuine retrieval/recommendation desynchronisation, not a
content error. Both recommendations were rewritten against the corrected, final retrieval
output (`COURSE-040` Automobile Mechanic, `COURSE-012` Refrigeration & Air Conditioning
Technician — both of which score highly in the final retrieval and are grounded in real
course text). This is disclosed here as evidence that the automated audit step in this
architecture does real, load-bearing work, not just decorative validation.

**BM25 noise on very short documents**: several retrieved parents in raw retrieval logs
(see `retrieval_audit.csv`) are lexically matched but not topically relevant — for
example `COURSE-049` "Business Managemant" and `COURSE-006` "National Diploma in ICT"
appear in the top-15 for multiple unrelated queries (construction, hospitality) because
this corpus's very short documents (median ~20 content tokens after stopword removal)
let a single coincidental shared word (e.g. "work," "local") produce a disproportionately
high BM25 score. **This was not silently accepted**: in every affected respondent's
reasoning pass, such spuriously-retrieved courses were reviewed against their full text
and excluded from the final recommendation when they did not genuinely match — retrieval
rank/score was never treated as suitability. This is precisely why the architecture
separates retrieval from reasoning; see §17 for the direct comparison this enables.

---

## 11. Unsupported-inference failures

None reached the final delivered output (0/19 FAIL). The mechanical check specifically
scans for un-labelled inferences, protected/technical field leakage, and
recommendation-of-unretrieved/excluded courses; it found only the retrieval-desync issue
in §10, which was a grounding-location problem, not an invented-fact problem — no
recommendation anywhere in the sample stated an invented respondent characteristic,
invented course property, fabricated fee/location/eligibility/placement claim, or
converted a group percentage into an individual fact.

---

## 12. Examples of GOOD contextual reasoning

- **Permitted-inference pattern used correctly** (matches the task's own worked example):
  for `nysc-acaf63b5` (D, primary earner, already balancing paid work + post-graduate
  study), the system recommended a part-time/weekend Business Management course and
  reasoned: *"a weekend/part-time course format may be easier to fit alongside existing
  income and study commitments... This is an inference about practicality, not a claim
  that the respondent cannot attend full-time."* — explicitly hedged, tied to two real
  facts (primary earner + already working while studying) and one real course fact
  (weekend schedule).
- **Concrete, evidenced feasibility conflict surfaced rather than ignored**: for
  `nysc-346623df` (F), the system recommended `COURSE-022` (Computer Network Technician,
  full-time weekdays) while explicitly disclosing: *"the respondent directly reported
  currently working 40 hours per week under a temporary 12-36 month contract. This is a
  genuine, directly-evidenced scheduling tension... though the respondent's actual
  capacity to arrange this... is unknown and not assumed here either way."* This is the
  correct, non-catastrophising handling of a real conflict.
- **Vocabulary-bridging retrieval catching what a naive baseline could not**: for
  `nysc-33aaf2f7`, whose stated sector was "Wholesale, retail, or repair," the system
  identified `COURSE-029` "Mobile Phone Repair Technician" via the literal shared word
  "repair" plus the respondent's existing IT-technician occupational background — a
  connection the simple sector-bridge baseline structurally could not make (see §16).
- **Correctly declining rather than inventing** (twice): for both `nysc-a04f7d96` and
  `nysc-465701ee`, the system returned `NO_DEFENSIBLE_RECOMMENDATION` and — critically —
  explicitly identified and rejected the temptation to substitute an
  `individual_context_only` opinion field ("IT and digital skills is a useful quality
  for a job") for a genuine stated preference, naming exactly why that would have been a
  policy violation.
- **Missing catalogue information treated as unknown, not negative**: for
  `nysc-00e2c251` (G, O/L-level education, no prior work experience), the system
  recommended "Construction Site Supervisor" while stating: *"no entry requirement,
  minimum prior experience, or minimum education level is stated anywhere in the course
  document — it is therefore unknown, not confirmed either way, whether this course is
  designed for entry-level candidates."*

## 13. Examples of BAD / unsupported reasoning that was caught before delivery

- The retrieval-desync issue in §10 (recommending courses not actually retrieved) — caught
  by the mechanical audit and corrected before appearing in `test_recommendations.jsonl`.
- During drafting, the retrieval query's approximate sector-bridge mapping for "Education
  and teaching" pulled in Japanese/French/Korean/Tamil language courses for respondent
  `nysc-acaf63b5` (via an over-broad "education → languages" mapping in the baseline
  bridge table). This was recognised during reasoning as an unsupported inferential leap
  (wanting to work in "education and teaching" does not imply wanting to learn a foreign
  language) and explicitly **not** recommended; instead the report records this as a
  genuine catalogue gap (no course addresses "education and teaching" as a sector) rather
  than papering over it with a weak lexical coincidence.

No example of an actually-delivered fabricated fact, invented eligibility claim, or
profile-to-individual conversion was found in this sample.

---

## 14. Did profile context help?

**Consistently no independent content value in this sample, but consistently used
correctly.** In all 8 respondents that received recommendations, the cited profile
context (labelled `GROUP-LEVEL: ... — NOT INDIVIDUAL FACT` throughout) was used only as
background corroboration of information the respondent had *already stated directly* in
Section 1 (e.g. a profile labelled "predominantly self-income provider" cited alongside a
respondent who had already directly answered `primary_earner_status = Yes`). In zero
cases did profile context introduce new information not already present in direct
evidence, and in zero cases was profile context used to select course content. This is
the policy-correct behaviour (direct evidence must always take priority), but it also
means that, in this sample, profile documents added no independent recommendation value
beyond reinforcing what direct evidence already established — see §17 answer D.

---

## 15. Did full-text course knowledge help?

**Yes, clearly, in most recommendations** — and in one case (§16) it was the difference
between a right and a structurally-impossible answer. Concrete instances:

- Fee (LKR 20,000), duration (3 months), age eligibility (15-45), and certificate status
  for `COURSE-001` — none of which exist in the reduced V2 structured dataset's
  `skill_keywords`-only representation of that course.
- Distinguishing two identically-titled "Computer Hardware Technician" courses
  (`COURSE-008` full-time vs. `COURSE-055` part-time) that would be indistinguishable
  from a bare course-name/sector listing.
- The explicit "Baker Management" module line that justified ranking Baker above
  Professional Cookery for a respondent who stated self-employment intent.
- Directly checking (and correctly reporting as absent) entry requirements, which the
  reduced dataset never carried in the first place.

**One clear case where full text did NOT help, and the reduced V2 dataset was actually
better**: duration is stated in the V2 structured dataset's `duration_months` field for
nearly every course, but the course-knowledge validation audit itself found duration is
the single most commonly *lost* field in the raw screenshot text (absent from 84 of 85
defensibly-matched records). In this prototype, no recommendation could confirm whether a
course fit within a respondent's stated urgency window (e.g. `nysc-131a2b60`'s "within 3
months") because duration was simply not present in the retrieved full text — this is an
honest limitation, not glossed over.

---

## 16. Comparison against the sector-only baseline

`baseline_sector_match.csv` and `llm_added_value_analysis.csv` record a simple
"match respondent's stated sector to the V2 catalogue's `skill_area` field" baseline for
every respondent, explicitly **not** presented as a recommendation system — a comparison
tool only.

| Respondent | Baseline matches | RAG+LLM recommendations | What changed |
|---|---:|---:|---|
| acaf63b5 | 8 (via an over-broad sector-bridge mapping) | 2 | Baseline mapping was actively wrong (language courses); RAG used the real field preference instead |
| 346623df | 17 | 2 | Narrowed using job-change reason + self-employment intent; surfaced a real schedule conflict |
| 131a2b60 | 17 | 3 | Narrowed using named training-type preference; distinguished a full-time/part-time duplicate pair |
| a04f7d96 | 1 (no match) | 0 | Agreement — both correctly produce nothing, RAG explains why |
| 3a86d117 | 17 | 3 | Narrowed using self-employment intent; supplied fee/duration/certification detail |
| 0c6c34a2 | 21 (two skill areas) | 2 | Narrowed using employer-training signal + a real work-hours/schedule check |
| 33aaf2f7 | 5 (baseline's sector-bridge cannot reach "repair" trades at all) | 2 | **RAG found courses the baseline's category mapping structurally could not represent** |
| 00e2c251 | 8 | 2 | Narrowed using barrier evidence; disclosed an eligibility unknown |
| 465701ee | 1 (no match) | 0 | Agreement — both correctly produce nothing |
| 55bdfdcc | 5 | 3 | Ranked within-category using self-employment intent + a specific course module |

RAG **meaningfully narrowed** the list in 8/8 cases where a recommendation was produced
(never just re-listing the baseline), **reordered/prioritised** within-category in every
narrowed case using evidence the baseline cannot access (stated intent, barriers, prior
experience, schedule facts), **identified feasibility differences** (schedule conflicts
and compatibilities) invisible to category filtering in 4 cases, and **used course
details unavailable in the reduced V2 dataset** in 7 of 8 narrowed cases. In the two
weak-evidence cases, RAG and the baseline correctly agree on producing nothing, but RAG's
explicit, auditable reasoning for declining is itself a meaningful improvement in
transparency over a baseline that would simply return an empty or generic list without
explanation.

---

## 17. LLM_ADDED_VALUE distribution

| Classification | Count | Respondents |
|---|---:|---|
| HIGH | 6 | acaf63b5, 346623df, 131a2b60, 3a86d117, 33aaf2f7, 55bdfdcc |
| MODERATE | 4 | a04f7d96, 0c6c34a2, 00e2c251, 465701ee |
| LOW | 0 | — |
| NONE | 0 | — |

Full per-respondent reasoning (8-point assessment: within-field distinction, evidence
used, context effect, defensibility, full-text usefulness, profile usefulness, unsupported
assumptions, baseline-equivalence) is in `llm_added_value_analysis.csv`. The two
weak-evidence cases were rated MODERATE rather than HIGH specifically because their value
was confined to reasoning transparency, not course-list improvement — an intentionally
conservative rating, not an inflated one.

---

## Answers to the required questions

**A. Does RAG + LLM reasoning provide meaningful value beyond category filtering?**
Yes, in 8 of 10 tested cases, and the value is traceable to specific evidence (stated
intent, barriers, prior experience, schedule facts) that a sector-only filter structurally
cannot use. In 1 of 10 cases (`nysc-33aaf2f7`) the baseline's coarse category mapping was
not just less precise but unable to reach the correct courses at all. In the remaining 2
of 10 cases (weak/no direct preference), RAG and the baseline correctly agree on
producing no recommendation, and RAG's explicit reasoning is itself the value-add.

**B. Can the model use respondent circumstances (household responsibility, employment
insecurity, barriers, experience) without turning them into unsupported facts?** Yes in
every recommendation examined. The evidence audit found zero cases of an unlabelled
inference, zero cases of a circumstance being converted into a claimed constraint the
respondent never stated (e.g. no "cannot attend full-time" claim from provider/parent
status appears anywhere in the sample), and multiple cases where a real, directly-
evidenced feasibility tension (e.g. a stated 40-60 hour work week vs. a full-time weekday
course) was surfaced honestly rather than hidden or over-interpreted.

**C. Does full-text course knowledge improve recommendation reasoning compared with the
reduced V2 matching dataset?** Mostly yes (§15) — fee, duration-in-some-cases, age range,
specific module content, and schedule-pair disambiguation all came only from full text.
One clear exception: course *duration* is more reliably present in the reduced V2 dataset
than in the raw screenshot text, which is an honest, documented limitation.

**D. Does frozen profile context provide useful additional information?** Not
independently, in this sample. Profile context was used correctly (as background,
clearly labelled, never overriding direct evidence, never substituting for a missing
preference) in every case, but it never contributed information the respondent's own
direct answers had not already established. This may reflect that this sample's direct
evidence was generally rich; a future test with more respondents having sparser direct
evidence could reveal cases where profile context matters more.

**E. Is the system scientifically defensible as an exploratory AI-assisted programme
recommendation prototype?** Yes, within the tested scope. Every recommendation traces to
real source text; every inference is labelled and grounded; missing information is
consistently treated as unknown, not negative; protected/technical fields never leak into
recommendations; excluded/unsafe course documents never appear; and the one real error
found in this process (§10) was caught by the automated audit, not missed.

**F. Is it ready to expand to all 362 respondents?**

---

## 18. Limitations

- **Retrieval is lexical (BM25) only**, not semantic/embedding-based — no embedding API
  or credentials were available/used in this environment, per the task's explicit "stop
  before fabricating" instruction. This corpus's very short documents make BM25 more
  noise-prone than it would be on longer text (§10); the sector-vocabulary expansion
  step mitigates but does not eliminate this.
- **The sector-vocabulary bridge table (survey sector → V2 `skill_area`) is
  hand-built and approximate**, documented as such in code and reused for both the
  retrieval-query expansion and the baseline comparison. It is a reasonable prototype
  device, not a validated instrument.
- **Duration information is frequently absent** from the retrieved full text, even where
  present in the reduced V2 dataset (§15) — urgency-based reasoning could not always be
  fully checked against actual course length.
- **Language fit could not be assessed for most recommendations**: none of the branches'
  survey instruments captures an instructional-language preference, so several strong
  content matches (e.g. `COURSE-001`, `COURSE-029`) are in Sinhala with no way to confirm
  the respondent's comprehension.
- **10 respondents is not enough to characterise system behaviour across the full
  diversity of 362** — the case types were deliberately chosen to stress-test known risk
  areas, but rarer combinations (e.g. very sparse Branch E evidence, multiple
  simultaneous barriers) were not all represented.
- **The evidence-policy human-review decisions from the prior audit stage remain
  pending approval** (see `outputs/rag_respondent_evidence/respondent_variable_human_review_report.md`).
  This prototype did not wait for that approval; instead, every recommendation in this
  sample was manually checked to avoid the specific forbidden inferences that audit
  flagged (e.g. never treating `primary_earner_status` or `has_children` as an
  independent schedule driver — see the repeated hedged phrasing throughout §12). This
  manual discipline is not the same as an enforced policy and does not scale to 362
  respondents without either (a) the human-review decisions being formally applied to
  `respondent_variable_policy.csv`, or (b) equivalent guardrails being encoded into
  whatever process replaces manual per-respondent reasoning at scale.

## 19. Reproducibility

All code is in `src/rag_prototype/` (`bm25.py`, `build_course_chunks.py`,
`select_and_retrieve.py`, `build_context_packs.py`, `recommendations_data.py`,
`run_evidence_audit.py`, `build_added_value_analysis.py`). Running them in that order
against the unmodified frozen inputs reproduces every file in
`outputs/rag_recommendation_prototype/` deterministically (BM25 and the chunking/parsing
logic contain no randomness). The `recommendations_data.py` module is the one
non-mechanical artefact — it is the recorded output of the reasoning pass performed
directly by Claude against each respondent's context pack (retained under
`_context_packs/` for full inspection), not a re-runnable script.

## 20. Cost / API requirements

**None.** No external embedding API, no external LLM API, no paid service of any kind was
used in this prototype. Retrieval is pure Python (BM25). Recommendation reasoning was
performed directly by Claude within this same session, reading local files only.

---

## READY AFTER SPECIFIC FIXES

The prototype demonstrates real, evidence-traceable value over simple category filtering
(6/10 HIGH, 4/10 MODERATE, 0 LOW/NONE), a working audit process that caught and corrected
a genuine error before delivery, and no unsupported-fact or policy-violation failures in
the delivered output. It is not yet a "ready to scale as-is" system for these reasons:

1. **Recommendation reasoning was performed manually by Claude reading each context pack**,
   not by a re-runnable, scriptable process — before scaling to 362 respondents, this
   needs to become a repeatable procedure (whether that means a scripted LLM-API call
   with this same prompt structure, or an explicitly resourced manual-review workflow)
   rather than one-at-a-time bespoke reasoning.
2. **The pending human-review decisions on borderline evidence variables** (household
   income/provider status/care responsibilities as schedule drivers, etc.) should be
   formally resolved and applied to `respondent_variable_policy.csv` before scale, rather
   than relied upon as manual discipline per recommendation.
3. **BM25 retrieval quality on this short-document corpus should be improved or
   supplemented** before relying on it unattended at scale — in this prototype, retrieval
   noise was caught by manual review of full text during reasoning; at scale, either
   better retrieval (a real embedding model, if credentials become available; a richer
   hybrid query; or curated course-level tags) or a more robust automated relevance
   filter should reduce how much noise the reasoning stage has to filter per respondent.
4. **The retrieval-recommendation desynchronisation bug found in §10** shows the pipeline
   needs a hard invariant check (already partially implemented in the audit script) run
   *before* any recommendation is finalised, not just after, if this becomes an automated
   process.
5. **Duration and language-fit information gaps** (§15, §18) should be addressed — either
   by supplementing the course corpus with the V2 dataset's `duration_months` field where
   full-text extraction lost it, or by adding an instructional-language question to
   future respondent data collection — before schedule/duration/language-sensitive
   recommendations are made at scale.
