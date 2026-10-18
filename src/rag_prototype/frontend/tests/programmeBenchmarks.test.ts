import assert from "node:assert/strict";
import test from "node:test";

import {
  BENCHMARK_RECORDS,
  RECORD_TYPE_LABELS,
  comparatorsForCourse,
  comparisonCaveat,
  groupModules,
  isDisplayable,
  verificationLabel,
} from "../src/programmeBenchmarks.ts";
import type { BenchmarkRecord } from "../src/programmeBenchmarks.ts";
import { loadAllComparisonData } from "../src/comparisonData.ts";

// Comparator data is loaded on demand in the dashboard; tests load all of it first.
await loadAllComparisonData();

const ids = (records: BenchmarkRecord[]) => records.map((record) => record.record_id);


test("COURSE-005 shows the linked pilot records in the right groups", () => {
  const comparators = comparatorsForCourse("COURSE-005");
  assert.deepEqual(ids(comparators.sriLanka), ["LK-CGTTI-AUTO-TECH"]);
  assert.deepEqual(ids(comparators.developingEmerging), ["IN-DGT-CTS-MMV-V2", "PH-TESDA-ASER-NC2"]);
  assert.deepEqual(ids(comparators.developed), ["SG-ITE-HNITEC-AUTO-2Y", "AU-TAFENSW-AUR30620"]);
});


test("COURSE-040 reuses the same five comparator records as COURSE-005", () => {
  const ids005 = comparatorsForCourse("COURSE-005");
  const ids040 = comparatorsForCourse("COURSE-040");
  assert.deepEqual(ids(ids040.sriLanka), ids(ids005.sriLanka));
  assert.deepEqual(ids(ids040.developingEmerging), ids(ids005.developingEmerging));
  assert.deepEqual(ids(ids040.developed), ids(ids005.developed));
});


test("automotive courses carry the duration/level caveat, qualified by unstated comparator facts", () => {
  assert.match(comparisonCaveat("COURSE-038")!.text, /Only one source-inspected specialist curriculum/);
  assert.deepEqual(comparisonCaveat("COURSE-005"), comparisonCaveat("COURSE-040"));
  const caveat = comparisonCaveat("COURSE-040");
  assert.ok(caveat);
  assert.equal(caveat.text, "Different programme duration and qualification levels; curriculum content comparison only.");
  assert.deepEqual(
    caveat.unstated.map(({ record, fields }) => [record.record_id, fields]),
    [["LK-CGTTI-AUTO-TECH", ["qualification level"]], ["AU-TAFENSW-AUR30620", ["duration"]]],
  );
});


const ELECTRICIAN_IDS = {
  sriLanka: ["LK-CGTTI-POWER-ELEC"],
  developingEmerging: ["IN-DGT-CTS-ELEC-V3", "PH-TESDA-EIM-NC2", "PH-TESDA-EIM-NC3"],
  developed: ["SG-ITE-HNITEC-ELEC-2Y", "AU-TAFENSW-UEE30820"],
};


test("both Electrician courses show the six records in their groups (1 / 3 / 2)", () => {
  for (const courseId of ["COURSE-025", "COURSE-064"]) {
    const comparators = comparatorsForCourse(courseId);
    assert.deepEqual(ids(comparators.sriLanka), ELECTRICIAN_IDS.sriLanka);
    assert.deepEqual(ids(comparators.developingEmerging), ELECTRICIAN_IDS.developingEmerging);
    assert.deepEqual(ids(comparators.developed), ELECTRICIAN_IDS.developed);
  }
});


