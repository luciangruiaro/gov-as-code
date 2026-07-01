# Jira (the backlog mirror)

**Holds:** a **one-way mirror** of the backlog, one Markdown file per ticket, so people and agents can read the backlog without querying it each time. The system is Jira or Azure DevOps (`workspace.toml` `[backlog] system`); the folder keeps the name `Jira` either way.

| Path | What |
|---|---|
| [`index.md`](index.md) | Every ticket by group: current sprint (board rank), backlog (rank), done (newest first) |
| `current-sprint/<KEY-n>.md` | Tickets in the active sprint |
| `backlog/<KEY-n>.md` | Tickets not in a sprint and not done |
| `done/<KEY-n>.md` | Done or removed tickets |
| `_STATUS.md` | The last pulls: when, by whom (role), what changed (written by the tool) |

A ticket file opens with `# KEY-n: summary` and a Field/Value table (type, status, sprint, assignee role, points, epic, labels, parent, updated, link). Then come `## Description`, `## Acceptance criteria` and `## Comments`.

**Written by:** `tools/mirrors/backlog.py` only (the `gov-backlog-sync` skill), on a schedule. It writes a file only when its content changed, so the drive's modified dates show what moved, and it removes files of tickets that left the project. **Read by:** the team, agents planning or verifying work, the daily digest.

**Rules:**
- Never edit these files: change the ticket, and the next pull rewrites it.
- Text only: no attachments (screenshots are where data leaks).
- One pull at a time: check `_STATUS.md` before running one by hand.
- Tickets are claims; mainline code is the witness. "Done" here is checked against the code by `dev-spec-verify`.
