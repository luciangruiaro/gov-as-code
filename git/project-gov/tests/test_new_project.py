"""The bootstrap (tools/workspace/new_project.py): it finds the skeleton from its new home and leaves itself out."""
import importlib.util
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from support import ROOT

SCRIPT = ROOT / "tools" / "workspace" / "new_project.py"


def load():
    spec = importlib.util.spec_from_file_location("new_project", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@unittest.skipUnless((ROOT.parents[1] / "shared").is_dir(), "runs only inside the skeleton")
class Bootstrap(unittest.TestCase):
    def test_finds_both_halves(self):
        bootstrap = load()
        self.assertEqual(bootstrap.TEMPLATE_GOV, ROOT)
        self.assertTrue((bootstrap.TEMPLATE_SHARED / "PRD").is_dir())

    def test_every_sample_exists(self):
        bootstrap = load()
        missing = [p for p in bootstrap.sample_paths(bootstrap.TEMPLATE_GOV, bootstrap.TEMPLATE_SHARED)
                   if not p.exists()]
        self.assertEqual(missing, [])

    def test_leaves_itself_out_of_the_copy(self):
        bootstrap = load()
        self.assertIn(SCRIPT.name, bootstrap.SKIP(str(SCRIPT.parent), [SCRIPT.name, "index.py"]))

    def test_dry_run_changes_nothing(self):
        with tempfile.TemporaryDirectory() as tmp:
            dest = Path(tmp) / "ws"
            done = subprocess.run([sys.executable, str(SCRIPT), "--name", "Demo", "--slug", "demo", "--dest", str(dest),
                                   "--dry-run"], capture_output=True, encoding="utf-8")
            self.assertEqual(done.returncode, 0, done.stderr)
            self.assertIn("dry run: nothing changed", done.stdout)
            self.assertFalse(dest.exists())


if __name__ == "__main__":
    unittest.main()
