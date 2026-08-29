# NYSC Course Intelligence Dataset Report

## Outcome

The two supplied catalogue files contain **87 unique course entries**, not 95. The HTML has 87 structured course objects and the DOCX has 87 identifiable course entries; all 87 course names match exactly across the sources. Both catalogue designs display **95 courses**, leaving an unexplained shortfall of **8 entries**. No placeholder courses were invented.

The resulting dataset has **87 rows** (one per retained catalogue entry) and **157 columns**. It preserves the raw HTML object, the DOCX record text and page range, both source module lists, canonical explicit values, normalized matching fields, and source-support text.

## Source files

- `CourseCatalogDetails/NYSC_Course_Catalogue.html` — machine-readable structured core and a footer stating that current intake dates and fees must be obtained directly from NYSC.
- `CourseCatalogDetails/NYSC_Course_Catalogue.docx` — the same course-level core plus an explicit guide: Full Time courses run on weekdays; Part Time courses run on weekends; Max Students means maximum intake per batch; NVQ is the level awarded where applicable; Course Overview is the modules/units list.

## Reconciliation of the 95-course claim

| Category | DOCX heading claim | HTML entries | DOCX entries |
|---|---:|---:|---:|
| ICT & Computing | 18 | 18 | 18 |
| Automotive & Mechanical Engineering | 15 | 15 | 15 |
| Electrical & Electronics | 8 | 8 | 8 |
| Construction & Surveying | 8 | 8 | 8 |
| Hospitality & Culinary Arts | 6 | 6 | 6 |
| Beauty, Fashion & Personal Care | 9 | 9 | 9 |
| Agriculture & Environment | 5 | 5 | 5 |
| Business, Management & Administration | 5 | 5 | 5 |
| Languages & Communication | 8 | 8 | 8 |
| Creative Arts, Design & Media | 5 | 5 | 5 |

The ten category claims sum to 87, confirming that the internal category counts support 87 rather than the displayed 95. The supplied files do not identify the eight missing entries, so their identity and attributes remain unknown.

## Selected field completeness

| Field | Populated | Completeness |
|---|---:|---:|
| `exact_course_name` | 87/87 | 100.0% |
| `category` | 87/87 | 100.0% |
| `schedule_raw` | 87/87 | 100.0% |
| `language_raw` | 87/87 | 100.0% |
| `maximum_students` | 87/87 | 100.0% |
| `duration_raw` | 87/87 | 100.0% |
| `nvq_level_raw` | 32/87 | 36.8% |
| `modules_json` | 36/87 | 41.4% |
| `explicit_target_occupations` | 55/87 | 63.2% |
| `content_keywords` | 70/87 | 80.5% |
| `training_centre` | 0/87 | 0.0% |
| `fees` | 0/87 | 0.0% |
| `entry_requirements` | 0/87 | 0.0% |
| `start_dates` | 0/87 | 0.0% |
| `placement_job_support` | 0/87 | 0.0% |

The completeness audit CSV contains the percentage for every output field, not only this selected list.

## Explicitly absent information

The following information is not explicitly supplied and is therefore left blank/unknown rather than coded as false:

- target audience, objectives, outcomes and progression routes
- entry requirements, age, prerequisite subjects, prior experience and selection methods
- training centre, district, address, multi-centre status and online/hybrid delivery
- fees, registration/material costs, subsidies, scholarships, stipends and payment terms
- intake dates, frequency, deadlines and waiting-list information
- contact hours and practical/theory delivery split
- employer links, internships, apprenticeships, placement support and measured employment outcomes
- accommodation, transport, learner support, counselling and mentoring

`employment_support_present`, `entrepreneurship_content_present`, and `practical_training_present` deliberately use blank for **unknown**. A true value is used only when direct wording supports it; absence of wording is not treated as evidence that the feature is unavailable.

## Normalization and traceability rules

- Category is retained and normalized as the broad skill area and explicit sector tag.
- Full Time/Part Time is retained as schedule category. Weekdays/weekends is added only because the DOCX guide explicitly defines that mapping; no evening schedule is inferred.
- Duration is mechanically parsed to number/unit and total months, with the raw duration retained.
- Language spellings and separators are normalized to a JSON list, with the raw medium-of-instruction text retained.
- NVQ wording is normalized only where the source states an NVQ level.
- Occupation tags are added only when an occupation is named in the course title.
- Content keywords come only from exact course-title or module text using a documented controlled vocabulary.
- Practical, theory, assessment, entrepreneurship, language, safety, tools/software, and soft-skill fields contain the exact supporting title/module units. No unstated curriculum is inferred.

## Duplicates, variants and source conflicts

| Issue | Rows/pairs |
|---|---:|
| cross source module conflict | 2 |
| near duplicate course name | 1 |
| possible schedule or language variant | 16 |

Explicit Full Time/Part Time and language variants are retained as separate catalogue entries. The conflicts file identifies pairs for human confirmation rather than merging them automatically.

## Source richness

