# Product Requirements Document (Master) - Product name

> **Owner:** client (role) · **Drafted by:** delivery team (role) · **Status:** draft | agreed · **Version:** v0.1
>
> Keep this document in Word on the shared drive (`PRD/`), named `Product Requirements Document (Master) - <Product> vN.N.docx`. Git keeps a Markdown mirror of it: change the Word document, never the mirror.

How to write it so the mirror diffs well:

- Every requirement has a **stable id** and sits on **one table row**. A changed requirement is then one changed line in `git diff`, and `prd/sync/impact.py` can find every decision that cites it.
- Ids are never reused. When you renumber, keep the old id in the traceability table (section 9), so citations can still be followed.
- Name roles, not people. Cite contract sections; never paste contract text.

## 1. The product in brief

| Area | In brief |
|----|----|
| Problem | What hurts today, in the client's words. |
| Users | Who uses it (roles). |
| Scope | What is in; what is explicitly out. |
| Success | The one or two measures that say it worked (section 7). |

## 2. Users and roles

| Role | What they do with the product | How many |
|----|----|----|
| Role A | | |

## 3. Functional requirements (FR)

| Id | Requirement | Done when |
|----|----|----|
| FR-001 | One behaviour, in one sentence. | An observable check: this becomes an acceptance test. |

## 4. Non-functional requirements (NFR)

| Id | Requirement | Target |
|----|----|----|
| NFR-001 | Performance, availability, security, privacy, accessibility... | A number or a check. |

## 5. Guardrails (GR)

| Id | Rule the product must never break | Why |
|----|----|----|
| GR-001 | | |

## 6. Configuration (CFG)

| Id | Parameter | Default | Who sets it (role) |
|----|----|----|----|
| CFG-001 | | | |

## 7. Success measures (SM)

| Id | Measure | Target | How it is measured |
|----|----|----|----|
| SM-001 | | | |

## 8. Open items (OI)

| Id | Question | Owner (role) | Needed by |
|----|----|----|----|
| OI-001 | | | |

## 9. Traceability

| Requirement | Decisions (ADR) | Tests | Old id |
|----|----|----|----|
| FR-001 | ADR-0NN | scenario name | — |

## 10. Versions

| Version | Date | Change | Agreed by (role) |
|----|----|----|----|
| v0.1 | YYYY-MM-DD | First draft | |
