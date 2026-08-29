const DATA_URL = "data/branch_f_dashboard_data.json";
const COLORS = ["#075f4d", "#4f9a82", "#8bc4ad", "#d9ef91", "#d88b2c", "#356f82", "#8b6ca8", "#be7182", "#738c67", "#ba9b68"];

let dashboardData;
let activeProfile = "F-S1";

const el = (tag, className, text) => {
  const node = document.createElement(tag);
  if (className) node.className = className;
  if (text !== undefined) node.textContent = text;
  return node;
};

const fmt = value => Number(value).toLocaleString(undefined, { maximumFractionDigits: 1 });
const profileDatum = metric => metric.profiles[activeProfile];
const selectedProfile = () => dashboardData.profiles[activeProfile];

function renderTabs() {
  const tabs = document.querySelector("#profile-tabs");
  tabs.innerHTML = "";
  Object.values(dashboardData.profiles).forEach(profile => {
    const button = el("button", `profile-tab${profile.profile_id === activeProfile ? " active" : ""}`, profile.profile_id);
    button.type = "button";
    button.role = "tab";
    button.setAttribute("aria-selected", profile.profile_id === activeProfile);
    button.addEventListener("click", () => {
      activeProfile = profile.profile_id;
      render();
      document.querySelector("#profile-title").focus({ preventScroll: true });
    });
    tabs.append(button);
  });
  const p = selectedProfile();
  document.querySelector("#profile-selector-note").textContent = `${p.size} respondents · ${p.cohort_share}% of the frozen Branch F model cohort`;
}

function renderKpis() {
  const p = selectedProfile();
  const grid = document.querySelector("#kpi-grid");
  grid.innerHTML = "";
  const items = [
    ["Profile size", p.size, "Frozen respondents"],
    ["Model share", `${p.cohort_share}%`, `of n=${p.cohort_n}`],
    ["Uncertain assignment", `${p.ambiguous_percent}%`, `${p.ambiguous_n} of ${p.size}`],
  ];
  items.forEach(([label, value, note]) => {
    const card = el("div", "kpi");
    card.append(el("span", "", label), el("strong", "", value), el("small", "", note));
    grid.append(card);
  });
}

function stackedDistribution(data) {
  const wrap = el("div");
  const bar = el("div", "stacked-bar");
  const visible = data.categories.filter(item => item.count > 0);
  visible.forEach((item, index) => {
    const segment = el("div", "stack-segment");
    segment.style.width = `${item.percent}%`;
    segment.style.background = COLORS[index % COLORS.length];
    segment.title = `${item.category}: ${item.count}/${data.valid_n} (${item.percent}%)`;
    bar.append(segment);
  });
  const legend = el("div", "legend");
  visible.forEach((item, index) => {
    const row = el("div", "legend-row");
    const dot = el("span", "legend-dot");
    dot.style.background = COLORS[index % COLORS.length];
    row.append(dot, el("span", "legend-label", item.category), el("span", "legend-value", `${item.count} · ${item.percent}%`));
    legend.append(row);
  });
  wrap.append(bar, legend);
  return wrap;
}

function distributionTable(data) {
  const table = el("table", "stat-table");
  table.innerHTML = "<thead><tr><th>Response</th><th>n</th><th>% eligible</th></tr></thead>";
  const body = el("tbody");
  data.categories.filter(item => item.count > 0).forEach(item => {
    const row = el("tr");
    row.innerHTML = `<td></td><td>${item.count}</td><td>${item.percent}%</td>`;
    row.firstElementChild.textContent = item.category;
    body.append(row);
  });
  table.append(body);
  return table;
}

function cardShell(metric, validN, cautious = false) {
  const card = el("article", `metric-card${cautious ? " cautious" : ""}`);
  const head = el("div", "card-head");
  const left = el("div");
  const supporting = metric.display_priority.includes("cautious") || metric.display_priority.includes("secondary");
  left.append(el("span", `evidence-tag${supporting ? " supporting" : ""}`, supporting ? "Supporting / cautious" : metric.evidence_type));
  left.append(el("h3", "", metric.display_name));
  head.append(left, el("span", "denominator-badge", `valid n=${validN}`));
  card.append(head);
  return card;
}

function appendEvidence(card, metric) {
  if (metric.effect_size !== undefined) {
    const pValue = metric.adjusted_p_value < 0.001 ? "<0.001" : fmt(metric.adjusted_p_value);
    card.append(el("div", "evidence-stats", `Effect: ${metric.effect_size_name} = ${metric.effect_size} · BH-adjusted p ${pValue}`));
  }
  if (metric.caution) card.append(el("div", "caution-note", metric.caution));
  card.append(el("div", "source-line", `${metric.metric_id} · ${metric.source}`));
}

function renderDefinitions() {
  const grid = document.querySelector("#defining-grid");
  grid.innerHTML = "";
  dashboardData.defining_metrics.forEach(metric => {
    const data = profileDatum(metric);
    const card = cardShell(metric, data.valid_n);
    card.append(stackedDistribution(data));
    appendEvidence(card, metric);
    grid.append(card);
  });
}

