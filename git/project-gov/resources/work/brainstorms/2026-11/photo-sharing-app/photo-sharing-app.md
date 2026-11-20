# Brainstorm: Hello World becomes a photo-sharing app

> SAMPLE. A brainstorm about the fictional sample product. A new project drops it.

The seed asks to turn Hello World into "an application like Instagram", with the whole product in the PRD and every possible decision in ADRs before any building starts. In this repository, that means three things. The master PRD's sample approval portal gives way to a photo-sharing product. Hello World stays as its walking skeleton (Release 0). And the ADRs that bind the three Hello World repositories (ADR-004 to ADR-007) are superseded wherever a real app outgrows them. The product gets its own name and look (the Prodigy UI kit), never Instagram's.

**Slug:** `photo-sharing-app`
**Created:** 2026-11-20
**Author:** operator + dev-brainstorm, during the DevTalks demo
**Status:** exploratory

---

## Seed

> I want now to update this PRD to a state that will describe an application like Instagram. So I want basically my hello world to become an Instagram and to have all the details in the PRD, as well as all the ADRs possible before I start building it.

Clarified with the operator:
- **Scope:** full Instagram parity (posts, feed, social graph, stories, direct messages, short video, explore and recommendations, shopping, ads).
- **PRD shape:** the photo app replaces the sample portal; Hello World stays as Release 0.
- **Stack:** the same three repositories (`project-db`, `project-be`, `project-fe`) evolve. Lightweight stays a value, not a hard budget.
- **Scale:** demo-grade (local, plus one small cloud deployment), scale-aware: ADRs say where they would change at scale, without building it.

## Repo context: what already exists

- **The master PRD** (`prd/Product Requirements Document (Master) - Project Name v0.2.md`, mirrored from Word through `prd/sync/sync.py`) describes the sample request-approval portal (FR-001 to FR-004, NFR-001 to NFR-003, GR-001, CFG-001, SM-001, OI-001, OI-002) and Release 0, Hello World (FR-006, FR-007, NFR-005, NFR-006, GR-002, CFG-002, SM-002, OI-003). Ids are never reused (`AGENTS.md`, "IDs and naming"), so the photo app's requirements start at FR-008, NFR-007, GR-003, CFG-003, SM-003 and OI-004. FR-005 and NFR-004 are taken by the sample worksheet (`resources/audits/2026-01-20_prd-adr-alignment.md`).
- **Replacing the portal is a PRD change with impact.** `prd/sync/impact.py` will report the portal's ids as removed. ADR-002, the backlog (`adr-002`, `adr-003`) and `questions.md` (`q1`, `a1`) cite them, so the sync needs an alignment worksheet (`prd/sync/SYNC.md`, step 4), answered by the design authority.
- **Decisions in force** (`architecture/decisions/README.md`, all `DRAFT`):
  - ADR-002, identity only from the organisation's single sign-on. That doesn't fit a public consumer app, which needs its own sign-up, so it must be superseded.
  - ADR-004, three repositories, two contracts, a dependency budget, ports 47101 to 47103. The split survives. The budget and "two contracts" don't: media storage and real-time messaging add boundaries.
  - ADR-005, one table and a read-only API role. ADR-006, one endpoint on the standard library. ADR-007, `react` and `react-dom` only. All three are outgrown by a real app. Hard rule 2 (`AGENTS.md`) says never weaken them: supersede them.
- **Requirements that carry over unchanged:** NFR-003 (WCAG 2.2 AA) and NFR-005 (the UI kit), and GR-001 (never store card data), which matters again once shopping arrives.
- **The workspace already expects more repositories:** `workspace.toml` lists `project-data` (pipelines and models) and `project-devops` (infrastructure), which fit recommendations and video processing.
- **Code:** the three Hello World repositories in `git/` (Postgres with plain SQL, a standard-library API, React on Vite with the Prodigy tokens). No code yet for accounts, media, the graph or feeds.
- **Prior brainstorms and plans:** none in `resources/work/`.

## Framings

### Framing A: a release ladder

**Mental model:** one product, grown release by release, the way the reference product itself grew.

**Industry reference:** Instagram's own path: photo feed (2010), video (2013), direct messages (2013), stories (2016), shopping (2018), reels (2020). And user story mapping (Jeff Patton, *User Story Mapping*, 2014), which slices a product into releases across its backbone.

**Sketch:**
- The PRD's brief lists the releases: R0 Hello World (exists), R1 the core social loop, R2 stories and direct messages, R3 short video, R4 explore and recommendations, R5 shopping and ads.
- Each requirement row names its release, so `impact.py` and the ADRs can trace by release as well as by id.
- ADRs are numbered in release order: the foundation first, then each release's own decisions.
- The three repositories carry R0 to R2. R3 (video processing) and R4 (recommendations) bring in `project-devops` and `project-data`.

