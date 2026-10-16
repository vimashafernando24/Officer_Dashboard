import { Card, StepTitle, StepHint } from "../components/Card";
import { ChoiceGrid } from "../components/ChoiceGrid";
import { EnglishOnlyNotice, EnglishOriginal } from "../i18n/LanguageControls";
import { useLocalizer } from "../i18n/languageContext";
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
  const localizer = useLocalizer();
  const allVars = groups.flatMap((g) => g.questions.map((q) => q.variable));
  const complete = allVars.every((v) => answers[v] !== undefined && answers[v] !== "");

  return (
    <Card>
      <StepTitle>{localizer.t("step1.title")}</StepTitle>
      <StepHint>{localizer.t("step1.hint")}</StepHint>
      <EnglishOnlyNotice>{localizer.t("step1.translationNote")}</EnglishOnlyNotice>
      {groups.map((g) => (
        <div key={g.model_id}>
          <div className="q-model-badge">{localizer.modelLabel(g.model_id, g.model_id.replace(/_/g, " "))}</div>
          {g.questions.map((q) =>
            q.type === "number" ? (
              <div className="q-block" key={q.variable}>
                <div className="q-label">
                  {localizer.question(q.variable, q.question)}
                  <EnglishOriginal text={q.question} />
                </div>
                <input
                  type="number"
                  min={0}
                  value={answers[q.variable] ?? ""}
                  onChange={(e) => onAnswer(q.variable, e.target.value)}
                />
              </div>
            ) : (
              <div className="q-block" key={q.variable}>
                <div className="q-label">
                  {localizer.question(q.variable, q.question)}
                  <EnglishOriginal text={q.question} />
                </div>
                <ChoiceGrid
                  name={q.variable}
                  options={(q.options ?? []).map((option) => ({
                    code: option.code,
                    label: localizer.answer(option.label),
                  }))}
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
          {localizer.t("common.back")}
        </button>
        <button className="btn-primary" disabled={!complete} onClick={onNext}>
          {localizer.t("common.next")}
        </button>
      </div>
    </Card>
  );
}
