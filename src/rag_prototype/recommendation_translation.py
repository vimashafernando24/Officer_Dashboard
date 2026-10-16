"""
On-demand Sinhala translation of already-validated programme recommendation text.

This module is deliberately separate from the recommendation pipeline. It never
generates, ranks, filters or replaces programmes: it receives the officer-visible
English explanation text of a result the pipeline has ALREADY produced and
validated, translates it with one structured OpenAI call, checks that the
translation preserves structure, numbers and protected names, and returns it.

Security / cost properties:
  - strict input schema (unknown fields rejected, length and count limits);
  - fixed server-side model, prompt, timeout and output-token limit;
  - exactly one provider request per call (SDK retries are disabled in
    openai_client.get_client and no repair call is made here);
  - recommendation text and respondent details are never logged.
"""
from __future__ import annotations

import logging
import os
import re
import time
from typing import List, Optional

from pydantic import BaseModel, ConfigDict

from env_config import _load_dotenv_once
from openai_client import _failure_result, get_client

LOGGER = logging.getLogger(__name__)

# Translation-only model selection. Independent of the recommendation model
# (env_config.get_production_model(), which stays gpt-5-mini). The optional
# OPENAI_TRANSLATION_MODEL setting is server-side only and must name one of
# these approved models; anything else falls back to the default. Each entry
# fixes the reasoning effort, so no temperature is ever sent to these models.
DEFAULT_TRANSLATION_MODEL = "gpt-6.1-sol"
TRANSLATION_MODELS = {
    "gpt-6.1-sol": {"reasoning_effort": "low"},
    "gpt-6-astra": {"reasoning_effort": "low"},
    "gpt-6-luna": {"reasoning_effort": "low"},
    "gpt-5.4": {"reasoning_effort": "low"},
    "gpt-5.4-mini": {"reasoning_effort": "low"},
    "gpt-5-mini": {"reasoning_effort": "low"},
}


def get_translation_model() -> str:
    _load_dotenv_once()
    configured = os.environ.get("OPENAI_TRANSLATION_MODEL", "").strip()
    if not configured:
        return DEFAULT_TRANSLATION_MODEL
    if configured not in TRANSLATION_MODELS:
        LOGGER.warning("OPENAI_TRANSLATION_MODEL is not an approved translation model; using the default.")
        return DEFAULT_TRANSLATION_MODEL
    return configured


# A full nine-programme Sinhala translation is a long generation (Sinhala is
# token-heavy); 60 s proved too short for gpt-6.1-sol in local testing.
TRANSLATION_TIMEOUT_SECONDS = 150.0
TRANSLATION_MAX_OUTPUT_TOKENS = 16000

MAX_REQUEST_BYTES = 64 * 1024
MAX_PROGRAMMES = 9
MAX_QUESTIONS_PER_PROGRAMME = 5
MAX_COURSE_NAME_CHARS = 200
MAX_TEXT_CHARS = 2000
MAX_QUESTION_CHARS = 600
MAX_TOTAL_CHARS = 24000

_PROGRAMME_FIELDS = {"course_name", "why_it_may_suit_this_user", "cluster_finding_summary", "questions_to_discuss"}
_REQUEST_FIELDS = {"programmes", "no_recommendation_reason"}

_SINHALA = re.compile(r"[඀-෿]")
# A number token: an integer written with or without thousands separators,
# an optional decimal part, and an optional percent sign that may be
# separated by up to two spaces ("41.2%" and "41.2 %" are the same token).
_NUMBER = re.compile(
    r"(?<![\d.])(\d{1,3}(?:,\d{3})+(?!\d)|\d+)(?:\.(\d+))?(?:[ \u00a0\u202f]{0,2}(%))?"
)
_PLACEHOLDER = re.compile(r"\[\[P\d+\]\]")
# Placeholder with harmless inner whitespace, e.g. "[[ P1 ]]".
_LOOSE_PLACEHOLDER = re.compile(r"\[\[\s*P\s*(\d+)\s*\]\]")
_LATIN_WORD = re.compile(r"[A-Za-z]+(?:['’][A-Za-z]+)?")
# Latin-script terms a correct translation may contain even when the English
# source does not spell them out (organisation names and standard acronyms).
_ALLOWED_LATIN = {"nvq", "nysc", "naita", "vta", "ict", "ai", "lkr", "rs"}

