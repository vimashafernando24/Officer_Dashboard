"""Focused offline checks for Step 19C beauty, hairdressing and secretary evidence."""

from __future__ import annotations

import json
import unittest
from pathlib import Path

BASE = Path(__file__).resolve().parents[2]
BENCH = BASE / "outputs/programme_benchmarking"


class Step19CComparatorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.records = {
            record["record_id"]: record
            for name in ("beauty", "hairdressing", "secretary")
            for record in json.loads((BENCH / f"pilot_records_{name}.json").read_text(encoding="utf-8"))["records"]
        }
        cls.links = {
            item["nysc_course_id"]: item["record_ids"]
            for item in json.loads((BENCH / "course_comparator_links.json").read_text(encoding="utf-8"))["links"]
        }
        cls.mappings = {
            cid: json.loads((BENCH / f"competency_mapping_{cid.lower()}.json").read_text(encoding="utf-8"))
            for cid in ("COURSE-010", "COURSE-046", "COURSE-014", "COURSE-035", "COURSE-082")
        }

    def areas(self, course_id):
        mapping = self.mappings[course_id]
        result = []
        for competency in mapping["competencies"]:
            if competency["cells"][f"NYSC-{course_id}"]["status"] != "NOT_EXPLICIT":
                continue
            full = [
                c["record_id"] for c in mapping["columns"] if c["kind"] == "benchmark"
                and competency["cells"][c["column_id"]].get("coverage") == "FULL"
            ]
            if len(full) >= 2 and len({self.records[r]["country"] for r in full}) >= 2:
                result.append(competency["competency_id"])
        return result

    def test_record_types_do_not_overstate_delivery(self):
        self.assertEqual(self.records["LK-TVEC-NCS-BEAUTICIAN-2020"]["record_type"], "occupational_standard")
        self.assertEqual(self.records["IN-DGT-CTS-COSMETOLOGY-V2"]["record_type"], "national_curriculum")
        self.assertTrue(self.records["SG-ITE-HNITEC-BEAUTY-2Y"]["delivering_provider_verified"])
        self.assertEqual(self.records["AU-TGA-BSB30120"]["record_type"], "national_qualification")
        for record in self.records.values():
            if record["record_type"] != "programme":
                self.assertFalse(record["delivering_provider_verified"])

    def test_comparator_only_courses_have_links_but_no_mapping(self):
        for course_id, expected in (("COURSE-048", 4), ("COURSE-069", 3)):
            self.assertEqual(len(self.links[course_id]), expected)
            self.assertFalse((BENCH / f"competency_mapping_{course_id.lower()}.json").exists())

    def test_step19c_areas_follow_the_two_country_rule(self):
        self.assertEqual(self.areas("COURSE-010"), ["hair_removal", "client_consultation", "salon_hygiene_safety"])
        self.assertEqual(self.areas("COURSE-046"), ["hair_removal", "client_consultation", "salon_hygiene_safety"])
        self.assertEqual(self.areas("COURSE-014"), ["hair_salon_safety"])
        self.assertEqual(self.areas("COURSE-035"), ["diary_appointments"])
        self.assertEqual(self.areas("COURSE-082"), ["filing_records", "office_software", "diary_appointments"])

    def test_nysc_display_correction_is_kept_as_display_only(self):
        row = next(c for c in self.mappings["COURSE-082"]["competencies"] if c["competency_id"] == "mail_handling")
        evidence = row["cells"]["NYSC-COURSE-082"]["evidence"][0]
        self.assertIn("weekends", evidence["text"])
        self.assertNotIn("weekends", evidence["display_text"])

    def test_prior_covered_files_remain_byte_identical_to_generator_inputs(self):
        prior = {"COURSE-005", "COURSE-007", "COURSE-008", "COURSE-011", "COURSE-012", "COURSE-025", "COURSE-034", "COURSE-040", "COURSE-047", "COURSE-055", "COURSE-056", "COURSE-064"}
        self.assertTrue(prior <= set(self.links))
        self.assertEqual(len(prior), 12)


if __name__ == "__main__":
    unittest.main()
