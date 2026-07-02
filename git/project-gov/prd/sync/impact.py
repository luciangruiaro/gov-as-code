"""Show which decisions a PRD change touches: the deterministic step between a PRD sync and the decision review.

Usage: py -3.12 prd/sync/impact.py [--base REF] [--write [--date YYYY-MM-DD]]

Git is the time machine. After prd/sync/sync.py has rewritten the mirror, this script:
1. takes the mirror as committed at --base (default HEAD) with `git show`, found by the [prd] pattern in
   workspace.toml, so a mirror renamed for a new version is still compared with its predecessor;
2. compares it line by line with the mirror on disk. Requirement tables keep one requirement per line, so one
   changed requirement is one changed line. The banner and the change log are left out (they change on every
   sync), and whitespace or table-padding differences do not count as changes;
3. collects every requirement id ([prd] id_pattern) on a changed line and calls it added, removed or changed;
4. finds every line that cites each id in the decisions and the work ([prd] cited_in, less not_cited_in): ADRs,
   the ADR backlog, the open questions, plans and brainstorms.

It prints a Markdown report. With --write it also starts the alignment worksheet,
resources/audits/<date>_prd-adr-alignment.md: one question per changed id, with the decisions that cite it and blank
Options, Recommendation and Answer lines for a person or an agent to fill in. The gov-adr skill then lands the
answers in the decisions. This script never edits a decision: judgment stays with people.
"""
from __future__ import annotations

import argparse
import datetime as dt
import difflib
import fnmatch
import re
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))
from workspace import config  # noqa: E402  (tools/workspace/config.py)

BANNER = "> Mirror of the master PRD"
CHANGE_LOG = re.compile(r"^## Change log\n.*?<!-- /change log -->\n?", re.MULTILINE | re.DOTALL)
ADR_FILE = re.compile(r"\b(ADR-\d{3})\b")
AUDITS = ROOT / "resources" / "audits"


@dataclass
class Change:
    id: str
    kind: str                                   # added | removed | changed
    before: list[str] = field(default_factory=list)
    after: list[str] = field(default_factory=list)
    cited_by: list[tuple[str, int, str]] = field(default_factory=list)   # (path, line number, text)

    @property
    def lands_in(self) -> list[str]:
        """The ADRs that cite this id, then the other files, each once and in order."""
        adrs = [m.group(1) for path, _, _ in self.cited_by if (m := ADR_FILE.search(Path(path).name))]
        others = [path for path, _, _ in self.cited_by if not ADR_FILE.search(Path(path).name)]
        return list(dict.fromkeys(adrs + others))


