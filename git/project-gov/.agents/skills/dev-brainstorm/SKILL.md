---
name: dev-brainstorm
description: Take a raw idea (one sentence to multi-paragraph) and produce an exploration doc in the repo's brainstorming folder, filed by month — repo-grounded framings with industry references, tensions, open questions + fog, ONE recommended direction, and the next skill to invoke.
argument-hint: <empty for interactive idea capture, or a free-text idea, or a path to an existing brainstorm to refine/extend>
allowed-tools: Read, Glob, Grep, Bash, Write, Edit, AskUserQuestion, Agent, TodoWrite, WebSearch, WebFetch
user_invocable: true
---

# Brainstorm an idea — exploratory pass

Take an idea — however small or ambitious — and produce a Markdown
exploration that cross-checks the repo's existing vision +
documentation + code, surfaces multiple framings, calls out
industry SOA references, and lands a recommended forward path the
user can refine or feed into another skill.

The output is **exploratory, not prescriptive**.  dev-plan is the
skill that turns the chosen direction into shippable phases;
dev-brainstorm is the upstream pass that picks the direction
worth committing to.

## Modes / argument shapes

| Argument shape | Mode | Output location |
|---|---|---|
| _empty_ | Interactive: skill asks "what do you want to brainstorm?" then runs greenfield mode | `<brainstorming>/<YYYY-MM>/<slug>/<slug>.md` |
| Free-text idea (e.g. `add live collaboration to the SPA`) | Greenfield: full ideation flow | `<brainstorming>/<YYYY-MM>/<slug>/<slug>.md` |
| Path to existing brainstorm (a brainstorm `.md`) | Refinement: re-open + extend with new questions / discoveries | append a `## Update <date>` section to the same file |

Slugs: lowercase, hyphenated, no dates.  ✓ `multi-org-agent-routing`
✗ `2026-04-30-routing-thoughts`.

## Where brainstorms live

From the repo root, per kind (`plans`, `brainstorming`, `debug`), first match wins: (1) explicit path, or, when refining a file, the `<kind>` folder it sits under; (2) a location stated in AGENTS.md, CLAUDE.md, CONTRIBUTING.md or README.md; (3) first existing of `resources/work/<kind>`, `docs/work/<kind>`, `docs/<kind>`; (4) `<kind>` under the first existing of `resources/work`, `docs/work`; (5) `resources/work/<kind>`. Use the same steps when reading prior work. State the result.

Below, `<brainstorming>` is the resolved `brainstorming` location. `<plans>` is the resolved `plans` location.

## Portability

Tool names are Claude Code's. Elsewhere use the equivalent and keep every gate. AskUserQuestion: ask in chat and wait. Explore agents: subagents, else sequential reads. Worktree isolation: `git worktree add`. The ARGUMENTS placeholder (with a leading `$`): the text after the skill name. `/dev-x`: your invocation of dev-x. Other `dev-*` skills are optional; if absent, do the step here, never skip it.

## Hard rules

1. **Never write the brainstorm file before the user has approved
   the shape.**  Output the framings + recommended-direction
   summary in chat first; only write to disk after explicit
   consent.
2. **Always brainstorm BEFORE narrowing.**  Multiple framings are
   the deliverable.  Three is a floor; five is a comfortable
   ceiling.  A single-framing brainstorm is dev-plan in disguise
   — redirect the user to /dev-plan if their idea is already
   pinned.
3. **Cross-check the repo before riffing.**  Use Explore agents
   (parallel where useful) to find: existing docs that cover the
   topic; existing code that already partially solves it; prior
   plans under `<plans>/` that touched it; locked
   architectural decisions in the repo's agent guides, rules files,
   and architecture docs.  Cite file paths + line numbers — never
   handwave.
4. **Industry references are part of the deliverable.**  If a
   framing maps to a well-trodden pattern (event sourcing, CQRS,
   actor model, sagas, etc.), name it.  If a SaaS reference
   exists (GitHub PATs, Stripe Connect, LangChain RAG, etc.),
   cite it.  WebSearch + WebFetch are allowed and encouraged
   when the LLM's training data is stale on a fast-moving area.
5. **Surface tensions, don't paper over them.**  When two
   framings genuinely conflict (e.g. "centralised vs federated"),
   show the trade-off as a table; don't pick prematurely.
6. **One recommended direction at the end.**  After exploring
   N framings, the doc lands a single "given the repo's
   constraints + the user's intent + industry practice, this is
   the path most likely to ship cleanly" recommendation.  Label
   the others "viable but deprioritised" with the trade-off
   explicitly stated.
