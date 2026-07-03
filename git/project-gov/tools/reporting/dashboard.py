"""Build the project dashboard: one offline HTML page of the numbers that matter. STUB: the contract below.

Usage: py -3.12 tools/reporting/dashboard.py [--out resources/audits/YYYY-MM-DD_dashboard.html]

Contract: read only files that are already in the workspace (the mirrors on the shared drive, this repository and the
clones), and write one self-contained HTML page styled with resources/ui-kit/ (CSS inlined, no external assets).
- Backlog: tickets by state; points per sprint, carry-over and cycle time (from the Jira mirror).
- Feedback: items per week by kind and by triage status (from the Feedback mirror).
- Code: commits per repository per week, from the clones.
- Decisions: ADRs by status, open deviations by severity, unanswered alignment questions.
- Requirements: ids by prefix (FR, NFR, …) and changes per PRD version (from the mirror's change log).

Rules: numbers come only from the files, with each tile naming its source. The same inputs give the same page.
Write next to it a Markdown twin (same name, .md) that agents can read.
"""
from __future__ import annotations

import argparse
import sys


def main() -> int:
    p = argparse.ArgumentParser(description="Build the project dashboard as one offline HTML page (stub).")
    p.add_argument("--out", help="the output file (default resources/audits/<today>_dashboard.html)")
    p.parse_args()
    print("reporting/dashboard.py: not implemented yet. Its contract is this file's docstring, summarised in tools/README.md. "
          "Implement it for this project, tests first, then replace these two lines.", file=sys.stderr)
    return 2  # a stub


if __name__ == "__main__":
    sys.exit(main())
