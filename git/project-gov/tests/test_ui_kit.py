"""resources/ui-kit/: prodigy-tokens.css says exactly what the canonical ui-kit.md says."""
from __future__ import annotations

import re
import unittest

from support import ROOT

KIT = ROOT / "resources" / "ui-kit"
DECL = re.compile(r"(--[a-z0-9-]+):\s*([^;]+);")


def declarations(text: str) -> dict[str, str]:
    return {name: " ".join(value.split()) for name, value in DECL.findall(text)}


class UiKit(unittest.TestCase):
    def setUp(self):
        self.md = (KIT / "ui-kit.md").read_text(encoding="utf-8")
        css = (KIT / "prodigy-tokens.css").read_text(encoding="utf-8")
        self.light = declarations(css.split(':root[data-theme="dark"]', 1)[0])
        self.dark = declarations(css.split(':root[data-theme="dark"]', 1)[1].split("@media", 1)[0])

    def test_light_tokens_match_the_css_variable_reference(self):
        reference = self.md.split("## 9. CSS Variable Reference", 1)[1].split("### Superadmin SPA layout vars", 1)[0]
        expected = declarations(reference)
        self.assertTrue(expected, "section 9 has no declarations")
        for name, value in expected.items():
            with self.subTest(token=name):
                self.assertEqual(self.light.get(name), value)

    def test_dark_colours_match_the_dark_theme_table(self):
        table = self.md.split("### 1.2 Dark Theme", 1)[1].split("## 2.", 1)[0]
        expected = dict((name, value) for value, name in re.findall(r"`(#[0-9A-Fa-f]{6})` \| `(--color-[a-z-]+)`", table))
        self.assertEqual(len(expected), 13)
        self.assertEqual(self.dark, expected)


if __name__ == "__main__":
    unittest.main()
