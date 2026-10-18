# Research progress after Step 34

Running log for the remaining-course research (Steps 35 onward). Each batch is saved before the next begins. Nothing here is committed, pushed or deployed. All new records are `source_inspected_pending_human_review`.

## Step 35 — business and education (saved)

| Course | Result | Comparators | Notes |
|---|---|---|---|
| COURSE-041 Preschool Teacher (Early Childhood Development) | FULL_COMPARISON (8-row matrix; 4 Areas) | LK-TVEC-NCS-ECCD-TEACHER-2026; IN-DGT-CTS-EARLY-CHILDHOOD-EDUCATOR-V2; AU-TGA-CHC30125 | Heading 1 ('Handling skills and design') is too unspecific to cite. M80S001 revision 2 carried the NYSC title; revision 4 renames it. The endorsement page lists an undefined unit U12. |
| COURSE-071 Human Recources Management | FULL_COMPARISON (10-row matrix; 1 Area) | LK-TVEC-NCS-HR-ASSOCIATE-2024; LK-TVEC-NCS-HRM-DIPLOMA-2022; AU-TGA-BSB40420 | Abbreviations ('T and D', 'PE System', 'LR System') are INSUFFICIENT_DATA, never Areas. Both Sri Lankan standards are past their review dates. No developing-economy HR comparator exists in DGT, TESDA or the inspected NQR results. |
| COURSE-084 Store Management | COMPARATORS_ONLY | LK-TVEC-NCS-STORE-KEEPER-2019; IN-DGT-ATS-STORAGE-INVENTORY-EXECUTIVE; AU-TGA-TLI30325-WAREHOUSING | No governed headings. The Sri Lankan standard is past its review date; the DGT apprenticeship curriculum is undated. |
| COURSE-049 Business Managemant | RESEARCH_PENDING | — | No governed headings and a generic title. Candidate sources (Sri Lankan Business Associate J65S001 2014, Management Services Assistant/Officer K74S010/K74S011, Australian BSB40520/BSB50120) cannot be matched to an unstated scope without NYSC syllabi. |

Coverage after Step 35: 28 FULL_COMPARISON, 39 COMPARATORS_ONLY, 17 RESEARCH_PENDING; 112 records; 28 mappings.

## Step 36 — agriculture (saved)

| Course | Result | Comparators | Notes |
|---|---|---|---|
| COURSE-020 Landscape Development Assistant | COMPARATORS_ONLY | LK-TVEC-NCS-FLORICULTURE-LANDSCAPE-2022; IN-DGT-CTS-FLORICULTURE-LANDSCAPING-V2; PH-TESDA-LANDSCAPE-NC2; AU-TGA-AHC30921 | The exact-title Sri Lankan standard O92S001 (2014/2017) was not stored in favour of the 2022 A01S019. The Australian record is construction-weighted. |
| COURSE-026 Field Assistant (agricultural) | COMPARATORS_ONLY | LK-TVEC-NCS-FIELD-ASSISTANT-AGRICULTURE-2021; IN-DGT-CTS-HORTICULTURE-V2; PH-TESDA-AGRI-CROPS-NC3 | No developed comparator: AHC30122's only core units are generic. |
| COURSE-032 Plant Nursery Development Assistant | COMPARATORS_ONLY | LK-TVEC-NCS-PLANT-NURSERY-2022; IN-DGT-CTS-NURSERY-ORCHARD-V1; PH-TESDA-HORTICULTURE-NC3; AU-TGA-AHC31124 | Exact-title Sri Lankan standard. The TESDA regulations date from 2006/2008. |

Coverage after Step 36: 28 FULL_COMPARISON, 42 COMPARATORS_ONLY, 14 RESEARCH_PENDING; 123 records; 28 mappings.

TESDA PDFs: only direct `Downloadables` URLs were used. TESDA's own download modal (which asks for purpose and country) was not submitted.

## Step 37 — media and crafts (saved)

