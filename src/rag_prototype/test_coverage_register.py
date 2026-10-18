"""Checks for the coverage register of all governed NYSC courses."""

from __future__ import annotations

import json
import unittest

from src.rag_prototype.build_coverage_register import (
    BENCHMARK_DIR,
    INDEX_PATH,
    LOADERS_PATH,
    build_frontend_index,
    build_loaders,
    mapping_files,
    record_datasets,
    LINKS_PATH,
    OCCUPATION_GROUPS,
    REGISTER_PATH,
    SNAPSHOT_PATH,
    UNUSABLE_HEADINGS,
    build_register,
)
from src.rag_prototype.programme_design_evidence import load_governed_courses

FULL_COURSES = {"COURSE-005", "COURSE-007", "COURSE-008", "COURSE-010", "COURSE-011", "COURSE-012", "COURSE-014", "COURSE-025", "COURSE-034", "COURSE-035", "COURSE-040", "COURSE-046", "COURSE-047", "COURSE-055", "COURSE-064", "COURSE-082"}
COMPARATORS_ONLY_COURSES = {"COURSE-048", "COURSE-056", "COURSE-069"}
COMPLETE_COURSES = FULL_COURSES | COMPARATORS_ONLY_COURSES
RESEARCH = {"COMPLETE", "NOT_RESEARCHED", "IN_PROGRESS", "BLOCKED"}
AVAILABILITY = {"HEADINGS_AVAILABLE", "NO_HEADINGS", "HEADINGS_UNUSABLE"}
MODES = {"FULL_COMPARISON", "COMPARATORS_ONLY", "RESEARCH_PENDING", "EVIDENCE_UNAVAILABLE"}
PROPOSED_MODES = {"FULL_COMPARISON", "COMPARATORS_ONLY", "EVIDENCE_UNAVAILABLE"}


class CoverageRegisterTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.register = json.loads(REGISTER_PATH.read_text(encoding="utf-8"))
        cls.entries = cls.register["courses"]
        cls.by_id = {entry["course_id"]: entry for entry in cls.entries}
        cls.governed = {course["course_id"]: course for course in load_governed_courses()}
        cls.snapshot = {c["course_id"]: c for c in json.loads(SNAPSHOT_PATH.read_text(encoding="utf-8"))["courses"]}
        cls.links = {l["nysc_course_id"]: l["record_ids"] for l in json.loads(LINKS_PATH.read_text(encoding="utf-8"))["links"]}

    def test_register_is_up_to_date(self):
        self.assertEqual(
            self.register, build_register(),
            "Register is out of date: run python3 src/rag_prototype/build_coverage_register.py",
        )

    def test_exactly_84_unique_governed_courses_each_once(self):
        ids = [entry["course_id"] for entry in self.entries]
        self.assertEqual(len(ids), 84)
        self.assertEqual(len(set(ids)), 84)
        self.assertEqual(set(ids), set(self.governed))

    def test_titles_and_headings_come_from_the_governed_catalogue(self):
        for course_id, entry in self.by_id.items():
            governed = self.governed[course_id]
            with self.subTest(course=course_id):
                self.assertEqual(entry["governed_title"], governed["course_name"])
                self.assertEqual(entry["governed_heading_count"], len(governed["modules"]))
                flagged = len(self.snapshot[course_id]["module_review_flags"])
                self.assertEqual(entry["review_flagged_heading_count"], flagged)
                expected = 0 if course_id in UNUSABLE_HEADINGS else len(governed["modules"]) - flagged
                self.assertEqual(entry["verified_heading_count"], expected)
                self.assertGreaterEqual(entry["verified_heading_count"], 0)

    def test_every_course_is_in_exactly_one_occupation_group(self):
        members = [cid for _gid, _name, courses in OCCUPATION_GROUPS for cid in courses]
        self.assertEqual(len(members), len(set(members)))
        self.assertEqual(set(members), set(self.governed))
        for course_id, entry in self.by_id.items():
            with self.subTest(course=course_id):
                self.assertIn(course_id, entry["group_courses"])
                for other in entry["group_courses"]:
                    self.assertEqual(self.by_id[other]["occupation_group_id"], entry["occupation_group_id"])
                    self.assertEqual(self.by_id[other]["group_courses"], entry["group_courses"])

    def test_related_courses_are_valid_symmetric_and_outside_the_group(self):
        for course_id, entry in self.by_id.items():
            for other in entry["related_courses"]:
                with self.subTest(course=course_id, related=other):
                    self.assertIn(other, self.by_id)
                    self.assertNotIn(other, entry["group_courses"])
                    self.assertIn(course_id, self.by_id[other]["related_courses"])

    def test_comparator_and_mapping_status_match_the_stored_files(self):
        mapped = {
            json.loads(path.read_text(encoding="utf-8"))["nysc_course_id"]
            for path in BENCHMARK_DIR.glob("competency_mapping_course-*.json")
        }
        for course_id, entry in self.by_id.items():
            with self.subTest(course=course_id):
                self.assertEqual(entry["comparator_record_ids"], self.links.get(course_id, []))
                self.assertEqual(entry["comparator_record_count"], len(entry["comparator_record_ids"]))
                self.assertEqual(entry["competency_mapping_status"], "COMPLETE" if course_id in mapped else "NONE")

    def test_completed_courses_are_identified(self):
        complete = {cid for cid, e in self.by_id.items() if e["research_status"] == "COMPLETE"}
        self.assertEqual(complete, COMPLETE_COURSES)
        for course_id in COMPARATORS_ONLY_COURSES:
            entry = self.by_id[course_id]
            with self.subTest(course=course_id):
                # Verified comparators, but no headings to map against: no matrix is claimed.
                self.assertEqual(entry["evidence_availability"], "NO_HEADINGS")
                self.assertEqual(entry["competency_mapping_status"], "NONE")
                self.assertGreater(entry["comparator_record_count"], 0)
                self.assertEqual(entry["current_presentation_mode"], "COMPARATORS_ONLY")
        for course_id in FULL_COURSES:
            entry = self.by_id[course_id]
            with self.subTest(course=course_id):
                self.assertEqual(entry["competency_mapping_status"], "COMPLETE")
                self.assertGreaterEqual(entry["comparator_record_count"], 3)
                self.assertEqual(entry["evidence_availability"], "HEADINGS_AVAILABLE")
                self.assertEqual(entry["current_presentation_mode"], "FULL_COMPARISON")
                self.assertEqual(entry["proposed_presentation_mode"], "FULL_COMPARISON")
        # Variants in a completed group share the same comparator records.
        for left, right in (("COURSE-005", "COURSE-040"), ("COURSE-025", "COURSE-064"), ("COURSE-034", "COURSE-012"),
                            ("COURSE-008", "COURSE-055"), ("COURSE-008", "COURSE-056"),
                            ("COURSE-011", "COURSE-047"), ("COURSE-010", "COURSE-046"),
                            ("COURSE-010", "COURSE-048"), ("COURSE-014", "COURSE-069"),
                            ("COURSE-035", "COURSE-082")):
            self.assertEqual(self.by_id[left]["comparator_record_ids"], self.by_id[right]["comparator_record_ids"])

    def test_statuses_are_valid(self):
        for course_id, entry in self.by_id.items():
            with self.subTest(course=course_id):
                self.assertIn(entry["research_status"], RESEARCH)
                self.assertIn(entry["evidence_availability"], AVAILABILITY)
                self.assertIn(entry["current_presentation_mode"], MODES)
                self.assertIn(entry["proposed_presentation_mode"], PROPOSED_MODES)
                self.assertTrue(entry["proposed_mode_reason"].strip())
                self.assertTrue(entry["research_improvement"].strip())

    def test_unresearched_courses_are_distinguished_from_blocked_ones(self):
        for course_id, entry in self.by_id.items():
            with self.subTest(course=course_id):
                if entry["research_status"] == "NOT_RESEARCHED":
                    # No comparator is assumed from suggested sources.
                    self.assertEqual(entry["comparator_record_count"], 0)
                    self.assertEqual(entry["competency_mapping_status"], "NONE")
                    self.assertEqual(entry["current_presentation_mode"], "RESEARCH_PENDING")
                    self.assertIn("research has not started", entry["proposed_mode_reason"])
                    self.assertNotIn("blocking_evidence", entry)
                if entry["research_status"] == "BLOCKED":
                    self.assertTrue(entry["blocking_evidence"].strip())
                if entry["research_status"] != "COMPLETE":
                    # Never classified as permanently not comparable.
                    self.assertNotEqual(entry["proposed_presentation_mode"], "EVIDENCE_UNAVAILABLE")
                    self.assertTrue(entry["further_research_could_improve"])
        self.assertEqual(self.register["totals"]["research_status"], {"COMPLETE": 19, "NOT_RESEARCHED": 65})
        self.assertEqual(
            self.register["totals"]["current_presentation_mode"],
            {"COMPARATORS_ONLY": 3, "FULL_COMPARISON": 16, "RESEARCH_PENDING": 65},
        )

    def test_current_mode_is_derived_from_verified_evidence_only(self):
        for course_id, entry in self.by_id.items():
            with self.subTest(course=course_id):
                if entry["comparator_record_count"]:
                    expected = "FULL_COMPARISON" if entry["competency_mapping_status"] == "COMPLETE" else "COMPARATORS_ONLY"
                elif entry["research_status"] == "BLOCKED":
                    expected = "EVIDENCE_UNAVAILABLE"
                else:
                    expected = "RESEARCH_PENDING"
                self.assertEqual(entry["current_presentation_mode"], expected)
                # A proposed full comparison is never shown as current coverage.
                if entry["current_presentation_mode"] == "FULL_COMPARISON":
                    self.assertEqual(entry["research_status"], "COMPLETE")

    def test_evidence_availability_follows_the_governed_headings(self):
        for course_id, entry in self.by_id.items():
            with self.subTest(course=course_id):
                headings = entry["governed_heading_count"]
                if headings == 0:
                    self.assertEqual(entry["evidence_availability"], "NO_HEADINGS")
                elif course_id in UNUSABLE_HEADINGS:
                    self.assertEqual(entry["evidence_availability"], "HEADINGS_UNUSABLE")
                    self.assertEqual(entry["verified_heading_count"], 0)
                else:
                    self.assertEqual(entry["evidence_availability"], "HEADINGS_AVAILABLE")
                    self.assertGreater(entry["verified_heading_count"], 0)
        self.assertEqual(sorted(UNUSABLE_HEADINGS), ["COURSE-072", "COURSE-074", "COURSE-086"])

    def test_proposed_mode_follows_nysc_evidence_not_comparator_assumptions(self):
        for course_id, entry in self.by_id.items():
            with self.subTest(course=course_id):
                expected = "FULL_COMPARISON" if entry["evidence_availability"] == "HEADINGS_AVAILABLE" else "COMPARATORS_ONLY"
                self.assertEqual(entry["proposed_presentation_mode"], expected)
                if entry["evidence_availability"] == "NO_HEADINGS" and not entry["comparator_record_count"]:
                    # Missing NYSC headings are not treated as missing external comparators.
                    self.assertIn("do not imply that external comparators are missing", entry["proposed_mode_reason"])

    def test_totals_reconcile_with_the_course_entries(self):
        totals = self.register["totals"]

        def count(field):
            result = {}
            for entry in self.entries:
                result[entry[field]] = result.get(entry[field], 0) + 1
            return result

        self.assertEqual(totals["courses"], 84)
        self.assertEqual(totals["occupation_groups"], len({e["occupation_group_id"] for e in self.entries}))
        self.assertEqual(totals["occupation_groups"], len(OCCUPATION_GROUPS))
        for field in ("research_status", "evidence_availability", "current_presentation_mode", "proposed_presentation_mode"):
            self.assertEqual(totals[field], count(field), field)
            self.assertEqual(sum(totals[field].values()), 84, field)
        self.assertEqual(totals["courses_with_governed_headings"], 32)
        self.assertEqual(totals["evidence_availability"], {"HEADINGS_AVAILABLE": 29, "HEADINGS_UNUSABLE": 3, "NO_HEADINGS": 52})
        self.assertEqual(totals["proposed_presentation_mode"], {"COMPARATORS_ONLY": 55, "FULL_COMPARISON": 29})
        self.assertEqual(totals["courses_with_comparators"], 19)
        self.assertEqual(totals["courses_with_mapping"], 16)
        self.assertEqual(totals["occupation_groups_complete"], 11)
        self.assertIn(f"uses {totals['occupation_groups']} groups", self.register["reconciliation"][0])


