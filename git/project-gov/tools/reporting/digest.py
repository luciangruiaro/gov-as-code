"""Collect the evidence for the daily digest as one Markdown bundle. STUB: the contract below, no code yet.

Usage: py -3.12 tools/reporting/digest.py [--since HOURS] [--date YYYY-MM-DD] [--fetch]

The collector is deterministic: no language model, no judgment. The gov-digest skill composes the narrative from
its output and from nothing else.

Window: from Tuesday to Friday, the last 24 hours; on Monday, the last 72 hours; at weekends, exit 3 (no digest)
unless --since is given. Settings: workspace.toml [digest] (window_hours, team_notes, directives) and [[repo]].

Contract: print one Markdown document, with these sections in this order, each one saying "no change" when empty.
1. Code: for each repository in [[repo]] cloned in git/, plus this one, `git log --remotes --no-merges
   --since=<window>` (date, short sha, author mapped to a role through Team/Team structure.md, subject), and the
   paths changed (`git diff --stat`). --fetch runs `git fetch --all --prune` first.
2. Governance: this repository's commits touching prd/ (PRD versions), architecture/ (ADR status changes, new
   deviation rows, questions answered) and resources/audits/ (alignment worksheets with unanswered questions).
3. Backlog: the tickets in the Jira mirror whose `| Updated |` falls in the window, grouped by status change.
4. Feedback: the items created or changed in the window, from their front matter (kind, page, status).
5. Drive: the files saved in the window (a walk of the shared drive, four levels deep), leaving out the mirrors.
6. Calls: the notes and transcripts in Transcripts/ dated in the window.
7. Team: the directives dated in the window, the directives still running, and the full text of the bot notes.

Rules: read-only everywhere. Text copied from people's files is quoted as data. Exit 0 on success; exit 3 at weekends.
"""
from __future__ import annotations

import argparse
import sys


def main() -> int:
    p = argparse.ArgumentParser(description="Collect the daily digest's evidence bundle (stub).")
    p.add_argument("--since", type=int, metavar="HOURS", help="the window in hours (default: 24, or 72 on Mondays)")
    p.add_argument("--date", help="the digest's date, YYYY-MM-DD (default today)")
    p.add_argument("--fetch", action="store_true", help="git fetch every repository first")
    p.parse_args()
    print("reporting/digest.py: not implemented yet. Its contract is this file's docstring, summarised in tools/README.md. "
          "Implement it for this project, tests first, then replace these two lines.", file=sys.stderr)
    return 2  # a stub


if __name__ == "__main__":
    sys.exit(main())
