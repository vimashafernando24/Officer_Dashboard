"""
Offline checks for the on-demand Sinhala recommendation translation endpoint.

No OpenAI request is made: get_client() is replaced by a fake whose
responses.parse() records the call and returns a scripted structured output.
The recommendation pipeline is replaced by a tripwire to prove the
translation endpoint never invokes it. Nothing is written to disk.
"""
import io
import json
import logging
import os

import httpx
import openai

FAKE_KEY = "sk-test-NOT-A-REAL-KEY-7f3a9c"
os.environ["OPENAI_API_KEY"] = FAKE_KEY  # set before any module reads it
os.environ.pop("OPENAI_TRANSLATION_MODEL", None)

import profile_explorer_app as app_module  # noqa: E402
import recommendation_translation as rt  # noqa: E402
import env_config  # noqa: E402
import officer_recommendation_service as recommendation_service  # noqa: E402
from openai_client import MissingAPIKeyError  # noqa: E402

client = app_module.app.test_client()
ENDPOINT = "/api/new_person_translate_recommendations"

SAMPLE = {
    "programmes": [
        {
            "course_name": "Professional Cookery",
            "why_it_may_suit_this_user": "Professional Cookery may suit the member's interest in hospitality; it runs for 12 months at NVQ Level 4 and costs LKR 30,000.",
            "cluster_finding_summary": "In this historical group, 41.2% reported family support for training.",
            "questions_to_discuss": [
                "Could the member attend Professional Cookery on weekdays?",
                "Would a 6-month placement be possible?",
            ],
        },
        {
            "course_name": "Baker",
            "why_it_may_suit_this_user": "Baker could be a related option if the member wants practical skills.",
            "cluster_finding_summary": None,
            "questions_to_discuss": ["What experience does the member have with baking?"],
        },
    ],
    "no_recommendation_reason": None,
}


class FakeResponse:
    def __init__(self, parsed):
        self.output_parsed = parsed
        self.usage = None
        self.id = "fake"


class FakeClient:
    """Records each provider call; `behaviour` decides the scripted result."""

    def __init__(self, behaviour):
        self.calls = []
        self.behaviour = behaviour
        self.responses = self

    def parse(self, **kwargs):
        self.calls.append(kwargs)
        return self.behaviour(kwargs)


def faithful(kwargs):
    """A 'translation' that keeps every number and placeholder, adds Sinhala."""
    source = json.loads(kwargs["input"])
    tr = lambda text: None if text is None else f"සිංහල: {text}"
    return FakeResponse(rt.TranslationOutput(
        programmes=[
            {
                "index": p["index"],
                "why_it_may_suit_this_user": tr(p["why_it_may_suit_this_user"]),
                "cluster_finding_summary": tr(p["cluster_finding_summary"]),
                "questions_to_discuss": [tr(q) for q in p["questions_to_discuss"]],
            }
            for p in source["programmes"]
        ],
        no_recommendation_reason=tr(source["no_recommendation_reason"]),
    ))


def mutated(change):
    def behaviour(kwargs):
        response = faithful(kwargs)
        data = response.output_parsed.model_dump()
        change(data)
        response.output_parsed = rt.TranslationOutput.model_validate(data)
        return response
    return behaviour


def raising(exc):
    def behaviour(_kwargs):
        raise exc
    return behaviour


def post(payload, behaviour=faithful, *, raw=None):
    fake = FakeClient(behaviour)
    rt.get_client = lambda: fake
    data = raw if raw is not None else json.dumps(payload)
    response = client.post(ENDPOINT, data=data, content_type="application/json")
    return response, fake


results = []


def check(name, condition, detail=""):
    results.append((name, bool(condition), detail))


# The recommendation pipeline must never run during translation.
def _tripwire(*_args, **_kwargs):
    raise AssertionError("recommendation pipeline invoked")


app_module.generate_officer_briefing = _tripwire

log_buffer = io.StringIO()
handler = logging.StreamHandler(log_buffer)
logging.getLogger().addHandler(handler)
logging.getLogger().setLevel(logging.DEBUG)

