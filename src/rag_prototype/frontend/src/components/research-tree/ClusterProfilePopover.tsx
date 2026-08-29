import { useCallback, useEffect, useLayoutEffect, useRef, useState, type CSSProperties } from "react";
import { createPortal } from "react-dom";
import type { ClusterCatalogueEntry } from "../../types";

interface Props {
  profile: ClusterCatalogueEntry;
  assigned: boolean;
  anchor: SVGGElement;
  container: HTMLDivElement;
  onClose: () => void;
}

interface PopoverPosition {
  left: number;
  top: number;
  width: number;
  tailX: number;
  placement: "above" | "below";
}

function shortCode(code: string) {
  return code.replace(/^Cluster\s+/i, "");
}

function clamp(value: number, minimum: number, maximum: number) {
  return Math.min(Math.max(value, minimum), maximum);
}

export function ClusterProfilePopover({ profile, assigned, anchor, container, onClose }: Props) {
  const bubble = useRef<HTMLDivElement>(null);
  const [position, setPosition] = useState<PopoverPosition | null>(null);
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
    const width = Math.min(360, Math.max(270, containerRect.width - outerPadding * 2), window.innerWidth - outerPadding * 2);
    const height = bubble.current?.offsetHeight ?? 220;
    const anchorX = leafRect.left + leafRect.width / 2;
    const minLeft = Math.max(containerRect.left + outerPadding, outerPadding);
    const maxLeft = Math.max(minLeft, Math.min(containerRect.right, window.innerWidth) - width - outerPadding);
    const left = clamp(anchorX - width / 2, minLeft, maxLeft);

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
    const top = clamp(preferredTop, topBoundary, Math.max(topBoundary, bottomBoundary - height));
    const tailX = clamp(anchorX - left, 34, width - 34);

    setPosition((current) => {
      const next = { left, top, width, tailX, placement };
      return current
        && Math.abs(current.left - next.left) < 0.5
        && Math.abs(current.top - next.top) < 0.5
        && current.width === next.width
        && current.placement === next.placement
        ? current
        : next;
    });
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
  }, [container, updatePosition]);

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

  const style = position ? ({
    left: position.left,
    top: position.top,
    width: position.width,
    "--research-popover-tail-x": `${position.tailX}px`,
  } as CSSProperties) : undefined;

  return createPortal(
    <div
      ref={bubble}
      className={`research-profile-popover is-${position?.placement ?? "above"}${position ? " is-positioned" : ""}`}
      style={style}
      role="dialog"
      aria-labelledby="research-popover-title"
      aria-describedby="research-popover-description"
    >
      <button className="research-popover-close" type="button" onClick={closeAndRestoreFocus} aria-label="Close profile description">×</button>
      <span className="research-popover-code">{shortCode(profile.cluster_code)}</span>
      {assigned ? <span className="research-popover-assigned">Your assigned profile</span> : null}
      <h2 id="research-popover-title">{profile.cluster_name}</h2>
      <p id="research-popover-description">{profile.common_description}</p>
    </div>,
    document.body,
  );
}
