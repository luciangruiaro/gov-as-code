# Architecture overview: Project Name

> The architecture **as it is meant to be now**: current state only, no history (Git has that). Each claim either rests on a ratified ADR, or carries a question or assumption id from [`questions.md`](questions.md). Keep it short: details belong in the ADRs.

## 1. Context
What the system does, for whom, and what it talks to. One paragraph and a context diagram (the actors and the external systems).

| Actor or system | Relationship | Notes |
|---|---|---|
| Users (by role) | Use the app | PRD section 2 |
| External system | Data in / data out | Label unconfirmed with `q…` |

## 2. Building blocks
One row per product repository (the list is in `workspace.toml` and [`WORKSPACE.md`](../WORKSPACE.md) section 4).

| Repository | Owns | Talks to | ADRs it keeps |
|---|---|---|---|
| project-be | | | |
| project-fe | | | |
| project-data | | | |

## 3. Key flows
The few end-to-end flows that matter: who calls whom, what data moves, where it is stored.

## 4. Quality attributes
How the non-functional requirements are met, by id (`NFR-…`), with the ADR that decides each.

## 5. Risks and open questions
The architectural risks, and the `q…` ids they depend on.

## 6. Glossary
| Term | Meaning |
|---|---|
| | |
