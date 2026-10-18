import assert from "node:assert/strict";
import test from "node:test";

import { loadAllComparisonData } from "../src/comparisonData.ts";
import { comparatorsForCourse, findBenchmarkRecord } from "../src/programmeBenchmarks.ts";
import { investigationAreas, mappingForCourse } from "../src/programmeComparisonMatrix.ts";

await loadAllComparisonData();

const shownIds = (courseId: string) => {
  const groups = comparatorsForCourse(courseId);
  return [...groups.sriLanka, ...groups.developingEmerging, ...groups.developed]
    .map((record) => record.record_id);
};

const areaIds = (courseId: string) =>
  investigationAreas(mappingForCourse(courseId)!).map((area) => area.competency_id);

test("both Baker courses reuse the three verified records and keep separate mappings", () => {
  const expected = ["IN-DGT-CTS-BAKER-V2", "SG-ITE-HNITEC-PASTRY-2Y", "AU-TGA-FBP30521"];
  assert.deepEqual(shownIds("COURSE-011"), expected);
  assert.deepEqual(shownIds("COURSE-047"), expected);
  assert.equal(mappingForCourse("COURSE-011")!.nysc_course_id, "COURSE-011");
  assert.equal(mappingForCourse("COURSE-047")!.nysc_course_id, "COURSE-047");
});

test("Baker Areas follow the two-record and two-country rule", () => {
  const expected = [
    "desserts_puddings",
    "food_safety_hygiene",
    "workplace_safety",
    "biscuits_cookies",
    "chocolate_confectionery",
  ];
  assert.deepEqual(areaIds("COURSE-011"), expected);
  assert.deepEqual(areaIds("COURSE-047"), expected);
  assert.ok(!areaIds("COURSE-011").includes("artisan_bread"), "PARTIAL NYSC bread evidence must prevent an Area classification");
});

test("Professional Cookery loads four verified records and three deterministic Areas", () => {
  assert.deepEqual(shownIds("COURSE-007"), [
    "IN-DGT-CTS-FOOD-PROD-V2",
    "PH-TESDA-PRO-COOKERY-NC3",
    "SG-ITE-HNITEC-CULINARY-2Y",
    "AU-TGA-SIT30821",
  ]);
  assert.deepEqual(areaIds("COURSE-007"), [
    "workplace_safety",
    "food_safety_hygiene",
    "kitchen_management",
  ]);
});

test("national standards and qualifications are not displayed as delivered programmes", () => {
  for (const recordId of ["IN-DGT-CTS-BAKER-V2", "AU-TGA-FBP30521", "IN-DGT-CTS-FOOD-PROD-V2", "PH-TESDA-PRO-COOKERY-NC3", "AU-TGA-SIT30821"]) {
    const record = findBenchmarkRecord(recordId)!;
    assert.notEqual(record.record_type, "programme", recordId);
    assert.equal(record.delivering_provider_verified, false, recordId);
  }
  for (const recordId of ["SG-ITE-HNITEC-PASTRY-2Y", "SG-ITE-HNITEC-CULINARY-2Y"]) {
    const record = findBenchmarkRecord(recordId)!;
    assert.equal(record.record_type, "programme", recordId);
    assert.equal(record.delivering_provider_verified, true, recordId);
  }
});

test("the part-time Baker mapping preserves governed text and its approved display correction", () => {
  const mapping = mappingForCourse("COURSE-047")!;
  const row = mapping.competencies.find((item) => item.competency_id === "pastry_products")!;
  const evidence = row.cells["NYSC-COURSE-047"].evidence[0];
  assert.equal(evidence.text, "Produce Pastry weekends.");
  assert.equal(evidence.display_text, "Produce Pastry");
});
