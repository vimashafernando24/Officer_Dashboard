"""Integrity checks for the curated programme-benchmarking pilot records.

These records feed a future curriculum-difference analysis, so the checks
enforce the evidence rules from the feasibility study: standards are never
presented as delivered programmes, paraphrased content is never used as module
text, and every PDF source carries a hash so that later changes are detectable.
"""

from __future__ import annotations

import json
import re
import unittest
from pathlib import Path

BASE = Path(__file__).resolve().parents[2]
BENCHMARK_DIR = BASE / "outputs/programme_benchmarking"
SCHEMA_PATH = BENCHMARK_DIR / "benchmark_record_schema.json"
RECORD_PATHS = sorted(BENCHMARK_DIR.glob("pilot_records_*.json"))
LINKS_PATH = BENCHMARK_DIR / "course_comparator_links.json"


class ProgrammeBenchmarkingRecordTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
        cls.datasets = {
            path.name: json.loads(path.read_text(encoding="utf-8")) for path in RECORD_PATHS
        }
        cls.records = [record for dataset in cls.datasets.values() for record in dataset["records"]]
        cls.by_id = {record["record_id"]: record for record in cls.records}

    def test_records_conform_to_schema(self):
        try:
            import jsonschema
        except ImportError:  # optional dependency; the rule checks below still run
            self.skipTest("jsonschema is not installed")
        validator = jsonschema.Draft202012Validator(self.schema)
        for record in self.records:
            with self.subTest(record=record["record_id"]):
                errors = sorted(validator.iter_errors(record), key=lambda e: list(e.path))
                self.assertEqual([], [f"{list(e.path)}: {e.message}" for e in errors])

    def test_record_ids_are_unique(self):
        ids = [record["record_id"] for record in self.records]
        self.assertEqual(len(ids), len(set(ids)))

    def test_standards_are_not_presented_as_delivered_programmes(self):
        for record in self.records:
            with self.subTest(record=record["record_id"]):
                if record["record_type"] == "programme":
                    self.assertTrue(record["delivering_provider_verified"])

    def test_paraphrased_content_is_never_stored_as_module_text(self):
        for record in self.records:
            with self.subTest(record=record["record_id"]):
                if record["content_fidelity"] == "paraphrased_needs_manual_copy":
                    self.assertEqual(record["modules"], [])
                    self.assertEqual(record["verification"]["status"], "needs_manual_verbatim")
                else:
                    self.assertTrue(record["modules"])
                    self.assertIsNone(record.get("content_summary_paraphrased"))

    def test_pdf_sources_are_hashed(self):
        for record in self.records:
            with self.subTest(record=record["record_id"]):
                source = record["source"]
                if source["document_type"] == "pdf":
                    self.assertRegex(source["document_sha256"] or "", r"^[0-9a-f]{64}$")

    def test_module_text_is_present_and_untrimmed(self):
        for record in self.records:
            for module in record["modules"]:
                with self.subTest(record=record["record_id"], module=module["title_verbatim"][:40]):
                    self.assertTrue(module["title_verbatim"].strip())
                    self.assertEqual(module["title_verbatim"], module["title_verbatim"].strip())

    def test_no_record_claims_human_verification_yet(self):
        # Pilot records were collected automatically; a researcher must check
        # each against its source before the status may change.
        for record in self.records:
            with self.subTest(record=record["record_id"]):
                self.assertFalse(record["verification"]["human_reviewed"])
                self.assertNotEqual(record["verification"]["status"], "human_verified")

    def test_each_dataset_covers_each_country_group(self):
        self.assertEqual(
            sorted(self.datasets),
            [
                "pilot_records_automotive.json",
                "pilot_records_baker.json",
                "pilot_records_beauty.json",
                "pilot_records_cake_decorator.json",
                "pilot_records_cookery.json",
                "pilot_records_electrical.json",
                "pilot_records_hairdressing.json",
                "pilot_records_hardware.json",
                "pilot_records_ict.json",
                "pilot_records_rac.json",
                "pilot_records_secretary.json",
                "pilot_records_web.json",
            ],
        )
        for name, dataset in self.datasets.items():
            with self.subTest(dataset=name):
                groups = {record["country_group"] for record in dataset["records"]}
                # A missing group must be explained, never silently absent.
                gaps = dataset.get("country_group_gaps", {})
                self.assertFalse(groups & set(gaps))
                for reason in gaps.values():
                    self.assertTrue(reason.strip())
                self.assertEqual(groups | set(gaps), {"sri_lanka", "developing_emerging", "developed"})

    def test_module_order_and_codes_within_a_record_are_unique_where_published(self):
        for record in self.records:
            codes = [m["code"] for m in record["modules"] if m["code"]]
            refs = [m["published_ref"] for m in record["modules"] if m["published_ref"]]
            with self.subTest(record=record["record_id"]):
                # DGT repeats two outcome codes across years by design; refs stay unique.
                self.assertEqual(len(refs), len(set(refs)))
                if not record["record_id"].startswith("IN-DGT"):
                    self.assertEqual(len(codes), len(set(codes)))

    def test_course_links_reference_existing_records_and_governed_courses(self):
        from src.rag_prototype.programme_design_evidence import load_governed_courses

        links = json.loads(LINKS_PATH.read_text(encoding="utf-8"))["links"]
        record_ids = {record["record_id"] for record in self.records}
        course_ids = {course["course_id"] for course in load_governed_courses()}
        linked_courses = [link["nysc_course_id"] for link in links]
        self.assertEqual(len(linked_courses), len(set(linked_courses)))
        for link in links:
            with self.subTest(course=link["nysc_course_id"]):
                self.assertIn(link["nysc_course_id"], course_ids)
                self.assertTrue(link["record_ids"])
                self.assertEqual(len(link["record_ids"]), len(set(link["record_ids"])))
                self.assertTrue(set(link["record_ids"]) <= record_ids)
                self.assertTrue(link["basis"].strip())
                self.assertTrue(set(link) <= {"nysc_course_id", "record_ids", "basis", "comparison_caveat"})
                if "comparison_caveat" in link:
                    self.assertTrue(link["comparison_caveat"].strip())


