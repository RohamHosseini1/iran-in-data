# Discovery & Navigation Research — Iran in Data

**Scope:** How best-in-class data-encyclopedia / large-chart-catalog sites solve the "main menu, search,
browse" problem — letting a visitor dig through thousands of charts without feeling lost. Researched
firsthand (live browser inspection) for the top sites, supplemented by web search for the rest.

Context this research is answering to: ~1,800 charts, ~89 categories, macro (GDP/inflation/FX) down to
hyper-niche (fruit-type consumption), bilingual English+Persian (RTL), audience = general public AND
researchers simultaneously.

---

## 1. Ranked shortlist of reference sites

### 1. Our World in Data (OWID) — ourworldindata.org
**Why it matters:** The single closest precedent in subject matter (country-level socioeconomic
indicators) and scale (14,627 charts, 126 topic pages, 32 explorers per the homepage counter) to what
Iran in Data is building. It has solved "the wall of thousands of charts" about as well as anyone.

**Patterns worth stealing** (verified live at `/charts` and homepage):
- **The "Data Catalog" page is a single, filterable, infinite-scrolling grid grouped by topic
  section**, not a flat 1,800-row table. Each topic section (e.g. "Population & Demographic Change")
  shows its own chart count ("2,750 charts →") with a "see all in this topic" link, then a preview
  grid of that topic's charts. Scrolling moves you through topics in sequence; you never face a bare
  number with no structure.
- **Every chart card previews FOUR view-forms of the same data at once**, each a small icon+label
  toggle: Line chart | Data table | World map | Bar chart — plus a live-rendered mini chart, not a
  static thumbnail (e.g., a real sparkline showing "2.493B → 8.092B, 1950-2023"). This single card
  format handles time-series, cross-country comparison, and single-value lookup in one glance, and
  communicates instantly that OWID data is multi-dimensional (country × time), not a static PNG.
