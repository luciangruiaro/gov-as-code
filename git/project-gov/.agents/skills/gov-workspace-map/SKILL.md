---
name: gov-workspace-map
description: Keep WORKSPACE.md and the shared drive's INDEX.md true. Regenerates the tree and the index, then compares the map's prose with the disk and workspace.toml (repositories, drive folders, flows) and proposes edits.
argument-hint: <empty; or "check" to report only>
user_invocable: true
---

# Keep the workspace map current

[`WORKSPACE.md`](../../../WORKSPACE.md) is how people and agents find anything, and a wrong map is worse than none. A tool generates its tree, `shared/INDEX.md` lists the drive's files, and people keep the prose.

## Steps
1. **Generate.** Run `py -3.12 tools/workspace/index.py`, or with `--check` if the argument is "check". If the shared drive is not linked in, report it with the link command from WORKSPACE.md section 5, and stop.
2. **Compare the prose with the disk.**
   - Section 4: every `[[repo]]` in `workspace.toml` is in the repositories table, every repository in it exists in `../` (or is noted as not cloned yet), and each product repository's agent file has a `## Governance` block.
   - Section 5: every top-level drive folder is in the folders table, with nothing listed that is not on the drive.
   - Section 6: the flows' tools exist in `tools/`, and the stub status is still true.
   - Section 7: every path given in "Looking for… → go to" exists.
3. **Propose edits** as a short list of the line, the problem and the fix. Apply them once the user agrees, and set the **Refreshed** date at the top.
4. Run `py -3.12 tools/workspace/index.py --check` and the tests, then report.

## Hard rules
- Never hand-edit between the `TREE` markers or inside `INDEX.md`: they are generated.
- The map describes the current state only. History is in Git.
- Only names of roles go in WORKSPACE.md. Names of people belong on the drive, in `Team/`.