7. **Always end with a hand-off.**  The doc's final section says
   "next step: invoke /dev-plan against this brainstorm" OR
   "next step: build a 1-day spike for framing #2" OR similar.
   The user shouldn't have to guess what to do after reading.
8. **Out-of-scope is part of the doc.**  Adjacent ideas surfaced
   during the brainstorm get a "Not exploring here" list so
   they're captured but explicitly deferred.
9. **Refinement mode is append-only.**  When invoked on an
   existing brainstorm, add a new `## Update <YYYY-MM-DD>` block
   at the bottom — never rewrite earlier framings.  History is
   the durable record of how thinking evolved.
10. **Brainstorms live in a month bucket:
    `<brainstorming>/<YYYY-MM>/<slug>/`.**  The bucket
    is the month the brainstorm was **created** and never changes —
    refinement appends to the file in its ORIGINAL bucket, never
    copies it into the current month.  Get it with `date +%Y-%m`
    (PowerShell: `Get-Date -Format yyyy-MM`).

## Output template

The shape every brainstorm follows.  Don't deviate without a
reason.

```markdown
# Brainstorm: <Idea>

<2-3 sentence intent — quote the user's seed idea verbatim, then
the operator's gloss on what it means in repo-context terms.>

**Slug:** `<slug>`
**Created:** <YYYY-MM-DD>
**Author:** <skill-invocation context — e.g. "operator + dev-brainstorm">
**Status:** exploratory | refined | superseded

---

## Seed

> The user's input verbatim, including any caveats or tone they
> brought.  Don't reword.

## Repo context — what already exists

What the codebase + docs already say about this area.  Cite:
- Existing implementation: `<file>:<line>` references
- Existing docs: operator and developer docs, architecture docs
- Locked decisions in the agent guides and rules files
- Prior plans / brainstorms under `<plans>/` /
  `<brainstorming>/`
- Modules, integrations, services that touch the same surface

If something is missing entirely, say so explicitly: "No
existing surface covers <X>."

## Framings

For each framing (3-5 ideal):

### Framing A: <name>

**Mental model:** what worldview drives this framing.  One
sentence.

**Industry reference:** where this has been done before (named
SaaS / OSS pattern / RFC / book chapter).  One link or citation.

**Sketch:** 4-8 bullet points showing how the repo would change
if this framing won.  Concrete.

**Pros:** what this gets us.

**Cons / risks:** what could go wrong; what gets harder.

**Effort guess:** S / M / L / XL — order-of-magnitude only.

(Repeat for each framing.)

## Tensions

When two or more framings genuinely conflict, capture the
trade-off as a table:

| Dimension | Framing A | Framing B | Framing C |
|---|---|---|---|
| Latency | low | high | medium |
| Operator cost | high | low | medium |
| Locked-decision risk | high | medium | low |
| ... | ... | ... | ... |

## Open questions

Things this brainstorm couldn't answer; the user should resolve
before dev-plan converts a framing into phases.  Each carries its
blocking edge (another question, or an expedition that must run
first — `—` when freely answerable) and a recommended-default in
case the user wants to defer.

1. **<question>** — Blocked by: <Q<n> | an expedition | —> —
   Recommended default: <answer>.

## Fog of war

In-scope areas beyond this brainstorm's light radius — too murky
to even state as a precise question.  One bullet each: what's
murky · the candidate expedition (deeper brainstorm, spike,
research) that would light it · what event forces exploring it
sooner.

## Decision ledger

Micro-decisions locked DURING the brainstorm (framing eliminated
with the user, constraint accepted, naming settled) — the seed of
the eventual plan's locked-decisions table or the program's
`MAP.md` ledger:

| ID | Decision | Choice | Rationale |
|---|---|---|---|
| B1 | ... | ... | ... |

## Recommended direction

After weighing the framings against the repo's locked decisions,
the operator's tone, and industry practice: **Framing X**.

**Why this one:** 2-3 sentences explaining the call.

**Why not the others:** one sentence each.  Don't reduce them to
strawmen — name the real reason they didn't win.

## Not exploring here

Adjacent ideas that surfaced during the brainstorm and explicitly
do NOT need exploring in this pass:

- **<idea>** — out of scope because <reason>.

## Next step

What the user should invoke next:

- `/dev-plan <brainstorming>/<YYYY-MM>/<slug>/<slug>.md` —
  turn the recommended framing into phased work.  *(Most common.)*
- `/dev-map <program-slug>` — when the idea turned out to be a
  PROGRAM (several plans, months of work, real unknowns): chart a
  decision map first; this brainstorm's decision ledger and open
  questions seed the map's ledger and frontier.
- "Build a 1-day spike for Framing Y first" — when an unknown
  needs a quick prototype before committing.
- Manual refinement — when the user wants to live with the doc
  for a few days and let it season.
```

