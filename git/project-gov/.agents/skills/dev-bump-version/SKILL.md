---
name: dev-bump-version
description: Bump the app version per the repo's documented cadence (retroactively if forgotten) or on demand — validates against the current state, refuses random jumps and backward moves, and updates the changelog and every version file in one pass.
argument-hint: <empty for the default, "now" for force-bump, "minor" or "major" where no cadence is documented, or "x.y.z" for explicit target>
allowed-tools: Read, Glob, Grep, Bash, Edit
user_invocable: true
---

# Bump version

Take the running app's version forward by one or more cadence windows
(or by one patch on request, where the repo documents no cadence),
producing a new changelog entry per window and updating the
single-source-of-truth version file.

The skill **never jumps versions**.  Every bump is exactly +1 patch
from the current version, +N when N full cadence windows have
elapsed since the last release, or the next minor / major when the user
names it where the repo documents no cadence.  Random version targets are rejected
with a pushback message that explains what the natural next would be.

## Portability

Tool names are Claude Code's. Elsewhere use the equivalent and keep every gate. AskUserQuestion: ask in chat and wait. Explore agents: subagents, else sequential reads. Worktree isolation: `git worktree add`. The ARGUMENTS placeholder (with a leading `$`): the text after the skill name. `/dev-x`: your invocation of dev-x. Other `dev-*` skills are optional; if absent, do the step here, never skip it.

## Hard rules

1. **Never jump.** Versions are sequential.  Asking for `1.0.10`
   when current is `1.0.7` is rejected unless 3 full windows have
   elapsed since the last release.  The suggested fix is to run
   with no args and let the cadence catch up.  Where the repo documents
   no cadence, the next patch is the only valid patch target.
2. **Never go backwards.** Asking for a version `<= current` is
   rejected with "already released, see `<changelog>`".
3. **Never re-date released entries.** Existing `<changelog>`
   entries are immutable.  New windows append at the top of the
   entry list (after the header).
4. **Never push.** The skill ends with "next steps: commit + restart".
   `git push` is never invoked.
5. **Never auto-commit.** The user reviews the diff and runs the
   suggested `git commit` themselves.
6. **No major / minor bumps unless named.** This skill only moves the
   patch digit by default.  Where the repo documents a cadence, major /
   minor bumps are out of scope; do them by hand and then run this skill
   for the patch sequence.  Where it documents none, `minor` or `major` is
   accepted only when the user names it explicitly.

## Procedure

### 1. Read current state

First establish the repo's release setup from its release doc (look in
the agent guides, `CONTRIBUTING.md`, and `docs/`), release scripts, and CI:

