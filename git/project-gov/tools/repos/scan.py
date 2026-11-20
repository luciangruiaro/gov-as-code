"""Refresh the code graphs (Graphify and GitNexus) of this repository and the product repositories beside it.

Usage: py -3.12 tools/repos/scan.py [PATH ...] [--check] [--only graphify|gitnexus]

Agents read the code through these graphs instead of scanning whole repositories (AGENTS.md, "Code intelligence").
A graph is a snapshot, and this keeps the snapshots fresh. The targets are the PATHs given (relative to the current
folder), or else this governance repository plus every [[repo]] in workspace.toml that is cloned beside it.

For each target:
- Graphify: `python -m graphify update .` in the target. This is AST extraction only, so no language model and no
  cost. It writes graphify-out/ (GRAPH_REPORT.md, graph.json, graph.html). Docs and images join the graph only
  through the full /graphify skill in an AI assistant, which uses the model; run that on request, not from here.
- GitNexus: `gitnexus analyze . --index-only` in the target. This builds the index in .gitnexus/ that the GitNexus
  MCP server serves. It injects no files into the repository: no AGENTS.md or CLAUDE.md block, and no skills.
- Outputs stay out of Git: graphify-out/ is added to the repository's local .git/info/exclude unless it is already
  ignored. .gitnexus/ ignores itself. Nothing tracked is changed.

--check runs nothing. It reports each graph as fresh, stale (older than the last commit) or missing, and exits 1 if any
is not fresh. A tool that is not installed is reported and skipped: `pip install graphifyy`; `npm i -g gitnexus`.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))  # tools/, so the workspace package imports
from workspace import config  # noqa: E402

TOOLS = ("graphify", "gitnexus")
INSTALL = {"graphify": "pip install graphifyy", "gitnexus": "npm i -g gitnexus"}


def git(target: Path, *args: str) -> str | None:
    """Run git in target; its output, or None when git fails (for example, target is not in a repository)."""
    run = subprocess.run(["git", *args], cwd=target, capture_output=True, encoding="utf-8", errors="replace")
    return run.stdout.strip() if run.returncode == 0 else None


def head(target: Path) -> tuple[str | None, float | None]:
    """The commit target is at, and its time (seconds), or (None, None) outside a repository or before a commit."""
    when = git(target, "log", "-1", "--format=%ct")
    return git(target, "rev-parse", "HEAD"), (float(when) if when else None)


def find_targets(paths: list[str], ws: config.Workspace) -> list[Path]:
    if paths:
        return [Path(p).resolve() for p in paths]
    clones = [ws.git_dir / repo["slug"] for repo in ws.repos if repo.get("slug")]
    return [ws.root] + [clone for clone in clones if clone.is_dir()]


def graphify_state(target: Path, head_time: float | None) -> str:
    graph = target / "graphify-out" / "graph.json"
    if not graph.is_file():
        return "missing"
    return "stale" if head_time is not None and graph.stat().st_mtime < head_time else "fresh"


def gitnexus_state(target: Path, sha: str | None) -> str:
    meta = target / ".gitnexus" / "meta.json"
    if not meta.is_file():
        return "missing"
    if sha is None:
        return "fresh"  # not a repository, or no commit yet: nothing newer to compare with
    try:
        indexed = json.loads(meta.read_text(encoding="utf-8")).get("lastCommit", "")
    except (OSError, ValueError):
        return "stale"
    return "fresh" if indexed == sha else "stale"


def state(tool: str, target: Path) -> str:
    sha, when = head(target)
    return graphify_state(target, when) if tool == "graphify" else gitnexus_state(target, sha)


def command(tool: str, target: Path) -> list[str] | None:
    """The command that refreshes one graph, or None when the tool is not installed."""
    if tool == "graphify":
        return [sys.executable, "-m", "graphify", "update", "."] if importlib.util.find_spec("graphify") else None
    exe = shutil.which("gitnexus")
    if not exe:
        return None
    cmd = [exe, "analyze", ".", "--index-only"]
    # A folder inside a bigger repository (the skeleton's git/project-gov) is indexed on its own, not as the parent.
    return cmd if (target / ".git").exists() else cmd + ["--skip-git"]


def keep_out_of_git(target: Path) -> str | None:
    """Make sure graphify-out/ is ignored in target's repository; returns what was done, or None if nothing was."""
    if git(target, "rev-parse", "--show-toplevel") is None:
        return None
    if git(target, "check-ignore", "-q", "graphify-out/graph.json") is not None:
        return None  # already ignored (.gitignore or a previous run)
    exclude = git(target, "rev-parse", "--git-path", "info/exclude")
    if not exclude:
        return None
    path = Path(exclude) if Path(exclude).is_absolute() else target / exclude
    path.parent.mkdir(parents=True, exist_ok=True)
    text = path.read_text(encoding="utf-8") if path.is_file() else ""
    path.write_text(text + ("" if text.endswith("\n") or not text else "\n") + "graphify-out/\n", encoding="utf-8")
    return f"graphify-out/ added to {path}"


def label(target: Path) -> str:
    """target relative to the current folder when it is inside it, else in full."""
    try:
        rel = os.path.relpath(target)
    except ValueError:  # another drive on Windows
        return str(target)
    return str(target) if rel.startswith("..") else rel


def table(targets: list[Path], tools: tuple[str, ...]) -> tuple[list[str], bool]:
    rows = [f"{'target':<40} " + " ".join(f"{t:<10}" for t in tools)]
    fresh = True
    for target in targets:
        states = [state(t, target) for t in tools]
        fresh = fresh and all(s == "fresh" for s in states)
        rows.append(f"{label(target):<40} " + " ".join(f"{s:<10}" for s in states))
    return rows, fresh


def main() -> int:
    p = argparse.ArgumentParser(description="Refresh the Graphify and GitNexus code graphs.")
    p.add_argument("paths", nargs="*", metavar="PATH", help="folders to scan (default: this repo and the clones)")
    p.add_argument("--check", action="store_true", help="report fresh, stale or missing; run nothing; exit 1 if any "
                                                         "is not fresh")
    p.add_argument("--only", choices=TOOLS, help="refresh one of the two graphs")
    args = p.parse_args()
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    tools = (args.only,) if args.only else TOOLS
    targets = [t for t in find_targets(args.paths, config.load()) if t.is_dir()]
    if not targets:
        sys.exit("no folder to scan")

    if args.check:
        rows, fresh = table(targets, tools)
        print("\n".join(rows))
        if not fresh:
            print(f"\nrefresh with: py -3.12 {label(Path(__file__).resolve())}" + "".join(f" {p}" for p in args.paths))
        return 0 if fresh else 1

    failed = ran = 0
    for tool in tools:
        if command(tool, targets[0]) is None:
            print(f"{tool}: not installed, skipped ({INSTALL[tool]})")
    for target in targets:
        for tool in tools:
            cmd = command(tool, target)
            if cmd is None:
                continue
            print(f"{tool}: scanning {label(target)} ...", flush=True)
            run = subprocess.run(cmd, cwd=target, capture_output=True, encoding="utf-8", errors="replace",
                                 stdin=subprocess.DEVNULL)
            ran += 1
            if run.returncode:
                failed += 1
                tail = (run.stderr or run.stdout).strip().splitlines()[-5:]
                print(f"{tool}: FAILED in {label(target)}\n    " + "\n    ".join(tail))
        if note := keep_out_of_git(target):
            print(f"git: {note}")
    rows, _ = table(targets, tools)
    print("\n" + "\n".join(rows))
    if not ran:
        print("nothing ran: install a tool first")
        return 1
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