## Procedure

### Phase 1 — Determine mode + capture intent

If args is empty, AskUserQuestion: "What do you want to
brainstorm?  Give me the rough idea — a sentence or a paragraph.
The bigger the idea the more useful this skill is, but small
ideas work too."

If args is a path to an existing brainstorm: read it,
treat as refinement mode, ask "what new angle do you want to
explore?".

Otherwise: take args as the seed idea.

### Phase 2 — Brainstorm + clarify (3–7 questions)

Use AskUserQuestion to pin down what's vague.  Default questions:

- **Audience.**  Who benefits — operator / developer / end user
  / a future capability?  Different audiences pull the framings
  in different directions.
- **Scope sniff.**  Does this touch one subsystem or
  cross-cutting?  Single feature or framework-level shift?
- **Constraints / locked-decisions to honour.**  Anything in
  the repo's agent guides the user wants to push against, or
  anything that must stay invariant?
- **Time horizon.**  Ship-this-quarter vs. north-star vision
  framings need different framings.
- **Why now.**  What surfaced this idea today?  (The answer
  often reveals the un-named real constraint.)

Conditional follow-ups:
- If the idea is technical — ask which existing pattern feels
  closest.
- If it's UX — ask what the "after" demo would look like.
- If it's architectural — ask whether the user wants to evaluate
  3 existing precedents or generate 3 fresh framings.

Cap at 7 total.  More is procrastination.

### Phase 3 — Codebase + history research (parallel Explore agents)

Launch up to 3 Explore agents in parallel:

- **Existing surface** — find every code path, doc, and prior
  plan that touches this area.  Returns a "what already exists"
  briefing.
- **Locked decisions in scope** — read the agent guides, rules
  files, and architecture docs for any rule that constrains the
  framings.
- **Prior brainstorms / plans** — search
  `<brainstorming>/` and `<plans>/`
  for related history.

For ideas where industry practice matters (event sourcing,
streaming, multi-tenancy, agent protocols, etc.), supplement with
WebSearch + WebFetch — the LLM's training is often stale on
fast-moving SaaS patterns.

### Phase 4 — Synthesise framings + recommendation

Decide:

