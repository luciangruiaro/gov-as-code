---
name: dev-install
description: Install and bootstrap this repository on a fresh Windows or macOS machine — detects what's present, asks before installing, prefers user-scoped reversible installers, walks .env interactively, brings up the local stack, smoke-tests the app. Never installs silently.
argument-hint: <empty for full guided install, or one of "check" | "deps-only" | "env-only" | "stack-only" | "smoketest">
allowed-tools: Read, Glob, Grep, Bash, PowerShell, Edit, Write, AskUserQuestion
user_invocable: true
---

# Install this repository locally

Take a brand-new workstation (Windows or macOS) from "fresh checkout"
to "demo-ready running stack" without trampling the user's
environment.

The skill is **interactive by design**.  Every install asks consent
first, presents options, and prefers gentle (user-scoped, reversible)
install paths.  The user's existing tools are detected and re-used,
never replaced.

## Portability

Tool names are Claude Code's. Elsewhere use the equivalent and keep every gate. AskUserQuestion: ask in chat and wait. Explore agents: subagents, else sequential reads. Worktree isolation: `git worktree add`. The ARGUMENTS placeholder (with a leading `$`): the text after the skill name. `/dev-x`: your invocation of dev-x. Other `dev-*` skills are optional; if absent, do the step here, never skip it.

## Hard rules

1. **Never install anything without consent.** For each missing
   prereq, present at least two options (recommended + alternative)
   and a "skip + here's what breaks" path.  Wait for the user's pick
   before running any installer.
2. **Prefer user-scoped, reversible installers.** Mac: Homebrew /
   pyenv / nvm.  Windows: winget / scoop / nvm-windows / pyenv-win.
   Avoid `sudo` paths; avoid replacing system Python or system Node.
3. **Never use `--no-verify` or `--force` on any installer flag**
   that bypasses safety checks.  If a step fails, surface the error
   and ask the user, don't silently work around it.
4. **Never take credentials through the chat, and never echo them.**
   In the .env walkthrough the user types secrets straight into `.env`,
   and the skill acknowledges they were stored — never reads or quotes
   the value in the chat.
5. **Always provide rollback.** Track every tool installed in this
   session and show the user the uninstall command for each at the
   end.
6. **Never commit or push anything.**  The skill ends with the dev
   stack running locally; the user starts feature work from there.

## Scope flag

`$ARGUMENTS`:

| Value | Behaviour |
|---|---|
| _empty_ | Full guided flow: prereqs → install missing → .env → stack → smoketest. |
| `check` | Audit only — what's installed, what's missing, what would happen.  No installs, no edits. |
| `deps-only` | Stop after prereq install + repo bootstrap (locked dependency install, pre-commit). |
| `env-only` | Skip prereqs.  Just walk through `.env.example` and fill in `.env`. |
| `stack-only` | Skip prereqs + .env.  Just bring up the local stack + run migrations + smoketest. |
| `smoketest` | Only verify the running app, using the checks the repo documents (such as a health route). |

## Procedure

### 1. Detect OS + shell

Use Bash on macOS/Linux, PowerShell on Windows.  Detect:

```bash
# macOS / Linux
uname -s         # Darwin / Linux

# Windows
$PSVersionTable.OS  # Microsoft Windows ...
```

If on Linux, treat it as macOS-equivalent (Homebrew + pyenv + nvm
all work on Linux).  If on Windows, switch to PowerShell tooling.

Cap the rest of the skill's tool selection to the OS-appropriate
shell — the skill is one or the other for the duration.

### 2. Audit prerequisites

If the repo ships a prerequisite checker (such as
`scripts/utils/check-prereqs.sh` / `.ps1`, or a check its README names),
read it to confirm it only reports, then run it:

```bash
# macOS / Linux
bash <repo's checker>.sh
```

```powershell
# Windows
powershell -ExecutionPolicy Bypass -File <repo's checker>.ps1
```

The checker reports each tool's installed-or-missing + version.
Capture its output and parse into a structured "needs-install" list.
With no checker, build the same list from the repo's runtime pins,
manifests, lockfiles, CI setup, and setup docs.

