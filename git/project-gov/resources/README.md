# resources/: the brand, the working material, the reviews

| Path | Holds | Written by | Naming |
|---|---|---|---|
| [`ui-kit/`](ui-kit/README.md) | The design tokens and components every screen and report uses | People | — |
| [`work/brainstorms/`](work/brainstorms/README.md) | Framings of a rough idea, compared, with one recommended | `dev-brainstorm` | `<YYYY-MM>/<slug>/<slug>.md` |
| [`work/plans/`](work/plans/README.md) | Roadmaps and ship-in-one-session phase plans, program maps | `dev-plan`, `dev-map` | `<YYYY-MM>/<slug>/<slug>.md` + `STATUS.md` + `phases/`; `<program>/MAP.md` |
| [`work/debug/`](work/debug/README.md) | Investigations: symptom, hypotheses, evidence, cause, fix plan | `dev-debug`, `dev-dig` | `<slug>/<slug>.md` |
| [`audits/`](audits/README.md) | Reviews, audits, and the PRD alignment worksheets | `gov-prd-sync`, `dev-architecture-review`, `dev-spec-verify`, `dev-doc-audit` | `YYYY-MM-DD_slug.{md,html}` |
| `local/` | Your own scratch files, digest drafts (gitignored) | You | anything |

**Rules**
- Working material is versioned like everything else: a plan's history is part of the project's history.
- Nothing here is deleted. A superseded document gets a banner at the top (`> Superseded by …`) and stays.
- A brainstorm or plan cites the PRD ids it serves (`FR-002`), so a PRD change finds it (`prd/sync/impact.py`).
- The month in a path is the month the work started. A plan never moves when it runs late.