- **Version files:** the single source of truth (such as a `<version file>`
  file or a manifest's version field) plus the files the doc bumps with
  it.  A doc's `git add` or `git diff` list is good evidence.  Don't build
  this list by searching for the version string: lockfiles, tests, and
  unrelated manifests match too.  If the version comes from git tags, read
  the latest tag as `current_version`, skip the file edits below, and add
  the tag command to the hand-off.
- **Changelog:** its path and entry format.  With none, say so and ask
  whether to start one with this entry.
- **Cadence:** whether the repo documents one ("every two weeks",
  "2-week", a generator's window constant).  Read its length `N` in days;
  a generator's value wins if it disagrees with the prose.  No documented
  cadence means `cadence = none`.
- **Generator:** the command that regenerates the changelog, if any.

Then:

- Read the source of truth → `current_version` (e.g. `1.0.7`)
- Parse the latest entry header from `<changelog>` — the first
  line matching `^## \[` that names a version (skip an `[Unreleased]`
  section), or the repo format's equivalent — extract `latest_entry_version` and
  `latest_entry_date`
- Sanity check: `current_version` and `latest_entry_version` must
  match.  If they don't, abort with a "VERSION and CHANGELOG are
  out-of-sync; reconcile manually" message.  Never proceed.

### 2. Compute cadence

```bash
today=$(date +%Y-%m-%d)
# days_since = $today - $latest_entry_date  (use python -c if shell math is awkward)
# due_bumps = days_since // N
```

`due_bumps` is the count of full `N`-day windows that have completed
since the last release.  Skip this step when `cadence = none`.

The "natural next version" is `current_version` with the patch digit
bumped by `due_bumps`.  E.g. current `1.0.7`, `due_bumps=2`, natural
next `1.0.9`.  With `cadence = none`, it is `current_version` with patch+1.

### 3. Validate the user's input

With a documented cadence:

| Input | Rule |
|---|---|
| **(empty / no args)** | If `due_bumps == 0`: pushback "recently released".  If `due_bumps >= 1`: bump by `due_bumps`. |
| **`now` / `--force`** | If `due_bumps >= 1`: just take the natural cadence (no force needed); fall through to default path.  If `due_bumps == 0`: append a new entry dated today, bump patch by 1.  Use the on-demand path below. |
| **`x.y.z`** | Compute `target_steps = patch(x.y.z) - patch(current_version)`.  If `target_steps <= 0`: reject "behind current".  If `target_steps > due_bumps`: reject "skipping versions".  If `target_steps < due_bumps`: reject "behind cadence — run with no args to take all due bumps".  If `target_steps == due_bumps`: do it. |
| **`minor` / `major`** | Reject as out of scope (hard rule 6). |

With `cadence = none`:

| Input | Rule |
|---|---|
| **(empty / no args), `now` / `--force`** | Bump patch by 1.  Use the on-demand path below. |
| **`minor` / `major`** | Named explicitly, so allowed: bump that digit by 1 and reset the lower digits.  Use the on-demand path below. |
| **`x.y.z`** | Must be exactly the next patch, next minor, or next major.  If `x.y.z <= current`: reject "behind current".  Otherwise, if it is none of those three: reject "skipping versions, no cadence". |

#### Pushback message templates

Quote `current_version`, `latest_entry_date`, and the offending arg
verbatim so the user can see what's wrong without reading code.

**Recently released (`due_bumps == 0`, no args):**
> Current is **{current_version}** dated **{latest_entry_date}** —
> only {days_since} days ago.  Bumps run on a {N}-day cadence; no
> windows have completed yet.  Wait until day {N}, or pass `now`
> to force an immediate hotfix bump.

**Behind current (`x.y.z <= current`):**
> **{user_version}** is behind current **{current_version}**
> (already released on {latest_entry_date}).  See <changelog>.
> If you meant to take the next bump, run with no arguments.

**Skipping versions (`x.y.z > natural_next`):**
> Asked for **{user_version}** but only **{due_bumps}** windows
> have completed since {latest_entry_date}.  The natural next is
> **{natural_next}**.  Run without arguments to take the full
> cadence, or wait for additional windows to complete.

**Major / minor with a documented cadence:**
> This repo bumps patches on a {N}-day cadence, so **{arg}** is out of scope
> here.  Do it by hand, then run this skill for the patch sequence.

**Skipping versions, no cadence (`x.y.z` is not the next patch, minor, or major):**
> Asked for **{user_version}** but the next versions are
> **{next_patch}**, **{next_minor}** and **{next_major}**.  Versions are
> sequential: pick one of those, or run without arguments for the next patch.

**Behind cadence (`current < x.y.z < natural_next`):**
> Asked for **{user_version}** but **{due_bumps}** windows are
> due (cadence next is **{natural_next}**).  Bumps must take the
> full cadence — run without arguments.

**Out-of-sync (`current_version != latest_entry_version`):**
> {version_file} reads **{current_version}** but the latest <changelog>
> entry is **{latest_entry_version}** dated {latest_entry_date}.
> Reconcile manually before bumping; the skill won't proceed
> against an inconsistent state.

### 4. Apply the bump

#### Default cadence path (`due_bumps >= 1`, target == natural_next)

The repo's generator handles this idempotently, where it has one.
Read what it changes, then run the command its release doc gives:

```bash
<repo's changelog generator>
```

If reading it shows it would drop an `[Unreleased]` section, rewrite released
entries beyond what its docs describe, or overwrite uncommitted changelog
edits, stop and report that instead of running it.

The generator regenerates the changelog and the version files in one
pass.  Read the diff to confirm:
- Existing entries are unchanged, **except** where the repo's release
  doc or generator documents a one-time date correction (for example,
  the previously-latest entry's date shifting forward from a
  clipped-to-today date to its natural window-end date after an
  initial retroactive seed).
- N new entries appear at the top, dated at the natural window-end
  for each completed window, with versions
  `current_version + 1`, …, `natural_next`.

If the diff doesn't match, stop and report the mismatch.

With no generator, run the on-demand steps below once per due window,
dated at each natural window-end.

#### On-demand path (`now` with no due cadence, or `cadence = none`)

A generator can't manufacture a release inside an in-progress
window — it works on full window boundaries.  Do the bump manually
in five steps:

1. **Compute next version.**
   - If the release doc pins a version line (such as one major.minor
     per era), stay in it.
   - `next_version = current_version` with patch+1, or the named minor
     / major with the lower digits reset.

2. **Collect commits since the last entry.**
   ```bash
   git log --no-merges \
       --since="{latest_entry_date} 00:00:00" \
       --until="now" \
       --format="%H|%cs|%s"
   ```
   Drop subjects matching `^(wip|fixup|tmp|squash|drop|debug)\b`
   (case-insensitive).

3. **Bucket by section** using the repo generator's map if it has one, otherwise this one:

   | Prefix (case-insensitive, before the first colon) | Section |
   |---|---|
   | `feat`, `add` | Added |
   | `fix` | Fixed |
   | `refactor`, `rename`, `revert` | Changed |
   | `docs`, `doc` | Documentation |
   | `tests`, `test` | Tests |
   | `chore`, `upd`, `rm` | Maintenance |
   | `docker`, `scripts`, `ci`, `build` | Build |
   | _untyped_ — fall through to keyword scan: `fix`/`bug`/`broken` → Fixed; `doc`/`readme` → Documentation; `test`/`spec` → Tests; `refactor`/`rename`/`move`/`extract` → Changed; `add`/`implement`/`introduce`/`create`/`new` → Added; otherwise → Other | (per scan) |

   Strip the recognised prefix when rendering the bullet (e.g.
   `feat: add X` becomes `add X`).  Append the short SHA in
   parentheses: `add X (a1b2c3d)`.

4. **Render the new entry** in the changelog's existing format, or Keep-a-Changelog if it has none:
   ```markdown
   ## [{next_version}] - {today}

   ### Added
   - …

   ### Fixed
   - …
   ```
   Skip empty sections.  Sections render in this order: Added,
   Changed, Fixed, Documentation, Tests, Build, Maintenance, Other.

5. **Patch the changelog and every version file** (use the `Edit` tool, not `Write`):
   - `<changelog>`: insert the new entry between the header and
     the previously-latest entry.  Use the previous-latest entry's
     `## [` line as the unique anchor for `old_string`.  Insert below any
     `[Unreleased]` section; where the repo's docs say it folds into the next
     release, move its content into the new entry.
   - A file holding only the version: replace contents with `{next_version}\n`.
   - A manifest or config file: change only the line that holds the
     release version, e.g. `version = "{current_version}"` to
     `version = "{next_version}"` in `pyproject.toml`.

### 5. Verify

After either path, run these as a sanity sweep:

```bash
cat <version file>
head -40 <changelog>
grep -E "version" <each other version file>
```

All must agree on the new version.

### 6. Hand off — never commit, never push

Surface the suggested next steps as a copy-pasteable block:

```bash
git add <version files> <changelog>
git commit -m "chore: release v{next_version}"
<the repo's restart or deploy command, if it has one>
```

## Anti-patterns

- ❌ Trusting the user's version arg without validation.  Always
  read <changelog> and `<version file>` first.
- ❌ Editing <changelog> entries that already exist.  New entries
  go at the top; previous entries are immutable except for the
  one-time clipped-to-natural date shift the generator does.
- ❌ Bumping major / minor unless the user named it and the repo documents no cadence.  Otherwise out of scope; do those by hand.
- ❌ Auto-committing or pushing.  Hand off; the user commits.
- ❌ Skipping the validation pushback.  The pushback exists to
  prevent the user from breaking the version sequence.
- ❌ Calling a generator with date-range flags to bypass the
  cadence.  That's what `now` is for.

## When to invoke

- "Bump the version", "release a patch", "do the biweekly bump",
  "let's tag a new version".
- After a full cadence window has passed since the last release.
- Hotfix scenarios — pass `now` or `--force`.

## When NOT to invoke

- The user is asking for a new **feature** (different intent — write
  the code first, bump after the cadence requires it).
- The user wants to roll **back** a version — use `git revert` and
  manually edit `<changelog>` to add an "Unreleased" or "Reverted"
  section.  This skill only moves forward.
- A feature branch isn't release-ready — the bump should land on
  the release branch, not a WIP branch.

## See also

- The repo's changelog generator, if any — the regeneration tool the
  default cadence path delegates to.
- The repo's release doc — the human-runnable version of this workflow
  (what a release engineer would do without the skill).
- `dev-group-and-commit` — the natural follow-on once the diff
  exists; turns the bump diff into a single `chore: release` commit.
