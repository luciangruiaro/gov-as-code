@AGENTS.md

## Claude Code notes
- **One source.** `AGENTS.md` is the instruction set, and this file only imports it. When you work inside `git/project-gov/`, that folder's `CLAUDE.md` imports its own `AGENTS.md` the same way.
- **Skills.** When `gitnexus analyze` installs GitNexus's skills, they land in `.claude/skills/gitnexus/` (local and gitignored). The governance repository's shared skills live in `git/project-gov/.agents/skills/`. `py -3.12 git/project-gov/tools/skills/link.py` links them for Claude Code; open Claude Code in `git/project-gov/` to use them. The `/graphify` skill is installed per user, in `~/.claude/skills/graphify/`.
- **Never run `graphify claude install` here.** It would append a second copy of the code-graph section to this file. `AGENTS.md` already has it.
