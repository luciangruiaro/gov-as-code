"""Load workspace.toml and resolve the workspace's paths. Every tool in this repository goes through here.

Import it as `from workspace import config`, with tools/ on sys.path.

The governance repository sits in the workspace's git/ folder, next to the product repositories. The shared drive
is linked in beside git/ (WORKSPACE.md section 5). workspace.toml says where it is, so no tool hard-codes a path.
"""
from __future__ import annotations

import os
import tomllib
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]  # tools/workspace/config.py -> repo
CONFIG = ROOT / "workspace.toml"


@dataclass(frozen=True)
class Workspace:
    root: Path                       # this governance repository
    config: dict = field(repr=False)

    @property
    def name(self) -> str:
        return self.config["project"]["name"]

    @property
    def slug(self) -> str:
        return self.config["project"]["slug"]

    @property
    def shared(self) -> Path:
        """The shared drive's folder (it may be missing on a machine where the drive is not linked in)."""
        return self._resolve(self.config["shared"]["path"])

    @property
    def git_dir(self) -> Path:
        """The workspace's git/ folder, which holds this repository and the product repositories."""
        return self.root.parent

    @property
    def workspace_dir(self) -> Path:
        """The workspace's root: the folder that holds git/ and the link to the shared drive."""
        return self.git_dir.parent

    @property
    def prd(self) -> dict:
        return self.config["prd"]

    @property
    def repos(self) -> list[dict]:
        return list(self.config.get("repo", []))

    def section(self, name: str) -> dict:
        return dict(self.config.get(name, {}))

    def _resolve(self, value: str) -> Path:
        # normpath, not resolve: the shared drive is usually a link, and its path should stay inside the workspace.
        path = Path(value)
        return Path(os.path.normpath(path if path.is_absolute() else self.root / path))


def replace_block(text: str, name: str, content: str) -> str:
    """Replace what sits between <!-- NAME:BEGIN ... --> and <!-- NAME:END --> with content (generated blocks)."""
    begin, end = f"<!-- {name}:BEGIN", f"<!-- {name}:END -->"
    if begin not in text or end not in text:
        raise SystemExit(f"markers {begin} ... {end} not found")
    head, rest = text.split(begin, 1)
    marker_line, _, _ = rest.partition("\n")
    tail = rest.split(end, 1)[1]
    return f"{head}{begin}{marker_line}\n{content.strip(chr(10))}\n{end}{tail}"


def load(root: Path | None = None) -> Workspace:
    root = (root or ROOT).resolve()
    config_file = root / "workspace.toml"
    if not config_file.is_file():
        raise SystemExit(f"workspace.toml not found in {root}")
    with config_file.open("rb") as handle:
        return Workspace(root=root, config=tomllib.load(handle))
