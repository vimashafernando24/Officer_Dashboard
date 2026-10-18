"""Focused offline checks for Step 30 electrical/electronics evidence."""

from __future__ import annotations

import json
import unittest
from pathlib import Path

BASE = Path(__file__).resolve().parents[2]
BENCH = BASE / "outputs/programme_benchmarking"


class Step30ElectricalElectronicsTests(unittest.TestCase):
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
        cls.mapping = json.loads((BENCH / "competency_mapping_course-081.json").read_text(encoding="utf-8"))

    def test_five_new_records_are_source_inspected_and_pinned(self):
        expected = {
            "LK-TVEC-NCS-ELECTRONIC-APPLIANCES-2017",
            "IN-DGT-CTS-MCEA-V2",
            "PH-TESDA-EPAS-NC2",
            "LK-TVEC-NCS-ELECTRIC-MOTOR-WINDER",
            "AU-TGA-UEE30625",
        }
        for record_id in expected:
            with self.subTest(record=record_id):
                record = self.records[record_id]
                self.assertEqual(record["verification"]["status"], "source_inspected_pending_human_review")
                self.assertFalse(record["verification"]["human_reviewed"])
                self.assertRegex(record["source"]["document_sha256"], r"^[0-9a-f]{64}$")
                self.assertFalse(record["delivering_provider_verified"])

    def test_course_links_use_only_substantive_records(self):
        self.assertEqual(self.links["COURSE-013"]["record_ids"], [
            "LK-TVEC-NCS-ELECTRONIC-APPLIANCES-2017", "IN-DGT-CTS-MCEA-V2", "PH-TESDA-EPAS-NC2",
        ])
        self.assertEqual(self.links["COURSE-081"]["record_ids"], self.links["COURSE-013"]["record_ids"])
        self.assertEqual(self.links["COURSE-079"]["record_ids"], [
            "LK-CGTTI-POWER-ELEC", "IN-DGT-CTS-ELEC-V3", "PH-TESDA-EIM-NC3", "AU-TAFENSW-UEE30820",
        ])
        self.assertEqual(self.links["COURSE-080"]["record_ids"], [
            "LK-TVEC-NCS-ELECTRIC-MOTOR-WINDER", "LK-CGTTI-POWER-ELEC", "IN-DGT-CTS-ELEC-V3", "AU-TGA-UEE30625",
        ])
        self.assertNotIn("PH-TESDA-EIM-NC2", self.links["COURSE-079"]["record_ids"])
        self.assertNotIn("PH-TESDA-EIM-NC2", self.links["COURSE-080"]["record_ids"])

    def test_presentation_modes_and_no_fabricated_matrices(self):
        self.assertEqual(self.register["COURSE-081"]["current_presentation_mode"], "FULL_COMPARISON")
        for course_id in ("COURSE-013", "COURSE-079", "COURSE-080"):
            with self.subTest(course=course_id):
                self.assertEqual(self.register[course_id]["current_presentation_mode"], "COMPARATORS_ONLY")
                self.assertEqual(self.register[course_id]["competency_mapping_status"], "NONE")
                self.assertFalse((BENCH / f"competency_mapping_{course_id.lower()}.json").exists())

    def test_course_081_uses_exact_three_governed_headings(self):
        cited = {
            evidence["module_index"]
            for competency in self.mapping["competencies"]
            for evidence in competency["cells"]["NYSC-COURSE-081"]["evidence"]
        }
        self.assertEqual(cited, {0, 1, 2})
        basic = next(c for c in self.mapping["competencies"] if c["competency_id"] == "rtv_basic_electronics")
        self.assertEqual(basic["cells"]["NYSC-COURSE-081"]["evidence"][0]["display_text"], "Basic Electricity and Electronics")
        programming = next(c for c in self.mapping["competencies"] if c["competency_id"] == "rtv_microcontroller_led_programming")
        self.assertNotIn("display_text", programming["cells"]["NYSC-COURSE-081"]["evidence"][0])

    def test_deterministic_areas_to_investigate(self):
        nysc = "NYSC-COURSE-081"
        areas = []
        for competency in self.mapping["competencies"]:
            if competency["cells"][nysc]["status"] != "NOT_EXPLICIT":
                continue
            full = [
                column["record_id"] for column in self.mapping["columns"]
                if column["kind"] == "benchmark" and competency["cells"][column["column_id"]].get("coverage") == "FULL"
            ]
            if len(full) >= 2 and len({self.records[record_id]["country"] for record_id in full}) >= 2:
                areas.append(competency["competency_id"])
        self.assertEqual(areas, [
            "rtv_fault_diagnosis", "rtv_audio_amplifier_repair", "rtv_power_supply_repair",
        ])

    def test_updated_totals(self):
        totals = json.loads((BENCH / "coverage_register.json").read_text(encoding="utf-8"))["totals"]
        self.assertEqual(totals["current_presentation_mode"], {
            "COMPARATORS_ONLY": 22, "FULL_COMPARISON": 23, "RESEARCH_PENDING": 39,
        })
        self.assertEqual(totals["courses_with_mapping"], 23)
        self.assertEqual(len(self.records), 74)


if __name__ == "__main__":
    unittest.main()
