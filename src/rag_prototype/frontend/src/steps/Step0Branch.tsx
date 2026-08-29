import { Card, StepTitle, StepHint } from "../components/Card";
import { ChoiceGrid } from "../components/ChoiceGrid";
import inEducationMascot from "../../../../mascots/small/ineducation.png";
import unemployedMascot from "../../../../mascots/small/unemployed.png";
import employedMascot from "../../../../mascots/small/employed.png";
import outsideLabourMascot from "../../../../mascots/small/outsidelabour.png";

const BRANCH_OPTIONS = [
  { code: "D", label: "Currently in education (school, university, or a training programme)" },
  { code: "E", label: "Finished or left education and unemployed or searching for work" },
  { code: "F", label: "Currently employed (in paid work)" },
  { code: "G", label: "Not working, not studying, and not currently searching for work" },
];

const BRANCH_MASCOTS: Record<string, string> = {
  D: inEducationMascot,
  E: unemployedMascot,
  F: employedMascot,
  G: outsideLabourMascot,
};

export function Step0Branch({
  value,
  onSelect,
}: {
  value: string | null;
  onSelect: (branch: string) => void;
}) {
  return (
    <Card>
      <StepTitle>Which best describes the member's current situation?</StepTitle>
      <StepHint>
        Ask the member this directly. It determines which set of cluster-assignment questions
        applies — the same branch logic used for the original 362-respondent study.
      </StepHint>
      <ChoiceGrid
        name="branch"
        options={BRANCH_OPTIONS}
        value={value}
        onChange={onSelect}
        optionImages={BRANCH_MASCOTS}
        tiles
      />
    </Card>
  );
}
