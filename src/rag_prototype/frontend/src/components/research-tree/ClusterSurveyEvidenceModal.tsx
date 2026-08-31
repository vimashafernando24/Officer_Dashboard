import { useEffect, useId, useRef, type CSSProperties } from "react";
import { createPortal } from "react-dom";
import surveyEvidenceLibraryJson from "../../data/clusterSurveyEvidenceLibrary.json";
import "./ClusterSurveyEvidenceModal.css";

interface EvidenceProfile {
  profile_key: string;
  profile_code: string;
  profile_name: string;
  historical_profile_size: number;
}

interface ProfileValue {
  profile_key: string | null;
  profile_label?: string;
  count: number | null;
  denominator: number;
  percentage: number;
}

interface AnswerDistribution {
  answer: string;
  profile_values: ProfileValue[];
}

interface RetainedContrast {
  source_evidence_id: string;
  answer: string;
  focus_profile_key: string;
  profile_values: ProfileValue[];
}

interface NumericValue {
  profile_key: string;
  denominator: number;
  median: number;
  iqr: string;
}

interface SharedFinding {
  evidence_id: string;
  source_evidence_ids: string[];
  title: string;
  survey_question: string;
  question_id: string;
  evidence_status: "FDR-supported" | "Retained descriptive";
  cautions: string[];
  comparison_type: "full_categorical_distribution" | "retained_category_contrast" | "numeric_summary";
  answer_categories?: string[];
  answer_distribution?: AnswerDistribution[];
  retained_contrasts?: RetainedContrast[];
  numeric_values?: NumericValue[];
  simple_conclusion: string;
}

interface ModelEvidence {
  dimension_title: string;
  profiles: EvidenceProfile[];
  findings: SharedFinding[];
}

interface EvidenceLibrary {
  models: Record<string, ModelEvidence>;
}

const evidenceLibrary = surveyEvidenceLibraryJson as EvidenceLibrary;

interface Props {
  modelKey: string;
  selectedProfileKey: string;
  onClose: () => void;
}

function profileLabel(model: ModelEvidence, profileKey: string | null, fallback?: string) {
  if (!profileKey) return fallback ?? "Other sibling profiles collectively";
  return model.profiles.find((profile) => profile.profile_key === profileKey)?.profile_code ?? fallback ?? profileKey;
}

function numberLabel(value: number) {
  return Number.isInteger(value) ? value.toFixed(0) : value.toFixed(1);
}

function ExactValue({ value, model }: { value: ProfileValue; model: ModelEvidence }) {
  const label = profileLabel(model, value.profile_key, value.profile_label);
  const count = value.count === null ? "count not retained" : `${value.count}/${value.denominator}`;
  return (
    <div className="survey-contrast-value">
      <div><strong>{label}</strong><span>{count}</span></div>
      <div className="survey-contrast-track" aria-hidden="true">
        <span style={{ width: `${value.percentage}%` }} />
      </div>
      <b>{value.percentage.toFixed(1)}%</b>
    </div>
  );
}

function CategoricalChart({ finding, model }: { finding: SharedFinding; model: ModelEvidence }) {
  const distributions = finding.answer_distribution ?? [];
  return (
    <div className="survey-chart-wrap">
      <div className="survey-chart-label">Percentage of profile respondents</div>
      <div
        className="survey-grouped-chart"
        role="img"
        aria-label={`Grouped percentage chart for ${finding.survey_question}`}
      >
        {distributions.map((distribution) => (
          <div className="survey-chart-category" key={distribution.answer}>
            <div className="survey-chart-bars">
              {distribution.profile_values.map((value, index) => {
                const label = profileLabel(model, value.profile_key, value.profile_label);
                return (
                  <div
                    className={`survey-chart-series series-${index + 1}`}
                    key={`${distribution.answer}-${value.profile_key ?? value.profile_label}`}
                    title={`${label}: ${value.percentage.toFixed(1)}% (${value.count ?? "count unavailable"}/${value.denominator})`}
                    style={{ "--bar-height": `${Math.max(value.percentage, 1.5)}%` } as CSSProperties}
                  >
                    <span>{value.percentage.toFixed(1)}%</span>
                    <i aria-hidden="true" />
                  </div>
                );
              })}
            </div>
            <div className="survey-chart-category-label">{distribution.answer}</div>
          </div>
        ))}
      </div>
    </div>
  );
}

