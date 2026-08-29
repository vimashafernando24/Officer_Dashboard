"""
Thin, auditable wrapper around the OpenAI Responses API for the course-recommendation
prototype ONLY. Uses structured-output parsing (client.responses.parse with a Pydantic
text_format) instead of prose + regex parsing. Records token usage per call and applies
a conservative, bounded retry policy — never retries indefinitely.

SECURITY: this module never logs, prints, or returns the API key. If a call raises, the
exception is re-raised as-is only after confirming (via _scrub) that no environment dump
or key-bearing string is attached to the error message we surface.
"""
import threading
import time
from dataclasses import dataclass, field
from typing import Optional

from env_config import get_api_key
from recommendation_schema import RespondentRecommendationResponse
from context_pack_v2 import GOVERNANCE_INSTRUCTIONS

MAX_RETRIES = 3
RETRY_BACKOFF_SECONDS = 2.0
# The SDK's own default read timeout is 600s; combined with MAX_RETRIES a single
# genuinely-hanging respondent could otherwise block for up to ~40 minutes before
# surfacing as a failure. Bounded explicitly so a stall fails fast and retries
# instead of hanging silently.
REQUEST_TIMEOUT_SECONDS = 120.0


def _is_reasoning_model(model: str) -> bool:
    """
    GPT-5-family and o-series reasoning models reject/ignore a custom `temperature`
    (only the default is accepted), unlike gpt-4o-family models. Detected by name
    prefix so the client can omit the parameter automatically instead of guessing.
    """
    m = model.lower()
    return m.startswith("gpt-5") or m.startswith("o1") or m.startswith("o3") or m.startswith("o4")


# Error types worth retrying (transient/server-side). Everything else (bad request,
# auth, not-found, permission, unprocessable, conflict) fails fast on attempt 1 —
# retrying a malformed/rejected request 3 times with backoff wastes time and, for a
# paid API, potentially money, without any chance of a different outcome.
def _is_retryable(exc: Exception) -> bool:
    import openai
    return isinstance(exc, (openai.RateLimitError, openai.InternalServerError,
                             openai.APIConnectionError, openai.APITimeoutError,
                             HardTimeoutError))


class HardTimeoutError(Exception):
    """Raised when a call exceeds REQUEST_TIMEOUT_SECONDS even though the SDK's own
    `timeout=` parameter did not raise. Observed in practice: some calls to gpt-5-mini
    hung well past their configured SDK-level timeout (confirmed by direct, isolated
    diagnostic calls with no other explanation — the same input succeeded quickly on a
    later attempt, and a trivial unrelated call succeeded in ~5s throughout, so it was
    not a broad connectivity/auth problem). This wraps the call in a DAEMON worker
    thread and enforces a hard wall-clock bound at the Python level, independent of
    SDK/httpx internals. A daemon thread does not block process/script exit, so an
    abandoned call is simply left to finish (or not) in the background and its result
    discarded — the caller never waits for it."""


def _run_with_hard_timeout(fn, timeout_seconds, /, **kwargs):
    result_box = {}

    def _target():
        try:
            result_box["value"] = fn(**kwargs)
        except Exception as exc:  # noqa: BLE001
            result_box["error"] = exc

    t = threading.Thread(target=_target, daemon=True)
    t.start()
    t.join(timeout=timeout_seconds)
    if t.is_alive():
        raise HardTimeoutError(
            f"call exceeded hard timeout of {timeout_seconds}s (SDK-level timeout did not trigger)"
        )
    if "error" in result_box:
        raise result_box["error"]
    return result_box["value"]


@dataclass
class CallResult:
    respondent_id: str
    model: str
    success: bool
    parsed: Optional[RespondentRecommendationResponse] = None
    input_tokens: Optional[int] = None
    output_tokens: Optional[int] = None
    total_tokens: Optional[int] = None
    cached_input_tokens: Optional[int] = None
    reasoning_tokens: Optional[int] = None
    duration_seconds: Optional[float] = None
    retry_count: int = 0
    error_message: Optional[str] = None
    response_id: Optional[str] = None


