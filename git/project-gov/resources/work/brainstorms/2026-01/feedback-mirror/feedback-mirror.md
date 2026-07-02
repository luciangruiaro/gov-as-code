# Brainstorm: how in-app feedback reaches the team

> SAMPLE. A fictional brainstorm in the shape `dev-brainstorm` writes. A new project drops it.
> **Date:** 2026-01-15 · **Serves:** FR-004 · **Led to:** proposal `2026-01-16 - Where in-app feedback lives` (shared drive, `Team/Proposals/`), then `adr-003`

## The idea
FR-004 puts a feedback button on every screen. The question is not the button, but what happens next: who sees an item, how fast, and how it becomes work.

## Framings
1. **Feedback as a ticket.** Every item becomes a backlog ticket straight away. *For:* one queue. *Against:* floods the backlog, and most items are not work.
2. **Feedback as a stream.** Items land in the app's database and are mirrored to the shared drive, where the whole team sees them; triage turns some into tickets. *For:* visible to all, with cheap triage. *Against:* needs a pull tool.
3. **Feedback as a conversation.** Items go to a chat channel. *For:* immediate. *Against:* no context (page, build) and hard to search later.

## Tensions
- Visibility against noise: everyone should see feedback, but not everyone should triage it.
- Context against privacy: the page and the build help, but the author's name does not belong in the mirror.

## Recommendation
Framing 2. It keeps the data in the client's environment, gives every item its context, and lets the daily digest group items by screen and requirement.

## Open decisions
- Where the items are stored, and the pull's schedule (→ the proposal on the drive, then `adr-003`).
- Whether an item may carry the requirement id of its screen (idea I-01 on the drive).
