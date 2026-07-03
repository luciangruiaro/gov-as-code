"""tools/skills/: the linker and the upstream sync are idempotent, and never touch what is not theirs."""
from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from support import load_script

link = load_script("tools/skills/link.py", "skills_link")
sync_upstream = load_script("tools/skills/sync_upstream.py", "skills_sync_upstream")


def skill(root: Path, name: str, body: str = "x") -> None:
    (root / name).mkdir(parents=True, exist_ok=True)
    (root / name / "SKILL.md").write_text(f"---\nname: {name}\ndescription: {body}\n---\n", encoding="utf-8")


class LinkSkills(unittest.TestCase):
    def test_links_once_then_keeps_removes_and_leaves_real_folders(self):
        with tempfile.TemporaryDirectory() as tmp:
            source, dest = Path(tmp) / "src", Path(tmp) / "dest"
            skill(source, "gov-a")
            skill(source, "dev-b")
            self.assertEqual(sorted(link.link_skills(source, dest)["linked"]), ["dev-b", "gov-a"])
            self.assertEqual(sorted(link.link_skills(source, dest)["kept"]), ["dev-b", "gov-a"])
            self.assertTrue((dest / "gov-a" / "SKILL.md").is_file())
            for path in (source / "dev-b").iterdir():
                path.unlink()
            (source / "dev-b").rmdir()
            (dest / "local-c").mkdir()
            skill(source, "local-c")
            result = link.link_skills(source, dest)
            self.assertEqual(result["removed"], ["dev-b"])
            self.assertEqual(result["conflict"], ["local-c"])


class SyncDevSkills(unittest.TestCase):
    def test_adds_updates_and_reports_obsolete_without_touching_gov(self):
        with tempfile.TemporaryDirectory() as tmp:
            upstream = Path(tmp) / "up" / ".agents" / "skills"
            dest = Path(tmp) / "here"
            skill(upstream, "dev-new")
            skill(upstream, "dev-same")
            skill(dest, "dev-same")
            skill(dest, "dev-gone")
            skill(dest, "gov-own")
            source = sync_upstream.upstream_skills(Path(tmp) / "up")
            result = sync_upstream.compare(source, dest)
            self.assertEqual(result, {"added": ["dev-new"], "updated": [], "unchanged": ["dev-same"],
                                      "obsolete": ["dev-gone"]})
            sync_upstream.apply(source, dest, result)
            self.assertTrue((dest / "dev-new" / "SKILL.md").is_file())
            self.assertTrue((dest / "dev-gone").is_dir(), "obsolete skills are listed, not deleted")
            self.assertTrue((dest / "gov-own").is_dir())
            skill(upstream, "dev-same", body="changed upstream")
            self.assertEqual(sync_upstream.compare(source, dest)["updated"], ["dev-same"])


if __name__ == "__main__":
    unittest.main()
