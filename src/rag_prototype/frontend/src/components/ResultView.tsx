import { useState } from "react";
import type { RecommendResponse, SuggestedProgramme } from "../types";
import ideaRabbit from "../../../../mascots/small/rabbit3.png";
import discussionRabbit from "../../../../mascots/small/rabbit4.png";

interface MemberAnswer {
  label: string;
  value: string;
}

function ProgrammeCard({ programme }: { programme: SuggestedProgramme }) {
  const [flipped, setFlipped] = useState(false);

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
            <div className="programme-mismatch-box" role="note" aria-label="Important constraints">
              <strong>Important to check</strong>
              <ul>
                {programme.important_mismatches.map((mismatch) => <li key={mismatch}>{mismatch}</li>)}
              </ul>
            </div>
          ) : null}
          {programme.cluster_finding_summary ? (
            <details className="cluster-finding-box">
              <summary tabIndex={flipped ? -1 : 0}>
                <img src={ideaRabbit} alt="" aria-hidden="true" />
                <span>
                  <strong>Cluster finding</strong>
                  <small>See the research context used</small>
                </span>
                <span className="cluster-finding-toggle" aria-hidden="true">⌄</span>
              </summary>
              <div className="cluster-finding-content">
                <p>{programme.cluster_finding_summary}</p>
                <small>Historical group context—not a personal answer from this member.</small>
              </div>
            </details>
          ) : null}
          <button
            type="button"
            className="programme-flip-button"
            tabIndex={flipped ? -1 : 0}
            onClick={() => setFlipped(true)}
            aria-label={`Show questions to discuss for ${programme.course_name}`}
          >
            Questions to discuss <span aria-hidden="true">↻</span>
          </button>
        </div>

        <div className="programme-card programme-card-back" aria-hidden={!flipped}>
          <div className="programme-back-heading">
            <div>
              <span>Officer discussion</span>
              <h3>{programme.course_name}</h3>
              <p>Useful points to clarify with the member before deciding together.</p>
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
            aria-label={`Return to recommendation for ${programme.course_name}`}
          >
            <span aria-hidden="true">↶</span> Back to programme
          </button>
        </div>
      </div>
    </article>
  );
}

export function ResultView({ data, memberAnswers }: { data: RecommendResponse; memberAnswers: MemberAnswer[] }) {
  if (data.error) return <div className="simple-alert">We could not generate options: {data.error}</div>;

  return (
    <div className="simple-results" aria-live="polite">
      <section className="flow-section programme-section" aria-labelledby="programme-options-title">
        <div className="programme-layout">
          <aside className="answers-sidebar">
            <details className="answers-box" open>
              <summary>
                <span>
                  <strong>Member's answers</strong>
                  <small>See the sector, skills and preferences behind these options</small>
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
            <div className="flow-section-heading">
              <span className="step-number">3</span>
              <div>
                <span className="section-kicker">Programme options</span>
                <h2 id="programme-options-title">Options to review together</h2>
                <p>These suggestions combine the member’s answers, course facts and relevant profile context.</p>
              </div>
            </div>

            {data.recommendation_status === "NO_DEFENSIBLE_RECOMMENDATION" ? (
              <div className="simple-alert">{data.no_recommendation_reason ?? "No suitable option could be supported from the available catalogue."}</div>
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
