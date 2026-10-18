import { comparisonCaveat } from "../programmeBenchmarks";

/** The course's comparison caveat, or nothing when the course has none. */
export function ComparisonCaveatNote({ courseId }: { courseId: string }) {
  const caveat = comparisonCaveat(courseId);
  if (!caveat) return null;
  return (
    <div className="pcd-caveat" role="note">
      <strong>{caveat.text}</strong>
      {caveat.unstated.length > 0 && (
        <span>
          {" "}Not stated in the comparator records:{" "}
          {caveat.unstated
            .map(({ record, fields }) => `${fields.join(" and ")} for ${record.title_verbatim} (${record.country})`)
            .join("; ")}
          .
        </span>
      )}
    </div>
  );
}
