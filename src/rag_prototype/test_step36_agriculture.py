"""Focused offline regressions for Step 36 agriculture evidence (landscape, field assistant, plant nursery)."""

from __future__ import annotations

import json
import unittest
from pathlib import Path

BASE = Path(__file__).resolve().parents[2]
BENCH = BASE / "outputs/programme_benchmarking"
LINKS = {
    "COURSE-020": ["LK-TVEC-NCS-FLORICULTURE-LANDSCAPE-2022", "IN-DGT-CTS-FLORICULTURE-LANDSCAPING-V2", "PH-TESDA-LANDSCAPE-NC2", "AU-TGA-AHC30921"],
    "COURSE-026": ["LK-TVEC-NCS-FIELD-ASSISTANT-AGRICULTURE-2021", "IN-DGT-CTS-HORTICULTURE-V2", "PH-TESDA-AGRI-CROPS-NC3"],
    "COURSE-032": ["LK-TVEC-NCS-PLANT-NURSERY-2022", "IN-DGT-CTS-NURSERY-ORCHARD-V1", "PH-TESDA-HORTICULTURE-NC3", "AU-TGA-AHC31124"],
}
DATASETS = {"landscape": "COURSE-020", "field_agriculture": "COURSE-026", "plant_nursery": "COURSE-032"}


class Step36Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.datasets = {k: json.loads((BENCH / f"pilot_records_{k}.json").read_text(encoding="utf-8")) for k in DATASETS}
        cls.links = {l["nysc_course_id"]: l for l in json.loads((BENCH / "course_comparator_links.json").read_text(encoding="utf-8"))["links"]}
        cls.register = {e["course_id"]: e for e in json.loads((BENCH / "coverage_register.json").read_text(encoding="utf-8"))["courses"]}

    def test_records_pending_review_and_linked_comparators_only(self):
        for key, course in DATASETS.items():
            self.assertEqual([r["record_id"] for r in self.datasets[key]["records"]], LINKS[course])
            self.assertEqual(self.links[course]["record_ids"], LINKS[course])
            self.assertIn("COMPARATORS_ONLY", self.links[course]["comparison_caveat"])
            self.assertEqual(self.register[course]["current_presentation_mode"], "COMPARATORS_ONLY")
            self.assertFalse((BENCH / f"competency_mapping_{course.lower()}.json").exists())
            for record in self.datasets[key]["records"]:
                with self.subTest(record=record["record_id"]):
                    self.assertEqual(record["verification"]["status"], "source_inspected_pending_human_review")
                    self.assertFalse(record["verification"]["human_reviewed"])
                    self.assertFalse(record["delivering_provider_verified"])
                    self.assertRegex(record["source"]["document_sha256"], r"^[0-9a-f]{64}$")

    def test_parsed_curricula_are_complete(self):
        records = {r["record_id"]: r for d in self.datasets.values() for r in d["records"]}
        self.assertEqual(len(records["IN-DGT-CTS-FLORICULTURE-LANDSCAPING-V2"]["modules"]), 11)
        self.assertEqual(len(records["IN-DGT-CTS-NURSERY-ORCHARD-V1"]["modules"]), 16)
        self.assertEqual(len(records["IN-DGT-CTS-HORTICULTURE-V2"]["modules"]), 27)
        # Running page headers never leak into outcome text.
        for rid in ("IN-DGT-CTS-NURSERY-ORCHARD-V1", "IN-DGT-CTS-HORTICULTURE-V2"):
            for m in records[rid]["modules"]:
                self.assertNotIn("Nursery & Orchard Technician", m["title_verbatim"], rid)
        landscape = records["PH-TESDA-LANDSCAPE-NC2"]["modules"]
        self.assertEqual(len([m for m in landscape if m["group"] == "Core Competencies"]), 14)
        self.assertTrue(any("Installation / Construction" in n and "Maintenance" in n for n in records["PH-TESDA-LANDSCAPE-NC2"]["notes"]))
        for rid in ("PH-TESDA-AGRI-CROPS-NC3", "PH-TESDA-HORTICULTURE-NC3"):
            self.assertNotIn("Elective Competencies", {m["group"] for m in records[rid]["modules"]})

    def test_gaps_and_exclusions_are_explained(self):
        self.assertIn("AHC30122", self.datasets["field_agriculture"]["country_group_gaps"]["developed"])
        lk = {r["record_id"]: r for r in self.datasets["landscape"]["records"]}["LK-TVEC-NCS-FLORICULTURE-LANDSCAPE-2022"]
        self.assertTrue(any("O92S001" in n for n in lk["notes"]))


if __name__ == "__main__":
    unittest.main()
