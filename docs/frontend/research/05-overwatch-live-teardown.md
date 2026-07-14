# Overwatch Live Teardown — thelobbynews.com/overwatch/congress/votes

**Scope of this doc:** a hands-on teardown of the reference site done by actually driving it in a browser
(clicking, hovering, reading computed CSS/colors, timing animations) on 2026-07-13, at the owner's
request, to build a screenshot/notes reference to build the Iran in Data UI against. This doc records
what the interface actually does, frame by frame, plus exact design-token values pulled from computed
styles — not a secondhand description from screenshots.

**This doc partially supersedes [`03-aesthetics-and-reference-analysis.md`](03-aesthetics-and-reference-analysis.md) on one point: color.**
That doc (written from static screenshots in an earlier session) recommended dropping the reference's
dark theme and color palette entirely, keeping only its interaction patterns. The owner's steer today
was explicitly the opposite: *"the rest of it is very much something that I would want to copy from this
website... colors and everything."* The one exception given was "we don't want it to be dark mode
primarily." See §6 for how this teardown reconciles that with the earlier research — there's a real
structural answer, not just a compromise.

---

## 1. The single most important structural finding

**thelobbynews.com itself is NOT a dark site.** Inspecting computed styles:

```
document.body → background-color: rgb(249, 244, 237)   /* warm cream, #F9F4ED */
```

"Overwatch" is a distinct sub-application that opts into its own dark theme via a wrapper:

```html
<div class="overwatch-theme" style="background: rgb(5, 5, 5)">  <!-- #050505, near-black -->
```

So the reference site's actual pattern is: **a light, warm, editorial parent site, with one
data-intensive sub-application (the vote visualizer) skinned dark as a deliberate, contained module.**
This is not "the site is dark except X" — it's "the site is light, and this one interactive tool is dark."

**This directly resolves the brief.** We don't have to choose between "light site" and "copy Overwatch's
colors." We can do what they did: keep the main Iran in Data site (nav, homepage, article/essay pages,
about, etc.) in a light theme, and give the **chart-detail / data-exploration screens** their own
contained dark module skin — lifting Overwatch's actual color values, corner treatment, and panel
system for that module specifically. This is the recommended reading of "copy the colors, don't make it
dark mode primarily": *primarily* the site is light; the deep-data screens get the dark treatment because
that's genuinely where it earns its keep (dense numeric tables, many data points, technical/rigorous
mood) — same logic Overwatch's own creators used.

Open question for the owner (see §8): should Iran in Data's dark module cover just the "chart focus/full
detail" view, or something broader (e.g. the whole researcher browse-list + inspector pattern)? Flagging
rather than deciding — this is a real product decision, not a default I should silently pick.

---

## 2. Exact design tokens (pulled from computed CSS, not eyeballed)

### Color
| Token | Value | Where used |
|---|---|---|
| Parent site background | `#F9F4ED` (warm cream) | thelobbynews.com main site, outside Overwatch |
| Overwatch module background | `#050505` (near-black) | Overwatch app wrapper |
| Panel background | `#0a0a0a` at 60% opacity + `backdrop-blur` | every card/section — glass-over-black, not flat black |
| Panel border | `zinc-800` equivalent (`oklch(0.274 0.006 286.033)`, ≈ `#27272a`) | hairline 1px borders on every panel |
| Democrat blue | `#2140E3` | hemicycle dots, registry bars, legend |
| Republican red | `#E32128` | hemicycle dots, registry bars, legend |
| Independent purple | `#8B5CF6` | hemicycle dots (rare) |
| Primary text | `#FFFFFF` | headline numbers, member names |
| Secondary text | `zinc-400` equivalent (muted gray) | labels, captions |
| Status-passed | a saturated green (`oklch(0.596 0.145 163.225)`) | "PASSED" badge text on white-fill badge |

The party colors are **bold and fully saturated**, not muted — a deliberate choice given the whole rest
of the palette is otherwise near-monochrome (black/white/gray). Color is spent on exactly one channel
(the thing that matters: which party) and nowhere else. That "one saturated channel, everything else
desaturated" discipline is worth stealing directly regardless of which literal hues we use for Iran vs.
comparator countries.

### Typography
| Role | Font stack | Notes |
|---|---|---|
| Body/UI/labels/headings | `switzer` (a proportional humanist sans, real typeface — not a system font) | This is NOT monospace. Most of the interface is a normal grotesque. |
| Numbers, IDs, badges, metadata | `redditMono` (monospace) | Reserved specifically for numerals, status pills, technical fields (session/roll-call/timestamp), NOT for prose or headings |

