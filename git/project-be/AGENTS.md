# project-be: Hello World's API

One endpoint on Python's standard library: `GET /api/hello`.

## Run
```
py -3.12 -m pip install -r requirements.txt   # once: psycopg
copy .env.example .env                        # the password is project-db's API_DB_PASSWORD
py -3.12 -m hello                             # http://127.0.0.1:47102/api/hello
py -3.12 -m unittest discover -s tests        # the tests, no database needed
```
On macOS and Linux, use `python3` for `py -3.12` and `cp` for `copy`.

## The contract (ADR-006)
| Request | Answer |
|---|---|
| `GET /api/hello` | `200 {"message": "<the greeting>"}` |
| `GET /api/hello`, database down | `503 {"error": "database unavailable"}` |
| Anything else | `404` |

CORS: only `ALLOWED_ORIGIN` (the web app) gets `Access-Control-Allow-Origin`.

## Governance
Governed by `project-gov` (cloned beside this repository, in `../project-gov`), at commit `97fa3f6` on `ciklum-devtalks-2026`.
ADRs this repository keeps:
- ADR-004: one job per repository, two contracts, a dependency budget, port 47102.
- ADR-006: one endpoint, the standard library plus `psycopg` only, one CORS origin, configuration from the environment, read-only.
