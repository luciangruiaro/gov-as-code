# Prodigy Design System — UI Kit

> Canonical design-token reference for the **prodigy-site** front-end.
> All values map directly to the CSS custom properties defined in `globals.css` and `tailwind.config.ts`.

---

## 1. Color Palette

### 1.1 Light Theme

| Token | Hex | CSS Variable | Usage |
|-------|-----|--------------|-------|
| `primary` | `#001FBA` | `--color-primary` | CTAs, links, active states |
| `primaryStrong` | `#0820B3` | `--color-primary-strong` | Hover states, dark variant |
| `accent` | `#00FFBD` | `--color-accent` | Highlights, success indicators, focus rings |
| `accentSoft` | `#70E8C0` | `--color-accent-soft` | Subtle accent backgrounds |
| `bgCanvas` | `#f9fafb` | `--color-bg-canvas` | Page background |
| `bgSurface` | `#ffffff` | `--color-bg-surface` | Cards, panels, modals |
| `bgSurfaceSoft` | `#f4f7ff` | `--color-bg-surface-soft` | Soft card backgrounds, alternating rows |
| `bgTint` | `#edf2ff` | `--color-bg-tint` | Tinted sections, hover fills |
| `textPrimary` | `#0f173d` | `--color-text-primary` | Headings, body text |
| `textSecondary` | `#4e5d85` | `--color-text-secondary` | Supporting text, labels |
| `textTertiary` | `#6f7ca1` | `--color-text-tertiary` | Muted text, placeholders |
| `borderSubtle` | `#d8e0f2` | `--color-border-subtle` | Card borders, dividers |
| `borderStrong` | `#bcc9e8` | `--color-border-strong` | Emphasized borders, active inputs |

### 1.2 Dark Theme

| Token | Hex | CSS Variable | Usage |
|-------|-----|--------------|-------|
| `primary` | `#3b5bff` | `--color-primary` | CTAs, links, active states |
| `primaryStrong` | `#5a74ff` | `--color-primary-strong` | Hover states, light variant |
| `accent` | `#00FFBD` | `--color-accent` | Highlights, success indicators, focus rings |
| `accentSoft` | `#1a6b52` | `--color-accent-soft` | Subtle accent backgrounds |
| `bgCanvas` | `#001528` | `--color-bg-canvas` | Page background |
| `bgSurface` | `#0a2540` | `--color-bg-surface` | Cards, panels, modals |
| `bgSurfaceSoft` | `#0d2e4d` | `--color-bg-surface-soft` | Soft card backgrounds |
| `bgTint` | `#102a45` | `--color-bg-tint` | Tinted sections, hover fills |
| `textPrimary` | `#ffffff` | `--color-text-primary` | Headings, body text |
| `textSecondary` | `#94a3c4` | `--color-text-secondary` | Supporting text, labels |
| `textTertiary` | `#6b7a9e` | `--color-text-tertiary` | Muted text, placeholders |
| `borderSubtle` | `#1c3a5c` | `--color-border-subtle` | Card borders, dividers |
| `borderStrong` | `#2a4f78` | `--color-border-strong` | Emphasized borders, active inputs |

---

## 2. Typography

### 2.1 Font Families

| Role | Family | Weights | Source |
|------|--------|---------|--------|
| Body | **Manrope** | 400 (regular), 500 (medium), 600 (semibold), 700 (bold), 800 (extrabold) | Google Fonts |
| Display | **Sora** | 500 (medium), 600 (semibold), 700 (bold) | Google Fonts |
| Mono | **JetBrains Mono** | 400 (regular), 500 (medium) | Google Fonts |

```css
--font-body: 'Manrope', sans-serif;
--font-display: 'Sora', sans-serif;
--font-mono: 'JetBrains Mono', monospace;
```

### 2.2 Type Scale

| Token | Size | Typical Use |
|-------|------|-------------|
| `xs` | 12px / 0.75rem | Badges, captions, footnotes |
| `sm` | 14px / 0.875rem | Secondary text, table cells |
| `md` | 16px / 1rem | Body copy (base) |
| `lg` | 18px / 1.125rem | Lead paragraphs, sub-headings |
| `xl` | 20px / 1.25rem | Section headings |

### 2.3 Line Height & Letter Spacing

| Context | Line Height | Letter Spacing |
|---------|-------------|----------------|
| Headings / tight | `1.2` | `-0.02em` |
| Body / copy | `1.6` | `0` (normal) |

---

## 3. Shadows

All shadows use the brand primary color as the tint to keep elevation consistent with the overall palette.

| Token | Value | Usage |
|-------|-------|-------|
| `brand-sm` | `0 8px 20px rgba(0, 31, 186, 0.06)` | Cards at rest |
| `brand-md` | `0 12px 32px rgba(0, 31, 186, 0.08)` | Cards on hover, elevated panels |
| `brand-lg` | `0 20px 48px rgba(0, 31, 186, 0.12)` | Modals, dropdowns, popovers |

```css
--shadow-brand-sm: 0 8px 20px rgba(0, 31, 186, 0.06);
--shadow-brand-md: 0 12px 32px rgba(0, 31, 186, 0.08);
--shadow-brand-lg: 0 20px 48px rgba(0, 31, 186, 0.12);
```

---

## 4. Border Radius

| Token | Value | Usage |
|-------|-------|-------|
| `sm` | 8px | Badges, chips, small tags |
| `md` | 12px | Inputs, small cards, tooltips |
| `lg` | 16px | Cards, dropdowns |
| `xl` | 20px | Large cards, modals |
| `2xl` | 24px | Hero sections, feature panels |

```css
--radius-sm: 8px;
--radius-md: 12px;
--radius-lg: 16px;
--radius-xl: 20px;
--radius-2xl: 24px;
```

---

## 5. Spacing

### 5.1 Base Scale (4px increments)

| Token | Value |
|-------|-------|
| `1` | 4px |
| `2` | 8px |
| `3` | 12px |
| `4` | 16px |
| `5` | 20px |
| `6` | 24px |
| `8` | 32px |
| `10` | 40px |
| `12` | 48px |
| `16` | 64px |

### 5.2 Layout Dimensions

| Element | Value | CSS Variable |
|---------|-------|--------------|
| Sidebar (expanded) | 260px | `--layout-sidebar` |
| Sidebar (collapsed) | 68px | `--layout-sidebar-collapsed` |
| Topbar height | 56px | `--layout-topbar` |
| Footer height | 36px | `--layout-footer` |

---

## 6. Component Patterns

### 6.1 Buttons

#### Primary

```html
<button class="bg-primary text-white rounded-xl px-8 py-4 shadow-brand-sm
               hover:-translate-y-0.5 hover:shadow-brand-md
               transition-all duration-200">
  Get Started
</button>
```

