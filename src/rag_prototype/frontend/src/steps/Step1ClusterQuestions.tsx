import { Card, StepTitle, StepHint } from "../components/Card";
import { ChoiceGrid } from "../components/ChoiceGrid";
import { HOUSEHOLD_COUNT_MAX, validateNumberAnswers } from "../householdValidation";
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
  const numberVars = groups.flatMap((g) => g.questions.filter((q) => q.type === "number").map((q) => q.variable));
  const numberErrors = validateNumberAnswers(answers, numberVars);
  const valid = Object.keys(numberErrors).length === 0;

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
                  min={q.variable === "household_size" ? 1 : 0}
                  max={HOUSEHOLD_COUNT_MAX}
                  step={1}
                  inputMode="numeric"
                  aria-invalid={numberErrors[q.variable] ? true : undefined}
                  aria-describedby={numberErrors[q.variable] ? `${q.variable}-error` : undefined}
                  className={numberErrors[q.variable] ? "input-invalid" : undefined}
                  value={answers[q.variable] ?? ""}
                  onChange={(e) => onAnswer(q.variable, e.target.value)}
                />
                {numberErrors[q.variable] && (
                  <div className="field-error" id={`${q.variable}-error`} role="alert">
                    {localizer.t(numberErrors[q.variable].key, numberErrors[q.variable].vars)}
                  </div>
                )}
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
                    label: localizer.answer(option.label, { variable: q.variable }),
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
        <button className="btn-primary" disabled={!complete || !valid} onClick={onNext}>
          {localizer.t("common.next")}
        </button>
      </div>
    </Card>
  );
}
