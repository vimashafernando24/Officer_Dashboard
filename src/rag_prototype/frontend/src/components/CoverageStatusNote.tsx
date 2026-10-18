import { coverageNote } from "../programmeCoverage";
import type { CourseCoverage } from "../programmeCoverage";

/** Explains why a course has no (full) comparison: research state and NYSC headings, stated separately. */
export function CoverageStatusNote({ coverage }: { coverage: CourseCoverage }) {
  const note = coverageNote(coverage);
  return (
    <div className="pcd-empty pcd-coverage-note" role="note">
      <p><strong>{note.title}</strong></p>
      {note.lines.map((line) => <p key={line}>{line}</p>)}
    </div>
  );
}
