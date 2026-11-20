# ADR-006 — SAMPLE: The API is one Python endpoint on the standard library

> **Status:** DRAFT · **Date:** 2026-11-20 · **Decided by:** solution architect · **Supersedes:** — · **Superseded-by:** —
> **Requirements:** FR-006, FR-007, NFR-006 · **Backlog:** adr-006 · **Governs:** project-be
> Deviations from this ADR are tracked in the [deviation register](../deviations/README.md), never here.

> SAMPLE. Part of Hello World, Release 0 of the fictional sample PRD. A new project drops this ADR.

## 1. Context
The web app shows the greeting that the API reads from the database (FR-006). When the database cannot be reached, the web app must be able to say so instead of showing a blank page (FR-007), so the API has to tell that case apart. The API must be as lightweight as possible and start with one command (NFR-006).

[ADR-004](ADR-004-sample-hello-world-three-repositories.md) makes one HTTP endpoint the only contract between the API and the web app, and [ADR-005](ADR-005-sample-hello-world-postgres.md) gives the API a read-only role on one table.

## 2. Options
| Option | For | Against |
|---|---|---|
| **Python's standard library (`http.server`), plus `psycopg`** | One runtime dependency; nothing to learn beyond Python | No routing, validation or OpenAPI for free; fine for one endpoint, not for fifty |
| Flask | Small and familiar; routing built in | A handful of transitive dependencies for one route |
| FastAPI | Validation and an OpenAPI document for free | FastAPI, Starlette, Pydantic and Uvicorn: the heaviest option for one endpoint |

## 3. Decision: the laws
1. **One endpoint, one contract.** `GET /api/hello` answers `200` with `{"message": "<the greeting>"}`. When the database cannot be reached it answers `503` with `{"error": "database unavailable"}`. Any other path answers `404`. This ADR is where the contract is written down. Changing it needs a new ADR, and the web app changes with it.
2. **Standard library, one dependency.** The API runs on Python 3.12 or newer, on `http.server`. Its only runtime dependency is `psycopg`. Its one start command is `py -3.12 -m hello`, which listens on port 47102 (ADR-004 law 5).
3. **Only the web app may call it.** CORS allows exactly one origin, the web app's, read from configuration. No other origin gets the `Access-Control-Allow-Origin` header.
4. **Configuration from the environment.** `DATABASE_URL`, `PORT` and `ALLOWED_ORIGIN` come from environment variables (a gitignored `.env` for local runs). Nothing environment-specific is in the code.
5. **Read-only, stateless.** The API keeps no state between requests and only reads `greeting` with the role from ADR-005 law 4.

## 4. Acceptance criteria (timeless)
1. Unit tests: `200` with the message from a test database; `503` with the database down; `404` for any other path.
2. A test asserts that the allowed origin gets the CORS header and another origin doesn't.
3. CI fails when the runtime dependencies are anything other than `psycopg`.

## 5. Consequences
- Easier: the whole API fits in one file that anyone can read, and it installs in seconds.
- Harder: every HTTP concern (routing, headers, errors) is written by hand. That is cheap for one endpoint and grows with each new one.
- Accepted: when the API needs a second resource, a new ADR weighs Flask or FastAPI again and supersedes this one.

## 6. References
- PRD v0.2: FR-006, FR-007, NFR-006.
- [ADR-004](ADR-004-sample-hello-world-three-repositories.md) (the contracts and the port), [ADR-005](ADR-005-sample-hello-world-postgres.md) (the read-only role), [ADR-007](ADR-007-sample-hello-world-react-web.md) (the caller).
