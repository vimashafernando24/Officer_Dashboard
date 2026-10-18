"""Evidence checks for the curated programme competency mappings.

A DOCUMENTED cell must cite text that exists, character for character, in the
governed NYSC catalogue or the stored benchmarking record. Missing or
uncaptured curriculum text must never be reported as DOCUMENTED.
"""

from __future__ import annotations

import json
import unittest
from pathlib import Path

from src.rag_prototype.programme_design_evidence import load_governed_courses

BASE = Path(__file__).resolve().parents[2]
BENCHMARK_DIR = BASE / "outputs/programme_benchmarking"
MAPPING_PATHS = sorted(BENCHMARK_DIR.glob("competency_mapping_course-*.json"))
RECORD_PATHS = sorted(BENCHMARK_DIR.glob("pilot_records_*.json"))
SNAPSHOT_PATH = BASE / "src/rag_prototype/frontend/src/data/nyscCourseCatalogue.json"
LINKS_PATH = BENCHMARK_DIR / "course_comparator_links.json"

STATUSES = {"DOCUMENTED", "NOT_EXPLICIT", "INSUFFICIENT_DATA"}

# Guards against a citation pointing at the wrong module: every cited text
# must name its competency in at least one of these word stems.
COMPETENCY_KEYWORDS = {
    "engine_systems": ["engine"],
    # CGTTI publishes gearboxes rather than the word "transmission" on its chassis lines.
    "transmission_drivetrain": ["transmission", "drivetrain", "gearbox"],
    "steering": ["steering"],
    # NYSC publishes its brake module as "Breaking System"; the misspelling is
    # accepted deliberately and the mapping cell records it in its note.
    "brakes": ["brak", "breaking system"],
    "suspension": ["suspension"],
    "vehicle_electrical": ["electric"],
    "starting_charging": ["start", "charg", "alternator"],
    # "electronic" admits CGTTI's electronic ignition / injection lines, which are PARTIAL support only.
    "engine_management": ["electronic control", "management", "electronic"],
    "emission_control": ["emission"],
    "fault_diagnosis": ["diagnos", "fault", "defect"],
    "high_voltage_ev": ["high voltage", "electric vehicle"],
    "workplace_safety": ["safe", "whs", "hazard"],
    # Electrician categories.
    "principles_circuits": ["principle", "circuit"],
    "domestic_wiring": ["domestic", "residential", "single-phase", "outlets"],
    "industrial_installation": ["industrial", "commercial", "three-phase"],
    "protection_earthing": ["protect", "earthing", "switchboard", "circuit breaker"],
    "motors_control": ["motor", "rotating machine", "machines"],
    "generators_transformers": ["generator", "alternator", "transformer"],
    "rewinding": ["winding"],
    "plc": ["plc", "p.l.c", "programmable"],
    "testing_fault_finding": ["test", "inspect", "fault", "measuring"],
    "solar_batteries_ev": ["solar", "batter", "electric vehicle"],
    "security_building": ["alarm", "security", "building"],
    "electrical_safety": ["safe", "whs"],
    # Refrigeration and air-conditioning categories. NYSC publishes "Refigerators".
    "refrigeration_cycle_components": ["cycle", "vapo", "compon", "compressor", "condenser", "evaporator", "expansion", "drier"],
    "psychrometrics_load": ["psych", "load"],
    "refrigerants_environment": ["recover", "recycl", "refrigerant", "environment", "ozone"],
    "pipework_brazing": ["tub", "pipe", "braz"],
    "leak_evacuation_charging": ["leak", "vacuum", "evacuat", "charg"],
    "domestic_refrigeration": ["domestic", "refrigerator", "refigerator", "freezer", "cooler"],
    "commercial_refrigeration": ["commercial", "industrial", "cold", "ice", "temperature", "display unit"],
    "ac_installation": ["install"],
    "ac_servicing_repair": ["servic", "repair", "maintain", "rectify"],
    "central_ducted_ac": ["central", "dx", "chill", "a.h.u", "duct", "vrv", "vrf", "air distribution", "fcu"],
    "electrical_motors_controls": ["electric", "motor", "control", "wiring", "circuit", "current"],
    "fault_diagnosis_testing": ["diagnos", "fault", "troubleshoot", "trouble shoot"],
    "cost_estimating": ["estimat"],
    # Computer hardware categories. NYSC publishes "Maintence".
    "pc_assembly": ["assembl"],
    "device_installation": ["device", "peripheral", "printer", "scanner"],
    "software_installation": ["software", "operating system"],
    "troubleshooting_repair": ["troubl", "repair", "fault"],
    "computer_maintenance": ["mainten", "maintain", "maintence"],
    "laptop_servicing": ["laptop"],
    "networking": ["network"],
    "server_setup": ["server"],
    "internet_email": ["internet", "email", "e-mail", "digital technologies"],
    "power_electronics": ["power suppl", "smps", "electronic"],
    "network_security": ["security", "attack", "firewall"],
    # Baker categories.
    "bread_products": ["bread"],
    "cake_products": ["cake"],
    "pastry_products": ["pastr"],
    "bakery_management": ["management", "schedule", "menu"],
    "food_safety_hygiene": ["food safety", "food handling", "hygiene", "cleanliness", "cleaning"],
    "artisan_bread": ["artisan", "bread"],
    "biscuits_cookies": ["biscuit", "cookie"],
    "chocolate_confectionery": ["chocolate", "cand", "confection"],
    "desserts_puddings": ["dessert", "pudding"],
    # Cake Decorator categories. NYSC publishes "Oicing Methods".
    "icing_methods": ["icing", "oicing"],
    "cake_decoration": ["decorat", "icing"],
    "icing_structures": ["icing structure"],
    "occasion_specialty_cakes": ["birthday cake", "wedding cake", "engagement cake", "eggless cake", "homecoming cake", "gateau", "advanced cake", "special types of cakes", "mousse cakes"],
    "basic_advanced_cake_production": ["cake"],
    "cake_outer_covering": ["cover cake", "icing", "decorative work"],
    "cake_food_safety_hygiene": ["food handling", "hygiene", "food safety"],
    "customer_led_cake_design": ["customer", "cake design"],
    "cake_business_operations": ["routine functions", "menu", "promotional"],
    # Professional Cookery categories.
    "menu_planning": ["menu", "recipe", "cost", "budget"],
    "regional_cuisines": ["cuisine", "indian", "continental", "chinese", "asian", "western"],
    "vegetable_egg_farinaceous": ["vegetable", "egg", "farinaceous", "fairnaceous", "starch"],
    "fish_meat_poultry": ["fish", "seafood", "meat", "poultry"],
    "beverages": ["beverage", "wine", "juice"],
    "stocks_sauces_soups_salads": ["stock", "sauce", "sause", "soup", "salad", "garde manger"],
    "desserts_sweets": ["dessert", "sweet", "patisserie"],
    "kitchen_management": ["cost", "stock", "inventory", "menu", "budget"],
    # Beautician categories.
    "facial_skin_care": ["facial", "skin care", "skin-care"],
    "manicure_pedicure": ["manicure", "menicure", "pedicure", "pedicare", "nail care", "nailcare"],
    "makeup_services": ["make-up", "make up", "makeup"],
    "bridal_beauty": ["bridal"],
    "hair_removal": ["hair removal", "superfluous hair", "epilation", "depilation", "waxing"],
    "client_consultation": ["client consultation"],
    "salon_hygiene_safety": ["health and safety", "safe hygiene", "occupational safety"],
    "salon_management": ["manage a beauty salon", "customer", "salon services"],
    # Hairdresser categories.
    "hair_straightening": ["straighten", "straightening", "relaxing"],
    "hair_colouring": ["colour", "color"],
    "hair_styling_setting": ["styling", "stylist", "setting", "dress hair", "hair designs"],
    "hair_scalp_treatment": ["hair and scalp", "hair treatment"],
    "hair_perming": ["perm", "curl and volumise"],
    "hair_cutting": ["haircut", "hair cutting", "cut and set"],
    "hair_client_consultation": ["consultation"],
    "hair_salon_safety": ["health and safety", "safe hygiene", "occupational safety"],
    "hair_salon_management": ["manage hairdressing salon", "customer service", "salon services"],
    # Secretary categories.
    "office_management": ["manage the office", "managing office", "office layout", "office administration", "business administrative", "business resources", "role of a secretary"],
    "meeting_coordination": ["meeting"],
    "filing_records": ["fil", "records"],
    "mail_handling": ["mail", "postal", "dispatch"],
    "business_correspondence": ["correspond", "corrspond", "business documents"],
    "office_software": ["word", "software", "automation"],
    "travel_arrangements": ["travel", "tickets", "hotels"],
    "workplace_communication": ["communication", "relationships", "communicating"],
    "diary_appointments": ["diary", "appointments", "schedules"],
    # ICT Technician and computer applications categories (Step 23).
    "ict_file_management": ["file", "folder"],
    "ict_word_processing": ["word processing", "document"],
    "ict_spreadsheets": ["spreadsheet", "workbook"],
    "ict_presentations": ["presentation", "slides"],
    "ict_databases": ["database", "sql", "mysql"],
    "ict_internet_email": ["internet", "e-mail", "email", "electronic mail", "e-commerce"],
    "ict_os_installation": ["operating system", "system software"],
    "ict_os_use": ["operating system", "computer"],
    "ict_networking": ["network"],
    "ict_graphics_multimedia": ["graphic", "print", "multimedia", "digital media"],
    "ict_web_design": ["web"],
    "ict_software_development": ["program", "software", "information system", "script"],
    "ict_system_maintenance": ["mainten", "maintain", "troubleshoot", "hardware"],
    "ict_information_security": ["secur", "firewall", "intrusion", "cryptograph"],
    "ict_workplace_safety": ["safety"],
    "ict_office_applications": ["office", "word processing", "spreadsheet", "workbook", "presentation", "application software"],
    # Web design and development categories (Step 24).
    "web_html": ["html", "markup"],
    "web_css": ["css", "style"],
    "web_javascript": ["javascript", "java script"],
    "web_forms_email": ["form", "email"],
    "web_responsive": ["responsive", "mobile layout"],
    "web_hosting_maintenance": ["host", "maint", "deploy", "publish", "server", "transfer content"],
    "web_design_ux": ["design", "user experience", "ux", "layout", "interface"],
    "web_backend": ["back-end", "backend", "server-side", "server side"],
    "web_databases": ["database"],
    "web_cms": ["cms", "content management"],
    "web_seo": ["search engine", "seo"],
    "web_testing": ["test", "accessibility"],
    "web_security": ["secur"],
    "web_requirements_methodology": ["requirement", "methodolog", "software development"],
    "web_workplace_safety": ["safety"],
    # Step 29: National Diploma in ICT (COURSE-006).
    "dip_analysis_design": ["analy", "requirement", "design"],
    "dip_programming": ["program", "software", "develop"],
    "dip_databases": ["database"],
    "dip_graphics": ["graphic", "print media"],
    "dip_web": ["web"],
    "dip_testing": ["test"],
    "dip_networking": ["network"],
    "dip_workplace_information": ["information"],
    "dip_workplace_communication": ["communicat"],
    "dip_work_planning": ["plan", "schedul"],
    "dip_mobile_apps": ["mobile"],
    "dip_multimedia": ["multimedia"],
    # Step 29: Computer Based Accounting (COURSE-058).
    "acc_software": ["accounting package", "tally", "accounting software", "computerised accounting"],
    "acc_transactions_ledgers": ["journal", "ledger", "transaction"],
    "acc_trial_balance_statements": ["trial balance", "balance sheet", "profit", "financial statement", "report"],
    "acc_bank_reconciliation": ["bank reconciliation"],
    "acc_payroll": ["payroll"],
    "acc_tax": ["tax", "gst", "tds"],
    "acc_spreadsheets": ["spreadsheet"],
    "acc_project": ["project"],
    # Step 30: Radio, TV and allied equipment repair (COURSE-081).
    "rtv_display_optical_repair": ["tv", "television", "display", "monitor", "video", "optical", "dvd", "consumer electronic"],
    "rtv_basic_electronics": ["electric", "electronic", "component", "digital"],
    "rtv_microcontroller_led_programming": ["microcontroller", "program", "led", "processor", "control board", "programmable"],
    "rtv_fault_diagnosis": ["fault", "diagnos", "troubleshoot"],
    "rtv_component_board_repair": ["board", "pcb", "input", "output"],
    "rtv_audio_amplifier_repair": ["audio", "amplifier", "receiver", "home theatre", "consumer electronic"],
    "rtv_power_supply_repair": ["power supply", "smps", "ups", "inverter"],
    "rtv_workplace_safety": ["safe", "safety"],
    # Step 33: Desktop Publisher (COURSE-062).
    "desktop_publishing_pagemaker": ["pagemaker"],
    "desktop_publishing_photoshop": ["photoshop"],
    "desktop_publishing_indesign": ["indesign"],
    "desktop_publishing_illustrator": ["illustrator"],
    # Step 34: Tailor and Dress Making Without Blocks.
    "garment_women_children_clothing": ["women", "ladies", "children", "childrens", "blouse", "skirt", "frock"],
    "ecd_child_development": ["development"],
    "ecd_child_psychology": ["psychology"],
    "ecd_environment_exploration": ["environment", "science", "geography"],
    "ecd_learning_methods": ["learning", "teaching", "philosoph"],
    "ecd_health_safety": ["safety", "health"],
    "ecd_language_literacy": ["language", "literacy"],
    "ecd_creative_arts": ["aesthetic", "art", "music"],
    "ecd_inclusion": ["inclusi", "special needs"],
    "hr_recruitment_selection": ["recruit", "selection", "resourcing"],
    "hr_induction": ["induction", "onboarding"],
    "hr_discipline": ["ipline"],
    "hr_training_development": ["training", "learning", "development"],
    "hr_performance": ["performance"],
    "hr_employee_relations": ["relations"],
    "hr_welfare": ["welfare"],
    "hr_labour_law": ["labour law"],
    "hr_payroll_records": ["payroll", "records", "information system", "hr operations", "human resource functions"],
    "hr_whs": ["safety", "whs"],
}

