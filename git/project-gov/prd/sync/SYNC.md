# Syncing the master PRD, and reviewing the decisions it touches

The master PRD is a Word document on the shared drive, in `PRD/` ([`WORKSPACE.md`](../../WORKSPACE.md) section 5). The client reads, comments on and agrees it there. Its Markdown mirror sits in [`prd/`](../) under the Word file's own name with `.md`. Git keeps every synced version, so a diff shows exactly what changed. The mirror ends with a change log: one row per sync, with the date the Word file was saved, its version and what changed. The Word document stays the source: change it there, then sync. Never edit the mirror by hand.

```
Word PRD (shared drive) ──sync.py──▶ prd/<name>.md ──git diff──▶ impact.py ──▶ alignment worksheet ──gov-adr──▶ ADRs
        people edit               deterministic         what moved      which decisions          people decide        the law
```

When asked to sync the PRD, an agent follows these steps (the `gov-prd-sync` skill); so can a person. Run everything from the repository root. On macOS and Linux, use `python3` where this says `py -3.12`.

## 1. Convert
```
py -3.12 prd/sync/sync.py                        # convert the newest master and rewrite the mirror
py -3.12 prd/sync/sync.py --check                # only say whether the mirror is current (exit 1 if not)
py -3.12 prd/sync/sync.py --log "what changed"   # add a change-log row (step 5)
py -3.12 prd/sync/sync.py --source FILE          # convert another copy of the master
```
`sync.py` picks the newest `*Master*.docx` in `PRD/`: the highest version in the file name, then the latest saved. The folder and the pattern are in `workspace.toml` (`[shared]`, `[prd]`). It needs pandoc 3 or newer. It rewrites the mirror and its images in `prd/assets/master/`, keeps the change log, and prints the file it used along with any warning: tracked changes shown as accepted, comments left out, raw HTML left in the text. When the version in the Word file's name changes, the mirror is renamed with it and keeps its change log.

If it stops, report its message and stop. A master kept as a Google Doc (`.gdoc`) has no content on disk: download it as Word (File › Download › Microsoft Word) and pass that file with `--source`.

## 2. Read what changed
- Run `git status --short -- prd/`. If nothing is listed, the mirror was already current: say so and stop.
- `git diff --word-diff -- prd/` shows the change inside each line. Tables keep one row per line, so a changed requirement is one changed line.
- If the mirror was renamed (a new version), stage `prd/` first so Git pairs the old and new names: `git add -A -- prd/`, then `git diff --staged -M --word-diff -- prd/`. Staging is not committing; `git reset -q -- prd/` undoes it.
- Formatting-only changes, such as table padding after a pandoc upgrade, go in a commit of their own, apart from content.

## 3. Check it may go into Git
The mirror follows the hard rules ([`AGENTS.md`](../../AGENTS.md)). Read the new and changed text for:
- a person's name (committed files name roles);
- customer or end-user data;
- contract (SOW) text quoted word for word (cite sections only);
- links to private documents, credentials or tokens;
- conversion faults: a broken table, a missing image, an empty section, a warning from step 1.

Don't fix any of these in the mirror: the next sync would undo it. Report them so the Word document is corrected, and wait for the user's decision.

## 4. Find the decisions it touches
```
py -3.12 prd/sync/impact.py            # report: ids added, removed or changed, and every line that cites them
py -3.12 prd/sync/impact.py --write    # also start resources/audits/<date>_prd-adr-alignment.md
py -3.12 prd/sync/impact.py --base HEAD~1   # after the sync is committed: compare with the sync before it
```
`impact.py` takes the mirror as committed at `--base` (default `HEAD`, the last committed sync) and compares it with the mirror on disk. It collects the requirement ids on changed lines (`[prd] id_pattern`: `FR-`, `NFR-`, `GR-`, `CFG-`, `SM-`, `TRG-`, `OI-`). It then lists every line in `architecture/` and `resources/work/` that cites them (`[prd] cited_in`). The script is deterministic and edits nothing.

With `--write` it starts the **alignment worksheet**. Each changed id gets a question: *Before*, *After*, *Cited by*, *Decision needed*, *Options*, *Recommendation*, *Lands in* and a blank **Answer**. An agent may draft the Options and the Recommendation. Only the design authority writes an Answer. Once the questions are answered, the `gov-adr` skill lands them: it amends or supersedes ADRs, adds backlog entries, closes questions and proposes deviation rows. A sync itself changes only the mirror.

## 5. Log and report
Add the change-log row: `py -3.12 prd/sync/sync.py --log "…"`. Write one line on what changed, by id where there are ids, for example `FR-001 reworded; FR-005 added; OI-002 closed`. Then tell the user, in plain words:
- the file converted, its version and when it was saved;
- what changed, by id: added, removed or reworded, and status changes such as draft to agreed;
- what the change touches here: the worksheet from step 4, or "no decision cites a changed id".

## 6. Commit when asked
Stage the mirror (with a renamed mirror's old name), `prd/assets/master/` and the worksheet, nothing else. Message: `docs(prd): sync the master PRD to v0.2` (the version from the file name), with the change-log line as the body. Answering the worksheet and changing ADRs are separate commits (`docs(adr): …`).

<!-- SAMPLE:BEGIN (new-project.py drops this section with the samples) -->
## Try it on the sample
The skeleton ships a SAMPLE master PRD, built from [`../templates/sample-master-prd.md`](../templates/sample-master-prd.md), and its mirror. One decision, [ADR-002](../../architecture/decisions/ADR-002-sample-single-sign-on.md), cites `FR-001`, `NFR-002` and `OI-001`. To see the whole chain on a commit of your own:
```
git add -A && git commit -m "baseline"                     # impact.py compares with HEAD
# change the sample: reword FR-001, add an FR-005 row, delete the OI-002 row, then build v0.3
pandoc prd/templates/sample-master-prd.md -o "../../shared/PRD/Product Requirements Document (Master) - Project Name v0.3.docx"
py -3.12 prd/sync/sync.py                                   # renames the mirror to v0.3, keeps the change log
git add -A -- prd/ && git diff --staged -M --word-diff -- prd/   # FR-001 reworded, FR-005 added, OI-002 gone
py -3.12 prd/sync/impact.py --write                         # FR-001 changed → ADR-002; FR-005 added; OI-002 removed
```
<!-- SAMPLE:END -->