This confirms something important: **the "terminal" feeling people read off screenshots comes almost
entirely from (a) the monospace numerals/labels, (b) ALL-CAPS with wide letter-spacing on section labels,
and (c) the dark background** — not from setting everything in a monospace font. Prose (bill titles,
descriptions) is in the humanist sans at normal case. This is a very transferable discipline for us:
Yekan Bakh for everything, tabular/monospace-style numeral treatment reserved for data figures only —
exactly what the existing [`MASTER_DESIGN_DOCUMENT.md`](../MASTER_DESIGN_DOCUMENT.md) already specifies (§ font
decision), so this reference reinforces rather than contradicts that call.

Big stat numbers (e.g. the "235" YEA tally): **80px, font-weight 300** (thin, not bold) in the mono font.
Large-but-light numerals read as precise/technical rather than shouty.

### Shape language
- **Border radius is 0px almost everywhere** — every panel, card, table, and button is sharp-cornered.
- The only rounded elements are **fully-pill badges** (status tags like "PASSED", "YEA") and **circular
  chart nodes** (the hemicycle dots). Nothing is rounded "a little" (no 8px/12px soft-card radius
  anywhere) — it's binary: sharp rectangle, or full pill/circle.
- No drop shadows anywhere. Depth comes entirely from the translucent-glass panel (`bg-black/60` +
  `backdrop-blur`) sitting over the near-black page background, plus hairline borders.
- A faint dot-grid ("graph paper") texture sits behind every panel at very low opacity — a technical/
  blueprint cue that's barely noticeable consciously but reads as "precision" ambiently.

---

## 3. Page-by-page walkthrough

### 3a. Record Queue (list/browse screen) — `/overwatch/congress/votes`

No gate/landing screen on this specific deep link — it goes straight to the list. (The owner's memory
of a "click Get Started" gate is from the Overwatch **root** `/overwatch`, a separate marketing splash;
the votes directory itself has no such gate.)

Layout, top to bottom:
- **Header bar**: logo mark (a small white square) + "OVERWATCH" wordmark, breadcrumb ("VOTES"), then
  right-aligned session metadata (`SESSION: 119-2`), a live counter (`TOTAL_VOTES: 191 / 191`), and a
  pulsing red dot + "LIVE_FEED_ACTIVE" label.
- **Left rail** ("SYS_NAV"): connection-status line ("LINK:OK"), "ACTIVE_CONTEXT" (congress/session/year),
  and a "DIRECTORIES" facet list (All Roll Calls, Appropriations, Amendments, Nominations, each with a
  record count).
- **Main panel**: "Record Queue" heading, live record count ("191 OF 191 RECORDS"), a terminal-styled
  search input (`> search --rc`), a "FILTERS" toggle that expands a drawer (Chamber: All/House/Senate,
  Sponsor, Category, Result: All/Passed/Failed, plus "ACTIVE FILTERS: NONE / CLEAR ALL"), then a dense
  sortable table: ID · Chamber · Measure (bill number in a bordered chip) · Subject · Date · Status (a
  small colored dot, green/red).
- Footer: "BUILT BY: THE LOBBY MEDIA LLC" + session tag, bottom-left/right, quiet and small.

### 3b. Vote detail — Hemicycle mode — `/overwatch/congress/votes/119-2026/house/191`

- **Full-width strip above the header content**: a session-wide sparkline of every vote's yea/nay margin
  (bars pointing up for yea margin, down for nay margin), with the current roll highlighted — gives
  "where does this vote sit in the whole session" context before you even look at the single record.
- **Left rail** (persistent across Hemicycle/Registry mode):
  - "FINAL TALLY" card: PASSED/FAILED pill, then two huge (80px/300-weight) numbers for Yea/Nay.
  - "MARGIN ANALYSIS" card: differential (+56 votes), a horizontal threshold gauge (a striped bar showing
    where the actual result landed relative to the majority line, with a red tick marking the line).
  - "PROCEDURAL META" card: session, roll-call #, timestamp, majority type (simple), chamber, result,
    present count, not-voting count — plain label/value rows.
  - **This left rail is the direct analog of the "mini-essay / Wikipedia-sidebar" idea the owner raised** —
    it's already exactly that pattern (persistent context card next to the visualization), just filled
    with procedural metadata instead of prose. For us this is where a short context essay + the
    confidence-scored policy/event annotations would live.
