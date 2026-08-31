# Branch F Group Programme Relevance Prototype

## Scope and verification

This prototype uses the actual answers of the **81 frozen Branch F respondents** and does not infer an individual's answers from F-S1 or F-S2 membership. Frozen assignments were verified as **F-S1 n=29** and **F-S2 n=52**. Each respondent was compared with all **87 V2 courses**, producing **7,047 respondent-course rows**. No clustering, profiles, medoids, assignments, cleaned data or course records were modified.

This is group-level descriptive programme relevance. It is **not individual eligibility prediction**, and a high-ranked group course does not mean every profile member should take it.

## Variables reviewed

| Survey variable | Coverage | Used in course score? | Decision |
|---|---:|---|---|
| `ideal_sector` | 81/81 | Yes | Strongest direct course-content direction; matched conservatively to V2 skill areas or explicit text. |
| `ideal_work_type` | 81/81 | Partly | Only “Start my own business” is actionable, and only for courses with explicit self-employment/freelancing wording. |
| `plans_further_edu_f` | 81/81 | No | Used to report training-interest rate, not to choose a specific course. |
| `occupational_class` | 81/81 | No | Describes the current job, not the desired future occupation. |
| `hopes_to_change_job` | 81/81 | No | Career-change interest is summarized, but it does not state a target course. |
| `reason_wants_to_change` | 46/81 eligible | No | Conditional on wanting to change; reasons such as pay or progression do not map to V2 course attributes. Structural N/A remains N/A. |
| `most_useful_quality_for_job` | 81/81 | No | It is a belief about labour-market value, not a personal learning preference; V2 module/soft-skill coverage is also sparse. |
| Previous training, education/job match and business barriers | varies | No | Useful context, but not a direct desired skill, sector or occupation. |
| `contract_type`, `job_security_12months`, `sector_formality` | 81/81 | No | Explicitly excluded: these form the F clusters and are not programme preferences. |

Demographics and household variables were not used.

## Conservative sector crosswalk

- Direct category mappings: ICT; creative/media; hospitality; beauty/personal services; agriculture; construction.
- Manufacturing/production maps broadly to automotive/mechanical and electrical/electronics and is flagged as broad.
- Finance matches only explicit finance/accounting text.
- Education matches only explicit teacher/teaching/education text.
- Wholesale/retail/repair, health/wellbeing, transport/logistics, public administration and “Not sure” receive no sector score because V2 cannot distinguish them defensibly.

## Individual relevance score

For respondent *i* and course *c*:

> relevance(i,c) = 100 × mean of the available component matches

Available components are:

1. **Sector match:** 1 when the course matches the respondent's actual `ideal_sector`, otherwise 0. The component is absent when no defensible crosswalk exists.
2. **Explicit entrepreneurship match:** 1 only when the respondent chose “Start my own business” and the course contains explicit self-employment/freelancing evidence. Generic “management” wording was not accepted as entrepreneurship evidence.

Components are equal-weighted only when both are available. This is a transparent baseline, not an optimized weighting system. A missing course component is omitted from the denominator, never coded as zero. The descriptive relevance threshold is **70/100**.

Exact score ties are common because the survey records broad sector interest rather than detailed course preferences. Strict Top 3/5 flags use score, positive evidence count, available evidence count and course ID for reproducibility. The report and profile ranking use **tie-adjusted Top 3/5 credit**, which divides boundary slots across tied courses instead of pretending an arbitrary course-ID ordering is substantive.

## Course fields that actually contributed

| V2 field | How it contributed | Missing-field treatment |
|---|---|---|
| `skill_area`, `sector_tags` | Primary direct/broad sector crosswalk | Complete for all 87 courses. |
| `course_name`, `skill_keywords`, `target_occupations`, `matching_text` | Only explicit accounting/finance and teacher/education checks | Positive text was used; absent detailed tags were not treated as proof of eligibility or outcomes. |
| `entrepreneurship_content` | Screened for explicit entrepreneurship, self-employment or freelancing wording | Blank and generic “management” wording were treated as unknown, not as “No entrepreneurship.” |
| Other V2 fields | Did not contribute | Language, schedule, duration and qualification could not be used because the original F survey did not collect the corresponding preferences. |

