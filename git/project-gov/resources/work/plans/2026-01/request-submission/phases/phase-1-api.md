# Phase 1: the request API

> SAMPLE. A fictional phase plan. A new project drops it.
> **Parent:** [request-submission](../request-submission.md) · **Implements:** FR-002, CFG-001

## Scope
- `POST /requests` creates a request (title, description) for the signed-in user (ADR-002).
- `POST /requests/{id}/attachments` uploads a file, refusing any upload that would take the request past CFG-001.

## Files (in project-be)
- `src/requests/api.py`, `src/requests/storage.py`, `config/defaults.toml` (CFG-001's default).

## Tests
- Upload just under, at and over the limit; the limit changed in configuration takes effect without a deploy.
- An anonymous call is refused (ADR-002 §4.1).

## Docs to refresh
- The API reference in project-be; this plan's `STATUS.md`.
