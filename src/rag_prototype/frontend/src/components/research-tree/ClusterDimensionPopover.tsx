import { useCallback, useEffect, useLayoutEffect, useRef, useState, type CSSProperties } from "react";
import { createPortal } from "react-dom";
import dimensionLibraryJson from "../../data/clusterDimensionResearchLibrary.json";
import { EnglishOriginal } from "../../i18n/LanguageControls";
import { useLocalizer } from "../../i18n/languageContext";

interface ClusterFormingVariable {
  variable: string;
  variable_key: string;
  survey_question?: string;
}

interface DimensionResearch {
  dimension_title: string;
  description: string;
  historical_sample_size: number;
  profile_count: number;
  profile_sizes: number[];
  cluster_forming_variables: ClusterFormingVariable[];
  validation: {
    silhouette?: number;
    ari?: number;
    pac?: number;
  };
  method?: {
    distance?: string;
    clustering?: string;
  };
}

const dimensionLibrary = dimensionLibraryJson as Record<string, DimensionResearch>;

interface Props {
  modelId: string;
  anchor: SVGGElement;
  container: HTMLDivElement;
  onClose: () => void;
  onViewEvidence: () => void;
}

interface PopoverPosition {
  left: number;
  top: number;
  width: number;
  tailX: number;
  placement: "above" | "below";
}

function clamp(value: number, minimum: number, maximum: number) {
  return Math.min(Math.max(value, minimum), maximum);
}

function metric(value: number) {
  return value.toFixed(3);
}

