# PRD → decisions alignment, 2026-01-20

> SAMPLE. Produced by the "Try it on the sample" walkthrough in `prd/sync/SYNC.md` (v0.1 → v0.2), then answered, to show the shape of an answered worksheet. The repository's mirror stays at v0.1, and these answers are not landed in the sample ADRs. A new project drops this file.

> Started by `prd/sync/impact.py`, comparing `HEAD:prd/Product Requirements Document (Master) - Project Name v0.1.md` with the synced mirror `prd/Product Requirements Document (Master) - Project Name v0.2.md`.
> Fill in every **Answer**, then land the answers in the decisions with the `gov-adr` skill. Keep this file once answered: it is the record of why the decisions moved.

## Summary

| Id | Change | Cited by |
|---|---|---|
| FR-001 | changed | ADR-002, architecture/decisions/backlog.md, architecture/questions.md |
| FR-005 | added | — |
| OI-002 | removed | resources/work/plans/2026-01/request-submission/request-submission.md |

## Questions

### Q1. FR-001 changed

**Before:**

```text
| FR-001 | Users sign in with the organisation’s single sign-on; the app keeps no passwords of its own. | A user without an organisation account cannot reach any page. |
```

**After:**

```text
| FR-001 | Users sign in with the organisation’s single sign-on; external guests sign in with a one-time code sent by email. The app keeps no passwords of its own. | A user without an organisation account or a valid code cannot reach any page. |
```

**Cited by:**

- `architecture/decisions/ADR-002-sample-single-sign-on.md` (lines 4, 7, 10, 16, 35): > **Requirements:** FR-001, NFR-002, OI-001 · **Backlog:** adr-002 · **Governs:** project-be, project-fe
- `architecture/decisions/backlog.md` (line 8): | adr-002 | SAMPLE: How do users sign in, and where do roles come from? | FR-001, NFR-002, OI-001 | partial | solution architect | [ADR-002…
- `architecture/questions.md` (lines 8, 13): | q1 | SAMPLE: Which identity provider does the organisation use, and does it support OpenID Connect with group claims? | FR-001, OI-001 | …

**Decision needed:** Do the decisions that cite it still hold as written? For each: keep it, amend it (a law or an acceptance criterion), supersede it with a new ADR, or record a deviation.

**Options:**
- A. Amend ADR-002 (it is still `DRAFT`): a second identity path for external guests, using short-lived, single-use email codes. Law 1 ("no credential store") still holds, because a code is not a password.
- B. Supersede ADR-002 with a new ADR that covers both the organisation's users and guests.
- C. Push back on the PRD change.

**Recommendation:** A. The decision's shape does not change, only its scope, and a draft may be amended in place. Add a question: can guests approve, or only submit?

**Lands in:** ADR-002, architecture/decisions/backlog.md, architecture/questions.md

**Answer:** A. Amend ADR-002: add a law for guest one-time codes (expire in 15 minutes, single use, each use an audit event under NFR-002). Add `q2`: can guests approve, or only submit? Owner: client product owner. — solution architect, 2026-01-21

### Q2. FR-005 added

**After:**

```text
| FR-005 | An approver can hand a request over to another approver in the same area, with a note. | The new approver sees it in their queue with the note. |
```

**Decision needed:** A new requirement. Does it need a decision? If so, add an entry to `architecture/decisions/backlog.md`; if an existing ADR already covers it, cite the id there.

**Options:**
- A. No decision: it is a feature within approvals, so plan it directly.
- B. An ADR backlog entry: a hand-over changes who may decide, which touches the roles rule (ADR-002 law 2) and the audit trail (NFR-002).

**Recommendation:** B. Authorisation rules belong in a decision, not in a ticket.

**Lands in:** architecture/decisions/backlog.md

**Answer:** B. Add `adr-004`: "Who may hand a request over, to whom, and how is it audited?" (FR-005, NFR-002), status `open`. — solution architect, 2026-01-21

### Q3. OI-002 removed

**Before:**

```text
| OI-002 | How long are attachments kept after a decision? | Client product owner | Before go-live |
```

**Cited by:**

- `resources/work/plans/2026-01/request-submission/request-submission.md` (line 23): - Retention of attachments is still open (OI-002): phase 1 keeps them indefinitely until it is answered.

**Decision needed:** OI-002 left the PRD but is still cited. For each citation: drop it, point it at the requirement that replaced it (the PRD's traceability table keeps old ids), or mark the decision for review.

**Options:**
- A. The PRD's versions table says retention was "settled", but no requirement records the answer. Ask for it to be added as a requirement.
- B. Drop the risk from the plan.

**Recommendation:** A. An open item closed without a requirement is a decision that left no trace. The diff caught it; the PRD should carry it.

**Lands in:** resources/work/plans/2026-01/request-submission/request-submission.md

**Answer:** A. The client product owner adds the retention rule to the PRD as NFR-004 in v0.3. Until then, the plan's risk line points at this worksheet. — delivery lead, 2026-01-21
