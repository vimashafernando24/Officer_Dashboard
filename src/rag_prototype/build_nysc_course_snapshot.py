"""Write the read-only NYSC course snapshot used by the Programme Comparison Dashboard.

The dashboard's sector and course dropdowns and its course summary need the
governed 84-course catalogue, which no API serves. This script reads it through
the verified loader (manifest and document hashes are checked) and writes only
the fields the dashboard shows. It never modifies the catalogue.

Display-only module corrections: the NYSC pages were captured from screenshots
in which the module list sits beside the "Course Overview" paragraph, so text
extraction interleaved the two and some module headings absorbed a fragment of
the overview prose. A fragment is removed for display only when it is both
(1) a line standing alone in the governed course document and (2) an exact
word-ending of one of NYSC's standard overview sentences. The original heading
is kept alongside every correction. Remaining suspected contamination that
this rule cannot verify is flagged for review instead of being changed.

A heading the rule cannot repair may instead be corrected from the course's own
source screenshot (SCREENSHOT_VERIFIED_CORRECTIONS). Each entry is applied only
when the governed heading, the screenshot named in the governed document, the
screenshot's SHA-256 hash and the removed fragment all match; otherwise the
build fails. Wording from another course is never used as proof.

Run from the repository root:  python3 src/rag_prototype/build_nysc_course_snapshot.py
"""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

try:
    from .corpus_v2 import MANIFEST_CSV
    from .programme_design_evidence import COURSE_MATCHING_PATH, load_governed_courses
except ImportError:  # pragma: no cover - supports direct script execution
    from corpus_v2 import MANIFEST_CSV
    from programme_design_evidence import COURSE_MATCHING_PATH, load_governed_courses

BASE = Path(__file__).resolve().parents[2]
SNAPSHOT_PATH = BASE / "src/rag_prototype/frontend/src/data/nyscCourseCatalogue.json"


# NYSC's standard "Course Overview" sentences, as published on the course pages.
OVERVIEW_BOILERPLATE = (
    "job oriented practical skills that are necessary for employment and higher education.",
    "This is a part time course which will be held on weekends.",
    "This is a full time course which will be held on weekdays.",
    "the necessary knowledge, skills and gentle attitudes within a disciplined environment.",
)
CORRECTION_RULE = (
    "Removed a fragment that stands alone as a line in the governed course document and is an "
    "exact ending of a standard NYSC overview sentence."
)
SCREENSHOT_RULE = (
    "Replaced with the heading exactly as shown in the course's own source screenshot: the removed "
    "fragment is overview text (partly covered by a screenshot tooltip) from the adjacent column."
)
# Headings verified by eye against the course's own source screenshot.
SCREENSHOT_VERIFIED_CORRECTIONS = {
    "COURSE-012": (
        {
            "module_index": 3,
            "original": "Operate and Maintain Central A/C system gentle attitudes within a dis Screenshot unment.",
            "displayed": "Operate and Maintain Central A/C System",
            "removed_fragments": ["gentle attitudes within a dis Screenshot unment."],
            "source_screenshot": "CoursesSS/Screenshot 2026-04-12 at 22.26.56.png",
            "source_screenshot_sha256": "9c30b41d9c0ab1396b460d21a9558c3ef02a90bdb3d0ec682d4f5588386a635b",
        },
    ),
}
# Signs of contamination that the correction rule cannot verify.
REVIEW_PATTERNS = (
    (re.compile(r"Screenshot"), "Contains a screenshot-capture artefact."),
    (re.compile(r"gentle attitudes|disciplined|held on week|necessary for employment"),
     "Contains part of a standard overview sentence that does not match exactly."),
    (re.compile(r"\s\d+[l.]\.?\s"), "Appears to contain a second numbered module heading."),
)


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _overview_fragment_lines(document_text: str) -> list[str]:
    """Standalone document lines that are word-endings of a standard overview sentence."""
    endings = set()
    for sentence in OVERVIEW_BOILERPLATE:
        words = sentence.split()
        endings.update(" ".join(words[index:]) for index in range(len(words)))
    body = document_text.split("COMPLETE EXTRACTED COURSE TEXT", 1)[-1]
    lines = {line.strip() for line in body.splitlines()}
    return sorted((line for line in lines if line in endings), key=len, reverse=True)


