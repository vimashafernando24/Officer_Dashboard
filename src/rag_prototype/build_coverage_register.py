"""Write the machine-readable coverage register for all 84 governed NYSC courses.

Course IDs, titles and module headings come from the governed catalogue (via the
verified loader); comparator and mapping status come from the stored
benchmarking files. Only the occupation grouping, related variants, research
status and the reasons for any non-derivable classification are curated here.
Nothing in this register is evidence: it records what evidence exists.

It also writes two generated frontend files, so the dashboard ships only what it
needs and loads comparator data per selected course:
  * src/data/coverageIndex.json: per course, only the fields needed for display and
    state calculation, plus which record dataset holds each linked record;
  * src/data/comparisonDataLoaders.ts: one lazy loader per record dataset and per
    competency mapping, discovered from outputs/programme_benchmarking/.
A new occupation is registered by adding its pilot_records_<name>.json, its
competency_mapping_course-<id>.json files and its links, then re-running this script.

Run from the repository root:  python3 src/rag_prototype/build_coverage_register.py
"""

from __future__ import annotations

import json
from pathlib import Path

try:
    from .programme_design_evidence import load_governed_courses
except ImportError:  # pragma: no cover - supports direct script execution
    from programme_design_evidence import load_governed_courses

BASE = Path(__file__).resolve().parents[2]
BENCHMARK_DIR = BASE / "outputs/programme_benchmarking"
REGISTER_PATH = BENCHMARK_DIR / "coverage_register.json"
SNAPSHOT_PATH = BASE / "src/rag_prototype/frontend/src/data/nyscCourseCatalogue.json"
FRONTEND_DATA = BASE / "src/rag_prototype/frontend/src/data"
INDEX_PATH = FRONTEND_DATA / "coverageIndex.json"
LOADERS_PATH = FRONTEND_DATA / "comparisonDataLoaders.ts"
LINKS_PATH = BENCHMARK_DIR / "course_comparator_links.json"

