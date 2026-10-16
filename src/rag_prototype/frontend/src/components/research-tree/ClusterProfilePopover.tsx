import { useCallback, useEffect, useLayoutEffect, useRef, useState, type CSSProperties } from "react";
import { createPortal } from "react-dom";
import type { ClusterCatalogueEntry } from "../../types";
import profileMeaningLibraryJson from "../../data/clusterProfileMeaningLibrary.json";
import { EnglishOriginal } from "../../i18n/LanguageControls";
import { useLocalizer } from "../../i18n/languageContext";

interface SiblingProfile {
  profile_key: string;
  profile_name: string;
}

interface SummaryEvidence {
  evidence_id: string;
  evidence_status: "fdr_supported" | "retained_descriptive";
}

interface ProfileMeaning {
  model_key: string;
  profile_code: string;
  profile_name: string;
  historical_profile_size: number;
  sibling_profiles: SiblingProfile[];
  comparison_summary: string;
  summary_evidence: SummaryEvidence[];
}

const profileMeaningLibrary = profileMeaningLibraryJson as Record<string, ProfileMeaning>;

interface Props {
  profile: ClusterCatalogueEntry;
  assigned: boolean;
  anchor: SVGGElement;
  container: HTMLDivElement;
  peerIndex: number;
  peerCount: number;
  onClose: () => void;
}

interface PopoverPosition {
  left: number;
  top: number;
  width: number;
  maxHeight?: number;
  tailX: number;
  placement: "above" | "below";
  layout: "single" | "side-by-side" | "stacked";
}

function clamp(value: number, minimum: number, maximum: number) {
  return Math.min(Math.max(value, minimum), maximum);
}