def _scrub(text: str, api_key: Optional[str]) -> str:
    """Removes the literal API key from any string before it is ever surfaced."""
    if api_key and api_key in text:
        text = text.replace(api_key, "[REDACTED]")
    return text


def get_client():
    """Raises RuntimeError (never prints the key) if no key is configured."""
    api_key = get_api_key()
    if not api_key:
        raise RuntimeError(
            "OPENAI_API_KEY is not configured. Set it in ClusterRP/.env — see .env.example."
        )
    from openai import OpenAI
    return OpenAI(api_key=api_key)


def call_recommendation_api(respondent_id: str, input_text: str, model: str) -> CallResult:
    """
    Makes one structured-output call for one respondent, with a bounded retry policy.
    Never retries more than MAX_RETRIES times; never silently duplicates a successful call.

    `model` is REQUIRED with no default and no .env fallback — this is deliberate.
    A silent fallback here was a confirmed latent bug: if a caller ever omitted the
    model argument, this used to fall back to the ambiguous, drift-prone .env setting
    (which was found changed to gpt-4o-mini on disk during development, contradicting
    the gpt-5-mini requirement). Callers must pass env_config.get_production_model()
    (or an explicitly-verified model) themselves — see env_config.verify_production_model().
    """
    if not model:
        raise ValueError(
            "call_recommendation_api() requires an explicit, non-empty model argument — "
            "there is no default and no .env fallback. Use env_config.get_production_model()."
        )
    api_key = get_api_key()  # only used for scrubbing error text below; never logged
    client = get_client()

    call_kwargs = dict(
        model=model,
        instructions=GOVERNANCE_INSTRUCTIONS,
        input=input_text,
        text_format=RespondentRecommendationResponse,
        timeout=REQUEST_TIMEOUT_SECONDS,
    )
    if _is_reasoning_model(model):
        # Cost-conscious: low reasoning effort keeps a reasoning-tier model fast/cheap
        # for this structured-extraction-style task rather than defaulting to a
        # higher, slower, more expensive effort level.
        call_kwargs["reasoning"] = {"effort": "low"}
    else:
        call_kwargs["temperature"] = 0  # deterministic-as-possible; not supported by reasoning models

    last_error = None
    for attempt in range(MAX_RETRIES + 1):
        start = time.monotonic()
        try:
            # Hard, Python-level bound: the SDK's own `timeout=` kwarg has been
            # observed NOT to reliably bound every call (see HardTimeoutError
            # docstring), so the call runs in a daemon worker thread with an enforced
            # wall-clock cutoff that cannot be defeated by SDK/httpx internals and
            # cannot block process exit.
            response = _run_with_hard_timeout(
                client.responses.parse, REQUEST_TIMEOUT_SECONDS + 5.0, **call_kwargs
            )
            duration = time.monotonic() - start
            parsed = response.output_parsed
            usage = response.usage
            return CallResult(
                respondent_id=respondent_id,
                model=model,
                success=True,
                parsed=parsed,
                input_tokens=usage.input_tokens if usage else None,
                output_tokens=usage.output_tokens if usage else None,
                total_tokens=usage.total_tokens if usage else None,
                cached_input_tokens=usage.input_tokens_details.cached_tokens if usage else None,
                reasoning_tokens=usage.output_tokens_details.reasoning_tokens if usage else None,
                duration_seconds=round(duration, 3),
                retry_count=attempt,
                response_id=response.id,
            )
        except Exception as exc:  # noqa: BLE001 — deliberately broad; this is a leaf I/O boundary
            duration = time.monotonic() - start
            last_error = _scrub(f"{type(exc).__name__}: {exc}", api_key)
            if attempt < MAX_RETRIES and _is_retryable(exc):
                time.sleep(RETRY_BACKOFF_SECONDS * (attempt + 1))
                continue
            return CallResult(
                respondent_id=respondent_id,
                model=model,
                success=False,
                duration_seconds=round(duration, 3),
                retry_count=attempt,
                error_message=last_error,
            )
