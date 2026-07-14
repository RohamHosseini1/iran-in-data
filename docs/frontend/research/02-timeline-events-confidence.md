# Timeline Event Annotations + Confidence-of-Correlation Panel — Design Research

Scope: how to mark policy decisions / wars / revolutions / disasters / world events on an economic
time-series chart, how the hover/click detail panel should look and behave, and how to encode an
honest "confidence of correlation" metric without implying causation we can't support.

---

## 1. Reference examples (what to steal, specifically)

1. **FRED (Federal Reserve Economic Data) recession shading** — https://fred.stlouisfed.org/series/USREC (and any FRED chart, e.g. https://fred.stlouisfed.org/graph/?g=KKk)
   - Steal: **background band shading**, not a marker dot, for events that have *duration* (recessions, wars, sanctions regimes). Bands are pale gray, sit behind the data line, span the full chart height, and never carry a label directly on the chart — the reader already knows "gray = recession" from convention, or a one-line legend note does the job.
   - Why it matters for us: many of our "events" (sanctions regimes, wars) are ranges, not instants. FRED's convention — flat, low-opacity, full-height band, zero chart-ink competing with the data line — is the right default for range-type events. Point events (an assassination, a currency reform decree) should instead be a marker, not a band.
   - Also steal: FRED documents its shading methodology (peak-to-trough vs. peak-to-period-before-trough) in a public methodology note (https://fredhelp.stlouisfed.org/fred/data/understanding-the-data/recession-bars/) — a model for how *we* should publish our own event-dating methodology so users can audit why an event's start/end date was chosen.

2. **Datawrapper range highlights & reference lines** — https://www.datawrapper.de/academy/range-highlights-and-lines and https://www.datawrapper.de/blog/annotations-in-bar-charts
   - Steal the **explicit z-order rule**: range/band highlights render *behind* everything (data, gridlines, reference lines); reference lines render *above* gridlines but *below* annotations; text annotations render on top of all of it. This is a clean, reusable layering rule we should adopt verbatim: `band < gridlines < line-series < reference-line < event-marker < annotation-text/panel`.
   - Steal the **opacity discipline**: "choose either a very light color, or decrease opacity a lot" for anything that isn't the hero series. Applied to us: event bands/markers should never out-contrast the actual economic data line. The marker draws the eye at the point of interaction (hover/focus), not at rest.
   - Steal: line weight as a signal of importance (1px default / 2–3px for something worth calling out) — useful for differentiating "minor event" vs. "major event" markers without adding a new color.

3. **Datawrapper annotations blog + Academy "text in visualizations" guide** — https://www.datawrapper.de/blog/text-in-data-visualizations
   - Steal: **place explanatory text as close as possible to the thing it explains**, and **always put units/context in the annotation itself**, not just in a caption below. For our detail panel this argues for keeping the event title + one-line "what happened" directly adjacent to the marker (in a callout) even before the user opens the full panel — a "preview" tier before "full inspector" tier.

4. **Observable's "Five Techniques to Improve Chart Annotations"** — https://observablehq.com/blog/five-techniques-to-improve-chart-annotations
   - This is the single most directly transferable reference. Five patterns, all relevant:
     - **Pointer-driven marks with a static default.** Quoting NYT's Archie Tse's rule of thumb baked into the piece: "if you make a tooltip or rollover, assume no one will ever see it." The pattern: show a *default* annotation (e.g., the single most important event, or the most recent one) permanently on the chart, and only let hover/click *replace* it with a different, user-chosen event. This is directly what we should do: don't make every event marker inert until hovered — the single highest-confidence, most narratively important event per chart should have its detail panel state visible/expanded by default (or at least its callout label always-on), with the rest collapsed to small dots.
     - **Continuous crosshair tied to pointer, not snapped to data.** Lets the user feel the empty stretches of time between events, which matters for us because many decades in Iranian economic history have *no* marked event and that emptiness is itself informative (nothing recorded ≠ nothing happened — see caveat language below).
     - **Cross-facet highlighting** — hovering one event marker highlights corresponding moments in *other* linked charts (e.g., inflation and exchange-rate charts both flag the 2018 sanctions re-imposition simultaneously). This maps directly onto our "related charts" surfacing requirement.
     - **Staggered label rows** to de-collide dense clusters of event labels (Iran's chart timelines will have crowded event clusters — 1979, 2018, 2022 in particular).
     - **Grouped tooltips** showing multiple concurrent series/events at one x-position — useful when several policy changes land in the same year.

5. **Flourish "Introducing Annotations" + Story annotations** — https://flourish.studio/blog/introducing-annotations/ and https://helpcenter.flourish.studio/hc/en-us/articles/8761582943759-Timeline-an-overview
   - Steal: the **curved/elegant connector-arrow** treatment for tying a floating text note back to its exact point on the chart when space is tight — relevant for event clusters where the marker sits close to the axis but the label needs to float above the chart body.
   - Steal: Flourish timelines let the user toggle **equidistant vs. true-time-scale spacing** of events. For us: our event-density is uneven (many events cluster around 1979-1981 and around 2018-2022), so offering a toggle (or auto-detecting) between true chronological spacing and "readable" spacing for a dedicated events-timeline view (separate from the chart-overlay view) is worth planning for.

6. **The Economist's chart annotation discipline** (documented via chart-recreation retrospectives, e.g. https://medium.com/@timvanschaick/what-makes-the-economists-charts-so-good-0234e4271da3 and the FT/Economist "visual vocabulary" tradition)
   - Steal the **"one chart, one message" + de-emphasized context rule**: reference/context data (baselines, comparators) rendered at 30–50% opacity, never full saturation; the one thing the chart is arguing sits in full color. Applied to events: the event marker for the event being *discussed in the current context* (e.g., a chart embedded in an article about the 2018 sanctions) should be full-strength; all *other* markers on that same chart recede to a muted default so the page doesn't look like a firework display of dots.
   - Steal: annotate turning points *precisely at the inflection*, not floating generically nearby — i.e., the marker's x-position should sit exactly on the date, with the connector line making the exact linkage to the data point unambiguous (not just "somewhere in this decade").

7. **Financial Times Visual Vocabulary** (poster + site) — https://ft-interactive.github.io/visual-vocabulary/ and repo https://github.com/Financial-Times/chart-doctor
   - Not annotation-specific, but the FT's broader design ethos ("annotate any pattern the reader should see," don't leave the reader to infer the point) is the right north star for whether an event deserves a marker at all: if the event doesn't correspond to a visible pattern in *this specific* chart, don't force a marker onto it — reserve markers for events with plausible, chart-specific relevance (ties directly into the confidence metric below — an event with confidence too low to be interesting for this chart shouldn't clutter it).

8. **d3-annotation (Susie Lu)** — https://d3-annotation.susielu.com/ and https://www.susielu.com/data-viz/d3-annotation-design-and-modes
   - Implementation-level reference, not aesthetic: models an annotation as **subject + connector + note**, a clean separable structure. For engineering, adopt this exact decomposition: `subject` = the marker/dot on the timeline, `connector` = the line/leader from marker to panel, `note` = the panel content itself. Useful vocabulary for a component API (`<EventMarker subject connector note />`).

9. **Reuters Graphics `awesome-charts`** — https://github.com/reuters-graphics/awesome-charts
   - Steal the general engineering posture, not a specific visual: Reuters ships small, composable, open-source chart modules rather than one monolithic chart component. Useful precedent for us to build the "event marker" as a standalone overlay layer that composes onto *any* of our ~1,800 charts, rather than a bespoke one-off.

10. **IPCC uncertainty-language framework** (not data-viz, but the best-vetted honest-confidence-communication precedent that exists) — https://www.ipcc.ch/site/assets/uploads/2017/08/AR5_Uncertainty_Guidance_Note.pdf, background at https://link.springer.com/article/10.1007/s10584-020-02746-x
   - Steal the **two-axis structure**: IPCC separates *confidence* (qualitative: based on evidence type/amount + agreement among sources — "low/medium/high/very high confidence") from *likelihood* (quantitative probability band — "likely" = 66–100%, "very likely" = 90–100%, etc.), and always states both, plus the evidentiary basis, in the same breath. This maps very well onto our need: "confidence-of-correlation" for us should also be two things bundled — (a) how *strong* the historical/statistical association looks in the data, and (b) how much *documented expert consensus* exists that the specific policy caused it — and both need a plain-language caveat sentence every time, not just a number.

11. **Jessica Hullman / Padilla & Kay, "Uncertainty Visualization"** (academic survey) — https://users.eecs.northwestern.edu/~jhullman/Value_of_Uncertainty_Vis_CR.pdf and http://space.ucmerced.edu/Downloads/publications/Uncertainty_Visualization_Padilla_Kay_Hullman_2022.pdf
   - Key empirical finding to steal as a design constraint: a 2019 audit found 73% of published data-journalism visualizations presented inferential data but only 3% visualized uncertainty at all — i.e., omitting uncertainty is the industry default failure mode, and we are explicitly trying to not be that. Also steal the finding that **discrete/ordinal encodings (bins, categories, verbal likelihood terms) are read more accurately by lay audiences than continuous encodings (raw error bars, density curves, spaghetti plots)** — this argues for our confidence metric being a small ordinal scale (e.g., 5 discrete levels with plain-language labels) rather than a precise-looking percentage or a continuous gradient, which would overclaim precision we don't have.

12. **"Correlation vs. causation" illusion-of-causality research** (JMP explainer + underlying HCI literature, e.g. https://arxiv.org/pdf/2401.08411 "Using Counterfactuals to Improve Causal Inferences from Visualizations")
   - Empirical finding to steal as a hard constraint: users reliably over-attribute causal meaning to any two series that move together on a shared timeline, across bar/line/scatter forms — merely putting an event marker next to a chart bend *will* be read causally by most users regardless of our disclaimers being present elsewhere on the page. This means the caveat cannot live only in a footnote; it must sit inside the same visual unit as the confidence number itself (see recommendations, section 3).

---

## 2. Concrete recommendations for our timeline-event overlay

### Marker design

- **Two marker geometries by event type:**
  - **Point events** (assassination, currency redenomination decree, single-day disaster) → a small filled circle sitting exactly on the x-axis date, connected by a thin vertical guideline up into the plot area to the point on the data line it's annotating (or to a fixed height near the top if it doesn't correspond to one specific data point).
  - **Range events** (war, sanctions regime, multi-year drought) → a pale full-height background band (FRED-style), with a thin marker/flag only at the start (and optionally a lighter one at the end) to avoid two competing markers per event.
- **Visual weight scales with a "narrative importance" flag** (editorially set, distinct from the confidence-of-correlation metric — importance = "how major was this event in Iranian history," confidence = "how much does it explain this specific chart"): major events get a slightly larger marker + persistent label; minor events collapse to a small dot with no visible label until hovered/focused.
- **Color is neutral/desaturated at rest** (gray or a single muted "event" hue, not category-color-coded by event type, to avoid a legend explosion across 1,800 charts) and only gains saturation/emphasis on hover, focus, or when it is the event most relevant to the current confidence ranking for *this* chart.
- **Density handling:** when multiple events cluster within a few pixels at the current zoom level, merge them into a single "N events" cluster marker (like a map cluster pin) that expands into individual markers on click/zoom, rather than letting labels collide (Observable's staggered-axis pattern is the fallback if clustering isn't used).

### Panel behavior / animation

- **Progressive disclosure in three tiers**, matching the "hover a node → rich inspector" reference pattern the owner likes:
  1. **At rest:** marker only, optionally a tiny always-on label for high-importance events (NYT/Observable "static default" pattern).
  2. **On hover/focus (desktop) or tap (touch):** a lightweight callout appears immediately adjacent to the marker — title + one-sentence description + the confidence badge only. This should animate in fast (~120–150ms ease-out, slight upward slide + fade, not a bouncy spring — trust-critical products should feel calm, not playful) so it reads as responsive, not decorative.
  3. **On click/select:** the full "inspector" side panel slides in (from the right on desktop, from the bottom as a sheet on mobile) with: title, date/date-range, full description, the confidence-of-correlation metric with its plain-language justification and caveats (see section 3), a small sub-visualization (e.g., a zoomed-in mini version of *this* chart around the event date, or a small bar comparing before/after average), a "related events" list, and a "related charts" list. This is the "rich inspector" the owner referenced — same mechanism, adapted to our content (chart context + causal-honesty framing) rather than the reference's original aesthetic.
- **Persistence:** the tier-3 panel should stay open and pinned (not auto-dismiss on mouse-out) once explicitly clicked/selected, so a user can move the mouse back onto the chart to compare the marked point against the data line without losing the panel — this matters because the whole point of the feature is letting someone visually check "does the line actually bend here."
- **A subtle "scanning" / live feeling** (echoing the terminal-log reference): rather than literal fake terminal text (which would look gimmicky on an economic-data encyclopedia), translate the *feeling* — e.g., a thin animated progress trace that "draws" the sub-visualization inside the panel over ~400ms when it opens (a line chart drawing left-to-right), and a small monospace metadata strip at the panel's top or bottom (source, last-updated date, event ID) that reads like data provenance rather than theater. This keeps the "alive" quality without undermining the encyclopedia's credibility with decorative fakery.
- **Keyboard/accessibility:** markers must be independently focusable (tab-stops) and the tier-2 callout must appear on `:focus` identically to `:hover` (Reuters' 2024 election-map a11y pattern — tooltip exposed on keyboard focus, not just mouse hover) so screen-reader and keyboard users get the same disclosure tiers.

### How "related policies/charts" surface

- Inside the tier-3 panel, two short horizontal-scroll rows:
  - **Related events** — other events tagged with overlapping category (e.g., "monetary policy," "sanctions," "war") or temporally adjacent (within ~2 years), shown as small cards (title + date) that re-open the panel for that event on click.
  - **Related charts** — other charts in the database where this same event is also marked, surfaced via the event's own ID (an event should be a first-class entity referenced by multiple charts, not duplicated per-chart) — clicking navigates to that chart with the same event pre-selected/pre-opened, preserving context continuity (this is the cross-facet-highlight idea from Observable, applied as navigation rather than same-page highlighting, since our charts are separate pages).
- Both rows should be populated from the shared event/entity graph, not re-authored per chart, so editorial effort scales with number of *events* (dozens to low hundreds) rather than number of *charts* (~1,800).

### Confidence-of-correlation metric — display

- **Two-part badge, not a single bare number** (directly adapting the IPCC confidence+likelihood split):
  - **Strength-of-association** — how visually/statistically strong the co-movement is in *this specific* series around the event date (e.g., a discrete 5-point ordinal scale: "no visible change / weak / moderate / strong / very strong," derived from a defined simple rule such as % change in trend slope or level shift in a window around the event — document the exact rule).
  - **Attribution confidence** — how much documented historical/economic consensus exists that *this event specifically* (rather than confounding factors) explains that movement (also a discrete ordinal scale: "speculative / contested / plausible / well-documented," tied to how many independent sources attribute the effect).
- **Always paired with one plain-language sentence**, generated from a template, e.g.: "Prices rose sharply in the months after this event, and most economic historians attribute at least part of this to [event] — but [confounding factor, e.g., a currency reform six months earlier] makes it hard to isolate the effect." Never show the badge without this sentence sitting immediately beside it — per the causality-illusion research above, the caveat must live in the same visual unit as the number or it will be ignored.
- **No single blended "confidence score"** (e.g., no "73% confidence") — a precise-looking percentage overclaims precision for what is fundamentally a qualitative historical judgment. Use discrete ordinal levels with words, optionally reinforced by an icon (e.g., 1–5 filled segments of a bar, muted-gray palette, never red/green/traffic-light framing which implies good/bad rather than known/unknown).
- **Always show sourcing/provenance** for the confidence judgment inside the panel (who assessed it, what evidence — e.g., "Assessed against IMF/CBI data and 3 secondary sources; see citations") — this is both a trust signal and lets a researcher-tier user drill in.
- **Explicitly separate this event's chart-specific confidence from the event's general historical significance** — a globally major event (e.g., the 1979 revolution) may have *low* attribution confidence for a specific chart (e.g., regional literacy rates) if the link is tenuous; the UI must be able to show "major event, low relevance to this chart" without that reading as a contradiction. Consider a small caption under the badge: "How much this event explains the pattern in *this* chart" to anchor the metric's scope every time it appears, since it will appear differently-scored on different charts for the same event.

---

## 3. Uncertainty/confidence visualization — short survey and fit

| Technique | Best for | Fit for us |
|---|---|---|
| Error bars / CIs on the data series itself | Statistical uncertainty in a measured value (e.g., survey-based GDP estimate) | Good for the underlying chart data where we already record contested estimates as ranges (per existing bias policy) — but this is a *different* uncertainty than event-attribution confidence; don't conflate the two in one visual encoding. |
| Hypothetical Outcome Plots / ensemble ("spaghetti") plots | Communicating a distribution of possible futures/scenarios (weather forecasting) | Poor fit — irrelevant to retrospective historical attribution; also empirically criticized (Ars Technica critique of hurricane spaghetti plots) for confusing lay audiences; avoid. |
| Verbal/ordinal likelihood scales (IPCC-style: "likely," "very likely" + confidence level) | Qualitative expert-judgment uncertainty where a precise probability isn't defensible | **Best fit for our attribution-confidence axis** — this is exactly the kind of judgment (historians'/economists' consensus) IPCC-style language was built for. |
| Discrete/binned encodings generally (vs. continuous) | Lay audiences, per Padilla/Kay/Hullman's synthesis | Confirms the ordinal-badge choice over a continuous gradient or precise percentage. |
| Opacity/desaturation for "this is context, not the headline" | De-emphasizing comparison data (Economist convention) | Use for muting non-selected event markers and for range-event background bands. |
| Always-visible caveat sentence bound to the number | Preventing the causal-illusion effect | Mandatory pairing, not optional — see above. |

**Bottom line for a trust-critical public encyclopedia:** favor words over precise-looking numbers, always show the caveat in the same glance as the badge, separate "how strong does this look in the data" from "how much do experts agree this event caused it," and document/expose the assessment methodology (mirroring FRED's public recession-dating methodology note) so any user can audit why a given confidence level was assigned.

---

## 4. The key interaction, described precisely enough to mock

1. Chart renders with a baseline data line. Along the x-axis, event markers appear: small muted dots for point events, pale full-height bands for range events. One high-importance event (editorially flagged) shows a persistent small label at rest; all others are unlabeled dots.
2. User moves the mouse across the chart (or tabs via keyboard). A crosshair follows the pointer/focus continuously (not snapping between markers), showing the current date and value in a small floating readout — this works whether or not the pointer is over a marker.
3. When the pointer/focus lands within the hit-area of a marker (a generously padded invisible hit-box around the small visible dot), within ~100ms a **callout** fades and slides up (≈8px, ~140ms ease-out) next to the marker: event title, one-sentence description, and the confidence badge (ordinal icon + one word, e.g., "Moderate"). If two markers are close enough to collide at the current zoom, they've already been pre-merged into a cluster pin showing "3 events" that expands into individual dots on hover.
4. If the user clicks (or presses Enter/Space while focused) the marker, the callout is replaced by the full **inspector panel**, sliding in from the right edge of the viewport (bottom sheet on mobile), pushing or overlaying the chart depending on viewport width. Panel contents, top to bottom: event title + date/date-range; a monospace provenance strip (source, event ID, last reviewed date); a mini sub-chart that animates drawing itself (~400ms) showing this chart's series zoomed to a window around the event with the event's date/range marked; the full description paragraph; the two-part confidence badge with its plain-language caveat sentence directly beneath it; a "Related events" horizontal card row; a "Related charts" horizontal card row; a close control.
5. The panel remains open (pinned) even if the mouse returns to hover elsewhere on the chart, so the user can visually compare the marked date against the trend line at leisure. Selecting a different marker while the panel is open replaces its contents with a brief cross-fade rather than a full close/reopen cycle. Clicking a "related chart" card navigates to that chart's page with the same event already selected and its panel pre-opened, preserving the thread across pages.
6. Escape key or explicit close control dismisses the panel back to the tier-1 at-rest state.

---

## Sources consulted

- FRED recession bars: https://fredhelp.stlouisfed.org/fred/data/understanding-the-data/recession-bars/ , https://fred.stlouisfed.org/series/USREC
- Datawrapper range highlights/reference lines: https://www.datawrapper.de/academy/range-highlights-and-lines
- Datawrapper annotations: https://www.datawrapper.de/blog/annotations-in-bar-charts , https://www.datawrapper.de/blog/text-in-data-visualizations
- Observable, "Five techniques to improve chart annotations": https://observablehq.com/blog/five-techniques-to-improve-chart-annotations
- Flourish annotations/timelines: https://flourish.studio/blog/introducing-annotations/ , https://helpcenter.flourish.studio/hc/en-us/articles/8761582943759-Timeline-an-overview
- The Economist chart style retrospectives: https://medium.com/@timvanschaick/what-makes-the-economists-charts-so-good-0234e4271da3
- FT Visual Vocabulary: https://ft-interactive.github.io/visual-vocabulary/ , https://github.com/Financial-Times/chart-doctor
- d3-annotation (Susie Lu): https://d3-annotation.susielu.com/ , https://www.susielu.com/data-viz/d3-annotation-design-and-modes
- Reuters Graphics awesome-charts: https://github.com/reuters-graphics/awesome-charts
- IPCC uncertainty guidance: https://www.ipcc.ch/site/assets/uploads/2017/08/AR5_Uncertainty_Guidance_Note.pdf ; https://link.springer.com/article/10.1007/s10584-020-02746-x
- Uncertainty visualization survey (Padilla, Kay, Hullman): http://space.ucmerced.edu/Downloads/publications/Uncertainty_Visualization_Padilla_Kay_Hullman_2022.pdf ; https://users.eecs.northwestern.edu/~jhullman/Value_of_Uncertainty_Vis_CR.pdf
- Causal-illusion-from-visualization research: https://arxiv.org/pdf/2401.08411
