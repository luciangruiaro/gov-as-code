# Debug

Written by `dev-debug` (an investigation: symptom → at least three hypotheses → evidence → the supported cause → a fix plan and adjacent risks) and `dev-dig` (one bounded probe that measures one hypothesis).

**Layout:** `<slug>/<slug>.md`, with probe output and logs beside it. Name the slug after the symptom, not the suspected cause.

**Rules:** evidence comes from the code and the running system, not from tickets. Redact any customer data from logs before you save them here. A fix that departs from a ratified ADR is proposed as a deviation row, never made silently.
