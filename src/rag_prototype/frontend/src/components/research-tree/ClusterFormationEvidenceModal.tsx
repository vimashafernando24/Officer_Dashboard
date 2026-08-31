import { useEffect, useId, useRef, type CSSProperties } from "react";
import { createPortal } from "react-dom";
import formationLibraryJson from "../../data/clusterFormationEvidenceLibrary.json";
import "./ClusterFormationEvidenceModal.css";

interface ProfileValue {
  profile_key: string;
  count: number;
  denominator: number;
  percentage: number;
}

interface AnswerRow {
  answer: string;
  profile_values: ProfileValue[];
}

interface NumericValue {
  profile_key: string;
  denominator: number;
  observed: number;
  missing: number;
  mean?: number;
  median?: number;
  iqr?: number;
}

interface FormationVariable {
  variable: string;
  display_name: string;
  question_id?: string;
  survey_question?: string;
  provenance: string;
  kind: "categorical" | "numeric_summary" | "unavailable";
  availability: string;
  answer_distribution?: AnswerRow[];
  numeric_values?: NumericValue[];
  note?: string;
}

interface FormationProfile {
  profile_key: string;
  profile_code: string;
  profile_name: string;
  historical_profile_size: number;
}

interface FormationModel {
  model_key: string;
  dimension_title: string;
  source_file: string;
  profiles: FormationProfile[];
  cluster_forming_variables: FormationVariable[];
}

interface FormationLibrary {
  models: Record<string, FormationModel>;
}

const formationLibrary = formationLibraryJson as FormationLibrary;

interface Props {
  modelKey: string;
  onClose: () => void;
}

function percent(value: number) {
  return `${value.toFixed(1)}%`;
}

function number(value: number | undefined) {
  return value === undefined ? "—" : value.toFixed(1);
}

function profileCode(model: FormationModel, key: string) {
  return model.profiles.find((profile) => profile.profile_key === key)?.profile_code ?? key;
}

function CategoricalChart({ variable, model }: { variable: FormationVariable; model: FormationModel }) {
  const rows = variable.answer_distribution ?? [];
  return (
    <div className="formation-chart-wrap">
      <div className="formation-chart-axis-label">Percentage of respondents in each historical profile</div>
      <div
        className={`formation-chart has-${model.profiles.length}-profiles`}
        role="img"
        aria-label={`Response distribution by profile for ${variable.display_name}`}
      >
        {rows.map((row) => (
          <div className="formation-chart-category" key={row.answer}>
            <div className="formation-chart-bars">
              {row.profile_values.map((value, index) => (
                <div
                  className={`formation-chart-bar series-${index + 1}${value.percentage === 0 ? " is-zero" : ""}`}
                  key={value.profile_key}
                  title={`${profileCode(model, value.profile_key)}: ${percent(value.percentage)} (${value.count}/${value.denominator})`}
                  style={{
                    "--bar-height": value.percentage === 0
                      ? "0%"
                      : `${Math.max(value.percentage, 1.5)}%`,
                  } as CSSProperties}
                >
                  <span>{percent(value.percentage)}</span>
                  <i aria-hidden="true" />
                </div>
              ))}
            </div>
            <div className="formation-chart-category-label">{row.answer}</div>
          </div>
        ))}
      </div>
    </div>
  );
}

function NumericSummary({ variable, model }: { variable: FormationVariable; model: FormationModel }) {
  return (
    <div className="formation-numeric-summary" aria-label={`Numeric profile summaries for ${variable.display_name}`}>
      {(variable.numeric_values ?? []).map((value) => (
        <div className="formation-numeric-profile" key={value.profile_key}>
          <strong>{profileCode(model, value.profile_key)}</strong>
          <span>n = {value.denominator} · observed {value.observed}</span>
          <dl>
            <div><dt>Mean</dt><dd>{number(value.mean)}</dd></div>
            <div><dt>Median</dt><dd>{number(value.median)}</dd></div>
            <div><dt>IQR</dt><dd>{number(value.iqr)}</dd></div>
          </dl>
          {value.missing > 0 ? <small>{value.missing} response{value.missing === 1 ? "" : "s"} missing</small> : null}
        </div>
      ))}
    </div>
  );
}

export function ClusterFormationEvidenceModal({ modelKey, onClose }: Props) {
  const model = formationLibrary.models[modelKey];
  const titleId = useId();
  const closeButton = useRef<HTMLButtonElement>(null);

  useEffect(() => {
    closeButton.current?.focus();
    const onKeyDown = (event: KeyboardEvent) => {
      if (event.key === "Escape") onClose();
    };
    window.addEventListener("keydown", onKeyDown);
    return () => window.removeEventListener("keydown", onKeyDown);
  }, [onClose]);

  if (!model) return null;
  return createPortal(
    <div
      className="cluster-formation-evidence-layer"
      role="presentation"
      onMouseDown={(event) => { if (event.target === event.currentTarget) onClose(); }}
    >
      <section className="cluster-formation-evidence-modal" role="dialog" aria-modal="true" aria-labelledby={titleId}>
        <button ref={closeButton} className="formation-evidence-close" type="button" onClick={onClose} aria-label="Close survey evidence">×</button>
        <header className="formation-evidence-header">
          <span>Cluster-forming evidence</span>
          <h2 id={titleId}>{model.dimension_title}</h2>
          <p>These are the survey variables used to form this historical clustering model. The charts show how responses were distributed across the resulting profiles.</p>
        </header>

        <div className="formation-evidence-profiles" aria-label="Profiles compared">
          {model.profiles.map((profile, index) => (
            <div className={`formation-evidence-profile series-${index + 1}`} key={profile.profile_key}>
              <strong>{profile.profile_code}</strong>
              <span>{profile.profile_name}</span>
              <small>Historical profile size: n = {profile.historical_profile_size}</small>
            </div>
          ))}
        </div>
        <div className="formation-evidence-legend" aria-label="Chart legend">
          {model.profiles.map((profile, index) => <span className={`series-${index + 1}`} key={profile.profile_key}><i aria-hidden="true" />{profile.profile_code}</span>)}
        </div>

        <div className="formation-evidence-sections">
          {model.cluster_forming_variables.map((variable) => (
            <article className="formation-evidence-card" key={variable.variable}>
              <header>
                <span>Cluster-forming variable</span>
                <h3>{variable.display_name}</h3>
                {variable.question_id ? <small>Survey question {variable.question_id}</small> : null}
              </header>
              {variable.survey_question ? (
                <div className="formation-evidence-question">
                  <span>Survey question</span>
                  <p>{variable.survey_question}</p>
                </div>
              ) : null}
              {variable.kind === "categorical" ? <CategoricalChart variable={variable} model={model} /> : null}
              {variable.kind === "numeric_summary" ? <NumericSummary variable={variable} model={model} /> : null}
              {variable.kind === "unavailable" ? <p className="formation-evidence-unavailable">No final distribution or profile summary was available for this variable.</p> : null}
              {variable.note ? <small className="formation-evidence-note">{variable.note}</small> : null}
              <small className="formation-evidence-provenance">Source: {variable.provenance}</small>
            </article>
          ))}
        </div>
      </section>
    </div>,
    document.body,
  );
}
