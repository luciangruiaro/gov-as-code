# Product Requirements Document (Master) - Project Name

> Mirror of the master PRD, which is kept in Word on the shared drive (`PRD/`). Change the Word document, then sync with [`sync/SYNC.md`](sync/SYNC.md); never edit this file by hand. Last change: 2026-11-20 (v0.2), in the [change log](#change-log) at the end.

> **Owner:** client product owner · **Drafted by:** delivery lead · **Status:** draft · **Version:** v0.2
>
> SAMPLE. A fictional request-approval portal, here to show the PRD sync and the decision review end to end. Version 0.2 adds Release 0, Hello World: the smallest slice that proves the stack. Replace it with the real master PRD.

## 1. The product in brief

| Area | In brief |
|----|----|
| Problem | Requests are sent by email and approvals get lost; nobody can say what was decided, by whom or when. |
| Users | Requesters, approvers and an administrator. |
| Scope | Submitting, approving and tracking requests in a web app. Payments and procurement are out of scope. |
| Success | Most requests are decided within two working days (SM-001). |
| Release 0: Hello World | One page that shows a greeting read from the database through the API. It proves that the database, the API and the web app work together, before the request workflow is built. It runs on developer machines only (OI-003). |

## 2. Users and roles

| Role | What they do with the product | How many |
|----|----|----|
| Requester | Submits a request and follows it to a decision. | About 300 |
| Approver | Approves or rejects requests in their area. | About 25 |
| Administrator | Manages areas, approvers and configuration. | 2 |
| Team member | Opens the Hello World page to check that the stack works end to end. | The delivery team |

## 3. Functional requirements (FR)

| Id | Requirement | Done when |
|----|----|----|
| FR-001 | Users sign in with the organisation’s single sign-on; the app keeps no passwords of its own. | A user without an organisation account cannot reach any page. |
| FR-002 | A requester submits a request with a title, a description and attachments of up to 10 MB in total. | The request appears in the approver’s queue within a minute. |
| FR-003 | An approver approves or rejects each request with a reason; nothing proceeds without a decision. | Every decided request shows who decided, when and why. |
| FR-004 | Every screen has a feedback button that sends the message with the page, the app version and the user’s role. | Feedback appears in the team’s feedback mirror within an hour. |
| FR-006 | Hello World: the home page shows a greeting that is stored in the database and served by the API. | Changing the greeting in the database changes the page on the next load, with no deploy. |
| FR-007 | Hello World: when the greeting cannot be loaded, the page says so in plain words and offers to try again. | With the database stopped, the page shows the error state, never a blank screen. |

## 4. Non-functional requirements (NFR)

| Id | Requirement | Target |
|----|----|----|
| NFR-001 | Pages load quickly on the office network. | Under 2 seconds at the 95th percentile. |
| NFR-002 | Every sign-in and every decision is written to an audit log. | Kept for 12 months; readable by the administrator only. |
| NFR-003 | The app meets the accessibility standard the client uses. | WCAG 2.2 AA on every screen. |
| NFR-005 | Hello World follows the project’s UI kit (the Prodigy Design System), in light and dark themes. | Every colour, font and radius comes from the kit’s tokens. |
| NFR-006 | Hello World stays as lightweight as possible: each part (database, API, web app) has only the dependencies it needs and starts with one command. | From a fresh clone to the greeting page in under 10 minutes. |

## 5. Guardrails (GR)

| Id | Rule the product must never break | Why |
|----|----|----|
| GR-001 | The app never stores payment card data. | Out of scope, and it would bring compliance obligations. |
| GR-002 | Hello World holds no personal or customer data. | It runs before sign-in (FR-001) exists, so it must have nothing to protect. |

## 6. Configuration (CFG)

| Id | Parameter | Default | Who sets it (role) |
|----|----|----|----|
| CFG-001 | Maximum attachment size per request | 10 MB | Administrator |
| CFG-002 | The Hello World greeting | Hello, World! | Delivery lead |

## 7. Success measures (SM)

| Id | Measure | Target | How it is measured |
|----|----|----|----|
| SM-001 | Requests decided within two working days | 80% | Decision time from the audit log, weekly |
| SM-002 | Hello World runs end to end on every developer’s machine | The whole delivery team | A smoke check that each developer runs once |

## 8. Open items (OI)

| Id | Question | Owner (role) | Needed by |
|----|----|----|----|
| OI-001 | Which identity provider does the organisation use for single sign-on? | Client IT lead | Before the first sprint |
| OI-002 | How long are attachments kept after a decision? | Client product owner | Before go-live |
| OI-003 | Does Hello World ever run outside developer machines, and does it then need sign-in (FR-001) first? | Client product owner | Before Hello World is deployed anywhere |

## 9. Traceability

| Requirement | Decisions (ADR)           | Tests                   | Old id |
|-------------|---------------------------|-------------------------|--------|
| FR-001      | ADR-002                   | sign-in scenarios       | —      |
| NFR-002     | ADR-002                   | audit scenarios         | —      |
| FR-006      | ADR-005, ADR-006, ADR-007 | greeting scenario       | —      |
| FR-007      | ADR-006, ADR-007          | database-down scenario  | —      |
| NFR-005     | ADR-007                   | token check             | —      |
| NFR-006     | ADR-004                   | dependency budget check | —      |

## 10. Versions

| Version | Date       | Change                      | Agreed by (role) |
|---------|------------|-----------------------------|------------------|
| v0.1    | 2026-01-12 | First draft                 | —                |
| v0.2    | 2026-11-20 | Adds Release 0, Hello World | —                |

## Change log

<!-- change log, newest first: rows are added by prd/sync/sync.py (see sync/SYNC.md) -->

| Date | Version | What changed |
|---|---|---|
| 2026-11-20 | v0.2 | Release 0, Hello World (SAMPLE): FR-006, FR-007, NFR-005, NFR-006, GR-002, CFG-002, SM-002, OI-003 added |
| 2026-01-12 | v0.1 | First mirror in Git (SAMPLE): 4 functional requirements, 3 non-functional, 1 guardrail, 1 parameter, 1 measure, 2 open items. |

<!-- /change log -->
