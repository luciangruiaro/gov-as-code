# Operations: schedules, notifications, ports

## Schedules
The jobs that keep the workspace current. Times are the team's local time. A stub job does nothing until its tool is implemented (`tools/README.md`).

| Job | Command | When | Status |
|---|---|---|---|
| Code sync | `py -3.12 tools/repos/sync.py` | Weekdays 07:30 | stub |
| Code graphs (Graphify, GitNexus) | `py -3.12 tools/repos/scan.py` | Weekdays 07:40, after the code sync | implemented |
| Backlog mirror | `py -3.12 tools/mirrors/backlog.py` | Weekdays 07:00, 12:00, 16:00 | stub |
| Feedback mirror | `py -3.12 tools/mirrors/feedback.py` | Hourly, 08:00 to 18:00 | stub |
| Daily digest (collect, compose, approve, send) | `gov-digest` skill, run by a scheduled agent session; any time by a person | Weekdays 08:30, before stand-up | implemented |
| Workspace index | `py -3.12 tools/workspace/index.py` | Daily 07:45 | implemented |
| PRD sync | `gov-prd-sync` skill | On each new PRD version: a person runs it | implemented |

Schedule them on the machine that runs the team's jobs, so that only one machine writes each mirror:
- **Windows:** `schtasks /Create /SC WEEKLY /D MON,TUE,WED,THU,FRI /ST 07:30 /TN "<slug> code sync" /TR "py -3.12 <path>\tools\repos\sync.py"`
- **macOS:** a launchd agent in `~/Library/LaunchAgents/`.
- **Linux:** `cron`, for example `30 7 * * 1-5 cd <path> && python3 tools/repos/sync.py`.

## Notifications
| Space | What it gets | Webhook (`.env`) |
|---|---|---|
| Notifications | The daily digest and the on-demand workspace updates (`workspace.toml` `[digest] space`); mirror failures | `CHAT_WEBHOOK_NOTIFICATIONS` |
| Discussion | Questions to the team; decisions to note | `CHAT_WEBHOOK_DISCUSSION` |
| Test | Anything being tried out | `CHAT_WEBHOOK_TEST` |

Everything posts through `tools/reporting/chat.py` (skills `gov-chat` and `gov-digest`), signed with a persona: `CHAT_PERSONA_BOT` for automated posts, `CHAT_PERSONA_ARCHITECT` for posts made for the design authority. To get a webhook in Google Chat, open the space, then Apps & integrations > Webhooks > Add webhook, and paste the whole URL into `.env`. A webhook URL is a secret: it lives only in `.env`.

The digest never posts automatically unless `DIGEST_AUTO_SEND=true`. By default, a person approves each draft. Each draft and send is logged in `resources/local/digest/messages.md`, and the next update starts where the last *sent* one stopped.

## Ports
A block reserved for this project's local servers, so they don't collide with other projects on the same machine.

| Port | Serves |
|---|---|
| 47100 | Local preview of this repository's HTML (`py -3.12 -m http.server 47100`) |
| 47101–47199 | Free: assign here, one row each |
