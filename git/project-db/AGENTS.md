# project-db: Hello World's database

The schema of Hello World: Postgres from the official image, and plain SQL migrations.

## Run
```
copy .env.example .env      # then choose local passwords
docker compose up -d        # Postgres on localhost:47103, schema applied on first start
```
Start again from an empty database: `docker compose down -v`, then `up -d`.

## Rules
- Migrations are numbered (`NNN_slug.sql`, or `.sh` when a secret is needed) and never edited after merge: a change is a new file.
- One table, `greeting`. No personal or customer data, ever.
- Secrets live only in `.env`.

## Governance
Governed by `project-gov` (cloned beside this repository, in `../project-gov`), at commit `97fa3f6` on `ciklum-devtalks-2026`.
ADRs this repository keeps:
- ADR-004: one job per repository, two contracts, a dependency budget, port 47103.
- ADR-005: the official `postgres` image, append-only SQL, a read-only role for the API, credentials in `.env`.