# Hardware categories with several components: a FULL cell's cited text must name every one.
HW_COMPONENT_KEYWORDS = {
    "troubleshooting_repair": [["troubl", "fault", "diagnos"], ["repair"]],
    "power_electronics": [["power suppl", "smps"], ["electronic"]],
}
HW_IDS = ["IN-DGT-CTS-CHNM-V2", "PH-TESDA-CSS-NC2", "SG-ITE-HNITEC-ISN-2Y"]

# RAC categories with several components: a FULL cell's cited text must name every one.
RAC_COMPONENT_KEYWORDS = {
    "refrigeration_cycle_components": [["cycle", "vapo"], ["compon", "compressor", "condenser", "evaporator", "expansion", "drier"]],
    "psychrometrics_load": [["psych"], ["load"]],
    "refrigerants_environment": [["recover", "recycl"], ["environment", "ozone"]],
    "pipework_brazing": [["tub", "pipe"], ["braz", "solder"]],
    "leak_evacuation_charging": [["leak"], ["vacuum", "evacuat"], ["charg"]],
    "electrical_motors_controls": [["electric", "wiring", "circuit", "current"], ["motor"], ["control", "starter", "relay"]],
}
RAC_IDS = ["LK-CGTTI-RAC-MECH", "IN-DGT-CTS-RAC-V2", "PH-TESDA-DOMRAC-NC2", "PH-TESDA-CAC-NC3", "AU-TGA-UEE32225"]


class CompetencyMappingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.mappings = {
            path.name: json.loads(path.read_text(encoding="utf-8")) for path in MAPPING_PATHS
        }
        cls.records = {
            record["record_id"]: record
            for path in RECORD_PATHS
            for record in json.loads(path.read_text(encoding="utf-8"))["records"]
        }
        cls.corrections = {
            (course["course_id"], correction["module_index"]): correction["displayed"]
            for course in json.loads(SNAPSHOT_PATH.read_text(encoding="utf-8"))["courses"]
            for correction in course["module_display_corrections"]
        }
        cls.links = {
            link["nysc_course_id"]: link["record_ids"]
            for link in json.loads(LINKS_PATH.read_text(encoding="utf-8"))["links"]
        }
        cls.courses = {course["course_id"]: course for course in load_governed_courses()}

    def source_modules(self, column):
        if column["kind"] == "nysc":
            return [
                {"title_verbatim": title, "outcome_verbatim": None, "code": None}
                for title in self.courses[column["nysc_course_id"]]["modules"]
            ]
        return self.records[column["record_id"]]["modules"]

    def cells(self):
        for mapping in self.mappings.values():
            columns = {column["column_id"]: column for column in mapping["columns"]}
            for competency in mapping["competencies"]:
                for column_id, cell in competency["cells"].items():
                    yield competency, columns[column_id], cell

    def nysc_status(self, course_id, competency_id):
        mapping = self.mappings[f"competency_mapping_{course_id.lower()}.json"]
        competency = next(c for c in mapping["competencies"] if c["competency_id"] == competency_id)
        return competency["cells"][f"NYSC-{course_id}"]["status"]

    def test_expected_mappings_exist_one_per_course(self):
        self.assertEqual(
            sorted(self.mappings),
            [
                "competency_mapping_course-005.json",
                "competency_mapping_course-006.json",
                "competency_mapping_course-007.json",
                "competency_mapping_course-008.json",
                "competency_mapping_course-009.json",
                "competency_mapping_course-010.json",
                "competency_mapping_course-011.json",
                "competency_mapping_course-012.json",
                "competency_mapping_course-014.json",
                "competency_mapping_course-025.json",
                "competency_mapping_course-034.json",
                "competency_mapping_course-035.json",
                "competency_mapping_course-037.json",
                "competency_mapping_course-040.json",
                "competency_mapping_course-041.json",
                "competency_mapping_course-046.json",
                "competency_mapping_course-047.json",
                "competency_mapping_course-050.json",
                "competency_mapping_course-053.json",
                "competency_mapping_course-055.json",
                "competency_mapping_course-058.json",
                "competency_mapping_course-062.json",
                "competency_mapping_course-063.json",
                "competency_mapping_course-064.json",
                "competency_mapping_course-071.json",
                "competency_mapping_course-081.json",
                "competency_mapping_course-082.json",
                "competency_mapping_course-087.json",
            ],
        )
        course_ids = [mapping["nysc_course_id"] for mapping in self.mappings.values()]
        self.assertEqual(len(course_ids), len(set(course_ids)))

    def test_columns_are_the_course_and_exactly_its_linked_records(self):
        for name, mapping in self.mappings.items():
            with self.subTest(mapping=name):
                course_id = mapping["nysc_course_id"]
                self.assertIn(course_id, self.courses)
                nysc_columns = [c for c in mapping["columns"] if c["kind"] == "nysc"]
                self.assertEqual([c["nysc_course_id"] for c in nysc_columns], [course_id])
                record_columns = [c["record_id"] for c in mapping["columns"] if c["kind"] == "benchmark"]
                self.assertEqual(record_columns, self.links[course_id])
                self.assertTrue(set(record_columns) <= set(self.records))

    def test_every_competency_has_one_valid_cell_per_column(self):
        for name, mapping in self.mappings.items():
            competencies = mapping["competencies"]
            # A matrix follows the usable governed headings; garment courses may have one.
            self.assertTrue(1 <= len(competencies) <= 15)
            self.assertEqual(len({c["competency_id"] for c in competencies}), len(competencies))
            column_ids = [column["column_id"] for column in mapping["columns"]]
            for competency in competencies:
                with self.subTest(mapping=name, competency=competency["competency_id"]):
                    self.assertEqual(list(competency["cells"]), column_ids)
                    for cell in competency["cells"].values():
                        self.assertIn(cell["status"], STATUSES)

    def test_every_documented_cell_cites_exact_source_text(self):
        for competency, column, cell in self.cells():
            if cell["status"] != "DOCUMENTED":
                continue
            with self.subTest(competency=competency["competency_id"], column=column["column_id"]):
                self.assertTrue(cell["evidence"])
                modules = self.source_modules(column)
                for evidence in cell["evidence"]:
                    self.assertIn(evidence["field"], {"title_verbatim", "outcome_verbatim", "scope_verbatim"})
                    if evidence["field"] == "scope_verbatim":
                        # Scope citations quote the record's verified qualification scope.
                        self.assertEqual(column["kind"], "benchmark")
                        scope = self.records[column["record_id"]].get("scope_verbatim") or []
                        self.assertEqual(evidence["text"], scope[evidence["module_index"]])
                        self.assertIsNone(evidence["code"])
                        continue
                    module = modules[evidence["module_index"]]
                    self.assertEqual(evidence["text"], module[evidence["field"]])
                    self.assertEqual(evidence["code"], module["code"])

    def test_documented_cells_record_full_or_partial_coverage(self):
        for competency, column, cell in self.cells():
            with self.subTest(competency=competency["competency_id"], column=column["column_id"]):
                if cell["status"] == "DOCUMENTED":
                    self.assertIn(cell["coverage"], {"FULL", "PARTIAL"})
                    if cell["coverage"] == "PARTIAL":
                        self.assertTrue(cell["supported_component"].strip())
                    else:
                        self.assertNotIn("supported_component", cell)
                else:
                    self.assertNotIn("coverage", cell)
                    self.assertNotIn("supported_component", cell)

    def test_methodology_and_components_are_documented(self):
        for name, mapping in self.mappings.items():
            with self.subTest(mapping=name):
                methodology = mapping["methodology"]
                for key in ("FULL", "PARTIAL", "NOT_EXPLICIT", "INSUFFICIENT_DATA", "caution", "areas_rule"):
                    self.assertTrue(methodology[key].strip())
                self.assertIn("does not prove", methodology["caution"].replace("None of these statuses proves", "does not prove"))
                self.assertEqual(
                    set(mapping["category_components"]),
                    {c["competency_id"] for c in mapping["competencies"]},
                )

    def test_cited_text_names_its_competency(self):
        for competency, column, cell in self.cells():
            for evidence in cell["evidence"]:
                with self.subTest(competency=competency["competency_id"], column=column["column_id"]):
                    keywords = COMPETENCY_KEYWORDS[competency["competency_id"]]
                    shown = evidence.get("display_text") or evidence["text"]
                    self.assertTrue(any(k in shown.casefold() for k in keywords))

    def test_only_documented_cells_carry_evidence_and_others_explain_why(self):
        for competency, column, cell in self.cells():
            if cell["status"] == "DOCUMENTED":
                continue
            with self.subTest(competency=competency["competency_id"], column=column["column_id"]):
                self.assertEqual(cell["evidence"], [])
                self.assertTrue((cell["note"] or "").strip())

    def test_uncaptured_curriculum_is_never_documented(self):
        for competency, column, cell in self.cells():
            if column["kind"] != "benchmark":
                continue
            record = self.records[column["record_id"]]
            if not record["modules"] or record["content_fidelity"] == "paraphrased_needs_manual_copy":
                with self.subTest(competency=competency["competency_id"], column=column["column_id"]):
                    self.assertEqual(cell["status"], "INSUFFICIENT_DATA")

    def test_scope_limited_flags_appear_only_on_rac_tesda_evidence(self):
        for competency, column, cell in self.cells():
            if cell.get("scope_limited"):
                with self.subTest(competency=competency["competency_id"], column=column["column_id"]):
                    self.assertIn(column["column_id"], {"PH-TESDA-DOMRAC-NC2", "PH-TESDA-CAC-NC3"})
                    self.assertEqual(cell["status"], "DOCUMENTED")
                    self.assertTrue((cell["note"] or "").strip())

    def test_mapping_is_not_marked_as_human_reviewed(self):
        for name, mapping in self.mappings.items():
            with self.subTest(mapping=name):
                self.assertFalse(mapping["human_reviewed"])

    def test_shared_comparator_cells_are_identical_across_courses(self):
        by_course = {m["nysc_course_id"]: m for m in self.mappings.values()}
        for left, right in (("COURSE-005", "COURSE-040"), ("COURSE-025", "COURSE-064"), ("COURSE-034", "COURSE-012"), ("COURSE-008", "COURSE-055"), ("COURSE-011", "COURSE-047"), ("COURSE-010", "COURSE-046"), ("COURSE-035", "COURSE-082")):
            first, second = by_course[left], by_course[right]
            self.assertEqual(
                [c["competency_id"] for c in first["competencies"]],
                [c["competency_id"] for c in second["competencies"]],
            )
            for a, b in zip(first["competencies"], second["competencies"]):
                for column in first["columns"]:
                    if column["kind"] != "benchmark":
                        continue
                    with self.subTest(pair=left, competency=a["competency_id"], column=column["column_id"]):
                        self.assertEqual(a["cells"][column["column_id"]], b["cells"][column["column_id"]])

    def test_display_text_matches_the_approved_snapshot_correction(self):
        for competency, column, cell in self.cells():
            for evidence in cell["evidence"]:
                with self.subTest(competency=competency["competency_id"], column=column["column_id"]):
                    if column["kind"] != "nysc":
                        self.assertNotIn("display_text", evidence)
                        continue
                    key = (column["nysc_course_id"], evidence["module_index"])
                    if key in self.corrections:
                        # A corrected heading is cited by its governed text plus the correction.
                        self.assertEqual(evidence.get("display_text"), self.corrections[key])
                    else:
                        self.assertNotIn("display_text", evidence)

    def test_electrician_nysc_columns_follow_each_course_s_own_headings(self):
        expected = {
            "domestic_wiring": "DOCUMENTED",
            "industrial_installation": "DOCUMENTED",
            "motors_control": "DOCUMENTED",
            "generators_transformers": "DOCUMENTED",
            "plc": "DOCUMENTED",
            "security_building": "INSUFFICIENT_DATA",
            "rewinding": "NOT_EXPLICIT",
            "testing_fault_finding": "NOT_EXPLICIT",
            "electrical_safety": "NOT_EXPLICIT",
            "principles_circuits": "NOT_EXPLICIT",
            "protection_earthing": "NOT_EXPLICIT",
            "solar_batteries_ev": "NOT_EXPLICIT",
        }
        for course_id in ("COURSE-025", "COURSE-064"):
            for competency_id, status in expected.items():
                with self.subTest(course=course_id, competency=competency_id):
                    self.assertEqual(self.nysc_status(course_id, competency_id), status)

    def comparator_cell(self, course_id, competency_id, record_id):
        mapping = self.mappings[f"competency_mapping_{course_id.lower()}.json"]
        competency = next(c for c in mapping["competencies"] if c["competency_id"] == competency_id)
        return competency["cells"][record_id]

    def test_audit_corrections_are_applied(self):
        for course_id in ("COURSE-025", "COURSE-064"):
            with self.subTest(course=course_id):
                cgtti = self.comparator_cell(course_id, "testing_fault_finding", "LK-CGTTI-POWER-ELEC")
                self.assertEqual(cgtti["status"], "NOT_EXPLICIT")
                dgt = self.comparator_cell(course_id, "testing_fault_finding", "IN-DGT-CTS-ELEC-V3")
                self.assertEqual([e["code"] for e in dgt["evidence"]], ["PSS/N9501"])
                ite_safety = self.comparator_cell(course_id, "electrical_safety", "SG-ITE-HNITEC-ELEC-2Y")
                self.assertEqual(ite_safety["status"], "INSUFFICIENT_DATA")
                self.assertEqual(self.nysc_status(course_id, "security_building"), "INSUFFICIENT_DATA")
        for course_id in ("COURSE-005", "COURSE-040"):
            with self.subTest(course=course_id):
                ite = self.comparator_cell(course_id, "engine_management", "SG-ITE-HNITEC-AUTO-2Y")
                self.assertEqual(ite["status"], "NOT_EXPLICIT")
                self.assertIn("emission control", ite["note"])
                dgt = self.comparator_cell(course_id, "vehicle_electrical", "IN-DGT-CTS-MMV-V2")
                self.assertEqual([e["module_index"] for e in dgt["evidence"]], [22])

    def test_cgtti_automotive_column_assessed_from_its_captured_curriculum(self):
        expected = {
            "engine_systems": ("DOCUMENTED", "FULL"),
            "transmission_drivetrain": ("DOCUMENTED", "FULL"),
            "steering": ("DOCUMENTED", "FULL"),
            "brakes": ("DOCUMENTED", "FULL"),
            "suspension": ("DOCUMENTED", "FULL"),
            "vehicle_electrical": ("DOCUMENTED", "FULL"),
            "starting_charging": ("DOCUMENTED", "FULL"),
            "engine_management": ("DOCUMENTED", "PARTIAL"),
            "emission_control": ("DOCUMENTED", "FULL"),
            "fault_diagnosis": ("DOCUMENTED", "PARTIAL"),
            "high_voltage_ev": ("NOT_EXPLICIT", None),
            "workplace_safety": ("DOCUMENTED", "FULL"),
        }
        cells = {}
        for course_id in ("COURSE-005", "COURSE-040"):
            for competency_id, (status, coverage) in expected.items():
                cell = self.comparator_cell(course_id, competency_id, "LK-CGTTI-AUTO-TECH")
                with self.subTest(course=course_id, competency=competency_id):
                    self.assertEqual(cell["status"], status)
                    self.assertEqual(cell.get("coverage"), coverage)
                cells.setdefault(competency_id, []).append(cell)
        # Both automotive courses reference the same published programme.
        for competency_id, pair in cells.items():
            self.assertEqual(pair[0], pair[1], competency_id)
        self.assertIn("engine management is not named", cells["engine_management"][0]["supported_component"])

    def test_dgt_automotive_ev_evidence_is_awareness_level_only(self):
        for course_id in ("COURSE-005", "COURSE-040"):
            cell = self.comparator_cell(course_id, "high_voltage_ev", "IN-DGT-CTS-MMV-V2")
            self.assertEqual(cell["coverage"], "PARTIAL")
            self.assertIn("Awareness/identification", cell["supported_component"])
            self.assertIn("not high-voltage servicing", cell["supported_component"])

    def test_tesda_scope_evidence_supports_residential_and_industrial_cells(self):
        for course_id in ("COURSE-025", "COURSE-064"):
            nc2 = self.comparator_cell(course_id, "domestic_wiring", "PH-TESDA-EIM-NC2")
            nc3 = self.comparator_cell(course_id, "industrial_installation", "PH-TESDA-EIM-NC3")
            self.assertIn("residential houses/buildings", nc2["evidence"][0]["text"])
            self.assertEqual(nc2["evidence"][0]["field"], "scope_verbatim")
            self.assertIn("Industrial Electrician", nc3["evidence"][0]["text"])
            self.assertEqual(nc3["evidence"][0]["field"], "scope_verbatim")
            self.assertEqual((nc2["coverage"], nc3["coverage"]), ("FULL", "FULL"))

    def test_electrician_courses_cite_their_own_heading_positions(self):
        def evidence(course_id, competency_id):
            mapping = self.mappings[f"competency_mapping_{course_id.lower()}.json"]
            competency = next(c for c in mapping["competencies"] if c["competency_id"] == competency_id)
            return competency["cells"][f"NYSC-{course_id}"]["evidence"][0]

        # COURSE-025's Domestic heading is contaminated and corrected; COURSE-064's is clean.
        d025, d064 = evidence("COURSE-025", "domestic_wiring"), evidence("COURSE-064", "domestic_wiring")
        self.assertEqual((d025["module_index"], d025["display_text"]), (4, "Domestic Electrical Installation"))
        self.assertEqual((d064["module_index"], d064["text"]), (0, "Domestic Electrical Installation"))
        self.assertNotIn("display_text", d064)
        for course_id, index in (("COURSE-025", 1), ("COURSE-064", 2)):
            industrial = evidence(course_id, "industrial_installation")
            self.assertEqual(industrial["module_index"], index)
            self.assertNotEqual(industrial["text"], industrial["display_text"])

    def test_nysc_columns_are_assessed_independently(self):
        # COURSE-040 publishes "Suspension System" and no "Electrical System" heading;
        # COURSE-005 is the reverse.
        self.assertEqual(self.nysc_status("COURSE-040", "suspension"), "DOCUMENTED")
        self.assertEqual(self.nysc_status("COURSE-040", "vehicle_electrical"), "NOT_EXPLICIT")
        self.assertEqual(self.nysc_status("COURSE-005", "suspension"), "NOT_EXPLICIT")
        self.assertEqual(self.nysc_status("COURSE-005", "vehicle_electrical"), "DOCUMENTED")
        # A broad engine heading never establishes engine management in either course.
        for course_id in ("COURSE-005", "COURSE-040"):
            self.assertEqual(self.nysc_status(course_id, "engine_management"), "NOT_EXPLICIT")

    def test_course_040_engine_evidence_is_its_own_heading(self):
        mapping = self.mappings["competency_mapping_course-040.json"]
        engine = next(c for c in mapping["competencies"] if c["competency_id"] == "engine_systems")
        evidence = engine["cells"]["NYSC-COURSE-040"]["evidence"]
        self.assertEqual([e["text"] for e in evidence], ["Overhead Engine (Petrol and Diesel)"])