1. **3-5 framings** — distinct mental models, each with a real
   industry reference (or the explicit "no precedent; novel
   ground" callout).
2. **Tensions** — if any two framings genuinely conflict, capture
   the trade-off table.
3. **Open questions** — what the brainstorm can't answer; each
   gets its blocking edge (question / expedition / `—`) and a
   recommended default.
4. **Fog of war** — in-scope areas too murky to even phrase as a
   question yet, each with the expedition that would light it.
5. **Decision ledger** — micro-decisions locked with the user
   along the way; they seed the plan's locked-decisions table (or
   a program map's ledger).
6. **One recommended direction** — the framing most likely to
   ship cleanly given the repo's constraints + the user's intent.
7. **Hand-off** — what skill (or manual step) comes next.  When
   the scope revealed itself as program-sized, that hand-off is
   `/dev-map`, not `/dev-plan`.

### Phase 5 — Validate with the user before writing

Post a compact summary to chat:

```
Proposed brainstorm: <slug>
Mode: greenfield | refinement
Framings (N): A. ... | B. ... | C. ...
Recommended: <framing-name> + reason in one sentence
Open questions: <count>
Output: <brainstorming>/<YYYY-MM>/<slug>/<slug>.md
```

Ask: "Ship this?  Or want to redirect a framing / add a new one
before I write?"

The cost of editing an outline in chat is far smaller than
editing a written file — make the redirect cheap.

### Phase 6 — Write the brainstorm file

On approval, render the full doc using the template and write
to disk.  File naming:

| Mode | Path |
|---|---|
| Greenfield | `<brainstorming>/<YYYY-MM>/<slug>/<slug>.md` |
| Refinement | append a `## Update <YYYY-MM-DD>` section to the existing file |

If a sibling `STATUS.md` would help (the brainstorm has a clear
"superseded by /plans/X" outcome), write that too.

### Phase 7 — Hand off

After writing, surface:

```
✓ Brainstorm written to <path>
  - <N> framings explored
  - Recommended: <framing-name>
  - <K> open questions to resolve
  - Suggested next step: /dev-plan <path>   (or other)

The brainstorm is exploratory.  It's safe to live with for a
few days before committing — re-invoke /dev-brainstorm <path>
to add a new angle, or /dev-plan <path> when ready to phase.
```

Don't auto-invoke the next skill.  The user picks the cadence.

## Anti-patterns

- ❌ **Single-framing brainstorm.**  If you can only see one
  way to do this, the user already has a plan; redirect them to
  /dev-plan.
- ❌ **Reducing every framing to a strawman so one wins.**  Name
  the real reason each lost.  "Costs more than expected" is a
  reason; "is bad" is not.
- ❌ **Skipping repo research because the idea "sounds clear".**
  The repo always has prior art that shapes which framings are
  realistic.
- ❌ **Pretending to know the answer to every open question.**
  Some questions are genuinely open; capture them with
  recommended defaults and let the user choose.
- ❌ **Writing the file before showing the outline.**  The user's
  redirect is far cheaper at outline stage.
- ❌ **Output that overlaps dev-plan.**  Brainstorm is "what could
  this be?"; dev-plan is "how do we ship this specific shape?".
  Keep the boundary clean — no phase tables, no slice letters,
  no verification recipe.
- ❌ **Auto-invoking the next skill.**  Hand off; let the user
  pace.

## When to invoke

- "I'm not sure what we want here yet — let me throw an idea and
  you brainstorm it."
- "Take this fuzzy idea and tell me three good framings before I
  pick one."
- "Cross-check this against the repo and see if anything obvious
  blocks it."
- "I want to know what industry SOA looks like for X before we
  commit to a plan."
- After /dev-doc-audit surfaces a gap: brainstorm before planning
  if the gap is broad / unclear in shape.

## When NOT to invoke

- The user already knows the framing they want.  Run /dev-plan.
- The work is genuinely tiny (a typo, a one-line refactor).  Just
  do it.
- The user is debugging a real production issue.  Run /dev-debug.
- The output of the brainstorm would be < 100 words.  That's a
  chat reply, not a document.

## Worked example

User invokes `/dev-brainstorm should we add per-org branded login pages`.

**Phase 1**: Greenfield, free-text.

**Phase 2**: Asks 5 questions — audience (end users), scope sniff
(auth + branding subsystems), constraints (multi-tenancy already
shipped, branding tokens-per-realm exists), time horizon
(this quarter), why now (sales asked for it).

**Phase 3**: Three Explore agents in parallel:
- Existing surface: `auth/oidc/`, the login page component, the
  branding service, and the prior plan that added per-realm branding.
- Locked decisions: branding tokens are realm-scoped (parent
  multi-tenancy plan L7), login lives at `/auth/login` (app
  routing).
- Prior brainstorms: none on per-org login.

**Phase 4**: Three framings:
- A. URL-prefix `/<org-slug>/auth/login` with server-side
  branding lookup.  Industry ref: Slack workspace URLs.
- B. Subdomain `<org-slug>.example.com/auth/login` with DNS
  wildcard.  Industry ref: Stripe Connect.
- C. Unified `/auth/login` with email-domain → org auto-detect
  before render.  Industry ref: Google Workspace
  account-chooser.

Tensions table: ops complexity (subdomain wildcard cert) vs UX
(URL clarity) vs SEO.

Recommended: **C** — the existing email-domain → org resolution
already lives in the registration service; minimal
infrastructure churn.

**Phase 5**: Posts the outline.  User accepts but adds a question
"what about magic-link emails — do they need per-org branding
too?".  Skill adds it as Open Question #4.

**Phase 6**: Writes
`<brainstorming>/<YYYY-MM>/per-org-login/per-org-login.md`.

**Phase 7**: Hands off.  Suggests `/dev-plan
<brainstorming>/<YYYY-MM>/per-org-login/per-org-login.md`
when the user is ready to phase the work.

## See also

- `dev-plan` — the natural follow-on once
  a framing is picked.
- `dev-map` — the follow-on when the idea
  turned out to be a program; the brainstorm's decision ledger +
  open questions seed the map.
- `dev-doc-audit` — complementary;
  doc-audit gaps often become brainstorm seeds.
- `dev-spec-verify` — verify a
  brainstorm's recommended framing against current code before
  dev-plan turns it into phases.
