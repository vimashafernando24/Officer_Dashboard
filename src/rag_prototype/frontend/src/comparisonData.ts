// Loads comparator records and competency mappings on demand, per selected course,
// using the generated loaders (src/data/comparisonDataLoaders.ts) and the compact
// coverage index. Each dataset or mapping is fetched once and shared by every course
// that links to it, so course variants reuse the same records.
import { MAPPING_LOADERS, RECORD_DATASET_LOADERS, RECORD_DATASET_ORDER } from "./data/comparisonDataLoaders.ts";
import { registerRecordDataset } from "./programmeBenchmarks.ts";
import type { BenchmarkRecord } from "./programmeBenchmarks.ts";
import { registerMapping } from "./programmeComparisonMatrix.ts";
import type { CompetencyMapping } from "./programmeComparisonMatrix.ts";
import { indexEntry } from "./programmeCoverage.ts";

const pending = new Map<string, Promise<void>>();

function once(key: string, load: () => Promise<void>): Promise<void> {
  let promise = pending.get(key);
  if (!promise) {
    promise = load().catch((error: unknown) => {
      pending.delete(key); // allow a retry after a failed load
      throw error;
    });
    pending.set(key, promise);
  }
  return promise;
}

function loadDataset(key: string): Promise<void> {
  const loader = RECORD_DATASET_LOADERS[key];
  if (!loader) return Promise.reject(new Error(`Unknown record dataset: ${key}`));
  return once(`dataset:${key}`, async () => {
    const module = (await loader()).default as { records: BenchmarkRecord[] };
    registerRecordDataset(key, module.records, RECORD_DATASET_ORDER);
  });
}

function loadMapping(courseId: string): Promise<void> {
  const loader = MAPPING_LOADERS[courseId];
  if (!loader) return Promise.reject(new Error(`No mapping loader for ${courseId}`));
  return once(`mapping:${courseId}`, async () => {
    registerMapping((await loader()).default as CompetencyMapping);
  });
}

/** Whether a course has stored comparator data that must be loaded before display. */
export function courseNeedsData(courseId: string): boolean {
  const entry = indexEntry(courseId);
  return Boolean(entry && (entry.datasets.length > 0 || entry.mapping));
}

/** Loads everything a course's comparison needs: its record datasets and, if any, its mapping. */
export async function loadCourseComparison(courseId: string): Promise<void> {
  const entry = indexEntry(courseId);
  if (!entry) return;
  await Promise.all([
    ...entry.datasets.map(loadDataset),
    ...(entry.mapping ? [loadMapping(courseId)] : []),
  ]);
}

/** Loads every dataset and mapping (used by tests and checks, never by the dashboard). */
export async function loadAllComparisonData(): Promise<void> {
  await Promise.all([
    ...RECORD_DATASET_ORDER.map(loadDataset),
    ...Object.keys(MAPPING_LOADERS).map(loadMapping),
  ]);
}