Required tools the skill cares about are only the ones this repo needs:

| Tool | Min version | Why |
|---|---|---|
| `git` | any modern | Already on most machines; should be there. |
| Language runtime (`python`, `node`, …) | From the pin (`.python-version`, `.nvmrc`, `pyproject.toml`, `package.json`) | Runs the app. |
| Package manager (`uv`, `npm`, `pnpm`, …) | From the lockfile, pin, or setup docs | Resolves dependencies. |
| `docker` + `docker compose` | From setup docs, if the repo has a compose file | Dev stack. |
| `pre-commit` | any, if the repo has `.pre-commit-config.yaml` | Lint gate. |

### 3. Present install options + ask consent

For each missing tool, use AskUserQuestion to surface the choice.
The recommended option is always the gentlest (user-scoped, no sudo,
clean uninstall).  The tables cover common tools; for anything else, take
the install command from the tool's current official docs and offer it
the same way.

#### macOS recommendations

| Tool | Recommended (gentle) | Alternative | Skip impact |
|---|---|---|---|
| Homebrew | `curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh \| bash` | _system pkg manager_ | Most other installs assume brew. |
| Python | `brew install python@<pinned>` | `pyenv install <pinned>` | Python code won't run. |
| uv | `curl -LsSf https://astral.sh/uv/install.sh \| sh` | `brew install uv` | Python deps can't be resolved. |
| Node | `brew install nvm && nvm install <pinned> && nvm use <pinned>` (per-project versioning) | `brew install node@<pinned>` | JS code can't build. |
| Docker | Docker Desktop (download + install manually — runs the repo's containers) | colima (lighter, no GUI, CLI-only) | Its services have to be installed natively; tests that need them skip. |
| pre-commit | `uv tool install pre-commit` | `brew install pre-commit` | Lint hook won't fire. |

#### Windows recommendations

| Tool | Recommended (gentle) | Alternative | Skip impact |
|---|---|---|---|
| winget | _ships with Win 10/11_ | Install from MS Store | Most other installs assume winget. |
| Python | `winget install Python.Python.<pinned>` | `choco install python --version=<pinned>` | Python code won't run. |
| uv | `powershell -c "irm https://astral.sh/uv/install.ps1 \| iex"` | `winget install --id=astral-sh.uv` | Python deps can't be resolved. |
| Node | `winget install CoreyButler.NVMforWindows` then `nvm install <pinned> ; nvm use <pinned>` | `winget install OpenJS.NodeJS.LTS` | JS code can't build. |
| Docker | Docker Desktop for Windows (download + install manually) | _no good lighter alternative on Windows_ | Its services have to be installed natively. |
| pre-commit | `uv tool install pre-commit` | `winget install --id=pre-commit.pre-commit` | Lint hook won't fire. |

Wrap each install with:

1. AskUserQuestion: "I want to install <tool> via <recommended-method>.
   Alternative: <alternative>.  Skip: <consequence>.  Proceed?"
2. If approved, run the install.
3. On success, log the tool to a "rollback" list (what to show at the
   end).
4. On failure, surface the exact stderr to the user; offer to retry,
   pick the alternative, or skip.

Big installs (Docker Desktop) link the user to the download page
rather than scripting them — the GUI installer needs admin rights and
human consent, and installing it silently violates the user's trust.

### 4. Repo bootstrap

Once prereqs land, run the in-repo bootstrap: the script or commands
its README or `CONTRIBUTING.md` name.  Read a script before running it.
With none, run the locked install for each manifest, for example:

```bash
uv sync --locked              # Python with uv.lock
npm ci                        # Node with package-lock.json
pre-commit install            # if the repo has .pre-commit-config.yaml
pre-commit run --all-files
```

This:
- Resolves deps from the lockfile (idempotent, reproducible).
- Installs the pre-commit hook (so the user's first commit fires the
  lint gate).
- Runs the hook against the whole tree once — confirms a green local
  baseline.

Then build any frontend the repo's docs or Dockerfile say must be built
first, using its documented commands.

If a build fails on an old runtime, surface the version mismatch
and offer to bump via the version manager.

### 5. .env walkthrough — interactive + safety-aware

This is the most sensitive step.  The user is providing real
credentials (Jira API tokens, GitHub PATs, OpenRouter keys, etc.) in
exchange for a working local demo.

If the repo has no `.env.example` or equivalent, skip this step.

**Check first:** `.env` (or the repo's equivalent local file) must be
git-ignored and not tracked.  If it isn't, stop and report that before
any value is entered.  If it doesn't exist, copy `.env.example` to it, so
the user has a file to fill in.

**Open with the safety statement** before asking for any value:

> I'll walk through `.env.example` section by section.
> A few important notes:
>
> - You type credentials **directly into `.env`** in your editor.
>   `.env` is git-ignored, so it stays on this machine.
> - Please don't paste credentials into this chat: anything here
>   lives in the chat transcript.  I'll check that each one is set,
>   without reading its value.
> - You can hit "skip" on any non-essential value; the skill will
>   leave it unset and the related capability will simply be
>   disabled.
> - Required-for-boot values are: <the list found below>.  I'll
>   generate strong defaults for locally generated secrets if you
>   don't have any.

Read `.env.example` and parse it into sections (comment headers, where
the file uses them).  Walk section by section.

Find the required-for-boot values in the application's config
validation and startup scripts first, then `.env.example` comments and
setup or deployment docs.  Code wins when they disagree: a name found
only in docs may be stale, a secret can be required without appearing
in `.env.example`, and a placeholder shipped there may be refused at boot.

For each variable:

1. Show the variable name + the comment describing what it's for +
   any link to "where to get this token" (where the .env.example
   includes those URLs).
2. If `.env` already exists, show `set` or `missing` for the variable,
   never its value (treat existing values as a checkpoint — don't ask
   again unless the user wants to change it).
3. AskUserQuestion: provide it / skip / generate-strong-default
   (where applicable).
4. Write a non-secret value to `.env` immediately on response.  For a
   secret, wait until the user says it's saved.
5. Move to the next variable.

#### Required-for-boot defaults

If the user has no value to provide, generate one in the format the
application expects:

| Kind of value | Default generator |
|---|---|
| Random signing key | `python -c "import secrets; print(secrets.token_urlsafe(32))"` |
| Fernet key | `python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"` |
| Local database URL | Only if compose or config doesn't already supply it: match what step 6 starts (the service name inside compose, `localhost` from the host). |

Run these with whichever Python the repo uses (`uv run python`, `python3`,
`py -3`), and redirect the output straight into `.env`, so a secret never
lands in tool output or the chat.  For locally generated secrets, recommend the generated
default — there's no reason for a local demo to use a "real" one.
Roll a fresh value per install.

#### Sensitive sections (Jira, GitHub, etc.)

For Atlassian/GitHub/etc. tokens:

1. Acknowledge: "This is a credential.  See note above re. chat
   transcripts."
2. Ask the user to type the token into `.env` and say when it's saved.
3. Check only that the variable is set, without printing it.
4. Confirm in chat as: `"ATLASSIAN_API_TOKEN is set in .env"` — never
   echo the value itself.

#### Optional sections

Values not found to be required above, such as LLM provider keys (OpenAI, OpenRouter, Anthropic, Gemini), MCP
endpoints, integration credentials (Slack, Notion, Confluence,
Google Drive) — present each as a yes/skip question.  Skipping
disables the corresponding capability but doesn't break boot.

### 6. Bring up the stack

Once `.env` is in place, start the local target the repo documents:
its README, `CONTRIBUTING.md`, or task runner says how.  For example:

```bash
docker compose up -d --build
```

Read the compose file or script first, so you can say what it pulls,
builds, migrates, and seeds, and confirm any database it touches is
local.

Health-check the stack, using the health route the repo defines:

```bash
# Wait up to 60s for the app to become healthy
for i in {1..60}; do
    curl -fs <local-url>/<health-route> > /dev/null && break
    sleep 1
done
curl -s <local-url>/<health-route>
```

On Windows PowerShell, use `curl.exe`.  A CLI or library has no route: run
its documented smoke command instead.

If health-check times out, surface the service's recent logs (for a
container, `docker compose logs <service> --tail 50`)
to the user and ask them to paste relevant errors back.

### 7. Smoke-test in the browser (or CLI)

Print a "you're done" block:

```
✓ App running on <local-url>
✓ Health endpoint: <local-url>/<health-route>
✓ UI or CLI entry point: <url or command>

Default admin credentials, if the repo seeds any (change immediately for a real demo):
  <where the repo documents them>

Next steps:
  - Open the app, log in, change any seeded admin password.
  - If you skipped any integrations, add them later by editing .env
    and restarting: <restart command>
  - Check the lint gate works: make a tiny edit + git commit;
    pre-commit should fire.
```

### 8. Print the rollback summary

List every tool installed during this session with its uninstall
command:

```
What I installed during this run:
  ✓ Homebrew              → /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/uninstall.sh)"
  ✓ Python 3.12 (via brew) → brew uninstall python@3.12
  ✓ uv                    → rm ~/.local/bin/uv ~/.local/bin/uvx
  ✓ Node 20 (via nvm)     → nvm uninstall 20  (and `brew uninstall nvm` if you also installed nvm)
  ✓ Docker Desktop        → drag from /Applications to Trash + sudo rm -rf ~/Library/Containers/com.docker.docker
  ✓ pre-commit            → uv tool uninstall pre-commit

The repo itself is just a directory — `rm -rf <repo>` is
sufficient to remove it.  Container data, if any, lives in Docker volumes,
removed by `docker compose down -v`.
```

## Anti-patterns

- ❌ Running `curl … | bash` without the user seeing the URL first.
- ❌ Modifying the user's PATH in `.bashrc` / `.zshrc` /
  `$PROFILE` permanently (let the installers handle their own
  PATH; print the relevant lines for the user to add manually if
  needed).
- ❌ Replacing system Python or system Node.  Use a version manager
  (pyenv / nvm) when the user already has a system version.
- ❌ Asking the user to paste credentials into the chat, or echoing
  them back after they're in `.env`.  Confirm only that they're set.
- ❌ Auto-committing the populated `.env` (it's gitignored, but
  double-check; never `git add .env`).
- ❌ Pretending the install succeeded when a step failed.  Surface
  the error verbatim.

## When to invoke

- "Help me set this up on a new laptop"
- "Onboard me onto this repo"
- "Install this locally"
- "I want to demo this — what do I need?"

## When NOT to invoke

- The user already has a working install and just wants to run a
  workflow.  Use `dev-bump-version` / `dev-doc-audit` / etc. for
  task-specific work.
- The user is deploying to production.  See the repo's deployment
  docs instead.
- The user is on Linux and prefers system package managers
  (`apt` / `dnf` / `pacman`).  This skill assumes Mac/Win; Linux is
  best-effort via the same Homebrew/pyenv/nvm flow.

## See also

- The repo's prerequisite checker and bootstrap script, if it has them
  — the audit and bootstrap this skill orchestrates.
- `.env.example` or its equivalent — the schema the .env walkthrough
  reads from.
- The compose file or task runner — defines the services brought up in
  step 6.
- `CONTRIBUTING.md` — what the user reads after onboarding completes.

## Open implementation questions for first run

These get pinned the first time the skill is invoked; subsequent
runs respect the previous choice (skip any this repo doesn't need):

1. **Docker preference** — Docker Desktop (heavy, GUI, fully
   supported) vs colima (Mac only, lighter, CLI).  Recommended:
   Desktop unless the user has a low-end machine.
2. **Node version manager** — nvm (Mac) / nvm-windows (Win) is
   recommended for project-scoped Node.  For users who only ever
   touch this one project, system Node via Homebrew/winget is fine.
3. **Python isolation** — `uv` handles venv per-project, so even
   the user's system Python can be used as the base interpreter.
   No need for pyenv unless they're juggling many Python versions.
4. **Pre-commit scope** — install via `uv tool` (project-scoped) or
   globally via `brew install pre-commit`?  Recommended: `uv tool`
   for tighter scoping.
