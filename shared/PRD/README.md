# PRD

**Holds:** the **master PRD** in Word, the one source of the product requirements. The governance repository keeps a Markdown mirror of it in `prd/`, so every version is kept and every change is a reviewable diff.

| Path | What |
|---|---|
| `Product Requirements Document (Master) - <Product> vN.N.docx` | The master PRD. The sync picks the highest version in the name, then the latest saved. |
| `Templates/PRD template.docx` | The template to start one, built from `prd/templates/master-prd-template.md` |
| `Archive/` | Superseded versions, if you prefer to keep them as files (Git has them anyway) |

**Naming:** keep `(Master)` and the version `vN.N` in the file name. A new version in the name renames the mirror in Git, and its change log carries over.

**Written by:** the client's product owner and the delivery team. **Read by:** `prd/sync/sync.py` (on request: the `gov-prd-sync` skill), and then everything in Git that cites a requirement id.

**Rules:**
- Edit here, never the mirror in Git.
- Every requirement keeps a stable id on its own table row (`FR-001`), so a change is one line in the diff.
- A Google Doc has no content on disk: download it as Word before syncing.

<!-- SAMPLE:BEGIN -->
> The `… - Project Name v0.1.docx` and `v0.2.docx` files are SAMPLES, built from `prd/templates/sample-master-prd.md` (v0.2 adds Hello World). A new project drops them.
<!-- SAMPLE:END -->
