---
name: dev-architecture-review
description: Review a code scope for architectural violations against the repo's OWN documented architecture — discovers rules, architecture docs, ADRs and lint gates first (scripts/discover_context.py), derives checks that cite their sources, and falls back to a generic severity ladder when nothing is documented.
argument-hint: <path, PR number, --staged, or empty for uncommitted changes>
allowed-tools: Read, Glob, Grep, Bash, Agent
user_invocable: true
---

# Architecture Review

Audit a code scope for architectural violations against the repository's
documented philosophy, patterns, and separation of concerns. The skill is
**repo-agnostic**: it never assumes which documents define the architecture —
it discovers them first and derives its checks from what actually exists.

## Portability

Tool names are Claude Code's. Elsewhere use the equivalent and keep every gate. AskUserQuestion: ask in chat and wait. Explore agents: subagents, else sequential reads. Worktree isolation: `git worktree add`. The ARGUMENTS placeholder (with a leading `$`): the text after the skill name. `/dev-x`: your invocation of dev-x. Other `dev-*` skills are optional; if absent, do the step here, never skip it.

## Step 0 — Discover the corpus

Run the scanner that ships next to this skill (path is relative to this
SKILL.md's directory):

```bash
python <skill-dir>/scripts/discover_context.py
```

Use whichever Python launcher exists (`python3`, `python`, or `py -3`). If
none does, do the same discovery by hand with file search. Pass
`--repo-root <dir>` for a plain directory with no Git.

It reports the repo's architecture corpus: architecture docs, ADRs, rules
files (`.claude/rules/`, `.cursor/rules/`, `.agents/rules/`, `.codex/rules/`,
`.github/instructions/`), agent guides (CLAUDE.md / AGENTS.md /
CONTRIBUTING.md), shallow READMEs, `.mmd` diagram inventory, pre-commit hook
ids + entries, arch-lint scripts, and the git default/current branch. Its `Notes`
section says what's ABSENT — that determines which severity ladder applies
(see Output Format).

## Scope Resolution

Determine what to review from `$ARGUMENTS`, using the **discovered default
branch** (never a hardcoded `main`):

- **Empty / no args**: uncommitted changes (`git diff HEAD`)
- **A file or directory path**: all source files under that path
- **A number**: PR/MR — `git diff <default_branch>...HEAD`, or `gh pr diff` /
  `glab mr diff` where available
- **`--staged`**: staged changes only (`git diff --cached`)

Collect the list of changed/target files for analysis.

## Context Loading

Read EVERY file the scanner listed under "Read these before reviewing" —
agent guides, all rules files, architecture docs, and the ADR index if one
exists — ONCE, before reviewing. Do not cherry-pick: a rules file you skip
is a rule you can't enforce.

If the scanner found arch-lint scripts (e.g. `scripts/arch_review.py`),
run them in advisory mode against the scope and fold their findings into the
verdict table — they encode the mechanical subset of the rules; your job is
the intent-level layer above them. If pre-commit hooks reveal
architecture-related gates, note that passing them is necessary but not
sufficient.

If the corpus says which of its decisions bind (ADR statuses such as
ratified, draft or superseded), keeps a register of known deviations, or
sets its own checks, severity scale or report format, follow it. Findings
come only from binding rules; a non-binding one gives at most an advisory
note. A finding that matches a registered deviation is reported as known,
not new, unless the change extends it. The review never edits the
register: it lists proposed rows for the register's owner. The corpus's
own severity scale and report sections replace the ladders and table below.

## Deriving the review checks

From the loaded corpus, extract four check families. Every finding MUST cite
the document (and section) that establishes the rule it violates:

1. **Boundary / layer rules** — which modules may import which; which
   directions are one-way; which components must stay ignorant of which
   others.
2. **Protocol / contract rules** — interfaces every unit of a given kind
   must implement; required files per unit; base classes that must be used
   instead of copy-paste.
3. **Idiom rules** — logging, configuration, prompt placement, lazy loading,
   naming, file-size ceilings — whatever the corpus pins as "the way".
4. **Placement rules** — which directory a file of each kind belongs in,
   where tests mirror to, and single-consumer checks for shared layers
   (a "shared" module with exactly one consumer should live with its
   consumer).

Then evaluate every file in scope against each family. Review the INTENT,
not just the letter — an import that technically passes a mechanical
checker can still put domain knowledge where the corpus says it must
not live.

## Output Format

Present findings as a verdict table, each row citing its source rule:

```
| File | Issue | Severity | Source rule | Fix |
|------|-------|----------|-------------|-----|
| shared/foo.py | Single-consumer logic in shared layer | HIGH | CLAUDE.md "shared/" | Move beside its consumer |
| core/app.py | Imports a provider client directly | CRITICAL | architecture.md layering | Remove; route via its interface |
```

**Severity — documented-corpus ladder** (applies when the scanner found
architecture docs or rules):

- **CRITICAL**: violates a documented boundary or layer rule
- **HIGH**: violates a documented protocol/contract or config convention
- **MEDIUM**: violates a documented idiom (naming/logging/lazy-loading), or
  an industry convention the corpus is silent on (SRP, dependency direction,
  dead code)
- **LOW**: style or documentation gaps

**Severity — generic fallback ladder** (the scanner's Notes say no
architecture docs/rules exist): CRITICAL = cyclic dependencies,
cross-module reach-through into private internals, secrets/config
hardcoded in code; HIGH = contradicts anything the repo DOES document
(README, CONTRIBUTING); MEDIUM = industry-convention breaks; LOW = style.
In this mode the report MUST open with: *"No documented architecture was
found — findings below derive from generic principles. Consider writing
an architecture.md so future reviews can enforce YOUR rules."*

End with a summary: `X files reviewed, Y issues found (Z critical, W high)`.

If no issues found: `All files pass architectural review.`

## See also

- `scripts/discover_context.py` — the corpus scanner (also useful alone:
  `--format json` for tooling).
- `dev-spec-verify` — verifies a SPEC against the code; this skill verifies
  the code against the ARCHITECTURE. Run both before landing a large batch.
- `dev-refactor-module` — the fix-it follow-on for MEDIUM idiom findings
  concentrated in one module.