| Property | Value |
|----------|-------|
| Background | `primary` (#001FBA) |
| Text | white |
| Radius | `xl` (20px) |
| Shadow | `brand-sm` at rest, `brand-md` on hover |
| Hover | translate Y -2px, shadow lift |

#### Secondary

```html
<button class="border border-borderSubtle bg-white text-primary rounded-xl
               px-8 py-4 hover:bg-bgTint transition-all duration-200">
  Learn More
</button>
```

| Property | Value |
|----------|-------|
| Background | white, `bgTint` on hover |
| Text | `primary` |
| Border | `borderSubtle` |
| Radius | `xl` (20px) |

#### Ghost

```html
<button class="border border-borderSubtle text-textSecondary rounded-lg
               px-4 py-2 hover:text-primary hover:border-primary/30
               transition-all duration-200">
  Cancel
</button>
```

| Property | Value |
|----------|-------|
| Background | transparent |
| Text | `textSecondary`, `primary` on hover |
| Border | `borderSubtle` |
| Radius | `lg` (16px) |

### 6.2 Cards

#### Default Card

```html
<div class="rounded-2xl border border-borderSubtle bg-bgSurface shadow-brand-sm
            hover:-translate-y-0.5 hover:shadow-brand-md hover:border-primary/15
            transition-all duration-280">
  <!-- content -->
</div>
```

| State | Shadow | Border | Transform |
|-------|--------|--------|-----------|
| Rest | `brand-sm` | `borderSubtle` | none |
| Hover | `brand-md` | `primary/15` | translateY(-2px) |

#### Soft Card (no elevation)

```html
<div class="rounded-2xl border border-borderSubtle bg-bgSurfaceSoft p-6">
  <!-- content -->
</div>
```

### 6.3 Inputs

```html
<input class="bg-bgSurface border border-borderSubtle rounded-md px-3 py-2
              text-sm text-textPrimary placeholder:text-textTertiary
              focus:border-accent focus:ring-2 focus:ring-accent/30
              transition-colors duration-180" />
```

| State | Border | Ring |
|-------|--------|------|
| Rest | `borderSubtle` | none |
| Focus | `accent` | 2px `accent/30` |
| Error | `red-500` | 2px `red-500/30` |

### 6.4 Glass Effect

```css
.glass {
  background: rgba(255, 255, 255, 0.86);
  border: 1px solid rgba(0, 31, 186, 0.14);
  backdrop-filter: blur(14px);
  -webkit-backdrop-filter: blur(14px);
}
```

Use for overlays, floating toolbars, and sticky headers that need a translucent look while remaining readable.

---

## 7. Animations

### 7.1 Duration Tokens

| Token | Duration | Easing | Usage |
|-------|----------|--------|-------|
| `fast` | 180ms | `ease` | Micro-interactions (focus, color change) |
| `base` | 280ms | `cubic-bezier(0.2, 0.8, 0.2, 1)` | General transitions (hover, expand) |
| `slow` | 360ms | `cubic-bezier(0.2, 0.8, 0.2, 1)` | Page transitions, modals |

### 7.2 Named Easings

| Name | Value | Usage |
|------|-------|-------|
| `ease-default` | `cubic-bezier(0.2, 0.8, 0.2, 1)` | Standard transitions |
| `ease-expo` | `cubic-bezier(0.16, 1, 0.3, 1)` | Dramatic entrances, slide-ins |

```css
--transition-fast: 180ms ease;
--transition-base: 280ms cubic-bezier(0.2, 0.8, 0.2, 1);
--transition-slow: 360ms cubic-bezier(0.2, 0.8, 0.2, 1);
--ease-expo: cubic-bezier(0.16, 1, 0.3, 1);
```

---

## 8. Reasoning Phase Palette

Six accent colours that drive the **Live Reasoning constellation** in the
superadmin SPA (`/agentic-core/live-reasoning`).  They colour the hub
gradient, spoke recolouring, particle hue, and per-satellite halo as a
Brain cycle progresses through its phase sequence
(planning → routing → execution → evaluation → synthesis, with
replan in between when re-routing is needed).

| Token | Hex | CSS Variable | Phase |
|-------|-----|--------------|-------|
| `phasePlanning` | `#4F7FFF` | `--phase-planning` | Plan generation — the orchestrator is enumerating candidate handlers. |
| `phaseRouting` | `#00C9F0` | `--phase-routing` | Candidate evaluation — `is_related()` + acceptance handshake. |
| `phaseExecution` | `#00C896` | `--phase-execution` | A handler is running.  Also used for the `conversation` fallback. |
| `phaseEvaluation` | `#F7A23B` | `--phase-evaluation` | The Brain is judging whether the response is sufficient. |
| `phaseReplan` | `#F45B5B` | `--phase-replan` | A step failed; the orchestrator is re-planning. |
| `phaseSynthesis` | `#7C5CFC` | `--phase-synthesis` | Final-answer synthesis. |

The backend ships a frozen phase → CSS-var map (`service.tracing.visualization.phase_colors.PHASE_COLORS`)
so the SSE reasoning stream stamps `phase_color: "var(--phase-routing)"`
directly onto every frame — the SPA resolves the var against its own
theme without negotiating the palette across the wire.

```css
:root {
  --phase-planning:     #4F7FFF;
  --phase-routing:      #00C9F0;
  --phase-execution:    #00C896;
  --phase-evaluation:   #F7A23B;
  --phase-replan:       #F45B5B;
  --phase-synthesis:    #7C5CFC;
  --phase-conversation: var(--phase-execution);
  --phase-idle:         var(--color-text-tertiary);
}
```

The values are tuned to stay legible against both `--color-bg-canvas`
(light-theme `#f9fafb`) and the dark-theme canvas (`#001528`).  Branding
overrides via the design-tokens system don't touch these tokens — the
phase palette is intentionally constant so the reasoning visualization
reads the same regardless of which realm a tenant is on.

---

## 9. CSS Variable Reference

Complete map of all custom properties with their default (light-theme) values.

### Colors

```css
:root {
  --color-primary:            #001FBA;
  --color-primary-strong:     #0820B3;
  --color-accent:             #00FFBD;
  --color-accent-soft:        #70E8C0;
  --color-bg-canvas:          #f9fafb;
  --color-bg-surface:         #ffffff;
  --color-bg-surface-soft:    #f4f7ff;
  --color-bg-tint:            #edf2ff;
  --color-text-primary:       #0f173d;
  --color-text-secondary:     #4e5d85;
  --color-text-tertiary:      #6f7ca1;
  --color-border-subtle:      #d8e0f2;
  --color-border-strong:      #bcc9e8;

  /* Reasoning phase palette — see §8. */
  --phase-planning:     #4F7FFF;
  --phase-routing:      #00C9F0;
  --phase-execution:    #00C896;
  --phase-evaluation:   #F7A23B;
  --phase-replan:       #F45B5B;
  --phase-synthesis:    #7C5CFC;
  --phase-conversation: var(--phase-execution);
  --phase-idle:         var(--color-text-tertiary);
}
```

### Typography

```css
:root {
  --font-body:    'Manrope', sans-serif;
  --font-display: 'Sora', sans-serif;
  --font-mono:    'JetBrains Mono', monospace;

  --font-size-xs: 0.75rem;   /* 12px */
  --font-size-sm: 0.875rem;  /* 14px */
  --font-size-md: 1rem;      /* 16px */
  --font-size-lg: 1.125rem;  /* 18px */
  --font-size-xl: 1.25rem;   /* 20px */

  --line-height-tight: 1.2;
  --line-height-copy:  1.6;

  --letter-spacing-tight:  -0.02em;
  --letter-spacing-normal:  0;
}
```

### Shadows

```css
:root {
  --shadow-brand-sm: 0 8px 20px rgba(0, 31, 186, 0.06);
  --shadow-brand-md: 0 12px 32px rgba(0, 31, 186, 0.08);
  --shadow-brand-lg: 0 20px 48px rgba(0, 31, 186, 0.12);
}
```

### Radius

```css
:root {
  --radius-sm:  8px;
  --radius-md:  12px;
  --radius-lg:  16px;
  --radius-xl:  20px;
  --radius-2xl: 24px;
}
```

### Layout

```css
:root {
  --layout-sidebar:           260px;
  --layout-sidebar-collapsed:  68px;
  --layout-topbar:             56px;
  --layout-footer:             36px;
}
```

### Transitions

```css
:root {
  --transition-fast: 180ms ease;
  --transition-base: 280ms cubic-bezier(0.2, 0.8, 0.2, 1);
  --transition-slow: 360ms cubic-bezier(0.2, 0.8, 0.2, 1);
  --ease-expo:       cubic-bezier(0.16, 1, 0.3, 1);
}
```

### Superadmin SPA layout vars

The superadmin SPA uses slightly different layout variable names from
the marketing site, plus a few page-local additions.  Source of truth:
`clients/superadmin/src/index.css`.

```css
:root {
  /* Global chrome */
  --sidebar-width:           220px;
  --sidebar-collapsed-width:  56px;
  --topbar-height:            48px;
  --footer-height:            48px;

  /* Page-local secondary sidebar (Self-Aware Agent) */
  --sa-sidebar-default:   320px;
  --sa-sidebar-min:       280px;
  --sa-sidebar-max:       540px;
  --sa-sidebar-collapsed:  48px;
}
```

The global sidebar's expanded width is **runtime-mutable**: the
operator can drag-resize it within `[200, 360]` (see §10.9) and the
chosen value persists in `localStorage`.  The CSS var holds the
*default*; the actual width is driven by the `sidebar.store`'s
`width` field.

---

## 10. Composite Patterns (Superadmin SPA)

These are the production-grade composite components built on top of
the tokens above.  Each pattern names a canonical implementation file
so a new page can either import the primitive directly or lift the
snippet verbatim.

All patterns are **brand-aware** — every colour reads from a CSS var
(`--color-accent`, `--color-primary`, `--phase-*`), so switching the
realm's brand in `/settings/design` instantly retheme them.

### 10.1 Hero section with brand-grounded backdrop

**Where**: `clients/superadmin/src/components/observability/HeroSection.tsx`

**When**: any page that needs an inviting page header — Control
Plane dashboard, Observability section landings, sub-section
overviews.  Pairs well with a Pulse strip directly below (§10.2).

**Anatomy**: `motion.section` with `initial/animate` fade-up, a
two-column grid (left column for eyebrow + title + subtitle + badge
row; right column for a small stat card), and three drifting
brand-tinted orbs in the background (the `HeroBackdrop`).

The backdrop uses three CSS-blurred orbs at `opacity 0.25 / 0.20 /
0.15`, sized `w-72 h-72` (288 px) and animated with the
`animate-pulse-soft` Tailwind utility, staggered with
`animationDelay: 0s / 1.2s / 2.4s`.

```tsx
<HeroSection
  eyebrow="Observability · System Health"
  title={<>Everything is <span className="text-gradient">humming</span>.</>}
  subtitle={`${healthy}/${total} components healthy`}
  badges={
    <>
      <Badge variant="success">Online</Badge>
      <Badge variant="default">v1.0.7</Badge>
    </>
  }
  stat={
    <div className="rounded-xl border border-[var(--color-border)] bg-[var(--color-bg-surface-soft)]/80 backdrop-blur-sm p-4 space-y-3">
      <PulseRow label="Version" value="v1.0.7" />
      <PulseRow label="Uptime" value="1h 46m" />
    </div>
  }
/>
```

Backdrop colours: `--color-accent` (top-right), `--color-primary`
(middle-left), `--color-primary-strong` (bottom).  The result tracks
whatever the active realm's brand palette is.

### 10.2 Pulse tile + pulse strip

**Where**: `clients/superadmin/src/components/observability/PulseTile.tsx`,
`PulseStrip.tsx`

**When**: a row of compact KPI tiles.  4–6 tiles per row; phase-
palette accents (`planning` / `routing` / `execution` / `evaluation` /
`replan` / `synthesis`) drive the icon background tint.  Clickable
when an `onClick` is provided.

```tsx
<PulseStrip columns={6}>
  <PulseTile
    label="Active capabilities"
    value={36}
    subtitle="of 55"
    icon={<Puzzle size={16} />}
    accent="execution"
    onClick={() => navigate(ROUTES.CAPABILITIES)}
  />
  <PulseTile
    label="Reasoning cycles"
    value={2}
    subtitle="1 live now"
    icon={<Radar size={16} />}
    accent="routing"
    live={true}
  />
  {/* … */}
</PulseStrip>
```

`columns` accepts `4 | 5 | 6`.  Pass `displayValue` to override the
formatted number (e.g. `compactNumber(tokens)` → `"11.0k"`).
`live: true` adds a pulsing dot to signal the metric is currently
moving.

### 10.3 Action tile

**Where**: `clients/superadmin/src/components/observability/ActionTile.tsx`

**When**: cross-page navigation tiles in a "I can help you…" grid.
Icon + title + 2-line blurb + chevron.  Phase-palette accent on the
icon tile.

```tsx
const cards: ActionTileCard[] = [
  {
    title: 'Visualize live thinking',
    blurb: 'Watch the brain reason in real time as it routes to capabilities.',
    icon: <Radar size={20} />,
    accent: 'routing',
    onClick: () => openLiveReasoning(),
  },
  // …
]

<div className="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-3 gap-3">
  {cards.map((card) => (
    <ActionTile key={card.title} card={card} onNavigate={navigate} />
  ))}
</div>
```

Hover lifts the card `-translate-y-0.5` and promotes `shadow-brand-sm` → `shadow-brand-md`; the chevron also slides right.

### 10.4 Activity feed

**Where**: `clients/superadmin/src/components/observability/ActivityFeed.tsx`

**When**: right-rail activity list, generic over item shape.  Handles
loading skeletons, empty state, and 403 permission-denied fallback in
one place.

```tsx
<ActivityFeed<AuditItem>
  title="Recent activity"
  subtitle="Live from the audit log"
  items={auditItems}
  isLoading={auditQuery.isLoading}
  error={auditQuery.error}
  permissionRequiredMessage="Audit-log view requires the security & privacy permission."
  renderItem={(item) => (
    <div className="flex items-center gap-2">
      <ActivityIcon action={item.action} />
      <span className="text-xs font-mono">{item.action}</span>
      <span className="ml-auto text-2xs text-[var(--color-text-tertiary)]">
        {formatRelativeTime(item.created_at)}
      </span>
    </div>
  )}
/>
```

The component auto-detects 403/forbidden in the `error` and swaps to
`permissionRequiredMessage`.  Empty list → `emptyMessage`.

### 10.5 Metric chip

**Where**: `clients/superadmin/src/components/observability/MetricChip.tsx`

**When**: small "X of Y" stat cards with a progress bar.  Used for
capability fleet breakdown, pool slot phases, knowledge source
freshness — any "enabled / total" view at a glance.

```tsx
<MetricChip
  label="Fleet"
  enabled={17}
  total={20}
  hint="agents enabled"
  accentColor="var(--color-accent)"
/>
```

### 10.6 Coming-soon overlay

**Where**: `clients/superadmin/src/components/observability/ComingSoonOverlay.tsx`

**When**: a tile is laid out but the backing endpoint isn't shipped
yet.  Subtle scrim + corner badge so the page still reads as
complete-by-design.

```tsx
<div className="relative">
  <PulseTile … />
  <ComingSoonOverlay gap="routing-decisions" />
</div>
```

The overlay preserves underlying alt-text and keyboard nav (it's
visual-only) so screen readers still describe what's coming.

Overlay discipline: the scrim marks a REAL gap, never fake data —
`mockData.ts` is retired and the former mocked panels are either real
now (latency percentiles are client-computed from persisted trace
durations via `DurationSection`; error trends bucket real audit rows)
or honest empty states (process metrics, eval quality).

### 10.6b Analytics chart kit additions

**Where**: `clients/superadmin/src/components/charts/{LineChart,StackedBarChart,MatrixTable}.tsx`

**When**: the Observability → Analytics dashboard's multi-series
trends (`LineChart`), per-day composition stacks (`StackedBarChart`),
and the users×capabilities heatmap cross-tab (`MatrixTable` — plain
HTML with an accent tint layer whose opacity scales value/max, so it
stays theme-safe in light + dark).  All follow the AreaChart/BarChart
token conventions (`--color-border` grid, `--color-text-muted` 11px
ticks, surface-tokened tooltip); the pure aggregation helpers live in
`pages/Observability/lib/analytics.ts`.

### 10.7 Animated active-rail (LayoutGroup + `layoutId`)

**Where**: `clients/superadmin/src/layouts/Sidebar.tsx`

**When**: navigation surfaces where the active item changes — global
sidebar, tab strips, breadcrumbs, segmented controls.  The rail glides
between active mount points instead of remounting per route, which
reads as "production grade" without any extra cost.

**Pattern**:

```tsx
<LayoutGroup id="my-nav">
  <nav>
    {items.map((item) => (
      <button
        key={item.id}
        className="group relative …"
        onClick={() => navigate(item.path)}
      >
        {isActive(item.path) && (
          <motion.span
            layoutId="my-nav-active-rail"
            aria-hidden
            className="absolute -left-px top-1.5 bottom-1.5 w-[3px] rounded-r-full"
            style={{ backgroundColor: 'var(--color-accent)' }}
            transition={{ type: 'spring', stiffness: 380, damping: 32 }}
          />
        )}
        <span>{item.label}</span>
      </button>
    ))}
  </nav>
</LayoutGroup>
```

The `layoutId` value must be **shared across every active rail** in
the same `LayoutGroup`.  Spring values `stiffness: 380, damping: 32`
give the canonical glide — softer feels mushy, snappier feels
twitchy.

### 10.8 Button-feel nav row (border slot + hover lift + active press)

**Where**: `Sidebar.tsx` (`NavLink`, `NavGroup`, sub-item button)

**When**: any nav surface that needs to feel tactile rather than
text-y.  The trick is to reserve a 1 px transparent border slot at
rest so the hover state filling it doesn't shift adjacent content.

**Pattern**:

```tsx
<button
  className={cn(
    'group relative w-full flex items-center gap-3 px-3 py-2 rounded-lg text-sm',
    // Reserve the border slot at rest
    'border border-transparent',
    // Transition every property the hover/active touches
    'transition-[background-color,color,border-color,transform,box-shadow] duration-150',
    active
      ? 'bg-[var(--color-accent)]/10 text-[var(--color-accent)] font-medium border-[var(--color-accent)]/30'
      : cn(
          'text-[var(--color-text-secondary)]',
          // Hover: fill the border, lift 1px, soft shadow
          'hover:text-[var(--color-text-primary)]',
          'hover:bg-[var(--color-bg-surface)]',
          'hover:border-[var(--color-border)]/60',
          'hover:shadow-sm hover:-translate-y-px',
          // Active press: undo the lift, drop shadow, tint
          'active:translate-y-0 active:shadow-none',
          'active:bg-[var(--color-bg-tint)]',
        ),
  )}
>
  …
</button>
```

Keep the duration tight (`150ms`) — slower feels heavy on a row
that's already small.

### 10.9 Resizable sidebar (drag handle + persistence)

**Where**:
- Global: `clients/superadmin/src/stores/sidebar.store.ts` (width +
  bounds + drag logic in `Sidebar.tsx`)
- Page-local: `clients/superadmin/src/hooks/useResizableSidebar.ts`
  + `components/ui/ResizableSidebar.tsx`

**When**: any side rail the operator wants to resize.  The drag
handle is an 8 px-wide invisible hit zone on the edge, with a 1 px
visual hairline on hover.

**Mechanic** (page-local, via the hook):

```tsx
const sidebar = useResizableSidebar({
  storageKey: 'myPage:sidebar',
  defaultWidth: 320,
  minWidth: 280,
  maxWidth: 540,
})

<aside style={{ width: sidebar.width }}>
  <div
    role="separator"
    aria-orientation="vertical"
    onMouseDown={sidebar.startResize}
    onDoubleClick={sidebar.resetWidth}
    className="absolute right-0 top-0 bottom-0 w-2 cursor-col-resize group"
  >
    <div className="absolute right-0 top-0 bottom-0 w-px bg-transparent group-hover:bg-[var(--color-accent)]/60 transition-colors" />
  </div>
  {children}
</aside>
```

For the **global** sidebar, the width lives in the zustand
`sidebar.store` (already persisted alongside `pinned` / `collapsed` /
section state), with bounds exported as
`SIDEBAR_MIN_WIDTH` / `SIDEBAR_MAX_WIDTH` / `SIDEBAR_DEFAULT_WIDTH`.

**Always**: set `document.body.style.cursor = 'col-resize'` and
`userSelect = 'none'` for the duration of the drag so text selection
doesn't fight the resize.

### 10.10 Pin / flare auto-hide

**Where**: `Sidebar.tsx` (the global one) + `sidebar.store.ts`'s
`pinned` boolean

**When**: a side rail the operator wants to auto-hide.  *Pinned* mode
holds layout space; *unpinned* mode shrinks to a rail and flares out
as an overlay on hover.

**State table**:

| `pinned` | `flared` | Sidebar position | Sidebar width | Content margin |
|---|---|---|---|---|
| true | — | `fixed` | `width` | `width` |
| false | false | `fixed` | rail | rail |
| false | true | `fixed`, z-40 (above content) | `width` | rail (no shift) |

**Flare logic**:

```tsx
const [flared, setFlared] = useState(false)
const flareTimerRef = useRef<number | null>(null)

const handleMouseEnter = useCallback(() => {
  if (flareTimerRef.current !== null) {
    window.clearTimeout(flareTimerRef.current)
    flareTimerRef.current = null
  }
  if (!pinned) setFlared(true)
}, [pinned])

const handleMouseLeave = useCallback(() => {
  if (!pinned) {
    flareTimerRef.current = window.setTimeout(() => {
      setFlared(false)
      flareTimerRef.current = null
    }, 150) // grace window — cursor may briefly leave bounds
  }
}, [pinned])
```

The 150 ms grace is the magic number.  Less and the rail snaps shut
when the cursor swings toward a nav item near the edge; more and it
feels sticky.

Promote the shadow to `--shadow-brand-lg` while flared so the
overlay is unmistakable; revert to the discrete edge shadow
(§10.11) when pinned or rail-only.

### 10.11 Brand-tinted edge shadow (rail separation)

**When**: a fixed side rail needs visible separation from the page
without a heavy border.

```tsx
<aside
  className="border-r border-[var(--color-border)]"
  style={{
    boxShadow: '4px 0 12px -2px rgba(0, 31, 186, 0.06)',
    // Promote to var(--shadow-brand-lg) when in overlay/flare mode
  }}
>
```

The `0, 31, 186` is the brand primary in RGB — the same tint as the
`--shadow-brand-*` family.  This is the discrete "rail at rest"
treatment; promote to `var(--shadow-brand-lg)` for overlay states
(§10.10).

### 10.12 Logo with brand-pulse status dot

**Where**: `Sidebar.tsx` logo block

**When**: a product header / corner mark.  The pulse dot doubles as a
"system alive" signal.

```tsx
<motion.div
  whileHover={{ scale: 1.06 }}
  transition={{ duration: 0.18 }}
  className="relative w-8 h-8 rounded-lg gradient-accent flex items-center justify-center shadow-brand-sm"
>
  <span className="text-sm font-bold text-[var(--color-bg-primary)]">
    {brandName?.[0]?.toUpperCase() ?? 'C'}
  </span>
  <span
    aria-hidden
    className="absolute -bottom-0.5 -right-0.5 w-2 h-2 rounded-full ring-2 ring-[var(--color-bg-secondary)]"
    style={{ backgroundColor: 'var(--color-accent)' }}
  />
</motion.div>
```

Sub-pattern: small **brand-color dot** as a prefix for secondary
labels (operator role, realm name).

```tsx
<div className="text-2xs text-[var(--color-text-muted)] inline-flex items-center gap-1.5">
  <span
    aria-hidden
    className="w-1.5 h-1.5 rounded-full"
    style={{ backgroundColor: 'var(--color-accent)' }}
  />
  Superadmin
</div>
```

### 10.13 Glow focus on inputs

**When**: form inputs that want a modern, soft focus state instead of
a hard border colour change.  Apply on top of any input — search bar,
textarea, ComboBox trigger.

```tsx
<input
  className={cn(
    'w-full rounded-lg bg-[var(--color-bg-primary)]/80 backdrop-blur-sm',
    'border border-[var(--color-border)] px-3 py-2 text-sm',
    'text-[var(--color-text-primary)] placeholder:text-[var(--color-text-muted)]',
    'focus:outline-none focus:border-[var(--color-accent)]',
    // The "glow" — ring at 30% accent opacity
    'focus:ring-2 focus:ring-[var(--color-accent)]/30',
    'transition-[border,box-shadow,background] duration-200',
  )}
/>
```

Pair the icon-in-input pattern with `group-focus-within:text-accent`
so the icon also picks up the brand colour on focus.

### 10.14 Portal-rendered dropdown (overflow escape)

**Where**: `clients/superadmin/src/components/ui/ComboBox.tsx`,
`Dropdown.tsx`

**When**: any dropdown inside a parent with `overflow:hidden`
(`Card padding="none"`, sidebars, drawers).  Without portalling, the
menu list gets clipped or z-stacked behind sibling rows.

**Pattern**:

```tsx
const [menuRect, setMenuRect] = useState<MenuRect | null>(null)
const inputRef = useRef<HTMLInputElement>(null)

const recomputePosition = () => {
  const r = inputRef.current?.getBoundingClientRect()
  if (r) setMenuRect({ top: r.bottom + 4, left: r.left, width: r.width })
}

useLayoutEffect(() => { if (open) recomputePosition() }, [open])

useEffect(() => {
  if (!open) return
  const handler = () => recomputePosition()
  window.addEventListener('scroll', handler, true) // capture nested
  window.addEventListener('resize', handler)
  return () => {
    window.removeEventListener('scroll', handler, true)
    window.removeEventListener('resize', handler)
  }
}, [open])

{open && menuRect && createPortal(
  <div
    className="fixed z-[1000] rounded-lg border bg-[var(--color-bg-surface)] shadow-xl"
    style={{ top: menuRect.top, left: menuRect.left, width: menuRect.width }}
  >
    {options.map(/* … */)}
  </div>,
  document.body,
)}
```

**Always**:
- `z-[1000]` — above modals/drawers (`z-40`) but below toasts.
- Listen to `scroll` in *capture* mode so nested scrollers also
  trigger reposition.
- Outside-click handler must check BOTH the trigger container AND the
  portalled menu — otherwise clicking inside the menu closes it.

### 10.15 Sidebar section accordion

**Where**: `clients/superadmin/src/components/ui/SidebarSection.tsx`

**When**: tight in-rail collapsible groups (smaller than the
`CollapsibleSection` card-style).

```tsx
<SidebarSection
  title="Target Audience"
  icon={<Users size={14} />}
  badge={count > 0 ? <Badge variant="accent" size="sm">{count}/6</Badge> : undefined}
  isOpen={openSection === 'audience'}
  onToggle={() => setOpenSection(openSection === 'audience' ? null : 'audience')}
>
  <PersonaForm value={persona} onChange={setPersona} />
</SidebarSection>
```

Body animates `height: 0 → 'auto'` + `opacity` together over 200 ms
with `ease: [0.4, 0, 0.2, 1]`.  Header chevron rotates 0 → 90°.

### 10.16 Tabbed page shell (URL-driven)

**Where**: `clients/superadmin/src/pages/Platform/DataPage.tsx`,
`PdlcPage.tsx`

**When**: a section with N siblings that benefits from deep-linking.
The tab state lives in `?tab=<id>` so a refresh / paste preserves the
view.

```tsx
const tabs = [
  { id: 'sources', label: 'Sources', icon: <Database size={16} /> },
  { id: 'backlog', label: 'Backlog', icon: <ListChecks size={16} /> },
  // …
]

const VALID_TAB_IDS = new Set(tabs.map((t) => t.id))

export function MyPage() {
  const [searchParams, setSearchParams] = useSearchParams()
  const requestedTab = searchParams.get('tab')
  const activeTab = useMemo(
    () => (requestedTab && VALID_TAB_IDS.has(requestedTab) ? requestedTab : 'sources'),
    [requestedTab],
  )
  const handleTabChange = (tabId: string) => {
    const next = new URLSearchParams(searchParams)
    if (tabId === 'sources') next.delete('tab')  // default tab → drop the param
    else next.set('tab', tabId)
    setSearchParams(next, { replace: true })
  }

  return (
    <div className="space-y-6">
      <Tabs tabs={tabs} activeTab={activeTab} onChange={handleTabChange}>
        <TabPanel><SourcesTab /></TabPanel>
        {/* … */}
      </Tabs>
    </div>
  )
}
```

Each tab lives in its own file under `MyPage/tabs/`.  Cross-tab deep
links work via additional search params (`?tab=assets&conn=<id>`).

### 10.17 Integration / connector tile

**Where**: `clients/superadmin/src/pages/Platform/Data/components/ConnectorTile.tsx`,
`Pdlc/components/IntegrationTile.tsx`

**When**: a gallery of external services (DB connectors, SDLC
integrations, API providers).  Fixed 150 px width, simple-icons CDN
logo, status badge top-right, "X connections" / "X agent uses"
footer.

```tsx
<button
  onClick={onClick}
  className={cn(
    'group relative shrink-0 w-[150px] rounded-xl border bg-[var(--color-bg-surface)] p-3 shadow-sm',
    'text-left transition-all hover:shadow-md',
    'focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[var(--color-accent)]',
    available
      ? 'border-[var(--color-border)] hover:border-[var(--color-accent)]/60 hover:-translate-y-0.5'
      : 'border-[var(--color-border)] opacity-50 grayscale hover:opacity-70',
  )}
>
  <div className="w-10 h-10 rounded-lg bg-[var(--color-bg-secondary)] flex items-center justify-center overflow-hidden">
    <img src={`https://cdn.simpleicons.org/${iconSlug}/${brandHex}`} alt={label} className="w-7 h-7 object-contain" />
  </div>
  <div className="text-sm font-semibold mt-3">{label}</div>
  <p className="text-2xs text-[var(--color-text-muted)] line-clamp-2">{description}</p>
  <div className="mt-3 pt-3 border-t border-[var(--color-border)] flex items-center justify-between">
    <span className="text-2xs">{count} connection{count === 1 ? '' : 's'}</span>
    <span className="text-2xs group-hover:text-[var(--color-accent)]">→</span>
  </div>
</button>
```

The simple-icons CDN format is `https://cdn.simpleicons.org/<slug>/<brand-hex>` — keep an icon URL map in `<page>/lib/icons.ts` so a single import resolves every tile in the gallery.

### 10.18 Mock JSON contract (deferred-backend pattern)

**Where**: `clients/superadmin/src/pages/Platform/Pdlc/{types.ts,mocks/*.ts}`

**When**: a panel needs to ship before its backend endpoint does.
Define the public TS interface in `types.ts`, export a typed mock
constant from `mocks/<name>.ts`, and the consumer imports the mock
as if it were a `fetch()` result.

```ts
// types.ts
export interface BacklogMock {
  goal: { title: string; target_date: string; days_remaining: number }
  velocity: { sprint: string; planned: number; completed: number }[]
  epics: BacklogEpic[]
  burndown: { date: string; remaining: number; ideal: number }[]
  priority_distribution: { name: 'P0' | 'P1' | 'P2' | 'P3'; value: number }[]
}

// mocks/backlog.ts
import type { BacklogMock } from '../types'
export const BACKLOG_MOCK: BacklogMock = { /* … */ }

// tabs/BacklogTab.tsx
import { BACKLOG_MOCK } from '../mocks/backlog'
const data = BACKLOG_MOCK
// → later, swap to: const { data } = useQuery(['backlog'], fetchBacklog)
```

The swap to a real endpoint is one import + one hook.  No tab
internals change.

### 10.19 No-plan / informational card (graceful empty)

**Where**: `clients/superadmin/src/pages/SuperAdmin/LLMPlaygroundPage.tsx`
(`NoPlanCard`)

**When**: a backend returned `null` / empty as a *deliberate*
decision, not a failure.  Don't render that as a 14 px grey line —
render an explanatory card so the operator knows the request was
acknowledged.

```tsx
<Card
  padding="none"
  className="overflow-hidden border-[var(--color-accent)]/20 bg-[var(--color-bg-surface-soft)]"
>
  <div className="flex items-start gap-3 p-4">
    <div className="p-2 rounded-lg bg-[var(--color-accent)]/10 shrink-0">
      <MessageCircle size={18} className="text-[var(--color-accent)]" />
    </div>
    <div className="flex-1 min-w-0">
      <div className="flex items-center gap-2 mb-1">
        <h4 className="text-sm font-semibold">{heading}</h4>
        <Badge variant="default" size="sm">{contextLabel}</Badge>
      </div>
      <p className="text-sm text-[var(--color-text-secondary)] leading-relaxed">
        {explanation}
      </p>
      {originalInput && (
        <div className="mt-3 rounded-md bg-[var(--color-bg-surface)] border border-[var(--color-border)] px-3 py-2">
          <span className="text-2xs uppercase tracking-widest text-[var(--color-text-tertiary)]">
            Your prompt
          </span>
          <p className="mt-0.5 text-xs">{originalInput}</p>
        </div>
      )}
    </div>
  </div>
  {/* Optional: example-prompts block with click-to-fill buttons */}
</Card>
```

Rule of thumb: if the backend deliberately returned "nothing to
do", the UI must say so in **at least 13 px**.

### 10.20 Rotating tagline catalogue (greeting variety)

**Where**: `clients/superadmin/src/pages/Dashboard/DashboardPage.tsx`
(`GREETING_SUBS`)

**When**: a hero subtitle that benefits from variety on each visit.
Pick once per mount with `useState(() => …)` so it doesn't flicker
on every re-render.

```tsx
const TAGLINES = [
  // Open invitations
  'Ready to orchestrate.',
  "Let's make something improbable.",
  // Specific framework concepts — anchored on real pillars
  'Plan. Route. Evaluate. Ship.',
  'Pick a capability — or let the brain pick.',
  'Self-aware. Self-extending.',
  // …
]

const [greetingSub] = useState(
  () => TAGLINES[Math.floor(Math.random() * TAGLINES.length)],
)
```

Anchor each line to a **concrete framework concept** (orchestrator,
fleet, RCS, SDLC pipeline, multi-LLM strategy) rather than generic
copy — operators read it as "the product knows what it is."

---

### 10.21 App-chrome glass + brand shadow

**Where**:
- `clients/superadmin/src/layouts/Topbar.tsx`
- `clients/superadmin/src/layouts/Footer.tsx`

**When**: any fixed bar that frames the page (topbar / footer /
left rail).  The chrome should read as a single family — same
glass treatment, same gradient depth, same brand-tinted
directional drop-shadow.  Bleeding the shadow inward toward the
page (down for topbar, up for footer, right for sidebar) clearly
separates the chrome from scrolling content without a hard line.

```tsx
<header
  className={cn(
    'fixed top-0 right-0 z-30 h-[var(--topbar-height)]',
    'bg-[var(--color-bg-primary)]/80 backdrop-blur-xl',
    'border-b border-[var(--color-border)]',
    'overflow-hidden',                       // contains the orb
  )}
  style={{
    left: leftOffset,                        // tracks sidebar width
    backgroundImage:
      'linear-gradient(180deg, var(--color-bg-secondary) 0%, ' +
      'color-mix(in srgb, var(--color-bg-secondary) 92%, var(--color-bg-canvas)) 100%)',
    boxShadow: '0 4px 12px -2px rgba(0, 31, 186, 0.06)',
  }}
>
  {/* Decorative brand orb — top-left, mirrors sidebar's bottom-left orb. */}
  <div
    aria-hidden
    className="pointer-events-none absolute -top-12 left-4 w-24 h-24 rounded-full blur-2xl"
    style={{ backgroundColor: 'var(--color-accent)', opacity: 0.15 }}
  />
  {/* …content (each block needs ``relative`` to stack above the orb). */}
</header>
```

**Rules**:
- `backdrop-blur-xl` (heavy) — not `-sm`.  Soft blur lets text from
  the page below ghost through and hurts legibility.
- The directional shadow value `0 ±4px 12px -2px rgba(0, 31, 186, 0.06)`
  is the brand-tinted mirror of the sidebar's right shadow.  Flip
  the sign on the Y offset depending on which edge of the chrome
  the shadow should bleed from.
- The orb is **decorative only** — `aria-hidden`, `pointer-events-none`,
  positioned to peek above/below the chrome edge.  `overflow-hidden`
  on the parent clips it cleanly.  The orb is smaller for shorter
  chrome (w-24 for 48 px topbar, w-32 for 48 px footer, w-48 for
  the tall sidebar).
- Inner content blocks must be `relative` so they paint above the
  absolutely-positioned orb.

---

### 10.22 Modal panel with brand shadow + decorative orb

**Where**: `clients/superadmin/src/layouts/CommandPalette.tsx`

**When**: any keyboard-driven modal (palette, picker, command
menu).  Stock `shadow-2xl` reads as flat against the polished
chrome family — promote to `--shadow-brand-lg` plus the same
gradient + decorative orb vocabulary so the modal feels like part
of the same product, just floated over the page.

```tsx
<div
  className="relative w-full max-w-2xl rounded-xl border border-[var(--color-border)] overflow-hidden"
  style={{
    backgroundColor: 'var(--color-bg-surface)',
    backgroundImage:
      'linear-gradient(180deg, var(--color-bg-secondary) 0%, ' +
      'color-mix(in srgb, var(--color-bg-secondary) 92%, var(--color-bg-canvas)) 100%)',
    boxShadow: 'var(--shadow-brand-lg)',
  }}
>
  {/* Decorative orb — top-left of the panel, peeks under the edge. */}
  <div
    aria-hidden
    className="pointer-events-none absolute -top-12 -left-12 w-40 h-40 rounded-full blur-2xl"
    style={{ backgroundColor: 'var(--color-accent)', opacity: 0.15 }}
  />
  {/* …input header, results, footer hints (each ``relative``). */}
</div>
```

**Rules**:
- Backdrop stays `bg-black/50 backdrop-blur-sm` — the modal panel
  is what gets the brand chrome, the backdrop just dims the page.
- The orb is bigger (w-40) than chrome orbs because the modal
  surface is taller; tune the size so the orb takes up ~10% of
  the panel area.
- Section headers inside the panel use the sidebar group-header
  vocabulary: uppercase + `tracking-wider` + 2 px brand-accent
  dot before the label (see CommandPalette result groups).
- The footer hint row (kbd cues) wears a faint
  `color-mix(... var(--color-bg-tint) 40%, transparent)` band so
  the cues read as part of the chrome, not an afterthought.  kbd
  chips get `border-[var(--color-accent)]/30`.

---

### 10.23 Animated keyboard-cursor (modal / menu)

**Where**: `clients/superadmin/src/layouts/CommandPalette.tsx`
(result list)

**When**: any keyboard-navigated list where the cursor moves
between items — palettes, autocomplete dropdowns, menu pickers.
Static `bg-accent/10` highlight remounts the selection between
groups; the animated rail glides instead, so the cursor reads as
**one moving thing** rather than a flicker.

```tsx
<LayoutGroup id="cmdk-results">
  {groupItems.map((item, idx) => {
    const isSelected = idx === selectedIndex
    return (
      <button className="relative w-full …">
        {isSelected && (
          <motion.span
            layoutId="cmdk-active-rail"
            className="absolute left-0 top-1 bottom-1 w-[3px] rounded-r"
            style={{ backgroundColor: 'var(--color-accent)' }}
            transition={{ type: 'spring', stiffness: 380, damping: 32 }}
          />
        )}
        {/* …icon + label */}
      </button>
    )
  })}
</LayoutGroup>
```

**Rules**:
- `LayoutGroup` `id` must be **unique per surface** — `cmdk-results`,
  `sidebar-nav`, `tabs-{page}`.  Two `LayoutGroup`s sharing a
  `layoutId` will cross-animate, which is a bug.
- Spring values `stiffness: 380, damping: 32` match the sidebar
  active-rail — don't roll one-off numbers.
- The rail is **3 px** wide on the left edge, accent colour, with
  vertical padding (`top-1 bottom-1`) so it doesn't touch the
  group divider.  Larger surfaces (sidebar) use the same width.
- Hovered (not yet selected) rows get a softer treatment
  (`hover:bg-[var(--color-bg-surface)]/60`) so the keyboard
  cursor stays the dominant signal.

---

### 10.24 Filter-pill row with animated cursor

**Where**: `clients/superadmin/src/pages/Capabilities/CapabilityListPage.tsx`
(type filter row)

**When**: any single-select filter cluster of three or more
options that lives **on the page** (not as a URL-driven sub-tab).
Use this for chip-style filters above a card grid; for sibling
subpages with their own routes, use §10.16 tabbed shell instead.

The static `bg-accent/10` pill toggle that pre-dated this pattern
flickered on filter change — the new pill appeared and the old
one disappeared in place.  Wrapping the row in a `LayoutGroup`
and rendering the brand-tinted background as a `motion.span`
makes the cursor glide between pills, the way the sidebar's
active-rail glides between nav items.

```tsx
<LayoutGroup id="caps-filter">
  <div className="flex items-center gap-2 flex-wrap">
    {options.map((opt) => {
      const isActive = filter === opt
      return (
        <button
          key={opt}
          onClick={() => setFilter(opt)}
          className={cn(
            'relative flex items-center gap-2 px-3 py-2 text-xs font-medium rounded-full',
            'border border-transparent',
            isActive
              ? 'text-[var(--color-bg-primary)]'                    // white-on-accent
              : 'text-[var(--color-text-secondary)] hover:bg-[var(--color-bg-surface)] hover:border-[var(--color-border)]/60 hover:-translate-y-px hover:shadow-[0_2px_6px_rgba(0,31,186,0.06)]',
            'active:translate-y-0 active:shadow-none',
            'transition-[transform,box-shadow,border-color,color] duration-150',
          )}
          aria-pressed={isActive}
        >
          {isActive && (
            <motion.span
              layoutId="caps-active-pill"
              className="absolute inset-0 rounded-full"
              style={{ backgroundColor: 'var(--color-accent)' }}
              transition={{ type: 'spring', stiffness: 380, damping: 32 }}
            />
          )}
          <span className="relative">{label}</span>
        </button>
      )
    })}
  </div>
</LayoutGroup>
```

**Rules**:
- The active pill's *text* must be wrapped in `relative` so it
  paints **above** the `motion.span` background; otherwise the
  brand-tinted slab covers the label.
- Active text colour is `--color-bg-primary` (white on the brand
  accent) — not `--color-accent` (which would disappear into the
  same-colour background).
- The pill row mirrors §10.23 (animated keyboard-cursor) but the
  rail expands to fill the whole pill instead of a 3 px left
  strip — sliding background = "this is the selected option";
  sliding rail = "this is where the keyboard cursor is".
- `LayoutGroup` `id` scoped per filter cluster (`caps-filter`,
  `obs-filter`, etc.); never share an `id` across pages.

---

### 10.26 `<PageHero>` primitive

**Where**: `clients/superadmin/src/components/ui/PageHero.tsx`

**When**: every page-level header.  Replaces the bare
`<h1>` + `<p>` pattern that lives on most pages.  Wraps the
gradient + decorative-orb + brand-dot-subtitle vocabulary into a
single drop-in component so the polish family stays consistent
without ten copies of the same JSX.

```tsx
<PageHero
  title="User Management"
  subtitle="Manage users with access to the Control Plane."
  actions={<Button …>Invite User</Button>}
/>
```

Optional props:
- `eyebrow` — a node rendered above the title (badges, breadcrumbs).
- `orbPosition` — `'top-right'` (default) / `'top-left'` /
  `'bottom-right'` / `'bottom-left'`.  Use the opposite corner of
  any nearby chrome orb to keep the canvas balanced.
- `dotColor` — defaults to `--color-accent`; override only for
  phase-coded hero (e.g. a Brain-reasoning page tinting the dot
  with the current phase colour).
- `children` — free-form content rendered below the title row,
  inside the same brand panel.

The hero panel uses `--shadow-brand-sm`, the sidebar gradient
`backgroundImage`, and an `opacity-0.18` orb at the configured
corner.  Every page that adopts `PageHero` reads as part of the
same family with zero extra JSX.

---

### 10.27 `<SectionHeader>` primitive

**Where**: `clients/superadmin/src/components/ui/SectionHeader.tsx`

**When**: inline-card section labels — the brand-dot + uppercase
tracking-wider header that ships across ConfigViewMode, HealthTab,
AuditLogPanel, CommandPalette result groups, etc.  Every
section header should reach for this primitive instead of
repeating the JSX.

```tsx
<SectionHeader>Identity & Routing</SectionHeader>
<SectionHeader count={items.length}>Examples</SectionHeader>
<SectionHeader asCardBar trailing={<Badge>Active</Badge>}>
  Database Overrides
</SectionHeader>
```

Props:
- `count` — renders a muted `(N)` suffix after the label.
- `trailing` — right-aligned slot for a badge, action, or link.
- `asCardBar` — wraps the header in the `bg-secondary` band with
  `border-b` divider chrome.  Use when the header sits at the top
  of a `Card padding="none"` card; omit for inline section labels
  that don't need the band.

---

### 10.25 Animated tab underline

**Where**: `clients/superadmin/src/components/ui/Tabs.tsx`

**When**: any `Tabs` component on the SPA — the generic Tabs
primitive already paints this, so every page that mounts `<Tabs>`
gets the gliding 2 px underline for free.  Custom tab layouts
(graph filter chips, page-local tabs not using the primitive)
should adopt the same vocabulary explicitly.

```tsx
<LayoutGroup id={`tabs-${instanceId}`}>            // useId() — one per Tabs instance
  <div className="flex gap-1 border-b border-[var(--color-border)]">
    {tabs.map((tab) => {
      const isActive = activeTab === tab.id
      return (
        <button className="relative -mb-px …">
          {tab.icon}
          {tab.label}
          {tab.badge != null && <Badge variant="default" size="sm">{tab.badge}</Badge>}
          {isActive && (
            <motion.span
              layoutId="tabs-active-underline"
              className="absolute left-0 right-0 -bottom-px h-[2px] rounded-full"
              style={{ backgroundColor: 'var(--color-accent)' }}
              transition={{ type: 'spring', stiffness: 380, damping: 32 }}
            />
          )}
        </button>
      )
    })}
  </div>
</LayoutGroup>
```

**Rules**:
- `LayoutGroup` `id` is scoped per Tabs instance via `useId()` so
  two `<Tabs>` mounted on the same page (e.g. a per-row Tabs
  inside a list) don't cross-animate their underlines.
- `layoutId` on the `motion.span` stays the literal string
  `"tabs-active-underline"` — Framer matches the moving element
  to the same `layoutId` inside the same `LayoutGroup`, and
  unique `LayoutGroup` ids already keep instances isolated.
- The underline is **2 px** high, full-width per tab, brand
  accent, with the `rounded-full` cap so the moving rail reads
  as a smooth bar.  Sit it at `-bottom-px` so it covers the
  `border-b` exactly.
- Spring values `stiffness: 380, damping: 32` — same as the
  sidebar active-rail, CommandPalette keyboard cursor, and
  filter pill cursor.  Do not roll one-off numbers.
- The tab badge uses `<Badge variant="default" size="sm">`, not
  a one-off `<span>` — keeps the badge family consistent.

---

## 11. When to use which pattern

Quick mapping from "what I'm building" → "which pattern fits":

| Building | Use |
|---|---|
| Section overview / landing page | §10.1 Hero + §10.2 Pulse strip + §10.3 Action grid + §10.4 Activity feed |
| Live metrics dashboard | §10.2 Pulse strip + §10.6 Coming-soon for gaps |
| Side panel inside a card | §10.15 SidebarSection (tight) or `CollapsibleSection` (card-style) |
| Section with sibling subpages | §10.16 Tabbed page shell |
| Picker with long option labels | §10.14 Portal dropdown — never an inline `<div className="z-50">` |
| Service / connector gallery | §10.17 Integration tile (simple-icons CDN) |
| Backend not shipped yet | §10.18 Mock JSON contract |
| Deliberately empty backend response | §10.19 Informational card — not a 14 px grey line |
| Resizable rail | §10.9 Resizable sidebar |
| Auto-hide / pin rail | §10.10 Pin / flare |
| Navigation rail | §10.7 Active rail + §10.8 Button-feel rows |
| Inputs anywhere | §10.13 Glow focus |
| App / page header | §10.12 Logo with pulse dot |
| Fixed topbar / footer chrome | §10.21 Glass + brand shadow + orb |
| Keyboard-driven modal (palette / picker) | §10.22 Modal brand chrome + §10.23 Animated cursor |
| Keyboard-cursor highlight in a list | §10.23 Animated cursor (LayoutGroup) — never a static `bg-accent/10` flicker |
| On-page filter cluster (chips, ≥3 options) | §10.24 Filter-pill row with animated cursor |
| Tab strip (sibling subpages or sibling views inside a page) | §10.16 Tabbed shell + §10.25 Animated underline (free via `<Tabs>` primitive) |
| Page title block | §10.26 `<PageHero>` — never a bare `<h1>` |
| Inline-card section header | §10.27 `<SectionHeader>` — never a bare `uppercase tracking-wider <h3>` |

---

## 12. Pattern checklist for new pages

Before shipping a new page, verify:

- [ ] Hero or page-title block uses brand-aware colours (no hardcoded hex)
- [ ] KPIs use Pulse tiles with phase-palette accents (§10.2)
- [ ] All `Card` components honour the `padding` prop
- [ ] Inputs use the glow focus pattern (§10.13)
- [ ] Dropdowns inside any `overflow:hidden` parent are portalled (§10.14)
- [ ] Empty / loading / 403 states are handled by `ActivityFeed` or a similar fallback
- [ ] Gap-backed sections wear a `Coming soon` badge / overlay (§10.6)
- [ ] Mocked data lives in `<page>/mocks/*.ts` behind a typed
  interface in `<page>/types.ts` (§10.18)
- [ ] No rogue `text-[9px]` / `text-[10px]` font sizes — round up to
  `text-2xs` or `text-xs` UI-kit tokens
- [ ] Navigation surfaces use `LayoutGroup` + `layoutId` for active-
  state animations (§10.7)
- [ ] Any new fixed chrome (topbar / footer / rail) wears the
  glass + brand-shadow + decorative-orb vocabulary (§10.21) so it
  reads as part of the existing chrome family
- [ ] Any new modal (palette / picker / command menu) wears the
  brand panel chrome (§10.22) and animates its keyboard cursor
  via `LayoutGroup` + `layoutId` (§10.23) — never a static
  `bg-accent/10` flicker
- [ ] Any new on-page filter cluster (3+ chip options) glides its
  selection through `LayoutGroup` + a `motion.span` background
  (§10.24) — never a static `border-accent` swap
- [ ] Any new tab strip uses the `<Tabs>` primitive (which already
  ships the animated underline, §10.25) — never a custom
  `border-b-2` colour swap
- [ ] Page title block uses the `<PageHero>` primitive (§10.26) —
  never a bare `<h1>` + `<p>` pair
- [ ] Inline-card section header uses the `<SectionHeader>`
  primitive (§10.27) — never a bare `uppercase tracking-wider
  <h3>`
- [ ] Brand check: switch theme colours in `/settings/design` — every
  accent surface should track
