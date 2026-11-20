"""Post one message to a team chat space through its incoming webhook, signed with a persona.

Usage: py -3.12 tools/reporting/chat.py [--to test|notifications|discussion] [--persona bot|architect|"Name"]
                                        [--no-persona] [--thread KEY] [--dry-run] ("message" | --file PATH)

The one tool in tools/ that sends anything out. The gov-chat skill posts with it ("tell the team …"), and the
gov-digest skill delivers the workspace update with it.

Settings, from .env (gitignored; copy .env.example) or the process environment, which wins:
- Spaces (operations/README.md): CHAT_WEBHOOK_TEST, CHAT_WEBHOOK_NOTIFICATIONS, CHAT_WEBHOOK_DISCUSSION. The
  GCHAT_WEBHOOK_* names are read too, so a .env from an older workspace keeps working.
- Personas, the name that signs a message: CHAT_PERSONA_BOT (automated posts; default "<project name> bot") and
  CHAT_PERSONA_ARCHITECT (posts made for the design authority). Any other --persona value is used as the name.

Format: Google Chat markup, sent as is: *bold*, _italic_, ~strike~, `mono`, <https://url|text>. No Markdown
headings. Slack's incoming webhooks take the same payload ({"text": …}); threads are Google Chat's.

Rules: the webhook URL is a secret: it is never printed, and it must be https. A message over 4,096 characters is
refused, never split. --dry-run checks the settings and prints the message, sending nothing. Exit 0 when sent (or
on a dry run), 1 on any refusal or failure, with the reason after "ERROR:".
"""
from __future__ import annotations

import argparse
import json
import sys
import urllib.error
import urllib.request
from pathlib import Path
from typing import Callable

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))  # tools/, so the workspace package imports
from workspace import config  # noqa: E402

MAX_CHARS = 4096  # Google Chat's limit for a text message
SPACES = ("test", "notifications", "discussion")
PERSONAS = {"bot": "BOT", "architect": "ARCHITECT"}
REPLY = "messageReplyOption=REPLY_MESSAGE_FALLBACK_TO_NEW_THREAD"

Lookup = Callable[[str], str]


class Refused(Exception):
    """A message the tool will not send, with the reason."""


def setting(lookup: Lookup, suffix: str) -> tuple[str, str]:
    """The first set value among CHAT_<suffix> and GCHAT_<suffix>, with the name it came from."""
    for name in (f"CHAT_{suffix}", f"GCHAT_{suffix}"):
        value = lookup(name)
        if value:
            return name, value
    return f"CHAT_{suffix}", ""


def webhook(lookup: Lookup, space: str, required: bool = True) -> tuple[str, str]:
    if space not in SPACES:
        raise Refused(f"unknown space '{space}': use {', '.join(SPACES)}")
    name, url = setting(lookup, f"WEBHOOK_{space.upper()}")
    if not url and required:
        raise Refused(f"{name} is not set: paste the space's webhook into .env (Apps & integrations > Webhooks)")
    if url and not url.startswith("https://"):
        raise Refused(f"{name} must be an https:// webhook URL")
    return name, url


def signature(lookup: Lookup, persona: str, project: str) -> str:
    key = PERSONAS.get(persona.lower())
    if key is None:
        return persona  # a literal name
    _, name = setting(lookup, f"PERSONA_{key}")
    return name or (f"{project} bot" if key == "BOT" else "Architect")


def compose(message: str, signed_by: str | None) -> str:
    text = message.strip()
    if not text:
        raise Refused("the message is empty")
    if signed_by:
        text = f"*{signed_by}* · {text}"
    if len(text) > MAX_CHARS:
        raise Refused(f"the message is {len(text)} characters; Google Chat takes at most {MAX_CHARS}")
    return text


def request(url: str, text: str, thread: str = "") -> urllib.request.Request:
    payload: dict = {"text": text}
    if thread:
        payload["thread"] = {"threadKey": thread}
        url += ("&" if "?" in url else "?") + REPLY
    return urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), method="POST",
                                  headers={"Content-Type": "application/json; charset=UTF-8"})


def post(req: urllib.request.Request, opener=urllib.request.urlopen) -> str:
    """Send it; returns the message's name (its id) when the service gives one."""
    try:
        with opener(req, timeout=15) as resp:
            raw = resp.read()
    except urllib.error.HTTPError as e:
        raise Refused(f"HTTP {e.code} from the chat service: {e.read().decode('utf-8', 'replace')[:200]}") from None
    except urllib.error.URLError as e:
        raise Refused(f"cannot reach the chat service: {e.reason}") from None
    try:
        return json.loads(raw or b"{}").get("name", "?")
    except (ValueError, AttributeError):
        return "?"  # Slack answers "ok" in plain text


def main(argv: list[str] | None = None, lookup: Lookup | None = None, opener=urllib.request.urlopen) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")  # the Windows console
    p = argparse.ArgumentParser(description="Post one message to a team chat space, signed with a persona.")
    p.add_argument("message", nargs="?", help="the message text, in chat markup (*bold*, _italic_)")
    p.add_argument("--file", help="read the message from a file (UTF-8), for long or multi-line messages")
    p.add_argument("--to", default="test", help=f"the space: {' | '.join(SPACES)} (default: test)")
    p.add_argument("--persona", default="bot", help="bot | architect | a literal name (default: bot)")
    p.add_argument("--no-persona", action="store_true", help="send the message unsigned")
    p.add_argument("--thread", default="", help="a thread key to group messages under (Google Chat)")
    p.add_argument("--dry-run", action="store_true", help="check the settings and print the message; send nothing")
    args = p.parse_args(argv)

    ws = config.load()
    lookup = lookup or (lambda name: config.setting(name, ws.root))
    try:
        message = Path(args.file).read_text(encoding="utf-8-sig") if args.file else (args.message or "")
        name, url = webhook(lookup, args.to.lower(), required=not args.dry_run)
        signed_by = None if args.no_persona else signature(lookup, args.persona, ws.name)
        text = compose(message, signed_by)
        if args.dry_run:
            state = "set" if url else "NOT SET"
            print(f"dry run -> {args.to} ({name} {state}), {len(text)} chars, nothing sent\n---\n{text}")
            return 0
        message_id = post(request(url, text, args.thread), opener)
    except (Refused, OSError) as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1
    print(f"sent -> {args.to} as {signed_by or '(no persona)'} [{message_id}]")
    return 0


if __name__ == "__main__":
    sys.exit(main())