class CgttiAutomobileRecordTests(unittest.TestCase):
    """The CGTTI Automobile Technician curriculum captured from its official page."""

    @classmethod
    def setUpClass(cls):
        dataset = json.loads((BENCHMARK_DIR / "pilot_records_automotive.json").read_text(encoding="utf-8"))
        cls.matches = [r for r in dataset["records"] if r["record_id"] == "LK-CGTTI-AUTO-TECH"]
        cls.record = cls.matches[0]

    def test_record_is_updated_in_place_not_duplicated(self):
        self.assertEqual(len(self.matches), 1)

    def test_curriculum_is_captured_verbatim_in_published_order(self):
        modules = self.record["modules"]
        self.assertEqual(len(modules), 17)
        self.assertEqual(self.record["content_fidelity"], "verbatim")
        self.assertIsNone(self.record["content_summary_paraphrased"])
        self.assertEqual(
            [m["group"] for m in modules],
            ["First Year"] + ["Second Year"] * 4 + ["Third Year"] * 8 + ["Final Year"] * 3 + ["Theory"],
        )
        self.assertEqual(modules[0]["title_verbatim"], "Basic Training at CGTTI: Building Foundations for Excellence")
        self.assertEqual(modules[12]["title_verbatim"], "Electronic Ignition System, Fuel Injection System, Emission Control, Common Rail Electronic Diesel Supply System. – ( 02 Months )")
        self.assertEqual([m["published_ref"] for m in modules if m["published_ref"]], ["1", "2", "3", "4"])
        self.assertTrue(all(m["code"] is None for m in modules))

    def test_facts_stay_as_published(self):
        self.assertIsNone(self.record["level_as_published"])
        self.assertEqual(self.record["duration_as_published"], "Full Time, 4 Years")
        self.assertEqual(self.record["source"]["url"], "https://germantec.lk/index.php/automobile-mechanic-3/")
        self.assertIn("02/01/2024", self.record["source"]["publication_or_revision"])

    def test_verification_is_pending_human_review(self):
        self.assertEqual(self.record["verification"]["status"], "source_inspected_pending_human_review")
        self.assertFalse(self.record["verification"]["human_reviewed"])


