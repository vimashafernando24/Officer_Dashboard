"""Focused offline checks for Step 27 comparators for five occupation groups without NYSC headings."""

from __future__ import annotations

import json
import unittest
from pathlib import Path

BASE = Path(__file__).resolve().parents[2]
BENCH = BASE / "outputs/programme_benchmarking"
GROUPS = {
    "construction_supervisor": (["COURSE-023", "COURSE-060"],
                                ["LK-TVEC-NCS-CONSTRUCTION-SITE-SUPERVISOR-2025", "AU-TGA-CPC40120-SITE-MANAGEMENT"]),
    "motorcycle": (["COURSE-030", "COURSE-078"],
                   ["LK-TVEC-NCS-MOTORCYCLE-TECHNICIAN-2025", "IN-DGT-CTS-2W3W-V2", "PH-TESDA-MOTORCYCLE-NC2", "AU-TGA-AUR30820"]),
    "auto_electrical": (["COURSE-021", "COURSE-042"],
                        ["LK-TVEC-NCS-AUTO-ELECTRICIAN-2026", "IN-DGT-CTS-MAEE-V2", "PH-TESDA-ASER-ELEC-NC2", "AU-TGA-AUR30320"]),
    "mobile_repair": (["COURSE-029", "COURSE-077"],
                      ["LK-TVEC-NCS-MOBILE-PHONE-REPAIR-2024", "PH-TESDA-MOBILE-NC3", "IN-NQR-TSSC-HANDHELD-V2"]),
    "graphic_design": (["COURSE-016", "COURSE-068"],
                       ["LK-TVEC-NCS-GRAPHIC-DESIGNER-2025", "PH-TESDA-VGD-NC3", "SG-ITE-HNITEC-COMMDESIGN-2Y"]),
}


class Step27OccupationGroupTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.datasets = {key: json.loads((BENCH / f"pilot_records_{key}.json").read_text(encoding="utf-8")) for key in GROUPS}
        cls.links = {l["nysc_course_id"]: l for l in json.loads((BENCH / "course_comparator_links.json").read_text(encoding="utf-8"))["links"]}
        cls.register = {e["course_id"]: e for e in json.loads((BENCH / "coverage_register.json").read_text(encoding="utf-8"))["courses"]}

    def test_sixteen_new_records_pending_human_review(self):
        records = [r for d in self.datasets.values() for r in d["records"]]
        self.assertEqual(len(records), 16)
        for record in records:
            with self.subTest(record=record["record_id"]):
                self.assertEqual(record["verification"]["status"], "source_inspected_pending_human_review")
                self.assertFalse(record["verification"]["human_reviewed"])
                self.assertRegex(record["source"]["document_sha256"], r"^[0-9a-f]{64}$")
                self.assertEqual(record["source"]["retrieved_date"], "2026-10-18")
                # Only ITE's programme is a confirmed delivery; standards and qualifications are not.
                self.assertEqual(record["delivering_provider_verified"], record["record_type"] == "programme")
        programmes = [r["record_id"] for r in records if r["record_type"] == "programme"]
        self.assertEqual(programmes, ["SG-ITE-HNITEC-COMMDESIGN-2Y"])

    def test_courses_are_comparators_only_without_mappings(self):
        for key, (courses, ids) in GROUPS.items():
            self.assertEqual([r["record_id"] for r in self.datasets[key]["records"]], ids)
            for course_id in courses:
                with self.subTest(course=course_id):
                    self.assertEqual(self.links[course_id]["record_ids"], ids)
                    self.assertIn("COMPARATORS_ONLY", self.links[course_id]["comparison_caveat"])
                    entry = self.register[course_id]
                    self.assertEqual(entry["evidence_availability"], "NO_HEADINGS")
                    self.assertEqual(entry["current_presentation_mode"], "COMPARATORS_ONLY")
                    self.assertFalse((BENCH / f"competency_mapping_{course_id.lower()}.json").exists())

    def test_related_groups_are_not_linked(self):
        # Three Wheeler Mechanic and Desktop Publisher are separate occupation groups with too little specific evidence.
        for course_id in ("COURSE-038", "COURSE-062"):
            self.assertNotIn(course_id, self.links)
            self.assertEqual(self.register[course_id]["current_presentation_mode"], "RESEARCH_PENDING")

    def test_missing_country_groups_are_explained(self):
        self.assertEqual(set(self.datasets["construction_supervisor"]["country_group_gaps"]), {"developing_emerging"})
        self.assertEqual(set(self.datasets["mobile_repair"]["country_group_gaps"]), {"developed"})
        for key in ("motorcycle", "auto_electrical", "graphic_design"):
            self.assertEqual(self.datasets[key]["country_group_gaps"], {})

    def test_documented_source_limitations_are_kept(self):
        records = {r["record_id"]: r for d in self.datasets.values() for r in d["records"]}
        moto = records["LK-TVEC-NCS-MOTORCYCLE-TECHNICIAN-2025"]
        self.assertTrue(any("internally inconsistent" in n and "U10" in n for n in moto["notes"]))
        self.assertTrue(any("Q4L4" in s for s in moto["scope_verbatim"]))
        auto = records["LK-TVEC-NCS-AUTO-ELECTRICIAN-2026"]
        self.assertEqual(len(auto["scope_verbatim"]), 2)
        self.assertIn("U12 + U13", auto["scope_verbatim"][1])
        self.assertNotIn("U12", auto["scope_verbatim"][0])
        self.assertTrue(any("internally inconsistent" in n for n in records["IN-NQR-TSSC-HANDHELD-V2"]["notes"]))
        self.assertIn("blank", records["PH-TESDA-MOBILE-NC3"]["source"]["publication_or_revision"])
        self.assertEqual(records["PH-TESDA-MOBILE-NC3"]["modules"][-3]["title_verbatim"],
                         "Diagnose and identity hardware and software related problems")
        ite = records["SG-ITE-HNITEC-COMMDESIGN-2Y"]
        self.assertEqual([m["group"] for m in ite["modules"]],
                         ["Cluster Core Modules"] * 4 + ["Specialisation Modules (Graphic Design)"] * 9)
        self.assertTrue(all(m["outcome_verbatim"].startswith("On completion") for m in ite["modules"]))

    def test_australian_records_store_core_units_only(self):
        records = {r["record_id"]: r for d in self.datasets.values() for r in d["records"]}
        cpc = records["AU-TGA-CPC40120-SITE-MANAGEMENT"]
        self.assertEqual([m["group"] for m in cpc["modules"]], ["Core Units"] * 11 + ["Group B – Site Manager"] * 4)
        self.assertIn("All Group B electives", cpc["scope_verbatim"])
        self.assertEqual({m["group"] for m in records["AU-TGA-AUR30820"]["modules"]}, {"Core Units"})
        self.assertEqual(len(records["AU-TGA-AUR30820"]["modules"]), 23)
        self.assertEqual(len(records["AU-TGA-AUR30320"]["modules"]), 21)


if __name__ == "__main__":
    unittest.main()
