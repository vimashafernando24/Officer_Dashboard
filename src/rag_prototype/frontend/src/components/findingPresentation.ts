import type { Finding } from "../types";

const FEATURE_NAMES: Record<string, string> = {
  employment_network_quality: "Useful Employment Contacts",
  ideal_sector: "Preferred Employment Sector",
  study_field_preference: "Preferred Field of Study",
  institution_type: "Type of Education Institution",
  job_search_method_d: "How Members Searched for Work",
  already_job_searching: "Whether Members Were Job Searching",
  primary_income_source: "Main Source of Income",
  edu_funding_source: "How Education Was Funded",
  household_income: "Household Income Level",
  job_acceptance_conditions: "Conditions for Accepting a Job",
  network_helpfulness: "Helpfulness of Job-Search Contacts",
  search_method_primary: "How Members Searched for Work",
  social_support_job_search: "Support During Job Search",
  monthly_income_band: "Monthly Income",
  hopes_to_change_job: "Plans to Change Jobs",
  job_satisfaction: "Job Satisfaction",
  labour_market_connection: "Connection to Work Opportunities",
  employment_self_efficacy: "Confidence Finding Work or Training",
  most_important_life_goal: "Most Important Life Goal",
  support_for_engagement: "Expected Support for Work or Study",
  future_orientation_g: "Future Plans and Outlook",
};

export function findingFeatureName(finding: Finding) {
  const configured = FEATURE_NAMES[finding.variable];
  if (configured) return configured;

  const source = finding.distribution?.label ?? finding.variable;
  return source
    .replace(/[_/-]+/g, " ")
    .trim()
    .split(/\s+/)
    .filter(Boolean)
    .map((word) => word.charAt(0).toUpperCase() + word.slice(1))
    .join(" ");
}

export function meaningfulFindingText(finding: Finding) {
  const categorical = finding.finding.match(
    /[‘"](.+?)[’"].*?\(\d+\/\d+,\s*([\d.]+)% vs ([\d.]+)%/,
  );
  if (categorical) {
    const [, highlightedAnswer, profilePercentText, comparisonPercentText] = categorical;
    const profilePercent = Number(profilePercentText);
    const distribution = finding.distribution?.distribution ?? [];
    const highest = distribution.length
      ? Math.max(...distribution.map((item) => item.percent))
      : null;
    const leaders =
      highest === null
        ? []
        : distribution.filter((item) => Math.abs(item.percent - highest) < 0.05);

    if (highest !== null && Math.abs(profilePercent - highest) < 0.05 && leaders.length > 1) {
      const names = leaders.map((item) => item.value);
      const joined =
        names.length === 2
          ? `${names[0]} and ${names[1]}`
          : `${names.slice(0, -1).join(", ")}, and ${names.at(-1)}`;
      return `${joined} were joint-highest responses in this historical profile at ${highest.toFixed(
        1,
      )}% each. The retained comparison found “${highlightedAnswer}” at ${profilePercentText}% here versus ${comparisonPercentText}% across the other profiles.`;
    }

    if (highest !== null && Math.abs(profilePercent - highest) >= 0.05 && leaders.length) {
      const leaderNames = leaders.map((item) => item.value).join(" and ");
      return `${leaderNames} ${leaders.length === 1 ? "was" : "were"} the most common ${
        leaders.length === 1 ? "response" : "responses"
      } in this historical profile at ${highest.toFixed(
        1,
      )}%. The retained comparison highlights “${highlightedAnswer}”: ${profilePercentText}% here versus ${comparisonPercentText}% across the other profiles.`;
    }

    if (highest !== null && Math.abs(profilePercent - highest) < 0.05) {
      return `“${highlightedAnswer}” was the most common response in this historical profile at ${profilePercentText}%, compared with ${comparisonPercentText}% across the other profiles.`;
    }

    return `${profilePercentText}% of historical members in this profile answered “${highlightedAnswer}”, compared with ${comparisonPercentText}% across the other profiles.`;
  }

  const ordered = finding.finding.match(
    /had (higher|lower) median (.+?) \(([\d.]+) vs ([\d.]+)\)/i,
  );
  if (ordered) {
    return `Historical members in this profile generally gave ${ordered[1]} responses for ${ordered[2]} than members in the other profiles.`;
  }

  return finding.finding.replace(/\s*\[[^\]]+\]\s*$/, "");
}
