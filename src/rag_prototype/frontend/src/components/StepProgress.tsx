import "./StepProgress.css";

const STEP_NAMES = ["Situation", "Background", "Sector", "Programme match", "Briefing"];

export function StepProgress({ step }: { step: number }) {
  return (
    <nav className="steps-nav" aria-label="Intake progress">
      {STEP_NAMES.map((name, i) => (
        <div
          key={name}
          className={`step-item${i < step ? " done" : i === step ? " active" : ""}`}
          aria-current={i === step ? "step" : undefined}
        >
          <span className={`step-dot${i < step ? " done" : i === step ? " active" : ""}`} />
          <span className="step-label" data-short-label={i + 1}>
            {name}
          </span>
        </div>
      ))}
    </nav>
  );
}
