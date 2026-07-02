# ADR-002 — SAMPLE: Identity comes only from the organisation's single sign-on

> **Status:** DRAFT · **Date:** 2026-01-14 · **Decided by:** solution architect · **Supersedes:** — · **Superseded-by:** —
> **Requirements:** FR-001, NFR-002, OI-001 · **Backlog:** adr-002 · **Governs:** project-be, project-fe
> Deviations from this ADR are tracked in the [deviation register](../deviations/README.md), never here.

> SAMPLE. This ADR belongs to the fictional sample PRD. It exists so that `prd/sync/impact.py` has a decision to find when FR-001 changes. A new project drops it.

## 1. Context
The PRD asks that users sign in with the organisation's single sign-on and that the app keep no passwords of its own (FR-001). It also asks that every sign-in and every decision be written to an audit log (NFR-002). Which identity provider the organisation uses is still open (OI-001, `q1`). We assume it speaks OpenID Connect (`a1`).

## 2. Options
| Option | For | Against |
|---|---|---|
| **OpenID Connect against the organisation's identity provider** | No passwords to hold; the organisation's own policies (MFA, leavers) apply; standard libraries | Depends on the provider's group claims for roles (`q1`) |
| Local accounts with passwords | No dependency on the client's IT | Breaks FR-001; we would hold credentials and run resets |
| SAML | Widely supported by older providers | Heavier to integrate and test than OIDC; only worth it if the provider lacks OIDC |

## 3. Decision: the laws
1. **No credential store.** The app holds no passwords or password hashes. Identity is an OIDC token from the organisation's provider. Enforced by the schema, which has no credential columns, and a CI check that fails on any.
2. **Roles come from the provider.** Requester, approver and administrator are mapped from the provider's groups, never assigned in the app's own database.
3. **Every sign-in is an audit event.** Sign-ins and decisions are written to the audit log with who, when and what (NFR-002). The log is append-only for the app.

## 4. Acceptance criteria (timeless)
1. A request without a valid token reaches no page and no API (a test per entry point).
2. The schema check finds no credential columns.
3. Each sign-in and each decision produces exactly one audit event (an end-to-end scenario).

## 5. Consequences
- The organisation's joiner and leaver process controls access, at no cost to us.
- Local development needs a stub identity provider (a test double that issues tokens).
- If the provider has no OIDC (`q1` answered "SAML only"), this ADR is superseded, not edited.

## 6. References
- PRD v0.1: FR-001, NFR-002, OI-001.
- [`questions.md`](../questions.md): `q1`, `a1`.