function orderedCard(metric) {
  const data = profileDatum(metric);
  const card = cardShell(metric, data.valid_n, metric.display_priority.includes("cautious"));
  const stats = el("div", "ordered-summary");
  [["Median", data.median], ["Q1", data.q1], ["Q3", data.q3]].forEach(([label, value]) => {
    const box = el("div"); box.append(el("strong", "", fmt(value)), el("span", "", label)); stats.append(box);
  });
  card.append(stats);
  const map = dashboardData.value_label_maps[metric.variable] || [];
  const medianLabel = map.find(item => Number(item.value) === Number(data.median));
  if (medianLabel) card.append(el("p", "median-label", `Median category: ${medianLabel.label}`));
  appendEvidence(card, metric);
  return card;
}

function categoricalCard(metric) {
  const data = profileDatum(metric);
  const useTable = metric.sparse || metric.conditional;
  const card = cardShell(metric, data.valid_n, metric.display_priority.includes("cautious") || useTable);
  card.append(useTable ? distributionTable(data) : stackedDistribution(data));
  if (metric.conditional) {
    card.append(el("div", "caution-note", `Conditional gateway: ${metric.gateway}. ${data.missing_or_not_applicable_n} profile members are structurally not applicable.`));
  }
  if (metric.sparse) {
    const sparsePct = metric.sparse_expected_share !== null ? ` (${fmt(metric.sparse_expected_share * 100)}% of expected cells below 5)` : "";
    card.append(el("div", "caution-note", `Sparse-cell warning${sparsePct}. Rare categories are not interpreted individually.`));
  }
  appendEvidence(card, metric);
  return card;
}

function renderProfiling() {
  const grid = document.querySelector("#profiling-grid");
  grid.innerHTML = "";
  dashboardData.profiling_metrics.forEach(metric => grid.append(metric.variable_type === "categorical" ? categoricalCard(metric) : orderedCard(metric)));
}

function renderDirect() {
  const grid = document.querySelector("#direct-grid");
  grid.innerHTML = "";
  dashboardData.direct_metrics.forEach(metric => {
    const data = profileDatum(metric);
    const card = cardShell(metric, data.valid_n);
    card.append(stackedDistribution(data));
    appendEvidence(card, metric);
    grid.append(card);
  });
}

function renderSupply() {
  const supply = dashboardData.catalogue_supply;
  document.querySelector("#supply-total").textContent = `${supply.total_courses} courses`;
  document.querySelector("#supply-source").textContent = `${supply.metric_id} · ${supply.source}`;
  const chart = document.querySelector("#supply-chart");
  chart.innerHTML = "";
  const max = Math.max(...supply.areas.map(item => item.course_count));
  supply.areas.forEach(item => {
    const row = el("div", "supply-row");
    const track = el("div", "supply-track");
    const fill = el("div", "supply-fill");
    fill.style.width = `${100 * item.course_count / max}%`;
    track.append(fill);
    row.append(el("span", "", item.area), track, el("span", "supply-count", item.course_count));
    chart.append(row);
  });
}

function renderCautions() {
  const p = selectedProfile();
  const workType = dashboardData.profiling_metrics.find(metric => metric.variable === "work_while_study_type");
  const supportingNames = dashboardData.profiling_metrics
    .filter(metric => metric.display_priority.includes("cautious") && !metric.conditional)
    .map(metric => metric.display_name.toLowerCase());
  const items = [
    ["Group evidence", dashboardData.governance.group_warning],
    ["Denominators", "Every chart shows its valid or eligible n. Structural not-applicable responses are never treated as ‘No’."],
    ["Sparse and conditional evidence", `Primary income source has sparse cells. Work-while-study type applies only to ${workType.profiles["F-S1"].valid_n} F-S1 and ${workType.profiles["F-S2"].valid_n} F-S2 respondents and is an association, not a causal pathway.`],
    ["Supporting findings", `${supportingNames.join(", ")} did not remain below BH-adjusted 0.05. They are context charts, not headline KPIs.`],
    ["Assignment uncertainty", `${p.ambiguous_n}/${p.size} (${p.ambiguous_percent}%) selected-profile assignments were flagged uncertain. Frozen assignments remain unchanged.`],
    ["No course recommendation", dashboardData.governance.supply_warning],
  ];
  const grid = document.querySelector("#caution-grid");
  grid.innerHTML = "";
  items.forEach(([title, copy]) => { const card = el("article", "caution-card"); card.append(el("strong", "", title), el("p", "", copy)); grid.append(card); });
}

function render() {
  renderTabs();
  const p = selectedProfile();
  const title = document.querySelector("#profile-title");
  title.textContent = p.label;
  title.tabIndex = -1;
  document.querySelector("#profile-dimension").textContent = `${p.profile_id} · ${p.dimension}`;
  document.querySelector("#group-warning").textContent = dashboardData.governance.group_warning;
  document.querySelector("#supply-warning").textContent = dashboardData.governance.supply_warning;
  renderKpis(); renderDefinitions(); renderProfiling(); renderDirect(); renderSupply(); renderCautions();
  document.querySelector("#validation-summary").textContent = `${dashboardData.validation.checks.length} checks passed against frozen assignments, cleaned survey data, profiling outputs, and the 87-course V2 catalogue.`;
}

fetch(DATA_URL)
  .then(response => { if (!response.ok) throw new Error(`Data request failed: ${response.status}`); return response.json(); })
  .then(data => {
    dashboardData = data;
    if (!data.validation?.passed) throw new Error("Dashboard payload did not pass source validation.");
    render();
  })
  .catch(error => {
    document.querySelector("main").innerHTML = `<div class="error"><strong>Dashboard could not load.</strong><p>${error.message}</p><p>Run <code>python3 officer_dashboard/build_branch_f_data.py</code>, then serve the project over HTTP.</p></div>`;
  });
