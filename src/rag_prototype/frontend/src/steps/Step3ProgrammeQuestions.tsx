import { useMemo } from "react";
import { Card, StepTitle, StepHint } from "../components/Card";
import { ChoiceGrid, MultiChoiceGrid } from "../components/ChoiceGrid";
import { EnglishOnlyNotice } from "../i18n/LanguageControls";
import { useLocalizer } from "../i18n/languageContext";
import type { QuestionConfig } from "../types";

const NOT_SURE_SKILL = "Not sure yet";

interface Props {
  config: QuestionConfig;
  idealSectors: string[];
  skillsBySector: Record<string, string[]>;
  q2: string | null;
  q3: string | null;
  q4: string | null;
  q5: string | null;
  onSkillsChange: (sector: string, skills: string[]) => void;
  onChange: (field: "q2" | "q3" | "q4" | "q5", value: string) => void;
  onBack: () => void;
  onNext: () => void;
}

export function Step3ProgrammeQuestions({
  config,
  idealSectors,
  skillsBySector,
  q2,
  q3,
  q4,
  q5,
  onSkillsChange,
  onChange,
  onBack,
  onNext,
}: Props) {
  const localizer = useLocalizer();
  // Option codes stay the canonical English values sent to the backend;
  // only the visible labels are localized.
  const programmeOptions = (values: string[]) =>
    values.map((value) => ({ code: value, label: localizer.programmeOption(value) }));
  const sectorGroups = useMemo(() => {
    const byArea: Record<string, string[]> = JSON.parse(config.q1_options_by_skill_area);
    const labels = new Map(config.ideal_sector_options.map((option) => [option.code, option.label]));
    return idealSectors.map((sector) => {
      const areas = config.sector_bridge[sector] ?? [];
      const names = new Set<string>();
      areas.forEach((area) => (byArea[area] ?? []).forEach((name) => names.add(name)));
      (config.sector_extra_skills?.[sector] ?? []).forEach((name) => names.add(name));
      return { sector, label: labels.get(sector) ?? sector, areas, skills: Array.from(names) };
    });
  }, [config, idealSectors]);

  const skillsComplete = sectorGroups.every((group) =>
    group.sector === "not sure" || !group.areas.length || (skillsBySector[group.sector]?.length ?? 0) > 0);
  const complete = skillsComplete && !!q2 && !!q3 && !!q4 && !!q5;

  return (
    <Card>
      <StepTitle>{localizer.t("step3.title")}</StepTitle>
      <StepHint>{localizer.t("step3.hint")}</StepHint>
      <EnglishOnlyNotice>{localizer.t("step3.skillNamesNote")}</EnglishOnlyNotice>

      {sectorGroups.map((group, index) => (
        <section className="sector-skill-group" key={group.sector} aria-labelledby={`skills-sector-${index}`}>
          <div className="sector-skill-heading">
            <span>{localizer.t("step3.selectedSector")}</span>
            <h3 id={`skills-sector-${index}`}>{localizer.sector(group.sector, group.label)}</h3>
            {group.areas.length ? (
              <p>{localizer.t("step3.catalogueArea", { areas: group.areas.map(localizer.skillArea).join(", ") })}</p>
            ) : null}
          </div>
          {group.skills.length ? (
            <MultiChoiceGrid
              name={`skills-${group.sector}`}
              options={[
                ...group.skills.map((skill) => ({ code: skill, label: localizer.skill(skill) })),
                { code: NOT_SURE_SKILL, label: localizer.answer(NOT_SURE_SKILL) },
              ]}
              value={skillsBySector[group.sector] ?? []}
              onChange={(skills) => onSkillsChange(group.sector, skills)}
              maxSelected={3}
              exclusiveOptionCodes={[NOT_SURE_SKILL]}
            />
          ) : group.sector === "not sure" ? (
            <div className="preference-note">{localizer.t("step3.exploringNote")}</div>
          ) : (
            <div className="warn-box">{localizer.t("step3.noSkills")}</div>
          )}
        </section>
      ))}

      <div className="q-block">
        <div className="q-label">{localizer.t("step3.q2")}</div>
        <ChoiceGrid name="q2" options={programmeOptions(config.q2_options)} value={q2} onChange={(v) => onChange("q2", v)} />
      </div>
      <div className="q-block">
        <div className="q-label">{localizer.t("step3.q3")}</div>
        <ChoiceGrid name="q3" options={programmeOptions(config.q3_options)} value={q3} onChange={(v) => onChange("q3", v)} />
      </div>
      <div className="q-block">
        <div className="q-label">{localizer.t("step3.q4")}</div>
        <ChoiceGrid name="q4" options={programmeOptions(config.q4_options)} value={q4} onChange={(v) => onChange("q4", v)} />
      </div>
      <div className="q-block">
        <div className="q-label">{localizer.t("step3.q5")}</div>
        <ChoiceGrid name="q5" options={programmeOptions(config.q5_options)} value={q5} onChange={(v) => onChange("q5", v)} />
      </div>

      <div className="btn-row">
        <button className="btn-ghost" onClick={onBack}>{localizer.t("common.back")}</button>
        <button className="btn-primary" disabled={!complete} onClick={onNext}>{localizer.t("step3.submit")}</button>
      </div>
    </Card>
  );
}
