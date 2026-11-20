# Governance as Code: the project workspace skeleton

We version the code that defines our software, but the decisions, requirements, workflows and knowledge that shape its development usually live outside version control. **Governance as code** brings them into a shared, versioned, continuously evolving system. Natural-language instructions (rules, skills, procedures) work alongside deterministic tools (sync, diff, index), so a mixed team of people and coding agents shares one context across the whole delivery lifecycle.

This repository is the **skeleton** every new project starts from. It has structure, templates, rules, skills, working tools, and a small fictional sample that shows the loop end to end. It holds no client content.

## The two halves
```
<workspace>/
├── shared/            the SHARED DRIVE: synced in near real time to the whole team (Drive, OneDrive, Dropbox)
│   ├── Assets/  Decks/  Delivery/  Demos/  Documentation/
│   ├── Feedback/      one-way mirror of the app's in-app feedback
│   ├── Jira/          one-way mirror of the backlog, grouped by state
│   ├── PRD/           the master PRD, in Word: the client's document
│   ├── Team/          structure, responsibilities and competency matrices, directives, ideas, proposals, bot notes
│   └── Transcripts/   client and internal calls
└── git/               the VERSIONED half
    ├── project-gov/   the governance repository → becomes <slug>-gov
    └── <slug>-be, -fe, -data, …   the product repositories, cloned beside it (not part of the skeleton)
```
- **Shared drive:** live material, the things that change by the hour and must reach everyone at once.
- **Git:** agreed material, the things where someone will ask "when and why did this change?" (requirements, decisions, plans, reviews).
- **The map:** [`git/project-gov/WORKSPACE.md`](git/project-gov/WORKSPACE.md) says what lives where and how it flows.

## The loop it is built around
```
Word PRD ──sync.py──▶ prd/*.md ──git diff──▶ impact.py ──▶ alignment worksheet ──answers──▶ ADRs ──bind──▶ code
   ▲                                                                                                     │
   └──── feedback, backlog, calls, directives ◀── shared drive ◀── mirrors ◀── the daily digest ◀────────┘
```
A requirement changes in Word, and the mirror in Git shows the exact diff. `impact.py` turns the changed requirement ids into the list of decisions, questions and plans that cite them. The design authority answers each question, and the ADRs move with a recorded reason. Try it: [`git/project-gov/prd/sync/SYNC.md`](git/project-gov/prd/sync/SYNC.md), "Try it on the sample".

## Start a new project
```
py -3.12 new-project.py --name "Acme Portal" --slug acme --dest "C:\Clients\Acme\workspace"
py -3.12 new-project.py --name "Acme Portal" --slug acme --dest "C:\Clients\Acme\workspace" --shared "G:\Shared drives\Acme\Engineering Workspace"
```
The script:
1. Copies both halves. With `--shared`, it fills that existing drive folder and links it into the workspace.
2. Renames `project-gov` to `acme-gov`, and the other placeholders with it.
3. Drops the fictional samples (`--keep-samples` keeps them).
4. Rebuilds the indexes, runs `git init` on the governance repository, and links the skills for Claude Code.

It commits nothing, then prints the next steps. `--dry-run` shows the plan first.

Requirements: Python 3.12+ (standard library only), pandoc 3+ for the PRD sync, and git.

## What is real and what is a stub
| Part | State |
|---|---|
| Folder structure, READMEs, templates, naming rules (both halves) | Complete |
| `AGENTS.md` (one rule set for every agent tool), `CLAUDE.md`, Copilot instructions, `WORKSPACE.md` | Complete |
| Skills: 13 generic `dev-*` (from the upstream `dev-skills` repository) and 7 project `gov-*` | Complete. The 4 `gov-*` skills that rely on stub tools say so. |
| PRD sync (Word → Markdown), PRD impact (diff → decisions → worksheet), ADR index, workspace index, code-graph scan (Graphify, GitNexus), skill linker, upstream skill sync, bootstrap | Implemented and tested |
| Backlog pull (Jira or Azure DevOps), feedback pull, code sync, digest collector, dashboard | Stubs, each with its full contract in the docstring: implement per project |

## Samples
All fictional, marked `SAMPLE`, dropped by `new-project.py`:
- a request-approval portal's master PRD (Word, plus its mirror);
- one ADR that cites it;
- an answered alignment worksheet;
- a brainstorm, a plan with a phase, an investigation;
- three backlog tickets, a feedback item, a stand-up note, an idea and a proposal.

## Keeping the skeleton current
- Generic skills: `cd git/project-gov && py -3.12 tools/skills/sync_upstream.py` (from `workspace.toml` `[skills] upstream`).
- Checks: `cd git/project-gov && py -3.12 -m unittest discover -s tests`.
- Code graphs (Graphify and GitNexus, so agents read the code through a graph instead of rescanning it): `py -3.12 git/project-gov/tools/repos/scan.py .` from the root, or `--check .` to see whether they are fresh. The rules are in [`AGENTS.md`](AGENTS.md).
- An improvement made in a project that holds for every project belongs back here.
