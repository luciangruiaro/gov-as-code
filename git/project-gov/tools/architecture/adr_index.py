"""Rebuild the ADR index in architecture/decisions/README.md from the ADRs' own headers.

Usage: py -3.12 tools/architecture/adr_index.py [--check]

Reads every architecture/decisions/ADR-NNN-*.md: the number and the title from its first heading, and the Status,
Date and Requirements from its header. Writes the table between <!-- ADR-INDEX:BEGIN --> and <!-- ADR-INDEX:END -->.
--check changes nothing and exits 1 when the index is stale. Deterministic: sorted by number, no clock.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))  # tools/, so the workspace package imports
from workspace import config  # noqa: E402

DECISIONS = config.ROOT / "architecture" / "decisions"
HEADING = re.compile(r"^# (ADR-\d{3})\s*[—–-]+\s*(.+?)\s*$", re.MULTILINE)
FIELD = r"\*\*{}:\*\*\s*([^·\n]+?)\s*(?:·|$)"


def field(text: str, name: str) -> str:
    found = re.search(FIELD.format(name), text, re.MULTILINE)
    return found.group(1).strip() if found else "—"


def rows(decisions: Path = DECISIONS) -> list[str]:
    table = ["| ADR | Title | Status | Date | Requirements |", "|---|---|---|---|---|"]
    for path in sorted(decisions.glob("ADR-[0-9][0-9][0-9]-*.md")):
        text = path.read_text(encoding="utf-8")
        heading = HEADING.search(text)
        number, title = (heading.group(1), heading.group(2)) if heading else (path.stem[:7], path.stem[8:])
        table.append(f"| [{number}]({path.name}) | {title} | {field(text, 'Status')} | {field(text, 'Date')} "
                     f"| {field(text, 'Requirements')} |")
    if len(table) == 2:
        table.append("| — | No ADRs yet | | | |")
    return table


def main() -> int:
    p = argparse.ArgumentParser(description="Rebuild the ADR index in architecture/decisions/README.md.")
    p.add_argument("--check", action="store_true", help="exit 1 if the index is stale; change nothing")
    args = p.parse_args()
    readme = DECISIONS / "README.md"
    old = readme.read_text(encoding="utf-8")
    new = config.replace_block(old, "ADR-INDEX", "\n".join(rows()))
    if args.check:
        print("the ADR index is current" if new == old else "the ADR index is stale: run py -3.12 tools/architecture/adr_index.py")
        return 0 if new == old else 1
    if new != old:
        readme.write_text(new, encoding="utf-8", newline="\n")
    print(f"{'updated' if new != old else 'unchanged'}: {readme.relative_to(config.ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
