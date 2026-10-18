"""Focused offline regressions for Step 35 early childhood, human resources and store management evidence."""

from __future__ import annotations

import json
import unittest
from pathlib import Path

BASE = Path(__file__).resolve().parents[2]
BENCH = BASE / "outputs/programme_benchmarking"
LINKS = {
    "COURSE-041": ["LK-TVEC-NCS-ECCD-TEACHER-2026", "IN-DGT-CTS-EARLY-CHILDHOOD-EDUCATOR-V2", "AU-TGA-CHC30125"],
    "COURSE-071": ["LK-TVEC-NCS-HR-ASSOCIATE-2024", "LK-TVEC-NCS-HRM-DIPLOMA-2022", "AU-TGA-BSB40420"],
    "COURSE-084": ["LK-TVEC-NCS-STORE-KEEPER-2019", "IN-DGT-ATS-STORAGE-INVENTORY-EXECUTIVE", "AU-TGA-TLI30325-WAREHOUSING"],
}
DATASETS = {"early_childhood": "COURSE-041", "human_resources": "COURSE-071", "store_management": "COURSE-084"}


def areas(mapping, records):
    nysc = f"NYSC-{mapping['nysc_course_id']}"
    out = []
    for comp in mapping["competencies"]:
        if comp["cells"][nysc]["status"] != "NOT_EXPLICIT":
            continue
        full = [c["record_id"] for c in mapping["columns"] if c["kind"] == "benchmark" and comp["cells"][c["column_id"]].get("coverage") == "FULL"]
        if len(full) >= 2 and len({records[r]["country"] for r in full}) >= 2:
            out.append(comp["competency_id"])
    return out


class Step35Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.datasets = {k: json.loads((BENCH / f"pilot_records_{k}.json").read_text(encoding="utf-8")) for k in DATASETS}
        cls.records = {r["record_id"]: r for p in BENCH.glob("pilot_records_*.json") for r in json.loads(p.read_text(encoding="utf-8"))["records"]}
        cls.links = {l["nysc_course_id"]: l for l in json.loads((BENCH / "course_comparator_links.json").read_text(encoding="utf-8"))["links"]}
        cls.register = {e["course_id"]: e for e in json.loads((BENCH / "coverage_register.json").read_text(encoding="utf-8"))["courses"]}

    def test_new_records_are_pending_review_and_not_deliveries(self):
        for key, course in DATASETS.items():
            self.assertEqual([r["record_id"] for r in self.datasets[key]["records"]], LINKS[course])
            for record in self.datasets[key]["records"]:
                with self.subTest(record=record["record_id"]):
                    self.assertEqual(record["verification"]["status"], "source_inspected_pending_human_review")
                    self.assertFalse(record["verification"]["human_reviewed"])
                    self.assertFalse(record["delivering_provider_verified"])
                    self.assertRegex(record["source"]["document_sha256"], r"^[0-9a-f]{64}$")

    def test_links_and_coverage_states(self):
        for course_id, ids in LINKS.items():
            self.assertEqual(self.links[course_id]["record_ids"], ids)
        self.assertEqual(self.register["COURSE-041"]["current_presentation_mode"], "FULL_COMPARISON")
        self.assertEqual(self.register["COURSE-071"]["current_presentation_mode"], "FULL_COMPARISON")
        self.assertEqual(self.register["COURSE-084"]["current_presentation_mode"], "COMPARATORS_ONLY")
        self.assertFalse((BENCH / "competency_mapping_course-084.json").exists())
        # Business Management stays pending: generic title and no governed headings.
        self.assertEqual(self.register["COURSE-049"]["current_presentation_mode"], "RESEARCH_PENDING")
        self.assertNotIn("COURSE-049", self.links)

    def test_course_041_skips_the_unspecific_heading(self):
        mapping = json.loads((BENCH / "competency_mapping_course-041.json").read_text(encoding="utf-8"))
        cited = {e["module_index"] for c in mapping["competencies"] for e in c["cells"]["NYSC-COURSE-041"]["evidence"]}
        self.assertEqual(cited, {1, 2, 3})
        self.assertEqual(areas(mapping, self.records),
                         ["ecd_health_safety", "ecd_language_literacy", "ecd_creative_arts", "ecd_inclusion"])

    def test_course_071_abbreviations_are_never_interpreted(self):
        mapping = json.loads((BENCH / "competency_mapping_course-071.json").read_text(encoding="utf-8"))
        cells = {c["competency_id"]: c["cells"]["NYSC-COURSE-071"] for c in mapping["competencies"]}
        for cid in ("hr_training_development", "hr_performance", "hr_employee_relations"):
            self.assertEqual(cells[cid]["status"], "INSUFFICIENT_DATA", cid)
        self.assertEqual(cells["hr_recruitment_selection"]["evidence"][0]["display_text"], "JD, JA Recruitment, Selection, Hiring, Induction")
        self.assertEqual(areas(mapping, self.records), ["hr_whs"])

    def test_source_limitations_are_recorded(self):
        eccd = self.records["LK-TVEC-NCS-ECCD-TEACHER-2026"]
        self.assertTrue(any("M80S001U12" in n for n in eccd["notes"]))
        self.assertTrue(any("PRESCHOOL TEACHER" in n for n in eccd["notes"]))
        for rid in ("LK-TVEC-NCS-HR-ASSOCIATE-2024", "LK-TVEC-NCS-HRM-DIPLOMA-2022", "LK-TVEC-NCS-STORE-KEEPER-2019"):
            self.assertTrue(any("has passed" in n for n in self.records[rid]["notes"]), rid)
        self.assertIn("developing_emerging", self.datasets["human_resources"]["country_group_gaps"])
        self.assertTrue(all(m["code"] is None for m in self.records["LK-TVEC-NCS-STORE-KEEPER-2019"]["modules"][6:]))


if __name__ == "__main__":
    unittest.main()