class ElectricianRecordTests(unittest.TestCase):
    """The six verified Electrician comparators for COURSE-025 and COURSE-064."""

    ELECTRICIAN_IDS = [
        "LK-CGTTI-POWER-ELEC",
        "IN-DGT-CTS-ELEC-V3",
        "PH-TESDA-EIM-NC2",
        "PH-TESDA-EIM-NC3",
        "SG-ITE-HNITEC-ELEC-2Y",
        "AU-TAFENSW-UEE30820",
    ]

    @classmethod
    def setUpClass(cls):
        dataset = json.loads((BENCHMARK_DIR / "pilot_records_electrical.json").read_text(encoding="utf-8"))
        cls.records = {record["record_id"]: record for record in dataset["records"]}
        cls.links = {
            link["nysc_course_id"]: link
            for link in json.loads(LINKS_PATH.read_text(encoding="utf-8"))["links"]
        }

    def codes(self, record_id, group=None):
        return [m["code"] for m in self.records[record_id]["modules"] if group is None or m["group"] == group]

    def test_six_records_with_expected_types_and_groups(self):
        self.assertEqual(list(self.records), self.ELECTRICIAN_IDS)
        expected = {
            "LK-CGTTI-POWER-ELEC": ("programme", "sri_lanka"),
            "IN-DGT-CTS-ELEC-V3": ("national_curriculum", "developing_emerging"),
            "PH-TESDA-EIM-NC2": ("occupational_standard", "developing_emerging"),
            "PH-TESDA-EIM-NC3": ("occupational_standard", "developing_emerging"),
            "SG-ITE-HNITEC-ELEC-2Y": ("programme", "developed"),
            "AU-TAFENSW-UEE30820": ("programme", "developed"),
        }
        for record_id, (record_type, group) in expected.items():
            with self.subTest(record=record_id):
                self.assertEqual(self.records[record_id]["record_type"], record_type)
                self.assertEqual(self.records[record_id]["country_group"], group)

    def test_both_electrician_courses_link_all_six_records_with_a_scope_caveat(self):
        for course_id in ("COURSE-025", "COURSE-064"):
            with self.subTest(course=course_id):
                link = self.links[course_id]
                self.assertEqual(link["record_ids"], self.ELECTRICIAN_IDS)
                self.assertIn("NC II", link["comparison_caveat"])
                self.assertIn("NC III", link["comparison_caveat"])

    def test_course_005_now_carries_the_duration_and_level_caveat(self):
        self.assertEqual(
            self.links["COURSE-005"]["comparison_caveat"],
            "Different programme duration and qualification levels; curriculum content comparison only.",
        )

    def test_cgtti_is_not_assigned_an_nvq_level(self):
        self.assertIsNone(self.records["LK-CGTTI-POWER-ELEC"]["level_as_published"])

    def test_dgt_uses_version_3_with_28_coded_outcomes(self):
        record = self.records["IN-DGT-CTS-ELEC-V3"]
        self.assertIn("Version 3.0", record["source"]["publication_or_revision"])
        self.assertEqual([m["published_ref"] for m in record["modules"]], [f"LO{n}" for n in range(1, 29)])
        self.assertTrue(all(re.fullmatch(r"PSS/N\d{4}", m["code"]) for m in record["modules"]))
        self.assertTrue(any("spacing" in note.lower() for note in record["notes"]))

    def test_tesda_nc2_and_nc3_stay_separate_with_their_own_core_units(self):
        self.assertEqual(self.codes("PH-TESDA-EIM-NC2", "Core Competencies"), ["ELC741301", "ELC741302", "ELC741303"])
        self.assertEqual(self.codes("PH-TESDA-EIM-NC3", "Core Units of Competency"), ["ELC741304", "ELC741305", "ELC741306"])
        self.assertIn("NC II", self.records["PH-TESDA-EIM-NC3"]["entry_as_published"])

    def test_tafe_core_units_match_training_gov_au_release_6(self):
        record = self.records["AU-TAFENSW-UEE30820"]
        self.assertEqual(len(record["modules"]), 27)
        self.assertTrue(all(m["group"] == "Core" for m in record["modules"]))
        self.assertIn("Release 6", record["source"]["publication_or_revision"])

    def test_scope_verbatim_is_stored_only_for_the_tesda_electrician_standards(self):
        with_scope = {rid for rid, r in self.records.items() if r.get("scope_verbatim")}
        self.assertEqual(with_scope, {"PH-TESDA-EIM-NC2", "PH-TESDA-EIM-NC3"})
        self.assertIn("residential houses/buildings", self.records["PH-TESDA-EIM-NC2"]["scope_verbatim"][0])
        self.assertIn("Industrial Electrician", self.records["PH-TESDA-EIM-NC3"]["scope_verbatim"][1])

    def test_record_counts_and_links_are_unchanged(self):
        automotive = json.loads((BENCHMARK_DIR / "pilot_records_automotive.json").read_text(encoding="utf-8"))["records"]
        self.assertEqual(len(automotive), 5)
        self.assertEqual(len(self.records), 6)
        auto_ids = ["LK-CGTTI-AUTO-TECH", "IN-DGT-CTS-MMV-V2", "PH-TESDA-ASER-NC2",
                    "SG-ITE-HNITEC-AUTO-2Y", "AU-TAFENSW-AUR30620"]
        self.assertEqual(sorted(auto_ids), sorted(r["record_id"] for r in automotive))
        self.assertEqual(self.links["COURSE-005"]["record_ids"], auto_ids)
        self.assertEqual(self.links["COURSE-040"]["record_ids"], auto_ids)
        self.assertEqual(
            sorted(self.links),
            ["COURSE-001", "COURSE-005", "COURSE-007", "COURSE-008", "COURSE-009", "COURSE-010", "COURSE-011", "COURSE-012", "COURSE-014", "COURSE-025", "COURSE-034", "COURSE-035", "COURSE-040", "COURSE-046", "COURSE-047", "COURSE-048", "COURSE-050", "COURSE-051", "COURSE-053", "COURSE-054", "COURSE-055", "COURSE-056", "COURSE-057", "COURSE-064", "COURSE-069", "COURSE-082", "COURSE-087"],
        )

    def test_no_electrician_record_claims_human_review(self):
        for record_id, record in self.records.items():
            with self.subTest(record=record_id):
                self.assertEqual(record["verification"]["status"], "source_inspected_pending_human_review")
                self.assertFalse(record["verification"]["human_reviewed"])


