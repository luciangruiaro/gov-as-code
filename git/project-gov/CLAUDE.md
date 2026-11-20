@AGENTS.md

## Claude Code notes
- **Skills.** Claude Code reads skills only from `.claude/skills/`, and `.claude/` is gitignored here. After cloning, and after a skill is added or removed, run `py -3.12 tools/skills/link.py`: it links each shared skill from `.agents/skills/` into that folder.
- **Settings.** `.claude/settings.json` and the rest of `.claude/` are personal and stay on your machine.
- **Code graphs.** `AGENTS.md` ("Code intelligence") is the instruction; this file adds nothing to it. GitNexus reaches you through its MCP server, and Graphify through its CLI and the `/graphify` skill. Never run `graphify claude install` here: it would append a second copy of the section to this file.
