"""Focused offline regressions for Step 38 language courses and the documented remaining pending courses."""

from __future__ import annotations

import json
import unittest
from pathlib import Path

BASE = Path(__file__).resolve().parents[2]
BENCH = BASE / "outputs/programme_benchmarking"
EAL = ["AU-VIC-22643VIC-EAL-EMPLOYMENT", "AU-VIC-22644VIC-EAL-PROFESSIONAL"]
STILL_PENDING = ["COURSE-003", "COURSE-049", "COURSE-067", "COURSE-070", "COURSE-072", "COURSE-074", "COURSE-075", "COURSE-083", "COURSE-086"]


class Step38Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.dataset = json.loads((BENCH / "pilot_records_english_language.json").read_text(encoding="utf-8"))
        cls.links = {l["nysc_course_id"]: l for l in json.loads((BENCH / "course_comparator_links.json").read_text(encoding="utf-8"))["links"]}
        cls.register = {e["course_id"]: e for e in json.loads((BENCH / "coverage_register.json").read_text(encoding="utf-8"))["courses"]}

    def test_eal_records_and_links(self):
        records = {r["record_id"]: r for r in self.dataset["records"]}
        self.assertEqual(list(records), EAL)
        for record in records.values():
            self.assertEqual(record["verification"]["status"], "source_inspected_pending_human_review")
            self.assertFalse(record["verification"]["human_reviewed"])
            self.assertFalse(record["delivering_provider_verified"])
            self.assertEqual(record["record_type"], "national_qualification")
        self.assertEqual([m["group"] for m in records["AU-VIC-22644VIC-EAL-PROFESSIONAL"]["modules"]],
                         ["Core units", "Core units", "Professional Specialisation", "Professional Specialisation"])
        for course_id in ("COURSE-066", "COURSE-004"):
            self.assertEqual(self.links[course_id]["record_ids"], EAL)
            self.assertEqual(self.register[course_id]["current_presentation_mode"], "COMPARATORS_ONLY")
        self.assertEqual(set(self.dataset["country_group_gaps"]), {"sri_lanka", "developing_emerging"})

    def test_unsupported_courses_stay_pending_with_documented_reasons(self):
        pending = sorted(cid for cid, e in self.register.items() if e["current_presentation_mode"] == "RESEARCH_PENDING")
        self.assertEqual(pending, STILL_PENDING)
        for course_id in STILL_PENDING:
            with self.subTest(course=course_id):
                self.assertNotIn(course_id, self.links)
                self.assertEqual(self.register[course_id]["comparator_record_count"], 0)
                self.assertTrue(any(n.startswith("Researched (Step") for n in self.register[course_id]["notes"]))


if __name__ == "__main__":
    unittest.main()
