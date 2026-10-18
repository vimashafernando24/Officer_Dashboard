"""Regression tests for the retired /new-person page.

The standalone walkthrough page at /new-person was retired for Production, and the
new-person intake now lives in the officer dashboard at "/". Old links must redirect
there rather than return a 404, the retired walkthrough page must never be served,
and no other route may change. Uses Flask's test client only: no network or API calls.
"""

from __future__ import annotations

import os
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
os.environ.pop("ENABLE_LEGACY_PARTICIPANT_EXPLORER", None)

from profile_explorer_app import WALKTHROUGH_HTML_PATH, app  # noqa: E402


class NewPersonRouteTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = app.test_client()

    def test_new_person_redirects_to_the_officer_dashboard(self):
        for path in ("/new-person", "/new-person/"):
            with self.subTest(path=path):
                response = self.client.get(path)
                self.assertEqual(response.status_code, 302)
                self.assertEqual(response.headers["Location"], "/")

    def test_retired_walkthrough_page_is_never_served(self):
        response = self.client.get("/new-person", follow_redirects=False)
        body = response.get_data(as_text=True)
        # Only Flask's standard redirect stub is returned, never the walkthrough document.
        self.assertIn("Redirecting", body)
        if WALKTHROUGH_HTML_PATH.exists():
            walkthrough = WALKTHROUGH_HTML_PATH.read_text(encoding="utf-8")
            title = walkthrough.split("<title>", 1)[-1].split("</title>", 1)[0]
            self.assertNotIn(title, body)
            self.assertLess(len(body), len(walkthrough))

    def test_other_routes_are_unchanged(self):
        self.assertEqual(self.client.get("/does-not-exist").status_code, 404)
        # Guarded legacy participant-explorer endpoints stay hidden.
        for path in ("/api/respondents", "/api/explore"):
            with self.subTest(path=path):
                self.assertEqual(self.client.get(path).status_code, 404)
        self.assertEqual(self.client.get("/api/question_config").status_code, 200)
        # The dashboard root keeps its existing behaviour (served from the Vite build when present).
        root = self.client.get("/")
        self.assertIn(root.status_code, (200, 404))
        if root.status_code == 200:
            self.assertIn("text/html", root.content_type)


if __name__ == "__main__":
    unittest.main()
