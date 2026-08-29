import { Card, StepTitle, StepHint } from "../components/Card";
import { ChoiceGrid } from "../components/ChoiceGrid";
import type { ClusterQuestionGroup } from "../types";

export function Step1ClusterQuestions({
  groups,
  answers,
  onAnswer,
  onBack,
  onNext,
}: {
  groups: ClusterQuestionGroup[];
  answers: Record<string, string>;
  onAnswer: (variable: string, value: string) => void;
  onBack: () => void;
  onNext: () => void;
}) {
  const allVars = groups.flatMap((g) => g.questions.map((q) => q.variable));
  const complete = allVars.every((v) => answers[v] !== undefined && answers[v] !== "");

  return (
    <Card>
      <StepTitle>A few background questions to ask the member</StepTitle>
      <StepHint>
        These are the exact, already-validated cluster-forming questions for this branch — the
        same items the original study used to build these profile models.
      </StepHint>
      {groups.map((g) => (
        <div key={g.model_id}>
          <div className="q-model-badge">{g.model_id.replace(/_/g, " ")}</div>
          {g.questions.map((q) =>
            q.type === "number" ? (
              <div className="q-block" key={q.variable}>
                <div className="q-label">{q.question}</div>
                <input
                  type="number"
                  min={0}
                  value={answers[q.variable] ?? ""}
                  onChange={(e) => onAnswer(q.variable, e.target.value)}
                />
              </div>
            ) : (
              <div className="q-block" key={q.variable}>
                <div className="q-label">{q.question}</div>
                <ChoiceGrid
                  name={q.variable}
                  options={q.options ?? []}
                  value={answers[q.variable] ?? null}
                  onChange={(code) => onAnswer(q.variable, code)}
                />
              </div>
            ),
          )}
        </div>
      ))}
      <div className="btn-row">
        <button className="btn-ghost" onClick={onBack}>
          &larr; back
        </button>
        <button className="btn-primary" disabled={!complete} onClick={onNext}>
          Next
        </button>
      </div>
    </Card>
  );
}
