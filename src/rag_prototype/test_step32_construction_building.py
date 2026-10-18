"""Focused offline regressions for Step 32 construction and building-trades evidence."""

from __future__ import annotations

import json
import re
import unittest
from pathlib import Path


BASE = Path(__file__).resolve().parents[2]
BENCH = BASE / "outputs/programme_benchmarking"
COURSES = ("COURSE-019", "COURSE-024", "COURSE-033", "COURSE-036", "COURSE-061", "COURSE-065")


class Step32ConstructionBuildingTests(unittest.TestCase):
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

    def test_exact_links_preserve_specialist_scope(self):
        draught = [
            "LK-TVEC-NCS-DRAUGHTSPERSON-2023",
            "IN-DGT-CTS-DRAUGHTSMAN-CIVIL-V2",
            "PH-TESDA-TECHNICAL-DRAFTING-NC2",
        ]
        expected = {
            "COURSE-019": ["LK-TVEC-NCS-QUANTITY-SURVEYING-ASSISTANT-2024"],
            "COURSE-024": draught,
            "COURSE-061": draught,
            "COURSE-065": draught,
            "COURSE-033": [
                "LK-TVEC-NCS-PLUMBER-R5", "IN-DGT-CTS-PLUMBER-V3",
                "PH-TESDA-PLUMBING-NC2-2014", "AU-TGA-CPC32420-PLUMBING-R8",
            ],
            "COURSE-036": [
                "LK-TVEC-NCS-SURVEY-FIELD-ASSISTANT-2023",
                "IN-DGT-CTS-SURVEYOR-V2", "AU-TGA-CPP30226-SURVEYING-ASSISTANT",
            ],
        }
        for course_id, record_ids in expected.items():
            self.assertEqual(self.links[course_id]["record_ids"], record_ids)
            self.assertIn("COMPARATORS_ONLY", self.links[course_id]["comparison_caveat"])
        self.assertIn("do not prove coverage", self.links["COURSE-061"]["comparison_caveat"])

    def test_new_records_are_source_inspected_and_pinned(self):
        new_ids = {
            "LK-TVEC-NCS-QUANTITY-SURVEYING-ASSISTANT-2024",
            "LK-TVEC-NCS-DRAUGHTSPERSON-2023", "IN-DGT-CTS-DRAUGHTSMAN-CIVIL-V2",
            "PH-TESDA-TECHNICAL-DRAFTING-NC2", "LK-TVEC-NCS-PLUMBER-R5",
            "IN-DGT-CTS-PLUMBER-V3", "PH-TESDA-PLUMBING-NC2-2014",
            "AU-TGA-CPC32420-PLUMBING-R8", "LK-TVEC-NCS-SURVEY-FIELD-ASSISTANT-2023",
            "IN-DGT-CTS-SURVEYOR-V2", "AU-TGA-CPP30226-SURVEYING-ASSISTANT",
        }
        for record_id in new_ids:
            with self.subTest(record=record_id):
                record = self.records[record_id]
                self.assertEqual(record["verification"]["status"], "source_inspected_pending_human_review")
                self.assertFalse(record["verification"]["human_reviewed"])
                self.assertFalse(record["delivering_provider_verified"])
                self.assertRegex(record["source"]["document_sha256"], re.compile(r"^[0-9a-f]{64}$"))
                self.assertGreater(len(record["modules"]), 0)

    def test_no_fabricated_nysc_matrices_or_areas(self):
        for course_id in COURSES:
            with self.subTest(course=course_id):
                entry = self.register[course_id]
                self.assertEqual(entry["evidence_availability"], "NO_HEADINGS")
                self.assertEqual(entry["current_presentation_mode"], "COMPARATORS_ONLY")
                self.assertEqual(entry["competency_mapping_status"], "NONE")
                self.assertFalse((BENCH / f"competency_mapping_{course_id.lower()}.json").exists())

    def test_records_are_not_presented_as_delivered_programmes(self):
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
            "COMPARATORS_ONLY": 37, "FULL_COMPARISON": 24, "RESEARCH_PENDING": 23,
        })
        self.assertEqual(register["totals"]["courses_with_mapping"], 24)
        self.assertEqual(len(self.records), 100)


if __name__ == "__main__":
    unittest.main()
