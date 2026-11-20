"""tools/reporting/digest.py: the window, the log it resumes from, and what each section of the bundle picks up."""
from __future__ import annotations

import contextlib
import io
import os
import shutil
import subprocess
import tempfile
import time
import unittest
from datetime import datetime, timedelta
from pathlib import Path

from support import load_script

from workspace import config

digest = load_script("tools/reporting/digest.py", "reporting_digest")

WED = datetime(2026, 11, 18, 8, 30)
MON = datetime(2026, 11, 16, 8, 30)
SAT = datetime(2026, 11, 21, 8, 30)


def write(path: Path, text: str, age_hours: float = 0) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    if age_hours:
        then = time.time() - age_hours * 3600
        os.utime(path, (then, then))
    return path


def git(cwd: Path, *args: str, days_ago: int = 0) -> None:
    env = {**os.environ, "GIT_AUTHOR_NAME": "Ada Example", "GIT_AUTHOR_EMAIL": "ada@example.com",
           "GIT_COMMITTER_NAME": "Ada Example", "GIT_COMMITTER_EMAIL": "ada@example.com"}
    if days_ago:
        env["GIT_AUTHOR_DATE"] = env["GIT_COMMITTER_DATE"] = (datetime.now() - timedelta(days=days_ago)).isoformat()
    subprocess.run(["git", *args], cwd=cwd, check=True, capture_output=True, text=True, env=env)


def workspace(tmp: Path) -> config.Workspace:
    """A workspace laid out like the real one: shared/ beside git/, the gov repo in git/, one clone missing."""
    root = tmp / "git" / "demo-gov"
    root.mkdir(parents=True)
    (tmp / "shared").mkdir()
    return config.Workspace(root=root, config={
        "project": {"name": "Demo", "slug": "demo"},
        "shared": {"path": "../../shared"},
        "repo": [{"slug": "demo-be", "role": "Backend"}],
        "backlog": {"mirror_dir": "Jira", "project_key": "PRJ"},
        "feedback": {"mirror_dir": "Feedback"},
        "digest": {"window_hours": 24, "team_notes": "Team/Bot notes.md", "directives": "Team/Directives.md"},
    })


def last_24h() -> digest.Window:
    end = datetime.now() + timedelta(minutes=1)
    return digest.Window(end - timedelta(hours=24), end, "test")


class Window(unittest.TestCase):
    def test_standard_window_by_weekday(self):
        self.assertEqual(digest.choose_window(WED).hours, 24)
        self.assertEqual(digest.choose_window(MON).hours, 72)
        with self.assertRaises(digest.Weekend):
            digest.choose_window(SAT)

    def test_hours_and_the_last_sent_update_work_any_day(self):
        self.assertEqual(digest.choose_window(SAT, hours=6).hours, 6)
        since = SAT - timedelta(hours=50)
        window = digest.choose_window(SAT, since=since)
        self.assertEqual((window.start, window.reason), (since, "since the last sent update"))
        self.assertEqual(digest.choose_window(WED, since=WED + timedelta(hours=1)).hours, 24, "a stamp from the future")

    def test_last_sent_reads_only_sent_entries(self):
        with tempfile.TemporaryDirectory() as tmp:
            log = Path(tmp) / "messages.md"
            self.assertIsNone(digest.last_sent(log))
            write(log, "## 2026-11-17 (24h window, collected 2026-11-17 08:30) - status: SENT TO NOTIFICATIONS 2026-11-17\n"
                       "text\n---\n"
                       "## 2026-11-18 (24h window, collected 2026-11-18 08:30) - status: SENT TO TEST 2026-11-18 (message x)\n"
                       "---\n"
                       "## 2026-11-19 (24h window, collected 2026-11-19 08:30) - status: PENDING APPROVAL\n---\n")
            self.assertEqual(digest.last_sent(log), datetime(2026, 11, 18, 8, 30))

    def test_main_stops_at_weekends(self):
        err = io.StringIO()
        with contextlib.redirect_stderr(err), contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(digest.main(["--until", "2026-11-21 08:30"]), 3)
        self.assertIn("weekend", err.getvalue())


