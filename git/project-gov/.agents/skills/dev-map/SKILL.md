---
name: dev-map
description: Chart and steer a long-running program via a decision map (a MAP.md beside its plans) — destination, append-only decision ledger, typed frontier with blocked-by edges, fog-of-war. Modes chart (redraw the map) | work (resolve exactly ONE decision).
argument-hint: <empty to list maps, a program slug to chart, or a path to a MAP.md> [chart|work]
allowed-tools: Read, Glob, Grep, Bash, Write, Edit, AskUserQuestion, Agent, TodoWrite
user_invocable: true
---

# Map a program: chart the territory, then advance one decision at a time

Some work is bigger than a plan. A plan slices *known* work into
phases; a **program** — months of effort, several plans, real
unknowns — needs a shared substrate for what has been DECIDED, what
is still OPEN, and what is still FOG. That substrate is `MAP.md`:
one file per program, next to its plans, owned by no single session.

The mental model (borrowed with credit from the wayfinder pattern):
planning is **decision-resolution, not document production**. The
map is done when nothing is left to decide — execution belongs to
`/dev-plan` phases, not to the map. Sessions either **chart**
(survey the territory and redraw the map) or **work** (advance the
expedition by resolving exactly one decision).

| Argument shape | Mode | Output |
|---|---|---|
| _empty_ | List every `<plans>/*/MAP.md` + each map's open-frontier count; ask which map and which mode | — |
| Program slug with no existing map (e.g. `pdlc-consolidation`) | Chart (create) | `<plans>/<slug>/MAP.md` |
| Path to an existing `MAP.md` | Ask chart \| work (default **work**) | edits that file in place |

## Where maps live

From the repo root, per kind (`plans`, `brainstorming`, `debug`), first match wins: (1) explicit path, or, when refining a file, the `<kind>` folder it sits under; (2) a location stated in AGENTS.md, CLAUDE.md, CONTRIBUTING.md or README.md; (3) first existing of `resources/work/<kind>`, `docs/work/<kind>`, `docs/<kind>`; (4) `<kind>` under the first existing of `resources/work`, `docs/work`; (5) `resources/work/<kind>`. Use the same steps when reading prior work. State the result.

Below, `<plans>` is the resolved `plans` location. `<brainstorming>` is the resolved `brainstorming` location.

## Portability

Tool names are Claude Code's. Elsewhere use the equivalent and keep every gate. AskUserQuestion: ask in chat and wait. Explore agents: subagents, else sequential reads. Worktree isolation: `git worktree add`. The ARGUMENTS placeholder (with a leading `$`): the text after the skill name. `/dev-x`: your invocation of dev-x. Other `dev-*` skills are optional; if absent, do the step here, never skip it.

## Hard rules

1. **Resolve exactly ONE decision per work session.** The
   discipline is the product: one decision gets full attention,
   full context, and an honest ledger entry. "While we're here"
   batching is churn dressed as progress.
2. **The ledger is append-only.** A reversal is a NEW row whose
   Decision column says `supersedes D<n>` — never an edit to an
   existing row. The history of choices is the program's memory.
3. **A map is not a plan.** No implementation slices, no file
   lists, no code sketches in MAP.md. When a frontier ticket needs
   phasing, hand off to `/dev-plan`; the written plan's path
   becomes the ledger row's Artifact.
4. **Every frontier ticket carries a type and its blocked-by
   edges** (or an explicit `—` for unblocked). The unblocked,
   untaken tickets ARE the frontier — the edge a session can take
   next without waiting on anything.
5. **Fog stays honest.** The fog-of-war section holds in-scope
   areas too murky to state as a precise question. Never silently
   promote fog into a decision; graduate it explicitly once an
   expedition (brainstorm, spike, research) has lit it.
6. **Nothing is deleted.** Resolved frontier rows move to the
   ledger; work ruled irrelevant moves to Out of scope with the
   reason. A map that only grows sections can be trusted as a
   record.
7. **Chart before work when the map is stale.** If shipped code,
   a plan's `STATUS.md`, or the conversation contradicts the map,
   redraw first — working a stale frontier resolves the wrong
   question.
