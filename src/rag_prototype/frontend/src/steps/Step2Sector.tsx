import { Card, StepTitle, StepHint } from "../components/Card";
import { MultiChoiceGrid } from "../components/ChoiceGrid";
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
  return (
    <Card>
      <StepTitle>Which sectors interest the member?</StepTitle>
      <StepHint>Select up to three. The next step will ask which skills interest them within each selected sector.</StepHint>
      <MultiChoiceGrid name="sectors" options={options} value={value} onChange={(next) => {
        const changed = next.find((code) => !value.includes(code))
          ?? value.find((code) => !next.includes(code));
        if (changed) onSelect(changed);
      }} maxSelected={3} />
      <div className="btn-row">
        <button className="btn-ghost" onClick={onBack}>
          &larr; back
        </button>
        <button className="btn-primary" disabled={!value.length} onClick={onNext}>
          Next
        </button>
      </div>
    </Card>
  );
}
