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
import { EnglishOnlyNotice, EnglishOriginal } from "../i18n/LanguageControls";
import { useLocalizer } from "../i18n/languageContext";
import type { Localizer } from "../i18n/localize";


const teachingLibrary = teachingLibraryJson as ClusterResearchTeachingLibrary;

// English profile names as they appear inside conclusion sentences, mapped to
// profile keys so the Sinhala profile name can be substituted.
const PROFILE_KEY_BY_NAME = new Map<string, string>();
for (const model of teachingLibrary.models) {
  for (const profile of model.profiles) {
    PROFILE_KEY_BY_NAME.set(profile.canonical_profile_name, profile.profile_key);
    for (const finding of profile.retained_findings) {
      for (const item of finding.distribution.profiles) {
        if (item.profile_key) PROFILE_KEY_BY_NAME.set(item.profile_name, item.profile_key);
      }
    }
  }
}

function localizedConclusion(finding: ClusterResearchTeachingFinding, localizer: Localizer): string | null {
  return localizer.conclusion(finding.simple_conclusion, {
    questionId: finding.survey_question.question_id,
    profileName: (english) => localizer.profileName(PROFILE_KEY_BY_NAME.get(english), english),
  });
}

interface Props {
  assignedProfiles: AssignedProfile[];
}

interface EvidenceModalProps {
  finding: ClusterResearchTeachingFinding;
  profile: ClusterResearchTeachingProfile;
  assignedProfileKeys: ReadonlySet<string>;
  onClose: () => void;
}

function displayMetric(answer: TeachingDistributionAnswer, localizer: Localizer): string {
  if (answer.percentage !== null) {
    const count = answer.count === null ? "" : `${answer.count} · `;
    return `${count}${answer.percentage.toFixed(1)}%`;
  }
  if (answer.value !== null) {
    return answer.iqr ? `${answer.value.toLocaleString()} · IQR ${answer.iqr}` : answer.value.toLocaleString();
  }
  return localizer.t("teaching.notAvailable");
}

