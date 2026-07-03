"""Give Claude Code the shared skills.

Usage: py -3.12 tools/skills/link.py

Shared skills live in .agents/skills/, which Codex, Copilot and other agents read directly. Claude Code reads only
.claude/skills/, and .claude/ is gitignored here, so this script gives each shared skill a link there: a relative
symlink, or a directory junction on Windows without the symlink privilege. Run it once after cloning and again after a
skill is added or removed. A second run changes nothing. Links to skills that are gone are removed; real folders are
never touched.
"""
from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]  # tools/skills/link.py -> repo


def _is_link(path: Path) -> bool:
    return path.is_symlink() or path.is_junction()


def _make_link(link: Path, target: Path) -> None:
    try:
        link.symlink_to(os.path.relpath(target, link.parent), target_is_directory=True)
    except OSError:
        if os.name != "nt":
            raise
        # Windows without the symlink privilege: a directory junction needs none.
        subprocess.run(["cmd", "/c", "mklink", "/J", str(link), str(target)], check=True, capture_output=True)


def _remove_link(link: Path) -> None:
    try:
        link.unlink()
    except OSError:
        os.rmdir(link)  # a junction on Windows


def link_skills(source: Path, dest: Path) -> dict[str, list[str]]:
    """Link every skill folder in source into dest. Returns the skill names per outcome."""
    result: dict[str, list[str]] = {"linked": [], "kept": [], "removed": [], "conflict": []}
    skills = sorted(p.parent.name for p in source.glob("*/SKILL.md"))
    dest.mkdir(parents=True, exist_ok=True)
    for name in sorted(p.name for p in dest.iterdir()):
        entry = dest / name
        if _is_link(entry) and name not in skills:
            _remove_link(entry)
            result["removed"].append(name)
    for name in skills:
        link, target = dest / name, source / name
        if _is_link(link):
            if link.exists() and link.resolve() == target.resolve():
                result["kept"].append(name)
                continue
            _remove_link(link)
        elif link.exists():
            result["conflict"].append(name)
            continue
        _make_link(link, target)
        result["linked"].append(name)
    return result


def main() -> int:
    result = link_skills(ROOT / ".agents" / "skills", ROOT / ".claude" / "skills")
    print(f"{len(result['linked'])} linked, {len(result['kept'])} already linked, {len(result['removed'])} removed")
    for name in result["conflict"]:
        print(f"left alone: .claude/skills/{name} is a real folder, not a link")
    return 1 if result["conflict"] else 0


if __name__ == "__main__":
    sys.exit(main())