class FrontendCoverageIndexTests(unittest.TestCase):
    """The compact index and lazy loaders the dashboard ships instead of the full register."""

    @classmethod
    def setUpClass(cls):
        cls.register = json.loads(REGISTER_PATH.read_text(encoding="utf-8"))
        cls.index = json.loads(INDEX_PATH.read_text(encoding="utf-8"))

    def test_generated_files_are_up_to_date(self):
        self.assertEqual(self.index, build_frontend_index(self.register))
        self.assertEqual(LOADERS_PATH.read_text(encoding="utf-8"), build_loaders())

    def test_index_carries_only_display_and_state_fields(self):
        allowed = {"state", "research", "headings", "verified_headings", "records", "datasets", "mapping", "blocking_evidence"}
        self.assertEqual(len(self.index["courses"]), 84)
        for course_id, item in self.index["courses"].items():
            with self.subTest(course=course_id):
                self.assertTrue(set(item) <= allowed)
        # Research-only metadata stays out of the browser.
        text = INDEX_PATH.read_text(encoding="utf-8")
        for field in ("proposed_mode_reason", "research_improvement", "related_courses", "reconciliation"):
            self.assertNotIn(field, text)
        self.assertLess(len(text), len(REGISTER_PATH.read_text(encoding="utf-8")) // 4)

    def test_index_agrees_with_the_register(self):
        by_id = {entry["course_id"]: entry for entry in self.register["courses"]}
        for course_id, item in self.index["courses"].items():
            entry = by_id[course_id]
            with self.subTest(course=course_id):
                self.assertEqual(item["state"], entry["current_presentation_mode"])
                self.assertEqual(item["records"], entry["comparator_record_ids"])
                self.assertEqual(item["mapping"], entry["competency_mapping_status"] == "COMPLETE")

    def test_every_linked_record_and_mapping_has_a_loader(self):
        datasets = record_datasets()
        dataset_of = {rid: key for key, ids in datasets.items() for rid in ids}
        loaders = LOADERS_PATH.read_text(encoding="utf-8")
        for key in datasets:
            self.assertIn(f'"{key}": () => import(', loaders)
            self.assertTrue((BENCHMARK_DIR / f"pilot_records_{key}.json").exists())
        for course_id, name in mapping_files().items():
            self.assertIn(f'"{course_id}": () => import("../../../../../outputs/programme_benchmarking/{name}"', loaders)
        for course_id, item in self.index["courses"].items():
            with self.subTest(course=course_id):
                self.assertEqual(item["datasets"], sorted({dataset_of[rid] for rid in item["records"]}))
                if item["mapping"]:
                    self.assertIn(course_id, mapping_files())


if __name__ == "__main__":
    unittest.main()
