import { Card, StepTitle, StepHint } from "../components/Card";
import { ChoiceGrid } from "../components/ChoiceGrid";
import { useLocalizer } from "../i18n/languageContext";
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
  const localizer = useLocalizer();
  // Branch codes (D/E/F/G) are the submitted values; only labels change.
  const options = BRANCH_OPTIONS.map((option) => ({
    code: option.code,
    label: localizer.branchOption(option.code, option.label),
  }));
  return (
    <Card>
      <StepTitle>{localizer.t("step0.title")}</StepTitle>
      <StepHint>{localizer.t("step0.hint")}</StepHint>
      <ChoiceGrid
        name="branch"
        options={options}
        value={value}
        onChange={onSelect}
        optionImages={BRANCH_MASCOTS}
        tiles
      />
    </Card>
  );
}
