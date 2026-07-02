"""prd/sync/sync.py: the change log survives every sync, and the committed mirror matches its Word source."""
from __future__ import annotations

import shutil
import unittest

from support import load_script

sync = load_script("prd/sync/sync.py", "prd_sync")

CONVERTED = "# Product Requirements Document (Master) - Demo\n\n| Id | Requirement |\n|----|----|\n| FR-001 | A |"
ROWS = ["| 2026-01-20 | v0.2 | FR-001 reworded |", "| 2026-01-12 | v0.1 | First mirror |"]


class Assemble(unittest.TestCase):
    def test_change_log_round_trip(self):
        text = sync.assemble(CONVERTED, ROWS)
        self.assertEqual(sync.log_rows(text), ROWS)
        self.assertIn("Last change: 2026-01-20 (v0.2)", text)
        self.assertTrue(text.startswith("# Product Requirements Document (Master) - Demo\n\n> Mirror of the master PRD"))

    def test_no_rows_no_change_log(self):
        text = sync.assemble(CONVERTED, [])
        self.assertNotIn("## Change log", text)
        self.assertEqual(sync.log_rows(text), [])

    def test_version_of(self):
        self.assertEqual(sync.version_of("PRD (Master) - Demo v1.2"), "v1.2")
        self.assertIsNone(sync.version_of("PRD (Master) - Demo"))


@unittest.skipUnless(shutil.which("pandoc"), "pandoc is not installed")
class CommittedMirror(unittest.TestCase):
    def test_the_mirror_matches_its_source(self):
        docs = [p for p in sync.SOURCE_DIR.glob(f"{sync.PATTERN}.docx") if not p.name.startswith("~$")]
        mirrors = sorted(sync.PRD.glob(f"{sync.PATTERN}.md"))
        if not docs or not mirrors:
            self.skipTest("no master PRD on the shared drive, or no mirror yet")
        docx = sync.find_source(None)
        converted, media, _ = sync.convert(sync.find_pandoc(), docx.absolute())
        old = mirrors[0].read_text(encoding="utf-8")
        self.assertEqual(mirrors[0].name, f"{docx.stem}.md")
        self.assertEqual(sync.assemble(converted, sync.log_rows(old)), old, "run py -3.12 prd/sync/sync.py")


if __name__ == "__main__":
    unittest.main()
