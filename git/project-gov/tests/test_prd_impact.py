"""prd/sync/impact.py: a PRD change becomes the list of ids it touched, and the decisions that cite them."""
from __future__ import annotations

import re
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

from support import load_script

impact = load_script("prd/sync/impact.py", "prd_impact")
IDS = re.compile(r"\b(?:FR|NFR|GR|CFG|SM|TRG|OI)-[A-Z0-9]+(?:-[0-9]+)?\b")

OLD = """# PRD (Master) - Demo

> Mirror of the master PRD, which is kept in Word. Last change: 2026-01-12 (v0.1).

| Id | Requirement | Done when |
|----|----|----|
| FR-001 | Users sign in with single sign-on. | No page without a token. |
| FR-002 | Users submit a request. | It reaches the queue. |

| Id | Question |
|---|---|
| OI-001 | Which provider? |
| OI-002 | How long are attachments kept? |

## Change log

<!-- change log, newest first: rows are added by prd/sync/sync.py (see sync/SYNC.md) -->

| Date | Version | What changed |
|---|---|---|
| 2026-01-12 | v0.1 | First mirror |

<!-- /change log -->
"""

NEW = (OLD.replace("Users sign in with single sign-on.", "Users sign in with single sign-on; guests use a code.")
          .replace("| FR-002 | Users submit a request. | It reaches the queue. |",
                   "| FR-002   | Users submit a request.   | It reaches the queue.   |\n"
                   "| FR-005 | Approvers delegate. | A delegate decides. |")
          .replace("| OI-002 | How long are attachments kept? |\n", "")
          .replace("Last change: 2026-01-12 (v0.1)", "Last change: 2026-01-20 (v0.2)")
          .replace("| 2026-01-12 | v0.1 | First mirror |", "| 2026-01-20 | v0.2 | FR-001 reworded; FR-003 noted |\n"
                                                         "| 2026-01-12 | v0.1 | First mirror |"))


class Changes(unittest.TestCase):
    def setUp(self):
        self.found = {c.id: c for c in impact.changes(OLD, NEW, IDS)}

    def test_classifies_each_changed_id(self):
        self.assertEqual({k: c.kind for k, c in self.found.items()},
                         {"FR-001": "changed", "FR-005": "added", "OI-002": "removed"})

    def test_padding_banner_and_change_log_are_not_changes(self):
        self.assertNotIn("FR-002", self.found)  # only its table padding changed
        self.assertNotIn("FR-003", self.found)  # mentioned only in the change log

    def test_before_and_after_lines(self):
        self.assertIn("guests use a code", self.found["FR-001"].after[0])
        self.assertIn("single sign-on.", self.found["FR-001"].before[0])
        self.assertEqual(self.found["OI-002"].after, [])

    def test_no_previous_version_means_all_added(self):
        self.assertEqual({c.kind for c in impact.changes("", OLD, IDS)}, {"added"})


class Citations(unittest.TestCase):
    def test_cite_finds_decisions_and_skips_ignored_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "architecture" / "decisions").mkdir(parents=True)
            (root / "architecture" / "decisions" / "ADR-002-sso.md").write_text("Rests on FR-001.\n", encoding="utf-8")
            (root / "architecture" / "decisions" / "README.md").write_text("| ADR-002 | FR-001 |\n", encoding="utf-8")
            saved, impact.ROOT = impact.ROOT, root
            try:
                found = impact.changes(OLD, NEW, IDS)
                impact.cite(found, ["architecture/**/*.md"], IDS, ["architecture/decisions/README.md"])
            finally:
                impact.ROOT = saved
        fr1 = next(c for c in found if c.id == "FR-001")
        self.assertEqual(fr1.cited_by, [("architecture/decisions/ADR-002-sso.md", 1, "Rests on FR-001.")])
        self.assertEqual(fr1.lands_in, ["ADR-002"])

    def test_worksheet_has_a_question_with_a_blank_answer_per_id(self):
        found = impact.changes(OLD, NEW, IDS)
        sheet = impact.worksheet(found, "prd/a.md", "prd/b.md", "HEAD", "2026-01-20")
        self.assertEqual(sheet.count("**Answer:**"), len(found))
        self.assertIn("### Q1. FR-001 changed", sheet)


@unittest.skipUnless(shutil.which("git"), "git is not installed")
class PreviousMirror(unittest.TestCase):
    def test_finds_the_committed_mirror_after_a_rename(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            run = lambda *a: subprocess.run(["git", *a], cwd=root, check=True, capture_output=True)  # noqa: E731
            run("init", "-q")
            (root / "prd").mkdir()
            (root / "prd" / "PRD (Master) - Demo v0.1.md").write_text(OLD, encoding="utf-8", newline="\n")
            run("add", "-A")
            run("-c", "user.name=test", "-c", "user.email=test@example.com", "commit", "-q", "-m", "v0.1")
            (root / "prd" / "PRD (Master) - Demo v0.1.md").unlink()
            (root / "prd" / "PRD (Master) - Demo v0.2.md").write_text(NEW, encoding="utf-8", newline="\n")
            saved, impact.ROOT = impact.ROOT, root
            try:
                path, text = impact.previous_mirror("HEAD", "*Master*")
                missing = impact.previous_mirror("no-such-ref", "*Master*")
            finally:
                impact.ROOT = saved
        self.assertEqual(path, "prd/PRD (Master) - Demo v0.1.md")
        self.assertEqual(text, OLD)
        self.assertEqual(missing, (None, ""))


if __name__ == "__main__":
    unittest.main()