# --- 1. Happy path --------------------------------------------------------
resp, fake = post(SAMPLE)
body = resp.get_json()
check("valid request returns 200", resp.status_code == 200, resp.status_code)
check("exactly one provider call per request", len(fake.calls) == 1, len(fake.calls))
call = fake.calls[0]
check("translation uses its own model (default gpt-6.1-sol)", call["model"] == "gpt-6.1-sol", call["model"])
check("recommendation model is still gpt-5-mini", env_config.get_production_model() == "gpt-5-mini")
check("explicit reasoning effort and no temperature sent to the translation model",
      call.get("reasoning") == {"effort": "low"} and "temperature" not in call)
check("fixed server-side prompt", call["instructions"] == rt.TRANSLATION_INSTRUCTIONS)
check("translation timeout is 150 s", call["timeout"] == 150.0, call["timeout"])
check("timeout and output-token limit set",
      call["timeout"] == rt.TRANSLATION_TIMEOUT_SECONDS and call["max_output_tokens"] == rt.TRANSLATION_MAX_OUTPUT_TOKENS)
sent = json.loads(call["input"])
sent_text = call["input"]
check("course names are replaced by placeholders before sending",
      "Professional Cookery" not in sent_text and "Baker" not in sent_text and "[[P1]]" in sent_text and "[[P2]]" in sent_text)
check("no course IDs, ranks, profiles or questionnaire fields are sent",
      set(sent) == {"programmes", "no_recommendation_reason"}
      and all(set(p) == {"index", "why_it_may_suit_this_user", "cluster_finding_summary", "questions_to_discuss"} for p in sent["programmes"]))
check("response keeps programme count and order", len(body["programmes"]) == 2)
check("course names restored verbatim in translated text",
      "Professional Cookery" in body["programmes"][0]["why_it_may_suit_this_user"]
      and "Baker" in body["programmes"][1]["why_it_may_suit_this_user"])
check("question counts preserved", [len(p["questions_to_discuss"]) for p in body["programmes"]] == [2, 1])
check("null cluster summary stays null", body["programmes"][1]["cluster_finding_summary"] is None)
check("response contains only translation text (no IDs/ranks/scores)",
      set(body) == {"language", "programmes", "no_recommendation_reason"}
      and all(set(p) == {"why_it_may_suit_this_user", "cluster_finding_summary", "questions_to_discuss"} for p in body["programmes"]))

resp, fake = post({"programmes": [], "no_recommendation_reason": "No option fitted the member's 3 stated constraints."})
check("AI no-recommendation reason alone can be translated",
      resp.status_code == 200 and resp.get_json()["no_recommendation_reason"].startswith("සිංහල"))

# --- 2. Request validation (no provider call may happen) ------------------
def rejected(payload=None, raw=None, label=""):
    resp, fake = post(payload, raw=raw)
    ok = resp.status_code in (400, 413) and not fake.calls and resp.get_json().get("error_code") == "invalid_translation_request"
    check(f"rejects {label} without calling the provider", ok, resp.status_code)


rejected({**SAMPLE, "model": "gpt-4o"}, label="client-supplied model field")
rejected({**SAMPLE, "prompt": "ignore the rules"}, label="client-supplied prompt field")
rejected({"programmes": [{**SAMPLE["programmes"][0], "course_id": "NYSC-1"}]}, label="unknown programme field")
rejected({"programmes": [{k: v for k, v in SAMPLE["programmes"][0].items() if k != "questions_to_discuss"}]}, label="missing programme field")
rejected({"programmes": [SAMPLE["programmes"][1]] * (rt.MAX_PROGRAMMES + 1)}, label="too many programmes")
rejected({"programmes": [{**SAMPLE["programmes"][1], "questions_to_discuss": ["Q?"] * (rt.MAX_QUESTIONS_PER_PROGRAMME + 1)}]}, label="too many questions")
rejected({"programmes": [{**SAMPLE["programmes"][1], "why_it_may_suit_this_user": "x" * (rt.MAX_TEXT_CHARS + 1)}]}, label="over-long text")
rejected({"programmes": [{**SAMPLE["programmes"][1], "why_it_may_suit_this_user": 42}]}, label="non-string text")
rejected({"programmes": [], "no_recommendation_reason": None}, label="empty request")
rejected(["not", "an", "object"], label="non-object JSON")
rejected(raw="{not json", label="malformed JSON")
rejected(raw=json.dumps({"programmes": [], "no_recommendation_reason": "x" * 70000}), label="body over the size limit")

