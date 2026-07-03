# Plans + roadmaps

Implementation plans for this repository live here. Each plan is a
durable record of what we agreed to build, why, and at what cost —
written so any developer (or AI session) can pick it up cold and
ship it without follow-up design conversation.

## Layout

```
plans/
├── README.md                          # this file
└── <YYYY-MM>/                         # the month the plan was CREATED
    ├── <plan-name>/
    │   ├── <plan-name>.md             # parent roadmap (vision, locked decisions, phase split)
    │   ├── STATUS.md                  # implementation marker (see below)
    │   └── phases/
    │       └── phase-N-<slug>.md      # ship-in-one-session sub-plans, one per phase
    └── <standalone-plan>.md           # single-file plans (no phases)
```

Standalone plans (single markdown file, no `phases/` dir) get a
sibling `STATUS.md` in the same parent directory, or — if the file
lives directly in a month bucket — a sibling `<plan-name>-STATUS.md`.

## Month buckets

Plans are grouped by the month they were **created**
(`plans/2026-07/skills-infrastructure/`). Three rules
keep the scheme honest:

1. **The bucket is creation time, not delivery time.** A plan started
   in June that ships in September stays in `2026-06/`. The bucket
   answers "when did we decide to do this", which is the question
   that stays stable.
2. **A plan never moves between buckets.** Re-bucketing breaks every
   inbound link and the reader's memory of where it lived.
3. **Never rename a bucket.** `date +%Y-%m` at creation is the whole
   rule; there is no back-filling or tidying.

The same convention applies to the repository's brainstorming folder.
`/dev-plan` and `/dev-brainstorm` create the bucket automatically.

## `STATUS.md` — the implementation marker

A short markdown file next to the parent roadmap. Tells a future
maintainer at a glance whether the plan is shipped, in flight, or
superseded — without grepping git log.

### Status header values

| Header | Meaning |
|---|---|
| `# Status: ✅ Done` | All phases shipped + verified. The plan is the durable record of the *why*; the codebase is the source of truth for the *what*. |
| `# Status: 🚧 In Progress` | At least one phase has shipped; others are still pending. List which phases are done in the body. |
| `# Status: ❌ Superseded` | Plan was replaced by a newer one. Body links to the successor. |

Plans without a `STATUS.md` are treated as draft / pre-implementation.
Adding the file is the moment the plan transitions out of "just an
idea" into "we're building this".

### Template

```markdown
# Status: ✅ Done

**Shipped:** YYYY-MM-DD
**Shipped in version:** <version-tag-or-omit>
**Phases shipped:** <e.g. 0, 1, 2, 3, 4 — or omit for single-file plans>

## Scope landed

<3-6 bullets naming the major capabilities the plan delivered.
Anchor with file paths so a future reader can jump straight to the
code.>

## Notes

<Anything a future maintainer should know:
- Pre-existing failures still pre-existing.
- Out-of-scope items deferred to which follow-up.
- Surprises during implementation that aren't captured in commits.>
```

For in-progress plans, swap the header for `🚧 In Progress` and use
`**Phases shipped:**` to list only the done ones; add a
`**Phases pending:**` line below it. Flip to `✅ Done` once the last
phase lands.

For superseded plans, keep the body short:

```markdown
# Status: ❌ Superseded

**Replaced by:** <relative link to the successor plan's roadmap>
**Why:** <one sentence on what changed>
```

## When to write `STATUS.md`

- **At the start of implementation** — write a `🚧 In Progress`
  marker so concurrent work doesn't accidentally re-plan the same
  thing.
- **As phases ship** — update the body to list completed phases.
- **At completion** — flip the header to `✅ Done` and freeze the
  scope-landed bullets.
- **If the plan gets replaced** — flip to `❌ Superseded` and
  point at the successor.

A previously-shipped plan whose scope drifted (e.g. one phase got
ripped out and rebuilt under a different roadmap) keeps the
original `STATUS.md` and the successor's `STATUS.md` references
back via the `Notes` section. Don't rewrite history; document it.

## Why a sibling file (not frontmatter on the plan itself)

The parent roadmap is the durable record of the *why* — the locked
decisions, the brainstorm-turned-design, the trade-off table. We
don't edit it after the rollout because re-touching the durable
record loses the as-it-was-decided fidelity. A sibling file gives
us a status surface that can change as the world changes without
mutating the historical document.

The convention is doc-driven (no validator, no CI gate). New plan
authors discover it via `/dev-plan` and via this README. Drift is a
doc-review concern, not a build-break concern.

## See also

- `/dev-plan` — the skill that produces new plans in this folder.
- The repository's agent guides (such as `CLAUDE.md` or `AGENTS.md`)
  — repo-wide conventions.
