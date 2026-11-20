# project-fe: Hello World's web app

One page, React on Vite, styled only by the Prodigy Design System's tokens.

## Run
```
npm install
npm run dev      # http://localhost:47101, calls the API at VITE_API_URL (default http://localhost:47102)
npm test         # tokens match project-gov's, no raw colours, dependencies within budget
```

## Rules
- Runtime dependencies: `react` and `react-dom`. Nothing else.
- `src/prodigy-tokens.css` is a verbatim copy of `project-gov/resources/ui-kit/prodigy-tokens.css`. When the kit changes, copy it again.
- Styles use the tokens (`var(--color-primary)`), never raw colour values. Light and dark come from `data-theme` on `<html>`.
- The page has three states: loading, the message, and an error with "Try again".

## Governance
Governed by `project-gov` (cloned beside this repository, in `../project-gov`), at commit `97fa3f6` on `ciklum-devtalks-2026`.
ADRs this repository keeps:
- ADR-004: one job per repository, two contracts, a dependency budget, port 47101. Never talks to the database.
- ADR-007: React on Vite, `react` and `react-dom` only, the UI kit as the only source of style, one page with three states, WCAG 2.2 AA.
