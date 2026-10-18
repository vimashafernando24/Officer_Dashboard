import { useEffect, useRef, useState } from "react";
import type { KeyboardEvent } from "react";
import {
  COMPARISON_TABS,
  coursesInSector,
  courseOptionLabel,
  findCourse,
  listSectors,
  sectorLabel,
} from "../programmeComparison";
import type { ComparisonTab } from "../programmeComparison";
import { comparatorsForCourse } from "../programmeBenchmarks";
import type { BenchmarkRecord } from "../programmeBenchmarks";
import { BenchmarkRecordCard } from "./BenchmarkRecordCard";
import { ComparisonOverview } from "./ComparisonOverview";
import { ComparisonCaveatNote } from "./ComparisonCaveatNote";
import { CoverageStatusNote } from "./CoverageStatusNote";
import { coverageForCourse, coveragePresentation, EVIDENCE_REVIEW_NOTICE } from "../programmeCoverage";
import { courseNeedsData, loadCourseComparison } from "../comparisonData";
import "./ProgrammeComparisonDashboard.css";

interface ProgrammeComparisonDashboardProps {
  onReturnToOfficerDashboard: () => void;
}

const SECTORS = listSectors();

const NO_COMPARATORS = "No verified comparable programmes available yet.";
const LOADING = "Loading comparison data…";
const LOAD_FAILED = "Comparison data could not be loaded. Reload the page to try again.";

type DataStatus = "ready" | "loading" | "error";

/** Loads the selected course's comparator data on demand; courses without stored data are ready at once. */
function useCourseData(courseId: string): DataStatus {
  const [loaded, setLoaded] = useState<Record<string, DataStatus>>({});
  useEffect(() => {
    if (!courseId || !courseNeedsData(courseId)) return;
    let active = true;
    loadCourseComparison(courseId).then(
      () => { if (active) setLoaded((state) => ({ ...state, [courseId]: "ready" })); },
      () => { if (active) setLoaded((state) => ({ ...state, [courseId]: "error" })); },
    );
    return () => { active = false; };
  }, [courseId]);
  if (!courseId || !courseNeedsData(courseId)) return "ready";
  return loaded[courseId] ?? "loading";
}

function DataStatusNote({ status }: { status: DataStatus }) {
  return <div className="pcd-empty" role="status">{status === "error" ? LOAD_FAILED : LOADING}</div>;
}

/** Record cards for one group, or a labelled empty state. */
function RecordGroup({ title, records }: { title?: string; records: BenchmarkRecord[] }) {
  return (
    <div className="pcd-record-group">
      {title && <h4 className="pcd-record-group-title">{title} <span>({records.length})</span></h4>}
      {records.length === 0 ? (
        <div className="pcd-empty" role="note">{NO_COMPARATORS}</div>
      ) : (
        <div className="pcd-card-grid">
          {records.map((record) => <BenchmarkRecordCard record={record} key={record.record_id} />)}
        </div>
      )}
    </div>
  );
}

