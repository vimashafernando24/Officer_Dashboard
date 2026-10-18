import assert from "node:assert/strict";
import test from "node:test";

import { loadCourseComparison } from "../src/comparisonData.ts";
import { comparatorCounts, comparatorsForCourse, findBenchmarkRecord } from "../src/programmeBenchmarks.ts";
import { mappingForCourse } from "../src/programmeComparisonMatrix.ts";
import { coverageForCourse, coveragePresentation } from "../src/programmeCoverage.ts";

const DRAUGHT = [
  "LK-TVEC-NCS-DRAUGHTSPERSON-2023",
  "IN-DGT-CTS-DRAUGHTSMAN-CIVIL-V2",
  "PH-TESDA-TECHNICAL-DRAFTING-NC2",
];

const EXPECTED: Record<string, [string[], { sriLanka: number; developingEmerging: number; developed: number }]> = {
  "COURSE-019": [["LK-TVEC-NCS-QUANTITY-SURVEYING-ASSISTANT-2024"], { sriLanka: 1, developingEmerging: 0, developed: 0 }],
  "COURSE-024": [DRAUGHT, { sriLanka: 1, developingEmerging: 2, developed: 0 }],
  "COURSE-061": [DRAUGHT, { sriLanka: 1, developingEmerging: 2, developed: 0 }],
  "COURSE-065": [DRAUGHT, { sriLanka: 1, developingEmerging: 2, developed: 0 }],
  "COURSE-033": [["LK-TVEC-NCS-PLUMBER-R5", "IN-DGT-CTS-PLUMBER-V3", "PH-TESDA-PLUMBING-NC2-2014", "AU-TGA-CPC32420-PLUMBING-R8"], { sriLanka: 1, developingEmerging: 2, developed: 1 }],
  "COURSE-036": [["LK-TVEC-NCS-SURVEY-FIELD-ASSISTANT-2023", "IN-DGT-CTS-SURVEYOR-V2", "AU-TGA-CPP30226-SURVEYING-ASSISTANT"], { sriLanka: 1, developingEmerging: 1, developed: 1 }],
};

for (const courseId of Object.keys(EXPECTED)) await loadCourseComparison(courseId);

const shownIds = (courseId: string) => {
  const records = comparatorsForCourse(courseId);
  return [...records.sriLanka, ...records.developingEmerging, ...records.developed].map((record) => record.record_id);
};

test("Step 32 courses render verified comparator-only coverage", () => {
  for (const [courseId, [expectedIds, counts]] of Object.entries(EXPECTED)) {
    assert.deepEqual(shownIds(courseId).sort(), [...expectedIds].sort(), courseId);
    assert.deepEqual(comparatorCounts(comparatorsForCourse(courseId)), counts, courseId);
    const coverage = coverageForCourse(courseId)!;
    assert.equal(coverage.state, "COMPARATORS_ONLY", courseId);
    assert.equal(coverage.evidenceAvailability, "NO_HEADINGS", courseId);
    assert.equal(coverage.hasMapping, false, courseId);
    assert.equal(mappingForCourse(courseId), null, courseId);
    assert.deepEqual(coveragePresentation(coverage.state), { showComparators: true, showMatrix: false, showAreas: false });
  }
});

test("specialist records expose verified occupational content", () => {
  assert.ok(findBenchmarkRecord("LK-TVEC-NCS-QUANTITY-SURVEYING-ASSISTANT-2024")!.modules.some((unit) => /Bill of Quantities/i.test(unit.title_verbatim)));
  assert.ok(findBenchmarkRecord("IN-DGT-CTS-DRAUGHTSMAN-CIVIL-V2")!.modules.some((unit) => /orthographic|site plan/i.test(unit.title_verbatim)));
  assert.ok(findBenchmarkRecord("LK-TVEC-NCS-PLUMBER-R5")!.modules.some((unit) => /water supply/i.test(unit.title_verbatim)));
  assert.ok(findBenchmarkRecord("AU-TGA-CPP30226-SURVEYING-ASSISTANT")!.modules.some((unit) => /surveying/i.test(unit.title_verbatim)));
});
