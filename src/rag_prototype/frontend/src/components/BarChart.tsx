import "./BarChart.css";
import type { DistributionEntry } from "../types";

export function BarChart({ dist }: { dist: DistributionEntry | null }) {
  if (!dist) {
    return <div className="chart-ordered">No source distribution found for this variable.</div>;
  }
  if (dist.parse_failed || dist.raw_distribution) {
    return <div className="chart-ordered">{dist.raw ?? dist.raw_distribution ?? "Distribution not available."}</div>;
  }
  const suppliedItems = dist.distribution ?? [];
  if (!suppliedItems.length && dist.type === "ordered") {
    return (
      <div className="chart-ordered">
        median {dist.median} &middot; IQR {dist.iqr_low}&ndash;{dist.iqr_high}{" "}
        <span style={{ color: "var(--ink-faint)" }}>(n={dist.eligible_n})</span>
      </div>
    );
  }
  const items = dist.type === "ordered"
    ? [...suppliedItems]
    : [...suppliedItems].sort((a, b) => b.percent - a.percent);
  const highestPercent = items.length ? Math.max(...items.map((item) => item.percent)) : 0;
  const highestCount = items.filter((item) => Math.abs(item.percent - highestPercent) < 0.05).length;
  return (
    <div className="chart-full">
      {highestCount > 1 ? (
        <div className="chart-tie-note">Joint highest responses &middot; {highestPercent.toFixed(1)}% each</div>
      ) : null}
      {items.map((it) => (
        <div
          className={`chart-bar-full${Math.abs(it.percent - highestPercent) < 0.05 ? " hl" : ""}`}
          key={it.value}
        >
          <div className="cbf-row">
            <span className="cbf-label">{it.value}</span>
            <span className="cbf-stats mono">{it.percent.toFixed(1)}%</span>
          </div>
          <div className="cbf-track">
            <div className="cbf-fill" style={{ width: `${it.percent}%` }} />
          </div>
        </div>
      ))}
      {dist.eligible_n ? (
        <div className="chart-n">based on {dist.eligible_n} respondents in this profile</div>
      ) : null}
    </div>
  );
}
