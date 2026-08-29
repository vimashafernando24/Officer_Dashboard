import "./Badge.css";

type BadgeKind =
  | "direct"
  | "adjacent"
  | "strength"
  | "strength-strong"
  | "strength-moderate"
  | "context"
  | "status-available"
  | "status-nodef"
  | "status-offline"
  | "safe"
  | "review";

export function Badge({ kind, children }: { kind: BadgeKind; children: React.ReactNode }) {
  return <span className={`badge badge-${kind}`}>{children}</span>;
}
