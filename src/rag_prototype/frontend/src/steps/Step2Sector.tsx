import { Card, StepTitle, StepHint } from "../components/Card";
import { MultiChoiceGrid } from "../components/ChoiceGrid";
import { useLocalizer } from "../i18n/languageContext";
import type { Option } from "../types";

export function Step2Sector({
  options,
  value,
  onSelect,
  onBack,
  onNext,
}: {
  options: Option[];
  value: string[];
  onSelect: (code: string) => void;
  onBack: () => void;
  onNext: () => void;
}) {
  const localizer = useLocalizer();
  // Sector codes are the submitted values; only labels change.
  const displayOptions = options.map((option) => ({
    code: option.code,
    label: localizer.sector(option.code, option.label),
  }));
  return (
    <Card>
      <StepTitle>{localizer.t("step2.title")}</StepTitle>
      <StepHint>{localizer.t("step2.hint")}</StepHint>
      <MultiChoiceGrid name="sectors" options={displayOptions} value={value} onChange={(next) => {
        const changed = next.find((code) => !value.includes(code))
          ?? value.find((code) => !next.includes(code));
        if (changed) onSelect(changed);
      }} maxSelected={3} />
      <div className="btn-row">
        <button className="btn-ghost" onClick={onBack}>
          {localizer.t("common.back")}
        </button>
        <button className="btn-primary" disabled={!value.length} onClick={onNext}>
          {localizer.t("common.next")}
        </button>
      </div>
    </Card>
  );
}
