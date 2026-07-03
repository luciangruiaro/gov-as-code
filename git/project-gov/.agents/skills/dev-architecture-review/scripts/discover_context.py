#!/usr/bin/env python3
"""Discover a repository's architecture-review corpus.

``dev-architecture-review`` is repo-agnostic: instead of hardcoding which
documents define a repo's architecture, it runs this scanner first and
derives its review checks from whatever the repo actually documents.

The scanner walks the target repo (pruning vendored/build dirs and, in a Git
repo, gitignored files) and reports, per category:

* ``architecture_docs``  — architecture*.md and architecture/ docs near the root, *doctrine*.md under docs/
* ``adr``                — ADR directories (docs/adr, adr/, docs/decisions, architecture/decisions) + ADR-*.md files
* ``diagrams``           — *.mmd count + up to 20 sample paths grouped by top dir
* ``rules``              — .claude/rules/, .cursor/rules/**, .agents/rules/, .codex/rules/, .github/instructions/
* ``agent_guides``       — CLAUDE.md / AGENTS.md / CONTRIBUTING.md / copilot-instructions.md (root + common homes)
* ``readmes``            — README.* within two levels of the root, to follow links to architecture docs
* ``precommit_hooks``    — hook ids + entries from .pre-commit-config.yaml (regex, no YAML dep)
* ``arch_lint_scripts``  — scripts/*arch*.py, scripts/*lint*.py, tools/*arch*.py
* ``git``                — default branch (origin/HEAD, falling back to master/main) + current branch

``notes`` records absences ("no ADR directory found") so the review can
say honestly which parts of its verdict rest on generic principles
rather than documented rules.

Stdlib-only, Python >= 3.9. Output ``--format md`` (agent-readable,
default) or ``--format json`` (tooling).
"""

from __future__ import annotations

import argparse
import fnmatch
import json
import os
import re
import subprocess
import sys
from pathlib import Path

PRUNED_DIR_NAMES = {
    ".git",
    ".hg",
    ".svn",
    "node_modules",
    ".venv",
    "venv",
    "env",
    "__pycache__",
    "dist",
    "build",
    ".tox",
    ".mypy_cache",
    ".ruff_cache",
    ".pytest_cache",
    "site-packages",
    ".next",
    "target",
    "vendor",
    ".idea",
    ".cache",
    "coverage",
    ".gradle",
}
# Installed skills' examples must not become rules for the repo they are copied into.
SKILL_HOMES = {".claude", ".agents", ".codex", ".cursor", ".github"}
RULE_HOMES = {".agents", ".codex"}
RULE_SUFFIXES = (".md", ".mdc")
DIAGRAM_SAMPLE_CAP = 20
ADR_FILE_CAP = 20
ADR_DIR_NAMES = {"adr", "adrs", "decisions"}
HOOK_ID_RE = re.compile(r"^\s*-\s*id:\s*(\S+)")
HOOK_ENTRY_RE = re.compile(r"^\s*entry:\s*(.+?)\s*$")


def find_repo_root(start: Path) -> Path | None:
    """Walk upward to the first directory holding ``.git`` (dir or worktree file)."""
    for candidate in (start, *start.parents):
        if (candidate / ".git").exists():
            return candidate
    return None


def _rel(path: Path, root: Path) -> str:
    return path.relative_to(root).as_posix()


def _git(root: Path, *args: str) -> str | None:
    try:
        result = subprocess.run(
            ["git", *args], cwd=str(root), capture_output=True, text=True,
            encoding="utf-8", errors="replace", timeout=10, check=False,
        )
    except (OSError, subprocess.TimeoutExpired):
        return None
    output = result.stdout.strip()
    return output if result.returncode == 0 and output else None


def detect_git(root: Path, notes: list[str]) -> dict[str, str | None]:
    """Resolve the default + current branch without guessing ``main``."""
    default: str | None = None
    origin_head = _git(root, "symbolic-ref", "--quiet", "refs/remotes/origin/HEAD")
    if origin_head:
        default = origin_head.removeprefix("refs/remotes/origin/")
    else:
        has_master = _git(root, "rev-parse", "--verify", "--quiet", "refs/heads/master") is not None
        has_main = _git(root, "rev-parse", "--verify", "--quiet", "refs/heads/main") is not None
        if has_master and not has_main:
            default = "master"
        elif has_main and not has_master:
            default = "main"
        elif has_master and has_main:
            default = "main"
            notes.append("both master and main exist and origin/HEAD is unset — assumed main; verify")
        else:
            notes.append("no master/main branch found — diff-vs-default-branch scopes unavailable")
    return {"default_branch": default, "current_branch": _git(root, "branch", "--show-current")}


