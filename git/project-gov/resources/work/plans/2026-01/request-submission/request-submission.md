# Plan: request submission

> SAMPLE. A fictional roadmap in the shape `dev-plan` writes. A new project drops it.
> **Date:** 2026-01-13 · **Implements:** FR-002, CFG-001 · **Respects:** ADR-002 (requests need a signed-in user) · **Ticket:** PRJ-1

## Goal
A requester submits a request with a title, a description and attachments of up to the configured limit (CFG-001, 10 MB by default), and it reaches the approver's queue within a minute (FR-002).

## Locked decisions
| Decision | Why |
|---|---|
| The upload limit is read from configuration, never hard-coded | CFG-001 makes it the administrator's parameter |
| Attachments are stored outside the database, and the database keeps references | Size and backups |

## Phases
| Phase | Ships | File |
|---|---|---|
| 1 | The API: create a request, upload attachments, enforce CFG-001 | [`phases/phase-1-api.md`](phases/phase-1-api.md) |
| 2 | The form in the frontend, with the feedback button (FR-004) | not yet refined |
| 3 | The approver's queue notification | not yet refined |

## Risks
- Retention of attachments is still open (OI-002): phase 1 keeps them indefinitely until it is answered.
