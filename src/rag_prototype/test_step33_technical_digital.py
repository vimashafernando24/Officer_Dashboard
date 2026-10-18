"""Focused offline regressions for Step 33 technical and digital evidence."""

from __future__ import annotations

import json
import re
import unittest
from pathlib import Path


BASE = Path(__file__).resolve().parents[2]
BENCH = BASE / "outputs/programme_benchmarking"


class Step33TechnicalDigitalTests(unittest.TestCase):
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
        register = json.loads((BENCH / "coverage_register.json").read_text(encoding="utf-8"))
        cls.totals = register["totals"]
        cls.coverage = {item["course_id"]: item for item in register["courses"]}
        cls.mapping = json.loads((BENCH / "competency_mapping_course-062.json").read_text(encoding="utf-8"))

    def test_exact_course_links(self):
        expected = {
            "COURSE-002": ["IN-DGT-CTS-COPA-V3", "IN-DGT-CTS-AIPA-V1"],
            "COURSE-043": ["IN-DGT-ATS-CADCAM-OPERATOR-PROGRAMMER", "PH-TESDA-TECHNICAL-DRAFTING-NC2"],
            "COURSE-062": ["LK-TVEC-NCS-GRAPHIC-DESIGNER-2025", "PH-TESDA-VGD-NC3", "SG-ITE-HNITEC-COMMDESIGN-2Y", "IN-DGT-CTS-DTPO-V2"],
            "COURSE-073": ["PH-TESDA-PROGRAMMING-JAVA-NC3-2021"],
            "COURSE-076": ["IN-DGT-ATS-MECHANIC-EMBEDDED-PLC"],
        }
        for course_id, record_ids in expected.items():
            self.assertEqual(self.links[course_id]["record_ids"], record_ids)

    def test_new_records_are_pinned_official_curricula(self):
        new_ids = {
            "IN-DGT-CTS-AIPA-V1", "IN-DGT-ATS-CADCAM-OPERATOR-PROGRAMMER",
            "IN-DGT-CTS-DTPO-V2", "PH-TESDA-PROGRAMMING-JAVA-NC3-2021",
            "IN-DGT-ATS-MECHANIC-EMBEDDED-PLC",
        }
        for record_id in new_ids:
            with self.subTest(record=record_id):
                record = self.records[record_id]
                self.assertEqual(record["verification"]["status"], "source_inspected_pending_human_review")
                self.assertFalse(record["verification"]["human_reviewed"])
                self.assertFalse(record["delivering_provider_verified"])
                self.assertRegex(record["source"]["document_sha256"], re.compile(r"^[0-9a-f]{64}$"))
                self.assertGreater(len(record["modules"]), 0)

    def test_only_desktop_publisher_has_a_defensible_matrix(self):
        self.assertEqual(self.coverage["COURSE-062"]["current_presentation_mode"], "FULL_COMPARISON")
        for course_id in ("COURSE-002", "COURSE-043", "COURSE-073", "COURSE-076"):
            with self.subTest(course=course_id):
                self.assertEqual(self.coverage[course_id]["current_presentation_mode"], "COMPARATORS_ONLY")
                self.assertEqual(self.coverage[course_id]["evidence_availability"], "NO_HEADINGS")
                self.assertEqual(self.coverage[course_id]["competency_mapping_status"], "NONE")
                self.assertFalse((BENCH / f"competency_mapping_{course_id.lower()}.json").exists())

    def test_desktop_publisher_mapping_preserves_exact_headings(self):
        expected = [
            "Adobe pagemaker 7.0",
            "Adode photoshop Cs6 which will be held on weekends.",
            "Adobe Indesign Cs6",
            "Adobe Illustrator Cs6",
        ]
        self.assertEqual(
            [row["cells"]["NYSC-COURSE-062"]["evidence"][0]["text"] for row in self.mapping["competencies"]],
            expected,
        )
        for row in self.mapping["competencies"]:
            self.assertEqual(row["cells"]["IN-DGT-CTS-DTPO-V2"]["coverage"], "FULL")
            for record_id in ("LK-TVEC-NCS-GRAPHIC-DESIGNER-2025", "PH-TESDA-VGD-NC3", "SG-ITE-HNITEC-COMMDESIGN-2Y"):
                self.assertEqual(row["cells"][record_id]["status"], "NOT_EXPLICIT")

    def test_updated_totals(self):
        self.assertEqual(self.totals["current_presentation_mode"], {
            "COMPARATORS_ONLY": 37, "FULL_COMPARISON": 24, "RESEARCH_PENDING": 23,
        })
        self.assertEqual(self.totals["courses_with_mapping"], 24)
        self.assertEqual(self.totals["courses_with_comparators"], 61)
        self.assertEqual(self.totals["occupation_groups_complete"], 42)
        self.assertEqual(len(self.records), 100)


if __name__ == "__main__":
    unittest.main()