**Pros:** it reads like a roadmap people already understand, and every release ends in something demonstrable.
**Cons / risks:** the cut between releases is arguable, and cross-cutting concerns (privacy, moderation) belong to no single release.
**Effort guess:** L.

### Framing B: a domain map

**Mental model:** the product is a set of bounded domains, each with its own requirements and decisions.

**Industry reference:** domain-driven design's context maps (Evans, *Domain-Driven Design*, 2003), and Instagram's early Django monolith, split into apps by domain.

**Sketch:**
- The PRD's sections become domains: Identity, Media, Social graph, Feed, Messaging, Discovery, Commerce, Trust and safety.
- One ADR per domain boundary: what it owns, what it exposes, what it never touches.
- Each repository gets one module per domain (`project-be/accounts`, `project-be/media`…), with no imports across domains except through their interfaces.

**Pros:** clear ownership; cross-cutting concerns get a home (Trust and safety is a domain); the code splits cleanly later.
**Cons / risks:** no notion of order, so it says nothing about what to build first; domains drawn before any code tend to be drawn wrong.
**Effort guess:** L.

### Framing C: federated from day one

**Mental model:** the app is one server in an open network, not a silo.

**Industry reference:** Pixelfed (photo sharing on ActivityPub) and Mastodon. W3C ActivityPub Recommendation (2018).

**Sketch:**
- Accounts are ActivityPub actors; following, likes and comments are activities, delivered between servers.
- Feeds merge local and remote posts; moderation works per server and per remote instance.
- Media is fetched and cached from remote servers.

**Pros:** no lock-in, an existing ecosystem, and a distinctive story.
**Cons / risks:** it rewrites identity, feeds and moderation at the root, and remote content brings legal and safety exposure. It is far from "lightweight".
**Effort guess:** XL.

### Framing D: decide at the last responsible moment

**Mental model:** write the whole PRD now, but decide only what the next release needs.

**Industry reference:** Lean software development's "decide as late as possible" (Poppendieck, *Lean Software Development*, 2003). Also the ADR practice of recording decisions when they are made, not in advance (Nygard, 2011).

**Sketch:**
- The PRD is complete, R0 to R5.
- ADRs are written only for R0 and R1. R2 to R5 become backlog entries (`open`), each with its question and a recommended default.
- Each release starts by turning its backlog entries into ADRs.

**Pros:** no premature lock-in; fewer decisions to keep aligned when the PRD changes.
**Cons / risks:** it delivers less of what the seed asks for ("all the ADRs possible"), and later releases look less thought through.
**Effort guess:** M.

## Tensions

| Dimension | A. Release ladder | B. Domain map | C. Federated | D. Last responsible moment |
|---|---|---|---|---|
| Matches the seed ("all the details, all the ADRs") | high | high | medium | low |
| Says what to build first | yes | no | partly | yes |
| Home for cross-cutting concerns | weak | strong | weak | weak |
| Risk of locking in decisions years early | medium | medium | high | low |
| Fits the three-repository, lightweight setup | good | good | poor | good |
| PRD changes that ripple into ADRs | many | many | many | few |

The central tension is between A and B (completeness) and D (deciding late). The recommendation resolves it with **tiering**: foundation and R1 decisions become written ADRs, and later releases become backlog entries that already carry a recommended default.

## Open questions

1. **What is the product called?** — Blocked by: — — Recommended default: keep the "Project Name" placeholder; never Instagram's name or branding.
2. **Native mobile apps, or web only for now?** — Blocked by: — — Recommended default: a responsive web app (installable as a PWA), with native apps as a backlog entry for R2 or later.
3. **How do people sign up?** — Blocked by: — — Recommended default: email and password plus passkeys (WebAuthn), with social login later. Supersedes ADR-002.
4. **Do video and recommendations bring in `project-data` and `project-devops`?** — Blocked by: Q2 — Recommended default: yes, `project-devops` from R1 (deployment) and `project-data` at R4.
5. **How much moderation is in R1?** — Blocked by: — — Recommended default: reporting, blocking and an admin queue in R1; automated image scanning as a backlog entry.
6. **All ADRs now, or foundation ADRs plus backlog entries?** — Blocked by: — — Recommended default: tiered (see the recommended direction).
7. **Public accounts only, or private accounts in R1?** — Blocked by: Q5 — Recommended default: private accounts in R1. Follow requests are cheap early and costly to retrofit.