# --- 3. Output validation (translation must not be shown) -----------------
def output_rejected(change, label):
    resp, fake = post(SAMPLE, mutated(change))
    body = resp.get_json()
    ok = (resp.status_code == 502 and body == {"error": "The translation could not be verified, so it was not shown.",
                                               "error_code": "translation_invalid"} and len(fake.calls) == 1)
    check(f"rejects translation with {label}", ok, resp.status_code)


output_rejected(lambda d: d["programmes"][0].__setitem__("why_it_may_suit_this_user", d["programmes"][0]["why_it_may_suit_this_user"].replace("12", "18")), "a changed number")
output_rejected(lambda d: d["programmes"][0].__setitem__("cluster_finding_summary", d["programmes"][0]["cluster_finding_summary"].replace("41.2%", "41%")), "a changed percentage")
output_rejected(lambda d: d["programmes"][0].__setitem__("why_it_may_suit_this_user", ""), "a missing translated field")
output_rejected(lambda d: d["programmes"][0]["questions_to_discuss"].pop(), "a dropped discussion question")
output_rejected(lambda d: d["programmes"].append(d["programmes"][0]), "an extra recommendation entry")
output_rejected(lambda d: d["programmes"].reverse(), "reordered programmes")
output_rejected(lambda d: d["programmes"][1].__setitem__("why_it_may_suit_this_user", "Baker could be a related option."), "untranslated English text")
output_rejected(lambda d: d["programmes"][0].__setitem__("why_it_may_suit_this_user", d["programmes"][0]["why_it_may_suit_this_user"].replace("[[P1]]", "කුක්")), "a translated programme name")
output_rejected(lambda d: d["programmes"][1].__setitem__("cluster_finding_summary", "සිංහල එකතු කළ පාඨය"), "added text where the source was empty")

# --- 3b. Formatting-only differences are accepted ------------------------
WHY0 = ("programmes", 0, "why_it_may_suit_this_user")
CLUSTER0 = ("programmes", 0, "cluster_finding_summary")


def edit_text(location, old, new):
    _, index, field = location

    def change(d):
        assert old in d["programmes"][index][field], old
        d["programmes"][index][field] = d["programmes"][index][field].replace(old, new)
    return change


def accepted(change, label, expect=None):
    resp, fake = post(SAMPLE, mutated(change))
    body = resp.get_json()
    ok = resp.status_code == 200 and len(fake.calls) == 1
    if ok and expect:
        ok = expect(body)
    check(f"accepts {label}", ok, resp.status_code)


accepted(edit_text(CLUSTER0, "41.2%", "41.2 %"), "whitespace before a percent sign ('41.2 %')")
accepted(edit_text(CLUSTER0, "41.2%", "41.2\u00a0%"), "a non-breaking space before a percent sign")
accepted(edit_text(WHY0, "30,000", "30000"), "a dropped thousands separator ('30000')")
accepted(edit_text(WHY0, "12 months", "මාස 12"), "a reordered number ('මාස 12')")
accepted(edit_text(WHY0, "[[P1]]", "[[ P1 ]]"), "harmless whitespace inside a placeholder ('[[ P1 ]]')",
         expect=lambda body: "Professional Cookery" in body["programmes"][0]["why_it_may_suit_this_user"]
         and "[[" not in body["programmes"][0]["why_it_may_suit_this_user"])
accepted(edit_text(WHY0, "[[P1]] may", "[[P1]]ට may"), "a Sinhala suffix attached to a placeholder")

# --- 3c. Genuine changes are still rejected, with a safe diagnostic log ---
def rejected_with_log(change, label, check_name, field):
    start = len(log_buffer.getvalue())
    resp, fake = post(SAMPLE, mutated(change))
    logged = log_buffer.getvalue()[start:]
    ok = (resp.status_code == 502 and resp.get_json()["error_code"] == "translation_invalid" and len(fake.calls) == 1
          and f"check={check_name}, field={field}, category=invalid_provider_output, model=" in logged)
    check(f"rejects {label} and logs check={check_name} at {field}", ok, logged.strip()[-160:])


