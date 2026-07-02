# PRD templates

| File | Use it for |
|---|---|
| [`master-prd-template.md`](master-prd-template.md) | Starting a master PRD. Paste it into Word (or build a `.docx` with `pandoc master-prd-template.md -o "PRD template.docx"`) and keep the Word file on the shared drive in `PRD/`. |
| [`sample-master-prd.md`](sample-master-prd.md) | SAMPLE: the source of the sample Word PRD on the shared drive. It exists to demonstrate the sync and the decision review ([`../sync/SYNC.md`](../sync/SYNC.md), "Try it on the sample"). A new project drops it. |

The PRD is the client's document: it lives in Word, where the client reads, comments and agrees it. Git holds a mirror only, so every version is kept and every change is a diff. Requirements keep **stable ids on one table row each**: that is what lets `prd/sync/impact.py` turn a PRD change into a list of the decisions it touches.
