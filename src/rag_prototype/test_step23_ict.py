"""Focused offline checks for Step 23 ICT Technician and Computer Applications evidence."""

from __future__ import annotations

import json
import unittest
from pathlib import Path

BASE = Path(__file__).resolve().parents[2]
BENCH = BASE / "outputs/programme_benchmarking"
LK_SHA = "72f4a4d090506291"


class Step23IctTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.dataset = json.loads((BENCH / "pilot_records_ict.json").read_text(encoding="utf-8"))
        cls.records = {r["record_id"]: r for r in cls.dataset["records"]}
        cls.links = {l["nysc_course_id"]: l for l in json.loads((BENCH / "course_comparator_links.json").read_text(encoding="utf-8"))["links"]}
        cls.m009 = json.loads((BENCH / "competency_mapping_course-009.json").read_text(encoding="utf-8"))
        cls.m053 = json.loads((BENCH / "competency_mapping_course-053.json").read_text(encoding="utf-8"))

    def test_four_new_records_pending_human_review(self):
        self.assertEqual(sorted(self.records), ["AU-TGA-ICT20120", "IN-DGT-CTS-COPA-V3", "LK-TVEC-NCS-COMPUTER-APP-ASSIST-L3-2023", "LK-TVEC-NCS-ICT-TECH-L4-2023"])
        for record in self.records.values():
            with self.subTest(record=record["record_id"]):
                self.assertEqual(record["verification"]["status"], "source_inspected_pending_human_review")
                self.assertFalse(record["verification"]["human_reviewed"])
                self.assertRegex(record["source"]["document_sha256"], r"^[0-9a-f]{64}$")

    def test_sri_lankan_packages_match_the_published_packaging(self):
        l4, l3 = self.records["LK-TVEC-NCS-ICT-TECH-L4-2023"], self.records["LK-TVEC-NCS-COMPUTER-APP-ASSIST-L3-2023"]
        self.assertEqual(l4["source"], l3["source"])
        self.assertTrue(l4["source"]["document_sha256"].startswith(LK_SHA))
        self.assertTrue(l4["source"]["url"].endswith("K72S004_2_NCS.pdf"))
        self.assertEqual(len(l4["modules"]), 15)
        self.assertEqual([m["code"] for m in l3["modules"]],
                         [f"K72S004U0{i}" for i in range(1, 8)] + [f"K72S004BU0{i}" for i in range(1, 5)])
        self.assertIn("K72S004Q2L3", l3["scope_verbatim"][0])
        self.assertIn("K72S004Q3L4", l4["scope_verbatim"][0])

    def test_links_reuse_records_only_where_supported(self):
        self.assertEqual(self.links["COURSE-009"]["record_ids"], ["LK-TVEC-NCS-ICT-TECH-L4-2023", "IN-DGT-CTS-COPA-V3", "PH-TESDA-CSS-NC2", "SG-ITE-HNITEC-ISN-2Y", "AU-TGA-ICT20120"])
        for course_id in ("COURSE-053", "COURSE-054"):
            self.assertEqual(self.links[course_id]["record_ids"], ["LK-TVEC-NCS-COMPUTER-APP-ASSIST-L3-2023", "IN-DGT-CTS-COPA-V3", "AU-TGA-ICT20120"])
            self.assertNotIn("PH-TESDA-CSS-NC2", self.links[course_id]["record_ids"])
        self.assertIn("technical-support", self.links["COURSE-009"]["basis"])
        self.assertIn("COMPARATORS_ONLY", self.links["COURSE-054"]["comparison_caveat"])

    def test_course_054_has_no_matrix(self):
        self.assertFalse((BENCH / "competency_mapping_course-054.json").exists())

    def test_course_009_never_cites_its_merged_heading(self):
        cited = {e["module_index"] for c in self.m009["competencies"] for e in c["cells"]["NYSC-COURSE-009"]["evidence"]}
        self.assertEqual(cited, set(range(9)))
        statuses = {c["competency_id"]: c["cells"]["NYSC-COURSE-009"]["status"] for c in self.m009["competencies"]}
        self.assertEqual(statuses["ict_web_design"], "INSUFFICIENT_DATA")
        self.assertEqual(statuses["ict_software_development"], "INSUFFICIENT_DATA")

    def test_course_053_cites_its_own_headings_with_the_display_correction(self):
        evidence = [e for c in self.m053["competencies"] for e in c["cells"]["NYSC-COURSE-053"]["evidence"]]
        self.assertEqual({e["module_index"] for e in evidence}, {1, 2})
        corrected = [e for e in evidence if e["module_index"] == 2]
        self.assertTrue(all(e["display_text"] == "Using Internet & E-mail" and "weekends" in e["text"] for e in corrected))


if __name__ == "__main__":
    unittest.main()
