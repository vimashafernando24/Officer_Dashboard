import type { RecommendResponse } from "../types";

export function ResultView({ data }: { data: RecommendResponse }) {
  if (data.error) return <div className="simple-alert">We could not generate options: {data.error}</div>;

  return (
    <div className="simple-results" aria-live="polite">
      <section className="flow-section programme-section" aria-labelledby="programme-options-title">
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
              <article className="programme-card" key={programme.course_id}>
                <div className="programme-card-topline">
                  <span className="programme-rank">{programme.rank}</span>
                </div>
                <h3>{programme.course_name}</h3>
                <p className="programme-why">{programme.why_it_may_suit_this_user}</p>
              </article>
            ))}
          </div>
        )}
      </section>
    </div>
  );
}
