"""
Thin, auditable wrapper around the OpenAI Responses API for the course-recommendation
prototype ONLY. Uses structured-output parsing (client.responses.parse with a Pydantic
text_format) instead of prose + regex parsing. Records token usage per call and disables
both SDK and application retries so each invocation makes at most one provider request.

SECURITY: this module never logs, prints, or returns the API key or raw provider errors.
"""
import time
from dataclasses import dataclass
from typing import Optional

from env_config import get_api_key
from recommendation_schema import RespondentRecommendationResponse
from context_pack_v2 import GOVERNANCE_INSTRUCTIONS

SDK_MAX_RETRIES = 0
REQUEST_TIMEOUT_SECONDS = 90.0

PUBLIC_ERROR_MESSAGES = {
    "missing_configuration": "Programme recommendation service is temporarily unavailable.",
    "authentication_failure": "Programme recommendation service is temporarily unavailable.",
    "provider_unavailable": "Programme recommendation service is temporarily unavailable.",
    "upstream_timeout": "Programme recommendation service timed out. Please try again.",
    "invalid_provider_output": "Programme recommendation service returned an invalid response.",
}


def _is_reasoning_model(model: str) -> bool:
    """
    GPT-5-family and o-series reasoning models reject/ignore a custom `temperature`
    (only the default is accepted), unlike gpt-4o-family models. Detected by name
    prefix so the client can omit the parameter automatically instead of guessing.
    """
    m = model.lower()
    return m.startswith("gpt-5") or m.startswith("o1") or m.startswith("o3") or m.startswith("o4")


class MissingAPIKeyError(RuntimeError):
    """Internal configuration category; never returned verbatim to API clients."""


class InvalidProviderOutputError(ValueError):
    """The provider completed, but did not return the requested structured object."""


def _provider_error_category(exc: Exception) -> str:
    """Classify an SDK failure without retaining or exposing its message."""
    if isinstance(exc, MissingAPIKeyError):
        return "missing_configuration"
    if isinstance(exc, InvalidProviderOutputError):
        return "invalid_provider_output"

    import openai
    if isinstance(exc, openai.APITimeoutError):
        return "upstream_timeout"
    if isinstance(exc, openai.AuthenticationError):
        return "authentication_failure"
    if isinstance(exc, (
        openai.RateLimitError,
        openai.InternalServerError,
        openai.APIConnectionError,
    )):
        return "provider_unavailable"

    try:
        from pydantic import ValidationError
    except ImportError:  # pragma: no cover - pydantic is a required dependency
        ValidationError = None
    if (
        (ValidationError is not None and isinstance(exc, ValidationError))
        or isinstance(exc, (ValueError, TypeError))
    ):
        return "invalid_provider_output"
    return "provider_unavailable"


@dataclass
class CallResult:
    respondent_id: str
    model: str
    success: bool
    parsed: Optional[object] = None
    input_tokens: Optional[int] = None
    output_tokens: Optional[int] = None
    total_tokens: Optional[int] = None
    cached_input_tokens: Optional[int] = None
    reasoning_tokens: Optional[int] = None
    duration_seconds: Optional[float] = None
    retry_count: int = 0
    error_category: Optional[str] = None
    error_message: Optional[str] = None
    response_id: Optional[str] = None


def _failure_result(respondent_id: str, model: str, started_at: float,
                    exc: Exception) -> CallResult:
    category = _provider_error_category(exc)
    return CallResult(
        respondent_id=respondent_id,
        model=model,
        success=False,
        duration_seconds=round(time.monotonic() - started_at, 3),
        retry_count=0,
        error_category=category,
        error_message=PUBLIC_ERROR_MESSAGES[category],
    )


def get_client():
    """Build a no-retry SDK client without ever printing or returning the key."""
    api_key = get_api_key()
    if not api_key:
        raise MissingAPIKeyError("OpenAI credentials are unavailable")
    from openai import OpenAI
    return OpenAI(api_key=api_key, max_retries=SDK_MAX_RETRIES)


def call_recommendation_api(respondent_id: str, input_text: str, model: str) -> CallResult:
    """
    Makes one synchronous structured-output call for one respondent. SDK and
    application retries are disabled so one invocation means one paid request.

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
    start = time.monotonic()
    try:
        client = get_client()
        call_kwargs = dict(
            model=model,
            instructions=GOVERNANCE_INSTRUCTIONS,
            input=input_text,
            text_format=RespondentRecommendationResponse,
            timeout=REQUEST_TIMEOUT_SECONDS,
        )
        if _is_reasoning_model(model):
            call_kwargs["reasoning"] = {"effort": "low"}
        else:
            call_kwargs["temperature"] = 0

        response = client.responses.parse(**call_kwargs)
        parsed = response.output_parsed
        if parsed is None or not isinstance(parsed, RespondentRecommendationResponse):
            raise InvalidProviderOutputError("Structured response was absent or invalid")
        usage = response.usage
        input_details = getattr(usage, "input_tokens_details", None) if usage else None
        output_details = getattr(usage, "output_tokens_details", None) if usage else None
        return CallResult(
            respondent_id=respondent_id,
            model=model,
            success=True,
            parsed=parsed,
            input_tokens=usage.input_tokens if usage else None,
            output_tokens=usage.output_tokens if usage else None,
            total_tokens=usage.total_tokens if usage else None,
            cached_input_tokens=getattr(input_details, "cached_tokens", None),
            reasoning_tokens=getattr(output_details, "reasoning_tokens", None),
            duration_seconds=round(time.monotonic() - start, 3),
            retry_count=0,
            response_id=response.id,
        )
    except Exception as exc:  # noqa: BLE001 - leaf provider boundary
        return _failure_result(respondent_id, model, start, exc)