@unittest.skipUnless(shutil.which("git"), "git is not installed")
class Code(unittest.TestCase):
    def test_commits_roles_churn_and_work_in_progress(self):
        with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as tmp:
            ws = workspace(Path(tmp))
            write(ws.shared / "Team" / "Team structure.md",
                  "| Role | Name |\n|---|---|\n| Backend engineer | Ada Example |\n| QA engineer | <name> |\n")
            git(ws.root, "init", "-q", "-b", "main")
            write(ws.root / "old.py", "print('old')\n")
            git(ws.root, "add", ".")
            git(ws.root, "commit", "-q", "-m", "an old change", days_ago=5)
            write(ws.root / "app.py", "a = 1\nb = 2\n")
            git(ws.root, "add", "app.py")
            git(ws.root, "commit", "-q", "-m", "add the app")
            write(ws.root / "app.py", "a = 1\nb = 3\nc = 4\n")
            write(ws.root / "notes.md", "draft\n")
            notes: list[str] = []
            text = digest.code_section(ws, last_24h(), False, notes)
        self.assertIn("1 commit(s)", text)
        self.assertIn("Backend engineer · [main] · add the app", text)
        self.assertNotIn("an old change", text)
        self.assertIn("`app.py` +2 -0", text)
        self.assertIn("modified: `app.py` (+2 -1)", text)
        self.assertIn("new: `notes.md`", text)
        self.assertTrue(any("demo-be is not cloned" in n for n in notes))
        self.assertTrue(any("no remote yet" in n for n in notes))

    def test_adr_status_changes_against_the_window_start(self):
        index = "| ADR | Title | Status | Date | Requirements |\n|---|---|---|---|---|\n"
        with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as tmp:
            ws = workspace(Path(tmp))
            git(ws.root, "init", "-q", "-b", "main")
            path = write(ws.root / digest.ADR_INDEX, index + "| [ADR-001](a.md) | One | DRAFT | 2026-01-05 | — |\n")
            git(ws.root, "add", ".")
            git(ws.root, "commit", "-q", "-m", "index", days_ago=3)
            write(path, index + "| [ADR-001](a.md) | One | VISION-RATIFIED | 2026-01-05 | — |\n"
                                "| [ADR-002](b.md) | Two | DRAFT | 2026-11-19 | — |\n")
            write(ws.root / "architecture" / "questions.md",
                  "| Id | Question | Requirements | Owner (role) | Status | Answer (date) |\n|---|---|---|---|---|---|\n"
                  "| q1 | Which provider? | FR-001 | client IT lead | open | — |\n"
                  "| q2 | Which region? | NFR-001 | devops engineer | answered | EU (2026-11-01) |\n")
            text = digest.governance_section(ws, last_24h())
        self.assertIn("ADR-001: DRAFT → VISION-RATIFIED (One)", text)
        self.assertIn("ADR-002: new, DRAFT (Two)", text)
        self.assertIn("open questions: 1", text)
        self.assertNotIn("q2", text)


class Drive(unittest.TestCase):
    def test_backlog_feedback_drive_calls_and_team(self):
        with tempfile.TemporaryDirectory() as tmp:
            ws = workspace(Path(tmp))
            now = datetime.now()
            stamp = (now - timedelta(hours=2)).strftime(digest.STAMP)
            old = (now - timedelta(days=4)).strftime(digest.STAMP)
            ticket = "# PRJ-{n}: {title}\n\n| Field | Value |\n|---|---|\n| Status | {status} |\n| Sprint | S1 |\n" \
                     "| Assignee | backend engineer |\n| Updated | {updated} |\n"
            write(ws.shared / "Jira" / "current-sprint" / "PRJ-1.md",
                  ticket.format(n=1, title="Submit a request", status="In Progress", updated=stamp))
            write(ws.shared / "Jira" / "done" / "PRJ-2.md",
                  ticket.format(n=2, title="Old work", status="Done", updated=old), age_hours=96)
            created = (now - timedelta(hours=1)).astimezone().isoformat()
            write(ws.shared / "Feedback" / "2026-11-20-abcd1234.md",
                  f"---\nid: abcd\ncreated_at: {created}\nkind: bug\ncontext:\n  page: Request detail\nstatus: new\n"
                  "triage: untriaged\n---\n\n# Bug: The upload fails\n")
            write(ws.shared / "Delivery" / "Updates" / "weekly.md", "report\n")
            write(ws.shared / "Decks" / "old.pptx", "x", age_hours=72)
            write(ws.shared / "Decks" / "desktop.ini", "x")
            write(ws.shared / "INDEX.md", "generated\n")
            day = now.strftime("%Y-%m-%d")
            write(ws.shared / "Transcripts" / "Internal Calls" / f"{day} 10-00 - Stand-up - notes.md", "notes\n")
            write(ws.shared / "Transcripts" / "Client Calls" / f"{day} 14-00 - Review.gdoc", "{}")
            write(ws.shared / "Team" / "Directives.md",
                  f"## {day}\n- Ship M1 first.\n\n## 2026-01-05\n- Milestone M2 is due 2999-01-01.\n- Old rule.\n")
            write(ws.shared / "Team" / "Bot notes.md", "## Standing notes\n- Mention people by role.\n")
            window, notes = last_24h(), []
            backlog = digest.backlog_section(ws, window, notes)
            feedback = digest.feedback_section(ws, window, notes)
            drive = digest.drive_section(ws, window, notes)
            calls = digest.calls_section(ws, window)
            team = digest.team_section(ws, window)
        self.assertIn("- In Progress:", backlog)
        self.assertIn("PRJ-1 · Submit a request · backend engineer", backlog)
        self.assertNotIn("PRJ-2", backlog)
        self.assertIn("new: 2026-11-20-abcd1234 · bug · page Request detail", feedback)
        self.assertIn('"Bug: The upload fails"', feedback)
        self.assertIn("`Delivery/Updates/weekly.md`", drive)
        for left_out in ("old.pptx", "desktop.ini", "INDEX.md", "Jira/", "Feedback/", "Transcripts/"):
            self.assertNotIn(left_out, drive)
        self.assertIn("Stand-up - notes.md` (readable here)", calls)
        self.assertIn("Review.gdoc` (cloud-only: read it in the browser)", calls)
        self.assertIn(f"> {day}: Ship M1 first.", team)
        self.assertIn("> 2026-01-05: Milestone M2 is due 2999-01-01.", team)
        self.assertNotIn("Old rule", team)
        self.assertIn("> - Mention people by role.", team)
        self.assertEqual(notes, [])

    def test_missing_sources_become_collector_notes(self):
        with tempfile.TemporaryDirectory() as tmp:
            ws = workspace(Path(tmp))
            shutil.rmtree(ws.shared)
            notes: list[str] = []
            window = last_24h()
            self.assertIn("no mirror", digest.backlog_section(ws, window, notes))
            self.assertIn("drive not linked", digest.drive_section(ws, window, notes))
        self.assertEqual(len(notes), 2)


if __name__ == "__main__":
    unittest.main()