function FindingEvidence({ finding, model }: { finding: SharedFinding; model: ModelEvidence }) {
  return (
    <article className="survey-evidence-card">
      <div className="survey-evidence-card-heading">
        <div>
          <span className="survey-evidence-id">Survey question {finding.question_id}</span>
          <h3>{finding.title}</h3>
        </div>
        <span className={`survey-evidence-status${finding.evidence_status === "FDR-supported" ? " is-fdr" : ""}`}>
          {finding.evidence_status}
        </span>
      </div>

      <div className="survey-evidence-question">
        <span>Survey question</span>
        <p>{finding.survey_question}</p>
      </div>

      {finding.comparison_type === "full_categorical_distribution" ? (
        <CategoricalChart finding={finding} model={model} />
      ) : null}

      {finding.comparison_type === "retained_category_contrast" ? (
        <div className="survey-retained-contrasts">
          {(finding.retained_contrasts ?? []).map((contrast) => (
            <section key={contrast.source_evidence_id}>
              <span>Answer compared</span>
              <h4>“{contrast.answer}”</h4>
              <div className="survey-contrast-values">
                {contrast.profile_values.map((value) => (
                  <ExactValue
                    key={`${contrast.source_evidence_id}-${value.profile_key ?? value.profile_label}`}
                    value={value}
                    model={model}
                  />
                ))}
              </div>
            </section>
          ))}
          <small>Only the retained answer comparison is shown; a complete response distribution was not stored.</small>
        </div>
      ) : null}

      {finding.comparison_type === "numeric_summary" ? (
        <div className="survey-numeric-values">
          {(finding.numeric_values ?? []).map((value) => (
            <div key={value.profile_key}>
              <span>{profileLabel(model, value.profile_key)}</span>
              <strong>Median {numberLabel(value.median)}</strong>
              <small>IQR {value.iqr} · n={value.denominator}</small>
            </div>
          ))}
        </div>
      ) : null}

      <p className="survey-evidence-conclusion">{finding.simple_conclusion}</p>
      {finding.cautions.length ? (
        <ul className="survey-evidence-cautions">
          {finding.cautions.map((caution) => <li key={caution}>{caution}</li>)}
        </ul>
      ) : null}
    </article>
  );
}

export function ClusterSurveyEvidenceModal({ modelKey, selectedProfileKey, onClose }: Props) {
  const model = evidenceLibrary.models[modelKey];
  const titleId = useId();
  const closeButton = useRef<HTMLButtonElement>(null);
  const returnFocus = useRef<HTMLElement | null>(null);

  useEffect(() => {
    returnFocus.current = document.activeElement as HTMLElement | null;
    closeButton.current?.focus();
    const onKeyDown = (event: KeyboardEvent) => {
      if (event.key === "Escape") onClose();
    };
    window.addEventListener("keydown", onKeyDown);
    return () => {
      window.removeEventListener("keydown", onKeyDown);
      window.requestAnimationFrame(() => returnFocus.current?.focus());
    };
  }, [onClose]);

  if (!model) return null;
  return createPortal(
    <div
      className="cluster-survey-evidence-layer"
      role="presentation"
      onMouseDown={(event) => { if (event.target === event.currentTarget) onClose(); }}
    >
      <section className="cluster-survey-evidence-modal" role="dialog" aria-modal="true" aria-labelledby={titleId}>
        <button ref={closeButton} className="survey-evidence-close" type="button" onClick={onClose} aria-label="Close survey evidence">×</button>
        <header className="survey-evidence-header">
          <span>Historical profile comparison</span>
          <h2 id={titleId}>{model.dimension_title}</h2>
          <p>This is historical cluster research. It is not a personal answer from the newly assigned member.</p>
        </header>

        <div className="survey-evidence-profiles" aria-label="Profiles compared">
          {model.profiles.map((profile, index) => (
            <div className={`survey-evidence-profile series-${index + 1}${profile.profile_key === selectedProfileKey ? " is-source" : ""}`} key={profile.profile_key}>
              <span>{profile.profile_code}</span>
              <strong>{profile.profile_name}</strong>
              <small>n = {profile.historical_profile_size}</small>
              {profile.profile_key === selectedProfileKey ? <em>Opened from this profile</em> : null}
            </div>
          ))}
        </div>

        <div className="survey-evidence-legend" aria-label="Chart legend">
          {model.profiles.map((profile, index) => (
            <span className={`series-${index + 1}`} key={profile.profile_key}><i aria-hidden="true" />{profile.profile_code}</span>
          ))}
        </div>

        <div className="survey-evidence-findings">
          {model.findings.map((finding) => <FindingEvidence key={finding.evidence_id} finding={finding} model={model} />)}
        </div>
      </section>
    </div>,
    document.body,
  );
}
