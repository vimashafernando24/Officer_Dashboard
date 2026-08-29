"""
§4/§5 — API-calling wrapper for the NEW-person recommendation architecture.

openai_client.call_recommendation_api() is hardcoded to the frozen 362-person
GOVERNANCE_INSTRUCTIONS + RespondentRecommendationResponse (module-level
imports, not parameters) — reusing it directly would require either modifying
it (not allowed: preserve the old pipeline unmodified) or hardcoding the new
governance/schema into it (wrong layer). Instead, this module reuses every
underlying primitive that IS reusable as-is (hard-timeout thread wrapper,
retry classification, model-family detection, error scrubbing, client
construction) directly from openai_client.py, and only re-implements the one
function that needed different `instructions`/`text_format` — kept as small
as possible.
"""
import time

from openai_client import (
    MAX_RETRIES, RETRY_BACKOFF_SECONDS, REQUEST_TIMEOUT_SECONDS,
    _is_reasoning_model, _is_retryable, _run_with_hard_timeout, _scrub,
    get_client, CallResult,
)
from env_config import get_api_key


def call_new_person_recommendation_api(respondent_id: str, input_text: str, model: str,
                                        instructions: str, text_format) -> CallResult:
    if not model:
        raise ValueError("call_new_person_recommendation_api() requires an explicit, non-empty model.")
    api_key = get_api_key()
    client = get_client()

    call_kwargs = dict(
        model=model, instructions=instructions, input=input_text,
        text_format=text_format, timeout=REQUEST_TIMEOUT_SECONDS,
    )
    if _is_reasoning_model(model):
        call_kwargs["reasoning"] = {"effort": "low"}
    else:
        call_kwargs["temperature"] = 0

    last_error = None
    for attempt in range(MAX_RETRIES + 1):
        start = time.monotonic()
        try:
            response = _run_with_hard_timeout(
                client.responses.parse, REQUEST_TIMEOUT_SECONDS + 5.0, **call_kwargs
            )
            duration = time.monotonic() - start
            parsed = response.output_parsed
            usage = response.usage
            return CallResult(
                respondent_id=respondent_id, model=model, success=True, parsed=parsed,
                input_tokens=usage.input_tokens if usage else None,
                output_tokens=usage.output_tokens if usage else None,
                total_tokens=usage.total_tokens if usage else None,
                cached_input_tokens=usage.input_tokens_details.cached_tokens if usage else None,
                reasoning_tokens=usage.output_tokens_details.reasoning_tokens if usage else None,
                duration_seconds=round(duration, 3), retry_count=attempt, response_id=response.id,
            )
        except Exception as exc:  # noqa: BLE001 — leaf I/O boundary, same pattern as openai_client.py
            duration = time.monotonic() - start
            last_error = _scrub(f"{type(exc).__name__}: {exc}", api_key)
            if attempt < MAX_RETRIES and _is_retryable(exc):
                time.sleep(RETRY_BACKOFF_SECONDS * (attempt + 1))
                continue
            return CallResult(
                respondent_id=respondent_id, model=model, success=False,
                duration_seconds=round(duration, 3), retry_count=attempt, error_message=last_error,
            )