8. **Never write or rewrite MAP.md before the user approves the
   outline in chat** (house rule shared with `dev-plan` /
   `dev-brainstorm`).

## MAP.md template (the shape every map follows)

```markdown
# Map: <Program>

**Status:** charting | underway | arrived | abandoned
**Created:** YYYY-MM-DD · **Last charted:** YYYY-MM-DD

## Destination

2–4 sentences of end-state, then 2–3 measurable arrival criteria —
the map is DONE when these hold and the frontier is empty.

## Decisions so far (append-only ledger)

| ID | Date | Decision | Choice | Rationale | Artifact |
|----|------|----------|--------|-----------|----------|
| D1 | YYYY-MM-DD | <question that was open> | <what was chosen> | <the because> | <plan / brainstorm / commit / MR link, or —> |

## Frontier (open decisions & expeditions)

| ID | Ticket | Type | Blocked by | Size | Next action |
|----|--------|------|-----------|------|-------------|
| F1 | <precise question or expedition> | decision | — | S | resolve in a work session |
| F2 | <…> | expedition | F1 | M | /dev-brainstorm <seed> |

## Fog of war

In-scope areas we know we don't understand yet. One bullet each:
what's murky · which expedition would light it · what event forces
us to explore it sooner.

## Out of scope

Territory explicitly outside this program, each with the reason it
was ruled out.
```

**Ticket types** route each frontier row to the tool that resolves
it:

| Type | Meaning | Resolved via |
|---|---|---|
| `decision` | choosable NOW with what's known | a `dev-map` work session (options table → user picks → ledger row) |
| `expedition` | fog must be explored before anyone can decide | `/dev-brainstorm <seed>` |
| `plan` | direction locked; needs phasing into shippable slices | `/dev-plan <seed or path>` |
| `design` | a new component's shape is the open question | `/dev-brainstorm <idea>` |
| `verify` | a claim/spec must be checked against the code | `/dev-spec-verify <path-or-text>` |
| `probe` | something misbehaves and the cause is unknown | `/dev-debug <symptom>` |
| `task` | manual prerequisite (access, signup, data move) | the user does it; the outcome is the answer |
| `chore` | small direct work; no skill ceremony needed | just do it + commit |

Sizes are the usual S / M / L gut-call — they help pick the next
ticket, nothing more.

## Procedure — chart mode

1. **Name the destination.** 3–5 AskUserQuestion rounds max: what
   does "arrived" look like, measured how, for whom, by roughly
   when? A destination that can't state arrival criteria is itself
   the first frontier ticket.
2. **Inventory the territory.** Read everything that already
   exists for this program: plans + `STATUS.md` under
   `<plans>/<program>*/`, brainstorms under
   `<brainstorming>/`, and the shipped code (launch
   Explore agents in parallel for the code side). The map must
   start from reality, not from memory.
3. **Harvest the ledger.** Existing plans carry locked-decisions
   tables; existing brainstorms carry recommended directions that
   were acted on. Fold each into a ledger row with its Artifact
   link — the map inherits history instead of re-deriving it.
4. **Propose the frontier + fog + out-of-scope.** Type every
   frontier row, analyse blocked-by edges in a second pass (edges
   are easier to see once all tickets are on the table), and be
   honest about what is fog rather than forcing fuzzy areas into
   fake-precise tickets.
5. **Validate the outline in chat** — destination, ledger row
   count, frontier table, fog bullets. Redirects are cheap here.
6. **Write MAP.md** and stop. Charting is one session's work; the
   first work session is a new invocation.

## Procedure — work mode

1. **Read the map; check freshness.** Compare against plan
   STATUS.md files and recent commits. Stale → recommend chart
   mode and stop.
2. **Pick ONE ticket.** List the unblocked frontier rows,
   recommend the highest-leverage one (what unblocks the most
   downstream tickets), and let the user confirm or override.
3. **Resolve per type.**
   - `decision`: present an options table — choice, consequence,
     reversibility — with a recommendation. The user picks. Append
     the ledger row (with rationale) in the same session.
   - `chore`: do the work, commit via `/dev-group-and-commit`,
     record the outcome.
   - every other type: prepare the hand-off (the exact
     `/dev-brainstorm` / `/dev-plan` / … invocation with its seed
     text or path), present it, and STOP. The user runs the skill;
     a later work session records the outcome into the ledger and
     re-frontiers what it unblocked.