# Occupation groups: courses that can share one set of external comparator records.
# (group_id, occupation, course IDs). Closely related courses in other groups are
# listed in RELATED, not merged, because they may need different comparators.
OCCUPATION_GROUPS = [
    ("automobile_mechanic", "Automobile mechanic", ["COURSE-005", "COURSE-040"]),
    ("electrician", "Electrician", ["COURSE-025", "COURSE-064"]),
    ("rac_technician", "Refrigeration and air conditioning technician", ["COURSE-034", "COURSE-012"]),
    ("computer_hardware_technician", "Computer hardware technician", ["COURSE-008", "COURSE-055"]),
    ("computer_hardware_network_technician", "Computer hardware and network technician", ["COURSE-056"]),
    ("computer_network_technician", "Computer network technician", ["COURSE-022"]),
    ("ccna", "Cisco Certified Network Associate (vendor certification)", ["COURSE-052"]),
    ("baker", "Baker", ["COURSE-011", "COURSE-047"]),
    ("cake_decorator", "Cake decorator", ["COURSE-050", "COURSE-051"]),
    ("professional_cookery", "Professional cookery", ["COURSE-007"]),
    ("beautician", "Beautician", ["COURSE-010", "COURSE-046"]),
    ("bridal_dresser", "Bridal dresser", ["COURSE-048"]),
    ("hair_dresser", "Hair dresser", ["COURSE-014", "COURSE-069"]),
    ("secretary", "Secretary (secretarial practices)", ["COURSE-035", "COURSE-082"]),
    ("electronic_appliances_technician", "Electronic appliances technician", ["COURSE-013"]),
    ("radio_tv_repairer", "Radio, TV and allied equipment repairer", ["COURSE-081"]),
    ("ict_technician", "ICT technician", ["COURSE-009"]),
    ("national_diploma_ict", "National Diploma in ICT", ["COURSE-006"]),
    ("web_designer", "Web design and development", ["COURSE-087", "COURSE-057", "COURSE-001"]),
    ("graphic_designer", "Graphic designer", ["COURSE-016", "COURSE-068"]),
    ("desktop_publisher", "Desktop publisher", ["COURSE-062"]),
    ("tailor", "Tailor", ["COURSE-037", "COURSE-085"]),
    ("dressmaker", "Dressmaker", ["COURSE-063"]),
    ("preschool_teacher", "Preschool teacher (early childhood development)", ["COURSE-041"]),
    ("automobile_electrician", "Automobile electrician", ["COURSE-021", "COURSE-042"]),
    ("motorcycle_mechanic", "Motorcycle mechanic", ["COURSE-030", "COURSE-078"]),
    ("three_wheeler_mechanic", "Three-wheeler mechanic", ["COURSE-038"]),
    ("welder", "Welder", ["COURSE-045"]),
    ("machinist", "Machinist", ["COURSE-044"]),
    ("plumber", "Plumber", ["COURSE-033"]),
    ("agricultural_machinery_mechanic", "Agricultural machinery mechanic", ["COURSE-017"]),
    ("motor_winding", "Motor winding", ["COURSE-080"]),
    ("motor_control_technology", "Motor controlling technology", ["COURSE-079"]),
    ("mobile_phone_repair_technician", "Mobile phone repair technician", ["COURSE-029", "COURSE-077"]),
    ("draughtsperson", "Draughtsperson / draughtsmanship", ["COURSE-024", "COURSE-065", "COURSE-061"]),
    ("autocad", "AutoCAD (software course)", ["COURSE-043"]),
    ("construction_site_supervisor", "Construction site supervisor", ["COURSE-023", "COURSE-060"]),
    ("survey_field_assistant", "Survey field assistant", ["COURSE-036"]),
    ("quantity_surveying_assistant", "Quantity surveying assistant", ["COURSE-019"]),
    ("agricultural_field_assistant", "Agricultural field assistant", ["COURSE-026"]),
    ("landscape_development_assistant", "Landscape development assistant", ["COURSE-020"]),
    ("plant_nursery_assistant", "Plant nursery development assistant", ["COURSE-032"]),
    ("computer_applications", "Computer applications / computer literacy", ["COURSE-053", "COURSE-054"]),
    ("computer_based_accounting", "Computer-based accounting", ["COURSE-058"]),
    ("human_resource_management", "Human resource management", ["COURSE-071"]),
    ("store_management", "Store management", ["COURSE-084"]),
    ("business_management", "Business management", ["COURSE-049"]),
    ("tv_programme_production", "Television programme production", ["COURSE-031"]),
    ("video_editing_animation", "Video editing and 3D animation", ["COURSE-059"]),
    ("python_programming", "Python programming", ["COURSE-002"]),
    ("java_programming", "Java programming and software development", ["COURSE-073"]),
    ("microcontroller_design", "Micro-controller circuit design", ["COURSE-076"]),
    ("aluminium_fabricator", "Aluminium fabricator", ["COURSE-018"]),
    ("lapidarist", "Lapidarist (gem cutting)", ["COURSE-028"]),
    ("handicraft", "Handicraft", ["COURSE-070"]),
    ("english_language", "English language", ["COURSE-003", "COURSE-004", "COURSE-066"]),
    ("french_language", "French language", ["COURSE-067"]),
    ("japanese_language", "Japanese language", ["COURSE-072"]),
    ("korean_language", "Korean language", ["COURSE-074"]),
    ("sinhala_language", "Sinhala language", ["COURSE-083"]),
    ("tamil_language", "Tamil language", ["COURSE-086"]),
    ("mass_communication", "Mass communication", ["COURSE-075"]),
]

# Closely related courses in other groups (symmetric), e.g. siblings that may reuse some comparators.
RELATED = [
    ("COURSE-008", "COURSE-056"), ("COURSE-055", "COURSE-056"), ("COURSE-056", "COURSE-022"),
    ("COURSE-022", "COURSE-052"), ("COURSE-011", "COURSE-050"), ("COURSE-011", "COURSE-051"),
    ("COURSE-047", "COURSE-050"), ("COURSE-047", "COURSE-051"), ("COURSE-010", "COURSE-048"),
    ("COURSE-046", "COURSE-048"), ("COURSE-013", "COURSE-081"), ("COURSE-009", "COURSE-006"),
    ("COURSE-016", "COURSE-062"), ("COURSE-068", "COURSE-062"), ("COURSE-037", "COURSE-063"),
    ("COURSE-085", "COURSE-063"), ("COURSE-030", "COURSE-038"), ("COURSE-078", "COURSE-038"),
    ("COURSE-080", "COURSE-025"), ("COURSE-080", "COURSE-064"), ("COURSE-079", "COURSE-025"),
    ("COURSE-079", "COURSE-064"), ("COURSE-079", "COURSE-080"), ("COURSE-043", "COURSE-024"),
    ("COURSE-043", "COURSE-065"), ("COURSE-043", "COURSE-061"), ("COURSE-031", "COURSE-059"),
    ("COURSE-002", "COURSE-073"), ("COURSE-053", "COURSE-058"),
]

