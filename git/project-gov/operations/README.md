# Operations: schedules, notifications, ports

## Schedules
The jobs that keep the workspace current. Times are the team's local time. A stub job does nothing until its tool is implemented (`tools/README.md`).

| Job | Command | When | Status |
|---|---|---|---|
| Code sync | `py -3.12 tools/repos/sync.py` | Weekdays 07:30 | stub |
| Backlog mirror | `py -3.12 tools/mirrors/backlog.py` | Weekdays 07:00, 12:00, 16:00 | stub |
| Feedback mirror | `py -3.12 tools/mirrors/feedback.py` | Hourly, 08:00 to 18:00 | stub |
| Daily digest (collect, compose, approve, send) | `gov-digest` skill, run by a scheduled agent session | Weekdays 08:30, before stand-up | stub |
| Workspace index | `py -3.12 tools/workspace/index.py` | Daily 07:45 | implemented |
| PRD sync | `gov-prd-sync` skill | On each new PRD version: a person runs it | implemented |

Schedule them on the machine that runs the team's jobs, so that only one machine writes each mirror:
- **Windows:** `schtasks /Create /SC WEEKLY /D MON,TUE,WED,THU,FRI /ST 07:30 /TN "<slug> code sync" /TR "py -3.12 <path>\tools\repos\sync.py"`
- **macOS:** a launchd agent in `~/Library/LaunchAgents/`.
- **Linux:** `cron`, for example `30 7 * * 1-5 cd <path> && python3 tools/repos/sync.py`.

## Notifications
| Space | What it gets | Webhook (`.env`) |
|---|---|---|
| Notifications | The daily digest; mirror failures | `CHAT_WEBHOOK_NOTIFICATIONS` |
| Discussion | Questions to the team; decisions to note | `CHAT_WEBHOOK_DISCUSSION` |
| Test | Anything being tried out | `CHAT_WEBHOOK_TEST` |

The digest never posts automatically unless `DIGEST_AUTO_SEND=true`. By default, a person approves each draft.

## Ports
A block reserved for this project's local servers, so they don't collide with other projects on the same machine.

| Port | Serves |
|---|---|
| 47100 | Local preview of this repository's HTML (`py -3.12 -m http.server 47100`) |
| 47101–47199 | Free: assign here, one row each |
