import { useRef, useState } from "react";
import "./App.css";
import { StepProgress } from "./components/StepProgress";
import { Step0Branch } from "./steps/Step0Branch";
import { Step1ClusterQuestions } from "./steps/Step1ClusterQuestions";
import { Step2Sector } from "./steps/Step2Sector";
import { Step3ProgrammeQuestions } from "./steps/Step3ProgrammeQuestions";
import { Step4Review } from "./steps/Step4Review";
import { fetchQuestionConfig, submitRecommendation } from "./api";
import type { IntakeState, QuestionConfig, RecommendResponse } from "./types";
import officerMascot from "../../../mascots/small/rabbit4.png";

const INITIAL_STATE: IntakeState = {
  step: 0,
  branch: null,
  clusterAnswers: {},
  idealSectors: [],
  skillsBySector: {},
  q2: null,
  q3: null,
  q4: null,
  q5: null,
};

function App() {
  const [state, setState] = useState<IntakeState>(INITIAL_STATE);
  const [highestReachedStep, setHighestReachedStep] = useState(0);
  const [config, setConfig] = useState<QuestionConfig | null>(null);
  const [configLoading, setConfigLoading] = useState(false);
  const [result, setResult] = useState<RecommendResponse | null>(null);
  const [submitting, setSubmitting] = useState(false);
  const branchRequestId = useRef(0);
  const recommendationRequestId = useRef(0);

  function invalidateBriefing() {
    recommendationRequestId.current += 1;
    setResult(null);
    setSubmitting(false);
  }

  async function selectBranch(branch: string) {
    if (branch === state.branch && config) {
      goTo(1);
      return;
    }
    const requestId = ++branchRequestId.current;
    invalidateBriefing();
    setConfig(null);
    setHighestReachedStep(0);
    setState({ ...INITIAL_STATE, branch });
    setConfigLoading(true);
    try {
      const cfg = await fetchQuestionConfig(branch);
      if (requestId !== branchRequestId.current) return;
      setConfig(cfg);
      setHighestReachedStep(1);
      setState((s) => (s.branch === branch ? { ...s, step: 1 } : s));
    } finally {
      if (requestId === branchRequestId.current) setConfigLoading(false);
    }
  }

  function setClusterAnswer(variable: string, value: string) {
    invalidateBriefing();
    setState((s) => ({ ...s, clusterAnswers: { ...s.clusterAnswers, [variable]: value } }));
  }

  function toggleIdealSector(code: string) {
    invalidateBriefing();
    setState((state) => {
      if (code === "not sure") {
        const selected = state.idealSectors.includes(code) ? [] : [code];
        return { ...state, idealSectors: selected, skillsBySector: {} };
      }
      const withoutUnsure = state.idealSectors.filter((sector) => sector !== "not sure");
      const removing = withoutUnsure.includes(code);
      const idealSectors = removing
        ? withoutUnsure.filter((sector) => sector !== code)
        : withoutUnsure.length < 3 ? [...withoutUnsure, code] : withoutUnsure;
      const skillsBySector = { ...state.skillsBySector };
      if (removing) delete skillsBySector[code];
      return { ...state, idealSectors, skillsBySector };
    });
  }

  function setSkillsForSector(sector: string, skills: string[]) {
    invalidateBriefing();
    setState((state) => ({
      ...state,
      skillsBySector: { ...state.skillsBySector, [sector]: skills },
    }));
  }

  function setProgrammeAnswer(field: "q2" | "q3" | "q4" | "q5", value: string) {
    invalidateBriefing();
    setState((s) => ({ ...s, [field]: value }));
  }

  function goTo(step: number) {
    setHighestReachedStep((highest) => Math.max(highest, step));
    setState((s) => ({ ...s, step }));
  }

  function reviewSection(step: number) {
    if (step > highestReachedStep || step === state.step) return;
    setState((s) => ({ ...s, step }));
  }

  async function handleSubmit() {
    if (!state.branch || !state.idealSectors.length) return;
    const submittedState = state;
    const submittedBranch = state.branch;
    const submittedIdealSectors = state.idealSectors;
    const requestId = ++recommendationRequestId.current;
    setSubmitting(true);
    setResult(null);
    try {
      const res = await submitRecommendation({
        branch: submittedBranch,
        cluster_answers: submittedState.clusterAnswers,
        ideal_sectors: submittedIdealSectors,
        skills_by_sector: submittedState.skillsBySector,
        q2: submittedState.q2 ?? "",
        q3: submittedState.q3 ?? "",
        q4: submittedState.q4 ?? "",
        q5: submittedState.q5 ?? "",
      });
      if (requestId === recommendationRequestId.current) setResult(res);
    } catch (e) {
      if (requestId === recommendationRequestId.current) {
        setResult({
          error: (e as Error).message,
          branch: submittedBranch,
        } as RecommendResponse);
      }
    } finally {
      if (requestId === recommendationRequestId.current) setSubmitting(false);
    }
  }

  if (state.step === 4 && config) {
    return (
      <Step4Review
        state={state}
        idealSectorOptions={config.ideal_sector_options}
        clusterQuestionGroups={config.cluster_questions}
        onBack={() => goTo(3)}
        onSubmit={handleSubmit}
        loading={submitting}
        result={!result || result.branch === state.branch ? result : null}
      />
    );
  }

  return (
    <div className="app">
      <header className="app-header">
        <div className="app-header-inner">
          <div>
            <div className="product-mark">Youth Circles</div>
            <div className="eyebrow">Youth Services Officer</div>
            <h1>Member intake and programme support</h1>
          </div>
        </div>
        <img className="header-mascot" src={officerMascot} alt="" aria-hidden="true" />
      </header>
      <StepProgress
        step={state.step}
        highestReachedStep={highestReachedStep}
        onNavigate={reviewSection}
      />
      <main className="app-main">
        {state.step === 0 && <Step0Branch value={state.branch} onSelect={selectBranch} />}

        {state.step === 1 && config && !configLoading && (
          <Step1ClusterQuestions
            groups={config.cluster_questions}
            answers={state.clusterAnswers}
            onAnswer={setClusterAnswer}
            onBack={() => goTo(0)}
            onNext={() => goTo(2)}
          />
        )}

        {state.step === 2 && config && (
          <Step2Sector
            options={config.ideal_sector_options}
            value={state.idealSectors}
            onSelect={toggleIdealSector}
            onBack={() => goTo(1)}
            onNext={() => goTo(3)}
          />
        )}

        {state.step === 3 && config && state.idealSectors.length > 0 && (
          <Step3ProgrammeQuestions
            config={config}
            idealSectors={state.idealSectors}
            skillsBySector={state.skillsBySector}
            q2={state.q2}
            q3={state.q3}
            q4={state.q4}
            q5={state.q5}
            onSkillsChange={setSkillsForSector}
            onChange={setProgrammeAnswer}
            onBack={() => goTo(2)}
            onNext={() => goTo(4)}
          />
        )}
      </main>
    </div>
  );
}

export default App;
