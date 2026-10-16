import { useLayoutEffect, useRef, useState } from "react";
import { useLocalizer } from "../../i18n/languageContext";
import type { ClusterCatalogueEntry } from "../../types";
import { ClusterLeaf } from "./ClusterLeaf";
import type { BranchGeometry } from "./treeGeometry";

interface Props {
  geometry: BranchGeometry;
  assignedBranch: string;
  assignedProfiles: Set<string>;
  selectedProfileKeys: Set<string>;
  selectedModelId: string | null;
  onOpenProfile: (profile: ClusterCatalogueEntry, anchor: SVGGElement) => void;
  onOpenDimension: (modelId: string, anchor: SVGGElement) => void;
}

export function ResearchBranch({
  geometry, assignedBranch, assignedProfiles, selectedProfileKeys, selectedModelId, onOpenProfile, onOpenDimension,
}: Props) {
  const localizer = useLocalizer();
  const branchAssigned = geometry.branch.branch_id === assignedBranch;
  const branchLabel = localizer.branchLabel(geometry.branch.branch_id, geometry.branch.branch_label);
  const modelLabels = geometry.models.map((modelGeometry) =>
    localizer.modelLabel(modelGeometry.model.model_id, modelGeometry.model.model_label));
  // Character-count estimates suit Latin text but undershoot Sinhala, so the
  // rendered label widths are measured and plates grow to fit when needed.
  const labelGroup = useRef<SVGGElement>(null);
  const [textWidths, setTextWidths] = useState<Record<string, number>>({});
  const measureKey = [branchLabel, ...modelLabels].join("|");
  useLayoutEffect(() => {
    const group = labelGroup.current;
    const svg = group?.ownerSVGElement;
    if (!group || !svg) return;
    let cancelled = false;
    let frame = 0;
    const measure = () => {
      if (cancelled) return;
      const next: Record<string, number> = {};
      for (const text of group.querySelectorAll<SVGTextElement>("text[data-measure]")) {
        const width = text.getComputedTextLength();
        // A hidden tab reports zero widths; keep the last real measurement.
        if (!width) return;
        next[text.dataset.measure ?? ""] = Math.ceil(width);
      }
      setTextWidths((current) => (JSON.stringify(current) === JSON.stringify(next) ? current : next));
    };
    const schedule = () => {
      window.cancelAnimationFrame(frame);
      frame = window.requestAnimationFrame(measure);
    };
    schedule();
    // Re-measure once fonts arrive and whenever the tree becomes visible again.
    document.fonts?.ready.then(schedule);
    const observer = new ResizeObserver(schedule);
    observer.observe(svg);
    return () => {
      cancelled = true;
      window.cancelAnimationFrame(frame);
      observer.disconnect();
    };
  }, [measureKey]);
  const branchTextWidth = Math.max(textWidths["branch-title"] ?? 0, textWidths["branch-subtitle"] ?? 0);
  const branchPlateWidth = Math.max(
    Math.max(185, Math.min(245, branchLabel.length * 7.4 + 34)),
    branchTextWidth ? branchTextWidth + 28 : 0,
  );
  const preferredBranchLabelX = geometry.labelSide === "left"
    ? geometry.hub.x - branchPlateWidth - 18
    : geometry.hub.x + 18;
  const branchLabelX = Math.max(12, Math.min(preferredBranchLabelX, geometry.treeWidth - branchPlateWidth - 12));
  return (
    <g ref={labelGroup} className={`research-branch${branchAssigned ? " is-route" : ""}`} data-branch={geometry.branch.branch_id}>
      <path className="research-major-limb research-path-base" d={geometry.path} pathLength={1} />
      {branchAssigned ? <path className="research-major-limb research-path-light route-major" d={geometry.path} pathLength={1} /> : null}

      <g className="research-branch-label-group" transform={`translate(${branchLabelX} ${geometry.hub.y - 27})`}>
        <rect width={branchPlateWidth} height="54" rx="12" />
        <text className="research-branch-label" x="13" y="21" data-measure="branch-title">{localizer.t("tree.branch", { id: geometry.branch.branch_id })}</text>
        <text className="research-branch-subtitle" x="13" y="42" data-measure="branch-subtitle">{branchLabel}</text>
      </g>

      {geometry.models.map((modelGeometry, modelIndex) => {
        const modelLabel = modelLabels[modelIndex];
        const measuredModel = textWidths[`model-${modelIndex}`];
        const modelPlateWidth = Math.max(
          Math.max(170, Math.min(260, modelLabel.length * 7.2 + 28)),
          measuredModel ? measuredModel + 26 : 0,
        );
        return (
        <g className="research-model" key={modelGeometry.model.model_id} data-model={modelGeometry.model.model_id}>
          <path className="research-model-limb research-path-base" d={modelGeometry.path} pathLength={1} />
          {branchAssigned ? <path className="research-model-limb research-path-light route-model" d={modelGeometry.path} pathLength={1} /> : null}
          <circle className="research-model-knot" cx={modelGeometry.hub.x} cy={modelGeometry.hub.y} r="5" />

          {modelGeometry.leaves.map((leaf) => {
            const assigned = assignedProfiles.has(leaf.profile.profile_key);
            return (
              <g key={leaf.profile.profile_key}>
                <path className="research-leaf-stem research-path-base" d={leaf.stemPath} pathLength={1} />
                {assigned ? <path className="research-leaf-stem research-path-light route-leaf" d={leaf.stemPath} pathLength={1} /> : null}
                <ClusterLeaf
                  geometry={leaf}
                  assigned={assigned}
                  selected={selectedProfileKeys.has(leaf.profile.profile_key)}
                  onOpen={onOpenProfile}
                />
              </g>
            );
          })}
          <g
            className={`research-model-label-group research-dimension-button${selectedModelId === modelGeometry.model.model_id ? " is-selected" : ""}`}
            transform={`translate(${modelGeometry.hub.x - modelPlateWidth / 2} ${modelGeometry.hub.y + 13})`}
            role="button"
            tabIndex={0}
            aria-label={localizer.t("tree.openMethod", { model: modelLabel })}
            aria-haspopup="dialog"
            aria-expanded={selectedModelId === modelGeometry.model.model_id}
            onClick={(event) => onOpenDimension(modelGeometry.model.model_id, event.currentTarget)}
            onKeyDown={(event) => {
              if (event.key === "Enter" || event.key === " ") {
                event.preventDefault();
                onOpenDimension(modelGeometry.model.model_id, event.currentTarget);
              }
            }}
          >
            <rect width={modelPlateWidth} height="32" rx="10" />
            <text className="research-model-label" x={modelPlateWidth / 2} y="21" textAnchor="middle" data-measure={`model-${modelIndex}`}>{modelLabel}</text>
          </g>
        </g>
      );})}
    </g>
  );
}