# Headings that exist but contain no curriculum content (a fee/exam note or a generic statement).
UNUSABLE_HEADINGS = {
    "COURSE-072": "The only heading cites an exam syllabus level and course-material fees ('JLPT - N5 & NAT - N5 Course Syllabues (Rs. 1500.00 Fees for Course Meterials)'); it names no module content.",
    "COURSE-074": "The only heading is a generic statement ('Cover all skills of Korean Language required to use the language efficiently'); it names no module content.",
    "COURSE-086": "The only heading is a generic statement ('Cover all skills of Tamil Language required to use the language efficiently'); it names no module content.",
}

# Known evidence caveats that do not change a course's classification.
COURSE_NOTES = {
    "COURSE-009": "Heading 10 is flagged in the snapshot as two merged headings and is not counted as verified.",
    "COURSE-037": "A single broad heading ('Women and children clothing').",
    "COURSE-063": "A single broad heading ('Women and children clothing', display-corrected).",
    "COURSE-058": "Headings name accounting software packages rather than accounting competencies.",
    "COURSE-071": "Headings use unexplained abbreviations (e.g. 'JD, JA', 'PE System, T and D', 'LR System').",
    "COURSE-004": "The governed record states no sector, attendance type or duration.",
    "COURSE-052": "A vendor certification; an official occupational comparator may not exist (not yet researched).",
    "COURSE-024": "The three draughting courses are grouped provisionally; civil and engineering draughting may need separate comparators.",
    "COURSE-065": "The three draughting courses are grouped provisionally; civil and engineering draughting may need separate comparators.",
    "COURSE-061": "The three draughting courses are grouped provisionally; civil and engineering draughting may need separate comparators.",
}

# Research status for courses whose comparator research is not complete. Every
# course not listed here and not complete is NOT_RESEARCHED. BLOCKED requires a
# documented, attempted research obstacle; none has been recorded yet.
RESEARCH_OVERRIDES: dict[str, dict] = {}

