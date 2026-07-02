# architecture/: the decisions the code obeys

| Path | What it is | Who writes it |
|---|---|---|
| [`architecture.md`](architecture.md) | The overview: context, building blocks, flows, quality attributes. Current state only. | Solution architect, with agents |
| [`decisions/`](decisions/) | The ADRs, their [index](decisions/README.md), the [template](decisions/_template.md) and the [backlog](decisions/backlog.md) of questions that need an ADR | `gov-adr` skill, ratified by the solution architect |
| [`deviations/`](deviations/README.md) | Where the as-built code departs from a ratified ADR, with an exit condition per row | Proposed by `dev-architecture-review`, appended by the architect |
| [`questions.md`](questions.md) | Open questions (`q…`) and working assumptions (`a…`), cited wherever a claim is not yet confirmed | Anyone; answers are recorded with a date |

How the parts connect:

```
PRD requirement ids ──cited by──▶ ADR backlog entry ──becomes──▶ ADR (DRAFT → VISION-RATIFIED)
        ▲                                                             │
        │ prd/sync/impact.py: a changed id finds every citation       │ binds
        └─────────────────────────────────────────────────────────── code ──departs?──▶ deviations/
```
