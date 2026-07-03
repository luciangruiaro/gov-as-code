---
name: dev-refactor-module
description: Systematically refactor a module for its language's style rules, clean code, and modularity, through ten ordered quality passes (written for Python, applied by intent elsewhere)
argument-hint: <folder-path>
allowed-tools: Read, Edit, Write, Glob, Grep, Bash
---

# Refactor Module

Systematically refactor all source files in `$ARGUMENTS` to enforce the language's style
rules (PEP 8 for Python), clean code, modularity, and modern best practices.

The passes are written for Python. In another language, apply each pass's **Elsewhere** line
using the repo's own tooling, and mark a pass with no equivalent as N/A in the summary.

## Portability

Tool names are Claude Code's. Elsewhere use the equivalent and keep every gate. AskUserQuestion: ask in chat and wait. Explore agents: subagents, else sequential reads. Worktree isolation: `git worktree add`. The ARGUMENTS placeholder (with a leading `$`): the text after the skill name. `/dev-x`: your invocation of dev-x. Other `dev-*` skills are optional; if absent, do the step here, never skip it.

## Scope Rules

- **Only** modify files inside `$ARGUMENTS`. Never touch files outside that path.
- Shared utilities extracted during deduplication go into a `common.py` or `utils.py`
  **within** the target folder — never into a parent or sibling package.
- Imports from outside the target folder (e.g. `config`, `core`, shared modules) stay unchanged.
- If a shared utility already exists in the repo's shared or core modules (found in Scan), **import it** — do not create
  a local copy.

## Procedure

### 1. Scan

Use Glob to list every source file under `$ARGUMENTS` (Python: `$ARGUMENTS/**/*.py`). Read each file and note:
line count, existing type hints, imports, docstrings, logging usage, Pydantic patterns,
hardcoded constants, duplicated helper methods.

Also find the repo's shared and core modules, its established logger (the one most modules
already import), and its config mechanism, so later passes reuse them.

Also scan for:
- Any `config.yaml` already present in the target folder
- Any static methods that duplicate project shared helpers (see Pass 10)
- Any hardcoded lists, dicts, thresholds, or regex patterns that should be in config

### 2. Apply Quality Passes (in order)

Execute these passes sequentially on every file within scope:

#### Pass 1 — Type Hints (PEP 484)

- Add parameter and return type annotations to **all** functions and methods.
- Use `typing` module types: `Dict`, `List`, `Optional`, `Any`, `Union`, `Callable`, etc.
- For FastAPI route handlers, add response type annotations (`-> JSONResponse`, `-> HTMLResponse`, etc.).
- For async generators, use `AsyncGenerator[YieldType, SendType]`.
- **Elsewhere:** add the type information the language and repo support.

#### Pass 2 — Pydantic v2 Migration

Applies only where the repo is on Pydantic v2; otherwise N/A.

- Replace all `.dict()` calls with `.model_dump()`.
- Replace deprecated `class Config:` inner classes with `model_config = ConfigDict(...)`.
- Ensure mutable or computed defaults use `Field(default_factory=...)` instead of bare expressions
  (e.g. `created: int = int(time.time())` is a bug — it evaluates once at import).
- Import `ConfigDict` and `Field` from `pydantic` as needed.
- **Elsewhere:** replace APIs deprecated in the framework versions the repo already uses.

#### Pass 3 — Logging Consistency

- Replace `print()` calls used for debug/info output with `logger.debug()` or `logger.info()`.
- Use the project's established logger (found in Scan).
- Never silently swallow exceptions (`except Exception: pass`). At minimum log them.
- **Elsewhere:** same rule, for the language's debug-print calls and empty catch blocks.

#### Pass 4 — Docstrings

- Add concise docstrings to all public functions, classes, and modules: the repo's style, or Google-style if it has none.
- One summary line, plus `Args:` / `Returns:` sections only when parameters are non-obvious.
- Do **not** add docstrings to trivial `__init__.py` re-exports.
- Keep comments concise — explain *why*, not *what*.
- **Elsewhere:** the language's doc-comment format, same rules.

