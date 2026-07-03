---
name: gov-adr
description: Write or update architectural decisions. Turns an ADR backlog entry into ADR-0NN-slug.md from the template, or lands the answers of a PRD alignment worksheet in the ADRs, the backlog and the open questions; then rebuilds the ADR index.
argument-hint: <a backlog id such as adr-003, or the path of an answered resources/audits/*_prd-adr-alignment.md>
user_invocable: true
---

# Write a decision, or land a worksheet's answers

Read first: the hard rules in [`AGENTS.md`](../../../AGENTS.md), [`architecture/decisions/README.md`](../../../architecture/decisions/README.md) (rules and statuses), [`_template.md`](../../../architecture/decisions/_template.md), the [backlog](../../../architecture/decisions/backlog.md) and [`questions.md`](../../../architecture/questions.md).

## A. From a backlog entry (`adr-0NN`)
1. Read the entry, the PRD requirements it cites (in the mirror in `prd/`), and any brainstorm, proposal or worksheet that led to it.
2. Draft the ADR in chat first: its context, the options with their for and against, the laws, and the acceptance criteria. Ask the open questions. Write nothing until the user approves the outline.
3. Write `architecture/decisions/ADR-0NN-<kebab-slug>.md` from the template. The number is the backlog entry's number. Use `Status: DRAFT`, today's date, and `**Requirements:**` listing every PRD id it rests on. Label any unconfirmed claim with a `q…` or `a…` id, and add new ones to `questions.md`.
4. In the backlog, link the ADR and set the entry to `partial`.

## B. From an answered alignment worksheet
For each question that has an **Answer**, in order:
- **Keep:** nothing to change. Optionally refresh the ADR's References to the new PRD version.
- **Amend:** a `DRAFT` ADR may be edited in place. A `VISION-RATIFIED` ADR is never weakened: write a new ADR that supersedes it, and fill in both `Supersedes` lines.
- **New decision:** add a backlog entry (`open`), or follow A if the answer asks for the ADR now.
- **Removed requirement:** update each citation as the answer says.
- **Code already departs:** propose a deviation row in chat. The design authority appends it to `architecture/deviations/README.md`; you never write it.

Skip questions that have no Answer, and list them at the end.

## Then, every time
1. Run `py -3.12 tools/architecture/adr_index.py` (the index in `decisions/README.md`), then `py -3.12 -m unittest discover -s tests`.
2. Report every file changed, and each question you skipped.
3. Commit only when asked: `docs(adr): …`.

## Hard rules
- Only the design authority (the solution architect) sets `VISION-RATIFIED`. Set it only when that person tells you to, in this conversation.
- ADRs are vision: no sprints, no file:line evidence, no "as of now". Deviations go in the register.
- Never reuse an ADR number. Never delete a ratified ADR: supersede it.
