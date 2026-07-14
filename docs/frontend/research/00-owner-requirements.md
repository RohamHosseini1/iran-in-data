# Iran in Data — Owner Requirements (frontend design session)

Verbatim intent captured from the project owner (Roham) during the 2026-07-13 frontend-design
kickoff. This is the source-of-truth requirements list the master design document must satisfy.
Keep appending as more requirements arrive ("more on that later" items are flagged).

## Session framing
- Deliverable of THIS session = research + a **master DESIGN document** only. Flow: owner hands the
  doc to Claude *design* → visual design produced → handed back to me to BUILD. **Design-first, no
  tech-stack decision now, no code this session.**
- Audience = **both** the general public and researchers. It is a public-good **encyclopedia**
  (approachable surface, real depth/citations/downloads underneath).
- Goal: beautiful, intuitive, fun, **award-worthy**. But it stays a legible, trustworthy encyclopedia
  — NOT an "intelligence dashboard," NOT a one-off scrollytelling piece.

## Reference site (owner-supplied)
- "OVERWATCH / The Lobby Media" — a US congressional-vote visualizer. Two liked screens:
  1. **Record Queue + Inspector**: searchable/filterable tabular list of records (left) + rich detail
     "Inspector" panel (right) with title, description, a small tally sub-viz, metadata, and a live
     terminal-style "scanning" log.
  2. **Hemicycle**: records as a parliament arc of colored dots, a margin-bar strip across the top,
     left rail of tally/procedural metadata, and **hover a single dot → "Node Inspector"** (member
     photo, district, party, vote, party-alignment meter).
- **What the owner likes = the INTERACTION PATTERNS, not the dark terminal aesthetic**:
  browse-list → inspector; hover-a-single-node → animated rich detail panel; an alive/animated feel;
  always-visible provenance/metadata. The visual style is the designer's call.

## Signature feature: timeline + events + confidence
- Time-series charts overlay a curated timeline of **policies, wars, revolutions, disasters, and world
  events**. Hover/select an event marker → animated detail panel with **title, description, and a
  confidence-of-correlation/causation metric** + justification/caveats, plus related events and
  related charts. Must present confidence **honestly**, never overclaiming causation. (Data layer
  already exists: `POLICY_CHART_CORRELATIONS` + timeline CSVs, confidence-scored with justification.)

## Comparison countries (added 2026-07-13)
- **Per-chart, variable set** — comparators are NOT a fixed list. Each chart shows only the comparator
  countries that actually have data for that indicator; the set differs chart to chart.
- **Optional** — user can toggle the comparison on/off.
- **Iran is always the hero** — highlighted / full emphasis. Comparators render at **lower opacity**,
  purely as visual context; they must never compete with Iran for attention or drive chart inclusion.
- (Consistent with the existing data rule: a chart exists because IRAN has data; comparators fill in
  where available, blank elsewhere, never fabricated.)

## Chart toggle / control system (added 2026-07-13)
- Charts should carry **intuitive toggles matched to their subject matter** — the "coolness" is that a
  chart feels tailored, not generic. ("more on that later" — exact per-chart toggles TBD.)
- **One universal toggle is mandatory**: any money/USD chart has **inflation-adjusted (real) vs.
  nominal**. Real is the default. (Data infra already built: `currency_display` in meta.json.)
- Design implication → build a **standard reusable "chart control" toolkit** the platform knows how to
  render; each chart's meta declares which controls it supports. Candidate control types:
  - currency: nominal / real-USD
  - comparison countries: on/off + which comparators
  - calendar: Gregorian / Solar Hijri (Jalali) / Solar Imperial
  - per-capita vs. absolute
  - index-to-100 vs. raw values
  - linear / log scale
  - share-of-total (%) vs. level
  - time-range selection + optional smoothing
  - **contextual** controls derived from the chart's own data dimensions (e.g. "by fruit type,"
    "urban vs. rural," "official vs. parallel FX," "by province," "by gender").
- Open decisions to resolve in the master doc: default state of comparison (on vs. opt-in), how many
  comparators show by default, how contextual controls are declared in meta.json, control placement/UI.

## Typography (owner decision, added 2026-07-13)
- **Font = Yekan Bakh** (overrides the research's Vazirmatn suggestion). Owner already holds a license,
  it's installed on his machine, and the font files are available to hand over.
- **Owner confirmed he holds the FULL license — web embedding is covered.** No licensing follow-up
  needed. Build-time to-do (not now): get the font files → generate web formats (woff2) + `@font-face`.

## Standing constraints (from data phase, still binding)
- Bilingual English + Persian, RTL for Persian. Three user-selectable calendars. Currency toggle.
- Every chart/data point carries a real, linked source citation (98.9% coverage already).
- Numeral system: Western digits (0-9) for all DATA contexts in both languages (per research); Persian
  digits only for decorative prose if at all. RTL: do NOT flip time/ordinal chart axes; mirror all
  other chrome.
