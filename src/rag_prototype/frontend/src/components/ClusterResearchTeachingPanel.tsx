import { useEffect, useMemo, useRef, useState } from "react";
import teachingLibraryJson from "../data/clusterResearchTeachingLibrary.json";
import type {
  AssignedProfile,
  ClusterResearchTeachingFinding,
  ClusterResearchTeachingLibrary,
  ClusterResearchTeachingProfile,
  TeachingDistributionAnswer,
} from "../types";
import learningMascot from "../../../../mascots/small/rabbit1.png";


const teachingLibrary = teachingLibraryJson as ClusterResearchTeachingLibrary;

interface Props {
  assignedProfiles: AssignedProfile[];
}

interface EvidenceModalProps {
  finding: ClusterResearchTeachingFinding;
  profile: ClusterResearchTeachingProfile;
  onClose: () => void;
}

function displayMetric(answer: TeachingDistributionAnswer): string {
  if (answer.percentage !== null) {
    const count = answer.count === null ? "" : `${answer.count} · `;
    return `${count}${answer.percentage.toFixed(1)}%`;
  }
  if (answer.value !== null) {
    return answer.iqr ? `${answer.value.toLocaleString()} · IQR ${answer.iqr}` : answer.value.toLocaleString();
  }
  return "Not available";
}

function EvidenceModal({ finding, profile, onClose }: EvidenceModalProps) {
  const dialogRef = useRef<HTMLDialogElement>(null);

  useEffect(() => {
    const dialog = dialogRef.current;
    if (!dialog) return;
    dialog.showModal();
    return () => { if (dialog.open) dialog.close(); };
  }, []);

  const numericValues = finding.distribution.profiles.flatMap((item) =>
    item.answers.flatMap((answer) => answer.value === null ? [] : [answer.value]),
  );
  const numericMaximum = Math.max(...numericValues, 1) * 1.08;

  return (
    <dialog
      ref={dialogRef}
      className="research-evidence-dialog"
      aria-labelledby="research-evidence-title"
      onCancel={(event) => { event.preventDefault(); onClose(); }}
      onClick={(event) => { if (event.target === event.currentTarget) onClose(); }}
    >
      <div className="research-evidence-modal">
        <header>
          <div>
            <span className="section-kicker">Survey evidence</span>
            <h3 id="research-evidence-title">{finding.finding_title}</h3>
            <p>{profile.canonical_profile_name}</p>
          </div>
          <button type="button" className="research-modal-close" onClick={onClose} aria-label="Close survey evidence">×</button>
        </header>

        <section className="research-modal-question" aria-labelledby="research-question-label">
          <strong id="research-question-label">Exact survey question</strong>
          <p>{finding.survey_question.question_text ?? "Question text was not available in the final manifest."}</p>
        </section>

        <div className="research-evidence-status-row">
          <span className={`research-status-badge ${finding.evidence_status}`}>
            {finding.evidence_status === "fdr_supported" ? "FDR-supported" : "Retained descriptive"}
          </span>
          <span>{finding.distribution.note}</span>
        </div>

        <section className="research-distribution" aria-label="Survey response distributions">
          {finding.distribution.profiles.map((distributionProfile) => {
            const answers = finding.distribution.kind === "numeric_summary"
              ? distributionProfile.answers
              : finding.answer_categories.map((category) => (
                  distributionProfile.answers.find((answer) => answer.answer === category) ?? {
                    answer: category,
                    count: finding.distribution.availability === "complete" ? 0 : null,
                    percentage: finding.distribution.availability === "complete" ? 0 : null,
                    value: null,
                    iqr: null,
                  }
                ));
            return (
              <article className="research-profile-chart" key={distributionProfile.profile_key ?? distributionProfile.profile_name}>
                <div className="research-profile-chart-heading">
                  <h4>{distributionProfile.profile_name}</h4>
                  <span>{distributionProfile.denominator === null ? "Denominator not retained" : `n=${distributionProfile.denominator}`}</span>
                </div>
                <div className="research-category-bars">
                  {answers.map((answer) => {
                    const width = answer.percentage !== null
                      ? answer.percentage
                      : answer.value !== null ? (answer.value / numericMaximum) * 100 : 0;
                    return (
                      <div className="research-category-row" key={answer.answer}>
                        <div>
                          <span>{answer.answer}</span>
                          <strong>{displayMetric(answer)}</strong>
                        </div>
                        <div className="research-category-track" aria-hidden="true">
                          <span style={{ width: `${Math.max(width > 0 ? 2 : 0, width)}%` }} />
                        </div>
                      </div>
                    );
                  })}
                </div>
              </article>
            );
          })}
        </section>

        {finding.cautions.length ? (
          <section className="research-cautions">
            <strong>Read with care</strong>
            <ul>{finding.cautions.map((caution) => <li key={caution}>{caution}</li>)}</ul>
          </section>
        ) : null}

        <details className="research-stat-details">
          <summary>Statistical details</summary>
          <dl>
            <div><dt>Model sample</dt><dd>{finding.statistics.total_model_n}</dd></div>
            <div><dt>Eligible sample</dt><dd>{finding.statistics.eligible_n}</dd></div>
            <div><dt>Coverage</dt><dd>{finding.statistics.coverage_pct.toFixed(1)}%</dd></div>
            <div><dt>Effect size</dt><dd>{finding.statistics.effect_size.toFixed(3)} ({finding.statistics.effect_size_name})</dd></div>
            <div><dt>FDR-adjusted p</dt><dd>{finding.statistics.fdr_adjusted_p_value.toPrecision(3)}</dd></div>
          </dl>
        </details>
      </div>
    </dialog>
  );
}