4. **Update the map atomically.** One edit: frontier row removed,
   ledger row appended, newly-unblocked tickets noted, fog
   graduated if the resolution lit any of it, `Last charted`
   untouched (work isn't charting).
5. **Post the map delta** to chat — `resolved F<n> → D<m>;
   unblocked F<x>, F<y>; fog graduated: <…>` — and stop. One
   decision per session, hard stop.

## Anti-patterns

- ❌ **Resolving three decisions "while we're here".** Each extra
  decision gets a fraction of the context it deserves; the ledger
  fills with under-reasoned rows.
- ❌ **Map-as-plan.** Slices, file paths, and code sketches belong
  in `/dev-plan` output. The map records that the plan EXISTS.
- ❌ **Frontier rows without blocked-by analysis.** An edge-less
  frontier hides the real takeable edge and invites working a
  blocked ticket.
- ❌ **Fog silently promoted to decisions.** If nobody explored
  it, the "decision" is a guess wearing a ledger row.
- ❌ **Rewriting ledger history.** Supersede, never edit. A ledger
  that can be rewritten can't be trusted.
- ❌ **Charting every session.** Chart when stale or at program
  kickoff; otherwise the map is a substrate, not a deliverable to
  polish.
- ❌ **A map for a one-plan feature.** If the whole thing ships in
  one roadmap, `dev-plan`'s locked-decisions table is enough — a
  map would be ceremony.

## When to invoke

- A workstream spans (or will span) SEVERAL plans/roadmaps — e.g.
  a consolidation program, a platform migration, a multi-quarter
  hardening push.
- "Where were we on X?" keeps costing a re-derivation at the start
  of every session — the ledger answers it in one read.
- Decisions keep getting re-litigated because they live in chat
  history instead of an append-only record.
- A brainstorm concluded the idea is really a PROGRAM (its
  hand-off will say so) and the open questions outnumber what one
  roadmap can hold.

## When NOT to invoke

- Single feature, single roadmap → `/dev-plan` alone; its
  locked-decisions table already covers the record-keeping.
- The territory is unknown but small → `/dev-brainstorm` first;
  chart a map only if the brainstorm reveals program-scale scope.
- Mid-implementation of a phase → finish the phase; update the
  map in a work session afterwards.

## Worked example (reference)

The user invokes `/dev-map pdlc-consolidation`.

**Chart**: no `<plans>/pdlc-consolidation/MAP.md`
exists → chart mode. The skill asks 4 destination questions, then
inventories: two shipped roadmaps with STATUS ✅, one 🚧, one
brainstorm, and the shipped code for the completed waves. It
harvests 9 ledger rows from the existing locked-decisions tables
(each Artifact column linking the plan that recorded it), proposes
a 6-row frontier (2 `decision`, 1 `expedition`, 2 `plan`, 1
`task`), two fog bullets, and an out-of-scope list. The user
reorders one blocked-by edge in chat; the skill writes the map and
stops.

**Work, a week later**: `/dev-map
<plans>/pdlc-consolidation/MAP.md` → work mode. The
frontier's unblocked rows are F2 (`decision`: which store backs
capability-pack metadata) and F5 (`task`: request a staging
realm). The skill recommends F2 (it blocks both `plan` tickets),
presents a 3-option table with consequences and reversibility, the
user picks, and the skill appends `D10`, removes F2, notes F3+F4
are now unblocked, posts the delta, and stops — F5 remains for
another session.

## See also

- `dev-plan` — the doing side; `plan`-typed tickets hand off to
  it, and its plans mirror new locked decisions back into the
  map's ledger.
- `dev-brainstorm` — the expedition tool for lighting fog; its
  hand-off recommends `/dev-map` when an idea turns out to be a
  program.
- The `STATUS.md` convention the freshness check reads: a file beside
  a plan's roadmap headed `# Status: ✅ Done`, `# Status: 🚧 In Progress`
  or `# Status: ❌ Superseded`.  A plan without one is draft /
  pre-implementation.  `<plans>/README.md` documents it where one exists.
