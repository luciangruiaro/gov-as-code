"""Shared test setup: the repository's root, tools/ on the import path, and loading the PRD scripts as modules."""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "tools") not in sys.path:
    sys.path.insert(0, str(ROOT / "tools"))


def load_script(relative: str, name: str):
    """Import a script that is not in a package (prd/sync/*.py) as a module."""
    spec = importlib.util.spec_from_file_location(name, ROOT / relative)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module  # dataclasses look their module up while the module is still loading
    spec.loader.exec_module(module)
    return module