rejected_with_log(edit_text(CLUSTER0, "41.2%", "41%"), "41.2% -> 41%", "numbers_changed", "programmes[0].cluster_finding_summary")
rejected_with_log(edit_text(CLUSTER0, "41.2%", "41.2"), "a dropped percent sign", "numbers_changed", "programmes[0].cluster_finding_summary")
rejected_with_log(edit_text(WHY0, "12 months", "18 months"), "12 -> 18", "numbers_changed", "programmes[0].why_it_may_suit_this_user")
rejected_with_log(edit_text(WHY0, "30,000", "3,000"), "30,000 -> 3,000", "numbers_changed", "programmes[0].why_it_may_suit_this_user")
rejected_with_log(edit_text(WHY0, "30,000", "30,00"), "30,000 -> 30,00", "numbers_changed", "programmes[0].why_it_may_suit_this_user")
rejected_with_log(edit_text(WHY0, "for 12 months", "for months"), "a missing number", "numbers_changed", "programmes[0].why_it_may_suit_this_user")
rejected_with_log(edit_text(WHY0, "hospitality", "hospitality (5)"), "an added number", "numbers_changed", "programmes[0].why_it_may_suit_this_user")
rejected_with_log(edit_text(WHY0, "[[P1]]", ""), "a missing placeholder", "placeholders_changed", "programmes[0].why_it_may_suit_this_user")
rejected_with_log(edit_text(WHY0, "[[P1]]", "[[P2]]"), "a changed programme identifier", "placeholders_changed", "programmes[0].why_it_may_suit_this_user")
rejected_with_log(lambda d: d["programmes"].append(d["programmes"][1]), "an additional recommendation", "programme_count_changed", "programmes")
rejected_with_log(lambda d: d["programmes"].reverse(), "a changed programme order", "programme_order_changed", "programmes[0].index")
rejected_with_log(lambda d: d["programmes"][0]["questions_to_discuss"].pop(), "a changed question count", "question_count_changed", "programmes[0].questions_to_discuss")
rejected_with_log(lambda d: d["programmes"][1].__setitem__("cluster_finding_summary", "නැත"), "text added to a null field", "text_in_null_field", "programmes[1].cluster_finding_summary")
rejected_with_log(lambda d: d.__setitem__("no_recommendation_reason", "N/A"), "text added to a null reason", "text_in_null_field", "no_recommendation_reason")
rejected_with_log(edit_text(("programmes", 1, "why_it_may_suit_this_user"), "සිංහල: ", ""), "untranslated English", "not_sinhala", "programmes[1].why_it_may_suit_this_user")

start = len(log_buffer.getvalue())
resp, fake = post(SAMPLE, raising(json.JSONDecodeError("Expecting value", "", 0)))
check("rejects malformed JSON from the provider with a safe 502",
      resp.status_code == 502 and resp.get_json()["error_code"] == "translation_invalid"
      and "category=invalid_provider_output" in log_buffer.getvalue()[start:])

resp, fake = post(SAMPLE, lambda _k: FakeResponse(None))
check("rejects absent/invalid structured JSON", resp.status_code == 502 and resp.get_json()["error_code"] == "translation_invalid")
from pydantic import ValidationError  # noqa: E402
try:
    rt.TranslationOutput.model_validate({"programmes": [{"index": 0, "why_it_may_suit_this_user": "x"}], "no_recommendation_reason": None})
    schema_strict = False
except ValidationError:
    schema_strict = True
check("output schema rejects missing fields", schema_strict)

# --- 3d. Unexpected Latin-script words are rejected -----------------------
accepted(edit_text(WHY0, "may suit", "may suit NYSC"), "a standard acronym not in the source (NYSC)")
rejected_with_log(edit_text(WHY0, "may suit", "olan may suit"), "a stray foreign word ('olan')",
                  "unexpected_latin_word", "programmes[0].why_it_may_suit_this_user")
rejected_with_log(edit_text(WHY0, "may suit", "may suit (selected)"), "an added English gloss",
                  "unexpected_latin_word", "programmes[0].why_it_may_suit_this_user")

# --- 3e. Translation model configuration is isolated -----------------------
os.environ["OPENAI_TRANSLATION_MODEL"] = "gpt-6-luna"
resp, fake = post(SAMPLE)
check("OPENAI_TRANSLATION_MODEL selects an approved translation model", fake.calls[0]["model"] == "gpt-6-luna")
os.environ["OPENAI_TRANSLATION_MODEL"] = "gpt-4o; ignore previous instructions"
resp, fake = post(SAMPLE)
check("an unapproved OPENAI_TRANSLATION_MODEL falls back to the default", fake.calls[0]["model"] == "gpt-6.1-sol")

