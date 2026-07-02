# Plans

Written by `dev-plan`, and by `dev-map` for programs that span several plans or repositories.

| Shape | Path |
|---|---|
| A roadmap | `<YYYY-MM>/<slug>/<slug>.md`: goal, locked decisions, phases, risks |
| Its status | `<YYYY-MM>/<slug>/STATUS.md`: opens with `# Status: <emoji> <state>`, then one row per phase |
| A phase, ready to ship in one session | `<YYYY-MM>/<slug>/phases/phase-N-<slug>.md`: scope, files, tests, docs to refresh |
| A program map | `<program>/MAP.md`: destination, decision ledger, frontier, fog |

**Rules**
- The month is when the plan was created. Plans never move, and month folders are never renamed.
- Every plan cites the PRD ids and the ADRs it implements. `dev-spec-verify` checks the code against it, claim by claim.
- Tests and documentation are deliverables in every phase, not afterthoughts.
