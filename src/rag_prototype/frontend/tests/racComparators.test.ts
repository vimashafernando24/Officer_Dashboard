import assert from "node:assert/strict";
import test from "node:test";

import {
  BENCHMARK_RECORDS,
  RECORD_TYPE_LABELS,
  comparatorCounts,
  comparatorsForCourse,
  comparisonCaveat,
  coreCompetencyGroup,
  durationDisplay,
  modulePreview,
  qualificationDisplay,
  verificationLabel,
} from "../src/programmeBenchmarks.ts";
import {
  PARTIAL_DETAILS,
  SCOPE_LIMITED_DETAILS,
  STATUS_DETAILS,
  cellDisplay,
  investigationAreas,
  mappingForCourse,
  scopeLimitation,
} from "../src/programmeComparisonMatrix.ts";
import { loadAllComparisonData } from "../src/comparisonData.ts";

// Comparator data is loaded on demand in the dashboard; tests load all of it first.
await loadAllComparisonData();

const RAC_IDS = [
  "LK-CGTTI-RAC-MECH",
  "IN-DGT-CTS-RAC-V2",
  "PH-TESDA-DOMRAC-NC2",
  "PH-TESDA-CAC-NC3",
  "AU-TGA-UEE32225",
];
const RAC_COURSES = ["COURSE-034", "COURSE-012"];

const byId = new Map(BENCHMARK_RECORDS.map((record) => [record.record_id, record]));
const record = (id: string) => byId.get(id)!;


test("both RAC courses show the same five comparators, grouped 1 / 3 / 1", () => {
  for (const courseId of RAC_COURSES) {
    const comparators = comparatorsForCourse(courseId);
    assert.deepEqual(comparatorCounts(comparators), { sriLanka: 1, developingEmerging: 3, developed: 1 }, courseId);
    assert.deepEqual(comparators.sriLanka.map((r) => r.record_id), ["LK-CGTTI-RAC-MECH"]);
    assert.deepEqual(
      comparators.developingEmerging.map((r) => r.record_id),
      ["IN-DGT-CTS-RAC-V2", "PH-TESDA-DOMRAC-NC2", "PH-TESDA-CAC-NC3"],
    );
    assert.deepEqual(comparators.developed.map((r) => r.record_id), ["AU-TGA-UEE32225"]);
  }
});


test("every RAC record is displayable and pending human review", () => {
  for (const id of RAC_IDS) {
    assert.ok(byId.has(id), id);
    assert.equal(verificationLabel(record(id)), "Source inspected · pending human review");
  }
});


test("record types distinguish the programme, curriculum, standards and national qualification", () => {
  assert.deepEqual(
    RAC_IDS.map((id) => RECORD_TYPE_LABELS[record(id).record_type]),
    ["Delivered Programme", "National Curriculum", "Occupational Standard", "Occupational Standard", "National Qualification"],
  );
  assert.equal(record("AU-TGA-UEE32225").delivering_provider_verified, false);
});


test("the caveat states scope limits and the facts the comparators leave unstated", () => {
  for (const courseId of RAC_COURSES) {
    const caveat = comparisonCaveat(courseId);
    assert.ok(caveat, courseId);
    assert.match(caveat.text, /window-type air-conditioning and domestic refrigerators only/);
    assert.match(caveat.text, /commercial air-conditioning units only/);
    assert.match(caveat.text, /national qualification, not a delivered programme/);
    assert.deepEqual(
      caveat.unstated.map(({ record: r, fields }) => [r.record_id, fields]),
      [["LK-CGTTI-RAC-MECH", ["qualification level"]], ["AU-TGA-UEE32225", ["duration"]]],
    );
  }
});


test("durations restate only the published periods and totals", () => {
  const expected: Record<string, [string, boolean]> = {
    "LK-CGTTI-RAC-MECH": ["42 months (full-time)", false],
    "IN-DGT-CTS-RAC-V2": ["2 years", true],
    "PH-TESDA-DOMRAC-NC2": ["528 total hours (including supervised industry learning)", true],
    "PH-TESDA-CAC-NC3": ["720 total hours (including supervised industry learning)", true],
    "AU-TGA-UEE32225": ["Not stated", false],
  };
  for (const [id, [summary, hasDetails]] of Object.entries(expected)) {
    const display = durationDisplay(record(id).duration_as_published);
    assert.equal(display.summary, summary, id);
    assert.equal(display.details, hasDetails ? record(id).duration_as_published : null, id);
  }
  // The nominal-hours and SIL breakdown stays visible in the details.
  assert.match(durationDisplay(record("PH-TESDA-DOMRAC-NC2").duration_as_published).details!, /288 - Total; 240 – Supervised Industry Learning \(SIL\)/);
  assert.match(durationDisplay(record("PH-TESDA-CAC-NC3").duration_as_published).details!, /320 Hours - Total; 400 Hours – Supervised Industry Learning \(SIL\)/);
});