export function ClusterDimensionPopover({ modelId, anchor, container, onClose, onViewEvidence }: Props) {
  const bubble = useRef<HTMLDivElement>(null);
  const [position, setPosition] = useState<PopoverPosition | null>(null);
  const research = dimensionLibrary[modelId];
  const localizer = useLocalizer();
  const closeAndRestoreFocus = useCallback(() => {
    onClose();
    window.requestAnimationFrame(() => anchor.focus());
  }, [anchor, onClose]);

  const updatePosition = useCallback(() => {
    if (!anchor.isConnected || !container.isConnected) {
      onClose();
      return;
    }
    const anchorRect = anchor.getBoundingClientRect();
    const containerRect = container.getBoundingClientRect();
    const anchorVisible = anchorRect.right >= containerRect.left
      && anchorRect.left <= containerRect.right
      && anchorRect.bottom >= containerRect.top
      && anchorRect.top <= containerRect.bottom;
    if (!anchorVisible) {
      onClose();
      return;
    }

    const outerPadding = 12;
    const gap = 18;
    const width = Math.min(500, Math.max(300, containerRect.width - outerPadding * 2), window.innerWidth - outerPadding * 2);
    const height = bubble.current?.offsetHeight ?? 440;
    const anchorX = anchorRect.left + anchorRect.width / 2;
    const minLeft = Math.max(containerRect.left + outerPadding, outerPadding);
    const maxLeft = Math.max(minLeft, Math.min(containerRect.right, window.innerWidth) - width - outerPadding);
    const left = clamp(anchorX - width / 2, minLeft, maxLeft);
    const topBoundary = Math.max(containerRect.top + outerPadding, outerPadding);
    const bottomBoundary = Math.min(containerRect.bottom - outerPadding, window.innerHeight - outerPadding);
    const aboveTop = anchorRect.top - gap - height;
    const belowTop = anchorRect.bottom + gap;
    const placement: PopoverPosition["placement"] = aboveTop >= topBoundary
      ? "above"
      : belowTop + height <= bottomBoundary ? "below" : "below";
    const preferredTop = placement === "above" ? aboveTop : belowTop;
    const top = clamp(preferredTop, topBoundary, Math.max(topBoundary, bottomBoundary - height));
    const tailX = clamp(anchorX - left, 34, width - 34);
    setPosition({ left, top, width, tailX, placement });
  }, [anchor, container, onClose]);

  useLayoutEffect(() => {
    updatePosition();
    const frame = window.requestAnimationFrame(updatePosition);
    container.addEventListener("scroll", updatePosition, { passive: true });
    window.addEventListener("resize", updatePosition);
    window.addEventListener("scroll", updatePosition, true);
    return () => {
      window.cancelAnimationFrame(frame);
      container.removeEventListener("scroll", updatePosition);
      window.removeEventListener("resize", updatePosition);
      window.removeEventListener("scroll", updatePosition, true);
    };
  }, [container, updatePosition, localizer]);

  useEffect(() => {
    const onPointerDown = (event: PointerEvent) => {
      const target = event.target as Node;
      if (bubble.current?.contains(target) || anchor.contains(target)) return;
      onClose();
    };
    const onKeyDown = (event: KeyboardEvent) => {
      if (event.key === "Escape") closeAndRestoreFocus();
    };
    document.addEventListener("pointerdown", onPointerDown);
    window.addEventListener("keydown", onKeyDown);
    return () => {
      document.removeEventListener("pointerdown", onPointerDown);
      window.removeEventListener("keydown", onKeyDown);
    };
  }, [anchor, closeAndRestoreFocus, onClose]);

  if (!research) return null;
  const style = position ? ({
    left: position.left,
    top: position.top,
    width: position.width,
    "--research-popover-tail-x": `${position.tailX}px`,
  } as CSSProperties) : undefined;

  return createPortal(
    <div
      ref={bubble}
      className={`research-dimension-popover${position ? ` is-positioned is-${position.placement}` : ""}`}
      role="dialog"
      aria-modal="false"
      aria-labelledby="dimension-research-title"
      style={style}
    >
      <button type="button" className="research-popover-close" onClick={closeAndRestoreFocus} aria-label={localizer.t("dimension.close")}>×</button>
      <span className="research-dimension-kicker">{localizer.t("dimension.kicker")}</span>
      <h2 id="dimension-research-title">{localizer.modelLabel(modelId, research.dimension_title)}</h2>

      <section className="research-dimension-section">
        <h3>{localizer.t("dimension.represents")}</h3>
        <p>{localizer.modelDescription(modelId, research.description)}</p>
      </section>

      <section className="research-dimension-section">
        <h3>{localizer.t("dimension.variables")}</h3>
        <ul className="research-dimension-variables">
          {research.cluster_forming_variables.map((variable) => (
            <li key={variable.variable_key}>
              <strong>{localizer.variableName(variable.variable_key, variable.variable)}</strong>
              {variable.survey_question ? <span>{localizer.question(variable.variable_key, variable.survey_question)}</span> : null}
              {variable.survey_question ? <EnglishOriginal text={variable.survey_question} /> : null}
            </li>
          ))}
        </ul>
        <small>{localizer.t("dimension.variablesNote")}</small>
      </section>

      <section className="research-dimension-section">
        <h3>{localizer.t("dimension.model")}</h3>
        <dl className="research-dimension-model-facts">
          <div><dt>{localizer.t("dimension.respondents")}</dt><dd>{research.historical_sample_size}</dd></div>
          <div><dt>{localizer.t("dimension.profiles")}</dt><dd>{research.profile_count}</dd></div>
          <div><dt>{localizer.t("dimension.profileSizes")}</dt><dd>{research.profile_sizes.join(" / ")}</dd></div>
          {research.validation.silhouette !== undefined ? <div><dt>{localizer.t("dimension.separation")}</dt><dd>{metric(research.validation.silhouette)}</dd></div> : null}
          {research.validation.ari !== undefined ? <div><dt>{localizer.t("dimension.stability")}</dt><dd>{metric(research.validation.ari)}</dd></div> : null}
          {research.validation.pac !== undefined ? <div><dt>{localizer.t("dimension.ambiguity")}</dt><dd>{metric(research.validation.pac)}</dd></div> : null}
        </dl>
      </section>

      {research.method?.distance || research.method?.clustering ? (
        <section className="research-dimension-method">
          <h3>{localizer.t("dimension.method")}</h3>
          {research.method.distance ? <p><strong>{localizer.t("dimension.distance")}</strong> <span lang="en">{research.method.distance}</span></p> : null}
          {research.method.clustering ? <p><strong>{localizer.t("dimension.clustering")}</strong> <span lang="en">{research.method.clustering}</span></p> : null}
        </section>
      ) : null}

      <button type="button" className="research-dimension-evidence-button" onClick={onViewEvidence}>
        {localizer.t("dimension.viewEvidence")}
      </button>
    </div>,
    document.body,
  );
}
