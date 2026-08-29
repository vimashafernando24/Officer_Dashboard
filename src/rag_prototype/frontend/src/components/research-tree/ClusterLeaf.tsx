import type { ClusterCatalogueEntry } from "../../types";
import { LEAF_HEIGHT, LEAF_WIDTH, type LeafGeometry } from "./treeGeometry";

interface Props {
  geometry: LeafGeometry;
  assigned: boolean;
  selected: boolean;
  onOpen: (profile: ClusterCatalogueEntry, anchor: SVGGElement) => void;
}

function shortCode(code: string) {
  return code.replace(/^Cluster\s+/i, "");
}

export function ClusterLeaf({ geometry, assigned, selected, onOpen }: Props) {
  const { profile, point, rotation } = geometry;
  const activate = (anchor: SVGGElement) => onOpen(profile, anchor);
  return (
    <g transform={`translate(${point.x} ${point.y})`}>
      <g
        className={`research-leaf${assigned ? " is-assigned" : ""}${selected ? " is-selected" : ""}`}
        role="button"
        tabIndex={0}
        aria-pressed={selected}
        aria-haspopup="dialog"
        aria-expanded={selected}
        aria-label={`${profile.cluster_code}: ${profile.cluster_name}${assigned ? ", your assigned profile" : ""}`}
        onClick={(event) => activate(event.currentTarget)}
        onKeyDown={(event) => {
          if (event.key === "Enter" || event.key === " ") {
            event.preventDefault();
            activate(event.currentTarget);
          }
        }}
      >
        <ellipse className="research-leaf-hit" rx={LEAF_WIDTH / 2 + 8} ry={LEAF_HEIGHT / 2 + 4} />
        <g className="research-leaf-illustration" transform={`rotate(${rotation})`}>
          <path className="research-leaf-shadow" d="M -53 3 C -37 -25 31 -27 57 1 C 39 30 -29 33 -53 3 Z" />
          <path className="research-leaf-shape" d="M -55 0 C -40 -32 33 -35 57 -3 C 40 30 -31 34 -55 0 Z" />
          <path className="research-leaf-vein research-leaf-vein-main" d="M -44 0 C -14 -2 20 -2 44 -3" />
          <path className="research-leaf-vein" d="M -20 -1 C -14 -10 -4 -14 6 -16" />
          <path className="research-leaf-vein" d="M 4 -2 C 10 -10 20 -13 30 -14" />
          <path className="research-leaf-vein" d="M -20 1 C -14 9 -4 13 6 15" />
          <path className="research-leaf-vein" d="M 4 2 C 10 9 20 12 30 13" />
        </g>
        <text className="research-leaf-code" textAnchor="middle" dominantBaseline="central">
          {shortCode(profile.cluster_code)}
        </text>
      </g>
    </g>
  );
}
