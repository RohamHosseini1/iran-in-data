# Iran in Data — Master Design Document

**Project:** Iran in Data (iranindata.org) · byline "Compiled by Roham Hosseini" · CC BY 4.0
**Document purpose:** the single design brief handed to Claude design to produce the visual design,
which then returns to engineering to build. This is the "what and why" (product, content model,
IA, interaction, constraints, art-direction north star) — not final visuals. Where a decision is the
designer's to make, it says so; where a rule is non-negotiable (RTL, confidence honesty,
accessibility), it says that too.
**Status:** v1, 2026-07-13. Written after four research streams (see `docs/frontend/research/`
01–04) + the project owner's direction. Owner requirements of record live in
`docs/frontend/research/00-owner-requirements.md`.

---

## 1. The product in one page

**What it is:** a public-good, bilingual (English + Persian) encyclopedia of the Iranian economy —
from macro (GDP, inflation, exchange rates) down to the hyper-niche (consumption by fruit type,
housing per m², chicken prices), from the early 20th century to today. **~1,789 deduplicated chart
concepts** already exist as clean, cited, machine-readable data. A curated timeline of policies,
wars, revolutions, disasters, and world events overlays the charts, each event–chart link carrying
an honest confidence-of-correlation assessment.

**The ambition:** not "another stats portal." A genuinely **beautiful, intuitive, award-worthy**
(Awwwards-caliber) site that is *also* a rigorous, trustworthy reference. Both things at once.

**Audience — both, deliberately:** a calm, approachable, beautiful surface for the curious public;
real depth (citations, downloads, precise comparison, methodology) one layer down for researchers
and journalists. The design must not force a choice between the two — it layers them.

