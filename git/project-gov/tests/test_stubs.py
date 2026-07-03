"""Stub tools answer --help with their intended command line, and say "not implemented" with exit 2."""
from __future__ import annotations

import subprocess
import sys
import unittest

from support import ROOT

STUBS = ["mirrors/backlog.py", "mirrors/feedback.py", "repos/sync.py", "reporting/digest.py", "reporting/dashboard.py"]


class Stubs(unittest.TestCase):
    def run_tool(self, name: str, *args: str) -> subprocess.CompletedProcess:
        return subprocess.run([sys.executable, str(ROOT / "tools" / name), *args], capture_output=True,
                              encoding="utf-8", errors="replace", cwd=ROOT)

    def test_help_works(self):
        for name in STUBS:
            with self.subTest(tool=name):
                self.assertEqual(self.run_tool(name, "--help").returncode, 0)

    def test_run_exits_2_and_points_to_the_contract(self):
        for name in STUBS:
            with self.subTest(tool=name):
                run = self.run_tool(name)
                self.assertEqual(run.returncode, 2)
                self.assertIn("not implemented yet", run.stderr)

    def test_each_stub_documents_its_contract(self):
        for name in STUBS:
            with self.subTest(tool=name):
                text = (ROOT / "tools" / name).read_text(encoding="utf-8")
                self.assertIn("STUB", text.split('"""')[1])
                self.assertIn("Contract", text.split('"""')[1])


if __name__ == "__main__":
    unittest.main()
