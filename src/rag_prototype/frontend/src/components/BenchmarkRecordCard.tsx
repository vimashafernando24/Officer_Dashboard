import { useId, useState } from "react";
import {
  RECORD_TYPE_LABELS,
  durationDisplay,
  fidelityLabel,
  groupModules,
  moduleDisclosure,
  modulePreview,
  qualificationDisplay,
  verificationLabel,
} from "../programmeBenchmarks";
import type { BenchmarkModule, BenchmarkRecord } from "../programmeBenchmarks";

function ModuleItems({ modules }: { modules: BenchmarkModule[] }) {
  return (
    <ul>
      {modules.map((module, moduleIndex) => (
        <li key={`${moduleIndex}-${module.title_verbatim}`}>
          {module.code && <code>{module.code}</code>}
          <span>{module.title_verbatim}</span>
          {module.outcome_verbatim && <small>{module.outcome_verbatim}</small>}
        </li>
      ))}
    </ul>
  );
}

export function BenchmarkRecordCard({ record }: { record: BenchmarkRecord }) {
  // Each card keeps its own expansion state.
  const [showAll, setShowAll] = useState(false);
  const listId = useId();
  const fidelity = fidelityLabel(record);
  const duration = durationDisplay(record.duration_as_published);
  const qualification = qualificationDisplay(record);
  const disclosure = moduleDisclosure(record.modules.length, showAll);
  const preview = modulePreview(record.modules, showAll);

  return (
    <article className="pcd-card">
      <div className="pcd-card-tags">
        <span className={`pcd-tag pcd-tag-${record.record_type}`}>
          {RECORD_TYPE_LABELS[record.record_type]}
        </span>
        <span className="pcd-tag pcd-tag-status">{verificationLabel(record)}</span>
      </div>
      <h4>{record.title_verbatim}</h4>
      <p className="pcd-card-institution">{record.institution}</p>

      <dl className="pcd-card-facts">
        <div><dt>Country</dt><dd>{record.country}</dd></div>
        <div>
          <dt>Qualification level</dt>
          <dd>
            {qualification.label}
            {qualification.code && <span className="pcd-card-subtle"> · code {qualification.code}</span>}
            {qualification.framework && <small className="pcd-card-framework">{qualification.framework}</small>}
          </dd>
        </div>
        <div>
          <dt>Duration</dt>
          <dd>
            {duration.summary}
            {duration.details && (
              <details className="pcd-duration-details">
                <summary>Duration details</summary>
                <p>{duration.details}</p>
              </details>
            )}
          </dd>
        </div>
      </dl>

      <a className="pcd-card-source" href={record.source.url} target="_blank" rel="noreferrer">
        Official source
      </a>

      <details className="pcd-modules">
        <summary>
          View Modules / Competencies
          {record.modules.length > 0 && ` (${record.modules.length})`}
        </summary>
        {record.modules.length === 0 ? (
          <p className="pcd-modules-empty">Detailed curriculum not yet available.</p>
        ) : (
          <>
            {fidelity && <p className="pcd-modules-fidelity">{fidelity}</p>}
            <div id={listId}>
              {preview.mode === "core-preview" ? (
                <div className="pcd-module-group pcd-core-preview">
                  <h5>Core competencies — preview</h5>
                  <p className="pcd-preview-note">
                    Showing selected core competencies. View the complete published curriculum for
                    basic, common and core units.
                  </p>
                  <ModuleItems modules={preview.modules} />
                </div>
              ) : (
                groupModules(preview.modules).map(({ group, modules }, index) => (
                  <div className="pcd-module-group" key={`${index}-${group ?? "ungrouped"}`}>
                    {group && <h5>{group}</h5>}
                    <ModuleItems modules={modules} />
                  </div>
                ))
              )}
            </div>
            {disclosure && (
              <button
                type="button"
                className="pcd-modules-toggle"
                aria-expanded={disclosure.ariaExpanded}
                aria-controls={listId}
                onClick={() => setShowAll((value) => !value)}
              >
                {disclosure.label}
              </button>
            )}
          </>
        )}
      </details>
    </article>
  );
}