- **Center panel**: "VISUALIZER_MODE" segmented control (Hemicycle / Registry) top-right of the panel;
  bill number + title + vote-type line; then the hemicycle chart itself — 435 dots arranged in a
  semicircle by party bloc, **filled dot = voted with the headline position, hollow ring = voted against,
  small/dim dot = not voting**, colored by party (blue/red/purple per §2). A legend is always visible at
  the bottom of the panel (never hidden behind a tooltip): `DEM ●Y ○N ●NV | REP ●Y ○N ●NV | IND ●Y ○N ●NV`.
- **Right rail**: "NODE_INSPECTOR". Idle state = an empty crosshair-reticle box + "NO SIGNAL / AWAITING
  TARGET..." with dashed placeholder fields (District, Party, Vote Cast, Party Alignment). **Clicking (not
  just hovering) a single dot** animates the panel to show: a grayscale/duotone member photo, the name
  (see §4 for the text-decrypt reveal), District, Party, a colored outlined pill for Vote Cast (e.g.
  "YEA"), and a "Party Alignment" stat with a green dashed progress bar (e.g. "20/20 WITH PARTY").

### 3c. Vote detail — Registry mode

Same left rail, same bill header. The center panel swaps to:
- A restated headline stat block (`ROLL_CALL_ANALYSIS // FINAL_TALLY`) with big Yea/Nay counts, a
  "MARGIN +N" chip, and a horizontal threshold gauge (same visual language as the left rail's Margin
  Analysis card, just bigger/central here).
- Two party-breakdown cards (Democrat / Republican) each with a mini within-party yea/nay bar and exact
  counts.
- "MEMBER_REGISTRY: N RECORDS" — a full searchable, filterable (All/Yea/Nay), paginated table:
  Representative · Party · State · District · Vote Status (colored pill). This is the "browse-list"
  pattern from the earlier research doc's §2, confirmed live.

This mode-switch (same underlying data, two visualization lenses — spatial/hemicycle vs. tabular/registry)
is a genuinely reusable idea for us: a chart-detail page could offer "chart view" vs. "table view" of the
identical dataset via the same kind of segmented control, which also happens to be a good accessibility
fallback (screen-reader/keyboard users get the table for free).

---

## 4. Motion & delight catalog

These are the specific animated behaviors observed, with rough timing:

1. **Text-scramble/decrypt transitions.** On navigating between records (row click → detail page) and
   whenever new text populates a panel (member name and vote-cast badge in the Node Inspector), the text
   briefly renders as random alphanumeric noise, then "decrypts" character-by-character into the real
   content over roughly 0.5–1s. Applied to headings, table cells, and badges alike — it's the site's
   single most distinctive motion signature. **Note for us:** the raw device (scrambled-cipher text) is a
   very on-genre choice for a "surveillance/intelligence" skin; if we adopt the *mechanism* (a brief
   glyph-cycling reveal on data population) for our dark data-module, it should probably read as
   "resolving/computing a number" rather than "decrypting a secret" — same technique, different implied
   metaphor, so it doesn't borrow tone that doesn't fit an economic-data encyclopedia.
2. **Numeric count-up ("odometer") animation.** Big stat numbers (Yea/Nay totals, per-party vote counts,
   "MEMBER_REGISTRY: N RECORDS") animate from 0 up to their final value over a surprisingly long window —
   observed still climbing after 8+ seconds on a slow load. This is deliberate, not a loading-race
   artifact: it reinforces the "live system computing" feel. For our annual/periodic data, a **much
   shorter** count-up (under ~1s) on first render or on toggling a chart control (currency/comparator/
   calendar) would read as responsive polish without implying false real-time-ness.
3. **Panel-assembly / "HUD boot" loading state.** On a cold load of a page, panels first appear as empty
   sharp-cornered rectangles with small animated corner-bracket accents (the four corners draw in before
   the frame fills), then content populates. This corner-bracket motif also appears as a small standalone
   accent mark (a plain white square) used as the site's own favicon/logo glyph — a consistent visual
   signature at multiple scales.
4. **Hover/click → Node Inspector reveal.** Clicking a hemicycle dot smoothly swaps the right rail from
   its idle "awaiting target" placeholder to a fully populated card (photo, name, stats) — no page
   navigation, purely a panel-content transition, instant and spatially anchored (the rail doesn't move,
   only its content changes). This is the exact pattern flagged as most valuable in the earlier research
   doc (§2 "Transferable patterns"), now confirmed with real timing/feel: it's fast (near-instant swap)
   with the text-decrypt effect providing the "settling in" motion, not a slow fade.