**What already exists (the design serves this, doesn't invent it):**
- `data/charts/<chart_id>/{data.csv, meta.json}` — uniform, per-chart, frontend-ready. ~1,574
  machine-source charts materialized; ~123 archival charts point at clean processed series.
- Every chart carries **real, linked source citations** (`citations_json`, ~98.9% coverage).
- **Currency variants**: money charts have nominal-USD and real-2015-USD variants (`currency_display`
  in meta). Real is the default.
- **Comparator countries**: Korea, Turkey, Saudi Arabia, Venezuela, Argentina, USA, USSR/Russia,
  Germany, France, UK, Italy, Spain, Netherlands, Sweden, Portugal, Greece — **available per-chart,
  variably** (a chart shows only the comparators that actually have data for it).
- **Timeline layer**: `timeline/*.csv` (Iran ~105 events + comparators), and
  `POLICY_CHART_CORRELATIONS` — confidence-scored (1–5) event↔chart links with written
  justification + caveats, currently on ~30–40 flagship charts (schema extends to more later).
- **Categories**: ~89, mechanically derived — these are NOT the final nav taxonomy (see §6).

---

## 2. Design principles (the north star)

Six principles, in priority order. Every screen should be checkable against these.

1. **Iran is always the hero.** Visually, structurally, editorially. Comparators are context and
   never compete for attention. The whole site is about one country in depth.
2. **Beautiful and clean first — Swiss backbone, human warmth.** International-Typographic-Style
   discipline (a real grid, precise type, generous whitespace, ruthless restraint) as the skeleton —
   but warm, inviting, and a little experimental on top, never cold, robotic, or "dashboard." This
   is a design project meant to win awards, not a corporate BI tool. **No monospace type, no
   terminal/command-line motifs, no faux-liveness.**
3. **In-between, not any one genre.** Not purely editorial (too soft), not purely technical (too
   cold), not purely art-directed (too inconsistent at 1,800-chart scale). A confident blend.
4. **Trust is a feature.** Provenance is always visible and one click from any number — never a
   footnote. Confidence is expressed honestly (never overclaiming causation). This is what separates
   an encyclopedia from a pretty infographic.
5. **Never a wall of charts.** No screen ever dumps 1,800 undifferentiated items. Always structure,
   preview, and multiple ways in.
6. **Bilingual and RTL are design inputs, not a translation layer.** Persian is a first-class mode,
   designed for — not English with the strings swapped.

---

## 3. Art direction

The owner's steer: *"clean, beautiful, almost Swiss; not mono, not robotic; not purely art-directed,
editorial, or technical — some in-between; experimental; Awwwards-worthy."* This section gives the
designer a north star **with deliberate latitude to explore** — treat it as a starting brief, not a
locked spec.

### Identity concept
A **contemporary Persian archive**: the precision and calm of Swiss design meeting a warm,
distinctly Iranian material sensibility (textile, tilework, paper, pigment — abstracted, never
kitsch or literal "Persian-carpet" pastiche). The result should feel like a beautifully art-directed
national data archive — spacious, confident, quietly expressive. Kontinentalist's philosophy is the
right temperature reference: *dignified, warm, approachable, not clinical.*

### Typography
- **Primary typeface: Yekan Bakh** (owner holds the full commercial + web-embedding license; font
  files to be provided at build for woff2 subsetting). It carries both Persian and Latin, which keeps
  the bilingual experience visually unified — a real advantage over stitching two unrelated fonts.
  Use its weight range for hierarchy.
- **No monospace anywhere.** Where the research suggested a mono "provenance/ledger" treatment for
  numbers/metadata, replace it with **tabular (lining) figures in Yekan Bakh** — precise numeric
  alignment without the robotic feel the owner explicitly rejected.
- Discipline (from OWID/FT): a display treatment for headlines/hero titles; a quiet, small, neutral
  treatment *inside* charts so 1,800 charts don't each shout a different type personality. Chart
  labels are furniture, not expression.
- The designer may introduce a secondary display/experimental face for hero moments if it elevates
  the Awwwards ambition — provided Persian coverage and legibility hold, and it never leaks into
  chart internals.

### Color
- Derive a **bespoke, warm, slightly desaturated palette** from Persian material culture (e.g. a
  paper/cream base; accents in terracotta, saffron/ochre, deep teal/turquoise, indigo — abstracted,
  tested, tasteful). Explicitly **not** the default D3/Tableau-10 rainbow (reads generic instantly).
- **Iran gets one signature, saturated hero color** reserved for it alone. Comparators render in
  **muted neutrals at low opacity**. This single rule — hero color for Iran, quiet greys for the
  rest — does most of the "Iran is the hero" work automatically and scales across the whole corpus.
- Must pass accessibility: color-blind-safe, ≥3:1 for marks / ≥4.5:1 for text, and **never encode
  meaning by color alone** (pair with direct labels / line style / shape). One shared, tested palette
  token set, not per-chart choices.
- Light theme is the primary/default (a warm light, not stark white). A dark theme is optional/nice-
  to-have, not required, and must never resemble the rejected "intelligence dashboard."

### Grid & layout
- A visible, confident **Swiss grid** as the organizing logic — columns, baseline rhythm, clear
  margins. Structure the visitor can feel. Generous whitespace is part of the beauty, not wasted space.
- Restraint over density: this is the opposite of Bloomberg-terminal density. Let charts and single
  ideas breathe.

### Motion (tasteful, purposeful — never gimmick)
- The owner liked the reference's sense of **"aliveness."** Deliver it *honestly*: charts **draw
  themselves in** on load/scroll (once, ~300–500ms), hover/focus states respond immediately and
  smoothly, panels slide/cross-fade with calm easing (~140ms ease-out; no bouncy springs — this is
  trust-critical). Motion says "this is real data being rendered," not "look at me."
- **Respect `prefers-reduced-motion`** everywhere; any looping/auto-animated chart needs a
  pause control.
- Explicitly forbidden: fake terminal logs, "LAST SYNC / handshake / node" copy, blinking cursors,
  simulated real-time monitoring. Our data is mostly annual/periodic — pretending it's live is both a
  credibility risk and the wrong aesthetic. Show honest vintage instead ("latest available: 2024").

### Experimental latitude
The owner wants this to be a *design project*, not a template fill. Encouraged: a signature
homepage moment, an inventive era/timeline explorer, expressive-but-legible data-ink, a distinctive
Persian-informed identity system. The guardrail is only that experimentation must not break
legibility at 1,800-chart scale, the RTL/bilingual rules (§8), or accessibility (§9).

---

## 4. Information architecture — multiple front doors

**Core decision (strongly supported by research):** never funnel 1,800 charts through one page.
Provide **parallel ways in**, all feeding the same chart component. This is how OWID, Eurostat, and
Trading Economics each cope with scale, and it directly serves the dual audience.

The front doors:

1. **Homepage / "Start here"** — the curated, credibility-establishing entry (see §7, Screen A).
2. **Browse by theme** — a narrative, public-facing path: ~10–12 human-meaningful top-level themes
   (see taxonomy note below), each a landing page mixing short context with flagship charts, drilling
   into the full set for that theme. This is where a first-time non-researcher lands.
3. **Researcher catalog — the browse-list + Inspector** (the owner's favored master-detail pattern;
   see §7, Screen B). This is where the list+inspector idea lives — as *one* door for power users,
   not the whole site's architecture. It scales to 1,800 only with search + real facets doing the
   work before the list renders, and with a live mini-preview on every row (never text-only).
4. **Era / Timeline explorer** — a signature, project-unique door: scrub Iran's history (Qajar tail →
   Pahlavi → Revolution & War → Reconstruction → Reform → Sanctions era → present), see the charts
   and events for each period. Reuses the existing timeline + correlation data. No other stats site
   has this because none is organized around one country's political history — lean into it (§7,
   Screen C).
