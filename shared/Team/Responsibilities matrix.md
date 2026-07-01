# Responsibilities matrix

> What every role owns, decides and expects from the others, and what the others can expect from it. Agree it at kickoff and revisit it at each retrospective. Roles, not names: [`Team structure.md`](Team%20structure.md) maps them to people.

## Expectations by role
| Role | Owns | Decides | Expects from the others | The others can expect |
|---|---|---|---|---|
| Client product owner | The master PRD, priorities | Scope, acceptance | Clear options with trade-offs; demos on synthetic data | Answers to open items (`OI-…`) by the date they are needed |
| Delivery lead | Plan, risks, client communication | Sequencing, staffing | Honest status; blockers raised the same day | A current planner; blockers chased; the weekly report |
| Solution architect | ADRs, the architecture overview, the deviation register | Architecture (ratifies ADRs) | Proposals with pros and cons; deviations logged, not hidden | Decisions within a week of a complete proposal; reviews of risky changes |
| Engineers | Their repositories' code and tests | Implementation within the ADRs | Ratified decisions; small, clear tickets | Merge requests that cite the ticket and the ADRs; tests with every change |
| QA engineer | Test strategy, acceptance scenarios | Release readiness (with the delivery lead) | Acceptance criteria on every ticket | Scenarios per requirement id; a go or no-go with evidence |
| Coding agents | Nothing on their own | Nothing | Instructions in `AGENTS.md`; a person to review their work | Work within the rules, with evidence; questions instead of guesses |

## RACI by activity
R = responsible, A = accountable, C = consulted, I = informed.

| Activity | Client PO | Delivery lead | Solution architect | Engineers | QA |
|---|---|---|---|---|---|
| Change the master PRD | A/R | C | C | I | C |
| Sync the PRD and review its impact | I | I | A/R | C | I |
| Write and ratify an ADR | C | I | A/R | C | I |
| Log a deviation | I | I | A | R | I |
| Plan a sprint | C | A/R | C | C | C |
| Merge a change | I | I | C (risky changes) | A/R | C |
| Release | A | R | C | C | R |