#### Pass 5 — Unused Imports

- Remove any imports that are not referenced anywhere in the file.

#### Pass 6 — Pydantic Field Descriptions

Applies only where the repo uses Pydantic; otherwise N/A.

- Add `Field(description="...")` to Pydantic model fields, especially on public-facing API schemas.
- Keep descriptions short and factual.
- **Elsewhere:** add descriptions to public schemas in the repo's schema library, if it has one.

#### Pass 7 — Code Deduplication

- Identify functions or logic blocks duplicated **within** the target folder scope.
- **Before extracting** a new local `common.py`, check if the function already exists in
  the project's shared modules (found in Scan).
- If a shared utility exists, **import it** instead of creating a local duplicate.
- Only extract into a local `common.py` when the utility is genuinely specific to this module
  and does not exist anywhere in the project's shared modules.
- Use parameters or callbacks to handle minor variations between call sites.
- Do **not** extract code if the duplication is trivial (< 5 lines) or if merging
  would lose type safety (e.g. functions returning different Pydantic model types).

#### Pass 8 — Error Handling

- Replace bare `except:` with typed `except Exception as exc:`.
- Replace silent `except Exception: pass` with at minimum `except Exception as exc: logger.debug(...)`.
- Ensure consistent error response patterns within the folder.
- **Elsewhere:** catch the narrowest type the language allows; never leave a catch block empty.

#### Pass 9 — Config Externalisation

**Domain data and deployment-tunable values belong in the module's config, not in code.**

Move to config:
- Scenario lists, dimension lists, keyword lists, regex patterns, lookup tables
- Thresholds (e.g. `0.5`, `0.9`, `0.7`) — these should come from the config passed
  at init time, not be hardcoded
- Module paths and class names used for dynamic imports
- Supported dialect / DBMS / provider lists
- Any list or dict that an operator might want to change per deployment

Keep in code:
- Security invariants (hardcoded frozen allowlists that must NOT be overridable by config)
- String format templates for UI/log messages
- True compile-time constants (protocol versions, file extension literals)

If the repo keeps per-module config files and this module doesn't have one yet, create one
following that pattern (for example a `config.yaml` with a top-level key matching the module
name, loaded via `yaml.safe_load()` from the same directory as `__file__`). If the repo has no
such pattern, use its existing config mechanism; if it has none, keep named constants and
note that in the summary rather than introducing one.

**Elsewhere:** same rule, through the repo's config mechanism.

#### Pass 10 — Shared Helper Reuse

Scan all Python files in scope for locally reimplemented utilities that already exist
in project shared modules. Replace with imports.

Common duplications to detect (skip a row when the repo has no shared helper for it):

| Local pattern | Replace with |
|---|---|
| `_parse_llm_score()` static method | The repo's shared score parser |
| `_extract_response()` or inline `if hasattr(response, "content")` chains | The repo's shared response normaliser |
| Manual `yaml.safe_load` for loading prompt templates | The repo's shared prompt or template loader |
| JSON extraction from LLM markdown-fenced output | The repo's shared JSON extractor |
| `os.getenv()` / `os.environ[]` for config values | The repo's central config object, if it has one. Direct `os.getenv` is only acceptable for infrastructure vars not expressed in any config file. |
| Inline LLM result polishing prompts | The repo's shared polishing helper |

Use Grep to search for these patterns across the target folder before editing.
If a pattern is found, replace the local implementation with the shared import.

### 3. Verify

After all edits, run a syntax check on every modified file (elsewhere, the compiler's or
type checker's no-emit mode):

```bash
python -c "import ast; ast.parse(open('<file>').read())"
```

Report any failures immediately and fix them before continuing.

### 4. Summary

Output a markdown table with columns: **File**, **Changes Made**, **Lines Before → After**.
List any pass that was N/A below the table.
