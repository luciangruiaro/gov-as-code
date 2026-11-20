# ADR-004 — SAMPLE: Hello World is three small repositories beside the governance repository

> **Status:** DRAFT · **Date:** 2026-11-20 · **Decided by:** solution architect · **Supersedes:** — · **Superseded-by:** —
> **Requirements:** NFR-006, SM-002, GR-002, OI-003 · **Backlog:** adr-004 · **Governs:** project-db, project-be, project-fe
> Deviations from this ADR are tracked in the [deviation register](../deviations/README.md), never here.

> SAMPLE. Hello World is Release 0 of the fictional sample PRD: the smallest slice that proves the stack. A new project drops this ADR.

## 1. Context
Release 0 of the PRD is Hello World: one page that shows a greeting read from a database through an API. It proves that the three parts of the stack work together before the request workflow is built. It must stay as lightweight as possible, and each part must start with one command (NFR-006). Every developer runs it end to end (SM-002). It holds no personal or customer data (GR-002).

Hello World runs on developer machines only. Whether it ever runs anywhere else, and whether it then needs sign-in first, is still open (OI-003, `q2`). We assume it stays local (`a2`).

The workspace already expects product repositories cloned beside this one, in `git/` ([`WORKSPACE.md`](../../WORKSPACE.md) section 4). Hello World is the first time that model meets real code.

## 2. Options
| Option | For | Against |
|---|---|---|
| One repository with three folders | Simplest to clone and run; one pull request covers a change across the stack | Doesn't exercise the multi-repository model the workspace is built for; one repository ends up holding every decision |
| Two repositories: the database inside the API | One fewer repository | Couples the schema to the service; the web app's contract and the database's contract live in the same place |
| **Three repositories, one job each** | Matches `WORKSPACE.md`; each repository keeps only the ADRs that bind it; contracts are explicit at each boundary | Three clones, and a change that crosses a boundary needs two pull requests |

## 3. Decision: the laws
1. **One job per repository.** `project-db` owns the schema, `project-be` owns the REST API, `project-fe` owns the UI. All three are cloned in `git/`, beside `project-gov`. Code that belongs to one job never lives in another repository.
2. **Two contracts, nothing else.** The parts meet only at the SQL schema (database to API, [ADR-005](ADR-005-sample-hello-world-postgres.md)) and at one HTTP endpoint (API to web app, [ADR-006](ADR-006-sample-hello-world-python-api.md)). The web app never talks to the database.
3. **A lightweight budget.** Each repository starts with one command and carries only the runtime dependencies its ADR names ([ADR-005](ADR-005-sample-hello-world-postgres.md), [ADR-006](ADR-006-sample-hello-world-python-api.md), [ADR-007](ADR-007-sample-hello-world-react-web.md)). Each repository's CI fails when a dependency appears that its ADR does not name.
4. **Each repository is governed from here.** Its agent file (`AGENTS.md` or `CLAUDE.md`) has a `## Governance` block that links to this repository, names the commit it follows and lists the ADRs it keeps.
5. **Local ports come from the project's block.** The web app listens on 47101, the API on 47102 and Postgres on 47103 ([`operations/README.md`](../../operations/README.md), "Ports"), so Hello World never collides with another project on the same machine.
6. **Local only until OI-003 is answered.** Hello World runs on developer machines and holds no personal or customer data (GR-002). Deploying it anywhere else needs the answer to OI-003 and, if sign-in is required, a new ADR (`a2`).

## 4. Acceptance criteria (timeless)
1. A smoke check starts the three parts from fresh clones, each with its one command, and the page shows the greeting from the database (SM-002).
2. Each repository's CI checks its runtime dependencies against the list in its ADR.
3. Each repository's agent file has a `## Governance` block that lists this ADR.
4. The web app's source contains no database connection string or driver.

## 5. Consequences
- Easier: each repository is small enough to read in one sitting, and an architecture review of one part checks only the ADRs that part keeps.
- Harder: a change that crosses a boundary (a new field in the greeting) needs coordinated pull requests in two repositories.
- Accepted: three clones for a one-page app. The overhead is the point: Release 0 proves the workspace as much as the stack.

## 6. References
- PRD v0.2: NFR-006, SM-002, GR-002, OI-003 (Release 0, Hello World).
- [`questions.md`](../questions.md): `q2`, `a2`.
- [ADR-005](ADR-005-sample-hello-world-postgres.md) (database), [ADR-006](ADR-006-sample-hello-world-python-api.md) (API), [ADR-007](ADR-007-sample-hello-world-react-web.md) (web app).