def _screenshot_corrections(course_id: str, modules: list[str], document_text: str) -> dict[int, dict]:
    """Curated screenshot-verified corrections for a course, checked against their evidence."""
    corrections = {}
    lines = {line.strip() for line in document_text.splitlines()}
    for entry in SCREENSHOT_VERIFIED_CORRECTIONS.get(course_id, ()):
        index, screenshot = entry["module_index"], entry["source_screenshot"]
        if modules[index] != entry["original"]:
            raise ValueError(f"{course_id} heading {index + 1} no longer matches the corrected original")
        if f"SOURCE SCREENSHOT FILENAME(S): {Path(screenshot).name}" not in document_text:
            raise ValueError(f"{course_id}: {screenshot} is not the governed document's source screenshot")
        if _sha256(BASE / screenshot) != entry["source_screenshot_sha256"]:
            raise ValueError(f"{course_id}: source screenshot hash does not match")
        rebuilt = entry["original"]
        for fragment in entry["removed_fragments"]:
            if fragment not in lines:
                raise ValueError(f"{course_id}: removed fragment is not a standalone document line")
            rebuilt = rebuilt.replace(fragment, " ", 1)
        if " ".join(rebuilt.split()).casefold() != entry["displayed"].casefold():
            raise ValueError(f"{course_id}: correction changes more than the fragment and letter case")
        corrections[index] = {
            "module_index": index,
            "original": entry["original"],
            "displayed": entry["displayed"],
            "removed_fragments": list(entry["removed_fragments"]),
            "rule": SCREENSHOT_RULE,
            "source_screenshot": screenshot,
            "source_screenshot_sha256": entry["source_screenshot_sha256"],
        }
    return corrections


def module_display(modules: list[str], document_text: str, course_id: str = "") -> tuple[list[dict], list[dict]]:
    """Display-only corrections and review flags for a course's extracted module headings."""
    fragments = _overview_fragment_lines(document_text)
    verified = _screenshot_corrections(course_id, modules, document_text)
    corrections, review_flags = [], []
    for index, original in enumerate(modules):
        if index in verified:
            corrections.append(verified[index])
            continue
        displayed, removed = original, []
        for fragment in fragments:
            pattern = re.compile(r"(?<!\S)" + re.escape(fragment) + r"(?!\S)")
            if pattern.search(displayed):
                displayed = re.sub(r"\s+", " ", pattern.sub(" ", displayed, count=1)).strip()
                removed.append(fragment)
        if removed and displayed:
            corrections.append({
                "module_index": index,
                "original": original,
                "displayed": displayed,
                "removed_fragments": removed,
                "rule": CORRECTION_RULE,
            })
        for pattern, reason in REVIEW_PATTERNS:
            if pattern.search(displayed):
                review_flags.append({"module_index": index, "text": displayed, "reason": reason})
                break
    return corrections, review_flags


def _course_entry(course: dict) -> dict:
    document_text = (BASE / course["document_path"]).read_text(encoding="utf-8")
    corrections, review_flags = module_display(course["modules"], document_text, course["course_id"])
    return {
        "course_id": course["course_id"],
        "course_name": course["course_name"],
        "skill_area": course["skill_area"],
        "attendance_type": course["attendance_type"],
        "nvq_level": course["nvq_level"],
        "qualification_type": course["qualification_type"],
        "duration_months": course["duration_months"],
        "modules": course["modules"],
        "module_display_corrections": corrections,
        "module_review_flags": review_flags,
    }


def build_snapshot() -> dict:
    courses = sorted(
        (_course_entry(course) for course in load_governed_courses()),
        key=lambda course: course["course_id"],
    )
    return {
        "description": "Read-only snapshot of the governed NYSC course catalogue for the dashboard's course selectors and summary. 'modules' is the governed text unchanged; 'module_display_corrections' are display-only repairs of extraction contamination (see the generator's docstring), and 'module_review_flags' mark headings that still need manual review. Regenerate with src/rag_prototype/build_nysc_course_snapshot.py; do not edit by hand.",
        "source": {
            "manifest": str(MANIFEST_CSV.relative_to(BASE)),
            "manifest_sha256": _sha256(MANIFEST_CSV),
            "course_matching_layer": str(COURSE_MATCHING_PATH.relative_to(BASE)),
            "course_matching_layer_sha256": _sha256(COURSE_MATCHING_PATH),
        },
        "governed_course_count": len(courses),
        "courses": courses,
    }


def main() -> None:
    SNAPSHOT_PATH.write_text(
        json.dumps(build_snapshot(), ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(f"Wrote {SNAPSHOT_PATH.relative_to(BASE)}")


if __name__ == "__main__":
    main()
