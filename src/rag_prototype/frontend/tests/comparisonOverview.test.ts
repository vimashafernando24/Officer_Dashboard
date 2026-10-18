import assert from "node:assert/strict";
import test from "node:test";

import { courseSummaryFacts, findCourse } from "../src/programmeComparison.ts";
import { comparatorCounts, comparatorsForCourse } from "../src/programmeBenchmarks.ts";
import { investigationAreas, mappingForCourse } from "../src/programmeComparisonMatrix.ts";
import type { CompetencyMapping, CompetencyStatus } from "../src/programmeComparisonMatrix.ts";
import { loadAllComparisonData } from "../src/comparisonData.ts";

// Comparator data is loaded on demand in the dashboard; tests load all of it first.
await loadAllComparisonData();

/** A one-rule fixture: NYSC status plus one status per comparator record. */
function fixture(rows: { id: string; label: string; nysc: CompetencyStatus; comparators: (CompetencyStatus | "PARTIAL")[] }[], recordIds = ["R1", "R2", "R3"]): CompetencyMapping {
  const columns = [
    { column_id: "NYSC", kind: "nysc" as const, nysc_course_id: "COURSE-X", short_label: "NYSC" },
    ...recordIds.map((recordId, index) => ({
      column_id: `C${index}`,
      kind: "benchmark" as const,
      record_id: recordId,
      short_label: `Comparator ${index}`,
    })),
  ];
  // Fixture cells mark DOCUMENTED as FULL unless a PARTIAL test opts out.
  const cell = (status: CompetencyStatus | "PARTIAL") =>
    status === "PARTIAL"
      ? { status: "DOCUMENTED" as const, evidence: [], note: null, coverage: "PARTIAL" as const, supported_component: "one component" }
      : { status, evidence: [], note: null, ...(status === "DOCUMENTED" ? { coverage: "FULL" as const } : {}) };
  return {
    nysc_course_id: "COURSE-X",
    human_reviewed: false,
    columns,
    competencies: rows.map((row) => ({
      competency_id: row.id,
      label: row.label,
      cells: Object.fromEntries([
        ["NYSC", cell(row.nysc)],
        ...row.comparators.map((status, index) => [`C${index}`, cell(status)]),
      ]),
    })),
  };
}


/** Fixture records R1-R3 come from three different countries; SAME-RECORD from one. */
const FIXTURE_COUNTRIES: Record<string, string> = { R1: "Country A", R2: "Country B", R3: "Country C", "SAME-RECORD": "Country A" };
const areasOf = (mapping: CompetencyMapping, countries = FIXTURE_COUNTRIES) =>
  investigationAreas(mapping, (recordId) => countries[recordId]);


test("COURSE-005 investigation areas are computed from the stored mapping", () => {
  const mapping = mappingForCourse("COURSE-005");
  assert.ok(mapping);
  const areas = investigationAreas(mapping);
  assert.deepEqual(
    areas.map((area) => [area.label, area.supporting_comparators.length]),
    [
      ["Emission control", 4],
      ["Starting and charging systems", 4],
      ["Workplace safety and health", 4],
      ["Fault diagnosis", 3],
      ["Suspension systems", 2],
    ],
  );
  assert.ok(areas.every((area) => area.nysc_status === "NOT_EXPLICIT"));
  // CGTTI's partial fault diagnosis is shown alongside but not counted.
  const fault = areas.find((area) => area.competency_id === "fault_diagnosis")!;
  assert.deepEqual(fault.partial_comparators, ["CGTTI · Sri Lanka", "TESDA · Philippines"]);
  // Engine management has only partial support (DGT, TAFE NSW, CGTTI), so it is not an area.
  assert.ok(!areas.some((area) => area.competency_id === "engine_management"));
});


