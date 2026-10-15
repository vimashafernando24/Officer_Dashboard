"""Vercel serverless entrypoint for the existing Flask API.

The application itself remains in ``src/rag_prototype/profile_explorer_app.py``.
This adapter only makes that already-existing WSGI app discoverable to Vercel.
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "src" / "rag_prototype"
sys.path.insert(0, str(BACKEND))

from profile_explorer_app import app  # noqa: E402,F401
