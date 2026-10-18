"""Focused offline regressions for Step 31 automotive and metal-trades evidence."""

from __future__ import annotations

import json
import re
import unittest
from pathlib import Path


BASE = Path(__file__).resolve().parents[2]
BENCH = BASE / "outputs/programme_benchmarking"
COURSES = ("COURSE-017", "COURSE-018", "COURSE-038", "COURSE-044", "COURSE-045")


class Step31AutomotiveMetalTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.records = {
            record["record_id"]: record
            for path in BENCH.glob("pilot_records_*.json")
            for record in json.loads(path.read_text(encoding="utf-8"))["records"]
        }
        cls.links = {
            item["nysc_course_id"]: item
            for item in json.loads((BENCH / "course_comparator_links.json").read_text(encoding="utf-8"))["links"]
        }
        cls.register = {
            item["course_id"]: item
            for item in json.loads((BENCH / "coverage_register.json").read_text(encoding="utf-8"))["courses"]
        }

    def test_exact_links_and_specialist_scope(self):
        expected = {
            "COURSE-038": ["IN-DGT-CTS-2W3W-V2"],
            "COURSE-017": ["IN-DGT-CTS-AGMACH-V2", "PH-TESDA-AGMACH-4WT-NC3", "AU-TGA-AUR30420"],
            "COURSE-045": ["LK-TVEC-NCS-WELDER-R3", "IN-DGT-CTS-WELDER-V2", "AU-TGA-MEM31925-WELDING"],
            "COURSE-044": ["LK-TVEC-NCS-MACHINIST-R2", "PH-TESDA-MACHINING-NC2", "AU-TGA-MEM30219-MACHINING"],
            "COURSE-018": ["LK-TVEC-NCS-ALUMINIUM-FABRICATOR-2022"],
        }
        for course_id, record_ids in expected.items():
            self.assertEqual(self.links[course_id]["record_ids"], record_ids)
            self.assertIn("COMPARATORS_ONLY", self.links[course_id]["comparison_caveat"])

        self.assertIn("three", self.records["IN-DGT-CTS-2W3W-V2"]["title_verbatim"].lower())
        self.assertNotIn("LK-TVEC-NCS-MOTORCYCLE-TECHNICIAN-2025", expected["COURSE-038"])
        self.assertIn("4-WHEEL TRACTOR", self.records["PH-TESDA-AGMACH-4WT-NC3"]["title_verbatim"])

    def test_new_records_are_source_inspected_and_pinned(self):
        new_ids = {
            "IN-DGT-CTS-AGMACH-V2", "PH-TESDA-AGMACH-4WT-NC3", "AU-TGA-AUR30420",
            "LK-TVEC-NCS-WELDER-R3", "IN-DGT-CTS-WELDER-V2", "AU-TGA-MEM31925-WELDING",
            "LK-TVEC-NCS-MACHINIST-R2", "PH-TESDA-MACHINING-NC2", "AU-TGA-MEM30219-MACHINING",
            "LK-TVEC-NCS-ALUMINIUM-FABRICATOR-2022",
        }
        for record_id in new_ids:
            with self.subTest(record=record_id):
                record = self.records[record_id]
                self.assertEqual(record["verification"]["status"], "source_inspected_pending_human_review")
                self.assertFalse(record["verification"]["human_reviewed"])
                self.assertFalse(record["delivering_provider_verified"])
                self.assertRegex(record["source"]["document_sha256"], re.compile(r"^[0-9a-f]{64}$"))
                self.assertGreater(len(record["modules"]), 0)

    def test_no_fabricated_nysc_matrices(self):
        for course_id in COURSES:
            with self.subTest(course=course_id):
                entry = self.register[course_id]
                self.assertEqual(entry["evidence_availability"], "NO_HEADINGS")
                self.assertEqual(entry["current_presentation_mode"], "COMPARATORS_ONLY")
                self.assertEqual(entry["competency_mapping_status"], "NONE")
                self.assertFalse((BENCH / f"competency_mapping_{course_id.lower()}.json").exists())

    def test_record_types_are_not_presented_as_delivered_programmes(self):
        for course_id in COURSES:
            for record_id in self.links[course_id]["record_ids"]:
                with self.subTest(course=course_id, record=record_id):
                    self.assertIn(self.records[record_id]["record_type"], {
                        "national_curriculum", "occupational_standard", "national_qualification",
                    })
                    self.assertFalse(self.records[record_id]["delivering_provider_verified"])

    def test_updated_totals(self):
        register = json.loads((BENCH / "coverage_register.json").read_text(encoding="utf-8"))
        self.assertEqual(register["totals"]["current_presentation_mode"], {
            "COMPARATORS_ONLY": 47, "FULL_COMPARISON": 28, "RESEARCH_PENDING": 9,
        })
        self.assertEqual(register["totals"]["courses_with_mapping"], 28)
        self.assertEqual(len(self.records), 132)


if __name__ == "__main__":
    unittest.main()
