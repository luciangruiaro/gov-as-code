# Audits

Reviews and audits, dated: `YYYY-MM-DD_slug.{md,html}`. A review that has several parts gets a folder: `YYYY-MM-DD_slug/`.

| Kind | Written by |
|---|---|
| `*_prd-adr-alignment.md`: what a PRD change means for the decisions, question by question | `prd/sync/impact.py --write`, then people (the Answers) and `gov-adr` (landing them) |
| `*_architecture-review.md`: a design, diff or repository against the ratified ADRs | `dev-architecture-review` |
| `*_spec-verify.md`: the code against the PRD or a plan, claim by claim | `dev-spec-verify` |
| `*_doc-audit.md`: the documentation against the code | `dev-doc-audit` |

**Rules**
- An audit is never deleted. A superseded one gets a banner at the top: `> Superseded by YYYY-MM-DD_slug.md`.
- An alignment worksheet is the record of why a decision moved: keep it answered, and link it from the ADRs it changed.
- Findings name roles and cite evidence (file:line, a requirement id, an ADR section).