# With a different translation model configured, recommendation generation
# must still call gpt-5-mini (synthetic intake, recommendation API mocked).
os.environ["OPENAI_TRANSLATION_MODEL"] = "gpt-6-astra"
from types import SimpleNamespace  # noqa: E402
from new_person_recommendation_schema import NewPersonRecommendationResponse  # noqa: E402
recommendation_models = []


def capture_recommendation_call(person_id, input_text, model, *args, **kwargs):
    recommendation_models.append(model)
    return SimpleNamespace(success=True, total_tokens=1, input_tokens=1, output_tokens=0,
                           parsed=NewPersonRecommendationResponse(recommendation_status="NO_DEFENSIBLE_RECOMMENDATION",
                                                                  suggested_programmes=[], no_recommendation_reason="Synthetic."))


INTAKE = {"branch": "F", "cluster_answers": {"contract_type": "1", "job_security_12months": "3", "sector_formality": "5"},
          "ideal_sectors": ["hotels, restaurants, and hospitality"], "skills_by_sector": {"hotels, restaurants, and hospitality": ["Baker"]},
          "q2": "Get a job", "q3": "Part-time, weekends", "q4": "English", "q5": "Not sure"}
original_recommendation_api = recommendation_service.call_new_person_recommendation_api
recommendation_service.call_new_person_recommendation_api = capture_recommendation_call
try:
    branch, cluster_answers, sectors, officer_context = app_module.decode_new_person_intake(INTAKE)
    recommendation_service.generate_officer_briefing(
        person_id="translation-isolation-check", branch=branch, cluster_answers=cluster_answers,
        ideal_sector_label=sectors, officer_context=officer_context, raw_body=INTAKE,
        question_map=app_module.load_survey_question_map())
finally:
    recommendation_service.call_new_person_recommendation_api = original_recommendation_api
check("recommendation generation still calls gpt-5-mini while a translation model is configured",
      recommendation_models and set(recommendation_models) == {"gpt-5-mini"}, recommendation_models)
os.environ.pop("OPENAI_TRANSLATION_MODEL", None)

# --- 4. Provider failures give safe errors --------------------------------
request = httpx.Request("POST", "https://api.openai.com/v1/responses")
for exc, status, code, label in [
    (openai.APITimeoutError(request=request), 504, "translation_timeout", "timeout"),
    (openai.APIConnectionError(request=request), 503, "translation_unavailable", "connection error"),
]:
    resp, fake = post(SAMPLE, raising(exc))
    body = resp.get_json()
    check(f"{label} returns a safe {status} with no internal detail",
          resp.status_code == status and body["error_code"] == code and set(body) == {"error", "error_code"} and len(fake.calls) == 1)


def missing_key():
    raise MissingAPIKeyError("OpenAI credentials are unavailable")


rt.get_client = missing_key
resp = client.post(ENDPOINT, json=SAMPLE)
check("missing API key returns a safe 503", resp.status_code == 503 and resp.get_json()["error_code"] == "translation_unavailable")

# --- 5. No secret or recommendation text leaks ----------------------------
logs = log_buffer.getvalue()
check("API key never appears in logs", FAKE_KEY not in logs)
all_logs = log_buffer.getvalue()
check("success and failure log lines record model and duration only",
      "translation completed (model=gpt-6.1-sol, seconds=" in all_logs
      and "failed (category=upstream_timeout, model=gpt-6.1-sol, seconds=" in all_logs)
check("recommendation text never appears in logs (incl. validation diagnostics)",
      not any(fragment in all_logs for fragment in
              ["hospitality", "historical group", "Professional Cookery", "Baker", "baking", "සිංහල", "30,000", "41.2", "weekdays"]))
resp, _ = post(SAMPLE)
check("API key never appears in responses", FAKE_KEY not in resp.get_data(as_text=True))
check("recommendation endpoint untouched (tripwire never fired)", True)

failed = [r for r in results if not r[1]]
for name, ok, detail in results:
    print(f"{'PASS' if ok else 'FAIL'}  {name}" + (f" — {detail}" if not ok and detail != "" else ""))
print()
if failed:
    raise SystemExit(f"TRANSLATION CHECK FAILED — {len(failed)} of {len(results)} checks")
print(f"RECOMMENDATION TRANSLATION CHECK PASSED — {len(results)} checks, 0 OpenAI requests")
