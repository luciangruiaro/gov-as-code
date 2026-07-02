# ADR-0NN — Title in plain words

> **Status:** DRAFT · **Date:** YYYY-MM-DD · **Decided by:** role · **Supersedes:** — · **Superseded-by:** —
> **Requirements:** FR-0NN, NFR-0NN · **Backlog:** adr-0NN · **Governs:** repos or components
> Deviations from this ADR are tracked in the [deviation register](../deviations/README.md), never here.

## 1. Context
The problem and the forces at play, in two or three short paragraphs. Name the PRD requirements it rests on by id (`FR-0NN`), so `prd/sync/impact.py` finds this ADR when they change. Label anything not yet confirmed with a question or assumption id from [`questions.md`](../questions.md) (`q1`, `a1`).

## 2. Options
| Option | For | Against |
|---|---|---|
| A | | |
| B | | |

## 3. Decision: the laws
1. **The law, in bold.** One or two sentences that make it testable. Say how it is enforced structurally (a CI check, a schema, a credential boundary), not by instruction.
2. **The next law.**

## 4. Acceptance criteria (timeless)
1. A check that proves law 1 holds: a test, a probe, a CI rule.
2. A check for law 2.

## 5. Consequences
What gets easier, what gets harder, and what we accept.

## 6. References
- PRD: the requirement ids above, and the version they were read in.
- Related ADRs, alignment worksheets in `resources/audits/`, brainstorms.

<!--
Rules (architecture/decisions/README.md):
- An ADR is vision: it reads the same whether the system is 10% or 100% built. No sprints, no file:line evidence.
- Code that departs from a ratified ADR is a row in ../deviations/README.md, never an edit that weakens the ADR.
- To change a ratified decision, write a new ADR that supersedes it, and fill in both Supersedes lines.
-->
