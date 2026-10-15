import type { EvidencePreview, QuestionConfig, RecommendResponse } from "./types";

// Local development keeps using the Flask server. In a Vercel deployment the
// browser talks to the same origin, whose /api routes are served by the small
// Python adapter in the repository root.
const API_BASE = import.meta.env.VITE_API_BASE
  ?? (import.meta.env.DEV ? "http://127.0.0.1:5055" : "");

export async function fetchQuestionConfig(branch: string): Promise<QuestionConfig> {
  const res = await fetch(`${API_BASE}/api/question_config?branch=${encodeURIComponent(branch)}`);
  if (!res.ok) throw new Error(`question_config failed: ${res.status}`);
  return res.json();
}

export interface RecommendPayload {
  branch: string;
  cluster_answers: Record<string, string>;
  ideal_sectors: string[];
  skills_by_sector: Record<string, string[]>;
  q2: string;
  q3: string;
  q4: string;
  q5: string;
}

export async function submitRecommendation(payload: RecommendPayload): Promise<RecommendResponse> {
  const res = await fetch(`${API_BASE}/api/new_person_recommend`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  const data = await res.json();
  return data as RecommendResponse;
}

export async function fetchEvidencePreview(payload: RecommendPayload): Promise<EvidencePreview> {
  const res = await fetch(`${API_BASE}/api/new_person_evidence_preview`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  const data = await res.json();
  if (!res.ok) throw new Error(data.error ?? `evidence preview failed: ${res.status}`);
  return data as EvidencePreview;
}
