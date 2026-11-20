# ADR-007 — SAMPLE: The web app is React on Vite, styled only by the UI kit

> **Status:** DRAFT · **Date:** 2026-11-20 · **Decided by:** solution architect · **Supersedes:** — · **Superseded-by:** —
> **Requirements:** FR-006, FR-007, NFR-003, NFR-005, NFR-006 · **Backlog:** adr-007 · **Governs:** project-fe
> Deviations from this ADR are tracked in the [deviation register](../deviations/README.md), never here.

> SAMPLE. Part of Hello World, Release 0 of the fictional sample PRD. A new project drops this ADR.

## 1. Context
The web app has one page. It shows the greeting from the API (FR-006), or says plainly that it could not be loaded and offers to try again (FR-007). It follows the project's UI kit, the Prodigy Design System, in light and dark themes (NFR-005, [`resources/ui-kit/`](../../resources/ui-kit/README.md)). It meets WCAG 2.2 AA like every screen (NFR-003). It must be as lightweight as possible and start with one command (NFR-006).

[ADR-006](ADR-006-sample-hello-world-python-api.md) fixes the one endpoint the page calls. [ADR-004](ADR-004-sample-hello-world-three-repositories.md) forbids the web app any other way to reach the data.

## 2. Options
| Option | For | Against |
|---|---|---|
| **React on Vite, with plain CSS on the kit's tokens** | Two runtime dependencies; a fast dev server; the kit's `prodigy-tokens.css` is used as it is | No component library: the page's few elements are written by hand |
| Next.js | Routing, server rendering, conventions | Routing and server rendering that one page doesn't need; far more dependencies |
| React with Tailwind | Matches the kit's composite patterns (`ui-kit.md` sections 10 to 12) | Adds Tailwind and its build configuration for one page |

## 3. Decision: the laws
1. **React and nothing else at runtime.** Vite builds the app. Its only runtime dependencies are `react` and `react-dom`: no router, no state library, no component library. Its one start command is `npm run dev`, which serves on port 47101 (ADR-004 law 5).
2. **The UI kit is the only source of style.** `prodigy-tokens.css` is copied verbatim from `project-gov/resources/ui-kit/`. Styles use its variables (`var(--color-primary)`, `var(--radius-md)`), never raw colour values, and the fonts are the kit's (Manrope, Sora). Light and dark themes come from the tokens, never from the app's own palette.
3. **One page, three states.** The page calls `GET /api/hello` at the address in `VITE_API_URL`. It shows a loading state, then the message (FR-006), or an error in plain words with a "Try again" button (FR-007).
4. **Accessible by construction.** The page meets WCAG 2.2 AA (NFR-003). The error is announced to screen readers, and the button is reachable from the keyboard.

## 4. Acceptance criteria (timeless)
1. CI compares `prodigy-tokens.css` with the governance repository's copy and fails when they differ.
2. CI fails on a raw colour value (a hex code, `rgb()` or `hsl()`) anywhere in the source outside `prodigy-tokens.css`.
3. Component tests cover the loading, message and error states, and that "Try again" calls the endpoint again.
4. An automated accessibility check (axe) of the page reports no WCAG 2.2 AA violations in either theme.
5. CI fails when the runtime dependencies are anything other than `react` and `react-dom`.

## 5. Consequences
- Easier: the page looks like every other surface of the project, with no design work, and a change to the kit reaches it by copying one file.
- Harder: a component the kit describes for Tailwind (sections 10 to 12) is rebuilt in plain CSS when it's needed.
- Accepted: the tokens file is a copy, kept equal by a check, not shared at runtime. That keeps the web app free of any dependency on the governance repository.

## 6. References
- PRD v0.2: FR-006, FR-007, NFR-003, NFR-005, NFR-006.
- [`resources/ui-kit/README.md`](../../resources/ui-kit/README.md) and `ui-kit.md` (the Prodigy Design System).
- [ADR-004](ADR-004-sample-hello-world-three-repositories.md) (the port and the budget), [ADR-006](ADR-006-sample-hello-world-python-api.md) (the endpoint).
