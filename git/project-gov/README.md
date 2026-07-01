# project-gov: governance as code for Project Name

We version the code that defines our software, but the decisions, requirements and workflows that shape it usually live outside version control. This repository versions them: requirements, architectural decisions, workflows and project knowledge, all in one shared system that people and coding agents read and change by the same rules. Natural-language instructions (rules, skills, procedures) sit next to deterministic tools (sync, diff, index), so a mixed team shares context across the whole delivery lifecycle.

**Start here:** [`WORKSPACE.md`](WORKSPACE.md) (the map) · [`AGENTS.md`](AGENTS.md) (the rules, for people and agents) · [`prd/sync/SYNC.md`](prd/sync/SYNC.md) (how a PRD change reaches the decisions).

## The instruments
| Instrument | Where | Rule |
|---|---|---|
| Master PRD | Word on the shared drive; Markdown mirror in `prd/` | Edit Word, then sync. Never edit the mirror. |
| PRD impact | `prd/sync/impact.py` → `resources/audits/*_prd-adr-alignment.md` | A changed requirement id finds every decision that cites it. |
| Decisions | `architecture/decisions/ADR-*.md`, with a backlog and an index | Only ratified ADRs bind. Supersede; never weaken. |
| Deviations | `architecture/deviations/README.md` | Where code departs from a ratified ADR, with an exit condition. |
| Questions | `architecture/questions.md` | Unconfirmed claims carry a `q…` or `a…` id. |
| The map | `WORKSPACE.md` + `shared/INDEX.md` | Current state only; the tree and the index are generated. |
| Skills | `.agents/skills/` (`gov-*` and `dev-*`) | One set for every agent tool. |
| Working material | `resources/work/` (brainstorms, plans, debug), `resources/audits/` | Dated, never deleted; superseded with a banner. |

## How the law reaches the code
1. Each product repository's agent file has a `## Governance` block that links here and lists the ADRs it keeps.
2. Merge requests cite their ticket and the ADRs they touch. `dev-architecture-review` checks the diff against the ratified ADRs.
3. CI in the product repositories runs the checks named in the ADRs' acceptance criteria.
4. The daily digest's "architecture watch" names the ratified laws that the day's changes touch.

## Set up (once per machine)
```
py -3.12 --version                      # Python 3.12 or newer; pandoc 3+ for the PRD sync; git
copy .env.example .env                  # then fill in what you use (cp on macOS/Linux)
py -3.12 tools/skills/link.py           # Claude Code only: link the shared skills into .claude/skills/
py -3.12 -m unittest discover -s tests  # everything green
```
Link the shared drive in beside `git/` (WORKSPACE.md section 5), then `py -3.12 prd/sync/sync.py --check`.

## Status
| Part | State |
|---|---|
| PRD sync (`sync.py`), PRD impact (`impact.py`), ADR index, workspace index, skill linker, upstream skill sync | Implemented and tested |
| Backlog pull, feedback pull, code sync, digest collector, dashboard | Stubs with full contracts in their docstrings (`tools/README.md`): implement per project |