- **One search bar, two use modes**: a slim "Search for a topic, chart..." box in the header (site-wide,
  algolia-style instant results), AND a second, larger, more prominent
  "Search for an indicator, a topic, a country, or a keyword…" box that anchors the dedicated
  `/search` (their "Data Catalog") page, paired with a `Select country` pin-icon filter. Two
  entry points, same underlying index, sized for their context (small = "I know what I want, get me
  there fast"; big = "I'm exploring, help me").
- **A single row of 10 pill-style facet tags** directly under the search box ("FILTER BY AREA OF
  RESEARCH: Population & Demographic Change • Health • Energy & Environment • Food & Agriculture •
  Poverty & Economic Development • Education & Knowledge • Innovation & Technological Change • Living
  Conditions, Community & Wellbeing • Human Rights & Democracy • Violence & War") plus a Data/Writing
  radio toggle — this IS their entire top-level taxonomy, kept flat and visible at all times rather
  than buried in a mega-menu.
- Separately, "Browse by topic" in the header nav opens a **full topic tree** (126 topics) for
  people who want the encyclopedia view rather than the catalog/search view — OWID deliberately offers
  both an article-first path (topic pages, narrative + embedded charts) and a chart-first path (the
  catalog above), for the two audiences (public reader vs. researcher).

### 2. Data USA — datausa.io
**Why it matters:** The best example of avoiding a chart catalog entirely by making the **entity**
(place, industry, job, university), not the individual chart, the unit of navigation. Directly
relevant if Iran in Data ever wants "Iran" or a specific province/sector to be a first-class browsable
node rather than just a facet.

**Patterns worth stealing** (verified live):
- **Entity search is the front door**, not chart search: the homepage search box says "Search reports"
  and autocompletes to *things* (a state, an industry, a university), each with a count on the
  homepage ("37,016 Locations," "309 Industries," "650 Jobs," "7,624 Universities" as colored,
  icon-tagged stat tiles) — this reframes "1,800 charts" as "here are the handful of dimensions you can
  slice by," which is far less overwhelming.
- **Every entity resolves to an auto-generated "profile" page**: a hero KPI strip (Texas → 2024
  Population 30.2M, Poverty Rate 13.8%, Median Household Income $78,476, etc., each with a "1-year
  change" delta) followed by **six category tabs** (Population & Diversity, Health, Economy, Civics,
  Education, Housing & Living) that each scroll to a themed cluster of charts about that one entity.
  This turns "1,800 charts" into "~6 tabs × N charts about the thing you searched for" — the catalog
  is never faced head-on.
- **Comparison as a first-class primitive**: an "+ Add Comparison" button sits right in the profile
  header, letting a visitor stack a second entity (another state, another industry) directly against
  the one they're looking at — worth considering for cross-country or cross-era (pre/post-1979)
  comparisons in Iran in Data.

### 3. FRED (Federal Reserve Bank of St. Louis) — fred.stlouisfed.org
**Why it matters:** The purest "researcher power tool" example, and a cautionary tale for what NOT to
do for a general-audience section of the site. Confirms what a true wall-of-records feels like at
scale (845,364 series).

**Patterns worth stealing** (verified live):
- **Faceted left-rail with live counts**, exactly like a classic e-commerce filter: "Concepts" facet
  lists "Persons (110,000+), Employment (96,000+), 5-Year (94,000+), Population (78,000+)..." Each
  facet narrows the result count instantly. This is the "search box + facet filters + row list" pattern
  the project owner referenced, and FRED does it well for a power-user audience — but with **zero
  visual preview**, plain text rows only (title, units/frequency line, date range, "last updated N
  minutes ago").
- Checkboxes on every row feed into **bulk actions above the list**: "Add to Data List / Add to Graph
  / Add to Dashboard" — a multi-select-then-act pattern that a "Browse + Inspector" UI could reuse
  (select several charts, then "compare," "export," or "add to a custom collection").
- **What to avoid**: searching one common term ("inflation") returns 27,329 results with no
  thumbnails and no case for why the first result outranks the second beyond "Sort by Relevance" —
  for a lay visitor this is instantly overwhelming. FRED gets away with it because almost nobody
  browses this page cold; they arrive via a specific, pre-qualified search term or a direct link from
  a release page. This is a real risk for Iran in Data's ~89-category browse if it's the ONLY route in.

### 4. World Bank DataBank — databank.worldbank.org
**Why it matters:** A dated but structurally instructive analogue to Iran in Data's scope (multiple
databases/topics, mixed audience), useful as a "how much chrome is too much chrome" reference.

**Patterns worth stealing** (verified live):
- **"Explore databases" search box + two facet dropdowns (Topic, Source) + three sort modes (Most
  Used, Alphabetical, Last Updated)**, plus a literal **"Database preview: ON/OFF" toggle switch** that
  turns on inline previews next to each list row — an explicit, user-controlled way to trade list
  density for visual context, which could map to a "compact list / preview cards" view toggle in an
  1,800-chart list.
- **A "What's Popular" sidebar module** with its own internal tabs (Indicators / Countries) listing
  the top 5-8 most-viewed items — a cheap, effective way to give a lost visitor a starting point
  without them typing anything.
- **What to avoid**: the overall visual design is text-dense 2012-era enterprise UI; it functions but
  doesn't delight, and a first-time visitor cannot tell what's inside a "database" without clicking in.

### 5. Gapminder — gapminder.org / gapminder.org/tools
**Why it matters:** The best example of a **radically reduced entry point** for the general-public
side of a mixed audience: instead of browsing/searching a catalog, you pick one of ~7 named
visualization tools (Bubbles, Income Mountains, Maps, Ranks, Trends, Ages, Dollar Street) and every
one of ~500 underlying indicators is reachable as a dropdown *inside* that single, already-open,
already-animating chart.

**Patterns worth stealing:**
- **Tool-first, not chart-first, navigation**: pick a form of interaction (animated bubble chart over
  time, ranked bar chart, map) before picking a topic — inverts the usual "pick topic → get chart"
  flow and works because the interaction itself IS the hook for a lay audience.
- **In-chart indicator switching**: once inside a tool, changing "what indicator is on the Y axis" is
  a dropdown inside the visualization, not a return trip to a catalog — keeps a curious user in flow.
- **What to avoid**: this pattern doesn't scale to "I want the exact fruit-consumption-by-province
  chart" lookup — it's discovery-by-play, not lookup-by-name. Good for casual public exploration of
  macro indicators, weak for a researcher who needs one specific niche series (needs a companion
  search/catalog, which Gapminder does also provide separately).

### 6. Trading Economics — tradingeconomics.com
**Why it matters:** Shows the "matrix/heatmap + two orthogonal list browses (by country, by category)"
pattern common to financial-data terminals, at genuine scale (20 million indicators, 196 countries).

**Patterns worth stealing** (verified live, partially — cookie wall limited full inspection):
- **Two independent, symmetric entry lists**: `/countries` (browse by country) and `/indicators`
  (browse by category — GDP Growth, Interest Rate, Inflation Rate, Unemployment Rate, Balance of Trade,
  etc., in a starred "Main Indicators" shortlist above the full alphabetical category list) — the same
  data reachable from either axis, which matters for Iran in Data since a visitor might think "show me
  everything about trade" OR "show me everything from 1979-1989."
  - Iran in Data's macro-to-micro range (GDP down to fruit consumption) maps well to a similar
    dual-axis idea: browse by **category** (89 of them) or by **era/decade** (Pahlavi / Revolution /
    War / Reform / Sanctions-era, etc.) as two independent front doors into the same 1,800 charts.
- **A heatmap/matrix view** (`/matrix`) as a third, purely visual entry point: countries × indicators
  grid, colored by value or by recent change — a dense but scannable "everything at once" overview,
  good inspiration for a single "state of the Iranian economy" overview screen.
- **What to avoid**: extremely dense, text-first, dated visual design; a consent/paywall-heavy
  experience; not a model for aesthetics, only for the underlying two-axis browse structure.

### 7. Observable — observablehq.com
**Why it matters:** Best example of **"trending/popular" as its own discovery surface**, and of
letting user-made **collections** (curated sub-groupings) exist alongside the official taxonomy — a
possible model for "editor's picks" or "flagship charts" surfacing inside Iran in Data's own catalog
(the project already has a notion of ~38 "flagship charts" with policy-timeline correlations, per
existing bookkeeping — Observable's model validates giving those a dedicated discovery lane).

**Patterns worth stealing** (via search-verified secondary sources):
- A dedicated `/top` page surfacing trending + most-popular content as its own discovery lane,
  separate from search — good for a homepage "start here" rail distinct from the full catalog.
- **Collections**: nestable, named groupings of notebooks/content that sit alongside (not instead of)
  the formal taxonomy — lets curators hand-pick "10 charts that explain the 2018 currency crisis"
  without restructuring the category tree.
- Instant, boolean-capable search-as-you-type across all public content from a single global search
  box present on every page.

### 8. Eurostat — ec.europa.eu/eurostat
**Why it matters:** A government statistical agency's answer to the same problem at even larger scale
(9 statistical "themes," thousands of dataset codes), useful for the "official, credible, slightly
bureaucratic" register that a serious economic-data site sometimes needs to hit for researcher trust.

**Patterns worth stealing** (via search-verified secondary sources):
- **Two parallel gateways to the same underlying datasets**: "Statistics Explained" (an
  encyclopedia-style, narrative wiki gateway — read an article, see embedded charts, click through to
  the live dataset) vs. the raw "Database" (direct dataset-code browsing/download for people who
  already know what they want). This narrative-vs-raw split maps directly onto Iran in Data's stated
  dual audience (general public wants the story; researcher wants the series).
  - "Statistics Explained" also nicely models a *thematic hierarchy* (9 themes → sub-themes → article
    → embedded chart → link to live data) as an alternative to a flat category list, worth considering
    for the 89 categories if some can be nested under a handful of macro themes.

### 9. Kontinentalist — kontinentalist.com
**Why it matters:** The best design-forward example of a *regional* (Asia-focused) data-storytelling
outlet — closest in spirit to a country/region-specific project like Iran in Data rather than a
global aggregator, and explicitly about making a specific region's data feel "humanised" rather than
like a spreadsheet dump.

**Patterns worth stealing** (via search-verified secondary sources):
- Design language deliberately drawn from the region's own visual culture/iconography rather than a
  generic international-tech aesthetic — directly applicable: Iran in Data's Persian-mode UI (and even
  its English-mode chrome) could draw on Persian typographic/ornamental tradition rather than defaulting
  to a generic Western dashboard look, reinforcing the bilingual identity rather than treating Persian
  as a translation layer bolted onto an English design.
- Story-first packaging of data (scrollytelling long-form pieces built from many individual charts)
  as a *complement* to a raw catalog — a possible pattern for turning clusters of Iran in Data's niche
  charts into a handful of narrative "explainers" (e.g. "The 1979 Revolution in 12 charts") that serve
  as guided front doors into the wider catalog.

### 10. The Pudding — pudding.cool
**Why it matters:** Demonstrates that a data-heavy publication can succeed with almost no formal
taxonomy at all — relevant mainly as a **counter-example** for what Iran in Data should NOT copy, given
its scale.

**Patterns worth stealing / avoid:**
- No central editorial planning or rigid category structure; relies on a simple reverse-chronological
  archive/index and strong per-piece visual design to carry each story.
- **This works at their scale** (dozens to low hundreds of pieces) and fails at Iran in Data's scale
  (1,800 charts) — flagged explicitly as a pattern NOT to imitate for the primary catalog, though its
  visual-essay format is a good model for the "narrative explainer" idea borrowed from Kontinentalist
  above.

### 11. Datawrapper River — river.datawrapper.de
**Why it matters:** A genuinely novel discovery mechanic worth knowing even though it solves a
different problem (chart *syndication* between publishers, not visitor-facing catalog browsing).

**Patterns worth stealing** (via search-verified secondary sources):
- A reverse-chronological "feed" of newest charts, with a hand-curated "Our River favorites" lane
  sitting alongside the raw feed — again the "raw + curated" dual-lane pattern (see Observable,
  Kontinentalist) recurring across very different products, suggesting it's a genuinely load-bearing
  idea, not a one-off.
- Keyword search across the feed for topic-specific chart-hunting.
- Lower priority for Iran in Data specifically since the "syndication to other publishers" use case
  doesn't apply, but the curated-favorites-lane idea is directly reusable.

### 12. Statista — statista.com
**Why it matters:** The most commercially mainstream example of topic-hub navigation at huge scale
(hundreds of thousands of statistics/charts across industries), useful for its mega-menu-by-industry
pattern even though its freemium paywall and ad-heavy design are anti-patterns.

**Patterns worth stealing / avoid** (general knowledge, site's own cookie wall blocked live
inspection this session):
- Topic hub pages ("Industries" mega-menu → topic page → ranked list of statistics on that topic →
  individual chart page) is a clean three-level drill-down that scales to enormous catalogs without a
  single "browse everything" wall page ever being the primary route.
- **What to avoid**: paywalling most individual charts behind a login/subscription prompt is directly
  contrary to Iran in Data's public-good mission, and the page-level ad density undermines trust for a
  research-oriented visitor — useful as a "how not to monetize/clutter" reference, not a UX model to
  copy visually.

---

## 2. Recommended IA / navigation approach for Iran in Data

**Core recommendation: don't force 1,800 charts through one browse surface. Give visitors 3-4 parallel
front doors into the same underlying set, the way Eurostat, Trading Economics, and OWID each do — and
reserve the literal "browse list + inspector" master-detail view for ONE of those doors (the
researcher/power-user one), not as the whole site's architecture.**

### Does the "browse list + inspector" idea scale to 1,800 charts? Yes — but only as the researcher
lane, and only with search + facets doing the heavy lifting before the list ever renders.

FRED and World Bank DataBank prove the pattern (search box + facet filters + text row list + detail
panel) genuinely works at 100,000+ record scale for a researcher audience, **provided**:
1. The list is never shown "empty of intent" — i.e., it should not default to all 1,800 rows on
   page load. Default to either (a) a starting facet already applied (e.g., last-viewed category), or
   (b) the "popular / flagship" subset (see Data-catalog pattern below), with the full unfiltered list
   only one click away.
2. Facets do real work: at minimum, **category** (the 89, ideally collapsed into ~10-12 top-level
   groups with the 89 as a second-level refinement, mirroring OWID's "10 pill filters + 126 topic
   pages" split) and **era/time-period** (a second, orthogonal facet — Pahlavi / Revolution & War /
   Reconstruction / Reform / Sanctions-and-after — borrowing Trading Economics' dual-axis idea, since
   "macro to micro" alone doesn't capture the historical narrative arc this project cares about).
   A third useful facet: **chart "altitude"** — macro vs. sector vs. niche — since a GDP chart and a
   fruit-consumption chart shouldn't compete for attention in the same undifferentiated list.
3. Every row in the list carries a **live-rendered mini-preview**, not just text — OWID's four-icon
   card (line/table/map/bar) is the gold standard here; at minimum, a small sparkline per row turns a
   FRED-style wall of text into something scannable. This is the single highest-leverage visual
   upgrade over the FRED/DataBank precedents, which both suffer for being text-only.
4. The **Inspector panel** (right pane, selected-record detail) is where the bilingual/RTL and
   3-calendar and currency-toggle complexity the user has already scoped for the frontend session
   should live — it's a single, well-contained surface to get right once, rather than needing every
   card in a grid to support all of that.

### The other 2-3 front doors, non-master-detail:

- **"Start here" / topic-tree browse** (OWID's "Browse by topic" + Eurostat's "Statistics Explained"
  hybrid): a narrative-first path for the general-public audience — ~10-12 top-level themes (Macro &
  Money, Trade & Sanctions, Population & Society, Agriculture & Food, Energy, Industry, Education,
  Health, Politics & Governance, Foreign Relations, or similar — this is the "cleaner, more intuitive
  nav taxonomy" the project's own notes already flag as needed), each theme landing on a page that
  mixes short narrative context with embedded flagship charts and links deeper into the full catalog
  for that theme. This is where a first-time, non-researcher visitor should land from the homepage.
- **Era/timeline browse**: given the project's heavy Pahlavi/Revolution/War/Sanctions periodization
  and the existing policy-correlation data layer (`policy_chart_correlations_*.csv`,
  `timeline_lookup.py`), a literal **timeline UI** — click or scrub a decade, see the charts and policy
  events relevant to it — is a genuinely distinctive front door no other reference site in this list
  has, because none of them are organized around one country's political history. This is worth
  building as a signature feature, not an afterthought; it directly reuses data the project has already
  built out for ~38 flagship charts and could expand.
- **Global instant-search with live thumbnails** (OWID's algolia-style header search, scaled up):
  present on every page, searches chart titles/descriptions/tags, shows a mini preview per result as
  you type, and should be bilingual-aware (search Persian query terms against Persian-translated
  titles/tags once those exist). This is the fastest path for a researcher who already knows what they
  want ("fruit consumption by province") and shouldn't have to navigate any taxonomy at all.
- **"Popular / flagship" homepage rail** (Data USA's stat tiles + World Bank's "What's Popular"
  sidebar + Observable's `/top`): a curated, hand-picked set of ~15-25 signature charts (the ~38
  flagship-correlated charts are a natural source pool) as the very first thing a lost visitor sees,
  giving instant credibility and a "here's what this site is about" answer before they've typed
  anything or picked a category.

### Taxonomy note
The 89 categories, described in the project's own notes as "mechanically derived from WDI topic-prefix
codes," should NOT be the top-level nav. Collapse them into ~10-12 human-meaningful top-level themes
(as above) with the 89 surviving as a second-level facet/filter inside each theme or inside the
researcher list-view — exactly the OWID model (10 pill filters as level 1, 126 topic pages as level 2).

---

## 3. What to avoid

- **A flat, unfiltered 1,800-row list as any page's default state** — the single most reliable way to
  produce the "wall of charts" feeling. FRED and World Bank DataBank both only get away with a dense,
  unstructured list because their audience arrives pre-qualified via search; a general-public site
  cannot assume that.
- **Thumbnail-less rows.** Text-only lists (FRED, World Bank DataBank, Trading Economics) are the
  weakest experience among everything reviewed. Every reference site with strong discoverability (OWID,
  Data USA, Datawrapper River) shows a live or static visual preview per item.
- **Paywalling or ad-cluttering individual charts** (Statista) — directly contrary to the public-good
  mission; also erodes researcher trust in data credibility.
- **Treating Persian as a bolt-on translation layer** rather than a first-class design input (see
  Kontinentalist's regional-identity approach) — this is already flagged in the project's own frontend
  notes as an architecture decision, and this research reinforces it further: the *navigation
  taxonomy itself*, not just string translation, may read differently to a Persian-reading audience
  (e.g., different intuitive top-level groupings, different treatment of era names under the Pahlavi
  vs. Islamic Republic framing) — worth user-testing the taxonomy in both languages independently
  rather than assuming a 1:1 mirror.
- **No narrative/curated layer at all** (The Pudding's total lack of taxonomy) — fine at dozens of
  pieces, actively harmful at 1,800 charts.
- **Making the taxonomy the only entry point** — every strong reference site offers at least two
  parallel routes in (search vs. browse, raw feed vs. curated favorites, narrative page vs. raw
  database) rather than forcing every visitor through the same single funnel.

---

## 4. Three key screens, described precisely enough to mock

### Screen A — Homepage / "Start Here"
Single scrolling page, roughly OWID-homepage-shaped but scoped to one country instead of the globe.
Top: slim global header with logo/site name (bilingual toggle EN/FA top-right, a persistent small
search icon that expands into the instant-search overlay). Below the fold-line: a short one-paragraph
mission statement (what/why of the project, 2-3 sentences, in the active language). Then a **"Popular
/ Flagship charts" rail**: a horizontally-scrollable or 3-4-column grid of ~12-16 hand-picked chart
cards, each showing (a) a live-rendered mini chart (sparkline or small line/bar, not a static image),
(b) the chart's cleaned title, (c) a one-line description, (d) a small source-attribution tag. Below
that rail: a **"Browse by theme" grid** of ~10-12 large tappable tiles (one per top-level theme,
Macro & Money / Trade & Sanctions / Population & Society / etc.), each tile showing a representative
icon or micro-visualization and a chart count for that theme. Below that: a **"Explore by era" band** —
a horizontal timeline strip (Pahlavi era / Revolution & War / Reconstruction / Reform / Sanctions,
labeled with both Gregorian and, in Persian mode, Jalali year ranges) that's clickable, leading into
the era/timeline browse screen described in the IA section above. Footer: standard links (About,
Sources/Methodology, Bulk Download, bilingual toggle repeated).

### Screen B — Researcher Catalog (the master-detail "browse list + inspector" view)
Two-panel layout at desktop width (collapses to a single stacked panel with a back-button on
mobile/narrow-RTL). **Left panel** (list): top has a search-as-you-type box ("Search charts, topics,
countries, keywords…" — bilingual placeholder depending on active language) with instant results
appearing below as you type (each result row: mini sparkline thumbnail + title + one-line description +
category tag, matching OWID's live-render-per-row standard, not static images). Below/beside the
search box, a **facet rail** (collapsible on mobile) with three filter groups stacked vertically:
"Category" (the ~10-12 top-level themes, each expandable to show its sub-categories from the 89, with
live counts next to each, checkbox multi-select); "Era" (the 5 historical periods, radio or
checkbox); "Scale" (Macro / Sector / Niche, radio). Below the facets, the row list itself: each row a
compact card — mini-preview thumbnail on the left (~60x40px live sparkline), title + description
center, small metadata (source name, last-updated year, category tag chip) right-aligned, the whole
row highlightable/selectable on click. List defaults to the "Popular/flagship" subset with an
"×N filters active — showing 1,800 of 1,800, clear all" affordance always visible so the user always
knows the state of the filter, never facing an ambiguous unfiltered wall. **Right panel** (inspector):
once a row is selected, shows the full chart at large size with its own internal view-toggle (line /
table / map / bar, OWID-style), the calendar-system toggle (Gregorian / Jalali / Imperial) and
currency-toggle (nominal-USD / real-USD) controls specific to this project sitting directly above the
chart, full title + long-form description + source citation + last-updated date below the chart, and a
"related charts" mini-list at the bottom of the inspector (3-5 thumbnails, pulling from the same
category/era facets as the selected chart) to keep the visitor moving without returning to the left
list.

### Screen C — Era/Timeline Explorer
A distinctive, non-master-detail screen unique to this project. Full-width horizontal timeline spanning
the years covered by the data (roughly 1900s/1920s-present), rendered as a scrubbable axis with labeled
bands for each era (Qajar tail-end / Pahlavi / Revolution & War / Reconstruction / Reform / Sanctions
& after), color-coded per era. Overlaid on the timeline: small markers for policy/historical events
(pulled from the existing `policy_chart_correlations_*.csv` / `timeline_lookup.py` data layer),
each marker showing a short label on hover and expanding on click to a small popover listing the 1-5
charts whose data shows a confidence-scored correlation with that event. Below the timeline, a
selected-era or selected-event state populates a horizontal card row (same live-preview card format as
Screens A/B) of the charts relevant to that slice of history — e.g., scrubbing to 1979-1980 surfaces
currency/FX charts, oil-export charts, and any consumption charts with a sharp visible break in that
year. This screen is effectively "Screen B's inspector logic, but the facet is time instead of a
search box," and should reuse the same chart-card and inspector components as Screen B rather than
being built as a one-off.