test("qualifications keep their own framework; CGTTI states none", () => {
  assert.deepEqual(qualificationDisplay(record("LK-CGTTI-RAC-MECH")), { label: "Not stated", framework: null, code: null });
  assert.deepEqual(qualificationDisplay(record("IN-DGT-CTS-RAC-V2")), { label: "NSQF Level 4", framework: "NSQF (India)", code: null });
  assert.deepEqual(qualificationDisplay(record("PH-TESDA-DOMRAC-NC2")), { label: "NC II", framework: "Philippine TVET Qualification (NC)", code: null });
  assert.deepEqual(qualificationDisplay(record("PH-TESDA-CAC-NC3")), { label: "NC III", framework: "Philippine TVET Qualification (NC)", code: null });
  assert.deepEqual(qualificationDisplay(record("AU-TGA-UEE32225")), { label: "Certificate III", framework: "AQF (Australia)", code: "UEE32225" });
});


test("TESDA RAC cards preview their core competencies; others preview the first five items", () => {
  assert.deepEqual(
    modulePreview(record("PH-TESDA-DOMRAC-NC2").modules, false).modules.map((m) => m.code),
    ["HVC723337", "HVC723338", "HVC723339"],
  );
  assert.deepEqual(
    modulePreview(record("PH-TESDA-CAC-NC3").modules, false).modules.map((m) => m.code),
    ["HVC723340", "HVC723342", "HVC723344", "HVC723346"],
  );
  for (const id of ["LK-CGTTI-RAC-MECH", "IN-DGT-CTS-RAC-V2", "AU-TGA-UEE32225"]) {
    assert.equal(coreCompetencyGroup(record(id).modules), null, id);
    const preview = modulePreview(record(id).modules, false);
    assert.equal(preview.mode, "first-items", id);
    assert.deepEqual(preview.modules, record(id).modules.slice(0, 5));
  }
});


const RAC_AREAS = [
  ["AC installation", 5, 4],
  ["Fault diagnosis and testing", 5, 4],
  ["Workplace safety", 5, 4],
  ["Refrigerants, recovery and environmental practice", 3, 3],
  ["Electrical circuits, motors and controls", 2, 2],
  ["Pipework, tubing and brazing", 2, 2],
];

const areaSummary = (courseId: string) =>
  investigationAreas(mappingForCourse(courseId)!).map((area) => [
    area.label,
    area.supporting_comparators.length,
    area.supporting_countries.length,
  ]);


test("both RAC courses have a 14-row matrix over their five comparators", () => {
  for (const courseId of RAC_COURSES) {
    const mapping = mappingForCourse(courseId);
    assert.ok(mapping, courseId);
    assert.equal(mapping.human_reviewed, false);
    assert.equal(mapping.competencies.length, 14);
    assert.deepEqual(
      mapping.columns.map((column) => column.record_id ?? column.nysc_course_id),
      [courseId, ...RAC_IDS],
    );
  }
});


test("each RAC course has the six expected areas, with record and country counts", () => {
  for (const courseId of RAC_COURSES) {
    assert.deepEqual(areaSummary(courseId), RAC_AREAS, courseId);
  }
  const safety = investigationAreas(mappingForCourse("COURSE-034")!).find((a) => a.competency_id === "workplace_safety")!;
  // Two Philippine records count as records, but as one country.
  assert.deepEqual(safety.supporting_countries, ["Sri Lanka", "India", "Philippines", "Australia"]);
  const electrical = investigationAreas(mappingForCourse("COURSE-034")!).find((a) => a.competency_id === "electrical_motors_controls")!;
  assert.deepEqual(electrical.partial_comparators, [
    "CGTTI · Sri Lanka",
    "TESDA DomRAC NC II · Philippines",
    "TESDA Commercial AC NC III · Philippines",
  ]);
});


test("partial-only RAC categories are not areas", () => {
  for (const courseId of RAC_COURSES) {
    const ids = investigationAreas(mappingForCourse(courseId)!).map((area) => area.competency_id);
    for (const excluded of ["refrigeration_cycle_components", "psychrometrics_load", "leak_evacuation_charging", "commercial_refrigeration"]) {
      assert.ok(!ids.includes(excluded), `${courseId} ${excluded}`);
    }
  }
});