test("Electrician records keep standards, curricula and programmes distinct and unreviewed", () => {
  const byId = new Map(BENCHMARK_RECORDS.map((record) => [record.record_id, record]));
  const label = (id: string) => RECORD_TYPE_LABELS[byId.get(id)!.record_type];
  assert.equal(label("LK-CGTTI-POWER-ELEC"), "Delivered Programme");
  assert.equal(label("IN-DGT-CTS-ELEC-V3"), "National Curriculum");
  assert.equal(label("PH-TESDA-EIM-NC2"), "Occupational Standard");
  assert.equal(label("PH-TESDA-EIM-NC3"), "Occupational Standard");
  assert.equal(label("SG-ITE-HNITEC-ELEC-2Y"), "Delivered Programme");
  assert.equal(label("AU-TAFENSW-UEE30820"), "Delivered Programme");
  for (const id of Object.values(ELECTRICIAN_IDS).flat()) {
    assert.equal(verificationLabel(byId.get(id)!), "Source inspected · pending human review");
  }
});


test("Electrician caveat covers duration, level and TESDA scope, and names unstated facts", () => {
  for (const courseId of ["COURSE-025", "COURSE-064"]) {
    const caveat = comparisonCaveat(courseId);
    assert.ok(caveat);
    assert.match(caveat.text, /^Different programme duration and qualification levels; curriculum content comparison only\./);
    assert.match(caveat.text, /NC II .* NC III/);
    assert.deepEqual(
      caveat.unstated.map(({ record, fields }) => [record.record_id, fields]),
      [["LK-CGTTI-POWER-ELEC", ["qualification level"]], ["AU-TAFENSW-UEE30820", ["duration"]]],
    );
  }
});


test("courses without verified links get no records, even in the same sector", () => {
  for (const courseId of ["COURSE-003", "COURSE-999"]) {
    const comparators = comparatorsForCourse(courseId);
    assert.equal(comparators.sriLanka.length + comparators.developingEmerging.length + comparators.developed.length, 0);
  }
});


test("record types keep standards distinct from delivered programmes", () => {
  const byId = new Map(BENCHMARK_RECORDS.map((record) => [record.record_id, record]));
  assert.equal(RECORD_TYPE_LABELS[byId.get("IN-DGT-CTS-MMV-V2")!.record_type], "National Curriculum");
  assert.equal(RECORD_TYPE_LABELS[byId.get("PH-TESDA-ASER-NC2")!.record_type], "Occupational Standard");
  assert.equal(RECORD_TYPE_LABELS[byId.get("SG-ITE-HNITEC-AUTO-2Y")!.record_type], "Delivered Programme");
});


test("a programme without a verified provider is never displayed", () => {
  const record = { ...BENCHMARK_RECORDS[0], record_type: "programme", delivering_provider_verified: false } as BenchmarkRecord;
  assert.equal(isDisplayable(record), false);
});


test("no pilot record is reported as human verified", () => {
  for (const record of BENCHMARK_RECORDS) {
    assert.notEqual(verificationLabel(record), "Human verified");
  }
  const claimed = {
    ...BENCHMARK_RECORDS[0],
    verification: { status: "human_verified", method: "x", human_reviewed: false },
  } as BenchmarkRecord;
  assert.notEqual(verificationLabel(claimed), "Human verified");
});


test("the CGTTI Automobile Technician curriculum is captured and shown as pending review", () => {
  const cgtti = BENCHMARK_RECORDS.filter((record) => record.record_id === "LK-CGTTI-AUTO-TECH");
  assert.equal(cgtti.length, 1);
  assert.equal(cgtti[0].modules.length, 17);
  assert.equal(cgtti[0].content_fidelity, "verbatim");
  assert.equal(verificationLabel(cgtti[0]), "Source inspected · pending human review");
  assert.deepEqual(
    groupModules(cgtti[0].modules).map(({ group, modules }) => [group, modules.length]),
    [["First Year", 1], ["Second Year", 4], ["Third Year", 8], ["Final Year", 3], ["Theory", 1]],
  );
});


test("modules are grouped under their published headings in published order", () => {
  const ite = BENCHMARK_RECORDS.find((record) => record.record_id === "SG-ITE-HNITEC-AUTO-2Y")!;
  const groups = groupModules(ite.modules);
  assert.deepEqual(groups.map(({ group }) => group), [
    "Sector Foundation Modules",
    "Specialisation Modules",
    "Internship Programme",
  ]);
  assert.equal(groups.reduce((total, { modules }) => total + modules.length, 0), ite.modules.length);
});