5. **Sparkline strip as ambient/persistent context**, not an interactive chart in its own right — it's a
   static-looking bar visualization that just sits above the fold, giving session-wide scale before you
   engage with the single-record content below it.

---

## 5. What's specific to the US-Congress domain (not transferable)

- The hemicycle geometry itself (semicircle of 435/100 seats) — no natural analog for economic
  time-series/panel data. Confirmed by the earlier research doc (§2, "Aesthetic-only choices") and
  reconfirmed live: this is a shape specific to representing a legislature's seat composition.
- "LIVE_FEED_ACTIVE," session/roll-call vocabulary, and the multi-second real-time-feeling count-up
  animations are calibrated to an actually-live congressional data feed. Our data is periodic/annual —
  using the same *techniques* (count-up, decrypt-reveal) at *much shorter, more restrained* durations
  avoids the "simulated liveness on non-live data" trap the earlier research doc already flagged.
- One functional note from direct testing: **a cold, direct hard-navigation to the Record Queue list URL
  hung indefinitely** in this testing session (panels stuck in the "HUD boot" corner-bracket loading state
  and never populated) — this may be specific to automated browsing, but if it's a real production issue
  it's a cautionary example of over-choreographed loading states creating a real perceived-hang risk. Our
  loading states should have a hard timeout/fallback, not depend on an animation sequence completing.

---

## 6. Reconciling with the prior design session

The existing [`MASTER_DESIGN_DOCUMENT.md`](../MASTER_DESIGN_DOCUMENT.md) (written in an earlier chat this same day,
before this live teardown) explicitly "dropped the research's mono/ledger idea entirely" and treated dark
theme + color as "take-it-or-leave-it," landing on a light, warm "contemporary Persian archive" direction
for the *whole site*. Today's steer changes that: the owner wants Overwatch's actual colors, borders,
corners, loading behavior, and transitions carried over closely, with dark-mode-as-primary as the only
explicit exclusion.

**These aren't actually in conflict once you apply §1's structural finding.** Recommended synthesis,
which I have NOT yet applied to the master doc pending confirmation (see §8):
- Keep the master doc's light, warm, Yekan Bakh identity for the site shell — homepage, nav, category
  browsing, essay/article pages, about/methodology pages.
- For the **chart-detail / deep-data-exploration screens specifically**, adopt a contained dark module
  using the exact tokens in §2 (near-black glass panels, zinc-800 hairlines, 0px-radius sharp panels +
  pill badges only, saturated single-purpose color channel, monospace-for-numerals-only), and the motion
  language in §4 at restrained timings.
- This gives us both things the owner asked for in the same two conversations: "almost exactly copy this
  site" for the parts they pointed at, and "not primarily dark mode" for the site as a whole — because
  that's literally the reference site's own structure, not a hedge.

---

## 7. Direct translation table — Overwatch pattern → Iran in Data equivalent

| Overwatch | Iran in Data equivalent |
|---|---|
| Record Queue (searchable/filterable vote list) | Chart index / researcher browse-list (already planned per master doc IA) |
| Hemicycle (435 dots by seat) | N/A — no analog, do not force one |
| Registry mode (stat cards + member table) | The "table view" toggle for any chart — same data, tabular lens |
| Node Inspector (click a dot → member card) | Click/hover a data point (country line, bar, timeline marker) → inspector card with value, year, source, link |
| Left rail: Final Tally / Margin Analysis / Procedural Meta | Left rail: chart's mini-essay context + the confidence-scored policy/event annotation (owner's explicit ask) |
| Session-wide sparkline strip | A small "this chart in context" strip — e.g. this indicator's percentile among all Iran charts, or a mini-timeline of related events — optional, not required |
| VISUALIZER_MODE toggle (Hemicycle/Registry) | Not just view-mode — for us this control row is where the chart TOGGLE SYSTEM lives: nominal/real currency, 3-calendar, comparators on/off, per-capita, log/linear, zoom |
| Dark module contained inside light site | Exactly the structural pattern to copy — see §1/§6 |
| Text-decrypt reveal | Optional motion device for the dark data-module only, restyled as "resolving" rather than "decrypting" |
| Count-up numbers | Short count-up (<1s) on chart load/toggle-change, not multi-second |

---

## 8b. Responsive behavior — mobile teardown (driven live at 375–390px width)

Direct hard-navigation to a vote-detail URL rendered correctly at mobile width; the list page and a
couple of interactive follow-ups hung/froze the tab repeatedly in this testing session (see caveat at
the end of this section). What follows is confirmed from what did render.

