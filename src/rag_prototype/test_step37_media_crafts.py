"""Focused offline regressions for Step 37 media and crafts evidence (TV production, video/animation, gem cutting)."""

from __future__ import annotations

import json
import unittest
from pathlib import Path

BASE = Path(__file__).resolve().parents[2]
BENCH = BASE / "outputs/programme_benchmarking"
LINKS = {
    "COURSE-031": ["LK-TVEC-NCS-TV-DIGITAL-MEDIA-PRODUCTION-2025", "PH-TESDA-FILM-VIDEO-POSTPRODUCTION-NC3", "SG-ITE-HNITEC-FILM-VIDEO-2Y"],
    "COURSE-059": ["LK-TVEC-NCS-MULTIMEDIA-DESIGNING-ASSOCIATE-2019", "IN-DGT-CTS-MASE-V2", "PH-TESDA-3D-ANIMATION-NC3", "PH-TESDA-FILM-VIDEO-POSTPRODUCTION-NC3"],
    "COURSE-028": ["LK-TVEC-NCS-LAPIDARIST-2022"],
}
DATASETS = ["tv_production", "video_animation", "lapidary"]


class Step37Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.datasets = {k: json.loads((BENCH / f"pilot_records_{k}.json").read_text(encoding="utf-8")) for k in DATASETS}
        cls.records = {r["record_id"]: r for d in cls.datasets.values() for r in d["records"]}
        cls.links = {l["nysc_course_id"]: l for l in json.loads((BENCH / "course_comparator_links.json").read_text(encoding="utf-8"))["links"]}
        cls.register = {e["course_id"]: e for e in json.loads((BENCH / "coverage_register.json").read_text(encoding="utf-8"))["courses"]}

    def test_records_are_pending_review(self):
        self.assertEqual(len(self.records), 7)
        for record in self.records.values():
            with self.subTest(record=record["record_id"]):
                self.assertEqual(record["verification"]["status"], "source_inspected_pending_human_review")
                self.assertFalse(record["verification"]["human_reviewed"])
                self.assertEqual(record["delivering_provider_verified"], record["record_type"] == "programme")
                self.assertRegex(record["source"]["document_sha256"], r"^[0-9a-f]{64}$")

    def test_links_are_comparators_only(self):
        for course_id, ids in LINKS.items():
            self.assertEqual(self.links[course_id]["record_ids"], ids)
            self.assertIn("COMPARATORS_ONLY", self.links[course_id]["comparison_caveat"])
            self.assertEqual(self.register[course_id]["current_presentation_mode"], "COMPARATORS_ONLY")
            self.assertFalse((BENCH / f"competency_mapping_{course_id.lower()}.json").exists())
        # Mass Communication and Handycraft stay pending: weak or unspecified scope.
        for course_id in ("COURSE-075", "COURSE-070"):
            self.assertNotIn(course_id, self.links)
            self.assertEqual(self.register[course_id]["current_presentation_mode"], "RESEARCH_PENDING")

    def test_source_details_and_limitations(self):
        tesda = [m["code"] for m in self.records["PH-TESDA-FILM-VIDEO-POSTPRODUCTION-NC3"]["modules"]]
        self.assertEqual(len(tesda), 20)
        self.assertEqual(tesda.index("400311326"), tesda.index("400311325") + 1)
        tv = self.records["LK-TVEC-NCS-TV-DIGITAL-MEDIA-PRODUCTION-2025"]["modules"]
        self.assertEqual([m["group"] for m in tv], ["NVQ Level 5 units"] * 8 + ["NVQ Level 6 units"] * 10)
        self.assertTrue(any("O92S004" in n for n in self.records["LK-TVEC-NCS-MULTIMEDIA-DESIGNING-ASSOCIATE-2019"]["notes"]))
        self.assertTrue(any("NC II" in n for n in self.records["PH-TESDA-3D-ANIMATION-NC3"]["notes"]))
        self.assertEqual(set(self.datasets["lapidary"]["country_group_gaps"]), {"developing_emerging", "developed"})
        self.assertIn("CUA51020", self.datasets["video_animation"]["country_group_gaps"]["developed"])


if __name__ == "__main__":
    unittest.main()
