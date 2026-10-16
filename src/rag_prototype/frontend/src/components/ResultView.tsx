import { useState } from "react";
import type { ProgrammeTranslation, RecommendResponse, SuggestedProgramme } from "../types";
import { ModelReliabilityWarnings } from "./ModelReliabilityWarnings";
import { EnglishOnlyNotice, EnglishOriginal } from "../i18n/LanguageControls";
import { useLocalizer } from "../i18n/languageContext";
import { createLocalizer } from "../i18n/localize";
import type { MessageKey } from "../i18n/messages";
import { useRecommendationTranslation } from "./useRecommendationTranslation";
import ideaRabbit from "../../../../mascots/small/rabbit3.png";
import discussionRabbit from "../../../../mascots/small/rabbit4.png";

interface MemberAnswer {
  label: string;
  value: string;
}

// The fixed mismatch templates are translated locally (no API call) so the
// Sinhala view is fully Sinhala even when the interface is in English.
const sinhalaLocalizer = createLocalizer("si");

const TRANSLATION_ERRORS: Record<string, MessageKey> = {
  translation_unavailable: "translate.error.unavailable",
  translation_timeout: "translate.error.timeout",
  translation_invalid: "translate.error.invalid",
  invalid_translation_request: "translate.error.request",
};

// Course names, ranks, IDs and mismatch notices always come from the
// English result; only the three AI-written text fields are swapped.
function ProgrammeCard({ programme, translation }: { programme: SuggestedProgramme; translation: ProgrammeTranslation | null }) {
  const textLang = translation ? "si" : "en";
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
          <p className="programme-why" lang={textLang}>{translation?.why_it_may_suit_this_user ?? programme.why_it_may_suit_this_user}</p>
          {programme.important_mismatches?.length ? (
            <div className="programme-mismatch-box" role="note" aria-label={localizer.t("result.importantLabel")}>
              <strong>{localizer.t("result.important")}</strong>
              <ul>
                {programme.important_mismatches.map((mismatch) => (
                  <li key={mismatch} lang={translation ? "si" : undefined}>
                    {(translation ? sinhalaLocalizer : localizer).mismatch(mismatch)}
                  </li>
                ))}
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
                <p lang={textLang}>{translation?.cluster_finding_summary ?? programme.cluster_finding_summary}</p>
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
                <p lang={textLang}>{translation?.questions_to_discuss[index] ?? question}</p>
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

function TranslationControls({ state }: { state: ReturnType<typeof useRecommendationTranslation> }) {
  const localizer = useLocalizer();
  if (!state.available) return null;
  if (state.status === "ready") {
    return (
      <div className="recommendation-translation">
        <div className="translation-view-switch" role="group" aria-label={localizer.t("translate.viewLabel")}>
          <button type="button" lang="si" aria-pressed={state.view === "si"} className={state.view === "si" ? "is-active" : ""} onClick={() => state.setView("si")}>
            {localizer.t("translate.viewSinhala")}
          </button>
          <button type="button" lang="en" aria-pressed={state.view === "en"} className={state.view === "en" ? "is-active" : ""} onClick={() => state.setView("en")}>
            {localizer.t("translate.viewEnglish")}
          </button>
        </div>
        {state.view === "si" ? (
          <p className="translation-notice" role="note">
            <span lang="si">{localizer.t("translate.noticeSinhala")}</span>
            {!localizer.isSinhala ? <span lang="en">{localizer.t("translate.noticeEnglish")}</span> : null}
          </p>
        ) : null}
      </div>
    );
  }
  const loading = state.status === "loading";
  return (
    <div className="recommendation-translation">
      <button
        type="button"
        className="translate-recommendations-button"
        onClick={() => void state.translate()}
        disabled={loading}
        aria-busy={loading}
      >
        {loading ? <span className="translation-spinner" aria-hidden="true" /> : null}
        {localizer.t(loading ? "translate.loading" : "translate.button")}
      </button>
      {state.status === "error" ? (
        <p className="translation-error" role="alert">
          {localizer.t(TRANSLATION_ERRORS[state.errorCode ?? ""] ?? "translate.error.unavailable")}
        </p>
      ) : null}
    </div>
  );
}

export function ResultView({ data, memberAnswers }: { data: RecommendResponse; memberAnswers: MemberAnswer[] }) {
  const localizer = useLocalizer();
  const translationState = useRecommendationTranslation(data);
  const translation = translationState.translation;
  if (data.error) {
    const message = localizer.serviceMessage(data.error);
    return (
      <div className="simple-alert">
        {localizer.t("result.error", { error: message })}
        {message !== data.error ? <EnglishOriginal text={data.error} /> : <EnglishOnlyNotice />}
      </div>
    );
  }
  const noRecommendationReason = translation?.no_recommendation_reason
    ?? (data.no_recommendation_reason
      ? localizer.serviceMessage(data.no_recommendation_reason)
      : localizer.t("result.noRecommendation"));

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
                {translation ? null : <EnglishOnlyNotice>{localizer.t("result.aiEnglishNotice")}</EnglishOnlyNotice>}
              </div>
            </div>
            <TranslationControls state={translationState} />

            {data.recommendation_status === "NO_DEFENSIBLE_RECOMMENDATION" ? (
              <div className="simple-alert" lang={translation?.no_recommendation_reason ? "si" : undefined}>
                {noRecommendationReason}
                {data.no_recommendation_reason && noRecommendationReason !== data.no_recommendation_reason ? (
                  <EnglishOriginal text={data.no_recommendation_reason} />
                ) : null}
              </div>
            ) : (
              <div className="programme-grid">
                {data.suggested_programmes.map((programme, index) => (
                  <ProgrammeCard
                    programme={programme}
                    translation={translation?.programmes[index] ?? null}
                    key={programme.course_id}
                  />
                ))}
              </div>
            )}
          </div>
        </div>
      </section>
    </div>
  );
}
