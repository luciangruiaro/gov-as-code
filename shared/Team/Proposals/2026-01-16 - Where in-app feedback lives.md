# Proposal: Where in-app feedback lives

| | |
|---|---|
| **Status** | approved |
| **Proposed by** | <name> (solution architect) |
| **Date** | 2026-01-16 |
| **Decision by** | delivery lead and client product owner, before 2026-01-23 |
| **Requirements** | FR-004 |

> SAMPLE. A fictional proposal in the expected shape. A new project drops it.

## The question
FR-004 puts a feedback button on every screen. Where are the items stored, and how does the team see them?

## Context
The team reads the shared drive every day. The app already has a database. A third-party feedback tool would need a contract of its own.

## Options
| Option | Pros | Cons | Cost and risk |
|---|---|---|---|
| A table in the app's own database, mirrored to `Feedback/` on the shared drive | Data stays in the client's environment; triage in the app; everyone sees items on the drive | A pull tool to build and schedule | Low |
| A third-party feedback tool | Ready-made triage | Data leaves the environment; another contract | Medium |
| Email to a shared inbox | Nothing to build | No context (page, build); lost in inboxes | Low cost, high loss |

## Recommendation
Option A: it keeps the data in the client's environment and gives the team one place to look.

## Comments
- 2026-01-17, <name> (delivery lead): agreed; schedule the pull hourly in working hours.

## Outcome
Decided on 2026-01-19 by the delivery lead with the client product owner: option A. Promoted to: ADR backlog entry `adr-003` (`architecture/decisions/backlog.md`).
