import { useCallback, useMemo, useState } from "react";
import type { AssignedProfile, ClusterCatalogueEntry, ResearchTreeBranch } from "../../types";
import { ClusterDimensionPopover } from "./ClusterDimensionPopover";
import { ClusterFormationEvidenceModal } from "./ClusterFormationEvidenceModal";
import { ClusterProfilePopover } from "./ClusterProfilePopover";
import { ResearchBranch } from "./ResearchBranch";
import { buildTreeGeometry } from "./treeGeometry";
import "./ClusterResearchTree.css";

interface Props {
  assignedBranch: string;
  assignedProfiles: AssignedProfile[];
  tree: ResearchTreeBranch[];
}

interface LeafSelection {
  profile: ClusterCatalogueEntry;
  anchor: SVGGElement;
}

interface DimensionSelection {
  modelId: string;
  anchor: SVGGElement;
}

interface FormationEvidenceSelection {
  modelId: string;
}

export function ClusterResearchTree({ assignedBranch, assignedProfiles, tree }: Props) {
  const [treeContainer, setTreeContainer] = useState<HTMLDivElement | null>(null);
  const [selectedLeaves, setSelectedLeaves] = useState<LeafSelection[]>([]);
  const [selectedDimension, setSelectedDimension] = useState<DimensionSelection | null>(null);
  const [formationEvidence, setFormationEvidence] = useState<FormationEvidenceSelection | null>(null);
  const assignedKeys = useMemo(
    () => new Set(assignedProfiles.map((profile) => profile.profile_key)),
    [assignedProfiles],
  );
  const assignedByModel = useMemo(
    () => new Map(assignedProfiles.map((profile) => [profile.model_id, profile.profile_key])),
    [assignedProfiles],
  );
  const profileCountByModel = useMemo(
    () => new Map(tree.flatMap((branch) => branch.models.map((model) => [model.model_id, model.profiles.length] as const))),
    [tree],
  );
  const selectedProfileKeys = useMemo(
    () => new Set(selectedLeaves.map((selection) => selection.profile.profile_key)),
    [selectedLeaves],
  );
  const geometry = useMemo(() => buildTreeGeometry(tree), [tree]);
  const closePopover = useCallback((profileKey: string) => {
    setSelectedLeaves((current) => current.filter((selection) => selection.profile.profile_key !== profileKey));
  }, []);
  const closeDimensionPopover = useCallback(() => setSelectedDimension(null), []);
  const openFormationEvidence = useCallback((modelId: string) => {
    setSelectedDimension(null);
    setFormationEvidence({ modelId });
  }, []);
  const closeFormationEvidence = useCallback(() => setFormationEvidence(null), []);
  const openProfile = useCallback((profile: ClusterCatalogueEntry, anchor: SVGGElement) => {
    setSelectedLeaves((current) => {
      if (current.some((selection) => selection.profile.profile_key === profile.profile_key)) {
        return current.filter((selection) => selection.profile.profile_key !== profile.profile_key);
      }
      const next = { profile, anchor };
      if (!current.length || current[0].profile.model_id !== profile.model_id) return [next];
      if ((profileCountByModel.get(profile.model_id) ?? 0) === 2) return [...current, next].slice(-2);

      const assignedKey = assignedByModel.get(profile.model_id);
      const openAssigned = current.find((selection) => selection.profile.profile_key === assignedKey);
      if (profile.profile_key === assignedKey) {
        const comparison = current.find((selection) => selection.profile.profile_key !== assignedKey);
        return comparison ? [next, comparison] : [next];
      }
      return openAssigned ? [openAssigned, next] : [next];
    });
  }, [assignedByModel, profileCountByModel]);
  const openDimension = useCallback((modelId: string, anchor: SVGGElement) => {
    setSelectedDimension((current) => current?.modelId === modelId ? null : { modelId, anchor });
  }, []);

  return (
    <section className="research-tree-panel" aria-labelledby="research-tree-title">
      <div className="research-tree-heading">
        <div>
          <span className="section-kicker">Complete research map</span>
          <h2 id="research-tree-title">Where this member fits</h2>
          <p>All retained branches and profiles are visible. The illuminated route shows this member’s assignment.</p>
        </div>
        <div className="research-tree-legend" aria-label="Tree legend">
          <span><i className="legend-route" aria-hidden="true" />Assigned route</span>
          <span><i className="legend-leaf" aria-hidden="true" />Assigned profile</span>
        </div>
      </div>

      <div ref={setTreeContainer} className="research-tree-scroll" tabIndex={0} aria-label="Scrollable complete cluster research tree">
        <svg
          className="research-tree-svg"
          viewBox={geometry.viewBox}
          width={geometry.width}
          height={geometry.height}
          role="img"
          aria-labelledby="research-tree-svg-title research-tree-svg-desc"
        >
          <title id="research-tree-svg-title">Complete Youth Circles cluster research tree</title>
          <desc id="research-tree-svg-desc">Branches D, E, F and G and all seventeen retained profiles. The member’s assigned route is highlighted.</desc>
          <defs>
            <linearGradient id="trunkGradient" x1="0" y1="0" x2="1" y2="0">
              <stop offset="0" stopColor="#755b43" />
              <stop offset=".55" stopColor="#9a7956" />
              <stop offset="1" stopColor="#806247" />
            </linearGradient>
            <filter id="routeGlow" x="-60%" y="-60%" width="220%" height="220%">
              <feGaussianBlur stdDeviation="1.8" result="blur" />
              <feMerge><feMergeNode in="blur" /><feMergeNode in="SourceGraphic" /></feMerge>
            </filter>
            <radialGradient id="leafGradient" cx="35%" cy="30%" r="75%">
              <stop offset="0" stopColor="#c7e0b4" />
              <stop offset=".6" stopColor="#9dc082" />
              <stop offset="1" stopColor="#7fa668" />
            </radialGradient>
            <radialGradient id="leafGradientAssigned" cx="35%" cy="30%" r="75%">
              <stop offset="0" stopColor="#ffe8ad" />
              <stop offset=".6" stopColor="#ffcc55" />
              <stop offset="1" stopColor="#f0a202" />
            </radialGradient>
            <filter id="woodGrain" x="0%" y="0%" width="100%" height="100%">
              <feTurbulence type="fractalNoise" baseFrequency="0.004 0.09" numOctaves="3" seed="11" result="grain" />
              <feColorMatrix in="grain" type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0.5 0.5 0.5 0 -0.35" result="grainAlpha" />
              <feComposite in="grainAlpha" in2="SourceAlpha" operator="in" />
            </filter>
          </defs>

          <g className="research-tree-art">
            <path className="research-trunk-shadow" d={geometry.trunkShapePath} />
            <path className="research-trunk" d={geometry.trunkShapePath} />
            <path className="research-trunk-grain" d={geometry.trunkShapePath} />
            {geometry.barkPaths.map((path, index) => <path className="research-bark-line" d={path} key={index} />)}
            <path className="research-trunk-light" d={geometry.trunkPath} pathLength={1} />
            {geometry.branches.map((branchGeometry) => (
              <ResearchBranch
                key={branchGeometry.branch.branch_id}
                geometry={branchGeometry}
                assignedBranch={assignedBranch}
                assignedProfiles={assignedKeys}
                selectedProfileKeys={selectedProfileKeys}
                selectedModelId={selectedDimension?.modelId ?? null}
                onOpenProfile={openProfile}
                onOpenDimension={openDimension}
              />
            ))}
            <g className="research-root" aria-hidden="true">
              <ellipse cx={geometry.root.x} cy={geometry.root.y} rx="63" ry="41" />
              <text x={geometry.root.x} y={geometry.root.y - 6} textAnchor="middle">RESPONDENT</text>
              <text x={geometry.root.x} y={geometry.root.y + 15} textAnchor="middle">ROOT</text>
            </g>
          </g>
        </svg>
      </div>

      <p className="research-tree-note">Select any leaf to read its canonical profile description. Exploring another leaf never changes this member’s assignment.</p>

      {treeContainer ? selectedLeaves.map((selection, index) => (
        <ClusterProfilePopover
          key={selection.profile.profile_key}
          profile={selection.profile}
          assigned={assignedKeys.has(selection.profile.profile_key)}
          anchor={selection.anchor}
          container={treeContainer}
          peerIndex={index}
          peerCount={selectedLeaves.length}
          onClose={() => closePopover(selection.profile.profile_key)}
        />
      )) : null}
      {selectedDimension && treeContainer ? (
        <ClusterDimensionPopover
          key={selectedDimension.modelId}
          modelId={selectedDimension.modelId}
          anchor={selectedDimension.anchor}
          container={treeContainer}
          onClose={closeDimensionPopover}
          onViewEvidence={() => openFormationEvidence(selectedDimension.modelId)}
        />
      ) : null}
      {formationEvidence ? (
        <ClusterFormationEvidenceModal
          modelKey={formationEvidence.modelId}
          onClose={closeFormationEvidence}
        />
      ) : null}
    </section>
  );
}