def visible_files(root: Path) -> set[str] | None:
    """Tracked and untracked-but-not-ignored files, or None outside Git."""
    listing = _git(root, "ls-files", "--cached", "--others", "--exclude-standard", "-z")
    return set(listing.split("\0")) - {""} if listing else None


def walk_repo(root: Path) -> list[Path]:
    """Every file under *root*, with vendored/build dirs pruned."""
    found: list[Path] = []
    for dirpath, dirnames, filenames in os.walk(root):
        parent = Path(dirpath)
        dirnames[:] = sorted(
            d for d in dirnames
            if d not in PRUNED_DIR_NAMES
            and not (parent / d).is_symlink()
            and not (parent.name in SKILL_HOMES and d == "skills")
        )
        for filename in sorted(filenames):
            path = parent / filename
            if not path.is_symlink():
                found.append(path)
    return found


def parse_precommit(root: Path) -> list[dict[str, str]]:
    """Hook ids + entries from .pre-commit-config.yaml via line regexes."""
    config = root / ".pre-commit-config.yaml"
    if not config.is_file():
        return []
    hooks: list[dict[str, str]] = []
    current: dict[str, str] | None = None
    for line in config.read_text(encoding="utf-8", errors="replace").splitlines():
        id_match = HOOK_ID_RE.match(line)
        if id_match:
            current = {"id": id_match.group(1)}
            hooks.append(current)
            continue
        entry_match = HOOK_ENTRY_RE.match(line)
        if entry_match and current is not None and "entry" not in current:
            current["entry"] = entry_match.group(1)
    return hooks


def discover(root: Path) -> dict[str, object]:
    notes: list[str] = []
    corpus: dict[str, object] = {"repo_root": str(root), "git": detect_git(root, notes)}

    architecture_docs: list[str] = []
    adr_files: list[str] = []
    adr_dirs: list[str] = []
    diagrams: list[str] = []
    rules: list[str] = []
    agent_guides: list[str] = []
    readmes: list[str] = []
    arch_lint_scripts: list[str] = []

    # Gitignored files are local copies and scratch, not the repo's architecture.
    visible = visible_files(root)
    for path in walk_repo(root):
        relative = _rel(path, root)
        if visible is not None and relative not in visible:
            continue
        parts = Path(relative).parts
        lower_name = path.name.lower()

        # Depth caps keep the corpus to top-level docs — deep matches are
        # generated reports, per-component briefs, or vendored copies.
        if (
            lower_name.endswith(".md")
            and len(parts) <= 3
            and (lower_name.startswith("architecture") or "architecture" in [p.lower() for p in parts[:-1]])
        ) or (lower_name.endswith(".md") and "doctrine" in lower_name and parts[0] == "docs"):
            architecture_docs.append(relative)

        if lower_name.endswith(".md") and fnmatch.fnmatch(lower_name, "adr-*.md"):
            adr_files.append(relative)
        if (
            len(parts) > 1
            and any(part.lower() in ADR_DIR_NAMES for part in parts[:-1])
            and parts[0] in {"docs", "adr", "adrs", "decisions", "doc", "architecture"}
        ):
            parent = Path(relative).parent.as_posix()
            if parent not in adr_dirs:
                adr_dirs.append(parent)
            # EVERY record in the directory — listing only the first one seen
            # left every later ADR outside the review's corpus.
            if lower_name.endswith(".md") and relative not in adr_files:
                adr_files.append(relative)

        if lower_name.endswith(".mmd"):
            diagrams.append(relative)

        if (
            (lower_name.endswith(RULE_SUFFIXES) and ".claude" in parts and "rules" in parts)
            or (".cursor" in parts and "rules" in parts and path.is_file())
            or (lower_name.endswith(RULE_SUFFIXES) and RULE_HOMES.intersection(parts) and "rules" in parts)
            or (lower_name.endswith(".md") and ".github" in parts and "instructions" in parts)
        ):
            rules.append(relative)

        if lower_name in {"claude.md", "agents.md", "contributing.md", "copilot-instructions.md"} and len(parts) <= 2:
            agent_guides.append(relative)

        if lower_name.startswith("readme.") and len(parts) <= 2:
            readmes.append(relative)

        if (
            lower_name.endswith(".py")
            and len(parts) == 2
            and parts[0] in {"scripts", "tools"}
            and ("arch" in lower_name or "lint" in lower_name)
        ):
            arch_lint_scripts.append(relative)

    diagram_groups: dict[str, int] = {}
    for relative in diagrams:
        top = relative.split("/", 1)[0] if "/" in relative else "(root)"
        diagram_groups[top] = diagram_groups.get(top, 0) + 1

    # ADRs filed under an architecture/ folder are reported once, in the ADR group.
    corpus["architecture_docs"] = [doc for doc in architecture_docs if doc not in adr_files]
    corpus["adr"] = {"dirs": adr_dirs, "files": adr_files[:ADR_FILE_CAP], "total_files": len(adr_files)}
    corpus["diagrams"] = {
        "count": len(diagrams),
        "by_top_dir": diagram_groups,
        "samples": diagrams[:DIAGRAM_SAMPLE_CAP],
    }
    corpus["rules"] = rules
    corpus["agent_guides"] = agent_guides
    corpus["readmes"] = readmes
    corpus["precommit_hooks"] = parse_precommit(root)
    corpus["arch_lint_scripts"] = arch_lint_scripts

    if not architecture_docs and not rules:
        notes.append(
            "no architecture docs or rules files discovered — review must fall back to "
            "generic principles and should recommend writing architecture.md"
        )
    if not adr_files:
        notes.append("no ADR directory or ADR-*.md files found")
    if not corpus["precommit_hooks"]:
        notes.append("no .pre-commit-config.yaml hooks found")
    corpus["notes"] = notes
    return corpus