test("existing Automotive and Electrician comparators are unchanged", () => {
  const ids = (courseId: string) => {
    const c = comparatorsForCourse(courseId);
    return [...c.sriLanka, ...c.developingEmerging, ...c.developed].map((r) => r.record_id);
  };
  const automotive = ["LK-CGTTI-AUTO-TECH", "IN-DGT-CTS-MMV-V2", "PH-TESDA-ASER-NC2", "SG-ITE-HNITEC-AUTO-2Y", "AU-TAFENSW-AUR30620"];
  const electrician = ["LK-CGTTI-POWER-ELEC", "IN-DGT-CTS-ELEC-V3", "PH-TESDA-EIM-NC2", "PH-TESDA-EIM-NC3", "SG-ITE-HNITEC-ELEC-2Y", "AU-TAFENSW-UEE30820"];
  assert.deepEqual(ids("COURSE-005"), automotive);
  assert.deepEqual(ids("COURSE-040"), automotive);
  assert.deepEqual(ids("COURSE-025"), electrician);
  assert.deepEqual(ids("COURSE-064"), electrician);
  assert.equal(BENCHMARK_RECORDS.length, 47);
  // Rankings are unchanged by the two-country rule.
  assert.deepEqual(areaSummary("COURSE-005"), [
    ["Emission control", 4, 4],
    ["Starting and charging systems", 4, 4],
    ["Workplace safety and health", 4, 4],
    ["Fault diagnosis", 3, 3],
    ["Suspension systems", 2, 2],
  ]);
  assert.deepEqual(areaSummary("COURSE-040"), [
    ["Emission control", 4, 4],
    ["Starting and charging systems", 4, 4],
    ["Workplace safety and health", 4, 4],
    ["Fault diagnosis", 3, 3],
    ["Vehicle electrical systems (general)", 3, 3],
  ]);
  for (const courseId of ["COURSE-025", "COURSE-064"]) {
    assert.deepEqual(areaSummary(courseId), [
      ["Electrical principles and circuits", 4, 4],
      ["Solar PV, batteries and EV charging", 2, 2],
    ]);
  }
});


test("legend labels distinguish full from partial and keep the not-taught caution", () => {
  assert.equal(STATUS_DETAILS.DOCUMENTED.label, "Documented (full)");
  assert.equal(PARTIAL_DETAILS.label, "Documented (partial)");
  assert.match(STATUS_DETAILS.NOT_EXPLICIT.meaning, /does not mean it is not taught/);
  const full = mappingForCourse("COURSE-034")!.competencies[7].cells["PH-TESDA-DOMRAC-NC2"];
  assert.equal(cellDisplay(full).label, "Documented (full)");
});


test("TESDA scope limits are flagged on their cells and named in Areas, using the stored notes", () => {
  for (const courseId of RAC_COURSES) {
    const mapping = mappingForCourse(courseId)!;
    const row = (id: string) => mapping.competencies.find((c) => c.competency_id === id)!;
    const domrac = row("ac_servicing_repair").cells["PH-TESDA-DOMRAC-NC2"];
    assert.equal(scopeLimitation(domrac), domrac.note);
    assert.match(scopeLimitation(domrac)!, /window-type air-conditioning and domestic refrigerators only/);
    assert.match(scopeLimitation(row("ac_installation").cells["PH-TESDA-CAC-NC3"])!, /commercial air-conditioning units only/);
    // Unflagged cells, including other TESDA cells with notes, report no limitation.
    assert.equal(scopeLimitation(row("ac_servicing_repair").cells["IN-DGT-CTS-RAC-V2"]), null);
    assert.equal(scopeLimitation(row("central_ducted_ac").cells["PH-TESDA-DOMRAC-NC2"]), null);

    const areas = new Map(investigationAreas(mapping).map((area) => [area.competency_id, area]));
    const tesda = ["TESDA DomRAC NC II · Philippines", "TESDA Commercial AC NC III · Philippines"];
    assert.deepEqual(areas.get("ac_installation")!.scope_limited_comparators, tesda);
    assert.deepEqual(areas.get("fault_diagnosis_testing")!.scope_limited_comparators, tesda);
    assert.deepEqual(areas.get("workplace_safety")!.scope_limited_comparators, []);
    // Scope-limited support is still counted: counts and ranking are unchanged.
    assert.deepEqual(areaSummary(courseId), RAC_AREAS);
  }
  assert.equal(SCOPE_LIMITED_DETAILS.label, "Scope-limited");
});


test("no automotive or Electrician evidence is flagged as scope-limited", () => {
  for (const courseId of ["COURSE-005", "COURSE-040", "COURSE-025", "COURSE-064"]) {
    const mapping = mappingForCourse(courseId)!;
    for (const competency of mapping.competencies) {
      for (const cell of Object.values(competency.cells)) assert.equal(scopeLimitation(cell), null);
    }
    assert.ok(investigationAreas(mapping).every((area) => area.scope_limited_comparators.length === 0));
  }
});


test("every row of all eleven mappings has category components to show", () => {
  for (const courseId of ["COURSE-005", "COURSE-040", "COURSE-025", "COURSE-064", ...RAC_COURSES]) {
    const mapping = mappingForCourse(courseId)!;
    for (const competency of mapping.competencies) {
      const components = mapping.category_components[competency.competency_id];
      assert.ok(components?.length, `${courseId} ${competency.competency_id}`);
    }
  }
  assert.deepEqual(mappingForCourse("COURSE-034")!.category_components.refrigerants_environment, [
    "refrigerant recovery or recycling",
    "refrigerant environmental or regulatory practice, or explicit environmental procedures",
  ]);
});