TRANSLATION_INSTRUCTIONS = """You translate officer-facing explanations from an NYSC (Sri Lanka National Youth
Services Council) youth-training dashboard from English into Sinhala.

Rules:
1. Translate faithfully into natural, professional Sri Lankan Sinhala suitable for
   youth-services officers. Do not summarise, shorten or expand. Use natural Sinhala
   sentence order (verb at the end); do not copy English word order. Use standard
   Sinhala spelling (for example ගැළපේ, සඳහා).
1a. Write only in Sinhala script. The only exceptions are programme and skill names, acronyms
   and numbers that appear in the English source, which are copied unchanged. Never use words
   from any other language, and never transliterate ordinary English words into Latin letters.
1b. Use these dashboard terms consistently:
   member = සාමාජිකයා; officer = නිලධාරී; programme = වැඩසටහන; course = පාඨමාලාව;
   skill = කුසලතාව; selected skill = තෝරාගත් කුසලතාව; sector = ක්ෂේත්‍රය;
   exactly matches = හරියටම ගැළපේ; may suit = ගැළපිය හැක; practical skills = ප්‍රායෝගික කුසලතා;
   schedule preference = කැමති කාලසටහන; language preference = කැමති භාෂාව;
   full-time = පූර්ණ කාලීන; part-time = අර්ධ කාලීන; weekdays = සතියේ දිනවල;
   weekends = සති අන්තයේ; qualification = සුදුසුකම; course catalogue = පාඨමාලා නාමාවලිය;
   cluster = කණ්ඩායම; profile = කාණ්ඩය; historical survey group = පෙර සමීක්ෂණ කණ්ඩායම;
   household = ගෘහස්ථ; family = පවුල.
2. Preserve uncertainty exactly. Words such as "may", "might", "could", "possibly" and
   "potentially" must stay tentative in Sinhala (for example, "විය හැක", "හැකි විය හැක").
3. Keep the distinction between (a) what the individual member answered, (b) characteristics
   of a historical survey group or cluster, and (c) general programme or course information.
   Never present a group characteristic as the member's own answer.
4. Never turn a possible concern into a confirmed problem or deficiency.
5. Never add recommendations, claims, advice, warnings or statistics that are not in the source.
6. Preserve every number exactly as written, using the same digits: do not round, change
   precision (keep "28.0%" as "28.0%"), add or remove digits, or convert between digits and
   number words in either direction ("3" stays "3"; "two" is translated as a word, never "2").
7. Preserve percentages, dates, durations, monetary amounts, NVQ levels and qualification
   requirements exactly.
8. Tokens of the form [[P1]], [[P2]] stand for official programme names. Copy each token
   exactly, unchanged, as many times as it appears. Keep other technical acronyms
   (for example NVQ, ICT) in their original form.
9. Translate only the supplied explanatory text. Do not add explanations, notes or headings.
10. Return exactly one translated item per input programme, in the same order, with the same
   "index" values, the same number of discussion questions in the same order. Where an input
   value is null, the output value must be null: never write text into an empty field.
Return only the structured JSON requested."""


class TranslationRequestError(ValueError):
    """The client payload is not an acceptable translation request."""


class TranslationValidationError(ValueError):
    """The provider output failed the post-translation checks.

    `check` and `field` are fixed identifiers built from the structure only
    (never from recommendation text), so they are safe to log.
    """

    def __init__(self, check: str, field: str):
        super().__init__(f"{check} at {field}")
        self.check = check
        self.field = field


class _ProgrammeTranslation(BaseModel):
    model_config = ConfigDict(extra="forbid")
    index: int
    why_it_may_suit_this_user: str
    cluster_finding_summary: Optional[str]
    questions_to_discuss: List[str]


class TranslationOutput(BaseModel):
    model_config = ConfigDict(extra="forbid")
    programmes: List[_ProgrammeTranslation]
    no_recommendation_reason: Optional[str]