# Known gaps in completed comparisons that further official-source research could close.
COMPLETE_GAPS = {
    "automobile_mechanic": "TESDA's Chassis Repair and Electrical Repair regulations and TAFE NSW's specialty units are not collected; NYSC syllabi could add headings beyond the five published.",
    "electrician": "Singapore ITE life-skills and elective modules are not stored; NYSC syllabi could add headings beyond the five published.",
    "rac_technician": "No current Singapore RAC programme was verified and TESDA's Commercial Refrigeration NC III regulation was not obtained; NYSC syllabi could add headings beyond the four published.",
    "computer_hardware_technician": "No independent Sri Lankan programme with published modules was verified (DTET lists the course without modules; LAVTC is an NYSC centre); an Australian provider delivering hardware electives of ICT30120 could be added.",
    "baker": "No independent Sri Lankan Baker programme with sufficiently detailed published curriculum was verified; ITE's internally inconsistent course-specific elective text was excluded, and an Australian delivered-provider curriculum could complement the national qualification.",
    "cake_decorator": "The Sri Lankan source is an occupational standard rather than a confirmed delivery; COURSE-051 has no governed module headings, and the broader Australian Baking qualification was excluded because its cake-decoration evidence is incidental.",
    "ict_technician": "The Sri Lankan source is an occupational standard rather than a confirmed delivery; TESDA and ITE cover only the technical-support part of the role; Australian evidence is limited to ICT20120 core units; NYSC heading 10 is a merged heading that NYSC syllabi could clarify.",
    "computer_applications": "The Sri Lankan source is an occupational standard rather than a confirmed delivery; COPA is broader than computer applications; Australian evidence is limited to ICT20120 core units; COURSE-054 has no governed module headings.",
    "web_designer": "No Sri Lankan, Indian or Australian delivering provider was verified; India's qualification has broad module titles; ITE's programme is broader application development; COURSE-057 and COURSE-001 have no governed module headings.",
    "professional_cookery": "No independent Sri Lankan Professional Cookery programme with sufficiently detailed published curriculum was verified; TESDA NC III is broader and more supervisory, and Australian elective choices are not evidence that every learner completes them.",
    "beautician": "The Sri Lankan source is an occupational standard rather than a confirmed independent delivery; ITE course electives and Australian qualification electives are not guaranteed for every learner.",
    "bridal_dresser": "The governed catalogue publishes no module headings, so only broader beauty/cosmetology comparators can be shown and no Bridal Dresser competency matrix is defensible.",
    "hair_dresser": "The Sri Lankan source is an occupational standard rather than a confirmed independent delivery; ITE and Australian elective evidence is not guaranteed for every learner.",
    "secretary": "ITE is a broader business-administration programme, Australian administration/records units are elective choices, and the DGT source has an NSQF-level discrepancy between its current page and downloaded PDF.",
    "national_diploma_ict": "No developing/emerging-economy diploma-level ICT curriculum was verified (NIELIT's 'A' Level syllabus could not be retrieved); the Sri Lankan source is a competency standard without curriculum modules, ITE's programme covers application development only, and NYSC heading 7 is an uninterpretable fragment.",
    "computer_based_accounting": "No Sri Lankan computerised-accounting standard was verified; the NYSC headings name software packages rather than competencies, ITE's programme is a broader accounting diploma, and Australian evidence is limited to FNS30322 core units.",
    "radio_tv_repairer": "All three comparator sources are standards or national curricula rather than confirmed deliveries; no developed-economy comparator with sufficiently specific published radio/TV repair content was verified, and the NYSC LED-board heading retains an apparent governed-text typo.",
    "python_programming": "Only two broader Indian national curricula were verified; no Sri Lankan or developed-economy exact Python course with inspectable official curriculum content was collected, and the NYSC course has no governed headings.",
    "autocad": "The DGT source is a broader CAD/CAM apprenticeship curriculum and TESDA does not name AutoCAD; no Sri Lankan or developed-economy exact AutoCAD curriculum was verified, and the NYSC course has no governed headings.",
    "desktop_publisher": "Only the Indian DGT curriculum explicitly names all four governed applications; the other linked records provide related graphic-design evidence, and no exact Sri Lankan or developed-economy desktop-publishing curriculum was verified.",
    "java_programming": "Only one Java-specific national qualification was verified; no Sri Lankan, Indian or developed-economy exact comparator with inspectable official curriculum content was collected, and the NYSC course has no governed headings.",
    "microcontroller_design": "Only one broader Indian embedded-systems apprenticeship curriculum was verified; no Sri Lankan or second international exact comparator was collected, and the NYSC course has no governed headings.",
}


