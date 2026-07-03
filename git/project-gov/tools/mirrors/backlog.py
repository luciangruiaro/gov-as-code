"""Mirror the backlog (Jira or Azure DevOps) to the shared drive's Jira/ folder. STUB: the contract below, no code yet.

Usage: py -3.12 tools/mirrors/backlog.py [--full | --since MINUTES] [--dry-run]

Settings: workspace.toml [backlog] system (jira | ado), project_key, mirror_dir.
Credentials (.env): JIRA_BASE_URL, JIRA_EMAIL, JIRA_TOKEN for Jira; ADO_ORG_URL, ADO_PAT, ADO_TEAM for Azure DevOps.

Contract
1. Fetch every ticket of the project (--full), or those updated since the last run plus 15 minutes (the default delta,
   from .sync-state.json; --since overrides it).
   - Jira: /rest/api/2/search with JQL `project = <KEY> ORDER BY Rank` (paged), plus the agile API for sprints, and
     the rest of any truncated comment thread.
   - Azure DevOps: the team's iterations, then one WIQL query per iteration plus the backlog by area path, then
     workitemsbatch in chunks of 200.
2. Group each ticket: current-sprint (in the active sprint), done (status category Done, or removed), backlog (the rest).
3. Plan: new, refreshed (content changed), moved (group changed), removed (left the project). --dry-run prints the
   plan and stops.
4. Write, and only after every fetch has succeeded: <shared>/<mirror_dir>/<group>/<KEY-n>.md, in the format set out
   in the drive's Jira/README.md (title line, Field/Value table, Description, Acceptance criteria, Comments, the
   "Mirrored from …" footer). Write a file only when its content changed, so the drive's dates show what moved.
   Delete the files of moved and removed tickets.
5. Index: index.md (the current sprint in rank order, the backlog in rank order, done newest first), _STATUS.md (the
   last 10 runs: when, by whom (role), the counts) and .sync-state.json (last_run_utc).

Rules: text only, never attachments. The mirror is one-way: never write to the backlog. Standard library only
(urllib.request, json). Exit 0 on success; exit 1 on any fetch error, having written nothing.
"""
from __future__ import annotations

import argparse
import sys


def main() -> int:
    p = argparse.ArgumentParser(description="Mirror the backlog to the shared drive's Jira/ folder (stub).")
    mode = p.add_mutually_exclusive_group()
    mode.add_argument("--full", action="store_true", help="fetch every ticket, not only those updated since last run")
    mode.add_argument("--since", type=int, metavar="MINUTES", help="fetch tickets updated in the last MINUTES")
    p.add_argument("--dry-run", action="store_true", help="print the plan (new, refreshed, moved, removed) and stop")
    p.parse_args()
    print("mirrors/backlog.py: not implemented yet. Its contract is this file's docstring, summarised in tools/README.md. "
          "Implement it for this project, tests first, then replace these two lines.", file=sys.stderr)
    return 2  # a stub


if __name__ == "__main__":
    sys.exit(main())