5. **Global instant search** — present on every page, search-as-you-type across titles/descriptions/
   tags with a live mini-preview per result, bilingual-aware. The fastest path for someone who knows
   what they want ("fruit consumption by province"). Should not require navigating any taxonomy.

**Taxonomy note (a real task for the design/IA phase):** the existing ~89 categories are mechanically
derived and must NOT be the top-level nav. Collapse them into ~10–12 intuitive top-level themes
(illustrative: *Macro & Money · Trade & Sanctions · Oil & Energy · Agriculture & Food · Industry &
Mining · Population & Society · Health · Education · Labor & Living Standards · Infrastructure ·
Governance & Politics · Environment*), with the 89 surviving as second-level facets. Orthogonal
facets that matter for this project specifically: **era** (the historical periods above) and **chart
altitude** (macro / sector / niche — so a GDP chart and a fruit-consumption chart never compete in
one undifferentiated list). The Persian-mode taxonomy should be validated in Persian, not assumed to
be a 1:1 mirror of the English grouping.

---

## 5. The chart — anatomy & the control system

Every chart is one reusable, world-class component. Getting this right once is most of the product.

### Chart-detail anatomy (top → bottom)
1. **Title** (cleaned, human — not the raw WDI code) + one-line plain-language description of what it
   shows.
