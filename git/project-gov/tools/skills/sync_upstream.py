"""Refresh the generic dev-* skills from their upstream.

Usage: py -3.12 tools/skills/sync_upstream.py [--from PATH_OR_URL] [--check]

The upstream is workspace.toml [skills] upstream, or --from: a local checkout, or a git URL that is shallow-cloned
into a temporary folder. Skills are read from the upstream's .agents/skills/dev-*/ (else .claude/skills/dev-*/). Each
one is copied into .agents/skills/, replacing its dev-* folder whole. gov-* and local-* skills are never touched.
dev-* skills that the upstream no longer has are listed, not deleted. --check changes nothing and exits 1 if any skill
differs from the upstream.

After a sync: run tools/skills/link.py (for Claude Code) and the tests, which require every skill to be listed in
AGENTS.md.
"""
from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))  # tools/, so the workspace package imports
from workspace import config  # noqa: E402

SKILLS = config.ROOT / ".agents" / "skills"
IGNORED = {"__pycache__", ".DS_Store"}


def files(folder: Path) -> dict[str, bytes]:
    return {p.relative_to(folder).as_posix(): p.read_bytes() for p in sorted(folder.rglob("*"))
            if p.is_file() and not IGNORED & set(p.relative_to(folder).parts)}


def upstream_skills(root: Path) -> dict[str, Path]:
    for base in (root / ".agents" / "skills", root / ".claude" / "skills"):
        found = {p.parent.name: p.parent for p in sorted(base.glob("dev-*/SKILL.md"))}
        if found:
            return found
    sys.exit(f"no dev-*/SKILL.md under {root}/.agents/skills or {root}/.claude/skills")


def compare(source: dict[str, Path], dest: Path) -> dict[str, list[str]]:
    result: dict[str, list[str]] = {"added": [], "updated": [], "unchanged": [], "obsolete": []}
    for name, folder in source.items():
        here = dest / name
        kind = "added" if not here.is_dir() else "unchanged" if files(here) == files(folder) else "updated"
        result[kind].append(name)
    result["obsolete"] = sorted(p.name for p in dest.glob("dev-*") if p.is_dir() and p.name not in source)
    return result


def apply(source: dict[str, Path], dest: Path, result: dict[str, list[str]]) -> None:
    for name in result["added"] + result["updated"]:
        if (dest / name).exists():
            shutil.rmtree(dest / name)
        shutil.copytree(source[name], dest / name, ignore=shutil.ignore_patterns(*IGNORED))


def run(upstream: str, check: bool) -> int:
    with tempfile.TemporaryDirectory(prefix="dev-skills-") as tmp:
        root = Path(upstream)
        if not root.is_dir():
            clone = subprocess.run(["git", "clone", "--depth", "1", "--quiet", upstream, str(Path(tmp) / "up")],
                                   capture_output=True, encoding="utf-8", errors="replace")
            if clone.returncode:
                sys.exit(f"could not clone {upstream}: {clone.stderr.strip()}")
            root = Path(tmp) / "up"
        source = upstream_skills(root)
        result = compare(source, SKILLS)
        if not check:
            apply(source, SKILLS, result)
    for kind in ("added", "updated", "unchanged"):
        print(f"{kind:>9}: {', '.join(result[kind]) or '-'}")
    if result["obsolete"]:
        print(f" obsolete: {', '.join(result['obsolete'])} (not in the upstream; review and delete by hand)")
    if check:
        return 1 if result["added"] or result["updated"] else 0
    if result["added"] or result["updated"]:
        print("next: py -3.12 tools/skills/link.py, then py -3.12 -m unittest discover -s tests")
    return 0


def main() -> int:
    p = argparse.ArgumentParser(description="Refresh the dev-* skills from their upstream.")
    p.add_argument("--from", dest="upstream", help="a local checkout or a git URL (default: workspace.toml)")
    p.add_argument("--check", action="store_true", help="exit 1 if any skill differs; change nothing")
    args = p.parse_args()
    return run(args.upstream or config.load().config["skills"]["upstream"], args.check)


if __name__ == "__main__":
    sys.exit(main())
