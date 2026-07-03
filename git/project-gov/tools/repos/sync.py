"""Clone the product repositories beside this one and keep them current, fast-forward only. STUB: the contract below.

Usage: py -3.12 tools/repos/sync.py [--check] [--clone] [REPO ...]

Settings: workspace.toml [[repo]] slug, url. The clones live in the workspace's git/ folder, beside this repository.

Contract, for each repository (the REPO arguments, or every [[repo]]), one at a time, with stdin closed and
GIT_TERMINAL_PROMPT=0:
- Missing: clone it from url, but only with --clone. Otherwise report "missing".
- Present: `git fetch --all --prune`. Then, if the working tree is clean, HEAD is on a branch with an upstream, and
  the branch is only behind: `git merge --ff-only @{u}`. Skip and report any repository that is dirty, detached,
  diverged or has no upstream.
- --check fetches nothing and changes nothing; it only reports.
- Finish with a table: repository | branch | ahead/behind | dirty | last commit (date, short sha, subject) | action.

Rules: never merge (other than fast-forward), rebase, reset, stash, checkout or push. Exit 0 when every repository is
current or skipped with a reason; exit 1 on a git error.
"""
from __future__ import annotations

import argparse
import sys


def main() -> int:
    p = argparse.ArgumentParser(description="Keep the product repositories current, fast-forward only (stub).")
    p.add_argument("repos", nargs="*", metavar="REPO", help="repository slugs (default: every [[repo]])")
    p.add_argument("--check", action="store_true", help="report only: fetch nothing, change nothing")
    p.add_argument("--clone", action="store_true", help="clone the repositories that are missing")
    p.parse_args()
    print("repos/sync.py: not implemented yet. Its contract is this file's docstring, summarised in tools/README.md. "
          "Implement it for this project, tests first, then replace these two lines.", file=sys.stderr)
    return 2  # a stub


if __name__ == "__main__":
    sys.exit(main())
