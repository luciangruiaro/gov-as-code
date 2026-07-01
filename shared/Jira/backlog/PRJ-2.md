# PRJ-2: Sign in with the organisation's single sign-on

| Field | Value |
|---|---|
| Type | Story |
| Status | To Do |
| Sprint | — |
| Assignee | — |
| Points | 8 |
| Epic | PRJ-11 Access |
| Labels | FR-001, ADR-002 |
| Parent | — |
| Updated | 2026-01-14 11:20 |
| Link | https://example.atlassian.net/browse/PRJ-2 |

> SAMPLE. A fictional ticket. A new project drops it.

## Description
As a user, I sign in with my organisation account; the app keeps no passwords (FR-001, ADR-002). Blocked on the identity provider (OI-001, `q1`).

## Acceptance criteria
- Without a valid token, no page and no API answers.
- Each sign-in writes one audit event (NFR-002).

## Comments
_None._

_Mirrored from Jira. Do not edit: run the gov-backlog-sync skill to refresh._