2. **Persistent summary strip** (adapted from the reference's tally strip, honestly): latest available
   value, change since a reference year, and — when comparison is on — Iran's rank among the shown
   comparators. Always states vintage ("latest available: 2024"), never fakes liveness.
3. **The chart itself** — Iran in its signature hero color, big and central.
4. **The control bar** — the toggle system (below).
5. **Provenance / "Learn more about this data"** — always-visible source citation(s) with links, plus
   an expandable methodology/notes panel (OWID's single most transferable pattern). This is a
   first-class UI element, never a footnote.
6. **View switch** — line / table / (map, where geographic) / bar, so the same data serves
   time-series, lookup, and comparison. The **data-table view doubles as the accessibility
   alternative** (§9).
7. **Related charts** — 3–5 live-preview cards (same category/era) to keep the visitor moving.
8. **Download** — this chart's data (CSV) + image, tying into the bulk-download packaging.

### The control / toggle system (a reusable toolkit)
Design a **small set of well-designed, reusable control types** the platform knows how to render;
each chart's `meta.json` declares which it supports. The "coolness" the owner wants is that each
chart surfaces exactly the controls that fit its subject — tailored, not generic — from a consistent
kit (so it never feels random). Control types:

- **Currency** — `Nominal` / `Real (2015 USD)`, a visible two-state segmented pill (never a hidden
  dropdown — the reader must *notice* an adjustment is applied). Default **Real**. Mandatory on any
  money chart.
- **Comparison countries** — **off by default (opt-in)** per the owner. A clear `Compare countries +`
  control; when engaged, the available comparators fade in at **low opacity** with Iran still bold on
  top. The comparator set is per-chart (only those with data). Let the user pick which comparators
  (don't force all at once).
- **Calendar** — Gregorian / Solar Hijri (Jalali) / Solar Imperial, applied to every date/year shown.
  A pure display transform (§8).
- **Per-capita vs. absolute**, **index-to-100 vs. raw**, **linear / log**, **share-of-total (%) vs.
  level**, **time-range + optional smoothing** — offered where meaningful for the subject.
- **Contextual controls** — derived from the chart's own data dimensions: "by fruit type," "urban vs.
  rural," "official vs. parallel FX," "by province," "by gender," etc. These come from the data, and
  are what make a chart feel bespoke.

Design goals for the control bar: consistent placement and behavior across all charts; visually
quiet until used; obvious current state (especially currency and calendar, which change the numbers a
reader might screenshot or cite); identical between EN/FA except for RTL mirroring.

### Comparator rendering rules (important, from the owner)
- Iran: signature hero color, full weight/opacity, always on top, always labeled.
- Comparators: muted neutral, low opacity, thinner — present for visual context only, never
  out-contrasting Iran.
- Never fabricated: a comparator simply doesn't appear on charts where it has no data; its absence is
  silent (blank), not interpolated.

---

## 6. Signature feature — timeline events & confidence

This is the feature that makes the site distinctive and is the direct home of the owner's reference
(hover-a-node → animated rich detail panel). It appears both as an **overlay on individual charts**
and as the standalone **Era/Timeline explorer** (Screen C).

### Event markers on a chart
- **Two geometries by event type:** *point events* (a decree, assassination, single-day disaster) =
  a small marker on the exact x-axis date with a thin guideline to the data; *range events* (war,
  sanctions regime, drought) = a pale full-height background band (FRED-style), marker only at the
  start. Markers are **desaturated at rest**, gaining emphasis only on interaction or when most
  relevant to this chart. Cluster dense periods (1979, 2018, 2022) into an "N events" pin that
  expands, rather than colliding labels.
- **Importance ≠ confidence:** a major historical event may have *low* correlation confidence for a
  given chart. The UI must show "major event, low relevance to this chart" without it reading as a
  contradiction (small caption: "how much this event explains the pattern in *this* chart").

### Progressive disclosure — three tiers (this is the reference's mechanism, warmed up)
1. **At rest:** markers only; the single most narratively important event per chart may keep an
   always-on label (research: assume no one hovers).
2. **Hover / focus / tap:** a lightweight callout — title + one line + the confidence badge — fades
   and slides in (~140ms, calm easing). Keyboard focus triggers it identically to hover.
3. **Click / select:** the full **Inspector panel** slides in (right on desktop, bottom sheet on
   mobile), **pinned** (does not dismiss on mouse-out, so the reader can compare the marked date
   against the line). Contents: event title + date/range; the honest confidence badge + caveat (below);
   a mini sub-chart that **draws itself in** (~400ms) showing this series zoomed around the event; the
   full description; **Related events** and **Related charts** rows; a close control. Switching to
   another marker cross-fades contents rather than closing/reopening.

The "alive" feeling the owner liked comes from this choreography (smooth reveal, the self-drawing
sub-chart, immediate responsive states) — **not** from terminal/monospace theater.

### The confidence metric — display (trust-critical; non-negotiable rules)
Research is emphatic: people read *any* event-marker-next-to-a-bend as causation regardless of
disclaimers elsewhere. Therefore:
- **A two-part ordinal badge, never a single percentage** (adapting the IPCC confidence/likelihood
  split):
  - **Strength of association** — how strong the co-movement looks in *this* series around the event
    (e.g. 5-point word scale: none / weak / moderate / strong / very strong; from a documented rule).
  - **Attribution confidence** — how much documented expert/historical consensus says *this event*
    (not confounders) explains it (e.g. speculative / contested / plausible / well-documented).
- **The plain-language caveat sentence sits inside the same visual unit as the badge, always** —
  never a separate footnote. (Our data already stores `justification` + `caveats` per correlation.)
- **No traffic-light red/green** (implies good/bad rather than known/unknown) — use a muted, neutral
  ordinal treatment (e.g. filled segments).
- **Expose the assessment provenance** ("assessed against IMF/CBI data + N secondary sources; see
  citations"), mirroring how FRED publishes its recession-dating methodology, so any researcher can
  audit why a level was assigned.

### Events are first-class entities
An event exists once and is referenced by many charts (not re-authored per chart). "Related charts"
= other charts referencing the same event; clicking one navigates there with the event pre-selected.
This keeps editorial effort scaling with the number of *events* (dozens–hundreds), not *charts*
(~1,800).

---

## 7. Key screens (mock-ready)

### Screen A — Homepage / "Start here"
A single, beautifully art-directed scrolling page scoped to one country. Slim header (wordmark;
EN/FA toggle; persistent search that expands to an instant-search overlay). A short, confident
mission statement. A **Flagship charts rail** (~12–16 hand-picked cards, each a *live* mini-chart —
not a static image — with cleaned title, one-line description, source tag). A **Browse-by-theme grid**
(~10–12 large tiles, each with a representative micro-viz + chart count). An **Explore-by-era band**
(a clickable horizontal timeline strip, labeled in the active calendar) leading into Screen C.
Footer: About, Sources/Methodology, Bulk Download, license, EN/FA. This screen is the biggest
Awwwards opportunity — it should feel like an invitation, signature and warm, while staying clean.

### Screen B — Researcher Catalog (browse-list + Inspector)
Desktop: two panels (stacks with a back-button on mobile / narrow RTL). **Left = list:** search-as-
you-type (bilingual placeholder) with live results; a **facet rail** — Category (12 themes →
sub-categories, live counts, multi-select), Era (the periods), Scale (macro/sector/niche); then the
row list, each row a compact card with a **live mini-preview** (~60×40 sparkline) + title + one-line
description + source/updated/category chips. It **defaults to the flagship subset**, never a raw
1,800 wall, with an always-visible "showing N of 1,800 · clear filters" state so the user always
knows where they are. **Right = Inspector:** the full chart component from §5 (view switch, control
bar, provenance, related charts). This is where the calendar/currency/comparator complexity
concentrates — one surface to perfect.

### Screen C — Era / Timeline Explorer
The signature, non-master-detail screen. A full-width **scrubbable timeline** across the covered years
(~1900s–present), banded and color-coded by era, labeled in the active calendar. Event markers
overlaid (from the timeline data); hover shows a label, click opens the event Inspector (§6) listing
the confidence-scored charts linked to that event. Below, a selected era/event populates a row of
live-preview chart cards (e.g. scrubbing to 1979–81 surfaces FX, oil-export, and consumption charts
with visible breaks). Reuses the same chart-card and Inspector components as Screen B.

---

## 8. Bilingual / RTL / calendar / numerals — the rules (mostly settled)

These came back with clear, evidence-backed answers (research doc 04). Treat as rules unless the
owner overrides.

- **Language toggle:** direct EN⇄FA toggle (no dropdown for two languages), **no flags**, each option
  labeled in its own endonym ("English" / "فارسی"). Persisted; `/en/` + `/fa/` routes for shareable/
  indexable URLs. Header mirrors automatically via logical CSS in RTL.
- **RTL:** full layout/chrome/legend/label mirroring in Persian mode via logical CSS properties
  (`margin-inline-start`, `dir="rtl"`), **but do NOT flip the time/ordinal chart axis** — keep
  temporal and continuously-ordered axes left-to-right in *both* languages (matches neutral
  institutional publishers like BBC/CNN Arabic, and keeps our charts comparable to the LTR
  international sources we cite). **Categorical bar charts** (no inherent order) **do** fully mirror.
- **Numerals:** **Western digits (0–9) everywhere a number is data** — axes, tooltips, tables,
  exports — in both languages (avoids ۴/۵/۶ misread risk, screen-reader inconsistency, and a second
  render path). Persian digits only for decorative prose, if at all.
- **Font:** Yekan Bakh (owner-licensed), carrying both scripts.
- **Calendar:** a persisted global preference in the header (Gregorian default in EN, Solar Hijri
  default in FA; **Imperial always opt-in**), applied everywhere as a pure display transform, plus a
  small per-date "compare calendars" affordance so a reader can check the other systems without
  switching global state. Use a real Jalali library, not hand-rolled conversion.
- **Currency:** per-chart segmented pill (not global), Real default, state always visible; identical
  in both languages (it's data-layer, not language-layer).

---

## 9. Accessibility (WCAG 2.1 AA — must-haves)

Non-negotiable for a public-good reference; a few are true blockers:
1. **A data-table alternative for every chart** (the "table" view doubles as this) — alt text alone is
   insufficient beyond the simplest chart. We already have the tabular data.
2. **Contrast:** marks ≥3:1, text ≥4.5:1 — verified in light theme, any dark theme, and RTL.
3. **Never color alone** — pair every series with direct labels / line-style / shape.
4. **Color-blind-safe shared palette** (one tested token set, not per-chart).
5. **Full keyboard navigation** of every interactive control (event markers, toggles, view switch,
   search) with visible focus rings ≥3:1 and no traps. Event-marker callouts appear on `:focus`
   identically to `:hover`.
6. **`prefers-reduced-motion`** respected on every animation; pause control on any auto-animating
   chart.
7. **Meaningful screen-reader descriptions** — state metric, unit, date range, and source, not a
   generic "line chart."
8. A short **key-takeaway caption** near each chart aids screen-reader and quick-scan users alike.

---

## 10. Open decisions for the owner (to resolve during/after design)

1. **Final top-level taxonomy** (the ~10–12 themes) — needs a proper IA pass; §4 is illustrative. Best
   done with the real category list in hand, and validated separately in Persian.
2. **Dark theme** — build one or ship light-only for v1? (Light is the confirmed default either way.)
3. **How many flagship charts** to feature on the homepage, and which (the ~38 correlation-scored
   charts are the natural pool).
4. **Comparator picker default** — when a user opts into comparison, do we pre-select a sensible
   default set (e.g. Turkey + Korea) or start empty? (Off-by-default overall is decided.)
5. **Narrative "explainers"** — do we want a handful of guided data-essays ("The 1979 Revolution in
   12 charts") as extra front doors, or catalog + timeline only for v1?
6. **Confidence coverage** — the two-part badge is designed; the underlying correlation data currently
   covers ~30–40 flagship charts. Decide whether the badge appears only where assessed (recommended)
   vs. some "not yet assessed" state elsewhere.

## 11. Non-negotiables recap (so nothing regresses in design)
- Iran is the hero; comparators muted, low-opacity, opt-in, per-chart, never fabricated.
- No monospace, no terminal/intelligence-dashboard motifs, no faux-liveness.
- Provenance always visible; confidence always honest (two-part ordinal + caveat, never a lone %).
- Never a wall of 1,800 charts; always structure + preview + multiple entry points.
- RTL: mirror chrome, keep temporal axes LTR; Western digits for data; Yekan Bakh.
- WCAG 2.1 AA, including a data-table alternative per chart.

---

## Appendix — research basis
Full detail behind every recommendation here lives in:
- `docs/frontend/research/00-owner-requirements.md` — owner's requirements of record.
- `docs/frontend/research/01-discovery-navigation.md` — 12 reference sites, IA, the multi-front-door
  model, 3 screen specs.
- `docs/frontend/research/02-timeline-events-confidence.md` — event-annotation + confidence patterns,
  the three-tier interaction, uncertainty-viz best practice.
- `docs/frontend/research/03-aesthetics-and-reference-analysis.md` — 15 aesthetic references, the
  candid teardown of the Overwatch reference (keep the skeleton, drop the costume).
- `docs/frontend/research/04-bilingual-rtl-accessibility.md` — the RTL/numeral/calendar/font/a11y
  rules with their evidence base.
</content>
