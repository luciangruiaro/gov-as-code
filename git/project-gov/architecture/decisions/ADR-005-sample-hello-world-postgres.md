# ADR-005 — SAMPLE: Postgres holds the greeting, and the schema is plain SQL

> **Status:** DRAFT · **Date:** 2026-11-20 · **Decided by:** solution architect · **Supersedes:** — · **Superseded-by:** —
> **Requirements:** FR-006, CFG-002, GR-002, NFR-006 · **Backlog:** adr-005 · **Governs:** project-db
> Deviations from this ADR are tracked in the [deviation register](../deviations/README.md), never here.

> SAMPLE. Part of Hello World, Release 0 of the fictional sample PRD. A new project drops this ADR.

## 1. Context
Hello World shows a greeting that is stored in the database, so that changing it changes the page with no deploy (FR-006). The greeting's default is "Hello, World!" (CFG-002). The database holds nothing else, and never holds personal or customer data (GR-002). Like every part of Hello World, it must be as lightweight as possible and start with one command (NFR-006).

[ADR-004](ADR-004-sample-hello-world-three-repositories.md) gives the schema its own repository, `project-db`, and makes the schema the only contract between the database and the API.

## 2. Options
| Option | For | Against |
|---|---|---|
| **The official `postgres` image, with numbered plain SQL files** | Nothing to install beyond a container runtime; SQL is readable by anyone; no tool owns the schema | No automatic rollback; migrations are written by hand |
| Migrations owned by the API (an ORM, Alembic) | Schema and code change in one pull request | Adds dependencies to the API; puts the schema inside `project-be`, against ADR-004 law 1 |
| SQLite | Lighter still: a file, no server | Not the database the product will run on; proves less about the stack |

## 3. Decision: the laws
1. **The official image, pinned.** Postgres runs from the official `postgres` image, pinned to one major version. `project-db` holds a `compose.yaml` that starts it on port 47103 and applies the schema: that is its one start command.
2. **The schema is plain SQL, append-only.** Migrations are numbered files (`NNN_slug.sql`), applied in order to an empty database. A merged migration is never edited: a change is a new file.
3. **One table.** `greeting (id, message)` holds one row, seeded with the CFG-002 default. There are no other tables, and no column holds personal or customer data (GR-002).
4. **The API reads, nothing more.** The API connects as its own role, which can only `SELECT` from `greeting`. Changing the greeting is a person's job, done with the owner role.
5. **Credentials live in `.env`.** Passwords and connection strings are read from the environment, filled from a gitignored `.env`. The repository commits only `.env.example`, with placeholders.

## 4. Acceptance criteria (timeless)
1. CI applies every migration, in order, to an empty database, and the seed row reads "Hello, World!".
2. A write to `greeting` as the API's role fails.
3. A secret scan of the repository finds no credentials.
4. A migration file that changes after it is merged fails CI.

## 5. Consequences
- Easier: the schema is readable without tools, and the database starts with one command on any machine with a container runtime.
- Harder: migrations are hand-written, and there is no automatic down-migration.
- Accepted: a container runtime is the one prerequisite for running Hello World end to end.

## 6. References
- PRD v0.2: FR-006, CFG-002, GR-002, NFR-006.
- [ADR-004](ADR-004-sample-hello-world-three-repositories.md) (the three repositories and their ports), [ADR-006](ADR-006-sample-hello-world-python-api.md) (the API that reads the greeting).
