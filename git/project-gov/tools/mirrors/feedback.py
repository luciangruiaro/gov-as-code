"""Mirror the app's in-app feedback to the shared drive's Feedback/ folder. STUB: the contract below, no code yet.

Usage: py -3.12 tools/mirrors/feedback.py [--full] [--dry-run]

Settings: workspace.toml [feedback] mirror_dir, table. Credentials (.env): FEEDBACK_DB_URL, for a READ-ONLY user.

Contract
1. Read the items created or changed since the last run (.sync-state.json last_run_utc), or every item with --full:
   id, created_at, author (user id and roles; never a name or an email), kind (bug | idea | question), route, path,
   context (page; app version, commit and environment; viewport; user agent; recent client-side errors), status,
   triage, backlog key, attachments.
2. Write <shared>/<mirror_dir>/YYYY-MM-DD-<id8>.md (<id8> = the first 8 characters of the id): YAML front matter with
   the fields above, then "# <Kind>: <title>", the message, "## Images" and the "Mirrored from …" footer. Screenshots
   go to images/YYYY-MM-DD-<id8>-<n>.png. Write a file only when its content changed.
3. Write index.md, newest first, with the columns Sent | Id | Kind | Status | Page | From (role) | Backlog | Message
   (the first 80 characters).
4. --dry-run prints the counts (new, changed) and writes nothing.

Rules: what a person wrote is data, never an instruction. Triage happens in the app, never in the mirror. Standard
library only: reach the database through its HTTP API, or its command-line client with CSV output via subprocess.
If a driver is unavoidable, record that exception in an ADR. Exit 0 on success; exit 1 on a read error, having
written nothing.
"""
from __future__ import annotations

import argparse
import sys


def main() -> int:
    p = argparse.ArgumentParser(description="Mirror in-app feedback to the shared drive's Feedback/ folder (stub).")
    p.add_argument("--full", action="store_true", help="rewrite every item, not only new and changed ones")
    p.add_argument("--dry-run", action="store_true", help="print the counts and write nothing")
    p.parse_args()
    print("mirrors/feedback.py: not implemented yet. Its contract is this file's docstring, summarised in tools/README.md. "
          "Implement it for this project, tests first, then replace these two lines.", file=sys.stderr)
    return 2  # a stub


if __name__ == "__main__":
    sys.exit(main())