def build_register() -> dict:
    governed = load_governed_courses()
    by_id = {course["course_id"]: course for course in governed}
    snapshot = {c["course_id"]: c for c in json.loads(SNAPSHOT_PATH.read_text(encoding="utf-8"))["courses"]}
    links = {l["nysc_course_id"]: l["record_ids"] for l in json.loads(LINKS_PATH.read_text(encoding="utf-8"))["links"]}
    record_ids = {
        record["record_id"]
        for path in sorted(BENCHMARK_DIR.glob("pilot_records_*.json"))
        for record in json.loads(path.read_text(encoding="utf-8"))["records"]
    }
    mapped = {
        json.loads(path.read_text(encoding="utf-8"))["nysc_course_id"]
        for path in sorted(BENCHMARK_DIR.glob("competency_mapping_course-*.json"))
    }
    group_of = {cid: (gid, name, members) for gid, name, members in OCCUPATION_GROUPS for cid in members}
    related: dict[str, set[str]] = {}
    for left, right in RELATED:
        related.setdefault(left, set()).add(right)
        related.setdefault(right, set()).add(left)

    courses = []
    for course_id in sorted(by_id):
        course = by_id[course_id]
        group_id, occupation, members = group_of[course_id]
        flagged = {f["module_index"] for f in snapshot[course_id]["module_review_flags"]}
        headings = len(course["modules"])
        verified = 0 if course_id in UNUSABLE_HEADINGS else headings - len(flagged)
        comparators = [rid for rid in links.get(course_id, []) if rid in record_ids]
        has_mapping = course_id in mapped

        if headings == 0:
            availability = "NO_HEADINGS"
        elif course_id in UNUSABLE_HEADINGS:
            availability = "HEADINGS_UNUSABLE"
        else:
            availability = "HEADINGS_AVAILABLE"

        override = RESEARCH_OVERRIDES.get(course_id, {})
        if comparators and (has_mapping or availability != "HEADINGS_AVAILABLE"):
            # Complete: a mapping exists, or none is defensible because NYSC headings are missing or unusable.
            research = "COMPLETE"
        elif comparators:
            research = "IN_PROGRESS"  # verified comparators; mapping against usable headings still to do
        else:
            research = override.get("status", "NOT_RESEARCHED")

        # What the dashboard shows now, derived only from verified, stored evidence.
        if comparators:
            current_mode = "FULL_COMPARISON" if has_mapping else "COMPARATORS_ONLY"
        elif research == "BLOCKED":
            current_mode = "EVIDENCE_UNAVAILABLE"
        else:
            current_mode = "RESEARCH_PENDING"

        n = f"{verified} verified heading{'s' if verified != 1 else ''}"
        if research == "COMPLETE" and has_mapping:
            proposed = "FULL_COMPARISON"
            reason = (f"{n}, {len(comparators)} linked verified comparator records and a completed competency "
                      "mapping; the full comparison is already shown.")
        elif comparators:
            proposed = "FULL_COMPARISON" if availability == "HEADINGS_AVAILABLE" else "COMPARATORS_ONLY"
            reason = (f"{len(comparators)} linked verified comparator records. "
                      + ("A competency mapping against the usable NYSC headings has not been completed yet."
                         if availability == "HEADINGS_AVAILABLE" else
                         "The governed catalogue publishes no usable module headings for this course, so a competency "
                         "matrix cannot be assessed; the verified comparators are shown without one."))
        elif availability == "HEADINGS_AVAILABLE":
            proposed = "FULL_COMPARISON"
            reason = (f"{n} available. Comparator research has not started: a full comparison needs verified "
                      "official comparator records and a mapping first; no comparator is assumed.")
        elif availability == "HEADINGS_UNUSABLE":
            proposed = "COMPARATORS_ONLY"
            reason = (f"{UNUSABLE_HEADINGS[course_id]} A competency matrix cannot be assessed from it, but verified "
                      "comparator records could still be shown. Comparator research has not started.")
        else:
            proposed = "COMPARATORS_ONLY"
            reason = ("The governed catalogue publishes no module headings for this course, so a competency matrix "
                      "cannot be assessed; verified comparator records could still be shown. Comparator research "
                      "has not started. Missing NYSC headings do not imply that external comparators are missing.")

        if research == "COMPLETE" and has_mapping:
            improvement = COMPLETE_GAPS[group_id]
        elif comparators:
            improvement = ("NYSC syllabi or TVEC national competency standards could supply module headings for a full "
                           "comparison; further official comparators (e.g. a verified Sri Lankan programme) could be added.")
        elif availability == "HEADINGS_AVAILABLE":
            improvement = "Official comparator records (and NYSC syllabi) could enable a full comparison."
        else:
            improvement = ("Official comparator records could be verified and shown; NYSC syllabi or TVEC national "
                           "competency standards could supply headings for a full comparison.")

        entry = {
            "course_id": course_id,
            "governed_title": course["course_name"],
            "skill_area": course["skill_area"],
            "attendance_type": course["attendance_type"],
            "occupation_group_id": group_id,
            "occupation_group": occupation,
            "group_courses": members,
            "related_courses": sorted(related.get(course_id, set())),
            "governed_heading_count": headings,
            "display_corrected_heading_count": len(snapshot[course_id]["module_display_corrections"]),
            "review_flagged_heading_count": len(flagged),
            "verified_heading_count": verified,
            "comparator_record_ids": comparators,
            "comparator_record_count": len(comparators),
            "competency_mapping_status": "COMPLETE" if has_mapping else "NONE",
            "research_status": research,
            "evidence_availability": availability,
            "current_presentation_mode": current_mode,
            "proposed_presentation_mode": proposed,
            "proposed_mode_reason": reason,
            "further_research_could_improve": True,
            "research_improvement": improvement,
            "notes": [COURSE_NOTES[course_id]] if course_id in COURSE_NOTES else [],
        }
        if research == "BLOCKED":
            entry["blocking_evidence"] = override["blocking_evidence"]
        courses.append(entry)

    def count(field):
        totals: dict[str, int] = {}
        for entry in courses:
            totals[entry[field]] = totals.get(entry[field], 0) + 1
        return dict(sorted(totals.items()))

    occupation_ids = [gid for gid, _n, _m in OCCUPATION_GROUPS]
    complete_groups = sorted({e["occupation_group_id"] for e in courses if e["research_status"] == "COMPLETE"})
    return {
        "description": "Coverage register for all governed NYSC courses in the Programme Comparison Dashboard. It records which evidence exists for each course; it is not evidence itself. Course IDs, titles and headings come from the governed catalogue; comparator and mapping status from the stored benchmarking files. Regenerate with src/rag_prototype/build_coverage_register.py; do not edit by hand.",
        "register_version": "1.0.0",
        "created_date": "2026-10-18",
        "definitions": {
            "research_status": {
                "COMPLETE": "Verified comparator records are linked, and a competency mapping exists or cannot be defended because NYSC headings are missing or unusable.",
                "IN_PROGRESS": "Comparator research has started but records or a defensible mapping are incomplete.",
                "NOT_RESEARCHED": "No official comparator research has been carried out for this course.",
                "BLOCKED": "Research was attempted and a documented obstacle prevents progress (blocking_evidence is required).",
            },
            "evidence_availability": {
                "HEADINGS_AVAILABLE": "The governed catalogue publishes at least one usable NYSC module heading.",
                "NO_HEADINGS": "The governed catalogue publishes no NYSC module headings.",
                "HEADINGS_UNUSABLE": "Headings exist but name no curriculum content (e.g. a fee note or a generic statement).",
            },
            "presentation_mode": {
                "FULL_COMPARISON": "NYSC headings, verified comparators and a completed competency matrix with Areas to Investigate.",
                "COMPARATORS_ONLY": "Verified comparator records without a matrix, because no defensible NYSC competency mapping is available.",
                "RESEARCH_PENDING": "External comparator research has not been completed; no comparator records are linked.",
                "EVIDENCE_UNAVAILABLE": "Research was attempted, but the documented evidence is insufficient (research_status BLOCKED).",
            },
            "current_presentation_mode": "Derived only from verified, stored evidence (linked records, mappings, research status); never from the proposed mode.",
            "proposed_presentation_mode": "The target mode once research is complete; it is not shown on the dashboard as coverage.",
            "evidence_availability_scope": "Evidence availability describes NYSC headings only; it says nothing about whether external comparators exist.",
            "verified_heading_count": "Governed headings minus headings flagged for review; zero when the headings are unusable.",
        },
        "reconciliation": [
            "The Step 17 audit counted 49 occupation groups by merging five different languages and several distinct occupations; this register uses 62 groups, keeping occupations that would need different comparators separate and recording close siblings in related_courses.",
            "The Step 17 audit said at most 28 courses could receive a full comparison (6 + 22). The governed catalogue has 32 courses with headings; 3 of them (COURSE-072, COURSE-074, COURSE-086) contain no curriculum content, so 29 courses (6 complete + 23 not yet researched) have usable headings.",
            "The Step 17 audit placed about 9 courses in a 'not comparable' tier before any research. That is withdrawn: no unresearched course is classified as permanently not comparable, and none is BLOCKED because no research has been attempted.",
            "Step 18B: current_presentation_mode now uses RESEARCH_PENDING for courses whose comparator research has not been completed; EVIDENCE_UNAVAILABLE is reserved for BLOCKED research. Courses with verified comparators but no defensible mapping are COMPLETE (missing or unusable headings) or IN_PROGRESS (mapping still to do), never NOT_RESEARCHED.",
            "The Step 17 section-1 table's group and course counts did not match its batch table (e.g. 8 hard groups / 8 courses against 9 groups / 11 courses). The totals below are computed directly from the course entries.",
        ],
        "totals": {
            "courses": len(courses),
            "occupation_groups": len(occupation_ids),
            "occupation_groups_complete": len(complete_groups),
            "courses_with_governed_headings": sum(1 for e in courses if e["governed_heading_count"] > 0),
            "courses_with_comparators": sum(1 for e in courses if e["comparator_record_count"] > 0),
            "courses_with_mapping": sum(1 for e in courses if e["competency_mapping_status"] == "COMPLETE"),
            "research_status": count("research_status"),
            "evidence_availability": count("evidence_availability"),
            "current_presentation_mode": count("current_presentation_mode"),
            "proposed_presentation_mode": count("proposed_presentation_mode"),
        },
        "courses": courses,
    }