test("only NOT_EXPLICIT NYSC competencies qualify; documented or insufficient ones do not", () => {
  const areas = areasOf(fixture([
    { id: "a", label: "A", nysc: "NOT_EXPLICIT", comparators: ["DOCUMENTED", "DOCUMENTED", "DOCUMENTED"] },
    { id: "b", label: "B", nysc: "DOCUMENTED", comparators: ["DOCUMENTED", "DOCUMENTED", "DOCUMENTED"] },
    { id: "c", label: "C", nysc: "INSUFFICIENT_DATA", comparators: ["DOCUMENTED", "DOCUMENTED", "DOCUMENTED"] },
  ]));
  assert.deepEqual(areas.map((area) => area.competency_id), ["a"]);
});


test("at least two documented comparators are required, and insufficient data never counts", () => {
  const areas = areasOf(fixture([
    { id: "one", label: "One", nysc: "NOT_EXPLICIT", comparators: ["DOCUMENTED", "NOT_EXPLICIT", "INSUFFICIENT_DATA"] },
    { id: "two", label: "Two", nysc: "NOT_EXPLICIT", comparators: ["DOCUMENTED", "DOCUMENTED", "INSUFFICIENT_DATA"] },
    { id: "unknown", label: "Unknown", nysc: "NOT_EXPLICIT", comparators: ["INSUFFICIENT_DATA", "INSUFFICIENT_DATA", "DOCUMENTED"] },
  ]));
  assert.deepEqual(areas.map((area) => area.competency_id), ["two"]);
});


test("partial-only support never meets the threshold but is reported", () => {
  const areas = areasOf(fixture([
    { id: "partial", label: "Partial", nysc: "NOT_EXPLICIT", comparators: ["PARTIAL", "PARTIAL", "PARTIAL"] },
    { id: "mixed", label: "Mixed", nysc: "NOT_EXPLICIT", comparators: ["DOCUMENTED", "PARTIAL", "DOCUMENTED"] },
    { id: "short", label: "Short", nysc: "NOT_EXPLICIT", comparators: ["DOCUMENTED", "PARTIAL", "NOT_EXPLICIT"] },
  ]));
  assert.deepEqual(areas.map((area) => area.competency_id), ["mixed"]);
  assert.equal(areas[0].supporting_comparators.length, 2);
  assert.deepEqual(areas[0].partial_comparators, ["Comparator 1"]);
});


test("support is counted per distinct comparator record", () => {
  const areas = areasOf(fixture(
    [{ id: "dup", label: "Dup", nysc: "NOT_EXPLICIT", comparators: ["DOCUMENTED", "DOCUMENTED"] }],
    ["SAME-RECORD", "SAME-RECORD"],
  ));
  assert.deepEqual(areas, []);
});


test("two FULL records from the same country never qualify", () => {
  const mapping = fixture([{ id: "x", label: "X", nysc: "NOT_EXPLICIT", comparators: ["DOCUMENTED", "DOCUMENTED", "NOT_EXPLICIT"] }]);
  assert.deepEqual(areasOf(mapping, { R1: "Philippines", R2: "Philippines", R3: "India" }), []);
  // A third FULL record from another country completes the rule.
  const three = fixture([{ id: "x", label: "X", nysc: "NOT_EXPLICIT", comparators: ["DOCUMENTED", "DOCUMENTED", "DOCUMENTED"] }]);
  const [area] = areasOf(three, { R1: "Philippines", R2: "Philippines", R3: "India" });
  assert.equal(area.supporting_comparators.length, 3);
  assert.deepEqual(area.supporting_countries, ["Philippines", "India"]);
});


test("a record with an unknown country never counts towards the country threshold", () => {
  const mapping = fixture([{ id: "x", label: "X", nysc: "NOT_EXPLICIT", comparators: ["DOCUMENTED", "DOCUMENTED", "NOT_EXPLICIT"] }]);
  assert.deepEqual(areasOf(mapping, { R1: "India" }), []);
});


test("partial support from another country never completes the country threshold", () => {
  const mapping = fixture([{ id: "x", label: "X", nysc: "NOT_EXPLICIT", comparators: ["DOCUMENTED", "DOCUMENTED", "PARTIAL"] }]);
  assert.deepEqual(areasOf(mapping, { R1: "Philippines", R2: "Philippines", R3: "India" }), []);
});


