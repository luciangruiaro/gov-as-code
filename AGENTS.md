# AGENTS.md: rules for every agent in this repository

This repository is the **governance-as-code skeleton**: the template every new project's workspace starts from ([`README.md`](README.md)). It holds both halves of a workspace: `shared/` (the template of the synced drive) and `git/project-gov/` (the governance repository, which becomes `<slug>-gov`).

This file is canonical. [`CLAUDE.md`](CLAUDE.md) imports it, and every other agent tool reads it directly. **Inside `git/project-gov/`, that folder's own [`AGENTS.md`](git/project-gov/AGENTS.md) applies too**: it is the rule set every new project inherits. Change the template there, and keep this file for the skeleton itself.

## Rules for the skeleton
1. **No client content, ever.** No names, data or documents from a real client. Examples are fictional and marked `SAMPLE`, and the bootstrap (`git/project-gov/tools/workspace/new_project.py`) drops them.
2. **Keep the two halves in step.** A folder added to `shared/` gets a README and a row in `git/project-gov/WORKSPACE.md`. A tool added to `git/project-gov/tools/` gets a test and a row in that folder's README.
3. **Tests pass before you hand over:** `cd git/project-gov && py -3.12 -m unittest discover -s tests`.
4. **Commit only when asked, and never push unless asked.** Group commits with the `dev-group-and-commit` skill.

## Code intelligence: read the code through its graphs
This repository keeps two snapshots of its code, so an agent can answer from a graph instead of reading everything again every session. Most of the repository is Markdown, and the graphs cover its Python: the tools, the PRD sync and the bootstrap. For the documents, start from the map, [`git/project-gov/WORKSPACE.md`](git/project-gov/WORKSPACE.md).

| Graph | Where | Ask it |
|---|---|---|
| **Graphify** | `graphify-out/` at the root: `GRAPH_REPORT.md` (communities, god nodes, surprising links), `graph.json`, `graph.html` | The shape of the code: `graphify query "<question>"`, `graphify path "<A>" "<B>"`, `graphify explain "<concept>"` (or `py -3.12 -m graphify …` when `graphify` is not on the PATH) |
| **GitNexus** | `.gitnexus/` at the root, indexed as `gov-as-code` and served by the GitNexus MCP server. Tools: `query`, `context`, `impact`, `detect_changes`, `rename`, `cypher`. Resources: `gitnexus://repo/gov-as-code/context`, `…/clusters`, `…/processes`, `…/process/{name}`. Skills: `.claude/skills/gitnexus/`, when an analyze has installed them | The specifics: a symbol's callers and callees, execution flows, the blast radius of a change |

1. **Graph first.** Before exploring code, use whichever graph exists. Read `graphify-out/GRAPH_REPORT.md` for the shape, then ask GitNexus (`query`, `context`) or Graphify (`query`, `path`) for the part you need. Open source files only to confirm what a graph points to. Never scan the whole repository for a question that a graph can answer.
2. **Check freshness, then refresh if needed.** From the root, `py -3.12 git/project-gov/tools/repos/scan.py --check .` reports each graph as fresh, stale or missing. `py -3.12 git/project-gov/tools/repos/scan.py .` refreshes both. It is cheap: Graphify's AST pass uses no language model, and GitNexus indexes without injecting files. Run it after you change code. If you cannot refresh, say that your answer comes from the last scan's snapshot.
3. **Before you edit a function, class or method,** run GitNexus `impact` on it (upstream) and report the blast radius. Warn the user before going ahead on a HIGH or CRITICAL risk. Rename with `rename`, never with find-and-replace. Before you commit, run `detect_changes` to confirm that only the expected symbols and flows moved.
4. **No graph, no problem.** If neither tool is installed (`pip install graphifyy`, `npm i -g gitnexus`) or no graph exists yet, read the code directly, and say that a scan would make the next session faster.
5. **A graph is a snapshot, not the truth.** The code is the witness. Graph outputs are never committed: `graphify-out/`, `.gitnexus/` and `.claude/` are gitignored.
6. **Documents are opt-in.** The scan graphs code only. The full `/graphify .` skill can add the Markdown (most of this repository) to the graph, but it uses the language model and costs tokens: run it when the user asks.
7. **No tool writes into this file or `CLAUDE.md`.** `.gitnexusrc` sets `skipAgentsMd`, so `gitnexus analyze` leaves them alone. Don't run `graphify claude install` or `graphify codex install`: this section already covers what they would add.
