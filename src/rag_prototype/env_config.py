"""
Secure environment/config loader for the RAG recommendation prototype ONLY.

Deliberately separate from any other feature's model configuration (e.g. a
"Reflection Journey" feature elsewhere in this codebase, if one exists) — this
module defines and reads OPENAI_API_KEY (from .env) and the production model
(hardcoded, NOT from .env — see PRODUCTION MODEL CONFIGURATION below).

SECURITY RULES ENFORCED HERE:
  - The API key is never printed, logged, or returned in any string representation.
  - Nothing in this module writes the key to a file.
  - has_api_key() reports presence only (True/False), never the value.
  - describe_key_status() returns a value safe to put in a report ("YES"/"NO").

=== PRODUCTION MODEL CONFIGURATION — SINGLE AUTHORITATIVE SOURCE ===

`.env`'s OPENAI_RECOMMENDATION_MODEL was found changed on disk during development
(to gpt-4o-mini) despite explicit instructions to keep the pipeline on gpt-5-mini —
proof that an environment-file-driven model setting is not a reliable production
control for a value that must not drift. To remove that ambiguity permanently, the
production model is now a HARDCODED constant below (PRODUCTION_RECOMMENDATION_MODEL),
completely independent of .env, and it is the ONLY value the full-cohort runner is
allowed to use — enforced by verify_production_model() at startup, which prints the
selected model and aborts if it is not exactly this value.

get_recommendation_model() (the old .env-driven getter) is kept ONLY for the older,
already-completed experimental scripts (run_api_pipeline.py, run_experiment_v2.py) that
predate this fix and are not part of the production path — it must never be used as a
silent fallback default anywhere a model is actually selected for a real API call (see
openai_client.py, which now requires an explicit model argument with no default).
"""
import os
from pathlib import Path

PRODUCTION_RECOMMENDATION_MODEL = "gpt-5-mini"

PROJECT_ROOT = Path(__file__).resolve().parents[2]  # .../ClusterRP
ENV_PATH = PROJECT_ROOT / ".env"

_loaded = False


def _load_dotenv_once():
    global _loaded
    if _loaded:
        return
    _loaded = True
    try:
        from dotenv import load_dotenv
        # override=False: never let a .env value clobber a value the user already
        # exported in their real shell environment.
        load_dotenv(dotenv_path=ENV_PATH, override=False)
    except ImportError:
        # python-dotenv not installed — fall back to a minimal manual parser so this
        # module still works if the dependency is somehow missing.
        if ENV_PATH.exists():
            for line in ENV_PATH.read_text().splitlines():
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                key, _, value = line.partition("=")
                key = key.strip()
                value = value.strip().strip('"').strip("'")
                if key and key not in os.environ:
                    os.environ[key] = value


def get_api_key():
    """Returns the raw key string, or None. Caller must never print/log this."""
    _load_dotenv_once()
    val = os.environ.get("OPENAI_API_KEY", "").strip()
    return val or None


def has_api_key() -> bool:
    return get_api_key() is not None


def get_recommendation_model(default: str = "gpt-4o-mini") -> str:
    """
    DEPRECATED for production use — reads the ambiguous, drift-prone .env setting.
    Retained only for the pre-existing experimental scripts that already used it
    (run_api_pipeline.py, run_experiment_v2.py). Do not call this from the full-cohort
    runner or from any new production code — use get_production_model() instead.
    """
    _load_dotenv_once()
    val = os.environ.get("OPENAI_RECOMMENDATION_MODEL", "").strip()
    return val or default


def get_production_model() -> str:
    """
    THE single authoritative source for which model the production full-cohort
    pipeline uses. Hardcoded, not read from .env or any other environment-mutable
    source, so it cannot silently drift.
    """
    return PRODUCTION_RECOMMENDATION_MODEL


def verify_production_model(selected_model: str, expected: str = PRODUCTION_RECOMMENDATION_MODEL) -> None:
    """
    Prints the selected model name and aborts (raises SystemExit) unless it is
    exactly `expected`. Call this once at the start of any production run, before
    any API call is made.
    """
    print(f"Selected model for this run: {selected_model}")
    if selected_model != expected:
        raise SystemExit(
            f"ABORT: production model mismatch. Expected exactly '{expected}', got "
            f"'{selected_model}'. Refusing to proceed — fix the model configuration "
            f"before running."
        )


def describe_key_status() -> str:
    """Safe-to-report string. Never includes the key value."""
    return "OPENAI_API_KEY detected: YES" if has_api_key() else "OPENAI_API_KEY detected: NO"


def env_file_path() -> str:
    return str(ENV_PATH)
