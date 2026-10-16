import { useMemo, useRef, useState } from "react";
import { TranslationError, translateRecommendations } from "../api";
import { SI_SERVICE_MESSAGES } from "../i18n/siDomain";
import type {
  RecommendationTranslation,
  RecommendationTranslationRequest,
  RecommendResponse,
} from "../types";

export type TranslationStatus = "idle" | "loading" | "ready" | "error";
export type TranslationView = "si" | "en";

interface TranslationState {
  source: RecommendResponse;
  status: TranslationStatus;
  translation: RecommendationTranslation | null;
  errorCode: string | null;
  view: TranslationView;
}

const initialState = (source: RecommendResponse): TranslationState => ({
  source,
  status: "idle",
  translation: null,
  errorCode: null,
  view: "si",
});

/**
 * Only the officer-visible explanation text is sent — never course IDs,
 * ranks, profiles, member answers or the questionnaire. Canonical course
 * names are included so the server can protect them from translation.
 */
export function buildTranslationRequest(data: RecommendResponse): RecommendationTranslationRequest | null {
  if (data.error) return null;
  if (data.recommendation_status === "RECOMMENDATIONS_AVAILABLE" && data.suggested_programmes.length) {
    return {
      programmes: data.suggested_programmes.map((programme) => ({
        course_name: programme.course_name,
        why_it_may_suit_this_user: programme.why_it_may_suit_this_user,
        cluster_finding_summary: programme.cluster_finding_summary ?? null,
        questions_to_discuss: programme.questions_to_discuss,
      })),
      no_recommendation_reason: null,
    };
  }
  const reason = data.no_recommendation_reason;
  // Fixed server messages are already localized by the interface itself.
  if (reason && !Object.hasOwn(SI_SERVICE_MESSAGES, reason)) {
    return { programmes: [], no_recommendation_reason: reason };
  }
  return null;
}

// Defensive client-side check on top of the server's validation.
function matchesRequest(request: RecommendationTranslationRequest, translation: RecommendationTranslation) {
  const filled = (value: unknown) => typeof value === "string" && value.trim().length > 0;
  return (
    translation?.language === "si"
    && Array.isArray(translation.programmes)
    && translation.programmes.length === request.programmes.length
    && translation.programmes.every((item, index) => {
      const source = request.programmes[index];
      return filled(item.why_it_may_suit_this_user)
        && (source.cluster_finding_summary === null) === (item.cluster_finding_summary === null)
        && Array.isArray(item.questions_to_discuss)
        && item.questions_to_discuss.length === source.questions_to_discuss.length
        && item.questions_to_discuss.every(filled);
    })
    && (request.no_recommendation_reason === null || filled(translation.no_recommendation_reason))
  );
}

/**
 * Translation state for exactly one recommendation result. A different
 * result object starts from a clean state, so a new recommendation always
 * clears the previous translation. The English result is never modified.
 */
export function useRecommendationTranslation(data: RecommendResponse) {
  const [state, setState] = useState<TranslationState>(() => initialState(data));
  const inFlightFor = useRef<RecommendResponse | null>(null);
  const request = useMemo(() => buildTranslationRequest(data), [data]);
  const current = state.source === data ? state : initialState(data);

  async function translate() {
    // The ref blocks a second click before React has re-rendered.
    if (!request || inFlightFor.current === data || current.status === "ready") return;
    inFlightFor.current = data;
    setState({ ...initialState(data), status: "loading" });
    try {
      const translation = await translateRecommendations(request);
      if (!matchesRequest(request, translation)) throw new TranslationError("translation_invalid");
      setState((previous) =>
        previous.source === data ? { ...previous, status: "ready", translation, errorCode: null, view: "si" } : previous,
      );
    } catch (error) {
      const code = error instanceof TranslationError ? error.code : "translation_unavailable";
      setState((previous) =>
        previous.source === data ? { ...previous, status: "error", errorCode: code } : previous,
      );
    } finally {
      if (inFlightFor.current === data) inFlightFor.current = null;
    }
  }

  function setView(view: TranslationView) {
    setState((previous) => (previous.source === data ? { ...previous, view } : previous));
  }

  return {
    available: request !== null,
    status: current.status,
    errorCode: current.errorCode,
    view: current.view,
    translation: current.status === "ready" && current.view === "si" ? current.translation : null,
    translate,
    setView,
  };
}
