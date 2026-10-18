import assert from "node:assert/strict";
import test from "node:test";

import { loadCourseComparison } from "../src/comparisonData.ts";
import { comparatorsForCourse, findBenchmarkRecord } from "../src/programmeBenchmarks.ts";
import { investigationAreas, mappingForCourse } from "../src/programmeComparisonMatrix.ts";
import { coverageForCourse } from "../src/programmeCoverage.ts";

for (const courseId of ["COURSE-006", "COURSE-022", "COURSE-052", "COURSE-058"]) {
  await loadCourseComparison(courseId);
}

const ids = (courseId: string) => {
  const grouped = comparatorsForCourse(courseId);
  return [...grouped.sriLanka, ...grouped.developingEmerging, ...grouped.developed].map((record) => record.record_id);
};

test("COURSE-006 uses three substantive diploma-level comparisons", () => {
  assert.deepEqual(ids("COURSE-006"), [
    "LK-TVEC-NCS-ICT-L5-2025",
    "SG-ITE-HNITEC-ITAD-2Y",
    "SG-ITE-HNITEC-ISN-2Y",
  ]);
  assert.equal(coverageForCourse("COURSE-006")!.state, "FULL_COMPARISON");

  const mapping = mappingForCourse("COURSE-006")!;
  const networking = mapping.competencies.find((item) => item.competency_id === "dip_networking")!;
  assert.equal(networking.cells["SG-ITE-HNITEC-ISN-2Y"].coverage, "FULL");
  const programming = mapping.competencies.find((item) => item.competency_id === "dip_programming")!;
  assert.equal(programming.cells["SG-ITE-HNITEC-ISN-2Y"].coverage, "PARTIAL");
  assert.deepEqual(investigationAreas(mapping).map((area) => area.competency_id), ["dip_mobile_apps"]);
});

test("network-technician and CCNA courses stay comparator-only", () => {
  assert.deepEqual(ids("COURSE-022"), [
    "LK-TVEC-NCS-COMPUTER-SYSTEMS-NETWORK-2026",
    "IN-DGT-CTS-CHNM-V2",
    "PH-TESDA-CSS-NC2",
    "SG-ITE-HNITEC-ISN-2Y",
    "AU-TGA-ICT40120-NETWORKING",
  ]);
  assert.deepEqual(ids("COURSE-052"), [
    "LK-TVEC-NCS-COMPUTER-SYSTEMS-NETWORK-2026",
    "SG-ITE-HNITEC-ISN-2Y",
    "AU-TGA-ICT40120-NETWORKING",
  ]);
  for (const courseId of ["COURSE-022", "COURSE-052"]) {
    assert.equal(coverageForCourse(courseId)!.state, "COMPARATORS_ONLY");
    assert.equal(mappingForCourse(courseId), null);
  }
});

test("COURSE-058 keeps its independent computer-accounting mapping", () => {
  assert.deepEqual(ids("COURSE-058"), [
    "IN-NQR-HARTRON-COMPUTER-ACCOUNTING-V2",
    "SG-ITE-HNITEC-ACCOUNTING-2Y",
    "AU-TGA-FNS30322",
  ]);
  assert.equal(coverageForCourse("COURSE-058")!.state, "FULL_COMPARISON");
  assert.deepEqual(investigationAreas(mappingForCourse("COURSE-058")!).map((area) => area.competency_id), [
    "acc_transactions_ledgers",
    "acc_bank_reconciliation",
    "acc_payroll",
    "acc_tax",
    "acc_trial_balance_statements",
  ]);
});

test("all six new Step 29 records retain pending human review status", () => {
  for (const recordId of [
    "LK-TVEC-NCS-ICT-L5-2025",
    "LK-TVEC-NCS-COMPUTER-SYSTEMS-NETWORK-2026",
    "AU-TGA-ICT40120-NETWORKING",
    "IN-NQR-HARTRON-COMPUTER-ACCOUNTING-V2",
    "SG-ITE-HNITEC-ACCOUNTING-2Y",
    "AU-TGA-FNS30322",
  ]) {
    const record = findBenchmarkRecord(recordId)!;
    assert.equal(record.verification.status, "source_inspected_pending_human_review", recordId);
    assert.equal(record.verification.human_reviewed, false, recordId);
  }
});