def render_markdown(corpus: dict[str, object]) -> str:
    git_info = corpus["git"]
    adr = corpus["adr"]
    diagrams = corpus["diagrams"]
    lines = [
        f"# Architecture corpus: {corpus['repo_root']}",
        "",
        f"- default branch: `{git_info['default_branch']}` | current: `{git_info['current_branch']}`",
        "",
        "## Read these before reviewing",
    ]
    for relative in dict.fromkeys([*corpus["agent_guides"], *corpus["rules"], *corpus["architecture_docs"]]):
        lines.append(f"- {relative}")
    if adr["dirs"] or adr["files"]:
        lines.append(f"- ADRs: {', '.join(adr['dirs']) or '(files only)'} ({adr['total_files']} files)")
    lines.append("")
    lines.append(f"## Diagrams: {diagrams['count']} .mmd " + json.dumps(diagrams["by_top_dir"]))
    if corpus["precommit_hooks"]:
        lines.append("")
        lines.append("## Pre-commit hooks")
        for hook in corpus["precommit_hooks"]:
            lines.append(f"- {hook.get('id', '?')}: `{hook.get('entry', '')}`")
    if corpus["readmes"]:
        lines.append("")
        lines.append("## READMEs (follow links to architecture docs)")
        for relative in corpus["readmes"]:
            lines.append(f"- {relative}")
    if corpus["arch_lint_scripts"]:
        lines.append("")
        lines.append("## Arch lint scripts (run advisory)")
        for relative in corpus["arch_lint_scripts"]:
            lines.append(f"- {relative}")
    if corpus["notes"]:
        lines.append("")
        lines.append("## Notes")
        for note in corpus["notes"]:
            lines.append(f"- {note}")
    return "\n".join(lines) + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--repo-root", type=Path, default=None, help="target repo root (default: walk up from cwd)")
    parser.add_argument("--format", choices=("md", "json"), default="md")
    args = parser.parse_args(argv)
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    root = args.repo_root.resolve() if args.repo_root else find_repo_root(Path.cwd())
    if root is None:
        print("ERROR: no .git found above the current directory; pass --repo-root", file=sys.stderr)
        return 2
    if not root.is_dir():
        print(f"ERROR: not a directory: {root}", file=sys.stderr)
        return 2
    corpus = discover(root)
    if args.format == "json":
        print(json.dumps(corpus, indent=2))
    else:
        print(render_markdown(corpus), end="")
    return 0


if __name__ == "__main__":
    sys.exit(main())