function EvidenceModal({ finding, profile, assignedProfileKeys, onClose }: EvidenceModalProps) {
  const dialogRef = useRef<HTMLDialogElement>(null);
  const localizer = useLocalizer();

  useEffect(() => {
    const dialog = dialogRef.current;
    if (!dialog) return;
    dialog.showModal();
    return () => { if (dialog.open) dialog.close(); };
  }, []);

  // The member's box is the one whose profile_key is this assigned profile.
  // Box order is not guaranteed, and the pooled "other profiles" box has no
  // key, so if exactly one box does not match, no badge is shown at all.
  const assignedMatches = finding.distribution.profiles.filter((item) =>
    item.profile_key !== null
    && item.profile_key === profile.profile_key
    && assignedProfileKeys.has(item.profile_key));
  const assignedChartKey = assignedMatches.length === 1 ? assignedMatches[0].profile_key : null;

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
            <span className="section-kicker">{localizer.t("teaching.evidenceKicker")}</span>
            <h3 id="research-evidence-title">{localizer.findingTitle(finding.finding_title)}</h3>
            <p>{localizer.profileName(profile.profile_key, profile.canonical_profile_name)}</p>
          </div>
          <button type="button" className="research-modal-close" onClick={onClose} aria-label={localizer.t("teaching.closeEvidence")}>×</button>
        </header>

        <section className="research-modal-question" aria-labelledby="research-question-label">
          <strong id="research-question-label">{localizer.t("teaching.exactQuestion")}</strong>
          {finding.survey_question.question_text ? (
            <>
              <p>{localizer.surveyQuestion(finding.survey_question.question_id, finding.survey_question.question_text)}</p>
              <EnglishOriginal text={finding.survey_question.question_text} />
            </>
          ) : (
            <p>{localizer.t("teaching.questionMissing")}</p>
          )}
        </section>

        <div className="research-evidence-status-row">
          <span className={`research-status-badge ${finding.evidence_status}`}>
            {localizer.t(finding.evidence_status === "fdr_supported" ? "teaching.fdrSupported" : "teaching.retainedDescriptive")}
          </span>
          <span>{localizer.evidenceText(finding.distribution.note)}</span>
        </div>

        <section className="research-distribution" aria-label={localizer.t("teaching.distributionsLabel")}>
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
            const isAssigned = assignedChartKey !== null && distributionProfile.profile_key === assignedChartKey;
            return (
              <article
                className={`research-profile-chart ${isAssigned ? "is-assigned-cluster" : "is-comparison-group"}`}
                key={distributionProfile.profile_key ?? distributionProfile.profile_name}
              >
                {isAssigned ? (
                  <span className="assigned-cluster-badge">{localizer.t("teaching.assignedClusterBadge")}</span>
                ) : null}
                <div className="research-profile-chart-heading">
                  <h4>{localizer.profileName(distributionProfile.profile_key, distributionProfile.profile_name)}</h4>
                  <span>{distributionProfile.denominator === null ? localizer.t("teaching.denominatorMissing") : `n=${distributionProfile.denominator}`}</span>
                </div>
                <div className="research-category-bars">
                  {answers.map((answer) => {
                    const width = answer.percentage !== null
                      ? answer.percentage
                      : answer.value !== null ? (answer.value / numericMaximum) * 100 : 0;
                    return (
                      <div className="research-category-row" key={answer.answer}>
                        <div>
                          <span>{localizer.answer(answer.answer, { questionId: finding.survey_question.question_id })}</span>
                          <strong>{displayMetric(answer, localizer)}</strong>
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
            <strong>{localizer.t("teaching.readWithCare")}</strong>
            <ul>{finding.cautions.map((caution) => <li key={caution}>{localizer.evidenceText(caution)}</li>)}</ul>
          </section>
        ) : null}

        <details className="research-stat-details">
          <summary>{localizer.t("teaching.statDetails")}</summary>
          <dl>
            <div><dt>{localizer.t("teaching.modelSample")}</dt><dd>{finding.statistics.total_model_n}</dd></div>
            <div><dt>{localizer.t("teaching.eligibleSample")}</dt><dd>{finding.statistics.eligible_n}</dd></div>
            <div><dt>{localizer.t("teaching.coverage")}</dt><dd>{finding.statistics.coverage_pct.toFixed(1)}%</dd></div>
            <div><dt>{localizer.t("teaching.effectSize")}</dt><dd>{finding.statistics.effect_size.toFixed(3)} ({finding.statistics.effect_size_name})</dd></div>
            <div><dt>{localizer.t("teaching.fdrP")}</dt><dd>{finding.statistics.fdr_adjusted_p_value.toPrecision(3)}</dd></div>
          </dl>
        </details>
      </div>
    </dialog>
  );
}

export function ClusterResearchTeachingPanel({ assignedProfiles }: Props) {
  const localizer = useLocalizer();
  const assignedProfileKeys = useMemo(
    () => new Set(assignedProfiles.map((profile) => profile.profile_key)),
    [assignedProfiles],
  );
  const assignedTeachingProfiles = useMemo(() => teachingLibrary.models.flatMap((model) =>
    model.profiles
      .filter((profile) => assignedProfileKeys.has(profile.profile_key))
      .map((profile) => ({ model, profile })),
  ), [assignedProfileKeys]);
  const [selectedModelKey, setSelectedModelKey] = useState(assignedTeachingProfiles[0]?.model.model_key ?? "");
  const [openFinding, setOpenFinding] = useState<ClusterResearchTeachingFinding | null>(null);
  const selected = assignedTeachingProfiles.find((item) => item.model.model_key === selectedModelKey)
    ?? assignedTeachingProfiles[0];

  if (!selected) {
    return <div className="simple-alert">{localizer.t("teaching.noProfile")}</div>;
  }

  return (
    <section className="cluster-teaching-panel" aria-labelledby="cluster-teaching-title">
      <header className="cluster-teaching-header">
        <img src={learningMascot} alt={localizer.t("teaching.mascotAlt")} />
        <div>
          <span className="section-kicker">{localizer.t("teaching.kicker")}</span>
          <h3 id="cluster-teaching-title">{localizer.t("teaching.heading")}</h3>
          <p>{localizer.t("teaching.intro")}</p>
        </div>
      </header>

      {assignedTeachingProfiles.length > 1 ? (
        <div className="cluster-model-tabs" role="tablist" aria-label={localizer.t("teaching.modelsLabel")}>
          {assignedTeachingProfiles.map(({ model }) => (
            <button
              key={model.model_key}
              type="button"
              role="tab"
              aria-selected={selected.model.model_key === model.model_key}
              className={selected.model.model_key === model.model_key ? "is-active" : ""}
              onClick={() => setSelectedModelKey(model.model_key)}
            >
              {localizer.modelLabel(model.model_key, model.model_title)}
            </button>
          ))}
        </div>
      ) : null}

      <div className="cluster-teaching-profile">
        <span className="cluster-teaching-model">{localizer.modelLabel(selected.model.model_key, selected.model.model_title)}</span>
        <div className="cluster-teaching-title-row">
          <h4>{localizer.profileName(selected.profile.profile_key, selected.profile.canonical_profile_name)}</h4>
          <span>{localizer.t("teaching.assignedSize", { n: selected.profile.historical_profile_size })}</span>
        </div>
        <p className="cluster-comparison-summary">
          {localizer.profileSummary(selected.profile.profile_key, selected.profile.comparison_summary)}
        </p>
        <div className="cluster-sibling-list">
          <strong>{localizer.t("teaching.comparedWith")}</strong>
          {selected.profile.sibling_profiles.map((sibling) => (
            <span key={sibling.profile_key}>{localizer.profileName(sibling.profile_key, sibling.canonical_profile_name)} · n={sibling.historical_profile_size}</span>
          ))}
        </div>
      </div>

      {selected.profile.retained_findings.some((finding) => localizedConclusion(finding, localizer) === null) ? (
        <EnglishOnlyNotice>{localizer.t("teaching.conclusionsEnglish")}</EnglishOnlyNotice>
      ) : null}
      <div className="cluster-teaching-findings">
        {selected.profile.retained_findings.map((finding) => (
          <article className="cluster-teaching-finding" key={finding.evidence_id}>
            <div>
              <span className={`research-status-dot ${finding.evidence_status}`} aria-hidden="true" />
              <div>
                <h5>{localizer.findingTitle(finding.finding_title)}</h5>
                {(() => {
                  const conclusion = localizedConclusion(finding, localizer);
                  return <p lang={conclusion === null ? "en" : undefined}>{conclusion ?? finding.simple_conclusion}</p>;
                })()}
              </div>
            </div>
            <button type="button" onClick={() => setOpenFinding(finding)}>{localizer.t("teaching.viewEvidence")}</button>
          </article>
        ))}
      </div>

      <p className="cluster-research-boundary">
        {localizer.t("teaching.boundary")}
      </p>

      {openFinding ? (
        <EvidenceModal
          finding={openFinding}
          profile={selected.profile}
          assignedProfileKeys={assignedProfileKeys}
          onClose={() => setOpenFinding(null)}
        />
      ) : null}
    </section>
  );
}
