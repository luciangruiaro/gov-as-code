"""The agent files agree: one set of hard rules, one skills table, skills every tool can load."""
from __future__ import annotations

import re
import unittest

from support import ROOT

SKILLS = ROOT / ".agents" / "skills"
ALLOWED_KEYS = {"name", "description", "argument-hint", "allowed-tools", "user_invocable"}


def hard_rules(path) -> str:
    text = path.read_text(encoding="utf-8")
    return text.split("<!-- HARD-RULES:BEGIN -->", 1)[1].split("<!-- HARD-RULES:END -->", 1)[0]


def frontmatter(path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return {}
    block = text[4:].split("\n---", 1)[0]
    return {k.strip(): v.strip() for k, _, v in (line.partition(":") for line in block.splitlines()) if k.strip()}


def shared_skills() -> list:
    return sorted(p for p in SKILLS.iterdir() if p.is_dir() and not p.name.startswith("local-"))


class AgentFiles(unittest.TestCase):
    def test_copilot_repeats_the_hard_rules_exactly(self):
        self.assertEqual(hard_rules(ROOT / "AGENTS.md"), hard_rules(ROOT / ".github" / "copilot-instructions.md"))

    def test_claude_md_imports_agents_md(self):
        first = (ROOT / "CLAUDE.md").read_text(encoding="utf-8").splitlines()[0]
        self.assertEqual(first, "@AGENTS.md")

    def test_every_skill_has_valid_frontmatter(self):
        for folder in shared_skills():
            with self.subTest(skill=folder.name):
                meta = frontmatter(folder / "SKILL.md")
                self.assertEqual(meta.get("name"), folder.name, "name must match the folder")
                self.assertTrue(meta.get("description"), "description is required")
                self.assertLessEqual(set(meta), ALLOWED_KEYS, "only portable frontmatter keys")
                self.assertRegex(folder.name, r"^(gov|dev)-[a-z0-9-]+$")

    def test_agents_md_lists_exactly_the_shared_skills(self):
        text = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
        listed = set(re.findall(r"^\| `((?:gov|dev)-[a-z0-9-]+)` \|", text, re.MULTILINE))
        self.assertEqual(listed, {p.name for p in shared_skills()})


if __name__ == "__main__":
    unittest.main()
