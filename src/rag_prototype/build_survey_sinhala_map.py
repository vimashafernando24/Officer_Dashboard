"""
Build the officer dashboard's Sinhala survey map from the original NYSC survey.

The survey app keeps English questions in src/data/questions.js and the Sinhala
version in src/translations/si.js, keyed by the same question id with options
in the same order. This script pairs them so the dashboard shows the exact
Sinhala wording respondents saw instead of separately written translations.

Shortened analysis labels (the D_motivation canonical labels) are mapped to the
survey option with the same answer code; labels that differ from a survey
option only by letter case are mapped to that option.

Run:
    python3 build_survey_sinhala_map.py [path/to/survey/repo]

Default survey repo: ~/Desktop/RP/fullProject/SurveyFolder2
Output: frontend/src/data/surveySinhalaMap.json
"""
from __future__ import annotations

import json
import subprocess
import sys
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUTPUT = HERE / "frontend/src/data/surveySinhalaMap.json"
DASHBOARD_DATA = HERE / "frontend/src/data"
DEFAULT_SURVEY = Path.home() / "Desktop/RP/fullProject/SurveyFolder2"

sys.path.insert(0, str(HERE))
from new_respondent_cluster_assignment import _D_MOTIVATION_CANONICAL  # noqa: E402

DUMP_JS = """
import { Q } from './src/data/questions.js';
import { si } from './src/translations/si.js';
const out = Q.filter(q => q.var).map(q => ({
  id: q.id, variable: q.var, text: q.text,
  opts: Array.isArray(q.opts) ? q.opts.map(o => ({ v: String(o.v), l: o.l })) : [],
  si_text: si.questions[q.id]?.text ?? null,
  si_opts: (si.questions[q.id]?.opts ?? []).map(o => o.l),
}));
process.stdout.write(JSON.stringify(out));
"""


def dump_survey(survey: Path) -> list[dict]:
    result = subprocess.run(
        ["node", "--input-type=module", "-e", DUMP_JS],
        cwd=survey, capture_output=True, text=True, check=True,
    )
    return json.loads(result.stdout)


def survey_commit(survey: Path) -> str | None:
    try:
        return subprocess.run(
            ["git", "rev-parse", "--short", "HEAD"], cwd=survey,
            capture_output=True, text=True, check=True,
        ).stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def dashboard_answer_labels() -> set[str]:
    labels: set[str] = set()

    def walk(node):
        if isinstance(node, dict):
            for key, value in node.items():
                if key in ("answer", "answer_categories"):
                    values = value if isinstance(value, list) else [value]
                    labels.update(v for v in values if isinstance(v, str) and v)
                walk(value)
        elif isinstance(node, list):
            for value in node:
                walk(value)

    for path in DASHBOARD_DATA.glob("*.json"):
        if path.name != OUTPUT.name:
            walk(json.loads(path.read_text(encoding="utf-8")))
    return labels


def build(survey: Path) -> dict:
    questions = dump_survey(survey)
    problems: list[str] = []

    questions_by_id: dict[str, dict] = {}
    by_variable: dict[str, set[str]] = defaultdict(set)
    options_by_variable: dict[str, dict[str, dict[str, str]]] = defaultdict(dict)
    candidates: dict[str, Counter] = defaultdict(Counter)
    answers_by_question_id: dict[str, dict[str, str]] = defaultdict(dict)
    answers_by_variable: dict[str, dict[str, str]] = defaultdict(dict)
    variable_answer_clash: set[str] = set()

    for q in questions:
        if not q["si_text"]:
            problems.append(f"{q['id']}: no Sinhala question text")
            continue
        questions_by_id[q["id"]] = {"variable": q["variable"], "en": q["text"], "si": q["si_text"]}
        by_variable[q["variable"]].add(q["si_text"])
        if len(q["opts"]) != len(q["si_opts"]):
            problems.append(f"{q['id']}: {len(q['opts'])} English vs {len(q['si_opts'])} Sinhala options")
            continue
        for opt, si_label in zip(q["opts"], q["si_opts"]):
            candidates[opt["l"]][si_label] += 1
            options_by_variable[q["variable"]][opt["v"]] = {"en": opt["l"], "si": si_label}
            answers_by_question_id[q["id"]][opt["l"]] = si_label
            previous = answers_by_variable[q["variable"]].setdefault(opt["l"], si_label)
            if previous != si_label:
                variable_answer_clash.add(q["variable"])

    answers: dict[str, str] = {}
    conflicts: dict[str, list[str]] = {}
    for english, counts in sorted(candidates.items()):
        answers[english] = counts.most_common(1)[0][0]
        if len(counts) > 1:
            conflicts[english] = [label for label, _ in counts.most_common()]

    # Questions asked in several branches share one variable name; the
    # dashboard looks them up by variable, so keep it only when unambiguous.
    questions_by_variable = {var: next(iter(texts)) for var, texts in sorted(by_variable.items()) if len(texts) == 1}
    ambiguous_variables = sorted(var for var, texts in by_variable.items() if len(texts) > 1)

    aliases: dict[str, str] = {}
    for var, levels in _D_MOTIVATION_CANONICAL.items():
        for code, label in levels.items():
            option = options_by_variable.get(var, {}).get(str(code))
            if option:
                aliases[label] = option["si"]
                answers_by_variable[var][label] = option["si"]
                for qid, meta in questions_by_id.items():
                    if meta["variable"] == var:
                        answers_by_question_id[qid][label] = option["si"]
            else:
                problems.append(f"{var} code {code}: no survey option for canonical label")

    lower_index = {english.casefold(): si for english, si in answers.items()}
    unmatched = []
    for label in sorted(dashboard_answer_labels()):
        if label in answers or label in aliases:
            continue
        if label.casefold() in lower_index:
            aliases[label] = lower_index[label.casefold()]
        else:
            unmatched.append(label)

    return {
        "description": (
            "Generated by src/rag_prototype/build_survey_sinhala_map.py from the original NYSC survey "
            "(questions.js + translations/si.js); do not edit by hand."
        ),
        "source": {"survey_repo": survey.name, "commit": survey_commit(survey)},
        "questions_by_id": questions_by_id,
        "questions_by_variable": questions_by_variable,
        "answers": {**answers, **aliases},
        "answers_by_question_id": dict(sorted(answers_by_question_id.items())),
        "answers_by_variable": {
            var: labels for var, labels in sorted(answers_by_variable.items()) if var not in variable_answer_clash
        },
        "report": {
            "answer_aliases": sorted(aliases),
            "answer_conflicts": conflicts,
            "ambiguous_variables": ambiguous_variables,
            "variables_with_clashing_answers": sorted(variable_answer_clash),
            "dashboard_answers_without_survey_sinhala": unmatched,
            "problems": problems,
        },
    }


def main() -> int:
    survey = Path(sys.argv[1]).expanduser() if len(sys.argv) > 1 else DEFAULT_SURVEY
    data = build(survey)
    OUTPUT.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    report = data["report"]
    print(f"Wrote {OUTPUT.relative_to(HERE)}")
    print(f"  questions: {len(data['questions_by_id'])}, answers: {len(data['answers'])}, "
          f"aliases: {len(report['answer_aliases'])}")
    for key in ("answer_conflicts", "ambiguous_variables", "variables_with_clashing_answers", "dashboard_answers_without_survey_sinhala", "problems"):
        print(f"  {key}: {len(report[key])}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
