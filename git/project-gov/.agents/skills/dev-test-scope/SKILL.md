---
name: dev-test-scope
description: Assess, create, or enhance tests for a named code area following TDD patterns
argument-hint: <path or component description>
allowed-tools: Read, Edit, Write, Glob, Grep, Bash, Agent
user_invocable: true
---

# Test Scope

Assess test coverage for a code area, then create or enhance tests as needed.

The examples below use Python and pytest. In another stack, use the repo's test
framework and its equivalents (test functions, fixtures, exception assertions);
keep the same inventory, quality checks, and report.

## Portability

Tool names are Claude Code's. Elsewhere use the equivalent and keep every gate. AskUserQuestion: ask in chat and wait. Explore agents: subagents, else sequential reads. Worktree isolation: `git worktree add`. The ARGUMENTS placeholder (with a leading `$`): the text after the skill name. `/dev-x`: your invocation of dev-x. Other `dev-*` skills are optional; if absent, do the step here, never skip it.

## Context Loading

Read the repo's testing rules or docs (such as `.claude/rules/testing-standards.mdc`
or `CONTRIBUTING.md`), nearby tests, and its CI config to understand:
- TDD workflow (write failing test first, implement minimum, run suite)
- Test file organization (often a mirror `tests/` structure)
- Fixture patterns and naming conventions
- Available test commands

## Scope Resolution

Parse `$ARGUMENTS` to determine what to test:

1. **Path given** (e.g., `src/billing/invoices/`):
   - Glob for all source files under that path (Python: `.py`)
   - Identify the test directory the repo's convention gives (e.g., the mirror `tests/billing/invoices/`, or colocated tests)

2. **Component name** (e.g., "the retry watchdog"):
   - Grep the codebase to locate the component
   - Identify the source file(s) and their test mirror

3. **"uncommitted"** or empty:
   - Run `git diff --name-only HEAD` to find changed files
   - Focus on those files' tests

## Analysis Phase

For each source file in scope:

### 1. Inventory Functions

Read the source and list every public function/method:
```
module.py:
  - class Foo:
    - __init__(self, ...)
    - do_work(self, x, y) -> str    [TESTED]
    - handle_error(self, e)         [UNTESTED]
  - helper_func(a, b)               [UNTESTED]
```

### 2. Find Existing Tests

Check the test path found above. For each test file:
- List test classes and methods
- Map each test to the source function it covers
- Identify source functions with NO corresponding test

### 3. Assess Quality

For existing tests, check:
- Are assertions meaningful (not just `assert True`)?
- Are edge cases covered (empty input, None, boundary values)?
- Are error paths tested (`pytest.raises`, exception branches)?
- Are mocks appropriate (not over-mocking implementation details)?

## Action Phase

### For untested functions:

Write tests following the project pattern (Python example):
```python
class TestFunctionName:
    def test_happy_path(self):
        """GIVEN valid input WHEN function called THEN expected output."""
        ...

    def test_edge_case(self):
        """GIVEN edge input WHEN function called THEN handles gracefully."""
        ...

    def test_error_case(self):
        """GIVEN invalid input WHEN function called THEN raises/returns error."""
        ...
```

### For weak existing tests:

Add missing edge cases, strengthen assertions, remove redundant tests.

### Rules

- **Do NOT mock** internal implementation details — mock external boundaries only
  (HTTP calls, database, file I/O, LLM calls)
- **Do NOT add** tests for trivial getters/setters or `__init__` unless they
  contain logic
- Use the project's fixtures (Python: `pytest` fixtures from the project's `conftest.py` files)
- Put tests where the repo's convention puts them; in a mirror layout, source `src/X/Y.py` -> test `tests/X/Y/test_Y.py`

## Verification

After writing/editing tests:

```bash
# Run just the scope's tests with the repo's runner (Python: pytest <test_directory> -v --tb=short)
<test runner> <test_directory>

# If any fail, fix the test (not the source!) unless the source has a real bug
```

## Report

Output a summary:

```
## Test Coverage Report for <scope>

| Source File | Functions | Tested | Added | Enhanced |
|-------------|-----------|--------|-------|----------|
| foo.py      | 5         | 3      | 2     | 0        |
| bar.py      | 3         | 3      | 0     | 1        |

**New tests written:** 2
**Existing tests enhanced:** 1
**All tests passing:** Yes
```
