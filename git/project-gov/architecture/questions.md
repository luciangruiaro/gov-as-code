# Open questions and assumptions

Anything we state about the client's systems or the product that is **not yet confirmed** carries an id from this page: `q…` for a question we are waiting on, `a…` for an assumption we are working under. ADRs, plans and the architecture overview cite these ids, so an unconfirmed claim is never mistaken for a fact. When a question is answered, record the answer and the date, and update whatever cites it.

## Questions
| Id | Question | Requirements | Owner (role) | Status | Answer (date) |
|---|---|---|---|---|---|
| q1 | SAMPLE: Which identity provider does the organisation use, and does it support OpenID Connect with group claims? | FR-001, OI-001 | client IT lead | open | — |
| q2 | SAMPLE: Does Hello World ever run outside developer machines, and does it then need sign-in first? | OI-003, FR-001 | client product owner | open | — |

## Assumptions
| Id | Assumption | Requirements | Holds until | Status |
|---|---|---|---|---|
| a1 | SAMPLE: The identity provider supports OpenID Connect. | FR-001 | q1 is answered | assumed |
| a2 | SAMPLE: Hello World runs on developer machines only, so it needs no sign-in. | OI-003, GR-002 | q2 is answered | assumed |
