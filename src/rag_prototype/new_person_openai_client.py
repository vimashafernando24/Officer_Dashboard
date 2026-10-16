"""
§4/§5 — API-calling wrapper for the NEW-person recommendation architecture.

openai_client.call_recommendation_api() is hardcoded to the frozen 362-person
GOVERNANCE_INSTRUCTIONS + RespondentRecommendationResponse (module-level
imports, not parameters) — reusing it directly would require hardcoding the new
governance/schema into it (wrong layer). Instead, this module reuses every
underlying primitive that IS reusable as-is (model-family detection, safe
error classification, and client construction) directly from openai_client.py,
and only re-implements the one
function that needed different `instructions`/`text_format` — kept as small
as possible.
"""
import time

from openai_client import (
    REQUEST_TIMEOUT_SECONDS, InvalidProviderOutputError,
    _failure_result, _is_reasoning_model, get_client, CallResult,
)


def call_new_person_recommendation_api(respondent_id: str, input_text: str, model: str,
                                        instructions: str, text_format,
                                        *, timeout_seconds: float = REQUEST_TIMEOUT_SECONDS
                                        ) -> CallResult:
    if not model:
        raise ValueError("call_new_person_recommendation_api() requires an explicit, non-empty model.")
    start = time.monotonic()
    try:
        client = get_client()
        call_kwargs = dict(
            model=model,
            instructions=instructions,
            input=input_text,
            text_format=text_format,
            timeout=timeout_seconds,
        )
        if _is_reasoning_model(model):
            call_kwargs["reasoning"] = {"effort": "low"}
        else:
            call_kwargs["temperature"] = 0

        response = client.responses.parse(**call_kwargs)
        parsed = response.output_parsed
        if parsed is None or not isinstance(parsed, text_format):
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
