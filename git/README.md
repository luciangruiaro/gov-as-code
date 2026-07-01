# git/: the versioned half of the workspace

| Folder | What |
|---|---|
| [`project-gov/`](project-gov/README.md) | The governance repository: requirements (PRD mirror), decisions (ADRs), rules (`AGENTS.md`), skills, the workspace map. In a real project it is its own Git repository, `<slug>-gov`. |
| `project-be/`, `project-fe/`, … | The product repositories, cloned here beside the governance repo (listed in `project-gov/workspace.toml`, kept current by `tools/repos/sync.py`). Not part of the skeleton, and ignored by this repository's `.gitignore`. |

The product repositories sit beside the governance repository on purpose: agents, reviews and the daily digest read the **code itself**, because tickets and documents are only claims.