_PUBLIC_ERRORS = {
    "invalid_request": (400, "invalid_translation_request", "The translation request was not valid."),
    "missing_configuration": (503, "translation_unavailable", "Translation is temporarily unavailable."),
    "authentication_failure": (503, "translation_unavailable", "Translation is temporarily unavailable."),
    "provider_unavailable": (503, "translation_unavailable", "Translation is temporarily unavailable."),
    "upstream_timeout": (504, "translation_timeout", "Translation timed out. Please try again."),
    "invalid_provider_output": (502, "translation_invalid", "The translation could not be verified, so it was not shown."),
}


def safe_error(category: str) -> tuple[dict, int]:
    status, code, message = _PUBLIC_ERRORS.get(category, _PUBLIC_ERRORS["provider_unavailable"])
    return {"error": message, "error_code": code}, status


# ---------------------------------------------------------------------------
# Request validation
# ---------------------------------------------------------------------------

def _text(value, field: str, limit: int, *, nullable: bool = False) -> Optional[str]:
    if value is None and nullable:
        return None
    if not isinstance(value, str):
        raise TranslationRequestError(f"{field} must be a string")
    stripped = value.strip()
    if not stripped:
        if nullable:
            return None
        raise TranslationRequestError(f"{field} must not be empty")
    if len(stripped) > limit:
        raise TranslationRequestError(f"{field} is too long")
    return stripped


def validate_request(body) -> dict:
    """Return a normalised copy of an acceptable payload or raise TranslationRequestError."""
    if not isinstance(body, dict):
        raise TranslationRequestError("Body must be a JSON object")
    unknown = set(body) - _REQUEST_FIELDS
    if unknown:
        raise TranslationRequestError("Unknown request fields")
    programmes = body.get("programmes")
    if not isinstance(programmes, list) or len(programmes) > MAX_PROGRAMMES:
        raise TranslationRequestError("programmes must be a list of at most %d items" % MAX_PROGRAMMES)

    normalised = []
    for position, item in enumerate(programmes):
        if not isinstance(item, dict) or set(item) != _PROGRAMME_FIELDS:
            raise TranslationRequestError(f"programmes[{position}] has missing or unknown fields")
        questions = item["questions_to_discuss"]
        if not isinstance(questions, list) or len(questions) > MAX_QUESTIONS_PER_PROGRAMME:
            raise TranslationRequestError(f"programmes[{position}].questions_to_discuss is invalid")
        normalised.append({
            "course_name": _text(item["course_name"], "course_name", MAX_COURSE_NAME_CHARS),
            "why_it_may_suit_this_user": _text(item["why_it_may_suit_this_user"], "why_it_may_suit_this_user", MAX_TEXT_CHARS),
            "cluster_finding_summary": _text(item["cluster_finding_summary"], "cluster_finding_summary", MAX_TEXT_CHARS, nullable=True),
            "questions_to_discuss": [
                _text(question, "questions_to_discuss", MAX_QUESTION_CHARS) for question in questions
            ],
        })
    reason = _text(body.get("no_recommendation_reason"), "no_recommendation_reason", MAX_TEXT_CHARS, nullable=True)
    if not normalised and reason is None:
        raise TranslationRequestError("Nothing to translate")

    total = sum(
        len(p["why_it_may_suit_this_user"]) + len(p["cluster_finding_summary"] or "")
        + sum(len(q) for q in p["questions_to_discuss"])
        for p in normalised
    ) + len(reason or "")
    if total > MAX_TOTAL_CHARS:
        raise TranslationRequestError("Request text is too long")
    return {"programmes": normalised, "no_recommendation_reason": reason}


# ---------------------------------------------------------------------------
# Placeholder protection and output checks
# ---------------------------------------------------------------------------

