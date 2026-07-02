"""Mirror the master PRD from Word into Markdown, so Git shows what changed between versions.

Usage: py -3.12 prd/sync/sync.py [--source FILE] [--check | --log "what changed"]

The source is the newest "<pattern>.docx" in the shared drive's PRD folder (workspace.toml [shared] path and [prd]
source_dir, pattern): the highest version in its name, then the latest saved. pandoc 3 or newer converts it into
prd/ under the Word file's own name, and its images go to prd/assets/master/. A new version in the name renames the
mirror. The change log at the end of the mirror survives every sync; --log adds a row with the date the Word file
was saved, its version and the text given. SYNC.md says what to check before a sync is committed.
"""
from __future__ import annotations

import argparse
import datetime as dt
import fnmatch
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))
from workspace import config  # noqa: E402  (tools/workspace/config.py)

WS = config.load(ROOT)
SOURCE_DIR = WS.shared / WS.prd["source_dir"]
PATTERN = WS.prd["pattern"]
PRD = ROOT / "prd"
ASSETS = PRD / "assets" / "master"
LOG_START = "<!-- change log, newest first: rows are added by prd/sync/sync.py (see sync/SYNC.md) -->"
LOG_END = "<!-- /change log -->"
LOG_HEAD = ["| Date | Version | What changed |", "|---|---|---|"]
BANNER = "> Mirror of the master PRD"
# Word underlines links and sizes images; Markdown has neither, so both go rather than stay as raw HTML.
FILTER = "function Underline(el) return el.content end\nfunction Image(el) el.attr = pandoc.Attr() return el end\n"


def find_source(explicit: str | None) -> Path:
    if explicit:
        path = Path(explicit)
        if not path.is_file():
            sys.exit(f"not found: {explicit}")
        if not fnmatch.fnmatch(path.name, f"{PATTERN}.docx"):
            sys.exit(f"the mirror takes its source's name, so --source must be the master PRD: {path.name}")
        return path
    if not SOURCE_DIR.is_dir():
        sys.exit(f"the shared drive is not linked in ({SOURCE_DIR} is missing): see WORKSPACE.md section 5, "
                 "or pass --source FILE")
    found = [p for p in SOURCE_DIR.glob(f"{PATTERN}.docx") if not p.name.startswith("~$")]  # ~$ is Word's lock file
    if not found:
        if any(SOURCE_DIR.glob(f"{PATTERN}.gdoc")):
            sys.exit("the master PRD is a Google Doc, which has no content on disk: download it as Word "
                     "(File > Download > Microsoft Word) and pass that file with --source")
        sys.exit(f"no {PATTERN}.docx in {SOURCE_DIR}: pass --source FILE")

    def newest(path: Path) -> tuple[tuple[int, ...], float]:
        version = re.search(r"\bv(\d+(?:\.\d+)*)", path.stem, re.IGNORECASE)
        return (tuple(int(n) for n in version.group(1).split(".")) if version else ()), path.stat().st_mtime

    return max(found, key=newest)


def find_pandoc() -> str:
    exe = shutil.which("pandoc")
    if not exe:
        sys.exit("pandoc not found: install pandoc 3 or newer (https://pandoc.org/installing.html)")
    first = subprocess.run([exe, "--version"], capture_output=True, encoding="utf-8").stdout.partition("\n")[0]
    major = re.search(r"(\d+)\.", first)
    if not major or int(major.group(1)) < 3:
        sys.exit(f"pandoc 3 or newer needed, found {first or 'an unknown version'}")
    return exe


def notices(docx: Path) -> list[str]:
    """What the conversion settles on its own: tracked changes and comments."""
    with zipfile.ZipFile(docx) as z:
        body = z.read("word/document.xml").decode("utf-8")
    found = []
    if changes := len(re.findall(r"<w:(?:ins|del)\b", body)):
        found.append(f"{changes} tracked changes, shown as accepted")
    if comments := body.count("<w:commentReference"):
        found.append(f"{comments} comments, left out")
    return found


def convert(pandoc: str, docx: Path) -> tuple[str, dict[str, bytes], list[str]]:
    with tempfile.TemporaryDirectory(prefix="prd-sync-") as tmp:
        work = Path(tmp)
        (work / "filter.lua").write_text(FILTER, encoding="utf-8")
        run = subprocess.run(
            [pandoc, str(docx), "--from=docx", "--to=gfm", "--wrap=none", "--eol=lf", "--track-changes=accept",
             "--lua-filter=filter.lua", "--extract-media=extracted", "--output=out.md"],
            cwd=work, capture_output=True, encoding="utf-8", errors="replace")
        if run.returncode:
            sys.exit(f"pandoc failed: {run.stderr.strip()}")
        text = (work / "out.md").read_text(encoding="utf-8")
        media = {p.name: p.read_bytes() for p in sorted((work / "extracted").rglob("*")) if p.is_file()}
    text = re.sub(r"\]\(extracted[/\\]media[/\\]", f"]({ASSETS.relative_to(PRD).as_posix()}/", text)
    return text.strip("\n"), media, [line for line in run.stderr.splitlines() if line.strip()]


