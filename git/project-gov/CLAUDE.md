@AGENTS.md

## Claude Code notes
- **Skills.** Claude Code reads skills only from `.claude/skills/`, and `.claude/` is gitignored here. After cloning, and after a skill is added or removed, run `py -3.12 tools/skills/link.py`: it links each shared skill from `.agents/skills/` into that folder.
- **Settings.** `.claude/settings.json` and the rest of `.claude/` are personal and stay on your machine.
