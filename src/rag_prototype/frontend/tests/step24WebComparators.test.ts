import assert from "node:assert/strict";
import test from "node:test";

import { loadCourseComparison } from "../src/comparisonData.ts";
import { comparatorCounts, comparatorsForCourse, findBenchmarkRecord } from "../src/programmeBenchmarks.ts";
import { investigationAreas, mappingForCourse } from "../src/programmeComparisonMatrix.ts";
import { coverageForCourse } from "../src/programmeCoverage.ts";

// Only the data these courses need is loaded, as the dashboard would.
for (const courseId of ["COURSE-087", "COURSE-057", "COURSE-001"]) await loadCourseComparison(courseId);

const WEB = ["LK-TVEC-NCS-WEB-DEVELOPER-2025", "IN-NQR-HARTRON-WEB-MULTIMEDIA-V2", "PH-TESDA-WEBDEV-NC3", "SG-ITE-HNITEC-ITAD-2Y", "AU-TGA-ICT40120-WEBDEV"];
const ids = (courseId: string) => {
  const c = comparatorsForCourse(courseId);
  return [...c.sriLanka, ...c.developingEmerging, ...c.developed].map((r) => r.record_id);
};


test("the three web courses share five web-focused comparators", () => {
  for (const courseId of ["COURSE-087", "COURSE-057", "COURSE-001"]) {
    assert.deepEqual(ids(courseId), WEB, courseId);
    assert.deepEqual(comparatorCounts(comparatorsForCourse(courseId)), { sriLanka: 1, developingEmerging: 2, developed: 2 });
  }
  assert.equal(coverageForCourse("COURSE-087")!.state, "FULL_COMPARISON");
  assert.equal(coverageForCourse("COURSE-057")!.state, "COMPARATORS_ONLY");
  assert.equal(coverageForCourse("COURSE-001")!.state, "COMPARATORS_ONLY");
  assert.equal(mappingForCourse("COURSE-057"), null);
  assert.equal(mappingForCourse("COURSE-001"), null);
  assert.equal(findBenchmarkRecord("PH-TESDA-WEBDEV-NC3")!.modules.length, 34);
});


test("COURSE-087 Areas to Investigate follow the two-record, two-country rule", () => {
  const areas = investigationAreas(mappingForCourse("COURSE-087")!).map((a) => [a.label, a.supporting_comparators.length, a.supporting_countries.length]);
  assert.deepEqual(areas, [
    ["Website and interface design (UI/UX)", 5, 5],
    ["Back-end and server-side development", 3, 3],
    ["Content management systems", 3, 3],
    ["Databases for web applications", 3, 3],
    ["Requirements and development methodology", 3, 3],
    ["Website security", 3, 3],
    ["Website testing", 3, 3],
    ["Search engine optimisation", 2, 2],
  ]);
});
