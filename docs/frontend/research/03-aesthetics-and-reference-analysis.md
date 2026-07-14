# Aesthetics & Reference Analysis — Visual Direction for Iran in Data

**Scope of this doc:** a survey of award-caliber data-viz/editorial-data references, plus a candid
teardown of the owner's own reference screenshot (a dark, terminal-styled US congressional vote
visualizer called "Overwatch," by a studio/outlet called The Lobby — verified live at
`thelobbynews.com/overwatch`), to extract what's structurally worth stealing versus what's a one-genre
skin that doesn't belong on a public economic encyclopedia. Ends with 3 candidate visual directions and
an avoid-list.

---

## 1. Visual-direction survey

Organized by the dimension each reference is strongest on. A reference can appear once but inform
multiple dimensions — noted inline.

### Typography

1. **Our World in Data** (ourworldindata.org) — Body/UI/chart-label typeface is **Lato** (confirmed by
   inspecting computed styles on a live Grapher page: `font-family: Lato, "Helvetica Neue", Helvetica,
   Arial, "Liberation Sans", sans-serif`), a humanist sans that stays legible at the small sizes charts
   demand, paired with a serif (Playfair Display family) reserved for editorial headlines/titles —
   classic serif-display + sans-body pairing that reads "encyclopedia," not "dashboard." **Stealable
   detail:** the discipline of using the display serif ONLY for article-level headlines and never
   inside the chart itself — chart typography stays a plain, quiet sans so 1,800 charts don't compete
   with 1,800 different type treatments.
