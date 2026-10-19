import type { MouseEvent } from "react";
import { courseSummaryFacts, displayModules } from "../programmeComparison";
import type { NyscCourse } from "../programmeComparison";
import { comparatorCounts, comparatorsForCourse } from "../programmeBenchmarks";
import {
  MIN_SUPPORTING_COMPARATORS,
  MIN_SUPPORTING_COUNTRIES,
  SCOPE_LIMITED_DETAILS,
  STATUS_DETAILS,
  investigationAreas,
  mappingForCourse,
  matrixRowId,
} from "../programmeComparisonMatrix";
import { CurriculumComparisonMatrix } from "./CurriculumComparisonMatrix";
import { CoverageStatusNote } from "./CoverageStatusNote";
import { areasUnavailableMessage, coverageForCourse, coveragePresentation } from "../programmeCoverage";
import { ComparisonCaveatNote } from "./ComparisonCaveatNote";

const SELECT_PROMPT = "Select a sector and an NYSC course to begin.";

function plural(count: number, singular: string, pluralForm = `${singular}s`): string {
  return `${count} ${count === 1 ? singular : pluralForm}`;
}

/** Scrolls to and focuses the matching matrix row without changing the URL. */
function showMatrixRow(event: MouseEvent<HTMLAnchorElement>, competencyId: string) {
  const row = document.getElementById(matrixRowId(competencyId));
  if (!row) return;
  event.preventDefault();
  row.scrollIntoView({ behavior: "smooth", block: "center" });
  row.focus({ preventScroll: true });
}