class RefrigerationRecordTests(unittest.TestCase):
    """The five verified RAC comparators for COURSE-034 and COURSE-012 (Step 14C)."""

    RAC_IDS = [
        "LK-CGTTI-RAC-MECH",
        "IN-DGT-CTS-RAC-V2",
        "PH-TESDA-DOMRAC-NC2",
        "PH-TESDA-CAC-NC3",
        "AU-TGA-UEE32225",
    ]
    # Hashes of the official PDFs inspected in Step 14B and re-downloaded unchanged on 2026-10-18.
    PDF_HASHES = {
        "IN-DGT-CTS-RAC-V2": "b462381f252c906edd15cf1abef333f00c48303ee7e50376a630af69462fab21",
        "PH-TESDA-DOMRAC-NC2": "7b406c8d341940a1aff4564e58b1e687fc0c6b9ea328221ebbd25e491bd73fbc",
        "PH-TESDA-CAC-NC3": "19b93da68e0ebe0aaaf24cd826d2e0b8524dfb5c6f2c36a0f2b2ff00581f0a2a",
        "AU-TGA-UEE32225": "ea28c2075c52c81623187fca20acddfb9828ccc9705ab72b94775c7daa4f10a3",
    }

    @classmethod
    def setUpClass(cls):
        dataset = json.loads((BENCHMARK_DIR / "pilot_records_rac.json").read_text(encoding="utf-8"))
        cls.records = {record["record_id"]: record for record in dataset["records"]}
        cls.links = {
            link["nysc_course_id"]: link
            for link in json.loads(LINKS_PATH.read_text(encoding="utf-8"))["links"]
        }

    def modules(self, record_id, group=None):
        return [m for m in self.records[record_id]["modules"] if group is None or m["group"] == group]

    def test_five_records_with_expected_types_groups_and_counts(self):
        self.assertEqual(list(self.records), self.RAC_IDS)
        expected = {
            "LK-CGTTI-RAC-MECH": ("programme", "sri_lanka", True, 18),
            "IN-DGT-CTS-RAC-V2": ("national_curriculum", "developing_emerging", False, 56),
            "PH-TESDA-DOMRAC-NC2": ("occupational_standard", "developing_emerging", False, 21),
            "PH-TESDA-CAC-NC3": ("occupational_standard", "developing_emerging", False, 22),
            "AU-TGA-UEE32225": ("national_qualification", "developed", False, 27),
        }
        for record_id, (record_type, group, provider, count) in expected.items():
            with self.subTest(record=record_id):
                record = self.records[record_id]
                self.assertEqual(record["record_type"], record_type)
                self.assertEqual(record["country_group"], group)
                self.assertEqual(record["delivering_provider_verified"], provider)
                self.assertEqual(len(record["modules"]), count)

    def test_both_rac_courses_link_the_same_five_records_with_a_scope_caveat(self):
        for course_id in ("COURSE-034", "COURSE-012"):
            with self.subTest(course=course_id):
                link = self.links[course_id]
                self.assertEqual(link["record_ids"], self.RAC_IDS)
                self.assertIn("window-type air-conditioning and domestic refrigerators only", link["comparison_caveat"])
                self.assertIn("commercial air-conditioning units only", link["comparison_caveat"])
                self.assertIn("not a delivered programme", link["comparison_caveat"])
        self.assertNotEqual(self.links["COURSE-034"]["basis"], self.links["COURSE-012"]["basis"])

    def test_pdf_sources_keep_the_verified_hashes_and_versions(self):
        for record_id, digest in self.PDF_HASHES.items():
            with self.subTest(record=record_id):
                self.assertEqual(self.records[record_id]["source"]["document_sha256"], digest)
        revisions = {rid: r["source"]["publication_or_revision"] for rid, r in self.records.items()}
        self.assertEqual(revisions["IN-DGT-CTS-RAC-V2"], "Version 2.0, revised July 2022")
        self.assertEqual(revisions["PH-TESDA-DOMRAC-NC2"], "HVCDRA221; Promulgated: June 8, 2021")
        self.assertEqual(revisions["PH-TESDA-CAC-NC3"], "HVCCAC321; Promulgated: June 8, 2021")
        self.assertIn("Release 1", revisions["AU-TGA-UEE32225"])
        self.assertIn("02/01/2024", revisions["LK-CGTTI-RAC-MECH"])

    def test_cgtti_curriculum_is_grouped_by_published_year(self):
        record = self.records["LK-CGTTI-RAC-MECH"]
        self.assertIsNone(record["level_as_published"])
        self.assertEqual(record["duration_as_published"], "Full Time, 42 Months")
        self.assertEqual(
            [m["group"] for m in record["modules"]],
            ["First Year"] + ["Second Year"] * 6 + ["Third Year"] * 5 + ["Final Year (In-plant Training)"] * 6,
        )
        self.assertEqual(record["modules"][11]["title_verbatim"], "Prepare estimate for Repair & Maintenance work")

    def test_dgt_outcomes_are_numbered_and_codes_have_no_internal_spaces(self):
        modules = self.modules("IN-DGT-CTS-RAC-V2")
        self.assertEqual([m["published_ref"] for m in modules], [f"LO{n}" for n in range(1, 57)])
        self.assertEqual({m["group"] for m in modules[:26]}, {"First Year learning outcomes"})
        self.assertEqual({m["group"] for m in modules[26:]}, {"Second Year learning outcomes"})
        self.assertTrue(all(re.fullmatch(r"(ELE|CSC)/N\d{4}", m["code"]) for m in modules))
        self.assertEqual([modules[0]["code"], modules[6]["code"]], ["ELE/N1002", "ELE/N3108"])
        self.assertFalse(any("NOS" in m["title_verbatim"] for m in modules))
        self.assertEqual(modules[54]["title_verbatim"], modules[24]["title_verbatim"])
        self.assertEqual(self.records["IN-DGT-CTS-RAC-V2"]["level_as_published"], "NSQF LEVEL - 4")

    def test_tesda_nc2_and_nc3_stay_separate_with_their_own_core_units(self):
        self.assertEqual(
            [m["code"] for m in self.modules("PH-TESDA-DOMRAC-NC2", "Core Competencies")],
            ["HVC723337", "HVC723338", "HVC723339"],
        )
        self.assertEqual(
            [m["code"] for m in self.modules("PH-TESDA-CAC-NC3", "Core Competencies")],
            ["HVC723340", "HVC723342", "HVC723344", "HVC723346"],
        )
        for record_id in ("PH-TESDA-DOMRAC-NC2", "PH-TESDA-CAC-NC3"):
            groups = [m["group"] for m in self.modules(record_id)]
            self.assertEqual(groups[:18], ["Basic Competencies"] * 9 + ["Common Competencies"] * 9)
        self.assertIn("window-type air-conditioning and domestic refrigerators only",
                      self.records["PH-TESDA-DOMRAC-NC2"]["scope_verbatim"][0])
        self.assertIn("commercial air-conditioning units", self.records["PH-TESDA-CAC-NC3"]["scope_verbatim"][0])
        self.assertIn("DomRAC) NC II", self.records["PH-TESDA-CAC-NC3"]["entry_as_published"])
        self.assertIn("528 Hour - Total training duration", self.records["PH-TESDA-DOMRAC-NC2"]["duration_as_published"])
        self.assertIn("720 Hours - Total training duration", self.records["PH-TESDA-CAC-NC3"]["duration_as_published"])

    def test_uee32225_is_a_current_national_qualification_without_a_stated_duration(self):
        record = self.records["AU-TGA-UEE32225"]
        codes = [m["code"] for m in record["modules"]]
        self.assertEqual({m["group"] for m in record["modules"]}, {"Core units"})
        self.assertIn("UEERA0099", codes)
        self.assertNotIn("UEERA0051", codes)
        self.assertEqual(codes.index("UEERA0099"), codes.index("UEERA0050") + 1)  # published order
        self.assertIsNone(record["duration_as_published"])
        self.assertFalse(any("*" in m["title_verbatim"] for m in record["modules"]))

    def test_no_rac_record_claims_human_review(self):
        for record_id, record in self.records.items():
            with self.subTest(record=record_id):
                self.assertEqual(record["verification"]["status"], "source_inspected_pending_human_review")
                self.assertFalse(record["verification"]["human_reviewed"])