## Profile matching summaries

| Profile | n | Enough matching data | Plans further training: Yes | Not sure | Start own business | Wants to change job |
|---|---:|---:|---:|---:|---:|---:|
| F-S1 | 29 | 24 (82.8%) | 23 (79.3%) | 5 (17.2%) | 12 (41.4%) | 18 (62.1%) |
| F-S2 | 52 | 48 (92.3%) | 48 (92.3%) | 3 (5.8%) | 27 (51.9%) | 28 (53.8%) |

### Actual sector interests

| Profile | Actual `ideal_sector` answer | n | Within-profile % |
|---|---|---:|---:|
| F-S1 | Information technology and communications | 18/29 | 62.1% |
| F-S1 | Wholesale, retail, or repair | 3/29 | 10.3% |
| F-S1 | Public administration, government, and defence | 2/29 | 6.9% |
| F-S1 | Education and teaching | 1/29 | 3.4% |
| F-S1 | Personal services (beauty, fitness, wellness) | 1/29 | 3.4% |
| F-S1 | Creative, media, and arts | 1/29 | 3.4% |
| F-S1 | Not sure | 1/29 | 3.4% |
| F-S1 | Transport, storage, and logistics | 1/29 | 3.4% |
| F-S1 | Manufacturing or production | 1/29 | 3.4% |
| F-S2 | Information technology and communications | 34/52 | 65.4% |
| F-S2 | Agriculture, forestry, and fishing | 5/52 | 9.6% |
| F-S2 | Manufacturing or production | 3/52 | 5.8% |
| F-S2 | Not sure | 2/52 | 3.8% |
| F-S2 | Personal services (beauty, fitness, wellness) | 2/52 | 3.8% |
| F-S2 | Finance, banking, and insurance | 2/52 | 3.8% |
| F-S2 | Creative, media, and arts | 1/52 | 1.9% |
| F-S2 | Hotels, restaurants, and hospitality | 1/52 | 1.9% |
| F-S2 | Public administration, government, and defence | 1/52 | 1.9% |
| F-S2 | Wholesale, retail, or repair | 1/52 | 1.9% |

## F-S1 Top 10 programme relevance

