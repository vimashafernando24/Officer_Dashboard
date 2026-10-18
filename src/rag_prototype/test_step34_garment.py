"""Focused offline regressions for Step 34 garment evidence."""

from __future__ import annotations

import json
import unittest
from pathlib import Path


BASE = Path(__file__).resolve().parents[2]
BENCH = BASE / "outputs/programme_benchmarking"
RECORD_IDS = [
    "LK-TVEC-NCS-TAILOR-R2-2017",
    "IN-DGT-CTS-SEWING-TECHNOLOGY-V2",
    "PH-TESDA-DRESSMAKING-NC2-2005",
]


class Step34GarmentTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        dataset = json.loads((BENCH / "pilot_records_garment.json").read_text(encoding="utf-8"))
        cls.records = {record["record_id"]: record for record in dataset["records"]}
        cls.links = {
            item["nysc_course_id"]: item
            for item in json.loads((BENCH / "course_comparator_links.json").read_text(encoding="utf-8"))["links"]
        }
        register = json.loads((BENCH / "coverage_register.json").read_text(encoding="utf-8"))
        cls.totals = register["totals"]
        cls.coverage = {item["course_id"]: item for item in register["courses"]}
        cls.mappings = {
            cid: json.loads((BENCH / f"competency_mapping_{cid.lower()}.json").read_text(encoding="utf-8"))
            for cid in ("COURSE-037", "COURSE-063")
        }

    def test_records_are_unique_pinned_official_sources(self):
        self.assertEqual(set(self.records), set(RECORD_IDS))
        expected_hashes = {
            "LK-TVEC-NCS-TAILOR-R2-2017": "dc0ef847b0d8134bb0786a417786c528e8f119f34a08177c2b7bbbc01e85eb66",
            "IN-DGT-CTS-SEWING-TECHNOLOGY-V2": "921fe728f2f38c4b3a36c05e8903e9db725a7268e0e844e5bacce5f5b6ab5eb8",
            "PH-TESDA-DRESSMAKING-NC2-2005": "021baaa89023391a14a4e8dd6d41cb4be8cc2159e16395f2ad6cf4cffe03ca9e",
        }
        for record_id, expected_hash in expected_hashes.items():
            with self.subTest(record=record_id):
                record = self.records[record_id]
                self.assertEqual(record["source"]["document_sha256"], expected_hash)
                self.assertEqual(record["verification"]["status"], "source_inspected_pending_human_review")
                self.assertFalse(record["verification"]["human_reviewed"])
                self.assertFalse(record["delivering_provider_verified"])

    def test_all_three_courses_share_one_deduplicated_record_set(self):
        for course_id in ("COURSE-037", "COURSE-063", "COURSE-085"):
            self.assertEqual(self.links[course_id]["record_ids"], RECORD_IDS, course_id)
        self.assertIn("block-free", self.links["COURSE-063"]["comparison_caveat"])
        self.assertIn("no published governed headings", self.links["COURSE-085"]["comparison_caveat"])

    def test_only_supported_courses_have_one_row_mappings(self):
        expected = {
            "COURSE-037": ("Women and children clothing", None),
            "COURSE-063": (
                "Women and children clothing which will be held on weekends.",
                "Women and children clothing",
            ),
        }
        for course_id, (raw, display) in expected.items():
            mapping = self.mappings[course_id]
            self.assertEqual(len(mapping["competencies"]), 1)
            row = mapping["competencies"][0]
            evidence = row["cells"][f"NYSC-{course_id}"]["evidence"][0]
            self.assertEqual(evidence["text"], raw)
            self.assertEqual(evidence.get("display_text"), display)
            self.assertEqual(row["cells"]["LK-TVEC-NCS-TAILOR-R2-2017"]["coverage"], "FULL")
            self.assertEqual(row["cells"]["IN-DGT-CTS-SEWING-TECHNOLOGY-V2"]["coverage"], "FULL")
            self.assertEqual(row["cells"]["PH-TESDA-DRESSMAKING-NC2-2005"]["coverage"], "PARTIAL")
        self.assertFalse((BENCH / "competency_mapping_course-085.json").exists())

    def test_block_free_method_is_not_claimed_by_evidence(self):
        mapping = self.mappings["COURSE-063"]
        combined = json.dumps(mapping, ensure_ascii=False).casefold()
        self.assertIn("block-free method remains unverified", combined)
        self.assertIn("not method-equivalent", combined)
        self.assertNotIn("block-free method is documented", combined)

    def test_final_modes_and_totals(self):
        self.assertEqual(self.coverage["COURSE-037"]["current_presentation_mode"], "FULL_COMPARISON")
        self.assertEqual(self.coverage["COURSE-063"]["current_presentation_mode"], "FULL_COMPARISON")
        self.assertEqual(self.coverage["COURSE-085"]["current_presentation_mode"], "COMPARATORS_ONLY")
        self.assertEqual(self.totals["current_presentation_mode"], {
            "COMPARATORS_ONLY": 47, "FULL_COMPARISON": 28, "RESEARCH_PENDING": 9,
        })
        self.assertEqual(self.totals["courses_with_mapping"], 28)


if __name__ == "__main__":
    unittest.main()