| Course | Result | Comparators | Notes |
|---|---|---|---|
| COURSE-031 National Diploma In Television Program Production | COMPARATORS_ONLY | LK-TVEC-NCS-TV-DIGITAL-MEDIA-PRODUCTION-2025; PH-TESDA-FILM-VIDEO-POSTPRODUCTION-NC3; SG-ITE-HNITEC-FILM-VIDEO-2Y | The Sri Lankan endorsement and review dates are blank. TESDA covers post-production only. Australia's CUA51020 was not used (generic core). |
| COURSE-059 Non-Liner Video Editing With Digital 3D Animation | COMPARATORS_ONLY | LK-TVEC-NCS-MULTIMEDIA-DESIGNING-ASSOCIATE-2019; IN-DGT-CTS-MASE-V2; PH-TESDA-3D-ANIMATION-NC3; PH-TESDA-FILM-VIDEO-POSTPRODUCTION-NC3 | The Sri Lankan Video Editor standard (O92S004) is an unendorsed 'Final document for validation' and was not stored. No developed-economy comparator. |
| COURSE-028 Lapiderist (Gem Cutting) | COMPARATORS_ONLY | LK-TVEC-NCS-LAPIDARIST-2022 | Single exact-occupation Sri Lankan standard. The searches made (training.gov.au, TESDA's training-regulations listing, web searches of India's NQR) did not identify an international gem-cutting curriculum with inspectable content. |
| COURSE-075 Mass Communication | RESEARCH_PENDING | — | The single heading mixes literary and arts components with print and radio; journalism standards match only a fragment. |
| COURSE-070 Handycraft | RESEARCH_PENDING | — | The craft type is unspecified. |

## Step 38 — languages (saved)

| Course | Result | Comparators | Notes |
|---|---|---|---|
| COURSE-066 Professional English | COMPARATORS_ONLY | AU-VIC-22643VIC-EAL-EMPLOYMENT; AU-VIC-22644VIC-EAL-PROFESSIONAL | Victorian EAL Framework (accredited 2024–2028, CC BY-ND); its units are published only in the Victorian government curriculum document, not on training.gov.au. |
| COURSE-004 Professional English | COMPARATORS_ONLY | same as COURSE-066 | The governed record omits sector, attendance type and duration. |
| COURSE-003, 067, 072, 074, 083, 086 | RESEARCH_PENDING (research status NO_DEFENSIBLE_COMPARATOR) | — | No language qualification with inspectable content was found in the sources searched (training.gov.au search, TESDA's training-regulations listing, the Sri Lankan NVQ occupation list); DGT, India's NQR and Singapore's ITE were not searched for language courses. JLPT and TOPIK are tests, not curricula. The Open University of Sri Lanka pages that could be read show descriptions but no module lists (some certificate and Korean pages could not be read); module-less records would depart from the methodology. |

## Final status after Step 38

- 84 courses: 28 FULL_COMPARISON, 47 COMPARATORS_ONLY, 9 RESEARCH_PENDING.
- 132 records; 28 mappings.
- Still RESEARCH_PENDING, each with a documented reason in the coverage register (`COURSE_NOTES`): COURSE-003, 049, 067, 070, 072, 074, 075, 083, 086.

Validation note: `racComparators.test.ts` pinned 63 records at HEAD although HEAD already held 100. That was a pre-existing stale count, now updated to the current total.

## Post-audit fixes (read-only audit findings)

- **Stale tests:** `test_step27_occupation_groups.py` and `step27OccupationComparators.test.ts` now assert the current classifications. COURSE-038 links only IN-DGT-CTS-2W3W-V2; COURSE-062 is a full comparison including IN-DGT-CTS-DTPO-V2; COURSE-049 is pending with research status NO_DEFENSIBLE_COMPARATOR.
- **Search-scope claims:** the register notes for COURSE-003, 067, 072, 074, 083 and 086, the dataset gap notes (human_resources, lapidary, english_language, ict_diploma) and the COURSE-028 link caveat now name only the sources actually searched or read.
- **New research status:** the 9 researched-but-unresolved courses now carry research status `NO_DEFENSIBLE_COMPARATOR`. They remain `RESEARCH_PENDING` in the dashboard, which shows "No defensible comparison found" with each documented reason.
- **Dashboard notice:** a dashboard-level notice states that comparator records have not yet been independently reviewed. `source_inspected_pending_human_review` is unchanged.
- **Source disclosure:** each comparator card now has a collapsed "Source version and notes" section showing the stored version/revision text, retrieval date and record notes, including passed review dates.
- **MASE duration:** IN-DGT-CTS-MASE-V2's duration is now the exact general-information wording ("One Years (1200 Hours + 150 Hours OJT/Group Project)").
