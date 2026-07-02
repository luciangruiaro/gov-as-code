"""tools/architecture/adr_index.py: the ADR index comes from the ADRs' own headers, and the committed one is current."""
from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from support import load_script

from workspace import config

adr_index = load_script("tools/architecture/adr_index.py", "adr_index")

ADR = """# ADR-00{n} — Title {n}

> **Status:** {status} · **Date:** 2026-01-0{n} · **Decided by:** architect · **Supersedes:** — · **Superseded-by:** —
> **Requirements:** FR-00{n} · **Backlog:** adr-00{n}
"""


class AdrIndex(unittest.TestCase):
    def test_rows_come_from_the_headers(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp)
            (folder / "ADR-002-b.md").write_text(ADR.format(n=2, status="DRAFT"), encoding="utf-8")
            (folder / "ADR-001-a.md").write_text(ADR.format(n=1, status="VISION-RATIFIED"), encoding="utf-8")
            (folder / "_template.md").write_text(ADR.format(n=9, status="DRAFT"), encoding="utf-8")
            table = adr_index.rows(folder)
        self.assertEqual(table[2], "| [ADR-001](ADR-001-a.md) | Title 1 | VISION-RATIFIED | 2026-01-01 | FR-001 |")
        self.assertEqual(table[3], "| [ADR-002](ADR-002-b.md) | Title 2 | DRAFT | 2026-01-02 | FR-002 |")
        self.assertEqual(len(table), 4)

    def test_the_committed_index_is_current(self):
        readme = (adr_index.DECISIONS / "README.md").read_text(encoding="utf-8")
        self.assertEqual(config.replace_block(readme, "ADR-INDEX", "\n".join(adr_index.rows())), readme,
                         "run py -3.12 tools/architecture/adr_index.py")


if __name__ == "__main__":
    unittest.main()
