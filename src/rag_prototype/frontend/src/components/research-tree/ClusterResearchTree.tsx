import { useCallback, useMemo, useState } from "react";
import type { AssignedProfile, ClusterCatalogueEntry, ResearchTreeBranch } from "../../types";
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

export function ClusterResearchTree({ assignedBranch, assignedProfiles, tree }: Props) {
  const [treeContainer, setTreeContainer] = useState<HTMLDivElement | null>(null);
  const [selectedLeaf, setSelectedLeaf] = useState<LeafSelection | null>(null);
  const assignedKeys = useMemo(
    () => new Set(assignedProfiles.map((profile) => profile.profile_key)),
    [assignedProfiles],
  );
  const geometry = useMemo(() => buildTreeGeometry(tree), [tree]);
  const closePopover = useCallback(() => setSelectedLeaf(null), []);
  const openProfile = useCallback((profile: ClusterCatalogueEntry, anchor: SVGGElement) => {
    setSelectedLeaf((current) => current?.profile.profile_key === profile.profile_key
      ? null
      : { profile, anchor });
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
          </defs>

          <g className="research-tree-art">
            <path className="research-trunk-shadow" d={geometry.trunkShapePath} />
            <path className="research-trunk" d={geometry.trunkShapePath} />
            {geometry.barkPaths.map((path, index) => <path className="research-bark-line" d={path} key={index} />)}
            <path className="research-trunk-light" d={geometry.trunkPath} pathLength={1} />
            {geometry.branches.map((branchGeometry) => (
              <ResearchBranch
                key={branchGeometry.branch.branch_id}
                geometry={branchGeometry}
                assignedBranch={assignedBranch}
                assignedProfiles={assignedKeys}
                selectedProfileKey={selectedLeaf?.profile.profile_key ?? null}
                onOpenProfile={openProfile}
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

      {selectedLeaf && treeContainer ? (
        <ClusterProfilePopover
          key={selectedLeaf.profile.profile_key}
          profile={selectedLeaf.profile}
          assigned={assignedKeys.has(selectedLeaf.profile.profile_key)}
          anchor={selectedLeaf.anchor}
          container={treeContainer}
          onClose={closePopover}
        />
      ) : null}
    </section>
  );
}
