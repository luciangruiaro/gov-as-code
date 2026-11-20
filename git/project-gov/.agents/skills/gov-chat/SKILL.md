---
name: gov-chat
description: Post one message to a team chat space (Google Chat test, notifications or discussion) with tools/reporting/chat.py, signed with a persona. Use it for "tell the team", "post to chat", "send me a note", or when another skill delivers a message. Webhooks and personas live in .env.
argument-hint: <message, optionally "to notifications|discussion" and "as architect|bot">
user_invocable: true
---

# Post to the team chat

Send one message to one of the team's chat spaces, signed with a persona. The spaces and what each one gets are in `operations/README.md` ("Notifications"). Webhooks and personas come from `.env` (copy `.env.example`).

## Defaults
- **Space:** `test`, the sandbox (`CHAT_WEBHOOK_TEST`).
- **Persona:** `bot` (`CHAT_PERSONA_BOT`; when it is empty, "<project name> bot"). `architect` signs with `CHAT_PERSONA_ARCHITECT`. Any other value is used as the name.
- **Thread:** none, so the message starts its own.

## Steps
1. Read the intent: the text, the space, the persona, and whether a thread was asked for.
2. Confirm before posting to `discussion`, the team's room: read the message back and ask "send this?", unless the user dictated the exact text. `test` and `notifications` need no confirmation.
3. Write the message in chat markup (below). Pass a short one as the argument. Put a multi-line one in a file under `resources/local/` (gitignored), for example `resources/local/chat/message.md`.
4. Run from this repository's root:
   ```
   py -3.12 tools/reporting/chat.py [--to test|notifications|discussion] [--persona bot|architect|"Name"] [--thread KEY] [--no-persona] [--dry-run] ("message" | --file PATH)
   ```
   `--dry-run` checks the settings and the 4,096-character limit, prints the message and sends nothing.
5. Report the tool's `sent ->` line (it carries the message id) or its `ERROR:` line, verbatim. When a webhook is missing, tell the user which variable to fill in `.env`: the error names it.

## Chat markup
`*bold*`, `_italic_`, `~strike~`, `` `mono` ``, `<https://url|link text>`, and `<users/all>` (@all: in the discussion space only, and only when the user asks to ping everyone). No Markdown headings or tables.

## Hard rules
1. **Never post to `discussion` without explicit intent.** It is the team's room.
2. **Webhook URLs stay in `.env`.** Never print, log or paste them anywhere.
3. **Send only what you were asked to.** Every post traces to the user's request, or to a scheduled run whose switch is on (`DIGEST_AUTO_SEND` for `gov-digest`).
4. **One audience.** Anyone in the space may read it: no secrets, no customer data, no contract text, nothing about other clients.
