import assert from "node:assert/strict";
import test from "node:test";

import { loadCourseComparison } from "../src/comparisonData.ts";
import { comparatorCounts, comparatorsForCourse, findBenchmarkRecord } from "../src/programmeBenchmarks.ts";
import { investigationAreas, mappingForCourse } from "../src/programmeComparisonMatrix.ts";
import { coverageForCourse } from "../src/programmeCoverage.ts";

// Only the data these courses need is loaded, as the dashboard would.
for (const courseId of ["COURSE-009", "COURSE-053", "COURSE-054"]) await loadCourseComparison(courseId);

const ids = (courseId: string) => {
  const c = comparatorsForCourse(courseId);
  return [...c.sriLanka, ...c.developingEmerging, ...c.developed].map((r) => r.record_id);
};
const summary = (courseId: string) =>
  investigationAreas(mappingForCourse(courseId)!).map((a) => [a.label, a.supporting_comparators.length, a.supporting_countries.length]);


test("COURSE-009 links the Level 4 standard and reuses technical-support records", () => {
  assert.deepEqual(ids("COURSE-009"), [
    "LK-TVEC-NCS-ICT-TECH-L4-2023", "IN-DGT-CTS-COPA-V3", "PH-TESDA-CSS-NC2", "SG-ITE-HNITEC-ISN-2Y", "AU-TGA-ICT20120",
  ]);
  assert.deepEqual(comparatorCounts(comparatorsForCourse("COURSE-009")), { sriLanka: 1, developingEmerging: 2, developed: 2 });
  assert.equal(coverageForCourse("COURSE-009")!.state, "FULL_COMPARISON");
  assert.equal(findBenchmarkRecord("LK-TVEC-NCS-ICT-TECH-L4-2023")!.modules.length, 15);
});


test("COURSE-053 and COURSE-054 use the Level 3 package; COURSE-054 is comparators only", () => {
  const expected = ["LK-TVEC-NCS-COMPUTER-APP-ASSIST-L3-2023", "IN-DGT-CTS-COPA-V3", "AU-TGA-ICT20120"];
  assert.deepEqual(ids("COURSE-053"), expected);
  assert.deepEqual(ids("COURSE-054"), expected);
  assert.equal(coverageForCourse("COURSE-053")!.state, "FULL_COMPARISON");
  assert.equal(coverageForCourse("COURSE-054")!.state, "COMPARATORS_ONLY");
  assert.equal(mappingForCourse("COURSE-054"), null);
  const l3 = findBenchmarkRecord("LK-TVEC-NCS-COMPUTER-APP-ASSIST-L3-2023")!;
  assert.equal(l3.modules.length, 11);
  // Level 4-only units are never part of the Level 3 qualification.
  assert.ok(!l3.modules.some((m) => ["K72S004U08", "K72S004U09", "K72S004U10", "K72S004U11"].includes(m.code ?? "")));
});


test("Areas to Investigate follow the two-record, two-country rule", () => {
  assert.deepEqual(summary("COURSE-009"), [
    ["Computer system maintenance", 3, 3],
    ["Workplace safety", 3, 3],
    ["Information and network security", 2, 2],
  ]);
  assert.deepEqual(summary("COURSE-053"), [
    ["Computer and operating system use", 3, 3],
    ["Databases", 2, 2],
    ["Workplace safety", 2, 2],
  ]);
});


test("COURSE-009's merged heading 10 is never cited", () => {
  const mapping = mappingForCourse("COURSE-009")!;
  const cited = mapping.competencies.flatMap((c) => c.cells["NYSC-COURSE-009"].evidence.map((e) => e.module_index));
  assert.ok(!cited.includes(9));
  for (const id of ["ict_web_design", "ict_software_development"]) {
    assert.equal(mapping.competencies.find((c) => c.competency_id === id)!.cells["NYSC-COURSE-009"].status, "INSUFFICIENT_DATA");
  }
});
