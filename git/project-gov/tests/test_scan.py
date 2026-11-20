"""tools/repos/scan.py: which folders it scans, how it judges freshness, and that graph output stays out of Git."""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

from support import ROOT, load_script

from workspace import config

scan = load_script("tools/repos/scan.py", "repos_scan")


def repo(folder: Path) -> str:
    """A git repository with one commit in folder; returns the commit."""
    run = lambda *a: subprocess.run(["git", *a], cwd=folder, check=True, capture_output=True, text=True)  # noqa: E731
    run("init", "-q")
    (folder / "app.py").write_text("print('hi')\n", encoding="utf-8")
    run("add", "app.py")
    run("-c", "user.name=t", "-c", "user.email=t@example.com", "commit", "-q", "-m", "init")
    return run("rev-parse", "HEAD").stdout.strip()


class Targets(unittest.TestCase):
    def test_default_is_this_repo_plus_the_clones_that_exist(self):
        targets = scan.find_targets([], config.load())
        self.assertEqual(targets[0], ROOT)
        self.assertTrue(all(t.is_dir() for t in targets[1:]))

    def test_paths_given_win(self):
        self.assertEqual(scan.find_targets(["."], config.load()), [Path(".").resolve()])


@unittest.skipUnless(shutil.which("git"), "git is not installed")
class Freshness(unittest.TestCase):
    def test_missing_fresh_and_stale(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)
            sha = repo(target)
            self.assertEqual(scan.state("graphify", target), "missing")
            self.assertEqual(scan.state("gitnexus", target), "missing")

            out = target / "graphify-out"
            out.mkdir()
            (out / "graph.json").write_text("{}", encoding="utf-8")
            (target / ".gitnexus").mkdir()
            (target / ".gitnexus" / "meta.json").write_text(json.dumps({"lastCommit": sha}), encoding="utf-8")
            self.assertEqual(scan.state("graphify", target), "fresh")
            self.assertEqual(scan.state("gitnexus", target), "fresh")

            os.utime(out / "graph.json", (0, 0))  # older than the commit
            (target / ".gitnexus" / "meta.json").write_text(json.dumps({"lastCommit": "0" * 40}), encoding="utf-8")
            self.assertEqual(scan.state("graphify", target), "stale")
            self.assertEqual(scan.state("gitnexus", target), "stale")

    def test_graph_output_is_excluded_once(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)
            repo(target)
            self.assertIn("graphify-out/ added to", scan.keep_out_of_git(target))
            self.assertIsNone(scan.keep_out_of_git(target), "a second run changes nothing")
            exclude = (target / ".git" / "info" / "exclude").read_text(encoding="utf-8")
            self.assertEqual(exclude.count("graphify-out/"), 1)

    def test_a_folder_outside_git_is_left_alone(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.assertIsNone(scan.keep_out_of_git(Path(tmp)))


class Commands(unittest.TestCase):
    def test_gitnexus_never_injects_files_and_indexes_subfolders_on_their_own(self):
        if not shutil.which("gitnexus"):
            self.skipTest("gitnexus is not installed")
        with tempfile.TemporaryDirectory() as tmp:
            cmd = scan.command("gitnexus", Path(tmp))
        self.assertIn("--index-only", cmd)
        self.assertIn("--skip-git", cmd)

    def test_graphify_is_the_llm_free_update(self):
        cmd = scan.command("graphify", ROOT)
        if cmd is None:
            self.skipTest("graphify is not installed")
        self.assertEqual(cmd[1:], ["-m", "graphify", "update", "."])


if __name__ == "__main__":
    unittest.main()
