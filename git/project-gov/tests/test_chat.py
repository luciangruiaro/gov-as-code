"""tools/reporting/chat.py and the .env loader: settings, signing, limits, and that a webhook URL never leaks."""
from __future__ import annotations

import contextlib
import io
import json
import os
import tempfile
import unittest
import urllib.error
from pathlib import Path
from unittest import mock

from support import load_script

from workspace import config

chat = load_script("tools/reporting/chat.py", "reporting_chat")

URL = "https://chat.googleapis.com/v1/spaces/AAA/messages?key=k&token=t"


class Response:
    def __init__(self, body: bytes):
        self.body = body

    def read(self) -> bytes:
        return self.body

    def __enter__(self):
        return self

    def __exit__(self, *exc) -> bool:
        return False


class Opener:
    """Stands in for urllib.request.urlopen and records what would have been sent."""

    def __init__(self, body: bytes = b'{"name": "spaces/AAA/messages/m1"}'):
        self.body, self.sent = body, []

    def __call__(self, req, timeout=None):
        self.sent.append(req)
        return Response(self.body)


def run(argv: list[str], settings: dict[str, str], opener=None) -> tuple[int, str, str]:
    out, err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        code = chat.main(argv, lookup=lambda name: settings.get(name, ""), opener=opener or Opener())
    return code, out.getvalue(), err.getvalue()


class Env(unittest.TestCase):
    def test_reads_comments_quotes_export_and_inline_comments(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / ".env"
            path.write_text("# a comment\nA=1\nexport B = two\nC=\"three # kept\"\nD='4'\nE=5 # dropped\nBROKEN\n"
                            "F=\n", encoding="utf-8")
            self.assertEqual(config.read_env(path), {"A": "1", "B": "two", "C": "three # kept", "D": "4", "E": "5",
                                                     "F": ""})
            self.assertEqual(config.read_env(Path(tmp) / "missing"), {})

    def test_the_environment_wins_over_the_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            (Path(tmp) / ".env").write_text("GOV_TEST_KEY=from-file\n", encoding="utf-8")
            self.assertEqual(config.setting("GOV_TEST_KEY", Path(tmp)), "from-file")
            with mock.patch.dict(os.environ, {"GOV_TEST_KEY": "from-env"}):
                self.assertEqual(config.setting("GOV_TEST_KEY", Path(tmp)), "from-env")
            self.assertEqual(config.setting("GOV_TEST_ABSENT", Path(tmp), "default"), "default")


class Settings(unittest.TestCase):
    def test_webhook_names_its_variable_and_accepts_the_older_names(self):
        with self.assertRaisesRegex(chat.Refused, "CHAT_WEBHOOK_TEST is not set"):
            chat.webhook({}.get, "test")
        self.assertEqual(chat.webhook({"GCHAT_WEBHOOK_TEST": URL}.get, "test"), ("GCHAT_WEBHOOK_TEST", URL))
        self.assertEqual(chat.webhook({}.get, "test", required=False), ("CHAT_WEBHOOK_TEST", ""))

    def test_refuses_unknown_spaces_and_plain_http(self):
        with self.assertRaisesRegex(chat.Refused, "unknown space"):
            chat.webhook({}.get, "general")
        with self.assertRaisesRegex(chat.Refused, "https"):
            chat.webhook({"CHAT_WEBHOOK_TEST": "http://example.com/hook"}.get, "test")

    def test_personas(self):
        self.assertEqual(chat.signature({}.get, "bot", "Acme"), "Acme bot")
        self.assertEqual(chat.signature({"CHAT_PERSONA_BOT": "Workspace bot"}.get, "BOT", "Acme"), "Workspace bot")
        self.assertEqual(chat.signature({"GCHAT_PERSONA_ARCHITECT": "The architect"}.get, "architect", "Acme"),
                         "The architect")
        self.assertEqual(chat.signature({}.get, "Release train", "Acme"), "Release train")


class Message(unittest.TestCase):
    def test_signs_and_keeps_the_limit(self):
        self.assertEqual(chat.compose("  hello  ", "Acme bot"), "*Acme bot* · hello")
        self.assertEqual(chat.compose("hello", None), "hello")
        with self.assertRaisesRegex(chat.Refused, "empty"):
            chat.compose("   ", "Acme bot")
        with self.assertRaisesRegex(chat.Refused, "4096"):
            chat.compose("x" * 4090, "Acme bot")

    def test_threads_go_in_the_payload_and_the_query(self):
        req = chat.request(URL, "hi", thread="digest-2026-11-20")
        self.assertTrue(req.full_url.endswith("&" + chat.REPLY))
        self.assertEqual(json.loads(req.data), {"text": "hi", "thread": {"threadKey": "digest-2026-11-20"}})
        self.assertEqual(chat.request(URL, "hi").full_url, URL)

    def test_service_errors_become_refusals(self):
        def failing(req, timeout=None):
            raise urllib.error.URLError("offline")
        with self.assertRaisesRegex(chat.Refused, "cannot reach"):
            chat.post(chat.request(URL, "hi"), failing)
        self.assertEqual(chat.post(chat.request(URL, "hi"), Opener(b"ok")), "?")


class CommandLine(unittest.TestCase):
    def test_dry_run_sends_nothing_and_works_without_a_webhook(self):
        opener = Opener()
        code, out, _ = run(["--to", "notifications", "--dry-run", "*Morning* team"], {}, opener)
        self.assertEqual(code, 0)
        self.assertIn("CHAT_WEBHOOK_NOTIFICATIONS NOT SET", out)
        self.assertIn("*Morning* team", out)
        self.assertEqual(opener.sent, [])

    def test_sends_signed_from_a_file_and_never_prints_the_url(self):
        opener = Opener()
        with tempfile.TemporaryDirectory() as tmp:
            draft = Path(tmp) / "draft.md"
            draft.write_text("﻿Line one\nLine two\n", encoding="utf-8")
            code, out, err = run(["--to", "test", "--persona", "architect", "--file", str(draft)],
                                 {"CHAT_WEBHOOK_TEST": URL, "CHAT_PERSONA_ARCHITECT": "The architect"}, opener)
        self.assertEqual(code, 0, err)
        self.assertIn("sent -> test as The architect [spaces/AAA/messages/m1]", out)
        self.assertNotIn("token", out + err)
        self.assertEqual(json.loads(opener.sent[0].data)["text"], "*The architect* · Line one\nLine two")

    def test_a_missing_webhook_is_an_error_not_a_crash(self):
        code, out, err = run(["--to", "discussion", "hi"], {})
        self.assertEqual(code, 1)
        self.assertIn("ERROR: CHAT_WEBHOOK_DISCUSSION is not set", err)
        self.assertEqual(out, "")


if __name__ == "__main__":
    unittest.main()
