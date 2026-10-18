"""Focused offline checks for Step 29 ICT diploma, networking and computer-based accounting evidence."""

from __future__ import annotations

import json
import unittest
from pathlib import Path

BASE = Path(__file__).resolve().parents[2]
BENCH = BASE / "outputs/programme_benchmarking"
NEW = {
    "ict_diploma": ["LK-TVEC-NCS-ICT-L5-2025"],
    "networking": ["LK-TVEC-NCS-COMPUTER-SYSTEMS-NETWORK-2026", "AU-TGA-ICT40120-NETWORKING"],
    "computer_accounting": ["IN-NQR-HARTRON-COMPUTER-ACCOUNTING-V2", "AU-TGA-FNS30322", "SG-ITE-HNITEC-ACCOUNTING-2Y"],
}
LINKS = {
    "COURSE-006": ["LK-TVEC-NCS-ICT-L5-2025", "SG-ITE-HNITEC-ITAD-2Y", "SG-ITE-HNITEC-ISN-2Y"],
    "COURSE-022": ["LK-TVEC-NCS-COMPUTER-SYSTEMS-NETWORK-2026", "IN-DGT-CTS-CHNM-V2", "PH-TESDA-CSS-NC2",
                   "SG-ITE-HNITEC-ISN-2Y", "AU-TGA-ICT40120-NETWORKING"],
    "COURSE-052": ["LK-TVEC-NCS-COMPUTER-SYSTEMS-NETWORK-2026", "SG-ITE-HNITEC-ISN-2Y", "AU-TGA-ICT40120-NETWORKING"],
    "COURSE-058": ["IN-NQR-HARTRON-COMPUTER-ACCOUNTING-V2", "SG-ITE-HNITEC-ACCOUNTING-2Y", "AU-TGA-FNS30322"],
}


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


class Step29Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.datasets = {k: json.loads((BENCH / f"pilot_records_{k}.json").read_text(encoding="utf-8")) for k in NEW}
        cls.records = {r["record_id"]: r for p in BENCH.glob("pilot_records_*.json") for r in json.loads(p.read_text(encoding="utf-8"))["records"]}
        cls.links = {l["nysc_course_id"]: l for l in json.loads((BENCH / "course_comparator_links.json").read_text(encoding="utf-8"))["links"]}
        cls.register = {e["course_id"]: e for e in json.loads((BENCH / "coverage_register.json").read_text(encoding="utf-8"))["courses"]}

    def test_six_new_records_pending_human_review(self):
        for key, ids in NEW.items():
            self.assertEqual([r["record_id"] for r in self.datasets[key]["records"]], ids)
            for record in self.datasets[key]["records"]:
                with self.subTest(record=record["record_id"]):
                    self.assertEqual(record["verification"]["status"], "source_inspected_pending_human_review")
                    self.assertFalse(record["verification"]["human_reviewed"])
                    self.assertRegex(record["source"]["document_sha256"], r"^[0-9a-f]{64}$")
                    self.assertEqual(record["delivering_provider_verified"], record["record_type"] == "programme")

    def test_links_use_scope_appropriate_records_only(self):
        for course_id, ids in LINKS.items():
            self.assertEqual(self.links[course_id]["record_ids"], ids, course_id)
        # Level 3/4 technician and generic computer-applications records are not reused for the diploma or accounting.
        for general in ("LK-TVEC-NCS-ICT-TECH-L4-2023", "IN-DGT-CTS-COPA-V3", "AU-TGA-ICT20120", "LK-TVEC-NCS-COMPUTER-APP-ASSIST-L3-2023"):
            self.assertNotIn(general, LINKS["COURSE-006"] + LINKS["COURSE-058"])
        # CCNA links networking-focused records only, and is never presented as a national qualification.
        for hardware in ("IN-DGT-CTS-CHNM-V2", "PH-TESDA-CSS-NC2"):
            self.assertNotIn(hardware, LINKS["COURSE-052"])
        self.assertIn("vendor certification", self.links["COURSE-052"]["comparison_caveat"])
        self.assertFalse(any("cisco" in rid.lower() for rid in self.records))

    def test_coverage_states(self):
        for course_id, mode in (("COURSE-006", "FULL_COMPARISON"), ("COURSE-058", "FULL_COMPARISON"),
                                ("COURSE-022", "COMPARATORS_ONLY"), ("COURSE-052", "COMPARATORS_ONLY")):
            self.assertEqual(self.register[course_id]["current_presentation_mode"], mode, course_id)
        for course_id in ("COURSE-022", "COURSE-052"):
            self.assertFalse((BENCH / f"competency_mapping_{course_id.lower()}.json").exists())

    def test_course_006_matrix_and_areas(self):
        mapping = json.loads((BENCH / "competency_mapping_course-006.json").read_text(encoding="utf-8"))
        cited = sorted({e["module_index"] for c in mapping["competencies"] for e in c["cells"]["NYSC-COURSE-006"]["evidence"]})
        # Heading 7 ('Documents & Resource Level 5 -') is an uninterpretable fragment and is never cited.
        self.assertEqual(cited, [0, 1, 2, 3, 4, 5, 7, 8, 9, 10, 11])
        systems = {c["competency_id"]: c["cells"]["SG-ITE-HNITEC-ISN-2Y"] for c in mapping["competencies"]}
        self.assertEqual(systems["dip_networking"]["coverage"], "FULL")
        self.assertEqual([e["module_index"] for e in systems["dip_networking"]["evidence"]], [0])
        self.assertEqual(systems["dip_programming"]["coverage"], "PARTIAL")
        self.assertEqual(systems["dip_databases"]["status"], "NOT_EXPLICIT")
        self.assertEqual(areas(mapping, self.records), ["dip_mobile_apps"])

    def test_course_058_cites_only_software_and_project_headings(self):
        mapping = json.loads((BENCH / "competency_mapping_course-058.json").read_text(encoding="utf-8"))
        documented = {c["competency_id"]: c["cells"]["NYSC-COURSE-058"] for c in mapping["competencies"]
                      if c["cells"]["NYSC-COURSE-058"]["status"] == "DOCUMENTED"}
        self.assertEqual(sorted(documented), ["acc_project", "acc_software"])
        self.assertEqual([e["module_index"] for e in documented["acc_software"]["evidence"]], [0, 2])
        self.assertEqual(documented["acc_software"]["evidence"][1]["display_text"], "Quick Books Accounting Package")
        self.assertEqual(areas(mapping, self.records),
                         ["acc_transactions_ledgers", "acc_trial_balance_statements", "acc_bank_reconciliation", "acc_payroll", "acc_tax"])

    def test_gaps_and_exclusions_are_explained(self):
        self.assertEqual(set(self.datasets["computer_accounting"]["country_group_gaps"]), {"sri_lanka"})
        self.assertIn("G52T002", self.datasets["computer_accounting"]["country_group_gaps"]["sri_lanka"])
        self.assertIn("NIELIT", self.datasets["ict_diploma"]["country_group_gaps"]["developing_emerging"])
        net = self.records["LK-TVEC-NCS-COMPUTER-SYSTEMS-NETWORK-2026"]
        self.assertTrue(any("K72S002" in n for n in net["notes"]))


if __name__ == "__main__":
    unittest.main()
