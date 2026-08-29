import "./Card.css";

export function Card({
  children,
  variant,
  className,
}: {
  children: React.ReactNode;
  variant?: "about" | "discuss";
  className?: string;
}) {
  const cls = ["ui-card", variant ? `ui-card-${variant}` : "", className ?? ""].filter(Boolean).join(" ");
  return <div className={cls}>{children}</div>;
}

export function StepTitle({ children, style }: { children: React.ReactNode; style?: React.CSSProperties }) {
  return (
    <div className="ui-step-title" style={style}>
      {children}
    </div>
  );
}

export function StepHint({ children }: { children: React.ReactNode }) {
  return <div className="ui-step-hint">{children}</div>;
}