test("areas sort by supporting count, then alphabetically", () => {
  const areas = areasOf(fixture([
    { id: "z", label: "Zeta", nysc: "NOT_EXPLICIT", comparators: ["DOCUMENTED", "DOCUMENTED", "NOT_EXPLICIT"] },
    { id: "b", label: "Beta", nysc: "NOT_EXPLICIT", comparators: ["DOCUMENTED", "DOCUMENTED", "DOCUMENTED"] },
    { id: "a", label: "Alpha", nysc: "NOT_EXPLICIT", comparators: ["DOCUMENTED", "DOCUMENTED", "NOT_EXPLICIT"] },
  ]));
  assert.deepEqual(areas.map((area) => area.label), ["Beta", "Alpha", "Zeta"]);
});


test("comparator counts reflect the linked records, and are zero for unlinked courses", () => {
  assert.deepEqual(comparatorCounts(comparatorsForCourse("COURSE-005")), {
    sriLanka: 1,
    developingEmerging: 2,
    developed: 2,
  });
  assert.deepEqual(comparatorCounts(comparatorsForCourse("COURSE-040")), {
    sriLanka: 1,
    developingEmerging: 2,
    developed: 2,
  });
  assert.deepEqual(comparatorCounts(comparatorsForCourse("COURSE-025")), {
    sriLanka: 1,
    developingEmerging: 3,
    developed: 2,
  });
  assert.deepEqual(comparatorCounts(comparatorsForCourse("COURSE-034")), {
    sriLanka: 1,
    developingEmerging: 3,
    developed: 1,
  });
  assert.deepEqual(comparatorCounts(comparatorsForCourse("COURSE-038")), {
    sriLanka: 0,
    developingEmerging: 1,
    developed: 0,
  });
});


test("COURSE-040 investigation areas are recalculated from its own NYSC column", () => {
  const mapping = mappingForCourse("COURSE-040");
  assert.ok(mapping);
  assert.deepEqual(
    investigationAreas(mapping).map((area) => [area.label, area.supporting_comparators.length]),
    [
      ["Emission control", 4],
      ["Starting and charging systems", 4],
      ["Workplace safety and health", 4],
      ["Fault diagnosis", 3],
      ["Vehicle electrical systems (general)", 3],
    ],
  );
});


test("courses without a mapping produce no investigation areas", () => {
  assert.equal(mappingForCourse("COURSE-021"), null);
  assert.equal(mappingForCourse("COURSE-001"), null);
});


test("Electrician investigation areas use the deterministic rule for both courses", () => {
  const expected = [
    ["Electrical principles and circuits", 4],
    ["Solar PV, batteries and EV charging", 2],
  ];
  for (const courseId of ["COURSE-025", "COURSE-064"]) {
    const mapping = mappingForCourse(courseId);
    assert.ok(mapping);
    const areas = investigationAreas(mapping);
    assert.deepEqual(areas.map((area) => [area.label, area.supporting_comparators.length]), expected);
    // The ambiguous "Security Solutions" heading is INSUFFICIENT_DATA, so it never becomes an area.
    assert.ok(!areas.some((area) => area.competency_id === "security_building"));
  }
});


test("the course summary uses only catalogue fields and marks unstated values", () => {
  const course005 = findCourse("COURSE-005");
  assert.ok(course005);
  assert.deepEqual(courseSummaryFacts(course005), [
    { label: "Qualification", value: "National Vocational Qualification (NVQ) · Level 4" },
    { label: "Duration", value: "12 months" },
    { label: "Attendance", value: "Full Time" },
  ]);
  assert.equal(course005.modules.length, 5);

  const unstated = { ...course005, qualification_type: "NOT_STATED", nvq_level: "NOT_STATED", duration_months: "NOT_STATED", attendance_type: "NOT_STATED" };
  assert.ok(courseSummaryFacts(unstated).every(({ value }) => value === "Not stated"));
});
