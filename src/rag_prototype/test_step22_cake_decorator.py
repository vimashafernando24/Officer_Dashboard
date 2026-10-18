"""Focused offline checks for Step 22 Cake Decorator evidence."""

from __future__ import annotations

import json
import unittest
from pathlib import Path

BASE = Path(__file__).resolve().parents[2]
BENCH = BASE / "outputs/programme_benchmarking"


class Step22CakeDecoratorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.dataset = json.loads((BENCH / "pilot_records_cake_decorator.json").read_text(encoding="utf-8"))
        cls.record = cls.dataset["records"][0]
        cls.mapping = json.loads((BENCH / "competency_mapping_course-050.json").read_text(encoding="utf-8"))
        cls.links = {
            item["nysc_course_id"]: item
            for item in json.loads((BENCH / "course_comparator_links.json").read_text(encoding="utf-8"))["links"]
        }

    def test_sri_lankan_standard_is_exact_occupation_and_not_delivery(self):
        self.assertEqual(self.record["record_id"], "LK-TVEC-NCS-CAKE-DECORATOR-2022")
        self.assertEqual(self.record["record_type"], "occupational_standard")
        self.assertFalse(self.record["delivering_provider_verified"])
        self.assertEqual(self.record["verification"]["status"], "source_inspected_pending_human_review")
        self.assertFalse(self.record["verification"]["human_reviewed"])
        self.assertEqual(len(self.record["modules"]), 12)
        self.assertEqual(self.record["modules"][0]["code"], "D15S010U01")
        self.assertEqual(self.record["modules"][-1]["code"], "D15S010BU04")
        self.assertEqual(self.record["source"]["document_sha256"], "086cec2e1cb921b3b1166e21cd2731250b44627fc9d71e2d972d0d1ed52463d8")

    def test_only_substantial_existing_records_are_reused(self):
        expected = [
            "LK-TVEC-NCS-CAKE-DECORATOR-2022",
            "IN-DGT-CTS-BAKER-V2",
            "SG-ITE-HNITEC-PASTRY-2Y",
        ]
        for course_id in ("COURSE-050", "COURSE-051"):
            self.assertEqual(self.links[course_id]["record_ids"], expected)
            self.assertNotIn("AU-TGA-FBP30521", self.links[course_id]["record_ids"])

    def test_course_051_is_comparator_only(self):
        self.assertFalse((BENCH / "competency_mapping_course-051.json").exists())
        self.assertIn("COMPARATORS_ONLY", self.links["COURSE-051"]["comparison_caveat"])

    def test_course_050_uses_only_its_four_governed_headings(self):
        nysc_evidence = [
            evidence
            for competency in self.mapping["competencies"]
            for evidence in competency["cells"]["NYSC-COURSE-050"]["evidence"]
        ]
        self.assertEqual({e["module_index"] for e in nysc_evidence}, {0, 1, 2, 3})
        corrected = [e for e in nysc_evidence if e["module_index"] == 3]
        self.assertTrue(corrected)
        self.assertTrue(all("gentle attitudes" in e["text"] for e in corrected))
        self.assertTrue(all("gentle attitudes" not in e["display_text"] for e in corrected))

    def test_areas_to_investigate_follow_existing_rule(self):
        records = {
            record["record_id"]: record
            for path in BENCH.glob("pilot_records_*.json")
            for record in json.loads(path.read_text(encoding="utf-8"))["records"]
        }
        areas = []
        for competency in self.mapping["competencies"]:
            if competency["cells"]["NYSC-COURSE-050"]["status"] != "NOT_EXPLICIT":
                continue
            full = [
                column["record_id"]
                for column in self.mapping["columns"]
                if column["kind"] == "benchmark"
                and competency["cells"][column["column_id"]].get("coverage") == "FULL"
            ]
            if len(full) >= 2 and len({records[record_id]["country"] for record_id in full}) >= 2:
                areas.append(competency["competency_id"])
        self.assertEqual(areas, ["cake_food_safety_hygiene"])


if __name__ == "__main__":
    unittest.main()