def _protect(request: dict) -> tuple[dict, dict[str, str]]:
    """Replace canonical programme names with [[Pn]] tokens (longest names first)."""
    names = sorted({p["course_name"] for p in request["programmes"]}, key=len, reverse=True)
    tokens = {name: f"[[P{i + 1}]]" for i, name in enumerate(names)}

    def mask(text: Optional[str]) -> Optional[str]:
        if text is None:
            return None
        for name, token in tokens.items():
            text = text.replace(name, token)
        return text

    protected = {
        "programmes": [
            {
                "index": index,
                "why_it_may_suit_this_user": mask(p["why_it_may_suit_this_user"]),
                "cluster_finding_summary": mask(p["cluster_finding_summary"]),
                "questions_to_discuss": [mask(q) for q in p["questions_to_discuss"]],
            }
            for index, p in enumerate(request["programmes"])
        ],
        "no_recommendation_reason": mask(request["no_recommendation_reason"]),
    }
    return protected, {token: name for name, token in tokens.items()}


def _normalise_placeholders(text: Optional[str]) -> Optional[str]:
    """Collapse harmless whitespace inside placeholders: "[[ P1 ]]" -> "[[P1]]"."""
    if text is None:
        return None
    return _LOOSE_PLACEHOLDER.sub(lambda match: f"[[P{match.group(1)}]]", text)


def normalise_output(output: TranslationOutput) -> TranslationOutput:
    return TranslationOutput(
        programmes=[
            {
                "index": item.index,
                "why_it_may_suit_this_user": _normalise_placeholders(item.why_it_may_suit_this_user),
                "cluster_finding_summary": _normalise_placeholders(item.cluster_finding_summary),
                "questions_to_discuss": [_normalise_placeholders(q) for q in item.questions_to_discuss],
            }
            for item in output.programmes
        ],
        no_recommendation_reason=_normalise_placeholders(output.no_recommendation_reason),
    )


def _number_tokens(text: str) -> list[tuple[str, str, str]]:
    """Canonical (integer, decimals, percent) tokens; precision is kept as written.

    Only thousands separators and spaces before "%" are normalised, so
    30,000 == 30000 and 41.2% == 41.2 %, while 41.2% != 41% and 28.0 != 28.
    """
    without_placeholders = _PLACEHOLDER.sub(" ", text)
    return sorted(
        (integer.replace(",", ""), decimals, percent)
        for integer, decimals, percent in _NUMBER.findall(without_placeholders)
    )


def _unexpected_latin_words(source: str, translated: str) -> bool:
    """True when the translation contains a Latin-script word absent from the source.

    Names, acronyms and other English terms copied from the source remain
    allowed; stray words from other languages (e.g. "olan") are not.
    """
    allowed = {word.lower() for word in _LATIN_WORD.findall(_PLACEHOLDER.sub(" ", source))} | _ALLOWED_LATIN
    return any(word.lower() not in allowed for word in _LATIN_WORD.findall(_PLACEHOLDER.sub(" ", translated)))


def _check_pair(source: Optional[str], translated: Optional[str], field: str) -> None:
    if source is None:
        if translated not in (None, ""):
            raise TranslationValidationError("text_in_null_field", field)
        return
    if not isinstance(translated, str) or not translated.strip():
        raise TranslationValidationError("missing_translation", field)
    if not _SINHALA.search(translated):
        raise TranslationValidationError("not_sinhala", field)
    if _unexpected_latin_words(source, translated):
        raise TranslationValidationError("unexpected_latin_word", field)
    if _number_tokens(source) != _number_tokens(translated):
        raise TranslationValidationError("numbers_changed", field)
    if sorted(_PLACEHOLDER.findall(source)) != sorted(_PLACEHOLDER.findall(translated)):
        raise TranslationValidationError("placeholders_changed", field)