def record_datasets() -> dict[str, list[str]]:
    """Record dataset key (file name without 'pilot_records_') to its record IDs, in file order."""
    return {
        path.stem.removeprefix("pilot_records_"): [r["record_id"] for r in json.loads(path.read_text(encoding="utf-8"))["records"]]
        for path in sorted(BENCHMARK_DIR.glob("pilot_records_*.json"))
    }


def mapping_files() -> dict[str, str]:
    """Course ID to its competency mapping file name."""
    return {
        json.loads(path.read_text(encoding="utf-8"))["nysc_course_id"]: path.name
        for path in sorted(BENCHMARK_DIR.glob("competency_mapping_course-*.json"))
    }


def build_frontend_index(register: dict) -> dict:
    """The compact per-course index the dashboard ships: display and state fields only."""
    dataset_of = {rid: key for key, ids in record_datasets().items() for rid in ids}
    courses = {}
    for entry in register["courses"]:
        item = {
            "state": entry["current_presentation_mode"],
            "research": entry["research_status"],
            "headings": entry["evidence_availability"],
            "verified_headings": entry["verified_heading_count"],
            "records": entry["comparator_record_ids"],
            "datasets": sorted({dataset_of[rid] for rid in entry["comparator_record_ids"]}),
            "mapping": entry["competency_mapping_status"] == "COMPLETE",
        }
        if "blocking_evidence" in entry:
            item["blocking_evidence"] = entry["blocking_evidence"]
        courses[entry["course_id"]] = item
    return {
        "description": "Generated from coverage_register.json by src/rag_prototype/build_coverage_register.py; do not edit by hand. Only the fields the dashboard needs for display and state calculation.",
        "courses": courses,
    }