export function ComparisonOverview({
  course,
  dataStatus = "ready",
}: {
  course: NyscCourse | null;
  /** Whether the course's comparator data has loaded; the course summary never waits for it. */
  dataStatus?: "ready" | "loading" | "error";
}) {
  const waiting = dataStatus !== "ready"
    ? (dataStatus === "error"
      ? "Comparison data could not be loaded. Reload the page to try again."
      : "Loading comparison data…")
    : null;
  const modules = course ? displayModules(course) : [];
  const screenshotChecked = modules.flatMap((module, index) =>
    module.verifiedAgainst ? [{ heading: index + 1, file: module.verifiedAgainst.split("/").pop() }] : [],
  );
  const mapping = course ? mappingForCourse(course.course_id) : null;
  const counts = course ? comparatorCounts(comparatorsForCourse(course.course_id)) : null;
  const coverage = course ? coverageForCourse(course.course_id) : null;
  const show = coverage ? coveragePresentation(coverage.state) : null;
  const areas = mapping && show?.showAreas ? investigationAreas(mapping) : [];

  return (
    <>
      <section className="pcd-panel">
        <h3>Selected NYSC Course</h3>
        <p className="pcd-panel-description">Published details from the governed NYSC catalogue.</p>
        {!course ? (
          <div className="pcd-empty" role="note">{SELECT_PROMPT}</div>
        ) : (
          <div className="pcd-course-summary">
            <p className="pcd-course-title">
              <strong>{course.course_name}</strong> <span>{course.course_id}</span>
            </p>
            <dl className="pcd-card-facts">
              {courseSummaryFacts(course).map(({ label, value }) => (
                <div key={label}><dt>{label}</dt><dd>{value}</dd></div>
              ))}
            </dl>
            <h4>Documented module headings</h4>
            {modules.length === 0 ? (
              <p className="pcd-modules-empty">
                The governed catalogue lists no module headings for this course.
              </p>
            ) : (
              <ol className="pcd-course-modules">
                {modules.map((module, index) => (
                  <li key={`${index}-${module.text}`}>
                    {module.text}
                    {module.reviewReason && (
                      <span className="pcd-flag pcd-flag-review" title={module.reviewReason}>Needs review</span>
                    )}
                  </li>
                ))}
              </ol>
            )}
            {(screenshotChecked.length > 0 || modules.some((module) => module.reviewReason)) && (
              <div className="pcd-module-notes">
                {screenshotChecked.map(({ heading, file }) => (
                  <p key={heading}>
                    Heading {heading} was checked against this course's own source screenshot ({file}).
                  </p>
                ))}
                {modules.filter((module) => module.reviewReason).map((module, index) => (
                  <p key={index}>Needs review: “{module.text}”. {module.reviewReason}</p>
                ))}
              </div>
            )}
          </div>
        )}
      </section>

      <section className="pcd-panel">
        <h3>Curriculum Comparison</h3>
        <p className="pcd-panel-description">
          Whether each competency area is named in the stored text of the NYSC course and each linked
          record. Statuses describe published descriptions only, not what is actually taught.
        </p>
        {!course || !counts ? (
          <div className="pcd-empty" role="note">{SELECT_PROMPT}</div>
        ) : waiting ? (
          <div className="pcd-empty" role="status">{waiting}</div>
        ) : (
          <>
            {show?.showComparators && (
              <>
                <ComparisonCaveatNote courseId={course.course_id} />
                <ul className="pcd-counts" aria-label="Comparator records">
                  <li><strong>{counts.sriLanka}</strong> Sri Lankan</li>
                  <li><strong>{counts.developingEmerging}</strong> Developing/Emerging</li>
                  <li><strong>{counts.developed}</strong> Developed</li>
                </ul>
              </>
            )}
            {mapping && show?.showMatrix ? (
              <CurriculumComparisonMatrix mapping={mapping} />
            ) : coverage ? (
              <CoverageStatusNote coverage={coverage} />
            ) : (
              <div className="pcd-empty" role="note">Curriculum comparison not available yet.</div>
            )}
          </>
        )}
      </section>

      <section className="pcd-panel">
        <h3>Areas to Investigate</h3>
        <p className="pcd-panel-description">
          Competencies that at least {MIN_SUPPORTING_COMPARATORS} comparator records, from at
          least {MIN_SUPPORTING_COUNTRIES} countries, document in full but the NYSC course description does not name; partial support is shown but not counted. These are prompts for curriculum review, not
          confirmed skill gaps or labour-market needs.
        </p>
        {!course ? (
          <div className="pcd-empty" role="note">{SELECT_PROMPT}</div>
        ) : waiting ? (
          <div className="pcd-empty" role="status">{waiting}</div>
        ) : !mapping || !show?.showAreas ? (
          <div className="pcd-empty" role="note">
            {coverage ? areasUnavailableMessage(coverage) : "Areas are identified from the curriculum comparison above."}
          </div>
        ) : areas.length === 0 ? (
          <div className="pcd-empty" role="note">
            No competency meets the threshold in the current mapping.
          </div>
        ) : (
          <div className="pcd-matrix-scroll">
            <table className="pcd-areas-table">
              <thead>
                <tr>
                  <th scope="col">Competency area</th>
                  <th scope="col">Supporting comparators</th>
                  <th scope="col">NYSC description</th>
                </tr>
              </thead>
              <tbody>
                {areas.map((area) => (
                  <tr key={area.competency_id}>
                    <th scope="row">
                      <a
                        href={`#${matrixRowId(area.competency_id)}`}
                        onClick={(event) => showMatrixRow(event, area.competency_id)}
                      >
                        {area.label}
                      </a>
                    </th>
                    <td>
                      <strong>
                        {plural(area.supporting_comparators.length, "record")} ·{" "}
                        {plural(area.supporting_countries.length, "country", "countries")}
                      </strong>
                      <small>
                        {area.supporting_comparators.map((name, index) => {
                          const limited = area.scope_limited_comparators.includes(name);
                          return (
                            <span key={name}>
                              {index > 0 && ", "}
                              {name}
                              {limited && (
                                <>
                                  {" "}
                                  <span className="pcd-scope-mark pcd-scope-mark-inline" aria-hidden="true">{SCOPE_LIMITED_DETAILS.symbol}</span>
                                  <span className="pcd-visually-hidden"> (scope-limited)</span>
                                </>
                              )}
                            </span>
                          );
                        })}
                      </small>
                      {area.scope_limited_comparators.length > 0 && (
                        <small>
                          <span className="pcd-scope-mark pcd-scope-mark-inline" aria-hidden="true">{SCOPE_LIMITED_DETAILS.symbol}</span> Scope-limited:
                          the source covers a narrower equipment type or qualification scope (still counted; see the
                          matrix cell for the limitation).
                        </small>
                      )}
                      {area.partial_comparators.length > 0 && (
                        <small>Partial only (not counted): {area.partial_comparators.join(", ")}</small>
                      )}
                    </td>
                    <td>{STATUS_DETAILS[area.nysc_status].label}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </section>
    </>
  );
}
