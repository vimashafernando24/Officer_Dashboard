import assert from "node:assert/strict";
import test from "node:test";

import { loadCourseComparison } from "../src/comparisonData.ts";
import { comparatorCounts, comparatorsForCourse, coreCompetencyGroup, findBenchmarkRecord, modulePreview } from "../src/programmeBenchmarks.ts";
import { mappingForCourse } from "../src/programmeComparisonMatrix.ts";
import { coverageForCourse, coveragePresentation } from "../src/programmeCoverage.ts";

const GROUPS: Record<string, [string[], string[], { sriLanka: number; developingEmerging: number; developed: number }]> = {
  construction: [["COURSE-023", "COURSE-060"], ["LK-TVEC-NCS-CONSTRUCTION-SITE-SUPERVISOR-2025", "AU-TGA-CPC40120-SITE-MANAGEMENT"],
    { sriLanka: 1, developingEmerging: 0, developed: 1 }],
  motorcycle: [["COURSE-030", "COURSE-078"], ["LK-TVEC-NCS-MOTORCYCLE-TECHNICIAN-2025", "IN-DGT-CTS-2W3W-V2", "PH-TESDA-MOTORCYCLE-NC2", "AU-TGA-AUR30820"],
    { sriLanka: 1, developingEmerging: 2, developed: 1 }],
  autoElectrical: [["COURSE-021", "COURSE-042"], ["LK-TVEC-NCS-AUTO-ELECTRICIAN-2026", "IN-DGT-CTS-MAEE-V2", "PH-TESDA-ASER-ELEC-NC2", "AU-TGA-AUR30320"],
    { sriLanka: 1, developingEmerging: 2, developed: 1 }],
  mobile: [["COURSE-029", "COURSE-077"], ["LK-TVEC-NCS-MOBILE-PHONE-REPAIR-2024", "PH-TESDA-MOBILE-NC3", "IN-NQR-TSSC-HANDHELD-V2"],
    { sriLanka: 1, developingEmerging: 2, developed: 0 }],
  graphic: [["COURSE-016", "COURSE-068"], ["LK-TVEC-NCS-GRAPHIC-DESIGNER-2025", "PH-TESDA-VGD-NC3", "SG-ITE-HNITEC-COMMDESIGN-2Y"],
    { sriLanka: 1, developingEmerging: 1, developed: 1 }],
};

// Only the data these courses need is loaded, as the dashboard would.
for (const [courses] of Object.values(GROUPS)) for (const courseId of courses) await loadCourseComparison(courseId);

const ids = (courseId: string) => {
  const c = comparatorsForCourse(courseId);
  return [...c.sriLanka, ...c.developingEmerging, ...c.developed].map((r) => r.record_id);
};


test("the ten courses show verified comparators without a matrix", () => {
  for (const [courses, records, counts] of Object.values(GROUPS)) {
    for (const courseId of courses) {
      assert.deepEqual([...ids(courseId)].sort(), [...records].sort(), courseId);
      assert.deepEqual(comparatorCounts(comparatorsForCourse(courseId)), counts, courseId);
      const coverage = coverageForCourse(courseId)!;
      assert.equal(coverage.state, "COMPARATORS_ONLY", courseId);
      assert.deepEqual(coveragePresentation(coverage.state), { showComparators: true, showMatrix: false, showAreas: false });
      assert.equal(mappingForCourse(courseId), null, courseId);
    }
  }
});


test("unresearched related occupation groups stay unlinked", () => {
  for (const courseId of ["COURSE-037"]) {
    assert.equal(ids(courseId).length, 0, courseId);
    assert.equal(coverageForCourse(courseId)!.state, "RESEARCH_PENDING", courseId);
  }
});


test("new TESDA cards preview their core competencies", () => {
  const expected: Record<string, string[]> = {
    "PH-TESDA-MOTORCYCLE-NC2": ["ALT723372", "ALT723373", "ALT723374", "ALT723375"],
    "PH-TESDA-ASER-ELEC-NC2": ["ALT723392", "ALT723393", "ALT723394", "ALT723395", "ALT723396"],
    "PH-TESDA-MOBILE-NC3": ["ELC742301", "ELC742302", "ELC742303", "ELC742304"],
    "PH-TESDA-VGD-NC3": ["ICT216313", "ICT216314", "ICT216315", "ICT216316", "ICT216317"],
  };
  for (const [id, codes] of Object.entries(expected)) {
    const record = findBenchmarkRecord(id)!;
    assert.equal(coreCompetencyGroup(record.modules), "Core Competencies", id);
    const preview = modulePreview(record.modules, false);
    assert.equal(preview.mode, "core-preview", id);
    assert.deepEqual(preview.modules.map((m) => m.code), codes, id);
  }
});
