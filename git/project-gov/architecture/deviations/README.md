# Deviation register

Where the as-built system departs from a **ratified** ADR. This register keeps the ADRs honest without weakening them: the ADR keeps the vision, and this page keeps the debt, with an exit condition for each row.

This folder sits beside `decisions/`: the decisions say what the system must be, the deviations say where it is not yet. The register below is the index. A deviation that needs more than a row (evidence, options, a remediation plan) gets its own file here, `DEV-0NN-kebab-slug.md`, linked from its row.

**Rules**
- A row is added the same day the deviation is found or knowingly introduced. A mid-sprint workaround is allowed if it is logged here.
- The `dev-architecture-review` skill **proposes** rows; the design authority (solution architect) appends them.
- A row is removed only with a link to the merge that closed it, in the commit message.
- Evidence is mainline code (`repo:path:line`), not a ticket: tickets and docs are claims; code is the witness.

**Severity:** `CRITICAL` (data protection, safety) · `HIGH` · `MEDIUM` · `LOW`.
**Disposition:** `remediate-now` · `refactor-planned` (cite the plan) · `accepted-until <condition>` · `tracked`.

| ID | ADR § | As-built deviation | Evidence (mainline code) | Severity | Disposition |
|---|---|---|---|---|---|
| — | — | No deviations recorded yet. | — | — | — |

<!-- Example row:
| DEV-001 | ADR-002 §3.2 | Roles are assigned in the app's admin screen while the provider's groups are not ready | project-be:src/auth/roles.py:41 | MEDIUM | accepted-until q1 answered |
-->