**Header** collapses hard: the right-side session/vote-count metadata and "LIVE_FEED_ACTIVE" text are
dropped, leaving just the logo mark, "OVERWATCH," and a breadcrumb (`VOTES / HOUSE · ROLL 191`), plus the
red status dot alone (no label) on the far right. Nothing is hidden behind a hamburger menu — it's a
content drop, not a menu collapse.

**The persistent desktop left rail (SYS_NAV / directories) becomes a single collapsed horizontal button**:
a back-chevron + a pill labeled "ARCHIVE BROWSER" with a small bar-chart icon and the current record count
(`191`) — presumably a tap target that opens the full filter/directory drawer as an overlay rather than
occupying permanent layout width. This is the standard "rail becomes a drawer trigger" pattern, but worth
noting they kept it visually consistent (same bordered-pill, monospace-label language) rather than
switching to a generic hamburger icon.

**The three left-rail cards (Final Tally / Margin Analysis / Procedural Meta) collapse into ONE combined
card**: bill number + PASSED badge on one line, vote-type + date, title, then the Yea/Nay numbers with the
margin gauge inline — all of what was three separate bordered panels on desktop becomes one panel with
internal dividers on mobile. This is a good pattern for us: our left-rail "chart context" card (tally,
margin, procedural meta today; mini-essay + policy/event annotations for us) should similarly fold into a
single scrollable card on narrow screens rather than three stacked panels with their own borders/padding.

**The hemicycle chart itself does NOT shrink to fit** — this is the most important mobile finding. Instead
of scaling ~435 dots down to fit 375px (which would make them unreadable/untappable), the "Hemicycle" mode
is replaced by default with a **"Quarter" mode**: the semicircle is split into two independent party-bloc
visualizations — "Democrats + Independents" rendered at full, legible dot size and scale, with
"Republicans" as a second column immediately to its right, appearing to require horizontal scroll to view
in full (confirmed the column is present and correctly colored; horizontal-scroll interaction itself
could not be confirmed in this session — see caveat). The `VISUALIZER_MODE` control still offers
`QUARTER / GRID / REGISTRY` (no plain "Hemicycle" option at this width) with a legend still fully visible
beneath it.

**General principle worth stealing**: don't shrink a wide/dense chart proportionally on mobile until dots
or bars become untappable — instead, decompose it into a paged/scrollable set of legibly-sized sub-views.
For our project this maps directly onto multi-country comparison line charts and any chart with many
series: on mobile, default to fewer simultaneous series (e.g., Iran + 1 comparator) with the rest
reachable via the comparator toggle, rather than rendering 8 thin lines at a shrunk size.

**Caveat on this section's completeness**: the tablet breakpoint (~768–820px) could not be captured —
the automated browser window got stuck reporting a 375px viewport regardless of resize requests, and the
tab's renderer froze on two follow-up interactions (clicking the GRID/REGISTRY mode toggles, and the
breadcrumb back to the list). This may be a genuine performance issue with the reference site itself (the
hemicycle alone renders ~1,700 SVG elements plus continuous scramble-text timers, which is a lot for a
constrained/automated tab) rather than purely a tooling artifact — worth keeping in mind as a "don't
overload the DOM with animated nodes" caution for our own chart components at scale. Grid mode's actual
visual difference from Quarter mode on mobile was not confirmed before the tab froze.

## 8. Open questions for the owner

1. **Scope of the dark module** (§1/§6): should the dark, Overwatch-styled treatment apply to (a) just
   the single chart's "full detail / focus" view, (b) the whole researcher browse-list + inspector screen,
   or (c) something broader? This changes how much of the site inherits these tokens vs. stays in the
   light "Warm Archive" language from the existing master doc.
2. Should the **party-blue/party-red saturated-color discipline** (one bold hue per data channel, else
   desaturated) replace or coexist with the master doc's existing "Iran = one signature saturated hero
   color, comparators muted" rule? They're compatible in spirit — just confirming before I fold this into
   the master doc.
3. On the **hero/landing** you described (half- or full-viewport, minimal, no gate screen, scroll down to
   the chart list/search): should that hero sit in the light site shell (per master doc) or could it also
   preview the dark data-module aesthetic (e.g., a live chart or stat ticker in the hero itself)?
4. Do you want me to fold this teardown's findings into `MASTER_DESIGN_DOCUMENT.md` directly (updating the
   sections that assumed dark-theme-is-dropped), or keep this as a standing reference doc and revisit the
   master doc's decided sections together with you first?
