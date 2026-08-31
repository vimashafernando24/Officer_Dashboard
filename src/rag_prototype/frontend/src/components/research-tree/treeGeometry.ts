import type { ResearchTreeBranch, ResearchTreeModel } from "../../types";

export interface Point { x: number; y: number }

export interface LeafGeometry {
  profile: ResearchTreeModel["profiles"][number];
  point: Point;
  rotation: number;
  stemPath: string;
}

export interface ModelGeometry {
  model: ResearchTreeModel;
  hub: Point;
  path: string;
  leaves: LeafGeometry[];
}

export interface BranchGeometry {
  branch: ResearchTreeBranch;
  hub: Point;
  path: string;
  treeWidth: number;
  labelSide: "left" | "right";
  models: ModelGeometry[];
}

export interface TreeGeometry {
  branches: BranchGeometry[];
  width: number;
  height: number;
  viewBox: string;
  root: Point;
  trunkPath: string;
  trunkShapePath: string;
  barkPaths: string[];
}

export const LEAF_WIDTH = 110;
export const LEAF_HEIGHT = 62;
export const LEAF_STEM_OVERLAP = 4;

const TREE_WIDTH = 1480;
const TREE_HEIGHT = 1080;
const ROOT: Point = { x: TREE_WIDTH / 2, y: 1000 };
const TRUNK_SPLIT: Point = { x: TREE_WIDTH / 2 - 14, y: 880 };
const LEAF_CENTER_GAP = 132;
const LEAF_RISE = 94;

// Vertical pitch between stacked models on the same branch. A leaf cluster reaches
// roughly LEAF_RISE + 50 above its model hub (rotation can swing a leaf's bounding
// box further than its flat half-height), and a model's own label sits roughly 60
// below its hub — so neighbouring hubs need at least ~215px apart or the leaves of
// the lower model overlap the label of the model above it. 225 keeps a safety margin.
const MODEL_PITCH = 225;

const BRANCH_LAYOUT: Record<string, { x: number; y: number; modelY: number[]; modelX: number[] }> = {
  D: { x: 315, y: 760, modelY: [190, 190 + MODEL_PITCH, 190 + MODEL_PITCH * 2], modelX: [-118, 92, -20] },
  E: { x: 650, y: 742, modelY: [300], modelX: [0] },
  F: { x: 950, y: 750, modelY: [340], modelX: [8] },
  G: { x: 1215, y: 766, modelY: [190, 190 + MODEL_PITCH], modelX: [-65, 60] },
};

const LEAF_ANGLES = [-26, 14, -10, 24, 7, -18, 28, -5, 19, -23, 11, -15, 30, -8, 21, -28, 4];
const LEAF_Y_VARIATION = [-7, 10, -15, 5, 13, -10, 8, -4, 15, -12, 4, -16, 9, -6, 12, -9, 2];
const LEAF_X_VARIATION = [-3, 4, -2, 3, 0, -4, 2, 5, -1, 3, -3, 1, 4, -2, 2, -4, 0];

function verticalCurve(from: Point, to: Point, bend = 0): string {
  const distance = Math.abs(from.y - to.y);
  return [
    `M ${from.x} ${from.y}`,
    `C ${from.x + bend} ${from.y - distance * 0.36},`,
    `${to.x - bend * 0.55} ${to.y + distance * 0.4},`,
    `${to.x} ${to.y}`,
  ].join(" ");
}

function majorBranchCurve(from: Point, to: Point, branchIndex: number): string {
  const horizontal = to.x - from.x;
  const irregularity = branchIndex % 2 === 0 ? -9 : 11;
  return [
    `M ${from.x} ${from.y}`,
    `C ${from.x + horizontal * 0.18 + irregularity} ${from.y - 42},`,
    `${to.x - horizontal * 0.24} ${to.y + 48 + irregularity * 0.3},`,
    `${to.x} ${to.y}`,
  ].join(" ");
}

/** Returns the rotated base/petiole point, slightly inside the leaf shape. */
export function getLeafAttachmentPoint(
  center: Point,
  width: number,
  rotation: number,
  overlap = LEAF_STEM_OVERLAP,
): Point {
  const radians = rotation * Math.PI / 180;
  const localX = -(width / 2) + overlap;
  return {
    x: center.x + localX * Math.cos(radians),
    y: center.y + localX * Math.sin(radians),
  };
}

function leafStemCurve(from: Point, attachment: Point, rotation: number, variant: number): string {
  const radians = rotation * Math.PI / 180;
  const cos = Math.cos(radians);
  const sin = Math.sin(radians);
  // Pull-back and perpendicular nudge defined in the leaf's own rotated frame (not world
  // space), so the stem always meets the leaf tangent to its actual orientation instead of
  // drifting off-angle once the leaf is rotated more than a few degrees.
  const localBackX = -27;
  const localPerpY = 4;
  const approach = {
    x: attachment.x + localBackX * cos - localPerpY * sin,
    y: attachment.y + localBackX * sin + localPerpY * cos,
  };
  const sway = ((variant % 5) - 2) * 5;
  return [
    `M ${from.x} ${from.y}`,
    `C ${from.x + sway} ${from.y - 38},`,
    `${approach.x} ${approach.y},`,
    `${attachment.x} ${attachment.y}`,
  ].join(" ");
}

