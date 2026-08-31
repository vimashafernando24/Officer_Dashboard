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
  const branchAssigned = geometry.branch.branch_id === assignedBranch;
  const branchPlateWidth = Math.max(185, Math.min(245, geometry.branch.branch_label.length * 7.4 + 34));
  const preferredBranchLabelX = geometry.labelSide === "left"
    ? geometry.hub.x - branchPlateWidth - 18
    : geometry.hub.x + 18;
  const branchLabelX = Math.max(12, Math.min(preferredBranchLabelX, geometry.treeWidth - branchPlateWidth - 12));
  return (
    <g className={`research-branch${branchAssigned ? " is-route" : ""}`} data-branch={geometry.branch.branch_id}>
      <path className="research-major-limb research-path-base" d={geometry.path} pathLength={1} />
      {branchAssigned ? <path className="research-major-limb research-path-light route-major" d={geometry.path} pathLength={1} /> : null}

      <g className="research-branch-label-group" transform={`translate(${branchLabelX} ${geometry.hub.y - 27})`}>
        <rect width={branchPlateWidth} height="54" rx="12" />
        <text className="research-branch-label" x="13" y="21">Branch {geometry.branch.branch_id}</text>
        <text className="research-branch-subtitle" x="13" y="42">{geometry.branch.branch_label}</text>
      </g>

      {geometry.models.map((modelGeometry) => {
        const modelPlateWidth = Math.max(170, Math.min(260, modelGeometry.model.model_label.length * 7.2 + 28));
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
            aria-label={`Open research method for ${modelGeometry.model.model_label}`}
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
            <text className="research-model-label" x={modelPlateWidth / 2} y="21" textAnchor="middle">{modelGeometry.model.model_label}</text>
          </g>
        </g>
      );})}
    </g>
  );
}