def build_loaders() -> str:
    """A generated TypeScript module with one lazy JSON loader per record dataset and mapping."""
    root = "../../../../../outputs/programme_benchmarking"
    lines = [
        "// GENERATED by src/rag_prototype/build_coverage_register.py: do not edit by hand.",
        "// One lazy loader per comparator record dataset and per competency mapping, so the",
        "// dashboard downloads comparator data only for the course being viewed.",
        "",
        "type JsonModule = Promise<{ default: unknown }>;",
        "",
        "export const RECORD_DATASET_LOADERS: Record<string, () => JsonModule> = {",
    ]
    for key in record_datasets():
        lines.append(f'  "{key}": () => import("{root}/pilot_records_{key}.json", {{ with: {{ type: "json" }} }}),')
    lines += ["};", "", "/** Dataset order, so loaded records keep a stable order. */",
              f"export const RECORD_DATASET_ORDER: string[] = {json.dumps(list(record_datasets()))};", "",
              "export const MAPPING_LOADERS: Record<string, () => JsonModule> = {"]
    for course_id, name in mapping_files().items():
        lines.append(f'  "{course_id}": () => import("{root}/{name}", {{ with: {{ type: "json" }} }}),')
    lines += ["};", ""]
    return "\n".join(lines)


def main() -> None:
    register = build_register()
    REGISTER_PATH.write_text(json.dumps(register, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    INDEX_PATH.write_text(json.dumps(build_frontend_index(register), ensure_ascii=False, separators=(",", ":")) + "\n", encoding="utf-8")
    LOADERS_PATH.write_text(build_loaders(), encoding="utf-8")
    for path in (REGISTER_PATH, INDEX_PATH, LOADERS_PATH):
        print(f"Wrote {path.relative_to(BASE)}")


if __name__ == "__main__":
    main()