def log_rows(mirror_text: str | None) -> list[str]:
    """The change log's rows in an existing mirror, newest first."""
    if not mirror_text or LOG_START not in mirror_text:
        return []
    block = mirror_text.split(LOG_START, 1)[1].split(LOG_END, 1)[0]
    return [line for line in block.splitlines() if line.startswith("|")][len(LOG_HEAD):]


def version_of(text: str) -> str | None:
    found = re.search(r"\bv\d+(?:\.\d+)*\b", text, re.IGNORECASE)
    return found.group(0) if found else None


def log_row(docx: Path, version: str, what: str) -> str:
    saved = dt.date.fromtimestamp(docx.stat().st_mtime).isoformat()
    return f"| {saved} | {version} | {' '.join(what.split()).replace('|', chr(92) + '|')} |"


def assemble(converted: str, rows: list[str]) -> str:
    title, _, body = converted.partition("\n") if converted.startswith("# ") else ("", "", converted)
    latest = ""
    if rows:
        date, version = (cell.strip() for cell in rows[0].strip("|").split("|")[:2])
        label = "" if version == "-" else f" ({version})"
        latest = f" Last change: {date}{label}, in the [change log](#change-log) at the end."
    note = (f"{BANNER}, which is kept in Word on the shared drive (`PRD/`). Change the Word document, "
            f"then sync with [`sync/SYNC.md`](sync/SYNC.md); never edit this file by hand.{latest}")
    parts = ([title, ""] if title else []) + [note, "", body.strip("\n")]
    if rows:
        parts += ["", "## Change log", "", LOG_START, "", *LOG_HEAD, *rows, "", LOG_END]
    return "\n".join(parts) + "\n"


def current_media() -> dict[str, bytes]:
    return {p.name: p.read_bytes() for p in sorted(ASSETS.iterdir()) if p.is_file()} if ASSETS.is_dir() else {}


def write(mirror: Path, text: str, media: dict[str, bytes]) -> None:
    mirror.write_bytes(text.encode("utf-8"))
    if ASSETS.is_dir():
        for old in ASSETS.iterdir():
            if old.name not in media:
                old.unlink()
    if media:
        ASSETS.mkdir(parents=True, exist_ok=True)
        for name, data in media.items():
            (ASSETS / name).write_bytes(data)


def main() -> int:
    p = argparse.ArgumentParser(description="Mirror the master PRD from Word into prd/, keeping its change log.")
    p.add_argument("--source", help="the master PRD in Word; default: the newest one on the shared drive")
    mode = p.add_mutually_exclusive_group()
    mode.add_argument("--check", action="store_true", help="only say whether the mirror is current; exit 1 if not")
    mode.add_argument("--log", metavar="TEXT", help="add a change-log row: the Word file's saved date, version, TEXT")
    args = p.parse_args()
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    docx = find_source(args.source)
    converted, media, warnings = convert(find_pandoc(), docx.absolute())
    mirror = PRD / f"{docx.stem}.md"
    found = sorted(PRD.glob(f"{PATTERN}.md"))
    if len(found) > 1:
        sys.exit(f"more than one mirror in prd/, keep one: {', '.join(f.name for f in found)}")
    previous = found[0] if found else None
    old = previous.read_text(encoding="utf-8") if previous else None
    rows = log_rows(old)
    title = converted.partition("\n")[0].lstrip("# ")
    if args.log:
        row = log_row(docx, version_of(docx.stem) or version_of(title) or "-", args.log)
        if rows[:1] != [row]:
            rows.insert(0, row)
    text = assemble(converted, rows)

    saved = dt.datetime.fromtimestamp(docx.stat().st_mtime).strftime("%Y-%m-%d %H:%M")
    print(f"source:  {docx.name} (saved {saved})")
    print(f"title:   {title}")
    warnings = notices(docx) + warnings
    named, titled = version_of(docx.stem), version_of(title)
    if named and titled and named.lower() != titled.lower():
        warnings.append(f"the file name says {named} but the title says {titled}")
    if leftover := sorted(set(re.findall(r"<([a-z][a-z0-9]*)(?=[\s/>])", converted))):
        warnings.append(f"raw HTML left in the text: {', '.join(leftover)}")
    for line in warnings:
        print(f"warning: {line}")

    unchanged = previous == mirror and old == text and current_media() == media
    if args.check:
        print("the mirror is current" if unchanged else "the mirror is out of date: run py -3.12 prd/sync/sync.py")
        return 0 if unchanged else 1
    if unchanged:
        print("no change: the mirror already matches this file")
        return 0
    write(mirror, text, media)
    if previous and previous != mirror:
        previous.unlink()
        print(f"renamed: {previous.name} -> {mirror.name}")
    images = f" and {len(media)} image(s) in {ASSETS.relative_to(ROOT).as_posix()}/" if media else ""
    print(f"wrote:   {mirror.relative_to(ROOT).as_posix()} ({text.count(chr(10))} lines){images}")
    print(f"logged:  {rows[0]}" if args.log else
          "next:    read what changed, run prd/sync/impact.py, then log it (sync/SYNC.md steps 2 to 5)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
