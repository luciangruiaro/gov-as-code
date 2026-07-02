# Product Requirements Document (Master) - Project Name

> Mirror of the master PRD, which is kept in Word on the shared drive (`PRD/`). Change the Word document, then sync with [`sync/SYNC.md`](sync/SYNC.md); never edit this file by hand. Last change: 2026-01-12 (v0.1), in the [change log](#change-log) at the end.

> **Owner:** client product owner · **Drafted by:** delivery lead · **Status:** draft · **Version:** v0.1
>
> SAMPLE. A fictional request-approval portal, here to show the PRD sync and the decision review end to end. Replace it with the real master PRD.

## 1. The product in brief

| Area | In brief |
|----|----|
| Problem | Requests are sent by email and approvals get lost; nobody can say what was decided, by whom or when. |
| Users | Requesters, approvers and an administrator. |
| Scope | Submitting, approving and tracking requests in a web app. Payments and procurement are out of scope. |
| Success | Most requests are decided within two working days (SM-001). |

## 2. Users and roles

| Role          | What they do with the product                   | How many  |
|---------------|-------------------------------------------------|-----------|
| Requester     | Submits a request and follows it to a decision. | About 300 |
| Approver      | Approves or rejects requests in their area.     | About 25  |
| Administrator | Manages areas, approvers and configuration.     | 2         |

## 3. Functional requirements (FR)

| Id | Requirement | Done when |
|----|----|----|
| FR-001 | Users sign in with the organisation’s single sign-on; the app keeps no passwords of its own. | A user without an organisation account cannot reach any page. |
| FR-002 | A requester submits a request with a title, a description and attachments of up to 10 MB in total. | The request appears in the approver’s queue within a minute. |
| FR-003 | An approver approves or rejects each request with a reason; nothing proceeds without a decision. | Every decided request shows who decided, when and why. |
| FR-004 | Every screen has a feedback button that sends the message with the page, the app version and the user’s role. | Feedback appears in the team’s feedback mirror within an hour. |

## 4. Non-functional requirements (NFR)

| Id | Requirement | Target |
|----|----|----|
| NFR-001 | Pages load quickly on the office network. | Under 2 seconds at the 95th percentile. |
| NFR-002 | Every sign-in and every decision is written to an audit log. | Kept for 12 months; readable by the administrator only. |
| NFR-003 | The app meets the accessibility standard the client uses. | WCAG 2.2 AA on every screen. |

## 5. Guardrails (GR)

| Id | Rule the product must never break | Why |
|----|----|----|
| GR-001 | The app never stores payment card data. | Out of scope, and it would bring compliance obligations. |

## 6. Configuration (CFG)

| Id      | Parameter                           | Default | Who sets it (role) |
|---------|-------------------------------------|---------|--------------------|
| CFG-001 | Maximum attachment size per request | 10 MB   | Administrator      |

## 7. Success measures (SM)

| Id | Measure | Target | How it is measured |
|----|----|----|----|
| SM-001 | Requests decided within two working days | 80% | Decision time from the audit log, weekly |

## 8. Open items (OI)

| Id | Question | Owner (role) | Needed by |
|----|----|----|----|
| OI-001 | Which identity provider does the organisation use for single sign-on? | Client IT lead | Before the first sprint |
| OI-002 | How long are attachments kept after a decision? | Client product owner | Before go-live |

## 9. Traceability

| Requirement | Decisions (ADR) | Tests             | Old id |
|-------------|-----------------|-------------------|--------|
| FR-001      | ADR-002         | sign-in scenarios | —      |
| NFR-002     | ADR-002         | audit scenarios   | —      |

## 10. Versions

| Version | Date       | Change      | Agreed by (role) |
|---------|------------|-------------|------------------|
| v0.1    | 2026-01-12 | First draft | —                |

## Change log

<!-- change log, newest first: rows are added by prd/sync/sync.py (see sync/SYNC.md) -->

| Date | Version | What changed |
|---|---|---|
| 2026-01-12 | v0.1 | First mirror in Git (SAMPLE): 4 functional requirements, 3 non-functional, 1 guardrail, 1 parameter, 1 measure, 2 open items. |

<!-- /change log -->