## Fog of war

- **Legal and regulatory exposure** (GDPR, the EU Digital Services Act, age verification, image rights). It's unclear what applies to a demo-grade deployment. Candidate expedition: a short research brainstorm with the client's legal contact. Forcing event: any public deployment, or OI-003 being answered "yes".
- **Feed ranking.** A chronological feed is simple. Ranked feeds need signals, experiments and `project-data`. Candidate expedition: a spike on a scoring function over likes and recency. Forcing event: R4 planning.
- **Media costs** (storage, transcoding, egress) at even modest use. Candidate expedition: a cost model per thousand users. Forcing event: choosing the cloud deployment target (ADR on deployment).
- **Ads and privacy.** Targeting without tracking is murky ground. Candidate expedition: research contextual-only ads. Forcing event: R5 planning.

## Decision ledger

| ID | Decision | Choice | Rationale |
|---|---|---|---|
| B1 | Scope of the PRD | Full parity, R0 to R5 | The operator asked for every detail before building. |
| B2 | Fate of the sample portal | Replaced; Hello World stays as R0 | One product per master PRD; the walking skeleton already exists. |
| B3 | Repositories | The three Hello World repositories evolve; `project-devops` and `project-data` join later | Keeps the governance model that the demo shows; both are already in `workspace.toml`. |
| B4 | Scale | Demo-grade, scale-aware | Each ADR names what changes at scale (CDN, fan-out on write) without building it. |
| B5 | Identity and look | Own name and the Prodigy UI kit; never the reference product's name, logo or visual design | Like Instagram, not a copy of it. |
| B6 | Superseding, not editing | ADR-002, ADR-005, ADR-006 and ADR-007 are superseded by new ADRs | Hard rule 2: a decision is never weakened to fit a new direction. |

## Recommended direction

**Framing A, the release ladder, with Framing B's domains inside each release, and the ADRs tiered.**

**Why this one:** it gives the operator what the seed asks for (the whole product in the PRD, and a decision for everything) while saying what to build first. The domains from B give cross-cutting concerns (privacy, trust and safety) a home inside each release. Tiering takes the best of D: the decisions that bind the next code are written as ADRs, and the later ones are captured as backlog entries with a recommended default, so nothing is forgotten and nothing is locked in years early.

**What it would produce:**
- **The PRD, master v0.3:** the photo app, R0 to R5, sections grouped by domain, each requirement tagged with its release; the portal's ids removed, and an alignment worksheet for ADR-002 and its backlog and questions.
- **About 11 DRAFT ADRs for the foundation and R1:**
  - consumer accounts and sessions (supersedes ADR-002);
  - the API framework (supersedes ADR-006);
  - the data model and migrations (supersedes ADR-005);
  - media storage: S3-compatible object storage, MinIO locally, uploads straight to storage, image variants;
  - the feed: assembled on read for now, pushed to followers at scale;
  - notifications;
  - privacy and data protection: private accounts, data export and deletion;
  - trust and safety: reports, blocks, the admin queue;
  - the API contract (OpenAPI, versioning);
  - the web app's architecture (supersedes ADR-007; still only the UI kit for style);
  - deployment (`project-devops`).
- **About 7 backlog entries for R2 to R5, each with a recommended default:** stories (expiry), direct messages (real-time transport), short-video processing, explore and recommendations (`project-data`), shopping (payments only through a provider, GR-001), ads, and native mobile apps.

**Why not the others:**
- **B alone** organises well but never says what comes first, so it can't drive a plan.
- **C** is a legitimate product, but it would rewrite identity, feeds and moderation and abandon "lightweight". It belongs in its own brainstorm.
- **D alone** is the most disciplined, but it under-delivers on the seed, which explicitly asks for the decisions up front.

## Not exploring here

- **Federation (ActivityPub)** — a product direction of its own; see Framing C.
- **Monetising creators** (subscriptions, badges, tips) — not in the reference product's first five releases.
- **Live video** — heavier infrastructure than short video; after R5.
- **AI features** (captions, filters, generated content) — they deserve their own brainstorm once media storage exists.

## Next step

`/dev-map photo-sharing-app` — this turned out to be a **program**: six releases, several repositories, months of work and real unknowns. A decision map comes first; this brainstorm's decision ledger and open questions seed its ledger and frontier. Then:
1. Answer open questions 1 to 7, or accept the defaults.
2. Write master PRD v0.3 in Word, sync it with `gov-prd-sync`, and answer the alignment worksheet.
3. Write the foundation and R1 ADRs and the R2 to R5 backlog entries with `gov-adr`.
4. `/dev-plan` for R1.