At course level, HTML and DOCX have essentially the same structured attributes. HTML is easier to parse reliably; DOCX is semantically richer because its guide defines schedule, batch size, NVQ and overview meanings and retains page context. Course-level module wording is reconciled in the conflicts file wherever it differs.

## Courses needing human review

- High priority: 2
- Medium priority: 32
- Low priority: 49
- No course-specific issue: 4

High priority denotes a cross-source discrepancy or unmatched record. Medium priority denotes a record with neither module/overview detail nor an NVQ level. Low priority covers one missing core detail or a likely deliberate course variant.

- NYSC-C018: Freelancer of Web Design & Development — cross-source conflict or unmatched record | no NVQ level stated
- NYSC-C077: Japanese Language — cross-source conflict or unmatched record | no NVQ level stated
- NYSC-C006: Computer Hardware And Network Technician — no course overview/modules stated | no NVQ level stated
- NYSC-C007: Computer Certificate — no course overview/modules stated | no NVQ level stated
- NYSC-C010: Cisco Certified Network Associate — no course overview/modules stated | no NVQ level stated
- NYSC-C011: Multimedia & Web Design — no course overview/modules stated | no NVQ level stated
- NYSC-C012: Micro Controller Circuit Designing — no course overview/modules stated | no NVQ level stated
- NYSC-C013: Java Programming With Software Applications Development — no course overview/modules stated | no NVQ level stated
- NYSC-C015: AutoCAD — no course overview/modules stated | no NVQ level stated
- NYSC-C016: Non-Linear Video Editing With Digital 3D Animation — no course overview/modules stated | no NVQ level stated
- NYSC-C017: PYTHON — no course overview/modules stated | no NVQ level stated
- NYSC-C022: Automobile Electrician (Full Time – Sinhala) — no course overview/modules stated | no NVQ level stated | possible duplicate or explicit course variant
- NYSC-C026: Aluminium Fabricator — no course overview/modules stated | no NVQ level stated
- NYSC-C030: Motorcycle Mechanic (Part Time) — no course overview/modules stated | no NVQ level stated | possible duplicate or explicit course variant
- NYSC-C031: Motor Winding — no course overview/modules stated | no NVQ level stated
- NYSC-C032: Motor Controlling Technology — no course overview/modules stated | no NVQ level stated
- NYSC-C040: Mobile Phone Repair Technician (Part Time) — no course overview/modules stated | no NVQ level stated | possible duplicate or explicit course variant
- NYSC-C046: Construction Site Supervisor (Part Time) — no course overview/modules stated | no NVQ level stated | possible duplicate or explicit course variant
- NYSC-C047: Draughtperson — no course overview/modules stated | no NVQ level stated
- NYSC-C048: Engineering Draughtsmanship — no course overview/modules stated | no NVQ level stated
- NYSC-C049: Designing & Space Planning For Draughtsmanship — no course overview/modules stated | no NVQ level stated
- NYSC-C053: Cook — no course overview/modules stated | no NVQ level stated
- NYSC-C054: Cake Decorator — no course overview/modules stated | no NVQ level stated
- NYSC-C059: Hair Dresser (Part Time) — no course overview/modules stated | no NVQ level stated | possible duplicate or explicit course variant
- NYSC-C060: Bridal Dresser — no course overview/modules stated | no NVQ level stated
- NYSC-C062: Tailor (Part Time) — no course overview/modules stated | no NVQ level stated | possible duplicate or explicit course variant
- NYSC-C064: Handycraft — no course overview/modules stated | no NVQ level stated
- NYSC-C069: Landscaping Technician (Part Time) — no course overview/modules stated | no NVQ level stated | possible duplicate or explicit course variant
- NYSC-C072: Business Management — no course overview/modules stated | no NVQ level stated
- NYSC-C074: Store Management — no course overview/modules stated | no NVQ level stated
- NYSC-C076: Professional English — no course overview/modules stated | no NVQ level stated
- NYSC-C079: French Language — no course overview/modules stated | no NVQ level stated
- NYSC-C080: Sinhala Language — no course overview/modules stated | no NVQ level stated
- NYSC-C084: Graphics Designer (Part Time) — no course overview/modules stated | no NVQ level stated | possible duplicate or explicit course variant

The complete course-level review list, including low-priority items, is in `outputs/nysc_course_catalogue_completeness_audit.csv` under `audit_type=course_human_review`.

## Output files

- `outputs/nysc_course_intelligence_dataset.csv` — one row per unique catalogue entry.
- `outputs/nysc_course_intelligence_data_dictionary.csv` — field definitions, types, null meaning and support rules.
- `outputs/nysc_course_catalogue_completeness_audit.csv` — claim reconciliation, source/category counts, all-field completeness, source richness and course review flags.
- `outputs/nysc_course_source_conflicts.csv` — source disagreements, exact/near duplicates and explicit schedule/language variants.

## Interpretation boundary

This is catalogue extraction and explicit normalization, not a recommendation model. A blank means **not stated in the supplied catalogues**. It must not be interpreted as “No,” “not eligible,” or “not available.” Current operational details should be verified with NYSC before future recommendation logic treats them as filters.
