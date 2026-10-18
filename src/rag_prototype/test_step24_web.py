"""Focused offline checks for Step 24 web design and development evidence."""

from __future__ import annotations

import json
import unittest
from pathlib import Path

BASE = Path(__file__).resolve().parents[2]
BENCH = BASE / "outputs/programme_benchmarking"
WEB_IDS = ["LK-TVEC-NCS-WEB-DEVELOPER-2025", "IN-NQR-HARTRON-WEB-MULTIMEDIA-V2", "PH-TESDA-WEBDEV-NC3",
           "SG-ITE-HNITEC-ITAD-2Y", "AU-TGA-ICT40120-WEBDEV"]


class Step24WebTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.records = {r["record_id"]: r for r in json.loads((BENCH / "pilot_records_web.json").read_text(encoding="utf-8"))["records"]}
        cls.links = {l["nysc_course_id"]: l for l in json.loads((BENCH / "course_comparator_links.json").read_text(encoding="utf-8"))["links"]}
        cls.mapping = json.loads((BENCH / "competency_mapping_course-087.json").read_text(encoding="utf-8"))

    def test_five_new_web_records_pending_human_review(self):
        self.assertEqual(list(self.records), WEB_IDS)
        for record in self.records.values():
            with self.subTest(record=record["record_id"]):
                self.assertEqual(record["verification"]["status"], "source_inspected_pending_human_review")
                self.assertFalse(record["verification"]["human_reviewed"])
                self.assertRegex(record["source"]["document_sha256"], r"^[0-9a-f]{64}$")
        self.assertEqual(self.records["AU-TGA-ICT40120-WEBDEV"]["record_type"], "national_qualification")
        self.assertEqual(self.records["IN-NQR-HARTRON-WEB-MULTIMEDIA-V2"]["record_type"], "national_qualification")
        self.assertEqual(self.records["SG-ITE-HNITEC-ITAD-2Y"]["record_type"], "programme")

    def test_only_web_focused_records_are_linked(self):
        for course_id in ("COURSE-087", "COURSE-057", "COURSE-001"):
            ids = self.links[course_id]["record_ids"]
            self.assertEqual(ids, WEB_IDS)
            for general in ("IN-DGT-CTS-COPA-V3", "LK-TVEC-NCS-ICT-TECH-L4-2023", "SG-ITE-HNITEC-ISN-2Y"):
                self.assertNotIn(general, ids)
        for course_id in ("COURSE-057", "COURSE-001"):
            self.assertIn("COMPARATORS_ONLY", self.links[course_id]["comparison_caveat"])
            self.assertFalse((BENCH / f"competency_mapping_{course_id.lower()}.json").exists())

    def test_australian_record_is_core_plus_group_g(self):
        au = self.records["AU-TGA-ICT40120-WEBDEV"]
        self.assertEqual([m["group"] for m in au["modules"]], ["Core units"] * 7 + ["Group G Web Development Specialisation"] * 7)
        self.assertIn("Select all 7 elective units from Group G", au["scope_verbatim"][0])

    def test_course_087_cites_its_six_headings_with_corrections(self):
        evidence = [e for c in self.mapping["competencies"] for e in c["cells"]["NYSC-COURSE-087"]["evidence"]]
        self.assertEqual(sorted({e["module_index"] for e in evidence}), [0, 1, 2, 3, 4, 5])
        corrected = {e["module_index"]: e for e in evidence if "display_text" in e}
        self.assertEqual(corrected[2]["display_text"], "Java Script")
        self.assertEqual(corrected[5]["display_text"], "Host and Maintenance Website")
        self.assertIn("gentle attitudes", corrected[5]["text"])


if __name__ == "__main__":
    unittest.main()