export function ProgrammeComparisonDashboard({
  onReturnToOfficerDashboard,
}: ProgrammeComparisonDashboardProps) {
  const [sector, setSector] = useState("");
  const [courseId, setCourseId] = useState("");
  const [activeTab, setActiveTab] = useState<ComparisonTab>("overview");
  const tabRefs = useRef<Record<ComparisonTab, HTMLButtonElement | null>>({
    overview: null,
    "sri-lanka": null,
    international: null,
  });

  const dataStatus = useCourseData(courseId);
  const sectorCourses = sector ? coursesInSector(sector) : [];
  const selectedCourse = courseId ? findCourse(courseId) : null;
  const comparators = selectedCourse ? comparatorsForCourse(selectedCourse.course_id) : null;
  const coverage = selectedCourse ? coverageForCourse(selectedCourse.course_id) : null;
  // Courses without verified comparators explain their research state instead of a generic empty state.
  const pendingNote = coverage && !coveragePresentation(coverage.state).showComparators
    ? <CoverageStatusNote coverage={coverage} />
    : null;
  const hasInternational = Boolean(
    comparators && comparators.developingEmerging.length + comparators.developed.length > 0,
  );
  const awaitingSelection = selectedCourse
    ? null
    : "Select a sector and an NYSC course to begin.";

  function moveTabFocus(event: KeyboardEvent<HTMLButtonElement>, index: number) {
    const offset = event.key === "ArrowRight" ? 1 : event.key === "ArrowLeft" ? -1 : 0;
    if (offset === 0) return;
    event.preventDefault();
    const next = COMPARISON_TABS[(index + offset + COMPARISON_TABS.length) % COMPARISON_TABS.length];
    setActiveTab(next.id);
    tabRefs.current[next.id]?.focus();
  }

  return (
    <div className="pcd-page">
      <header className="pcd-header">
        <div className="pcd-header-inner">
          <button className="pcd-back" type="button" onClick={onReturnToOfficerDashboard}>
            ← Officer dashboard
          </button>
          <div className="pcd-brand">Youth Circles <span>Management workspace</span></div>
          <h1>Programme Comparison Dashboard</h1>
          <p className="pcd-intro">
            Compare a governed NYSC course with published Sri Lankan and international training
            programmes.
          </p>
          <p className="pcd-review-notice" role="note">{EVIDENCE_REVIEW_NOTICE}</p>
        </div>
      </header>

      <main className="pcd-main">
        <section className="pcd-selector" aria-label="Course selection">
          <label>
            <span>Sector</span>
            <select
              value={sector}
              onChange={(event) => {
                setSector(event.target.value);
                setCourseId("");
              }}
            >
              <option value="">Select a sector</option>
              {SECTORS.map((value) => (
                <option value={value} key={value}>{sectorLabel(value)}</option>
              ))}
            </select>
          </label>

          <label>
            <span>NYSC course</span>
            <select
              value={courseId}
              disabled={!sector}
              onChange={(event) => setCourseId(event.target.value)}
            >
              <option value="">{sector ? "Select a course" : "Select a sector first"}</option>
              {sectorCourses.map((course) => (
                <option value={course.course_id} key={course.course_id}>
                  {courseOptionLabel(course)}
                </option>
              ))}
            </select>
          </label>
        </section>

        <div className="pcd-tabs" role="tablist" aria-label="Comparison views">
          {COMPARISON_TABS.map((tab, index) => (
            <button
              key={tab.id}
              ref={(element) => { tabRefs.current[tab.id] = element; }}
              id={`pcd-tab-${tab.id}`}
              className="pcd-tab"
              type="button"
              role="tab"
              aria-selected={activeTab === tab.id}
              aria-controls={`pcd-tabpanel-${tab.id}`}
              tabIndex={activeTab === tab.id ? 0 : -1}
              onClick={() => setActiveTab(tab.id)}
              onKeyDown={(event) => moveTabFocus(event, index)}
            >
              {tab.label}
            </button>
          ))}
        </div>

        {activeTab === "overview" && (
          <div
            className="pcd-overview"
            role="tabpanel"
            id="pcd-tabpanel-overview"
            aria-labelledby="pcd-tab-overview"
          >
            <ComparisonOverview course={selectedCourse} dataStatus={dataStatus} />
          </div>
        )}

        {activeTab === "sri-lanka" && (
          <div
            className="pcd-programmes"
            role="tabpanel"
            id="pcd-tabpanel-sri-lanka"
            aria-labelledby="pcd-tab-sri-lanka"
          >
            <section className="pcd-panel">
              <h3>Sri Lankan programmes</h3>
              <p className="pcd-panel-description">
                Programmes offered by other Sri Lankan training institutions, with published modules and
                official sources.
              </p>
              {awaitingSelection || !comparators ? (
                <div className="pcd-empty" role="note">{awaitingSelection}</div>
              ) : pendingNote ? (
                pendingNote
              ) : dataStatus !== "ready" ? (
                <DataStatusNote status={dataStatus} />
              ) : (
                <>
                  {comparators.sriLanka.length > 0 && selectedCourse && (
                    <ComparisonCaveatNote courseId={selectedCourse.course_id} />
                  )}
                  <RecordGroup records={comparators.sriLanka} />
                </>
              )}
            </section>
          </div>
        )}

        {activeTab === "international" && (
          <div
            className="pcd-programmes"
            role="tabpanel"
            id="pcd-tabpanel-international"
            aria-labelledby="pcd-tab-international"
          >
            <section className="pcd-panel">
              <h3>International programmes</h3>
              <p className="pcd-panel-description">
                Programmes and standards from developing, emerging, and developed economies, with
                published modules and official sources.
              </p>
              {awaitingSelection || !comparators ? (
                <div className="pcd-empty" role="note">{awaitingSelection}</div>
              ) : pendingNote ? (
                pendingNote
              ) : dataStatus !== "ready" ? (
                <DataStatusNote status={dataStatus} />
              ) : !hasInternational ? (
                <div className="pcd-empty" role="note">{NO_COMPARATORS}</div>
              ) : (
                <>
                  {selectedCourse && <ComparisonCaveatNote courseId={selectedCourse.course_id} />}
                  <RecordGroup title="Developing/Emerging" records={comparators.developingEmerging} />
                  <RecordGroup title="Developed" records={comparators.developed} />
                </>
              )}
            </section>
          </div>
        )}
      </main>
    </div>
  );
}

export default ProgrammeComparisonDashboard;