function buildTrunkShapePath(root: Point, split: Point): string {
  return [
    `M ${root.x - 15} ${root.y}`,
    `C ${root.x - 17} ${root.y - 40}, ${split.x - 9} ${split.y + 44}, ${split.x - 7} ${split.y}`,
    `C ${split.x - 2} ${split.y - 5}, ${split.x + 3} ${split.y - 4}, ${split.x + 7} ${split.y}`,
    `C ${split.x + 12} ${split.y + 42}, ${root.x + 13} ${root.y - 42}, ${root.x + 15} ${root.y}`,
    "Z",
  ].join(" ");
}

export function buildTreeGeometry(tree: ResearchTreeBranch[]): TreeGeometry {
  let leafOrdinal = 0;
  const branches = tree.map((branch, branchIndex) => {
    const fallbackX = 250 + branchIndex * 310;
    const layout = BRANCH_LAYOUT[branch.branch_id] ?? {
      x: fallbackX,
      y: 754 + (branchIndex % 2) * 10,
      modelY: branch.models.map((_, index) => 190 + index * MODEL_PITCH),
      modelX: branch.models.map((_, index) => (index % 2 ? 18 : -18)),
    };
    const branchHub = { x: layout.x, y: layout.y };
    const models = branch.models.map((model, modelIndex) => {
      const modelHub = {
        x: layout.x + (layout.modelX[modelIndex] ?? 0),
        y: layout.modelY[modelIndex] ?? 270 + modelIndex * 145,
      };
      const firstLeafX = modelHub.x - ((model.profiles.length - 1) * LEAF_CENTER_GAP) / 2;
      const leaves = model.profiles.map((profile, profileIndex) => {
        const variant = leafOrdinal % LEAF_ANGLES.length;
        leafOrdinal += 1;
        const point = {
          x: firstLeafX + profileIndex * LEAF_CENTER_GAP + LEAF_X_VARIATION[variant],
          y: modelHub.y - LEAF_RISE + LEAF_Y_VARIATION[variant],
        };
        const rotation = LEAF_ANGLES[variant];
        const attachment = getLeafAttachmentPoint(point, LEAF_WIDTH, rotation);
        return {
          profile,
          point,
          rotation,
          stemPath: leafStemCurve(modelHub, attachment, rotation, variant),
        };
      });
      // Bend proportional to this model's own horizontal offset from the branch hub, so
      // sibling limbs sharing one hub point diverge immediately on leaving it instead of
      // running bundled together for most of their length and only splitting apart near
      // the top (which reads as one branch, not several, when models start close together).
      const horizontalOffset = modelHub.x - branchHub.x;
      const bend = horizontalOffset * 0.85;
      return {
        model,
        hub: modelHub,
        path: verticalCurve(branchHub, modelHub, bend),
        leaves,
      };
    });
    return {
      branch,
      hub: branchHub,
      treeWidth: TREE_WIDTH,
      labelSide: branchIndex < tree.length / 2 ? "left" as const : "right" as const,
      path: majorBranchCurve(TRUNK_SPLIT, branchHub, branchIndex),
      models,
    };
  });

  return {
    branches,
    width: TREE_WIDTH,
    height: TREE_HEIGHT,
    viewBox: `0 0 ${TREE_WIDTH} ${TREE_HEIGHT}`,
    root: ROOT,
    trunkPath: verticalCurve(ROOT, TRUNK_SPLIT, -5),
    trunkShapePath: buildTrunkShapePath(ROOT, TRUNK_SPLIT),
    barkPaths: [
      `M ${ROOT.x - 5} ${ROOT.y - 18} C ${ROOT.x - 7} ${ROOT.y - 54}, ${TRUNK_SPLIT.x - 2} ${TRUNK_SPLIT.y + 50}, ${TRUNK_SPLIT.x - 3} ${TRUNK_SPLIT.y + 18}`,
      `M ${ROOT.x + 7} ${ROOT.y - 28} C ${ROOT.x + 4} ${ROOT.y - 60}, ${TRUNK_SPLIT.x + 5} ${TRUNK_SPLIT.y + 44}, ${TRUNK_SPLIT.x + 3} ${TRUNK_SPLIT.y + 30}`,
      `M ${ROOT.x - 11} ${ROOT.y - 12} C ${ROOT.x - 13} ${ROOT.y - 46}, ${TRUNK_SPLIT.x - 6} ${TRUNK_SPLIT.y + 38}, ${TRUNK_SPLIT.x - 6} ${TRUNK_SPLIT.y + 8}`,
      `M ${ROOT.x + 1} ${ROOT.y - 34} C ${ROOT.x - 1} ${ROOT.y - 64}, ${TRUNK_SPLIT.x} ${TRUNK_SPLIT.y + 46}, ${TRUNK_SPLIT.x - 1} ${TRUNK_SPLIT.y + 22}`,
    ],
  };
}
