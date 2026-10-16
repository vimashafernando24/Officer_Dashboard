import { useState } from "react";
import type { RecommendResponse, SuggestedProgramme } from "../types";
import { ModelReliabilityWarnings } from "./ModelReliabilityWarnings";
import { EnglishOnlyNotice, EnglishOriginal } from "../i18n/LanguageControls";
import { useLocalizer } from "../i18n/languageContext";
import ideaRabbit from "../../../../mascots/small/rabbit3.png";
import discussionRabbit from "../../../../mascots/small/rabbit4.png";

interface MemberAnswer {
  label: string;
  value: string;
}

function ProgrammeCard({ programme }: { programme: SuggestedProgramme }) {
  const [flipped, setFlipped] = useState(false);
  const localizer = useLocalizer();

  return (
    <article className="programme-flip-shell">
      <div className={`programme-flip-card${flipped ? " is-flipped" : ""}`}>
        <div className="programme-card programme-card-front" aria-hidden={flipped}>
          <div className="programme-card-topline">
            <span className="programme-rank">{programme.rank}</span>
          </div>
          <h3>{programme.course_name}</h3>
          <p className="programme-why">{programme.why_it_may_suit_this_user}</p>
          {programme.important_mismatches?.length ? (
            <div className="programme-mismatch-box" role="note" aria-label={localizer.t("result.importantLabel")}>
              <strong>{localizer.t("result.important")}</strong>
              <ul>
                {programme.important_mismatches.map((mismatch) => <li key={mismatch}>{localizer.mismatch(mismatch)}</li>)}
              </ul>
            </div>
          ) : null}
          {programme.cluster_finding_summary ? (
            <details className="cluster-finding-box">
              <summary tabIndex={flipped ? -1 : 0}>
                <img src={ideaRabbit} alt="" aria-hidden="true" />
                <span>
                  <strong>{localizer.t("result.clusterFinding")}</strong>
                  <small>{localizer.t("result.clusterFindingDetail")}</small>
                </span>
                <span className="cluster-finding-toggle" aria-hidden="true">⌄</span>
              </summary>
              <div className="cluster-finding-content">
                <p>{programme.cluster_finding_summary}</p>
                <small>{localizer.t("result.clusterFindingBoundary")}</small>
              </div>
            </details>
          ) : null}
          <button
            type="button"
            className="programme-flip-button"
            tabIndex={flipped ? -1 : 0}
            onClick={() => setFlipped(true)}
            aria-label={localizer.t("result.questionsAria", { course: programme.course_name })}
          >
            {localizer.t("result.questions")} <span aria-hidden="true">↻</span>
          </button>
        </div>

        <div className="programme-card programme-card-back" aria-hidden={!flipped}>
          <div className="programme-back-heading">
            <div>
              <span>{localizer.t("result.discussionKicker")}</span>
              <h3>{programme.course_name}</h3>
              <p>{localizer.t("result.discussionIntro")}</p>
            </div>
            <img src={discussionRabbit} alt="" aria-hidden="true" />
          </div>
          <ol className="programme-question-list">
            {programme.questions_to_discuss.map((question, index) => (
              <li key={index}>
                <span>{index + 1}</span>
                <p>{question}</p>
              </li>
            ))}
          </ol>
          <button
            type="button"
            className="programme-flip-button programme-flip-back"
            tabIndex={flipped ? 0 : -1}
            onClick={() => setFlipped(false)}
            aria-label={localizer.t("result.backAria", { course: programme.course_name })}
          >
            <span aria-hidden="true">↶</span> {localizer.t("result.backToProgramme")}
          </button>
        </div>
      </div>
    </article>
  );
}

export function ResultView({ data, memberAnswers }: { data: RecommendResponse; memberAnswers: MemberAnswer[] }) {
  const localizer = useLocalizer();
  if (data.error) {
    const message = localizer.serviceMessage(data.error);
    return (
      <div className="simple-alert">
        {localizer.t("result.error", { error: message })}
        {message !== data.error ? <EnglishOriginal text={data.error} /> : <EnglishOnlyNotice />}
      </div>
    );
  }
  const noRecommendationReason = data.no_recommendation_reason
    ? localizer.serviceMessage(data.no_recommendation_reason)
    : localizer.t("result.noRecommendation");

  return (
    <div className="simple-results" aria-live="polite">
      <section className="flow-section programme-section" aria-labelledby="programme-options-title">
        <div className="programme-layout">
          <aside className="answers-sidebar">
            <details className="answers-box" open>
              <summary>
                <span>
                  <strong>{localizer.t("result.answersTitle")}</strong>
                  <small>{localizer.t("result.answersDetail")}</small>
                </span>
                <span className="answers-toggle" aria-hidden="true">⌄</span>
              </summary>
              <dl className="answers-content">
                {memberAnswers.map((item, index) => (
                  <div key={index}>
                    <dt>{item.label}</dt>
                    <dd>{item.value}</dd>
                  </div>
                ))}
              </dl>
            </details>
          </aside>

          <div className="programme-main">
            <ModelReliabilityWarnings
              assignedProfiles={data.assigned_profiles}
              catalogue={data.cluster_catalogue}
            />
            <div className="flow-section-heading">
              <span className="step-number">3</span>
              <div>
                <div className="programme-heading-labels">
                  <span className="section-kicker">{localizer.t("result.kicker")}</span>
                  <span className="ai-generated-label">{localizer.t("result.aiLabel")}</span>
                </div>
                <h2 id="programme-options-title">{localizer.t("result.heading")}</h2>
                <p>{localizer.t("result.intro")}</p>
                <EnglishOnlyNotice>{localizer.t("result.aiEnglishNotice")}</EnglishOnlyNotice>
              </div>
            </div>

            {data.recommendation_status === "NO_DEFENSIBLE_RECOMMENDATION" ? (
              <div className="simple-alert">
                {noRecommendationReason}
                {data.no_recommendation_reason && noRecommendationReason !== data.no_recommendation_reason ? (
                  <EnglishOriginal text={data.no_recommendation_reason} />
                ) : null}
              </div>
            ) : (
              <div className="programme-grid">
                {data.suggested_programmes.map((programme) => (
                  <ProgrammeCard programme={programme} key={programme.course_id} />
                ))}
              </div>
            )}
          </div>
        </div>
      </section>
    </div>
  );
}