export function ClusterResearchTeachingPanel({ assignedProfiles }: Props) {
  const assignedTeachingProfiles = useMemo(() => {
    const assignedKeys = new Set(assignedProfiles.map((profile) => profile.profile_key));
    return teachingLibrary.models.flatMap((model) =>
      model.profiles
        .filter((profile) => assignedKeys.has(profile.profile_key))
        .map((profile) => ({ model, profile })),
    );
  }, [assignedProfiles]);
  const [selectedModelKey, setSelectedModelKey] = useState(assignedTeachingProfiles[0]?.model.model_key ?? "");
  const [openFinding, setOpenFinding] = useState<ClusterResearchTeachingFinding | null>(null);
  const selected = assignedTeachingProfiles.find((item) => item.model.model_key === selectedModelKey)
    ?? assignedTeachingProfiles[0];

  if (!selected) {
    return <div className="simple-alert">No reviewed research teaching profile matches this assignment.</div>;
  }

  return (
    <section className="cluster-teaching-panel" aria-labelledby="cluster-teaching-title">
      <header className="cluster-teaching-header">
        <img src={learningMascot} alt="Youth Circles research guide rabbit" />
        <div>
          <span className="section-kicker">Historical cluster research</span>
          <h3 id="cluster-teaching-title">Learn what distinguishes each assigned profile</h3>
          <p>These are findings about earlier survey groups—not answers given by this member.</p>
        </div>
      </header>

      {assignedTeachingProfiles.length > 1 ? (
        <div className="cluster-model-tabs" role="tablist" aria-label="Assigned research models">
          {assignedTeachingProfiles.map(({ model }) => (
            <button
              key={model.model_key}
              type="button"
              role="tab"
              aria-selected={selected.model.model_key === model.model_key}
              className={selected.model.model_key === model.model_key ? "is-active" : ""}
              onClick={() => setSelectedModelKey(model.model_key)}
            >
              {model.model_title}
            </button>
          ))}
        </div>
      ) : null}

      <div className="cluster-teaching-profile">
        <span className="cluster-teaching-model">{selected.model.model_title}</span>
        <div className="cluster-teaching-title-row">
          <h4>{selected.profile.canonical_profile_name}</h4>
          <span>Assigned profile · historical n={selected.profile.historical_profile_size}</span>
        </div>
        <p className="cluster-comparison-summary">{selected.profile.comparison_summary}</p>
        <div className="cluster-sibling-list">
          <strong>Compared with</strong>
          {selected.profile.sibling_profiles.map((sibling) => (
            <span key={sibling.profile_key}>{sibling.canonical_profile_name} · n={sibling.historical_profile_size}</span>
          ))}
        </div>
      </div>

      <div className="cluster-teaching-findings">
        {selected.profile.retained_findings.map((finding) => (
          <article className="cluster-teaching-finding" key={finding.evidence_id}>
            <div>
              <span className={`research-status-dot ${finding.evidence_status}`} aria-hidden="true" />
              <div>
                <h5>{finding.finding_title}</h5>
                <p>{finding.simple_conclusion}</p>
              </div>
            </div>
            <button type="button" onClick={() => setOpenFinding(finding)}>View survey evidence</button>
          </article>
        ))}
      </div>

      <p className="cluster-research-boundary">
        Use these findings to understand the historical profile. Do not treat them as this member’s answers or as programme eligibility rules.
      </p>

      {openFinding ? (
        <EvidenceModal finding={openFinding} profile={selected.profile} onClose={() => setOpenFinding(null)} />
      ) : null}
    </section>
  );
}
