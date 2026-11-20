# tools/: the deterministic half

Everything that can be computed is computed here, so people and agents spend judgment only where it is needed. Each tool uses the standard library only (Python 3.12+), reads `workspace.toml` through `workspace/config.py`, and gives the same output for the same input. The tools are grouped **one folder per job**, and the tools in a folder work together.

```
tools/
├── workspace/      the workspace itself
│   ├── config.py       loads workspace.toml, resolves every path, reads .env (all tools import it)
│   ├── index.py        writes the shared drive's INDEX.md and the tree in WORKSPACE.md
│   └── new_project.py  starts a new project's workspace from the skeleton (skeleton only; not copied)
├── architecture/   the decisions
│   └── adr_index.py    rebuilds the ADR index in architecture/decisions/README.md
├── skills/         the shared skills
│   ├── link.py         links .agents/skills/* into .claude/skills/ for Claude Code
│   └── sync_upstream.py  refreshes the dev-* skills from their upstream
├── mirrors/        one-way mirrors onto the shared drive                    (stubs)
│   ├── backlog.py      Jira or Azure DevOps → Jira/, grouped by state
│   └── feedback.py     the app's feedback table → Feedback/
├── repos/          the product repositories beside this one
│   ├── sync.py         clones them, then fast-forwards only                 (stub)
│   └── scan.py         refreshes their code graphs: Graphify and GitNexus
└── reporting/      what people read
    ├── digest.py       the workspace update's evidence bundle, since the last update sent
    ├── chat.py         posts one message to a team chat space (the only tool that sends anything)
    └── dashboard.py    one offline HTML dashboard                            (stub)
```

The PRD's own tools live with the PRD, in [`../prd/sync/`](../prd/sync/SYNC.md): `sync.py` (Word → Markdown mirror) and `impact.py` (mirror diff → the decisions it touches).

| Tool | State | Skill | Run |
|---|---|---|---|
| `workspace/index.py` | implemented | `gov-workspace-map` | `py -3.12 tools/workspace/index.py [--check]` |
| `workspace/new_project.py` | implemented; skeleton only, left out of new projects | — | from the skeleton's root: `py -3.12 git/project-gov/tools/workspace/new_project.py --name NAME --slug SLUG --dest PATH [--shared PATH] [--keep-samples] [--no-git] [--dry-run]` |
| `architecture/adr_index.py` | implemented | `gov-adr` | `py -3.12 tools/architecture/adr_index.py [--check]` |
| `skills/link.py` | implemented | — | `py -3.12 tools/skills/link.py` |
| `skills/sync_upstream.py` | implemented | — | `py -3.12 tools/skills/sync_upstream.py [--from PATH] [--check]` |
| `mirrors/backlog.py` | **stub** | `gov-backlog-sync` | `py -3.12 tools/mirrors/backlog.py [--full] [--dry-run]` |
| `mirrors/feedback.py` | **stub** | `gov-feedback-sync` | `py -3.12 tools/mirrors/feedback.py [--full] [--dry-run]` |
| `repos/sync.py` | **stub** | `gov-code-sync` | `py -3.12 tools/repos/sync.py [--check] [--clone]` |
| `repos/scan.py` | implemented | `gov-code-sync` | `py -3.12 tools/repos/scan.py [--check] [--only graphify\|gitnexus] [PATH ...]` |
| `reporting/digest.py` | implemented | `gov-digest` | `py -3.12 tools/reporting/digest.py [--since-last] [--hours N] [--until "YYYY-MM-DD HH:MM"] [--fetch]` |
| `reporting/chat.py` | implemented | `gov-chat`, `gov-digest` | `py -3.12 tools/reporting/chat.py [--to SPACE] [--persona NAME] [--thread KEY] [--dry-run] ("message" \| --file PATH)` |
| `reporting/dashboard.py` | **stub** | — | `py -3.12 tools/reporting/dashboard.py [--out FILE]` |

**A stub** has its intended command line and its full contract in the module docstring: inputs, outputs and file formats, and rules. It exits 2, pointing to that contract. To implement one: plan it (`dev-plan`), write the tests first, and keep the contract, or change the docstring and this README in the same commit.

**Conventions**
- **Placement:** a new tool goes in the folder of the job it serves. Create a new folder only for a new job.
- **Imports:** a tool puts `tools/` on `sys.path` and imports `from workspace import config`. Tools never import each other across folders; shared code belongs in `workspace/`.
- **Flags:** `--check` changes nothing and exits 1 when an output is stale. `--dry-run` prints the plan and writes nothing.
- **Writes:** write files only after every fetch has succeeded, and only when their content changed.