class RacCompetencyMappingTests(unittest.TestCase):
    """The RAC matrices for COURSE-034 and COURSE-012 (Step 14E)."""

    NYSC_EXPECTED = {
        "refrigeration_cycle_components": ("NOT_EXPLICIT", None, None),
        "psychrometrics_load": ("NOT_EXPLICIT", None, None),
        "refrigerants_environment": ("NOT_EXPLICIT", None, None),
        "pipework_brazing": ("NOT_EXPLICIT", None, None),
        "leak_evacuation_charging": ("NOT_EXPLICIT", None, None),
        "domestic_refrigeration": ("DOCUMENTED", "FULL", 0),
        "commercial_refrigeration": ("DOCUMENTED", "PARTIAL", 0),
        "ac_installation": ("NOT_EXPLICIT", None, None),
        "ac_servicing_repair": ("DOCUMENTED", "FULL", 2),
        "central_ducted_ac": ("DOCUMENTED", "FULL", 3),
        "electrical_motors_controls": ("NOT_EXPLICIT", None, None),
        "fault_diagnosis_testing": ("NOT_EXPLICIT", None, None),
        "cost_estimating": ("DOCUMENTED", "FULL", 1),
        "workplace_safety": ("NOT_EXPLICIT", None, None),
    }
    # (status, coverage) per comparator, in RAC_IDS order, from the Step 14D audit.
    D, P, N = ("DOCUMENTED", "FULL"), ("DOCUMENTED", "PARTIAL"), ("NOT_EXPLICIT", None)
    COMPARATOR_EXPECTED = {
        "refrigeration_cycle_components": [D, P, N, N, P],
        "psychrometrics_load": [D, P, N, N, N],
        "refrigerants_environment": [D, D, N, P, D],
        "pipework_brazing": [D, D, N, N, P],
        "leak_evacuation_charging": [N, D, N, N, P],
        "domestic_refrigeration": [D, D, D, N, N],
        "commercial_refrigeration": [D, D, N, N, D],
        "ac_installation": [D, D, D, D, D],
        "ac_servicing_repair": [D, D, D, D, D],
        "central_ducted_ac": [P, D, N, N, P],
        "electrical_motors_controls": [P, D, P, P, D],
        "fault_diagnosis_testing": [D, D, D, D, D],
        "cost_estimating": [D, N, N, N, N],
        "workplace_safety": [D, D, D, D, D],
    }

    @classmethod
    def setUpClass(cls):
        cls.mappings = {
            course_id: json.loads((BENCHMARK_DIR / f"competency_mapping_{course_id.lower()}.json").read_text(encoding="utf-8"))
            for course_id in ("COURSE-034", "COURSE-012")
        }
        cls.governed = {course["course_id"]: course["modules"] for course in load_governed_courses()}

    def rows(self, course_id):
        return {c["competency_id"]: c for c in self.mappings[course_id]["competencies"]}

    def test_fourteen_rows_in_the_approved_order(self):
        for course_id, mapping in self.mappings.items():
            with self.subTest(course=course_id):
                self.assertEqual([c["competency_id"] for c in mapping["competencies"]], list(self.NYSC_EXPECTED))
                self.assertEqual([c["record_id"] for c in mapping["columns"][1:]], RAC_IDS)
                self.assertFalse(mapping["human_reviewed"])
                self.assertIn("two different countries", mapping["methodology"]["areas_rule"])

    def test_nysc_columns_cite_each_course_s_own_headings(self):
        for course_id in self.mappings:
            for competency_id, (status, coverage, index) in self.NYSC_EXPECTED.items():
                cell = self.rows(course_id)[competency_id]["cells"][f"NYSC-{course_id}"]
                with self.subTest(course=course_id, competency=competency_id):
                    self.assertEqual((cell["status"], cell.get("coverage")), (status, coverage))
                    if index is not None:
                        self.assertEqual([e["module_index"] for e in cell["evidence"]], [index])
                        self.assertEqual(cell["evidence"][0]["text"], self.governed[course_id][index])
        # COURSE-012 cites its governed (contaminated) headings 2 and 4 with the verified corrections.
        rows012, rows034 = self.rows("COURSE-012"), self.rows("COURSE-034")
        central = rows012["central_ducted_ac"]["cells"]["NYSC-COURSE-012"]["evidence"][0]
        self.assertEqual(central["text"], "Operate and Maintain Central A/C system gentle attitudes within a dis Screenshot unment.")
        self.assertEqual(central["display_text"], "Operate and Maintain Central A/C System")
        estimate = rows012["cost_estimating"]["cells"]["NYSC-COURSE-012"]["evidence"][0]
        self.assertEqual((estimate["text"], estimate["display_text"]), ("Prepare Estimates course which will be held on weekends.", "Prepare Estimates"))
        for competency_id in ("central_ducted_ac", "cost_estimating"):
            evidence = rows034[competency_id]["cells"]["NYSC-COURSE-034"]["evidence"][0]
            self.assertNotIn("display_text", evidence)
        self.assertEqual(rows034["central_ducted_ac"]["cells"]["NYSC-COURSE-034"]["evidence"][0]["text"], "Operate and Maintain Central A/C System")

    def test_nysc_commercial_refrigeration_is_partial(self):
        for course_id in self.mappings:
            cell = self.rows(course_id)["commercial_refrigeration"]["cells"][f"NYSC-{course_id}"]
            self.assertEqual(cell["coverage"], "PARTIAL")
            self.assertIn("display units, bottle coolers", cell["supported_component"])

    def test_comparator_cells_follow_the_audit(self):
        for course_id in self.mappings:
            for competency_id, expected in self.COMPARATOR_EXPECTED.items():
                cells = self.rows(course_id)[competency_id]["cells"]
                actual = [(cells[r]["status"], cells[r].get("coverage")) for r in RAC_IDS]
                with self.subTest(course=course_id, competency=competency_id):
                    self.assertEqual(actual, expected)

    def test_full_cells_name_every_component(self):
        for course_id in self.mappings:
            for competency_id, groups in RAC_COMPONENT_KEYWORDS.items():
                for column_id, cell in self.rows(course_id)[competency_id]["cells"].items():
                    if cell.get("coverage") != "FULL":
                        continue
                    text = " ".join((e.get("display_text") or e["text"]).casefold() for e in cell["evidence"])
                    with self.subTest(course=course_id, competency=competency_id, column=column_id):
                        for group in groups:
                            self.assertTrue(any(k in text for k in group), group)

    def test_scope_limits_and_accepted_evidence_are_noted(self):
        rows = self.rows("COURSE-034")
        for competency_id in ("ac_installation", "ac_servicing_repair", "fault_diagnosis_testing"):
            self.assertIn("window-type", rows[competency_id]["cells"]["PH-TESDA-DOMRAC-NC2"]["note"])
            self.assertIn("commercial air-conditioning units only", rows[competency_id]["cells"]["PH-TESDA-CAC-NC3"]["note"])
        uee_env = rows["refrigerants_environment"]["cells"]["AU-TGA-UEE32225"]
        self.assertIn("UEERE0001", [e["code"] for e in uee_env["evidence"]])
        self.assertIn("UEERE0001", uee_env["note"])
        uee_comm = rows["commercial_refrigeration"]["cells"]["AU-TGA-UEE32225"]
        self.assertEqual([e["code"] for e in uee_comm["evidence"]], ["UEERA0052", "UEERA0053"])
        self.assertIn("Low- and medium-temperature", uee_comm["note"])
        central = rows["central_ducted_ac"]["cells"]["AU-TGA-UEE32225"]
        self.assertEqual(central["evidence"][0]["field"], "scope_verbatim")
        self.assertEqual(central["coverage"], "PARTIAL")

    def test_refrigerant_handling_safety_is_not_workplace_safety_evidence(self):
        cell = self.rows("COURSE-034")["workplace_safety"]["cells"]["AU-TGA-UEE32225"]
        self.assertEqual([e["code"] for e in cell["evidence"]], ["UEECD0007", "UEECD0016"])

    def test_scope_limited_cells_reuse_verified_tesda_scope_notes(self):
        records = {
            record["record_id"]: record
            for path in RECORD_PATHS
            for record in json.loads(path.read_text(encoding="utf-8"))["records"]
        }
        expected = {
            ("domestic_refrigeration", "PH-TESDA-DOMRAC-NC2"),
            ("ac_installation", "PH-TESDA-DOMRAC-NC2"),
            ("ac_installation", "PH-TESDA-CAC-NC3"),
            ("ac_servicing_repair", "PH-TESDA-DOMRAC-NC2"),
            ("ac_servicing_repair", "PH-TESDA-CAC-NC3"),
            ("fault_diagnosis_testing", "PH-TESDA-DOMRAC-NC2"),
            ("fault_diagnosis_testing", "PH-TESDA-CAC-NC3"),
        }
        phrases = {
            "PH-TESDA-DOMRAC-NC2": "domestic refrigerators",
            "PH-TESDA-CAC-NC3": "commercial air-conditioning units",
        }
        for course_id in self.mappings:
            flagged = set()
            for competency_id, competency in self.rows(course_id).items():
                for column_id, cell in competency["cells"].items():
                    if not cell.get("scope_limited"):
                        continue
                    flagged.add((competency_id, column_id))
                    with self.subTest(course=course_id, competency=competency_id, column=column_id):
                        self.assertIs(cell["scope_limited"], True)
                        self.assertEqual(cell["status"], "DOCUMENTED")
                        # The limitation is the existing note, restating the record's own verified scope wording.
                        self.assertIn(phrases[column_id], cell["note"])
                        record = records[column_id]
                        published = " ".join(record["scope_verbatim"] + record["notes"])
                        self.assertIn(phrases[column_id], published)
            self.assertEqual(flagged, expected, course_id)

    def test_uee_environmental_cell_cites_its_refrigerant_regulation_scope(self):
        for course_id in self.mappings:
            cell = self.rows(course_id)["refrigerants_environment"]["cells"]["AU-TGA-UEE32225"]
            self.assertEqual(cell["coverage"], "FULL")
            self.assertEqual([e["code"] for e in cell["evidence"]], ["UEERA0062", "UEERA0079", "UEERE0001", None])
            scope = cell["evidence"][-1]
            self.assertEqual((scope["field"], scope["module_index"]), ("scope_verbatim", 0))
            self.assertIn("regulatory requirements for purchasing and handling refrigerants", scope["text"])

    def test_repeated_dgt_outcomes_are_not_cited(self):
        for competency in self.rows("COURSE-034").values():
            refs = [e["module_index"] for e in competency["cells"]["IN-DGT-CTS-RAC-V2"]["evidence"]]
            self.assertFalse({54, 55} & set(refs), competency["competency_id"])


