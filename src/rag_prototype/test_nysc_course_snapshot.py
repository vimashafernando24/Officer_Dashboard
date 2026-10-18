"""The dashboard's course snapshot must match the governed catalogue exactly."""

from __future__ import annotations

import json
import unittest

from src.rag_prototype.build_nysc_course_snapshot import (
    BASE,
    OVERVIEW_BOILERPLATE,
    SCREENSHOT_VERIFIED_CORRECTIONS,
    SNAPSHOT_PATH,
    _sha256,
    build_snapshot,
)
from src.rag_prototype.programme_design_evidence import load_governed_courses


class NyscCourseSnapshotTests(unittest.TestCase):
    def test_snapshot_matches_governed_catalogue(self):
        committed = json.loads(SNAPSHOT_PATH.read_text(encoding="utf-8"))
        self.assertEqual(
            committed,
            build_snapshot(),
            "Snapshot is out of date: run python3 src/rag_prototype/build_nysc_course_snapshot.py",
        )

    def test_snapshot_covers_all_84_governed_courses(self):
        snapshot = build_snapshot()
        self.assertEqual(snapshot["governed_course_count"], 84)
        self.assertEqual(len({course["course_id"] for course in snapshot["courses"]}), 84)

    def test_governed_module_text_is_kept_unchanged(self):
        governed = {course["course_id"]: course["modules"] for course in load_governed_courses()}
        for course in build_snapshot()["courses"]:
            with self.subTest(course=course["course_id"]):
                self.assertEqual(course["modules"], governed[course["course_id"]])

    def test_each_display_correction_is_supported_by_the_governed_document(self):
        documents = {
            course["course_id"]: (BASE / course["document_path"]).read_text(encoding="utf-8")
            for course in load_governed_courses()
        }
        endings = {
            " ".join(sentence.split()[index:])
            for sentence in OVERVIEW_BOILERPLATE
            for index in range(len(sentence.split()))
        }
        for course in build_snapshot()["courses"]:
            lines = {line.strip() for line in documents[course["course_id"]].splitlines()}
            for correction in course["module_display_corrections"]:
                if "source_screenshot" in correction:
                    continue  # checked in test_screenshot_verified_corrections
                with self.subTest(course=course["course_id"], module=correction["module_index"]):
                    self.assertEqual(correction["original"], course["modules"][correction["module_index"]])
                    rebuilt = correction["original"]
                    for fragment in correction["removed_fragments"]:
                        self.assertIn(fragment, endings)  # an exact overview-sentence ending
                        self.assertIn(fragment, lines)  # a standalone line in the source
                        rebuilt = rebuilt.replace(fragment, " ", 1)
                    self.assertEqual(" ".join(rebuilt.split()), correction["displayed"])
                    self.assertTrue(correction["displayed"])

    def test_known_contamination_is_corrected_or_flagged(self):
        courses = {course["course_id"]: course for course in build_snapshot()["courses"]}
        electrician = {c["module_index"]: c["displayed"] for c in courses["COURSE-025"]["module_display_corrections"]}
        self.assertEqual(electrician[1], "Industrial Electrical Installation (Motor Controlling System)")
        self.assertEqual(electrician[4], "Domestic Electrical Installation")
        # Garbled or merged text the rule cannot verify stays unchanged and flagged.
        self.assertEqual([f["module_index"] for f in courses["COURSE-009"]["module_review_flags"]], [9])
        self.assertFalse(courses["COURSE-005"]["module_display_corrections"])

    def test_screenshot_verified_corrections(self):
        courses = {course["course_id"]: course for course in build_snapshot()["courses"]}
        documents = {
            course["course_id"]: (BASE / course["document_path"]).read_text(encoding="utf-8")
            for course in load_governed_courses()
        }
        self.assertEqual(list(SCREENSHOT_VERIFIED_CORRECTIONS), ["COURSE-012"])
        for course_id, entries in SCREENSHOT_VERIFIED_CORRECTIONS.items():
            corrections = {c["module_index"]: c for c in courses[course_id]["module_display_corrections"]}
            for entry in entries:
                with self.subTest(course=course_id, module=entry["module_index"]):
                    correction = corrections[entry["module_index"]]
                    self.assertEqual(correction["original"], courses[course_id]["modules"][entry["module_index"]])
                    self.assertEqual(_sha256(BASE / correction["source_screenshot"]), correction["source_screenshot_sha256"])
                    name = correction["source_screenshot"].rsplit("/", 1)[-1]
                    self.assertIn(f"SOURCE SCREENSHOT FILENAME(S): {name}", documents[course_id])
                    # Only the overview fragment is removed; the rest differs at most in letter case.
                    rebuilt = correction["original"].replace(correction["removed_fragments"][0], " ", 1)
                    self.assertEqual(" ".join(rebuilt.split()).casefold(), correction["displayed"].casefold())

    def test_course_012_heading_4_is_corrected_from_its_own_screenshot(self):
        course = {c["course_id"]: c for c in build_snapshot()["courses"]}["COURSE-012"]
        corrections = {c["module_index"]: c for c in course["module_display_corrections"]}
        self.assertEqual(corrections[3]["displayed"], "Operate and Maintain Central A/C System")
        self.assertEqual(corrections[3]["source_screenshot"], "CoursesSS/Screenshot 2026-04-12 at 22.26.56.png")
        # The governed text and the existing heading 2 correction are preserved.
        self.assertEqual(course["modules"][3], "Operate and Maintain Central A/C system gentle attitudes within a dis Screenshot unment.")
        self.assertEqual(corrections[1]["displayed"], "Prepare Estimates")
        self.assertNotIn("source_screenshot", corrections[1])
        self.assertEqual(course["module_review_flags"], [])

    def test_published_typos_are_not_treated_as_contamination(self):
        courses = {course["course_id"]: course for course in build_snapshot()["courses"]}
        displayed = [c["displayed"] for c in courses["COURSE-062"]["module_display_corrections"]]
        self.assertIn("Adode photoshop Cs6", displayed)


if __name__ == "__main__":
    unittest.main()
