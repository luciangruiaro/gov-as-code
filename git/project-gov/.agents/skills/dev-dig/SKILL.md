---
name: dev-dig
description: One diagnostic probe, end to end. Use for "run a probe", "dig into this number", "why is this metric flat", and when a surprising number needs its next measured fact — an eval delta that didn't move, a component contributing nothing, a cost spike nobody can explain. Falsifiable hypothesis, cheapest kill first, measured numbers recorded on the owning ticket or work doc, and a mandatory successor question — no probe is a leaf.
argument-hint: <the surprising number or question, e.g. "recall flat after the rerank change" — or empty to pull from an open debug doc>
allowed-tools: Read, Glob, Grep, Bash, Write, Edit, AskUserQuestion, Agent, TodoWrite
user_invocable: true
---

# Dig — one diagnostic probe, end to end

A diagnostic probe is scheduled work with a ritual, not spare-time
curiosity. This skill runs one probe end to end and refuses to close
without naming its successor. Probes **measure**; fixes are their own
MRs/PRs. If mid-probe the fix becomes obvious, note it and finish the
measurement — then route the fix through `/dev-plan` or a plain MR/PR.

## Where probe docs live

From the repo root, per kind (`plans`, `brainstorming`, `debug`), first match wins: (1) explicit path, or, when refining a file, the `<kind>` folder it sits under; (2) a location stated in AGENTS.md, CLAUDE.md, CONTRIBUTING.md or README.md; (3) first existing of `resources/work/<kind>`, `docs/work/<kind>`, `docs/<kind>`; (4) `<kind>` under the first existing of `resources/work`, `docs/work`; (5) `resources/work/<kind>`. Use the same steps when reading prior work. State the result.

Below, `<debug>` is the resolved `debug` location.

## Portability

Tool names are Claude Code's. Elsewhere use the equivalent and keep every gate. AskUserQuestion: ask in chat and wait. Explore agents: subagents, else sequential reads. Worktree isolation: `git worktree add`. The ARGUMENTS placeholder (with a leading `$`): the text after the skill name. `/dev-x`: your invocation of dev-x. Other `dev-*` skills are optional; if absent, do the step here, never skip it.

## When it fires

- A number in a report surprised someone. Surprise is the queue's input.
- An MR/PR claimed to fix a quality problem and the metric came back flat:
  flat plus "fix" means the wrong layer may have been fixed. That is a
  probe trigger, not a pass to shrug at.
- An open investigation under `<debug>/` needs its next
  measured fact.

## Process

1. **Hypothesis, falsifiable, one sentence.** "FTS loses golds at
   fusion" is one; "look into FTS" is not. Record which ticket or work
   doc owns it (a ticket in the repo's tracker, an issue/MR/PR, or a doc under
   `<debug>/`). If nothing owns it, create the debug doc
   first — a probe without an owning question is usually a symptom of
   an unfiled decision.
2. **Cheapest kill first.** Name the smallest measurement that could
   prove the hypothesis wrong, and estimate it in hours. If the
   cheapest probe is more than a day, slice the hypothesis. The house
   toolbox, cheapest first. Resolve each class to this repo's own tool
   from its agent guides, docs, routes, and scripts, and skip a class it
   doesn't have:
   - a read-only census (such as SQL counts) against the authoritative
     data store;
   - one request through the real pipeline, reading its trace or debug
     output — a component contributing nothing is visible in one response;
   - the repo's eval, benchmark, or golden-test harness for before/after
     deltas;
   - the effective-configuration view or dump when the hypothesis is "the
     config isn't what we think it is" — check each value's source and
     what overrides it before blaming the code;
   - usage metadata or the cost ledger for spend hypotheses.
3. **Instrument before you argue.** If the needed signal never leaves
   the pipeline, a **default-off** knob or trace event that exposes it
   is in scope for the probe (the pattern: add a typed event to the
   repo's trace or structured logging, or a config-gated diagnostic field —
   never a print). Serving behavior must not change; a before/after run of
   the repo's tests or eval harness on the instrument change proves it did not.
4. **Run and record.** Measured numbers land on the owning ticket or
   work doc, with the artifact path and the exact command that produced
   them. Anything posted to an issue tracker goes through the user first —
   draft the comment, human confirms. A probe whose result lives only
   in chat did not happen.
5. **Verdict updates the owner**: hypothesis confirmed / killed / needs
   a bigger instrument. Killed is a full success — it retires a
   work-stream nobody has to argue about again.
6. **Name the next question.** Mandatory. The closing note ends with
   "Next probe: …" and either points at an existing ticket/doc or
   creates one. No probe is a leaf.

## What this skill never does

- Fix anything. Probes measure; fixes are their own MRs/PRs with their own
  before/after deltas.
- Run load against a shared or production deployment without asking —
  a local stack or a snapshot is the default target.
- Close without a successor question.
- Post to an issue tracker or chat without human confirmation.