class HardwareCompetencyMappingTests(unittest.TestCase):
    """The Computer Hardware matrices for COURSE-008 and COURSE-055 (Step 19A)."""

    D, P, N, I = ("DOCUMENTED", "FULL"), ("DOCUMENTED", "PARTIAL"), ("NOT_EXPLICIT", None), ("INSUFFICIENT_DATA", None)
    # NYSC COURSE-008, NYSC COURSE-055, then DGT, TESDA, ITE.
    EXPECTED = {
        "pc_assembly": [D, D, D, N, N],
        "device_installation": [N, D, D, N, D],
        "software_installation": [N, D, D, N, D],
        "troubleshooting_repair": [P, P, D, P, P],
        "computer_maintenance": [D, D, D, D, D],
        "laptop_servicing": [N, N, D, N, N],
        "networking": [N, D, D, D, D],
        "server_setup": [N, N, D, D, D],
        "internet_email": [N, D, D, N, N],
        "power_electronics": [N, N, P, P, N],
        "network_security": [N, N, D, N, D],
        "cost_estimating": [D, N, N, N, N],
        "workplace_safety": [N, N, D, D, I],
    }

    @classmethod
    def setUpClass(cls):
        cls.mappings = {
            cid: json.loads((BENCHMARK_DIR / f"competency_mapping_{cid.lower()}.json").read_text(encoding="utf-8"))
            for cid in ("COURSE-008", "COURSE-055")
        }
        cls.governed = {course["course_id"]: course["modules"] for course in load_governed_courses()}

    def rows(self, course_id):
        return {c["competency_id"]: c for c in self.mappings[course_id]["competencies"]}

    def test_rows_columns_and_statuses_follow_the_assessment(self):
        for course_id, mapping in self.mappings.items():
            self.assertEqual([c["competency_id"] for c in mapping["competencies"]], list(self.EXPECTED))
            self.assertEqual([c["record_id"] for c in mapping["columns"][1:]], HW_IDS)
            self.assertFalse(mapping["human_reviewed"])
        for competency_id, expected in self.EXPECTED.items():
            actual = []
            for course_id in ("COURSE-008", "COURSE-055"):
                cell = self.rows(course_id)[competency_id]["cells"][f"NYSC-{course_id}"]
                actual.append((cell["status"], cell.get("coverage")))
            cells = self.rows("COURSE-008")[competency_id]["cells"]
            actual += [(cells[r]["status"], cells[r].get("coverage")) for r in HW_IDS]
            with self.subTest(competency=competency_id):
                self.assertEqual(actual, expected)

    def test_each_course_cites_its_own_headings_with_display_corrections(self):
        devices = self.rows("COURSE-055")["device_installation"]["cells"]["NYSC-COURSE-055"]["evidence"][0]
        self.assertEqual(devices["text"], self.governed["COURSE-055"][2])
        self.assertEqual(devices["display_text"], "Install and Configure Internal, External Devices")
        network = self.rows("COURSE-055")["networking"]["cells"]["NYSC-COURSE-055"]["evidence"][0]
        self.assertEqual(network["display_text"], "Network and Internet")
        assembly = self.rows("COURSE-008")["pc_assembly"]["cells"]["NYSC-COURSE-008"]["evidence"]
        self.assertEqual([e["text"] for e in assembly], ["Assembling", "Disassembling"])
        self.assertTrue(all("display_text" not in e for e in assembly))

    def test_full_cells_name_every_component(self):
        for course_id in self.mappings:
            for competency_id, groups in HW_COMPONENT_KEYWORDS.items():
                for column_id, cell in self.rows(course_id)[competency_id]["cells"].items():
                    if cell.get("coverage") != "FULL":
                        continue
                    text = " ".join((e.get("display_text") or e["text"]).casefold() for e in cell["evidence"])
                    with self.subTest(course=course_id, competency=competency_id, column=column_id):
                        for group in groups:
                            self.assertTrue(any(k in text for k in group), group)

    def test_ite_cells_cite_module_objectives(self):
        for competency in self.rows("COURSE-008").values():
            for evidence in competency["cells"]["SG-ITE-HNITEC-ISN-2Y"]["evidence"]:
                self.assertEqual(evidence["field"], "outcome_verbatim")