class BakerAndCookeryRecordTests(unittest.TestCase):
    """Step 19B official-source records and course links."""

    @classmethod
    def setUpClass(cls):
        cls.baker = json.loads((BENCHMARK_DIR / "pilot_records_baker.json").read_text(encoding="utf-8"))["records"]
        cls.cookery = json.loads((BENCHMARK_DIR / "pilot_records_cookery.json").read_text(encoding="utf-8"))["records"]
        cls.links = {
            link["nysc_course_id"]: link
            for link in json.loads(LINKS_PATH.read_text(encoding="utf-8"))["links"]
        }

    def test_baker_records_and_links_are_complete(self):
        expected = ["IN-DGT-CTS-BAKER-V2", "SG-ITE-HNITEC-PASTRY-2Y", "AU-TGA-FBP30521"]
        self.assertEqual([record["record_id"] for record in self.baker], expected)
        for course_id in ("COURSE-011", "COURSE-047"):
            self.assertEqual(self.links[course_id]["record_ids"], expected)
        self.assertEqual([len(record["modules"]) for record in self.baker], [13, 17, 31])

    def test_cookery_records_and_link_are_complete(self):
        expected = [
            "IN-DGT-CTS-FOOD-PROD-V2",
            "PH-TESDA-PRO-COOKERY-NC3",
            "SG-ITE-HNITEC-CULINARY-2Y",
            "AU-TGA-SIT30821",
        ]
        self.assertEqual([record["record_id"] for record in self.cookery], expected)
        self.assertEqual(self.links["COURSE-007"]["record_ids"], expected)
        self.assertEqual([len(record["modules"]) for record in self.cookery], [11, 26, 19, 49])

    def test_step_19b_pdf_hashes_are_pinned(self):
        expected = {
            "IN-DGT-CTS-BAKER-V2": "a203db963d1e27dd212a4d47620ffccd3e2472d24435d5a65d79b44020fe38b7",
            "SG-ITE-HNITEC-PASTRY-2Y": "ae91007ed283a413cddc702cc92229adcf8ce7a0f132c525564629a7671334d4",
            "AU-TGA-FBP30521": "8cc99cb2926c409e149b722cda93e764e5536eab85a8c48d7f9dcf4e941741f0",
            "IN-DGT-CTS-FOOD-PROD-V2": "74cf6cb0424666f510f24f266518f40ff24930571ac0bc99b7bc24a707e30c06",
            "PH-TESDA-PRO-COOKERY-NC3": "f546571e3b3a37cf430458b22976536c7123eee78190b7ed4174734f249ecd4d",
            "SG-ITE-HNITEC-CULINARY-2Y": "a5819f2de4c6df6454c354eb3e8e1b7fcd0696089158f804068b244c12a2cf30",
            "AU-TGA-SIT30821": "3d03daee227fb60dc26df9ef62132b4ae0470209d7ca8b07e37a4e33a9bd0c43",
        }
        records = {record["record_id"]: record for record in self.baker + self.cookery}
        self.assertEqual({rid: records[rid]["source"]["document_sha256"] for rid in expected}, expected)

    def test_ite_baker_inconsistent_electives_are_excluded(self):
        ite = next(record for record in self.baker if record["record_id"] == "SG-ITE-HNITEC-PASTRY-2Y")
        self.assertFalse(any(module["group"].startswith("Elective") for module in ite["modules"]))
        self.assertTrue(any("disagree" in note for note in ite["notes"]))

    def test_national_qualifications_are_not_presented_as_delivered_programmes(self):
        for record_id in ("AU-TGA-FBP30521", "PH-TESDA-PRO-COOKERY-NC3", "AU-TGA-SIT30821"):
            record = next(record for record in self.baker + self.cookery if record["record_id"] == record_id)
            self.assertFalse(record["delivering_provider_verified"])
            self.assertNotEqual(record["record_type"], "programme")


if __name__ == "__main__":
    unittest.main()