| Aggregate rank | Course ID | Course | Valid score n | Mean | Median | Tie-adjusted Top 3 | Tie-adjusted Top 5 | ≥70 | Dominant reasons | Broad-category-only? |
|---:|---|---|---:|---:|---:|---:|---:|---:|---|---|
| 1 | NYSC-C018 | Freelancer of Web Design & Development | 24 | 85.4 | 100.0 | 20.9% | 29.4% | 83.3% | sector interest: Information technology and communications [direct category crosswalk: Information technology and communications → ICT & Computing] (n=18); explicit self-employment/freelancing content (n=12) | No |
| 2 | NYSC-C001 | National Diploma in Information & Communication Technology | 22 | 81.8 | 100.0 | 12.6% | 21.0% | 75.0% | sector interest: Information technology and communications [direct category crosswalk: Information technology and communications → ICT & Computing] (n=18) | Yes |
| 2 | NYSC-C002 | Information & Communication Technology Technician | 22 | 81.8 | 100.0 | 12.6% | 21.0% | 75.0% | sector interest: Information technology and communications [direct category crosswalk: Information technology and communications → ICT & Computing] (n=18) | Yes |
| 2 | NYSC-C003 | Computer Hardware Technician (Full Time) | 22 | 81.8 | 100.0 | 12.6% | 21.0% | 75.0% | sector interest: Information technology and communications [direct category crosswalk: Information technology and communications → ICT & Computing] (n=18) | Yes |
| 2 | NYSC-C004 | Computer Network Technician | 22 | 81.8 | 100.0 | 12.6% | 21.0% | 75.0% | sector interest: Information technology and communications [direct category crosswalk: Information technology and communications → ICT & Computing] (n=18) | Yes |
| 2 | NYSC-C005 | Computer Hardware Technician (Part Time) | 22 | 81.8 | 100.0 | 12.6% | 21.0% | 75.0% | sector interest: Information technology and communications [direct category crosswalk: Information technology and communications → ICT & Computing] (n=18) | Yes |
| 2 | NYSC-C006 | Computer Hardware And Network Technician | 22 | 81.8 | 100.0 | 12.6% | 21.0% | 75.0% | sector interest: Information technology and communications [direct category crosswalk: Information technology and communications → ICT & Computing] (n=18) | Yes |
| 2 | NYSC-C007 | Computer Certificate | 22 | 81.8 | 100.0 | 12.6% | 21.0% | 75.0% | sector interest: Information technology and communications [direct category crosswalk: Information technology and communications → ICT & Computing] (n=18) | Yes |
| 2 | NYSC-C008 | Computer Applications Assistant | 22 | 81.8 | 100.0 | 12.6% | 21.0% | 75.0% | sector interest: Information technology and communications [direct category crosswalk: Information technology and communications → ICT & Computing] (n=18) | Yes |
| 2 | NYSC-C009 | Computer Based Accounting | 22 | 81.8 | 100.0 | 12.6% | 21.0% | 75.0% | sector interest: Information technology and communications [direct category crosswalk: Information technology and communications → ICT & Computing] (n=18) | Yes |

These courses reflect aggregated evidence across F-S1. They are not recommendations for every F-S1 member.

The table is limited to ten rows. Several ICT courses have exactly the same aggregate rank and metrics; course ID controls which tied rows are displayed and does not imply that an omitted tied ICT course is less suitable.

## F-S2 Top 10 programme relevance

| Aggregate rank | Course ID | Course | Valid score n | Mean | Median | Tie-adjusted Top 3 | Tie-adjusted Top 5 | ≥70 | Dominant reasons | Broad-category-only? |
|---:|---|---|---:|---:|---:|---:|---:|---:|---|---|
| 1 | NYSC-C009 | Computer Based Accounting | 48 | 75.0 | 100.0 | 16.0% | 23.8% | 75.0% | sector interest: Information technology and communications [direct category crosswalk: Information technology and communications → ICT & Computing] (n=34); sector interest: Finance, banking, and insurance [explicit finance/accounting text crosswalk] (n=2) | No |
| 2 | NYSC-C018 | Freelancer of Web Design & Development | 48 | 82.3 | 100.0 | 13.9% | 21.8% | 70.8% | sector interest: Information technology and communications [direct category crosswalk: Information technology and communications → ICT & Computing] (n=34); explicit self-employment/freelancing content (n=27) | No |
| 3 | NYSC-C001 | National Diploma in Information & Communication Technology | 48 | 70.8 | 100.0 | 11.8% | 19.8% | 70.8% | sector interest: Information technology and communications [direct category crosswalk: Information technology and communications → ICT & Computing] (n=34) | Yes |
| 3 | NYSC-C002 | Information & Communication Technology Technician | 48 | 70.8 | 100.0 | 11.8% | 19.8% | 70.8% | sector interest: Information technology and communications [direct category crosswalk: Information technology and communications → ICT & Computing] (n=34) | Yes |
| 3 | NYSC-C003 | Computer Hardware Technician (Full Time) | 48 | 70.8 | 100.0 | 11.8% | 19.8% | 70.8% | sector interest: Information technology and communications [direct category crosswalk: Information technology and communications → ICT & Computing] (n=34) | Yes |
| 3 | NYSC-C004 | Computer Network Technician | 48 | 70.8 | 100.0 | 11.8% | 19.8% | 70.8% | sector interest: Information technology and communications [direct category crosswalk: Information technology and communications → ICT & Computing] (n=34) | Yes |
| 3 | NYSC-C005 | Computer Hardware Technician (Part Time) | 48 | 70.8 | 100.0 | 11.8% | 19.8% | 70.8% | sector interest: Information technology and communications [direct category crosswalk: Information technology and communications → ICT & Computing] (n=34) | Yes |
| 3 | NYSC-C006 | Computer Hardware And Network Technician | 48 | 70.8 | 100.0 | 11.8% | 19.8% | 70.8% | sector interest: Information technology and communications [direct category crosswalk: Information technology and communications → ICT & Computing] (n=34) | Yes |
| 3 | NYSC-C007 | Computer Certificate | 48 | 70.8 | 100.0 | 11.8% | 19.8% | 70.8% | sector interest: Information technology and communications [direct category crosswalk: Information technology and communications → ICT & Computing] (n=34) | Yes |
| 3 | NYSC-C008 | Computer Applications Assistant | 48 | 70.8 | 100.0 | 11.8% | 19.8% | 70.8% | sector interest: Information technology and communications [direct category crosswalk: Information technology and communications → ICT & Computing] (n=34) | Yes |

