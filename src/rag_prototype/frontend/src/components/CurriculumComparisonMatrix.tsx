import { useState } from "react";
import {
  PARTIAL_DETAILS,
  SCOPE_LIMITED_DETAILS,
  STATUS_DETAILS,
  cellDisplay,
  matrixRowId,
  scopeLimitation,
} from "../programmeComparisonMatrix";
import type { CompetencyCell, CompetencyMapping } from "../programmeComparisonMatrix";

const LEGEND = [
  { key: "DOCUMENTED", ...STATUS_DETAILS.DOCUMENTED },
  { key: "PARTIAL", ...PARTIAL_DETAILS },
  { key: "NOT_EXPLICIT", ...STATUS_DETAILS.NOT_EXPLICIT },
  { key: "INSUFFICIENT_DATA", ...STATUS_DETAILS.INSUFFICIENT_DATA },
];

interface SelectedCell {
  competency: string;
  column: string;
  cell: CompetencyCell;
}

export function CurriculumComparisonMatrix({ mapping }: { mapping: CompetencyMapping }) {
  const [selected, setSelected] = useState<SelectedCell | null>(null);
  const isSelected = (competencyId: string, columnId: string) =>
    selected?.competency === competencyId && selected.column === columnId;

  return (
    <div className="pcd-matrix">
      <ul className="pcd-matrix-legend" aria-label="Status legend">
        {LEGEND.map((item) => (
          <li key={item.key}>
            <span className={`pcd-status pcd-status-${item.key}`} aria-hidden="true">{item.symbol}</span>
            <span><strong>{item.label}:</strong> {item.meaning}</span>
          </li>
        ))}
        <li key="SCOPE_LIMITED">
          <span className="pcd-scope-mark pcd-scope-mark-legend" aria-hidden="true">{SCOPE_LIMITED_DETAILS.symbol}</span>
          <span><strong>{SCOPE_LIMITED_DETAILS.label}:</strong> {SCOPE_LIMITED_DETAILS.meaning}</span>
        </li>
      </ul>
      <p className="pcd-matrix-instruction">Select any cell to see its source text or the reason for its status.</p>

      <p className="pcd-scroll-hint" aria-hidden="true">Scroll sideways to see all {mapping.columns.length} columns →</p>
      <div className="pcd-matrix-scroll" role="region" aria-label="Curriculum comparison matrix" tabIndex={0}>
        <table className="pcd-matrix-table">
          <thead>
            <tr>
              <th scope="col">Competency area</th>
              {mapping.columns.map((column) => (
                <th scope="col" key={column.column_id}>{column.short_label}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {mapping.competencies.map((competency) => (
              <tr key={competency.competency_id} id={matrixRowId(competency.competency_id)} tabIndex={-1}>
                <th scope="row">{competency.label}</th>
                {mapping.columns.map((column) => {
                  const cell = competency.cells[column.column_id];
                  const details = cellDisplay(cell);
                  const limitation = scopeLimitation(cell);
                  return (
                    <td key={column.column_id}>
                      <button
                        type="button"
                        className={`pcd-status pcd-status-${details.key}`}
                        aria-label={`${competency.label}, ${column.short_label}: ${details.label}${limitation ? `. Scope-limited: ${limitation}` : ""}`}
                        aria-pressed={isSelected(competency.competency_id, column.column_id)}
                        title={limitation ? `${details.label} · ${SCOPE_LIMITED_DETAILS.label}` : details.label}
                        onClick={() => setSelected(
                          isSelected(competency.competency_id, column.column_id)
                            ? null
                            : { competency: competency.competency_id, column: column.column_id, cell },
                        )}
                      >
                        {details.symbol}
                        {limitation && <span className="pcd-scope-mark" aria-hidden="true">{SCOPE_LIMITED_DETAILS.symbol}</span>}
                      </button>
                    </td>
                  );
                })}
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <div className="pcd-matrix-detail" aria-live="polite" hidden={!selected}>
        {selected && (
          <>
            <p>
              <strong>{mapping.competencies.find((c) => c.competency_id === selected.competency)?.label}</strong>
              {" · "}
              {mapping.columns.find((c) => c.column_id === selected.column)?.short_label}
              {" · "}
              {cellDisplay(selected.cell).label}
            </p>
            {selected.cell.evidence.length > 0 && (
              <ul>
                {selected.cell.evidence.map((evidence) => (
                  <li key={`${evidence.module_index}-${evidence.field}`}>
                    {evidence.code && <code>{evidence.code}</code>}
                    {evidence.field === "scope_verbatim" && <span className="pcd-flag pcd-flag-scope">Qualification scope</span>}
                    “{evidence.display_text ?? evidence.text}”
                    {evidence.display_text && (
                      <>
                        {" "}<span className="pcd-flag pcd-flag-corrected">Display corrected</span>
                        <small className="pcd-evidence-original">Governed text: “{evidence.text}”</small>
                      </>
                    )}
                  </li>
                ))}
              </ul>
            )}
            {selected.cell.coverage === "PARTIAL" && selected.cell.supported_component && (
              <p className="pcd-matrix-note"><strong>Partial support:</strong> {selected.cell.supported_component}</p>
            )}
            {scopeLimitation(selected.cell) ? (
              <p className="pcd-matrix-note">
                <span className="pcd-flag pcd-flag-scope">{SCOPE_LIMITED_DETAILS.label}</span>
                {scopeLimitation(selected.cell)}
              </p>
            ) : (
              selected.cell.note && <p className="pcd-matrix-note">{selected.cell.note}</p>
            )}
            {(mapping.category_components?.[selected.competency] ?? []).length > 0 && (
              <div className="pcd-matrix-components">
                <p>
                  <strong>Category components.</strong> Documented (full) names every component below;
                  Documented (partial) names only some.
                </p>
                <ul>
                  {mapping.category_components[selected.competency].map((component) => (
                    <li key={component}>{component}</li>
                  ))}
                </ul>
              </div>
            )}
          </>
        )}
      </div>

      {!mapping.human_reviewed && (
        <p className="pcd-matrix-review">Hand-curated mapping, not yet reviewed by a second researcher.</p>
      )}
    </div>
  );
}
