import assert from "node:assert/strict";
import test from "node:test";

import { loadCourseComparison } from "../src/comparisonData.ts";
import {
  comparatorCounts,
  comparatorsForCourse,
  comparisonCaveat,
  durationDisplay,
  findBenchmarkRecord,
  modulePreview,
  qualificationDisplay,
} from "../src/programmeBenchmarks.ts";
import { investigationAreas, mappingForCourse, scopeLimitation } from "../src/programmeComparisonMatrix.ts";
import { coverageForCourse } from "../src/programmeCoverage.ts";

const HW = ["IN-DGT-CTS-CHNM-V2", "PH-TESDA-CSS-NC2", "SG-ITE-HNITEC-ISN-2Y"];
const COURSES = ["COURSE-008", "COURSE-055", "COURSE-056"];

// Only the hardware data is loaded here, as the dashboard would for these courses.
for (const courseId of COURSES) await loadCourseComparison(courseId);

const summary = (courseId: string) =>
  investigationAreas(mappingForCourse(courseId)!).map((a) => [a.label, a.supporting_comparators.length, a.supporting_countries.length]);


test("the three hardware courses share three verified comparators, with no Sri Lankan record", () => {
  for (const courseId of COURSES) {
    const comparators = comparatorsForCourse(courseId);
    assert.deepEqual(comparatorCounts(comparators), { sriLanka: 0, developingEmerging: 2, developed: 1 }, courseId);
    assert.deepEqual(
      [...comparators.developingEmerging, ...comparators.developed].map((r) => r.record_id),
      HW,
      courseId,
    );
    assert.match(comparisonCaveat(courseId)!.text, /No independent Sri Lankan programme with published modules was verified/);
  }
  assert.equal(findBenchmarkRecord("IN-DGT-CTS-CHNM-V2")!.modules.length, 17);
  assert.equal(findBenchmarkRecord("PH-TESDA-CSS-NC2")!.modules.length, 15);
  assert.equal(findBenchmarkRecord("SG-ITE-HNITEC-ISN-2Y")!.modules.length, 14);
});


test("COURSE-008 and COURSE-055 are full comparisons; COURSE-056 is comparators only", () => {
  assert.equal(coverageForCourse("COURSE-008")!.state, "FULL_COMPARISON");
  assert.equal(coverageForCourse("COURSE-055")!.state, "FULL_COMPARISON");
  assert.equal(coverageForCourse("COURSE-056")!.state, "COMPARATORS_ONLY");
  assert.equal(mappingForCourse("COURSE-056"), null);
  for (const courseId of ["COURSE-008", "COURSE-055"]) {
    const mapping = mappingForCourse(courseId)!;
    assert.equal(mapping.competencies.length, 13);
    assert.equal(mapping.human_reviewed, false);
    // No hardware evidence carries an equipment-scope flag.
    for (const competency of mapping.competencies) {
      for (const cell of Object.values(competency.cells)) assert.equal(scopeLimitation(cell), null);
    }
  }
});


test("Areas to Investigate follow the two-record, two-country rule", () => {
  assert.deepEqual(summary("COURSE-008"), [
    ["Computer network setup", 3, 3],
    ["Server setup", 3, 3],
    ["Installing and configuring devices and peripherals", 2, 2],
    ["Network security", 2, 2],
    ["Operating system and software installation", 2, 2],
    ["Workplace safety", 2, 2],
  ]);
  assert.deepEqual(summary("COURSE-055"), [
    ["Server setup", 3, 3],
    ["Network security", 2, 2],
    ["Workplace safety", 2, 2],
  ]);
  // Partial-only and single-country support never becomes an area.
  const ids = investigationAreas(mappingForCourse("COURSE-008")!).map((a) => a.competency_id);
  for (const excluded of ["laptop_servicing", "internet_email", "power_electronics", "troubleshooting_repair"]) {
    assert.ok(!ids.includes(excluded), excluded);
  }
});


test("cards keep TESDA's core preview and published durations and levels", () => {
  const tesda = findBenchmarkRecord("PH-TESDA-CSS-NC2")!;
  assert.deepEqual(modulePreview(tesda.modules, false).modules.map((m) => m.code), ["ELC724331", "ELC724332", "ELC724333", "ELC724334"]);
  assert.equal(durationDisplay(findBenchmarkRecord("IN-DGT-CTS-CHNM-V2")!.duration_as_published).summary, "1 year");
  assert.equal(durationDisplay(tesda.duration_as_published).summary, tesda.duration_as_published);
  assert.equal(durationDisplay(findBenchmarkRecord("SG-ITE-HNITEC-ISN-2Y")!.duration_as_published).summary, "2 years");
  assert.deepEqual(qualificationDisplay(findBenchmarkRecord("IN-DGT-CTS-CHNM-V2")!), { label: "NSQF Level 3.5", framework: "NSQF (India)", code: null });
});
