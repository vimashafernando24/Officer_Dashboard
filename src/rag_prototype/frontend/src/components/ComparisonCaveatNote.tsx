import { comparatorsForCourse, comparisonCaveat, plainCaveatSummary, technicalCaveatText } from "../programmeBenchmarks";
import { coverageForCourse, coverageStateTitle } from "../programmeCoverage";

/**
 * The course's comparison caveat, or nothing when the course has none: a plain
 * summary built from structured facts, with the stored caveat kept verbatim
 * under "Technical details".
 */
export function ComparisonCaveatNote({ courseId }: { courseId: string }) {
  const caveat = comparisonCaveat(courseId);
  if (!caveat) return null;
  const state = coverageForCourse(courseId)?.state;
  const { sriLanka, developingEmerging, developed } = comparatorsForCourse(courseId);
  const summary =
    state === "FULL_COMPARISON" || state === "COMPARATORS_ONLY"
      ? plainCaveatSummary({
          state,
          records: [...sriLanka, ...developingEmerging, ...developed],
          unstatedCount: caveat.unstated.length,
        })
      : null;

  const technical = (
    <>
      {technicalCaveatText(caveat.text)}
      {caveat.unstated.length > 0 && (
        <>
          {" "}Not stated in the comparator records:{" "}
          {caveat.unstated
            .map(({ record, fields }) => `${fields.join(" and ")} for ${record.title_verbatim} (${record.country})`)
            .join("; ")}
          .
        </>
      )}
    </>
  );

  if (!summary) {
    return <div className="pcd-caveat" role="note"><strong>{technical}</strong></div>;
  }

  return (
    <div className="pcd-caveat" role="note">
      <p className="pcd-caveat-summary">{summary.join(" ")}</p>
      <details className="pcd-caveat-details">
        <summary>Technical details</summary>
        <p className="pcd-caveat-status">Comparison status: {coverageStateTitle(state!)}</p>
        <p className="pcd-caveat-technical">{technical}</p>
      </details>
    </div>
  );
}
