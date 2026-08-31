import "./StepProgress.css";

const STEP_NAMES = ["Situation", "Background", "Sector", "Programme match", "Briefing"];

interface Props {
  step: number;
  highestReachedStep: number;
  onNavigate: (step: number) => void;
}

export function StepProgress({ step, highestReachedStep, onNavigate }: Props) {
  return (
    <nav className="steps-nav" aria-label="Intake progress">
      {STEP_NAMES.map((name, i) => {
        const current = i === step;
        const reviewable = i <= highestReachedStep && !current;
        const completed = i < step;
        const previouslyReached = reviewable && i > step;
        const className = `step-item${completed ? " done" : ""}${current ? " active" : ""}${previouslyReached ? " reached" : ""}${reviewable ? " reviewable" : " locked"}`;
        const stateLabel = current ? "current section" : reviewable ? "available for review" : "not yet available";

        return (
          <button
            key={name}
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
