import { useEffect, useState } from "react";
import { fetchEvidencePreview } from "../api";
import { ClusterResearchTree } from "../components/research-tree/ClusterResearchTree";
import { ResultView } from "../components/ResultView";
import { ClusterResearchTeachingPanel } from "../components/ClusterResearchTeachingPanel";
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

  useEffect(() => {
    if (result) setActiveTab("programmes");
  }, [result]);

  const sectorLabel = (code: string) =>
    idealSectorOptions.find((option) => option.code === code)?.label ?? code;

  const memberAnswers = [
    ...state.idealSectors.map((code) => ({
      label: sectorLabel(code),
      value: state.skillsBySector[code]?.length ? state.skillsBySector[code].join(", ") : "No specific skill selected",
    })),
    { label: "Reason for training", value: state.q2 ?? "Not stated" },
    { label: "Schedule preference", value: state.q3 ?? "Not stated" },
    { label: "Language preference", value: state.q4 ?? "Not stated" },
    { label: "Qualification preference", value: state.q5 ?? "Not stated" },
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
          <span className="simple-product">Youth Services Officer</span>
          <h1>Member profile and programme options</h1>
        </div>
        <img src={officerMascot} alt="" aria-hidden="true" />
      </header>

      <div className="simple-body">
        <nav className="simple-sidebar" aria-label="Officer workflow">
          <button type="button" className="sidebar-tab is-done" onClick={onBack}>
            <span className="sidebar-tab-number">1</span>
            <strong>Intake</strong>
          </button>
          <button
            type="button"
            className={`sidebar-tab${activeTab === "profile" ? " is-active" : ""}`}
            onClick={() => setActiveTab("profile")}
          >
            <span className="sidebar-tab-number">2</span>
            <strong>Cluster assignment</strong>
          </button>
          <button
            type="button"
            className={`sidebar-tab${activeTab === "programmes" ? " is-active" : ""}${!result ? " is-locked" : ""}`}
            onClick={() => setActiveTab("programmes")}
          >
            <span className="sidebar-tab-number">3</span>
            <strong>Programme options</strong>
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
                  <span className="section-kicker">Cluster assignment</span>
                  <h2 id="profile-step-title">Branch and cluster assignment</h2>
                  <p>The assignment below uses the existing frozen nearest-match models.</p>
                </div>
              </div>

              {previewError ? <div className="simple-alert">Could not load the profile assignment: {previewError}</div> : null}
              {!preview && !previewError ? <div className="simple-loading">Assigning the profile…</div> : null}
              {preview ? (
                <>
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
                <button className="simple-back" type="button" onClick={onBack}>← Back to intake</button>
                {!result ? (
                  <div className="generate-action">
                    <img src={supportMascot} alt="" aria-hidden="true" />
                    <div><small>Ready for officer review</small><span>Generates concise options and follow-up questions.</span></div>
                    <button className="simple-primary" type="button" onClick={onSubmit} disabled={loading || !preview}>
                      {loading ? "Preparing options…" : "Get programme options"}
                    </button>
                  </div>
                ) : (
                  <button className="simple-primary" type="button" onClick={() => setActiveTab("programmes")}>
                    View programme options →
                  </button>
                )}
              </div>
          </section>

          {activeTab !== "profile" && loading ? (
            <div className="simple-loading result-loading">Reviewing the member’s answers and course catalogue…</div>
          ) : null}

          {activeTab === "programmes" && !loading ? (
            result ? (
              <ResultView data={result} memberAnswers={memberAnswers} />
            ) : (
              <div className="simple-loading">
                No programme options yet — finish the profile step and click “Get programme options”.
              </div>
            )
          ) : null}
        </main>
      </div>
    </div>
  );
}