These courses reflect aggregated evidence across F-S2. They are not recommendations for every F-S2 member.

The table is limited to ten rows. Several ICT courses have exactly the same aggregate rank and metrics; course ID controls which tied rows are displayed and does not imply that an omitted tied ICT course is less suitable.

## Diagnostics

- Respondent-course scores available: **6,092/7,047 (86.4%)**. Unavailable rows remain blank, not zero.
- Scores based on sector with no entrepreneurship component: **6,053/6,092 (99.4%)**.
- Respondent-course rows with explicit entrepreneurship evidence: **39**.
- Only **1 of 87 courses** has defensible explicit entrepreneurship/self-employment wording after rejecting generic management wording: NYSC-C018 Freelancer of Web Design & Development.
- V2 has no individual-fit fields for fees, centres/location, entry requirements, current intake, delivery support, placements or employment outcomes. None was inferred.
- Many courses within a matched broad category receive identical evidence. Their internal ordering is therefore not a defensible claim of precise demand; this is why tie-adjusted metrics and broad-category flags are reported.
- The two displayed Top 10 sets overlap on **10/10 courses**. This overlap is descriptive and partly reflects tied ICT courses rather than fine-grained course preference.
- The 70/100 threshold is a transparent descriptive convention for this prototype, not an empirically validated cut-off.
- The individual file retains the actual answers, every component, N/A status, strict rank, tie-adjusted credit, reasons and cautions.

## Scientific judgment

### 1. Is this defensible for Branch F?

**Yes, as an exploratory group-level broad programme-relevance summary; no, as a precise course recommender.** It is defensible because it aggregates actual individual answers and never assigns preferences from cluster membership. However, it mostly measures sector demand, not detailed course fit.

### 2. What should change before D/E/G?

- Collect direct desired skill/topic, target occupation, instruction language, attendance availability, maximum duration and NVQ/certificate preference.
- Confirm and document the sector-to-course crosswalk with NYSC subject experts.
- Correct or separately validate V2's over-broad `entrepreneurship_content` field; generic management wording is not sufficient evidence of entrepreneurship training.
- Obtain course location, fees, entry requirements, current intake and support information before applying hard filters.
- Pre-specify weights and perform sensitivity analysis only after stronger inputs exist.
- Use a declared tie policy because broad survey categories cannot distinguish many courses within the same catalogue category.

### 3. Do F-S1 and F-S2 show meaningfully different demand patterns?

The profiles show **modest contextual differences but not a clearly different course-demand structure**. ICT is dominant in both (F-S1 18/29=62.1%; F-S2 34/52=65.4%). F-S2 has somewhat higher further-training interest and self-employment interest, while F-S1 has higher job-change interest. These differences are descriptive and do not justify treating cluster membership itself as a course recommendation rule.
