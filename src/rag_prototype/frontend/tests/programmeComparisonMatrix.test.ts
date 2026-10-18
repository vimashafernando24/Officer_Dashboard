import assert from "node:assert/strict";
import test from "node:test";

import { BENCHMARK_RECORDS, comparatorsForCourse } from "../src/programmeBenchmarks.ts";
import { cellDisplay, mappingForCourse } from "../src/programmeComparisonMatrix.ts";
import { findCourse } from "../src/programmeComparison.ts";
import { loadAllComparisonData } from "../src/comparisonData.ts";

// Comparator data is loaded on demand in the dashboard; tests load all of it first.
await loadAllComparisonData();

const mapping = mappingForCourse("COURSE-005");
const recordsById = new Map(BENCHMARK_RECORDS.map((record) => [record.record_id, record]));


test("COURSE-005 matrix columns are the course and its linked records", () => {
  assert.ok(mapping);
  const comparators = comparatorsForCourse("COURSE-005");
  const linked = [...comparators.sriLanka, ...comparators.developingEmerging, ...comparators.developed]
    .map((record) => record.record_id);
  const columns = mapping.columns.filter((column) => column.kind === "benchmark").map((column) => column.record_id);
  assert.deepEqual([...columns].sort(), [...linked].sort());
  assert.deepEqual(
    mapping.columns.filter((column) => column.kind === "nysc").map((column) => column.nysc_course_id),
    ["COURSE-005"],
  );
});


test("documented benchmark cells quote the stored record text exactly", () => {
  assert.ok(mapping);
  for (const competency of mapping.competencies) {
    for (const column of mapping.columns.filter((c) => c.kind === "benchmark")) {
      const cell = competency.cells[column.column_id];
      if (cell.status !== "DOCUMENTED") continue;
      assert.ok(cell.evidence.length > 0, `${competency.competency_id}/${column.column_id} has no evidence`);
      const record = recordsById.get(column.record_id!);
      assert.ok(record);
      for (const evidence of cell.evidence) {
        assert.notEqual(evidence.field, "scope_verbatim");
        assert.equal(evidence.text, record.modules[evidence.module_index][evidence.field as "title_verbatim" | "outcome_verbatim"]);
      }
    }
  }
});


test("records without stored modules are never documented", () => {
  assert.ok(mapping);
  for (const column of mapping.columns.filter((c) => c.kind === "benchmark")) {
    const record = recordsById.get(column.record_id!);
    if (record && record.modules.length > 0) continue;
    for (const competency of mapping.competencies) {
      assert.equal(competency.cells[column.column_id].status, "INSUFFICIENT_DATA");
    }
  }
});


test("non-documented cells carry no evidence", () => {
  assert.ok(mapping);
  for (const competency of mapping.competencies) {
    for (const cell of Object.values(competency.cells)) {
      if (cell.status !== "DOCUMENTED") assert.equal(cell.evidence.length, 0);
    }
  }
});


test("COURSE-040 has its own NYSC column and shares the comparator columns", () => {
  const mapping040 = mappingForCourse("COURSE-040");
  assert.ok(mapping && mapping040);
  assert.deepEqual(
    mapping040.columns.filter((c) => c.kind === "nysc").map((c) => c.nysc_course_id),
    ["COURSE-040"],
  );
  const comparatorColumns = mapping.columns.filter((c) => c.kind === "benchmark");
  for (const [index, competency] of mapping.competencies.entries()) {
    const other = mapping040.competencies[index];
    assert.equal(other.competency_id, competency.competency_id);
    for (const column of comparatorColumns) {
      assert.deepEqual(other.cells[column.column_id], competency.cells[column.column_id]);
    }
  }
  const status = (id: string) =>
    mapping040.competencies.find((c) => c.competency_id === id)!.cells["NYSC-COURSE-040"].status;
  assert.equal(status("suspension"), "DOCUMENTED");
  assert.equal(status("vehicle_electrical"), "NOT_EXPLICIT");
});


const MAPPED = ["COURSE-005", "COURSE-040", "COURSE-025", "COURSE-064"];


