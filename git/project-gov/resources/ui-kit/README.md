# UI kit: the Prodigy Design System

The brand for everything this project builds with a screen: the app's own UI (unless the client mandates its own design system), and this repository's reports, dashboards and explainers. It is the design system of the Prodigy Agentic Framework.

| File | What it is |
|---|---|
| [`ui-kit.md`](ui-kit.md) | **The canonical reference**, copied verbatim from the framework. Sections 1–9 hold the tokens (colour, type, shadows, radius, spacing, motion) and the CSS variable map. Sections 10–12 hold the component and composite patterns, written for the framework's React and Tailwind front-ends. |
| [`prodigy-tokens.css`](prodigy-tokens.css) | The tokens as CSS custom properties, light and dark, with a minimal base, for this repository's HTML pages. Values come from `ui-kit.md` sections 1 and 9; `tests/test_ui_kit.py` keeps them equal. |

## The system at a glance
- **Colour:** primary `#001FBA` (dark theme `#3b5bff`), accent `#00FFBD`. Canvas `#f9fafb` in light, `#001528` in dark; text `#0f173d` in light, `#ffffff` in dark. The phase palette (planning, routing, execution, evaluation, replan, synthesis) doubles as a categorical palette for charts.
- **Type:** Manrope for body text, Sora for display, JetBrains Mono for code and data. All are on Google Fonts.
- **Shape:** radius from 8 to 24 px; shadows tinted with the brand primary.
- **Motion:** 180, 280 and 360 ms, plus an expo ease.

## Use it in a page
```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700;800&family=Sora:wght@500;600;700&family=JetBrains+Mono:wght@400;500&display=swap">
<link rel="stylesheet" href="prodigy-tokens.css">
```
Use the tokens (`var(--color-primary)`, `var(--radius-md)`), never raw hex values. For a self-contained report, inline the CSS. Offline, the fonts fall back to the system sans-serif and monospace.

## Keeping it current
- When the framework's kit changes, copy its `resources/work/ui-kit.md` over this one. If sections 1 or 9 changed, update `prodigy-tokens.css` in the same commit; the test will name any value that differs.
- When a client mandates its own brand, replace both files with the client's kit and keep the token names (`--color-*`, `--font-*`, `--radius-*`), so existing pages keep working. Record the switch as an ADR.
