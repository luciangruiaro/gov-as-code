# Investigation: the upload limit is ignored on the test environment

> SAMPLE. A fictional investigation in the shape `dev-debug` writes. A new project drops it.
> **Date:** 2026-01-15 · **Touches:** CFG-001, FR-002 · **Status:** cause supported, fix planned

## Symptom
On the test environment, a 25 MB attachment is accepted, though CFG-001 is 10 MB.

## Hypotheses
| # | Hypothesis | Evidence | Verdict |
|---|---|---|---|
| H1 | The limit is read from the wrong configuration key | The key in `config/defaults.toml` is `upload_max_mb`; the code reads `upload_limit_mb` | **Supported** |
| H2 | The reverse proxy allows larger bodies and the app never sees the size | The proxy limit is 50 MB, but the app does receive the full body | Not the cause (an adjacent risk) |
| H3 | The limit is checked per file, not per request | True, but a single 25 MB file should still fail | Not the cause |

## Cause
H1: a key mismatch, so the check falls back to "no limit".

## Fix plan
Read `upload_max_mb`, fail closed when the key is missing, and add a test that changes the limit through configuration (phase 1 of the request-submission plan).

## Adjacent risks
- H3: FR-002 says "up to 10 MB in total", so the check must sum the request's attachments.
- H2: set the proxy limit just above CFG-001's maximum.