test("every mapping's documented comparator cells quote the stored record text exactly", () => {
  for (const courseId of MAPPED) {
    const courseMapping = mappingForCourse(courseId);
    assert.ok(courseMapping, courseId);
    for (const competency of courseMapping.competencies) {
      for (const column of courseMapping.columns) {
        const cell = competency.cells[column.column_id];
        if (cell.status !== "DOCUMENTED") {
          assert.equal(cell.evidence.length, 0);
          continue;
        }
        assert.ok(cell.evidence.length > 0);
        if (column.kind !== "benchmark") continue;
        const record = recordsById.get(column.record_id!);
        assert.ok(record, column.record_id);
        for (const evidence of cell.evidence) {
          const source = evidence.field === "scope_verbatim"
            ? record.scope_verbatim?.[evidence.module_index]
            : record.modules[evidence.module_index][evidence.field];
          assert.equal(evidence.text, source);
          assert.equal(evidence.display_text, undefined);
        }
      }
    }
  }
});


test("Electrician NYSC citations keep governed text and add only the verified correction", () => {
  const nyscEvidence = (courseId: string, competencyId: string) =>
    mappingForCourse(courseId)!.competencies.find((c) => c.competency_id === competencyId)!
      .cells[`NYSC-${courseId}`].evidence[0];
  const course025 = findCourse("COURSE-025")!;
  const industrial = nyscEvidence("COURSE-025", "industrial_installation");
  assert.equal(industrial.text, course025.modules[industrial.module_index]);
  assert.equal(industrial.display_text, "Industrial Electrical Installation (Motor Controlling System)");
  assert.equal(
    industrial.display_text,
    course025.module_display_corrections.find((c) => c.module_index === industrial.module_index)!.displayed,
  );
  // COURSE-064's Domestic heading needs no correction, so none is attached.
  assert.equal(nyscEvidence("COURSE-064", "domestic_wiring").display_text, undefined);
  assert.equal(nyscEvidence("COURSE-025", "domestic_wiring").display_text, "Domestic Electrical Installation");
});


test("Electrician courses share comparator cells and differ only in their NYSC columns", () => {
  const a = mappingForCourse("COURSE-025")!;
  const b = mappingForCourse("COURSE-064")!;
  for (const [index, competency] of a.competencies.entries()) {
    for (const column of a.columns.filter((c) => c.kind === "benchmark")) {
      assert.deepEqual(b.competencies[index].cells[column.column_id], competency.cells[column.column_id]);
    }
  }
  const security = a.competencies.find((c) => c.competency_id === "security_building")!;
  assert.equal(security.cells["NYSC-COURSE-025"].status, "INSUFFICIENT_DATA");
});


test("every DOCUMENTED cell is classified FULL or PARTIAL, and partial cells name their support", () => {
  for (const courseId of MAPPED) {
    for (const competency of mappingForCourse(courseId)!.competencies) {
      for (const cell of Object.values(competency.cells)) {
        if (cell.status === "DOCUMENTED") {
          assert.ok(cell.coverage === "FULL" || cell.coverage === "PARTIAL");
          if (cell.coverage === "PARTIAL") assert.ok(cell.supported_component?.trim());
          assert.equal(cellDisplay(cell).key, cell.coverage === "PARTIAL" ? "PARTIAL" : "DOCUMENTED");
        } else {
          assert.equal(cell.coverage, undefined);
        }
      }
    }
  }
});


test("audit corrections: CGTTI testing and ITE engine management are no longer documented", () => {
  const status = (courseId: string, competencyId: string, recordId: string) =>
    mappingForCourse(courseId)!.competencies.find((c) => c.competency_id === competencyId)!.cells[recordId].status;
  assert.equal(status("COURSE-025", "testing_fault_finding", "LK-CGTTI-POWER-ELEC"), "NOT_EXPLICIT");
  assert.equal(status("COURSE-005", "engine_management", "SG-ITE-HNITEC-AUTO-2Y"), "NOT_EXPLICIT");
  assert.equal(status("COURSE-025", "electrical_safety", "SG-ITE-HNITEC-ELEC-2Y"), "INSUFFICIENT_DATA");
  assert.equal(status("COURSE-064", "security_building", "NYSC-COURSE-064"), "INSUFFICIENT_DATA");
});


test("unmapped courses get no comparison", () => {
  for (const courseId of ["COURSE-021", "COURSE-001", "COURSE-999"]) {
    assert.equal(mappingForCourse(courseId), null);
  }
});