2. **FT Visual Vocabulary** (github.com/Financial-Times/chart-doctor) — not a typeface choice but a
   **naming/labeling discipline**: every chart type has a plain-English name and a one-line "when to
   use it" caption baked into the taxonomy. **Stealable detail:** apply the same discipline to chart
   metadata — every one of the ~1,800 charts should carry a one-line, human-language caption of what
   it shows, not just an auto-generated WDI-style title (this echoes the "clean up mechanically
   generated titles before translating" note already flagged in project bookkeeping).
3. **Bloomberg Graphics** — uses **Neue Haas Grotesk** (a stricter, more geometric cousin of
   Helvetica) across terminal and web graphics. **Stealable detail:** a slightly more "neutral/technical"
   grotesque than Lato's warmth, worth A/B-ing against Lato if the owner wants the site to read more
   "financial-data-serious" and less "essay."
4. **Pentagram / Deloitte Insights** (pentagram.com/work/deloitte-insights) — bold display type
   layered over a **visible grid system inspired by tax-ledger columns**. **Stealable detail:** a
   literal ledger/grid motif (thin rules, column guides visible as a design element, not just an
   invisible layout grid) is a tasteful way to signal "rigor" typographically without going dark/terminal.

### Color

5. **Federica Fragapane** (federicafragapane.com; profiled by Designboom 2025, "soft forms visualize
   hard facts") — muted, desaturated palette (dusty reds, soft greens, cloudy purples) applied to
   organic/non-Cartesian shapes. **Stealable detail:** a desaturated, "paper-like" palette family
   (as opposed to saturated dashboard neons) that stays legible and calm across 1,800 charts and works
   in both light backgrounds and print/PDF export.
6. **Kontinentalist** (kontinentalist.com) — a color system explicitly "inspired by the warm tropical
   climate of Southeast Asia and commonplace household items," built to feel "friendly, approachable,
   and dignified" rather than clinical, with "a hint of brutalism." **Stealable detail:** the
   *methodology*, not the palette — derive an Iran-specific warm/earthy palette (e.g., referencing
   textiles, pottery, desert/oasis tones) rather than a generic Tableau10/D3-category10 palette, so the
   site has a visual identity distinct from every other stats portal, while explicitly using the same
   "dignity over spectacle" framing Kontinentalist states as its goal.
7. **Nadieh Bremer / Visual Cinnamon** (visualcinnamon.com) — vibrant, high-chroma palettes, but
   always used to encode a *specific variable* rather than decoratively. **Stealable detail:** reserve
   saturated color for the ONE encoding channel that matters per chart (e.g., the series being
   highlighted), keep everything else in a muted neutral — a rule that scales well across a huge
   corpus where most charts are single-series time trends.
8. **Datawrapper's own blog on chart fonts/colors** (datawrapper.de/blog) — pragmatic, tested
   guidance (not aspirational studio work) on what actually stays legible at small multiples scale.
   **Stealable detail:** useful as an engineering-side sanity check once the aesthetic direction is
   chosen, precisely because Datawrapper is optimized for exactly this project's problem — hundreds to
   thousands of similar small charts.

### Motion

9. **Reuters Graphics** (graphics.thomsonreuters.com) — projects like "A window into Delhi's
   pollution" combine a fixed camera feed with live sensor data; motion is used to make an abstract
   number (PM2.5) *legible as lived experience*, not to decorate. **Stealable detail:** for an economic
   encyclopedia, the equivalent move is animating a chart's line drawing-in on scroll/load once,
   tastefully, then stopping — motion establishes trust ("this is real data being drawn," not a static
   image) without becoming a scrollytelling gimmick.
10. **Pudding** (pudding.cool) — interactivity is used to let the reader *drive* comparisons (e.g.
    scrubbing a timeline, selecting an entity) rather than to animate for spectacle. **Stealable
    detail:** the "sparse text, data carries the narrative" ethic — good encyclopedia chart pages
    should default to interactive exploration (hover for values, toggle series) before any prose.
11. **Giorgia Lupi / Accurat "perfectly imperfect"** approach (Eye on Design profile) — intentionally
    avoids sterile "visual standards," favoring slightly hand-touched, warm compositions even in
    corporate data work (IBM guidelines, Deloitte Insights). **Stealable detail:** small, tasteful
    imperfections (rounded corners, hand-adjusted label placement, subtle texture) signal "made by
    people who cared," a useful counterweight to a purely templated 1,800-chart machine feel.

### Layout / composition

12. **Our World in Data — 2023/2024 Grapher redesign** (ourworldindata.org/redesigning-our-interactive-data-visualizations)
    — reorganized controls by *purpose*: view-switcher (chart/map/table) top-left, view-specific
    settings top-right, download/share bottom-right; added an expandable **"Learn more about this
    data"** panel that surfaces the underlying source/methodology inline. **Stealable detail #1:** this
    exact spatial grammar (view controls vs. settings vs. export, spatially separated) is directly
    reusable for a chart-card component used 1,800 times. **Stealable detail #2:** the "Learn more
    about this data" pattern is the single most directly transferable OWID feature for this project —
    visible, always-available provenance/methodology per chart, which is exactly what an economics
    encyclopedia needs and what most "pretty" dataviz sites skip.
13. **FT Visual Vocabulary poster/taxonomy** — organizes chart types into 9 purpose categories
    (deviation, correlation, ranking, distribution, change-over-time, magnitude, part-to-whole,
    spatial, flow). **Stealable detail:** use this exact taxonomy (or a close variant) as the
    *browsing/filtering facet* for the encyclopedia's chart index, layered on top of subject-matter
    categories — lets a visitor browse "how is this shown" in addition to "what is this about."
14. **Urban Institute Data Visualization Style Guide** (urbaninstitute.github.io/graphics-styleguide) —
    a full public style guide from a policy-research nonprofit: fonts, color rules, chart-type do's and
    don'ts, accessibility notes. **Stealable detail:** as a structural template for the design-system
    documentation this project should eventually produce internally (not a look to copy, but a document
    shape to copy).
15. **Voteview.com** (the academic congressional-ideology visualizer, jQuery/D3/DC.js/Bootstrap stack)
    — included deliberately as a *negative* aesthetic reference: functionally rich (NOMINATE ideology
    scores, full roll-call history back to the 1st Congress) but visually dated — dense Bootstrap
    defaults, no real typographic or color system. **Why it's here:** it proves that "encyclopedic
    completeness + academic credibility" and "looks unfinished" often travel together, which is exactly
    the trap this project must avoid while still being the credible, complete resource Voteview is for
    Congress.

---

## 2. The owner's reference, analyzed candidly

The reference is real and live: **thelobbynews.com/overwatch**, "Overwatch — Legislative Intelligence
Platform," described on-page as "Real-time monitoring and historical roll call archival of the 119th
United States Congress. Data synchronized across 435 district nodes." Confirmed live text includes
stat tiles ("TOTAL YEA AGGREGATE," "TOTAL NAY AGGREGATE," "PASSED RATE," "ACTIVE SESSION," "LAST SYNC")
and a dark, monospace, terminal-flavored UI with system-log flourishes ("Establishing handshake with
gov.archives.api"-style copy).

### Transferable patterns (adopt these — they're interaction/IA choices, not skin)

- **Browse-list + rich Inspector split.** A searchable/filterable record list on one side, a detail
  panel on the other with title, description, a small embedded sub-visualization, metadata, and
  provenance — this is structurally *identical* to what a good chart-encyclopedia page needs: a
  filterable index of ~1,800 charts on one side (or as a grid), and a rich detail view per chart with
  title, plain-language description, the chart itself, source/methodology metadata, and related charts.
  This is the single most valuable pattern to keep. It also maps almost exactly onto OWID's own
  "Learn more about this data" panel (ref #12 above) — the two references reinforce each other.
- **Hover/select a node → animated Inspector reveal.** In the Hemicycle screen, hovering one dot opens
  a "Node Inspector" with photo/district/party/vote/alignment meter. For an economic encyclopedia, the
  equivalent is: hovering a country on a map, a bar in a ranking chart, or a point on a timeline should
  smoothly reveal a small inspector card (value, year, source, link to that entity's full chart page).
  Keep the *reveal choreography* (smooth, immediate, spatially anchored to the hovered element) — lose
  the *dashboard-operator framing*.
  - **Note on scope for this project's data model:** Iran in Data doesn't have a natural per-record
    "member of parliament" analog — the closest equivalents are per-country, per-year, or per-indicator
    entities. The pattern still works; it just resolves to entity/time-point inspection rather than
    politician inspection.
- **Live tally strip / margin bar as a persistent summary.** The Hemicycle's top margin-bar and left-rail
  tally give an at-a-glance summary before any interaction. Translated: a chart-detail page benefits
  from a persistent, always-visible mini-summary strip (latest value, % change since a reference year,
  rank among comparators) above or beside the main chart — encyclopedic context without requiring a
  hover.
  - **What this is NOT the same as** — "Overwatch"'s copy explicitly performs *live-ness* ("LAST SYNC:
    52d AGO," "ACTIVE SESSION 02," terminal-log handshake messages) appropriate to an actual live feed
    of ongoing votes. Iran in Data's underlying data is annual/periodic economic statistics, most of it
    NOT live — a persistent summary strip should say what it is (e.g., "latest available: 2024") rather
    than borrow the vocabulary of real-time monitoring, which would misrepresent the data's actual
    cadence and undercut trust with researchers who care about vintage/source dates.
- **Visible provenance as a first-class UI element**, not a footnote — the pattern (not the terminal
  styling) of always showing where a number comes from is worth keeping and, per the OWID reference
  above, is already the industry's best-practice answer for this exact need.
- **A feeling of "aliveness."** The owner likes that the reference doesn't feel like a static
  spreadsheet-to-PDF export. That feeling is achievable through subtle load-in animation, responsive
  hover states, and smooth transitions — none of which require a dark terminal skin.

### Aesthetic-only choices (leave these behind for this project)

- **Dark theme + monospace + terminal/command-line chrome** (blinking-cursor titles like "Overwatch_",
  simulated system logs, "handshake," "node," "session" vocabulary). This is a genre convention for
  *political/surveillance-adjacent* data products — it borrows credibility from a "control room"
  metaphor, which the brief explicitly rules out ("NOT an intelligence dashboard"). For a public
  encyclopedia aimed at general readers as much as researchers, dark-terminal reads as niche/insider
  and actively works against approachability — it is the opposite instinct from Kontinentalist's
  explicit "friendly, welcoming, not intimidating" design goal (ref #6), which is a much better
  temperamental match for this brief.
- **Parliament/hemicycle geometry itself.** A semicircle of colored dots is a shape specific to
  representing a *legislature's seat composition*. There is no natural Iran-economic-data analog to
  "a seat" — forcing chart data into a hemicycle would be decorative rather than meaningful, exactly
  the "flashy one-off" failure mode the brief warns against.
- **Surveillance-adjacent copy and framing** ("Legislative Intelligence Platform," "monitoring,"
  "district nodes," aggregate tallies framed as an ongoing operation). Iran in Data is a reference
  resource, not a monitoring tool; that authorial voice would misrepresent the product and could read
  as politically loaded given the subject matter (Iran) in a way it doesn't for domestic US congress
  data — worth flagging explicitly since tone missteps here carry more risk than in the original genre.

**Net verdict:** keep the *skeleton* (list + inspector, hover-reveal, persistent summary strip, visible
provenance, subtle animation) and discard the *costume* (dark terminal, monospace, command-line
copywriting, hemicycle geometry). The owner's genuine likes map cleanly onto interaction design, not
color/typeface/tone — which is good news, because it means the site can be built to Awwwards-caliber
polish in a completely different, warmer visual language and still deliver everything the reference
demonstrated they wanted.

---

## 3. Three candidate visual directions

### A. "Warm Archive" — editorial-encyclopedia, OWID-adjacent but with an identity

- **Mood:** cream/off-white or warm-paper background, a restrained warm-earth accent palette (terracotta,
  ochre, deep teal — evoking Persian textiles/tilework without being kitsch), serif display headlines
  over a clean sans body and chart labels, generous whitespace, thin ledger-style rule lines.
- **Anchors:** Our World in Data (#1, #12) for structure and trust signals; Kontinentalist (#6) for the
  "warm, dignified, non-clinical" palette philosophy; Pentagram/Deloitte Insights (#4) for the
  ledger-grid typographic motif; Federica Fragapane (#5) for a desaturated, calm color family.
- **Best fit if:** the owner wants "encyclopedia first, beautiful second" to be unmistakable at a
  glance — safest, most credible-reading option, still distinctive because of the custom palette.

### B. "Living Field" — organic, data-humanist, quietly playful

- **Mood:** light background, but charts and category icons use soft, organic forms (rounded, slightly
  hand-touched shapes) instead of rigid bars/grids wherever the chart type allows it; motion is used
  generously but gently (charts breathe in on load, hover states ripple rather than snap).
- **Anchors:** Federica Fragapane (#5) and Giorgia Lupi/Accurat (#11) for organic-shape and
  "perfectly imperfect" philosophy; Nadieh Bremer (#7) for expressive but purposeful color-per-variable;
  Pudding (#10) for reader-driven interactivity over passive animation.
- **Best fit if:** the owner wants the site to feel more like a piece of data-humanism craftsmanship
  (award-bait in the IIBA sense) and is willing to accept a bolder, more art-directed identity — highest
  ceiling for "beautiful," slightly higher execution risk for "stays legible at 1,800-chart scale."

### C. "Field Notes" — structured, grid-forward, quietly technical (closest to honoring the owner's
   original instinct without going dark)

- **Mood:** light or very-light-gray background, strong visible grid/column structure (ledger lines,
  tabular numerals, a monospace or semi-mono accent used ONLY for numbers/metadata, never for prose),
  a cooler restrained palette (ink, slate, one warm accent), sharp small-multiples layout for browsing.
- **Anchors:** FT Visual Vocabulary (#2, #13) for taxonomy-driven browsing and chart-type discipline;
  Bloomberg (#3) for a technical grotesque typeface and numeric rigor; Pentagram/Deloitte Insights (#4)
  for the ledger-grid motif; the "record list + rich inspector" and "persistent tally strip" *patterns*
  from the owner's Overwatch reference (section 2), reskinned in this light, structured palette instead
  of dark terminal.
- **Best fit if:** the owner's real attachment is to the *structured, technical, slightly numeric* feel
  of the reference (not literally its darkness) — this direction keeps that appetite satisfied via
  grid/numeral treatment while staying light, warm-adjacent, and encyclopedia-appropriate.

---

## 4. What to avoid

- **Dark "intelligence dashboard" aesthetics** for the primary site theme — explicitly ruled out in the
  brief, and shown above to be a genre-specific skin borrowed from surveillance/monitoring products,
  not something intrinsic to good dataviz design.
- **One-off scrollytelling as the site's primary mode.** Pudding/Reuters-style single-scroll narrative
  pieces are great for *individual featured essays* the site might publish about specific findings, but
  the ~1,800-chart core of the site needs a *browsable, stable, linkable* pattern (grid/list + detail
  page), not a scroll-driven narrative shell — scrollytelling doesn't scale to an encyclopedia and
  breaks deep-linking/SEO for individual charts.
- **Decorative geometry with no data mapping** (e.g., adopting a hemicycle, radial, or other
  genre-specific shape because it looks striking, without a real one-to-one meaning for the underlying
  data) — a classic "flashy one-off" trap the brief calls out.
- **Category-10 default color palettes** (the default D3/Tableau rainbow) — instantly reads as
  "generic dashboard," undermines the distinct identity every reference studio above works hard to
  establish with a bespoke palette.
- **Simulated liveness on non-live data** — borrowing "LAST SYNC," "session," "handshake" style copy
  (as in the owner's reference) for data that is actually annual/periodic government/institutional
  statistics would misrepresent data freshness — a credibility risk specifically flagged for a
  researcher audience.
- **Burying provenance.** Every reference that reads as *trustworthy* (OWID above all) makes
  source/methodology an always-visible, one-click-away UI element, not a footnote or a separate "About"
  page — skipping this is the fastest way to look flashy-but-unreliable, the exact failure mode the
  brief is trying to avoid.
- **Skipping RTL/bilingual testing on the chosen direction.** Any of the three candidate directions
  above (ledger lines, hemicycle-derived hover patterns, tabular numerals) needs to be explicitly
  checked in Persian/RTL before being finalized — a visual direction that only works LTR is not a
  finished direction, per the project's existing bilingual requirement.
