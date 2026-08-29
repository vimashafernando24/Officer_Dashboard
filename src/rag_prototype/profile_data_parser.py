"""
Structured parser for the frozen profile knowledge documents
(outputs/rag_profile_knowledge/documents/*.txt). Built because the new-person
profile explorer needs to display the contents of those documents. It can
parse every DIRECT_GROUP_DISTRIBUTIONS variable for the read-only explorer,
but those distributions are explicitly NOT an officer-briefing evidence
source. Briefing eligibility is governed separately by
retained_cluster_evidence_registry.py.

Read-only: does not modify any profile document. Parsing failures degrade to
raw text, never silently drop a section.
"""
import re


SECTION_RE = re.compile(r"^\d+\. ([A-Z_]+)$")
DIST_ENTRY_RE = re.compile(
    r"^\* (.+?) \[(\w+)\] — type: (\w+), theme: (\w+), cohort coverage: ([\d.]+)% "
    r"(\[SCREENED FINDING\]|\[tested, not highlighted\])(.*)$"
)
CATEGORICAL_LINE_RE = re.compile(
    r"observed distribution \(eligible n=(\d+)\): (.+)$"
)
CATEGORICAL_ITEM_RE = re.compile(r"([^:;]+): (\d+) \(([\d.]+)%\)")
ORDERED_LINE_RE = re.compile(
    r"observed distribution \(eligible n=(\d+)\): median=([\d.]+), IQR=([\d.]+)–([\d.]+)"
)
STAT_DETAIL_RE = re.compile(
    r"^\s*- (.+?) \((\w+)\): coverage ([\d.]+)% of the model cohort; "
    r"effect size (.+?) = ([\d.]+); raw p = ([\deE.\-]+); "
    r"BH-adjusted p = ([\deE.\-]+) \((.+?)\); programme relevance rated '(\w+)'\.(.*)$"
)


def _split_sections(text: str) -> dict:
    lines = text.splitlines()
    markers = []
    for i, ln in enumerate(lines):
        m = SECTION_RE.match(ln.strip())
        if m:
            markers.append((i, m.group(1)))
    sections = {}
    for idx, (start, name) in enumerate(markers):
        end = markers[idx + 1][0] if idx + 1 < len(markers) else len(lines)
        # skip the divider line immediately after the header
        body_start = start + 1
        while body_start < end and set(lines[body_start].strip()) <= {"-"}:
            body_start += 1
        sections[name] = "\n".join(lines[body_start:end]).strip()
    header_end = markers[0][0] if markers else len(lines)
    sections["_HEADER"] = "\n".join(lines[:header_end]).strip()
    return sections


def _parse_header_fields(header_text: str) -> dict:
    fields = {}
    for key in ["profile_key", "branch", "retained_model_id", "retained_dimension",
                "profile_id", "profile_label", "profile_size_n"]:
        m = re.search(rf"^{key}: (.+)$", header_text, re.MULTILINE)
        if m:
            fields[key] = m.group(1).strip()
    return fields


def _parse_distributions(section3_text: str) -> list:
    entries = []
    blocks = re.split(r"\n\n+", section3_text)
    for block in blocks:
        block = block.strip()
        if not block.startswith("*"):
            continue
        lines = block.splitlines()
        m = DIST_ENTRY_RE.match(lines[0].strip())
        if not m:
            entries.append({"raw": block, "parse_failed": True})
            continue
        label, var_code, vtype, theme, coverage, screened, notes = m.groups()
        entry = {
            "label": label.strip(),
            "variable": var_code,
            "type": vtype,
            "theme": theme,
            "coverage_pct": float(coverage),
            "screened": screened == "[SCREENED FINDING]",
            "notes": notes.strip(" ()"),
        }
        rest = "\n".join(lines[1:])
        if vtype == "ordered":
            om = ORDERED_LINE_RE.search(rest)
            if om:
                n, median, iqr_lo, iqr_hi = om.groups()
                entry["eligible_n"] = int(n)
                entry["median"] = float(median)
                entry["iqr_low"] = float(iqr_lo)
                entry["iqr_high"] = float(iqr_hi)
            else:
                entry["raw_distribution"] = rest.strip()
        else:
            cm = CATEGORICAL_LINE_RE.search(rest)
            if cm:
                n, items_text = cm.groups()
                entry["eligible_n"] = int(n)
                items = []
                for im in CATEGORICAL_ITEM_RE.finditer(items_text):
                    items.append({
                        "value": im.group(1).strip(),
                        "count": int(im.group(2)),
                        "percent": float(im.group(3)),
                    })
                entry["distribution"] = items
            else:
                entry["raw_distribution"] = rest.strip()
        entries.append(entry)
    return entries


def _parse_findings(section2_text: str) -> dict:
    fdr_note = None
    fdr_m = re.search(r"^FDR-correction context.*$", section2_text, re.MULTILINE)
    if fdr_m:
        fdr_note = fdr_m.group(0)

    categories = []
    for cat_block in re.finditer(r"\[(.+?)\]\n((?:  - .+\n?)*)", section2_text):
        name = cat_block.group(1)
        if name.startswith("Strongest") or name in (
            "Barriers, support and financial context", "Aspirations and preferences",
            "Education, training and employment characteristics", "Programme-relevant evidence",
        ) or True:  # accept any bracketed category heading found in section 2
            bullets = [ln.strip().lstrip("- ").strip() for ln in cat_block.group(2).splitlines() if ln.strip()]
            if bullets:
                categories.append({"category": name, "findings": bullets})

    stat_details = []
    for ln in section2_text.splitlines():
        sm = STAT_DETAIL_RE.match(ln)
        if sm:
            label, var, coverage, effect_name, effect_val, raw_p, bh_p, sig_note, relevance, _ = sm.groups()
            stat_details.append({
                "label": label.strip(), "variable": var, "coverage_pct": float(coverage),
                "effect_size_name": effect_name.strip(), "effect_size": float(effect_val),
                "raw_p": raw_p, "bh_adjusted_p": bh_p, "significant_note": sig_note,
                "programme_relevance": relevance,
            })

    return {"fdr_note": fdr_note, "categories": categories, "statistical_detail": stat_details}


def select_validated_evidence(parsed: dict) -> list:
    """Compatibility wrapper for the governed retained-evidence registry.

    Earlier code inferred eligibility from every statistical-detail row that
    happened to have a high/medium relevance label.  That admitted findings
    which were explored or reported but were not explicitly retained in the
    final analysis.  Eligibility is now an exact allowlist decision in
    retained_cluster_evidence_registry; this parser no longer makes it.
    """
    from retained_cluster_evidence_registry import select_retained_evidence
    return select_retained_evidence(parsed)


def parse_profile_document(text: str) -> dict:
    sections = _split_sections(text)
    header_fields = _parse_header_fields(sections.get("_HEADER", ""))
    result = {
        "header": header_fields,
        "profile_definition_text": sections.get("PROFILE_DEFINITION", ""),
        "supported_findings": _parse_findings(sections.get("SUPPORTED_PROFILE_FINDINGS", "")),
        "distributions": _parse_distributions(sections.get("DIRECT_GROUP_DISTRIBUTIONS", "")),
        "cautions_text": sections.get("CAUTIONS", ""),
        "prohibited_inferences_text": sections.get("PROHIBITED_INFERENCES", ""),
    }
    return result
