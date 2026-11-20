---
name: gov-code-sync
description: Clone the product repositories listed in workspace.toml beside the governance repo, keep them current with fast-forward-only pulls (skipping any repository with local changes), then refresh their code graphs (Graphify and GitNexus); ends with a status table. The pull is a STUB until tools/repos/sync.py is implemented; the graph refresh (tools/repos/scan.py) works today.
argument-hint: <empty for all repositories; a repository slug for one; "check" to report only>
user_invocable: true
---

# Keep the product repositories current

The digest, the reviews and `dev-spec-verify` read the **code itself** in the workspace's `git/` folder, because tickets and documents are only claims. This skill keeps those clones current without ever touching anyone's work.

> **Status: stub.** `tools/repos/sync.py` documents its full contract and exits 2 until it is implemented. Until then, do the same by hand with plain `git` commands, keeping every rule below.

## Steps (once implemented)
1. Run `py -3.12 tools/repos/sync.py --check` and show the table: each repository's branch, how far it is ahead or behind, whether it is dirty, and the last commit.
2. For a missing repository, ask before cloning it (`url` comes from `workspace.toml`).
3. Run `py -3.12 tools/repos/sync.py`, which fetches and then fast-forwards only.
4. Report the final table, and list anything skipped and why.

## Then refresh the code graphs (works today)
5. Run `py -3.12 tools/repos/scan.py`. For this repository and each clone, it refreshes the Graphify graph (`graphify-out/`, an AST pass with no language model) and the GitNexus index (`.gitnexus/`, with no files injected). It keeps both out of Git.
6. Report its table: each graph is fresh, stale or missing, and any tool that is not installed. From here on, agents answer code questions from these graphs (`AGENTS.md`, "Code intelligence").

## Hard rules
- Fast-forward only. Never merge, rebase, reset, stash or force-push.
- Skip any repository that has local changes, a detached HEAD or a diverged branch, and report it.
- Run one repository at a time, with no interactive prompts (stdin closed).
