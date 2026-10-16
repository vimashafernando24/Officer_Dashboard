import "./StepProgress.css";
import { useLocalizer } from "../i18n/languageContext";
import type { MessageKey } from "../i18n/messages";

const STEP_NAMES: MessageKey[] = [
  "steps.situation",
  "steps.background",
  "steps.sector",
  "steps.programmeMatch",
  "steps.briefing",
];

interface Props {
  step: number;
  highestReachedStep: number;
  onNavigate: (step: number) => void;
}

export function StepProgress({ step, highestReachedStep, onNavigate }: Props) {
  const localizer = useLocalizer();
  return (
    <nav className="steps-nav" aria-label={localizer.t("steps.navLabel")}>
      {STEP_NAMES.map((nameKey, i) => {
        const name = localizer.t(nameKey);
        const current = i === step;
        const reviewable = i <= highestReachedStep && !current;
        const completed = i < step;
        const previouslyReached = reviewable && i > step;
        const className = `step-item${completed ? " done" : ""}${current ? " active" : ""}${previouslyReached ? " reached" : ""}${reviewable ? " reviewable" : " locked"}`;
        const stateLabel = localizer.t(current ? "steps.current" : reviewable ? "steps.reviewable" : "steps.locked");

        return (
          <button
            key={nameKey}
            type="button"
            className={className}
            aria-current={current ? "step" : undefined}
            aria-label={`${name}, ${stateLabel}`}
            disabled={!reviewable}
            onClick={() => onNavigate(i)}
          >
            <span className={`step-dot${completed ? " done" : current ? " active" : previouslyReached ? " reached" : ""}`} aria-hidden="true" />
            <span className="step-label" data-short-label={i + 1}>
              {name}
            </span>
          </button>
        );
      })}
    </nav>
  );
}