def git(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run(["git", *args], cwd=ROOT, capture_output=True, encoding="utf-8", errors="replace")


def previous_mirror(base: str, pattern: str) -> tuple[str | None, str]:
    """The mirror's path and text at base, or (None, "") when base has no mirror (or does not exist yet)."""
    if git("rev-parse", "--verify", "--quiet", f"{base}^{{commit}}").returncode:
        return None, ""
    listing = git("ls-tree", "-z", "--name-only", base, "prd/").stdout.split("\0")
    names = sorted(n for n in listing if n and fnmatch.fnmatch(Path(n).name, f"{pattern}.md"))
    if not names:
        return None, ""
    shown = git("show", f"{base}:./{names[0]}")
    if shown.returncode:
        sys.exit(f"git show failed: {shown.stderr.strip()}")
    return names[0], shown.stdout


def body(text: str) -> list[str]:
    """The mirror's lines without the parts every sync rewrites: the banner and the change log."""
    return [line for line in CHANGE_LOG.sub("", text).splitlines() if not line.startswith(BANNER)]


def normal(line: str) -> str:
    """A line as compared: whitespace runs and table padding do not make a change."""
    line = re.sub(r"\s+", " ", line).strip()
    return re.sub(r"\|\s*:?-{3,}:?\s*(?=\|)", "|---", line)


def changes(old_text: str, new_text: str, id_re: re.Pattern) -> list[Change]:
    old, new = body(old_text), body(new_text)
    matcher = difflib.SequenceMatcher(None, [normal(x) for x in old], [normal(x) for x in new], autojunk=False)
    removed: list[str] = []
    added: list[str] = []
    order: list[str] = []
    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag in ("replace", "delete"):
            removed += old[i1:i2]
        if tag in ("replace", "insert"):
            added += new[j1:j2]
        for line in old[i1:i2] + new[j1:j2] if tag != "equal" else []:
            order += id_re.findall(line)
    in_old, in_new = set(id_re.findall("\n".join(old))), set(id_re.findall("\n".join(new)))
    result = []
    for rid in dict.fromkeys(order):
        kind = "added" if rid not in in_old else "removed" if rid not in in_new else "changed"
        result.append(Change(rid, kind,
                             before=[x.strip() for x in removed if rid in id_re.findall(x)][:3],
                             after=[x.strip() for x in added if rid in id_re.findall(x)][:3]))
    return result


def cite(found: list[Change], globs: list[str], id_re: re.Pattern, ignore: list[str] = ()) -> None:
    """Fill each change's cited_by with every line in the decisions and the work that names its id."""
    wanted = {c.id: c for c in found}
    skipped = {p for pattern in ignore for p in ROOT.glob(pattern)}
    files = sorted({p for pattern in globs for p in ROOT.glob(pattern) if p.is_file()} - skipped)
    for path in files:
        rel = path.relative_to(ROOT).as_posix()
        for number, line in enumerate(path.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
            for rid in dict.fromkeys(id_re.findall(line)):
                if rid in wanted:
                    wanted[rid].cited_by.append((rel, number, line.strip()))


def question(change: Change) -> str:
    cited = bool(change.cited_by)
    if change.kind == "added":
        return ("A new requirement. Does it need a decision? If so, add an entry to "
                "`architecture/decisions/backlog.md`; if an existing ADR already covers it, cite the id there.")
    if change.kind == "removed":
        return (f"{change.id} left the PRD but is still cited. For each citation: drop it, point it at the "
                "requirement that replaced it (the PRD's traceability table keeps old ids), or mark the decision "
                "for review." if cited else
                f"{change.id} left the PRD and nothing cites it. Confirm that no decision is affected.")
    return ("Do the decisions that cite it still hold as written? For each: keep it, amend it (a law or an "
            "acceptance criterion), supersede it with a new ADR, or record a deviation." if cited else
            "Nothing cites it yet. Does the change need a decision (an entry in `architecture/decisions/backlog.md`), "
            "or none?")


def cited_lines(change: Change) -> list[str]:
    """One bullet per citing file: its line numbers, and the first citing line (shortened) for context."""
    by_file: dict[str, list[tuple[int, str]]] = {}
    for path, number, text in change.cited_by:
        by_file.setdefault(path, []).append((number, text))
    bullets = []
    for path, hits in by_file.items():
        first = hits[0][1] if len(hits[0][1]) <= 140 else hits[0][1][:139] + "…"
        numbers = ", ".join(str(n) for n, _ in hits)
        bullets.append(f"- `{path}` (line{'s' if len(hits) > 1 else ''} {numbers}): {first}")
    return bullets


def summary_rows(found: list[Change]) -> list[str]:
    rows = ["| Id | Change | Cited by |", "|---|---|---|"]
    rows += [f"| {c.id} | {c.kind} | {', '.join(c.lands_in) or '—'} |" for c in found]
    return rows


def report(found: list[Change], old_path: str | None, new_path: str, base: str) -> str:
    counts = {k: sum(c.kind == k for c in found) for k in ("added", "removed", "changed")}
    lines = [f"PRD impact: `{base}:{old_path}` -> `{new_path}`" if old_path else
             f"PRD impact: no mirror at `{base}`, so every id in `{new_path}` counts as added",
             "",
             f"{len(found)} ids: {counts['added']} added, {counts['removed']} removed, {counts['changed']} changed.",
             "", *summary_rows(found)]
    for c in found:
        if c.cited_by:
            lines += ["", f"{c.id} is cited by:", *cited_lines(c)]
    return "\n".join(lines) + "\n"


def worksheet(found: list[Change], old_path: str | None, new_path: str, base: str, date: str) -> str:
    source = f"`{base}:{old_path}`" if old_path else f"nothing at `{base}`"
    lines = [f"# PRD → decisions alignment, {date}",
             "",
             f"> Started by `prd/sync/impact.py`, comparing {source} with the synced mirror `{new_path}`.",
             "> Fill in every **Answer**, then land the answers in the decisions with the `gov-adr` skill. "
             "Keep this file once answered: it is the record of why the decisions moved.",
             "",
             "## Summary",
             "",
             *summary_rows(found),
             "",
             "## Questions"]
    for number, c in enumerate(found, 1):
        lines += ["", f"### Q{number}. {c.id} {c.kind}", ""]
        for label, text in (("Before", c.before), ("After", c.after)):
            if text:
                lines += [f"**{label}:**", "", "```text", *text, "```", ""]
        if c.cited_by:
            lines += ["**Cited by:**", "", *cited_lines(c), ""]
        lines += [f"**Decision needed:** {question(c)}",
                  "",
                  "**Options:** _to fill in_",
                  "",
                  "**Recommendation:** _to fill in_",
                  "",
                  f"**Lands in:** {', '.join(c.lands_in) or '_to decide_'}",
                  "",
                  "**Answer:** "]
    return "\n".join(lines) + "\n"


def free_name(date: str) -> Path:
    path, n = AUDITS / f"{date}_prd-adr-alignment.md", 2
    while path.exists():
        path, n = AUDITS / f"{date}_prd-adr-alignment-{n}.md", n + 1
    return path


def main() -> int:
    p = argparse.ArgumentParser(description="List the requirement ids a PRD sync changed and the decisions citing them.")
    p.add_argument("--base", default="HEAD", help="the commit to compare with (default HEAD: the last committed sync)")
    p.add_argument("--write", action="store_true", help="also start the alignment worksheet in resources/audits/")
    p.add_argument("--date", default=dt.date.today().isoformat(), help="the worksheet's date (default today)")
    args = p.parse_args()
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    ws = config.load(ROOT)
    pattern, id_re = ws.prd["pattern"], re.compile(ws.prd["id_pattern"])
    mirrors = sorted((ROOT / "prd").glob(f"{pattern}.md"))
    if len(mirrors) != 1:
        sys.exit(f"expected one mirror matching {pattern}.md in prd/, found {len(mirrors)}: run prd/sync/sync.py")
    new_path = mirrors[0].relative_to(ROOT).as_posix()
    old_path, old_text = previous_mirror(args.base, pattern)
    found = changes(old_text, mirrors[0].read_text(encoding="utf-8"), id_re)
    if not found:
        print(f"no requirement id changed between {args.base} and {new_path}")
        return 0
    cite(found, ws.prd.get("cited_in", []), id_re, ws.prd.get("not_cited_in", []))
    print(report(found, old_path, new_path, args.base), end="")
    if args.write:
        AUDITS.mkdir(parents=True, exist_ok=True)
        target = free_name(args.date)
        target.write_text(worksheet(found, old_path, new_path, args.base, args.date), encoding="utf-8", newline="\n")
        print(f"\nwrote:   {target.relative_to(ROOT).as_posix()} (fill in each Answer, then run the gov-adr skill)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
