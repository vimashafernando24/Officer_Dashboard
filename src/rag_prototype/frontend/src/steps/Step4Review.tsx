import { useEffect, useState } from "react";
import { fetchEvidencePreview } from "../api";
import { ClusterResearchTree } from "../components/research-tree/ClusterResearchTree";
import { ResultView } from "../components/ResultView";
import { ClusterResearchTeachingPanel } from "../components/ClusterResearchTeachingPanel";
import { ModelReliabilityWarnings } from "../components/ModelReliabilityWarnings";
import { LanguageSwitch } from "../i18n/LanguageControls";
import { useLocalizer } from "../i18n/languageContext";
import type { ClusterQuestionGroup, EvidencePreview, IntakeState, Option, RecommendResponse } from "../types";
import officerMascot from "../../../../mascots/small/rabbit4.png";
import supportMascot from "../../../../mascots/small/rabbit2.png";
import "./SimpleOfficerFlow.css";

interface Props {
  state: IntakeState;
  idealSectorOptions: Option[];
  clusterQuestionGroups: ClusterQuestionGroup[];
  onBack: () => void;
  onSubmit: () => void;
  loading: boolean;
  result: RecommendResponse | null;
}

type TabId = "profile" | "programmes";

export function Step4Review({ state, idealSectorOptions, onBack, onSubmit, loading, result }: Props) {
  const [preview, setPreview] = useState<EvidencePreview | null>(null);
  const [previewError, setPreviewError] = useState<string | null>(null);
  const [activeTab, setActiveTab] = useState<TabId>("profile");
  const localizer = useLocalizer();

  useEffect(() => {
    if (result) setActiveTab("programmes");
  }, [result]);

  const sectorLabel = (code: string) =>
    localizer.sector(code, idealSectorOptions.find((option) => option.code === code)?.label ?? code);
  const skillLabel = (skill: string) =>
    skill === "Not sure yet" ? localizer.answer(skill) : localizer.skill(skill);
  const preferenceLabel = (value: string | null) =>
    value ? localizer.programmeOption(value) : localizer.t("step4.notStated");

  // Display-only summary. The canonical answers in `state` are sent unchanged.
  const memberAnswers = [
    ...state.idealSectors.map((code) => ({
      label: sectorLabel(code),
      value: state.skillsBySector[code]?.length
        ? state.skillsBySector[code].map(skillLabel).join(", ")
        : localizer.t("step4.noSkill"),
    })),
    { label: localizer.t("step4.answerReason"), value: preferenceLabel(state.q2) },
    { label: localizer.t("step4.answerSchedule"), value: preferenceLabel(state.q3) },
    { label: localizer.t("step4.answerLanguage"), value: preferenceLabel(state.q4) },
    { label: localizer.t("step4.answerQualification"), value: preferenceLabel(state.q5) },
  ];

  useEffect(() => {
    if (!state.branch || !state.idealSectors.length) return;
    let cancelled = false;
    fetchEvidencePreview({
      branch: state.branch,
      cluster_answers: state.clusterAnswers,
      ideal_sectors: state.idealSectors,
      skills_by_sector: state.skillsBySector,
      q2: state.q2 ?? "",
      q3: state.q3 ?? "",
      q4: state.q4 ?? "",
      q5: state.q5 ?? "",
    })
      .then((data) => { if (!cancelled) setPreview(data); })
      .catch((error: Error) => { if (!cancelled) setPreviewError(error.message); });
    return () => { cancelled = true; };
  }, [state]);

  return (
    <div className="simple-officer-app">
      <header className="simple-header">
        <div>
          <span className="simple-brand">Youth Circles</span>
          <span className="simple-product">{localizer.t("app.eyebrow")}</span>
          <h1>{localizer.t("step4.title")}</h1>
        </div>
        <LanguageSwitch />
        <img src={officerMascot} alt="" aria-hidden="true" />
      </header>

      <div className="simple-body">
        <nav className="simple-sidebar" aria-label={localizer.t("step4.workflowLabel")}>
          <button type="button" className="sidebar-tab is-done" onClick={onBack}>
            <span className="sidebar-tab-number">1</span>
            <strong>{localizer.t("step4.tabIntake")}</strong>
          </button>
          <button
            type="button"
            className={`sidebar-tab${activeTab === "profile" ? " is-active" : ""}`}
            onClick={() => setActiveTab("profile")}
          >
            <span className="sidebar-tab-number">2</span>
            <strong>{localizer.t("step4.tabCluster")}</strong>
          </button>
          <button
            type="button"
            className={`sidebar-tab${activeTab === "programmes" ? " is-active" : ""}${!result ? " is-locked" : ""}`}
            onClick={() => setActiveTab("programmes")}
          >
            <span className="sidebar-tab-number">3</span>
            <strong>{localizer.t("step4.tabProgrammes")}</strong>
          </button>
        </nav>

        <main className="simple-main">
          <section
            className="flow-section profile-section"
            aria-labelledby="profile-step-title"
            hidden={activeTab !== "profile"}
          >
              <div className="flow-section-heading">
                <span className="step-number">2</span>
                <div>
                  <span className="section-kicker">{localizer.t("step4.tabCluster")}</span>
                  <h2 id="profile-step-title">{localizer.t("step4.clusterHeading")}</h2>
                  <p>{localizer.t("step4.clusterIntro")}</p>
                </div>
              </div>

              {previewError ? <div className="simple-alert">{localizer.t("step4.previewError", { error: previewError })}</div> : null}
              {!preview && !previewError ? <div className="simple-loading">{localizer.t("step4.assigning")}</div> : null}
              {preview ? (
                <>
                  <ModelReliabilityWarnings
                    assignedProfiles={preview.assigned_profiles}
                    catalogue={preview.cluster_catalogue}
                  />
                  <ClusterResearchTree
                    assignedBranch={preview.branch}
                    assignedProfiles={preview.assigned_profiles}
                    tree={preview.research_tree}
                  />
                  <ClusterResearchTeachingPanel
                    key={preview.assigned_profiles.map((profile) => profile.profile_key).join("|")}
                    assignedProfiles={preview.assigned_profiles}
                  />
                </>
              ) : null}

              <div className="profile-actions">
                <button className="simple-back" type="button" onClick={onBack}>{localizer.t("step4.backToIntake")}</button>
                {!result ? (
                  <div className="generate-action">
                    <img src={supportMascot} alt="" aria-hidden="true" />
                    <div><small>{localizer.t("step4.readyLabel")}</small><span>{localizer.t("step4.readyDetail")}</span></div>
                    <button className="simple-primary" type="button" onClick={onSubmit} disabled={loading || !preview}>
                      {loading ? localizer.t("step4.preparing") : localizer.t("step4.getOptions")}
                    </button>
                  </div>
                ) : (
                  <button className="simple-primary" type="button" onClick={() => setActiveTab("programmes")}>
                    {localizer.t("step4.viewOptions")}
                  </button>
                )}
              </div>
          </section>

          {activeTab !== "profile" && loading ? (
            <div className="simple-loading result-loading">{localizer.t("step4.reviewing")}</div>
          ) : null}

          {activeTab === "programmes" && !loading ? (
            result ? (
              <ResultView data={result} memberAnswers={memberAnswers} />
            ) : (
              <div className="simple-loading">
                {localizer.t("step4.noOptionsYet")}
              </div>
            )
          ) : null}
        </main>
      </div>
    </div>
  );
}