def verify_translation(protected: dict, output: TranslationOutput) -> None:
    """Raise TranslationValidationError for the first failing check.

    `output` must already be passed through normalise_output().
    """
    source_programmes = protected["programmes"]
    if len(output.programmes) != len(source_programmes):
        raise TranslationValidationError("programme_count_changed", "programmes")
    for position, (source, translated) in enumerate(zip(source_programmes, output.programmes)):
        base = f"programmes[{position}]"
        if translated.index != position:
            raise TranslationValidationError("programme_order_changed", f"{base}.index")
        _check_pair(source["why_it_may_suit_this_user"], translated.why_it_may_suit_this_user, f"{base}.why_it_may_suit_this_user")
        _check_pair(source["cluster_finding_summary"], translated.cluster_finding_summary, f"{base}.cluster_finding_summary")
        if len(translated.questions_to_discuss) != len(source["questions_to_discuss"]):
            raise TranslationValidationError("question_count_changed", f"{base}.questions_to_discuss")
        for q_index, (q_source, q_translated) in enumerate(zip(source["questions_to_discuss"], translated.questions_to_discuss)):
            _check_pair(q_source, q_translated, f"{base}.questions_to_discuss[{q_index}]")
    _check_pair(protected["no_recommendation_reason"], output.no_recommendation_reason, "no_recommendation_reason")


def _restore(text: Optional[str], names: dict[str, str]) -> Optional[str]:
    if text is None:
        return None
    return _PLACEHOLDER.sub(lambda match: names[match.group(0)], text)


# ---------------------------------------------------------------------------
# Provider call
# ---------------------------------------------------------------------------

def _build_input(protected: dict) -> str:
    import json
    return json.dumps(protected, ensure_ascii=False)


def call_translation_api(input_text: str):
    """Exactly one structured provider request. Returns the openai_client CallResult."""
    model = get_translation_model()
    started = time.monotonic()
    try:
        client = get_client()
        kwargs = dict(
            model=model,
            instructions=TRANSLATION_INSTRUCTIONS,
            input=input_text,
            text_format=TranslationOutput,
            timeout=TRANSLATION_TIMEOUT_SECONDS,
            max_output_tokens=TRANSLATION_MAX_OUTPUT_TOKENS,
        )
        kwargs["reasoning"] = {"effort": TRANSLATION_MODELS[model]["reasoning_effort"]}
        response = client.responses.parse(**kwargs)
        parsed = response.output_parsed
        if not isinstance(parsed, TranslationOutput):
            raise TranslationValidationError("structured_output_absent", "response")
        from openai_client import CallResult
        return CallResult(respondent_id="translation", model=model, success=True, parsed=parsed,
                          duration_seconds=round(time.monotonic() - started, 3), retry_count=0)
    except Exception as exc:  # noqa: BLE001 - provider boundary; never surface details
        return _failure_result("translation", model, started, exc)


def translate_recommendations(body) -> tuple[dict, int]:
    """Validate, translate once, verify. Never raises; returns (json, status)."""
    try:
        request = validate_request(body)
    except TranslationRequestError:
        return safe_error("invalid_request")

    protected, names = _protect(request)
    result = call_translation_api(_build_input(protected))
    # Timing/model diagnostics only — never any recommendation text.
    if not result.success:
        LOGGER.warning("Recommendation translation failed (category=%s, model=%s, seconds=%.1f).",
                       result.error_category, result.model, result.duration_seconds or 0.0)
        return safe_error(result.error_category or "provider_unavailable")

    output = normalise_output(result.parsed)
    try:
        verify_translation(protected, output)
    except TranslationValidationError as exc:
        # Only fixed check/field identifiers are logged — never any text.
        LOGGER.warning(
            "Recommendation translation rejected by validation (check=%s, field=%s, category=%s, model=%s, seconds=%.1f).",
            exc.check, exc.field, "invalid_provider_output", result.model, result.duration_seconds or 0.0,
        )
        return safe_error("invalid_provider_output")

    LOGGER.warning("Recommendation translation completed (model=%s, seconds=%.1f, programmes=%d).",
                   result.model, result.duration_seconds or 0.0, len(output.programmes))

    return {
        "language": "si",
        "programmes": [
            {
                "why_it_may_suit_this_user": _restore(item.why_it_may_suit_this_user, names),
                "cluster_finding_summary": _restore(item.cluster_finding_summary, names),
                "questions_to_discuss": [_restore(q, names) for q in item.questions_to_discuss],
            }
            for item in output.programmes
        ],
        "no_recommendation_reason": _restore(output.no_recommendation_reason, names),
    }, 200
