"""tools/workspace/: the configuration's marker helper, and the shared drive's INDEX.md."""
from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from support import ROOT, load_script

from workspace import config

index = load_script("tools/workspace/index.py", "workspace_index")


class Markers(unittest.TestCase):
    def test_replace_block_keeps_the_markers_and_the_rest(self):
        text = "before\n<!-- X:BEGIN (generated) -->\nold\n<!-- X:END -->\nafter\n"
        self.assertEqual(config.replace_block(text, "X", "new"),
                         "before\n<!-- X:BEGIN (generated) -->\nnew\n<!-- X:END -->\nafter\n")

    def test_missing_markers_stop(self):
        with self.assertRaises(SystemExit):
            config.replace_block("no markers", "X", "new")


class Config(unittest.TestCase):
    def test_paths_resolve_from_the_repository(self):
        ws = config.load()
        self.assertEqual(ws.root, ROOT)
        self.assertEqual(ws.git_dir, ROOT.parent)
        self.assertTrue(ws.slug)


class SharedIndex(unittest.TestCase):
    def test_index_is_deterministic_and_skips_noise(self):
        with tempfile.TemporaryDirectory() as tmp:
            shared = Path(tmp)
            (shared / "PRD").mkdir()
            (shared / "Decks").mkdir()
            (shared / "PRD" / "README.md").write_text("structure", encoding="utf-8")
            (shared / "PRD" / "~$lock.docx").write_bytes(b"x")
            (shared / "PRD" / "Master v0.1.docx").write_bytes(b"x" * 2048)
            first, second = index.index(shared), index.index(shared)
        self.assertEqual(first, second)
        self.assertIn("| [Master v0.1.docx](PRD/Master%20v0.1.docx) | 2 KB |", first)
        self.assertNotIn("~$lock", first)
        self.assertNotIn("README.md", first)
        self.assertIn("## Decks\n\n_No files yet", first)

    def test_workspace_md_has_the_tree_markers(self):
        text = (ROOT / "WORKSPACE.md").read_text(encoding="utf-8")
        self.assertIn("<!-- TREE:BEGIN", text)
        self.assertIn("<!-- TREE:END -->", text)


if __name__ == "__main__":
    unittest.main()
