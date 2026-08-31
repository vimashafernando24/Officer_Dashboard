import { useMemo } from "react";
import { Card, StepTitle, StepHint } from "../components/Card";
import { ChoiceGrid, MultiChoiceGrid } from "../components/ChoiceGrid";
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
  const sectorGroups = useMemo(() => {
    const byArea: Record<string, string[]> = JSON.parse(config.q1_options_by_skill_area);
    const labels = new Map(config.ideal_sector_options.map((option) => [option.code, option.label]));
    return idealSectors.map((sector) => {
      const areas = config.sector_bridge[sector] ?? [];
      const names = new Set<string>();
      areas.forEach((area) => (byArea[area] ?? []).forEach((name) => names.add(name)));
      return { sector, label: labels.get(sector) ?? sector, areas, skills: Array.from(names) };
    });
  }, [config, idealSectors]);

  const skillsComplete = sectorGroups.every((group) =>
    group.sector === "not sure" || !group.areas.length || (skillsBySector[group.sector]?.length ?? 0) > 0);
  const complete = skillsComplete && !!q2 && !!q3 && !!q4 && !!q5;

  return (
    <Card>
      <StepTitle>Skills and programme preferences</StepTitle>
      <StepHint>
        Choose up to three skills within each selected sector. These are the member’s own interests and will guide the course shortlist.
      </StepHint>

      {sectorGroups.map((group, index) => (
        <section className="sector-skill-group" key={group.sector} aria-labelledby={`skills-sector-${index}`}>
          <div className="sector-skill-heading">
            <span>Selected sector</span>
            <h3 id={`skills-sector-${index}`}>{group.label}</h3>
            {group.areas.length ? <p>Catalogue area: {group.areas.join(", ")}</p> : null}
          </div>
          {group.skills.length ? (
            <MultiChoiceGrid
              name={`skills-${group.sector}`}
              options={[
                ...group.skills.map((skill) => ({ code: skill, label: skill })),
                { code: NOT_SURE_SKILL, label: NOT_SURE_SKILL },
              ]}
              value={skillsBySector[group.sector] ?? []}
              onChange={(skills) => onSkillsChange(group.sector, skills)}
              maxSelected={3}
              exclusiveOptionCodes={[NOT_SURE_SKILL]}
            />
          ) : group.sector === "not sure" ? (
            <div className="preference-note">No sector-specific skills are required while the member is still exploring.</div>
          ) : (
            <div className="warn-box">No catalogue skills currently map to this sector.</div>
          )}
        </section>
      ))}

      <div className="q-block">
        <div className="q-label">What is the main reason they want this training?</div>
        <ChoiceGrid name="q2" options={config.q2_options.map((o) => ({ code: o, label: o }))} value={q2} onChange={(v) => onChange("q2", v)} />
      </div>
      <div className="q-block">
        <div className="q-label">Which training schedule works best for them?</div>
        <ChoiceGrid name="q3" options={config.q3_options.map((o) => ({ code: o, label: o }))} value={q3} onChange={(v) => onChange("q3", v)} />
      </div>
      <div className="q-block">
        <div className="q-label">Which language would they prefer to study in?</div>
        <ChoiceGrid name="q4" options={config.q4_options.map((o) => ({ code: o, label: o }))} value={q4} onChange={(v) => onChange("q4", v)} />
      </div>
      <div className="q-block">
        <div className="q-label">Is a formal NVQ or qualification important to them?</div>
        <ChoiceGrid name="q5" options={config.q5_options.map((o) => ({ code: o, label: o }))} value={q5} onChange={(v) => onChange("q5", v)} />
      </div>

      <div className="btn-row">
        <button className="btn-ghost" onClick={onBack}>&larr; back</button>
        <button className="btn-primary" disabled={!complete} onClick={onNext}>Review &amp; get briefing</button>
      </div>
    </Card>
  );
}