class BakerAndCookeryCompetencyMappingTests(unittest.TestCase):
    """Step 19B matrix decisions and deterministic Areas rule."""

    @classmethod
    def setUpClass(cls):
        cls.records = {
            record["record_id"]: record
            for path in (BENCHMARK_DIR / "pilot_records_baker.json", BENCHMARK_DIR / "pilot_records_cookery.json")
            for record in json.loads(path.read_text(encoding="utf-8"))["records"]
        }
        cls.mappings = {
            course_id: json.loads(
                (BENCHMARK_DIR / f"competency_mapping_{course_id.lower()}.json").read_text(encoding="utf-8")
            )
            for course_id in ("COURSE-007", "COURSE-011", "COURSE-047")
        }

    def areas(self, course_id):
        mapping = self.mappings[course_id]
        nysc = f"NYSC-{course_id}"
        result = []
        for competency in mapping["competencies"]:
            if competency["cells"][nysc]["status"] != "NOT_EXPLICIT":
                continue
            full_records = [
                column["record_id"]
                for column in mapping["columns"]
                if column["kind"] == "benchmark"
                and competency["cells"][column["column_id"]].get("coverage") == "FULL"
            ]
            countries = {self.records[record_id]["country"] for record_id in full_records}
            if len(full_records) >= 2 and len(countries) >= 2:
                result.append(competency["competency_id"])
        return result

    def test_baker_areas_follow_the_two_record_two_country_rule(self):
        expected = [
            "food_safety_hygiene",
            "workplace_safety",
            "biscuits_cookies",
            "chocolate_confectionery",
            "desserts_puddings",
        ]
        self.assertEqual(self.areas("COURSE-011"), expected)
        self.assertEqual(self.areas("COURSE-047"), expected)

    def test_cookery_areas_follow_the_two_record_two_country_rule(self):
        self.assertEqual(
            self.areas("COURSE-007"),
            ["food_safety_hygiene", "workplace_safety", "kitchen_management"],
        )

    def test_part_time_baker_keeps_governed_text_and_display_correction(self):
        mapping = self.mappings["COURSE-047"]
        row = next(c for c in mapping["competencies"] if c["competency_id"] == "pastry_products")
        evidence = row["cells"]["NYSC-COURSE-047"]["evidence"][0]
        self.assertEqual(evidence["text"], "Produce Pastry weekends.")
        self.assertEqual(evidence["display_text"], "Produce Pastry")

    def test_broad_nysc_headings_do_not_establish_specific_content(self):
        baker = {c["competency_id"]: c for c in self.mappings["COURSE-011"]["competencies"]}
        self.assertEqual(baker["artisan_bread"]["cells"]["NYSC-COURSE-011"]["coverage"], "PARTIAL")
        cookery = {c["competency_id"]: c for c in self.mappings["COURSE-007"]["competencies"]}
        self.assertEqual(cookery["fish_meat_poultry"]["cells"]["NYSC-COURSE-007"]["coverage"], "PARTIAL")
        self.assertEqual(cookery["vegetable_egg_farinaceous"]["cells"]["NYSC-COURSE-007"]["coverage"], "PARTIAL")

    def test_ite_baker_inconsistent_elective_is_not_documented(self):
        rows = {c["competency_id"]: c for c in self.mappings["COURSE-011"]["competencies"]}
        cell = rows["biscuits_cookies"]["cells"]["SG-ITE-HNITEC-PASTRY-2Y"]
        self.assertEqual(cell["status"], "NOT_EXPLICIT")
        self.assertIn("inconsistent", cell["note"])


if __name__ == "__main__":
    unittest.main()
