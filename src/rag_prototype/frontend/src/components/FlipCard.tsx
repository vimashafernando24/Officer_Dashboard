import { useState } from "react";
import "./FlipCard.css";
import { BarChart } from "./BarChart";
import type { Finding } from "../types";
import { findingFeatureName } from "./findingPresentation";

export function FlipCard({ finding }: { finding: Finding }) {
  const [flipped, setFlipped] = useState(false);
  const sq = finding.survey_question;
  const label = findingFeatureName(finding);

  return (
    <div className={`evidence-flip${flipped ? " is-flipped" : ""}`}>
      <button
        type="button"
        className="evidence-flip-button"
        onClick={() => setFlipped((current) => !current)}
        aria-pressed={flipped}
        aria-label={flipped ? `Show the front of ${label}` : `Show the question and chart for ${label}`}
      >
        <span className="evidence-flip-inner">
          <span className="evidence-face evidence-front" aria-hidden={flipped}>
            <span className="evidence-front-kicker">Profile evidence</span>
            <span className="evidence-feature-name">{label}</span>
            <span className="evidence-flip-cue">
              View question <span aria-hidden="true">&#8635;</span>
            </span>
          </span>

          <span className="evidence-face evidence-back" aria-hidden={!flipped}>
            <span className="evidence-back-topline">
              <span className="evidence-back-label">{label}</span>
              <span className="evidence-return-cue" aria-hidden="true">&#8634; Back</span>
            </span>

            <span className="evidence-back-scroll">
              {sq ? (
                <>
                  <span className="evidence-source">
                    Youth Circles survey &middot; Question {sq.question_id}
                  </span>
                  <span className="evidence-question">{sq.question_text}</span>
                </>
              ) : (
                <span className="evidence-source">Validated profile evidence</span>
              )}
              <BarChart dist={finding.distribution} />
            </span>
          </span>
        </span>
      </button>
    </div>
  );
}

export function FindingGrid({ findings }: { findings: Finding[] }) {
  if (!findings.length) return null;
  return (
    <div className="evidence-grid">
      {findings.map((finding, index) => (
        <FlipCard finding={finding} key={`${finding.profile_key}-${finding.variable}-${index}`} />
      ))}
    </div>
  );
}