export function ClusterProfilePopover({
  profile, assigned, anchor, container, peerIndex, peerCount, onClose,
}: Props) {
  const bubble = useRef<HTMLDivElement>(null);
  const [position, setPosition] = useState<PopoverPosition | null>(null);
  const meaning = profileMeaningLibrary[profile.profile_key];
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
    const leafRect = anchor.getBoundingClientRect();
    const containerRect = container.getBoundingClientRect();
    const leafVisible = leafRect.right >= containerRect.left
      && leafRect.left <= containerRect.right
      && leafRect.bottom >= containerRect.top
      && leafRect.top <= containerRect.bottom;
    if (!leafVisible) {
      onClose();
      return;
    }

    const outerPadding = 12;
    const gap = 18;
    const viewportLeft = Math.max(containerRect.left, 0) + outerPadding;
    const viewportRight = Math.min(containerRect.right, window.innerWidth) - outerPadding;
    const availableWidth = Math.max(0, viewportRight - viewportLeft);
    const peerGap = 16;
    const sideBySide = peerCount === 2 && availableWidth >= 620;
    const stacked = peerCount === 2 && !sideBySide;
    const width = sideBySide
      ? Math.min(420, (availableWidth - peerGap) / 2)
      : Math.min(440, Math.max(290, containerRect.width - outerPadding * 2), window.innerWidth - outerPadding * 2);
    const height = bubble.current?.offsetHeight ?? 430;
    const anchorX = leafRect.left + leafRect.width / 2;
    const minLeft = Math.max(containerRect.left + outerPadding, outerPadding);
    const maxLeft = Math.max(minLeft, Math.min(containerRect.right, window.innerWidth) - width - outerPadding);
    const groupWidth = width * 2 + peerGap;
    const groupLeft = viewportLeft + Math.max(0, (availableWidth - groupWidth) / 2);
    const left = sideBySide
      ? groupLeft + peerIndex * (width + peerGap)
      : clamp(anchorX - width / 2, minLeft, maxLeft);

    const topBoundary = Math.max(containerRect.top + outerPadding, outerPadding);
    const bottomBoundary = Math.min(containerRect.bottom - outerPadding, window.innerHeight - outerPadding);
    const aboveTop = leafRect.top - gap - height;
    const belowTop = leafRect.bottom + gap;
    const hasRoomAbove = aboveTop >= topBoundary;
    const hasRoomBelow = belowTop + height <= bottomBoundary;
    const placement: PopoverPosition["placement"] = hasRoomAbove
      ? "above"
      : hasRoomBelow
        ? "below"
        : leafRect.top - topBoundary >= bottomBoundary - leafRect.bottom
          ? "above"
          : "below";
    const preferredTop = placement === "above" ? aboveTop : belowTop;
    const stackedHeight = stacked ? Math.max(100, (bottomBoundary - topBoundary - peerGap) / 2) : undefined;
    const top = stacked && stackedHeight !== undefined
      ? topBoundary + peerIndex * (stackedHeight + peerGap)
      : clamp(preferredTop, topBoundary, Math.max(topBoundary, bottomBoundary - height));
    const tailX = clamp(anchorX - left, 34, width - 34);

    setPosition((current) => {
      const next: PopoverPosition = {
        left,
        top,
        width,
        maxHeight: stackedHeight,
        tailX,
        placement,
        layout: sideBySide ? "side-by-side" : stacked ? "stacked" : "single",
      };
      return current
        && Math.abs(current.left - next.left) < 0.5
        && Math.abs(current.top - next.top) < 0.5
        && current.width === next.width
        && current.placement === next.placement
        && current.layout === next.layout
        && current.maxHeight === next.maxHeight
        ? current
        : next;
    });
  }, [anchor, container, onClose, peerCount, peerIndex]);

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
      const element = target instanceof Element ? target : null;
      if (element?.closest(".research-leaf, .research-profile-popover, .cluster-survey-evidence-layer")) return;
      onClose();
    };
    const onKeyDown = (event: KeyboardEvent) => {
      if (event.key === "Escape" && !document.querySelector(".cluster-survey-evidence-layer")) closeAndRestoreFocus();
    };
    document.addEventListener("pointerdown", onPointerDown);
    window.addEventListener("keydown", onKeyDown);
    return () => {
      document.removeEventListener("pointerdown", onPointerDown);
      window.removeEventListener("keydown", onKeyDown);
    };
  }, [anchor, closeAndRestoreFocus, onClose]);

  const style = position ? ({
    left: position.left,
    top: position.top,
    width: position.width,
    maxHeight: position.maxHeight,
    "--research-popover-tail-x": `${position.tailX}px`,
  } as CSSProperties) : undefined;

  if (!meaning) return null;
  const idSuffix = profile.profile_key.replace(/[^a-zA-Z0-9_-]/g, "-");
  const titleId = `research-popover-title-${idSuffix}`;
  const descriptionId = `research-popover-description-${idSuffix}`;
  const siblingLabel = localizer.t(meaning.sibling_profiles.length === 1 ? "profile.comparedOne" : "profile.comparedMany");
  const siblingNames = meaning.sibling_profiles
    .map((sibling) => localizer.profileName(sibling.profile_key, sibling.profile_name))
    .join(" · ");
  const profileName = localizer.profileName(profile.profile_key, meaning.profile_name);

  return createPortal(
    <div
      ref={bubble}
      className={`research-profile-popover is-${position?.placement ?? "above"}${position ? ` is-positioned is-${position.layout}` : ""}`}
      style={style}
      role="dialog"
      aria-labelledby={titleId}
      aria-describedby={descriptionId}
    >
      <button className="research-popover-close" type="button" onClick={closeAndRestoreFocus} aria-label={localizer.t("profile.close")}>×</button>
      <span className="research-popover-code">{meaning.profile_code}</span>
      {assigned ? <span className="research-popover-assigned">{localizer.t("profile.assigned")}</span> : null}
      <h2 id={titleId}>
        {profileName}
        {profileName !== meaning.profile_name ? <EnglishOriginal text={meaning.profile_name} /> : null}
      </h2>
      <p className="research-popover-profile-size">{localizer.t("profile.size")} <strong>{meaning.historical_profile_size}</strong></p>

      <div className="research-popover-comparison">
        <span>{siblingLabel}</span>
        <p>{siblingNames}</p>
      </div>

      <section className="research-popover-meaning">
        <h3>{localizer.t("profile.distinguishes")}</h3>
        <p id={descriptionId}>{localizer.profileSummary(profile.profile_key, meaning.comparison_summary)}</p>
      </section>

    </div>,
    document.body,
  );
}
