# git/: the versioned half of the workspace

| Folder | What |
|---|---|
| [`project-gov/`](project-gov/README.md) | The governance repository: requirements (PRD mirror), decisions (ADRs), rules (`AGENTS.md`), skills, the workspace map. In a real project it is its own Git repository, `<slug>-gov`. |
| `project-be/`, `project-fe/`, … | The product repositories, cloned here beside the governance repo (listed in `project-gov/workspace.toml`, kept current by `tools/repos/sync.py`). Not part of the skeleton, and ignored by this repository's `.gitignore`. |
| [`project-db/`](project-db/AGENTS.md), [`project-be/`](project-be/AGENTS.md), [`project-fe/`](project-fe/AGENTS.md) | SAMPLE, on the `ciklum-devtalks-2026` branch only: Hello World (ADR-004 to ADR-007), built live at DevTalks and kept here as plain folders so the demo's exact end state is in one repository. In a real project each is its own repository. `new-project.py` never copies them. |

The product repositories sit beside the governance repository on purpose: agents, reviews and the daily digest read the **code itself**, because tickets and documents are only claims.
