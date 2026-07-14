# Bilingual (EN/FA) RTL Design + Accessibility Research

Research for iranindata.org — a bilingual English/Persian encyclopedia of ~1,800 Iran economic
charts, three calendar systems (Gregorian, Solar Hijri/Jalali, Solar Imperial), nominal/real
currency toggle. Design research only — no implementation.

---

## 0. Opinionated recommendations (read this first)

| Question | Recommendation |
|---|---|
| Should the time-series x-axis flip to RTL in Persian mode? | **No. Keep every axis with a temporal/numerical dimension left-to-right in both languages.** Mirror everything else (page chrome, legend, source/logo position, categorical bar charts). |
| Persian or Western numerals for data? | **Western numerals (0-9) for all chart data, axis ticks, and tables in both language modes.** Use Persian numerals (۰-۹) only for decorative/prose UI copy in Persian mode, never inside a chart or a number a researcher might copy into a spreadsheet. |
| Font | **Vazirmatn** for Persian, paired with a matching-weight Latin sans (e.g. Inter or Vazirmatn's bundled Roboto pairing) for English — SIL OFL 1.1, free for commercial use, variable font, actively maintained, on Google Fonts and npm. |
| Calendar toggle | A single small persistent control (not a modal), same control in both languages, showing the *destination* calendar's name in its own language; remember the user's choice in a cookie/localStorage, default Gregorian in English mode and Solar Hijri in Persian mode. |
| Currency toggle | A two-state pill/segmented toggle ("Nominal" / "Real, 2015 USD") next to the chart, not buried in a settings menu — this is a per-chart interpretive choice, not a global site setting. |

The rest of this document is the evidence and detail behind these calls.

---

## 1. The hard question: RTL chart-axis directionality

This is the one place credible publishers disagree, so the evidence is worth laying out in full
rather than asserting a rule.

### What the research literature actually found

**Alebri, Rakotondravony & Harrison, "Design Patterns in Right-to-Left Visualizations: The Case
of Arabic Content," IEEE VIS 2024** ([UCL paper PDF](https://discovery.ucl.ac.uk/10194127/1/Alebri_accessible-2024_VIS_RTL_short_paper.pdf), [IEEE listing](https://ieeexplore.ieee.org/document/10771109/)) is the only systematic empirical
study of this question. They coded 128 real visualizations from 51 articles across seven Arabic
news outlets (Al Jazeera, BBC Arabic, CNN Arabic, Al Arabiya, Inkyfada, Alsifr, Arij), Nov 2023–Apr
2024. Findings, with exact numbers:

- **Categorical x-axis (bar charts, non-ordinal data): strong RTL consensus.** 81% placed the
  y-axis on the right (mirrored); only 9% kept it on the left. Designers clearly treat "no inherent
  direction" data as fair game for full RTL mirroring.
- **Numerical/time-series x-axis: genuinely split, but LTR wins and skews by publisher type.**
  58% kept the classic LTR structure (y-axis left, time flowing left→right); 33% fully mirrored
  (y-axis right, time flowing right→left). Critically: **85% of the outlets using the LTR pattern
  were mainstream media** (CNN Arabic, BBC Arabic) — the closest analogues to an "encyclopedia of
  record" — while **84% of the outlets using the RTL-mirrored pattern were independent/activist
  outlets** (Inkyfada, Alsifr). The paper explicitly flags this as unresolved "ambiguity," not
  consensus, and calls for community guidelines.
- Chart-component mirroring correlates with *whether the piece itself was translated from an
  LTR-language original*: 66% of translated visualizations mirrored at least one component (axis,
  legend, source, logo), suggesting mirroring is applied as a translation/localization reflex more
  than a reading-comprehension necessity.
- Legend position, when translated, generally moved toward the RTL side but was inconsistent (top-
  centre 31%, top-right 24%, top-left 22% — no dominant pattern). Source citation moved to
  bottom-right (84%) and publication logo to top-left (71%) regardless of RTL/LTR axis choice —
  i.e. *chrome mirrors even when the data axis doesn't*.

### Corroborating evidence

- **Datawrapper** ([blog post](https://www.datawrapper.de/blog/right-to-left-visualizations/)) is
  the most-cited counter-example: it *does* flip x-axes to RTL for line/area/column/scatter charts
  under `ar-*`, `fa-IR`, `he-IL` locales, while explicitly leaving numeral formatting and chart
  *shape* untouched. This is a real, shipped, tool-level default — but it is a locale-wide default a
  publisher must actively adopt or override, not evidence of reader preference.
- **Nick Doiron's survey** ([Medium, "Charts when you read right-to-left"](https://mapmeld.medium.com/charts-when-you-read-right-to-left-614f0a2cf54d), companion reference site [mapmeld.com/rtl-guide](https://mapmeld.com/rtl-guide/))
  independently surveyed real examples (World Bank reports, Arabic/Persian Wikipedia, Hebrew
  Wikipedia, an Arabic/English bilingual report, a Dhivehi-language commission report) and concludes
  LTR is "the more common practice, especially for line charts," while flagging Hebrew Wikipedia as
  a notable RTL-flipping exception. His practical advice: "check for context and previous experience
  in your language and region first."
- **Cross-cultural cognition research** cited in the IEEE paper (Fuhrman & Boroditsky 2010;
  Fagard & Dahmen 2003) shows RTL readers *do* have a measurably different default mental timeline
  when given no other cue — so the disagreement isn't manufactured, it reflects a real perceptual
  split that publishers have resolved in different directions.

### Recommendation for iranindata.org, and why

**Keep every axis carrying a temporal or continuously-ordered numerical dimension left-to-right in
both English and Persian modes. Do not flip time-series, area, scatter, or ordered-bar axes.**
Reasons specific to this project:

1. **Audience is public + researcher, and the content spans ~1,800 charts pulled from
   international sources (World Bank, IMF, FAOSTAT, etc.) that are themselves LTR-axis.** A visitor
   comparing an Iran chart against the original WDI/IMF chart benefits from identical axis
   orientation; flipping only in Persian mode creates a translation seam exactly where accuracy
   matters most (e.g., comparing an inflation chart in Farsi against a cited IMF source in English).
2. **The empirical base rate among mainstream/institutional Arabic publishers (CNN Arabic, BBC
   Arabic) — the closest reference class to "encyclopedia of record" rather than "opinion outlet" —
   is 85% LTR for exactly this chart type.** This project's positioning (neutral, sourced, public-
   good reference work) maps to that reference class, not to the independent-outlet reference class
   that skews RTL.
3. **A single global rule is dramatically cheaper to build, test, and keep consistent across 1,800
   charts than a per-chart-type mirroring matrix**, and the paper's own discussion section explicitly
   warns that *inconsistent* mirroring (which is what happens when different chart types/tools drift)
   damages comprehension more than a wrong-but-consistent choice.
4. **Do mirror everything that has no reading-direction cost and every RTL reader expects**:
   legend position, y-axis label side (put primary axis text on the right in Persian mode even
   though the plotted zero/origin geometry doesn't move), source/footnote citation position, logo/
   wordmark position, and all surrounding page chrome, nav, and text alignment. This matches what
   the IEEE data shows happens *regardless* of the axis-direction choice (source and logo position
   mirror in both LTR-axis and RTL-axis outlets alike) — it's the low-risk, high-expectation part of
   RTL support.
5. **Categorical bar charts (non-ordinal, e.g. "GDP by province" or "exports by product") should
   mirror fully** (y-axis/category labels on the right, bars growing right-to-left) per the 81%
   consensus finding — this is the one place the RTL convention is genuinely settled, and it's low-
   risk because there's no time axis to create source-comparison confusion.

Document this as a per-chart-type rule at build time: **ordinal/temporal x-axis → always LTR;
categorical axis with no inherent order → mirror per locale.**

---

## 2. Named references: bilingual/RTL data-design examples

| Reference | What it does well |
|---|---|
| [Datawrapper — RTL support](https://www.datawrapper.de/blog/right-to-left-visualizations/) | The clearest documented, tool-level spec of exactly what flips (axis direction for temporal charts, legend, table columns, bar orientation) vs. what doesn't (numeral formatting, chart "shape"). Good reference implementation even where this project's own axis call diverges from Datawrapper's default. |
| [Alebri et al., IEEE VIS 2024 short paper](https://discovery.ucl.ac.uk/10194127/1/Alebri_accessible-2024_VIS_RTL_short_paper.pdf) | The only empirical survey of real-world RTL chart practice; gives hard percentages instead of opinions (see §1). Cite this if a future collaborator questions the axis-direction call. |
| [mapmeld.com RTL guide](https://mapmeld.com/rtl-guide/) | Practical engineering-level detail beyond layout: canvas text-anchor quirks for RTL, an SVG `<textPath>` RTL bug in Chromium/WebKit, per-script numeral tables (Arabic-Indic, Hebrew, Adlam), currency-symbol placement conventions. Useful at implementation time, not just design time. |
| [W3C — Structural markup and right-to-left text in HTML](https://www.w3.org/International/questions/qa-html-dir) | The baseline spec every mirroring decision should trace back to: use `dir="rtl"` on the document/region, not CSS `direction` alone, and don't hardcode `margin-left`/`float:left` — use logical CSS properties (`margin-inline-start`, etc.) so mirroring is automatic. |
| [Material Design 3 — Bidirectionality & RTL](https://m3.material.io/foundations/layout/bidirectionality-rtl) | A concrete "what mirrors / what doesn't" checklist at the component level (icons with directional meaning flip, icons depicting real-world objects/media-transport controls don't, numerals don't) — directly transferable to a chart-heavy site's icon set (download, share, sort-arrow icons). |
| [U.S. Web Design System — "Select a language: two languages" pattern](https://designsystem.digital.gov/patterns/select-a-language/two-languages/) | A government-grade, accessibility-audited reference implementation for exactly the 2-language case this project has (no dropdown needed for 2 languages — direct toggle showing the *other* language's name). |
| [Smart Interface Design Patterns — Language Selector UX](https://smart-interface-design-patterns.com/articles/language-selector/) and [SimpleLocalize — flags in language selectors](https://simplelocalize.io/blog/posts/flags-as-language-in-language-selector/) | Converging, evidence-based case against flag icons for language selection (flags represent countries, not languages — irrelevant confusion for Persian, which isn't tied to one flag) and for using each language's own endonym as the label. |
| [Vazirmatn font project](https://github.com/rastikerdar/vazirmatn) ([Google Fonts listing](https://fonts.google.com/specimen/Vazirmatn)) | The most actively maintained free/open Persian variable webfont; ships a matched Latin companion so EN/FA body text sits at consistent x-height and weight — solves the "two unrelated fonts stitched together" look common on bilingual Persian sites. |

---

## 3. Numeral system: recommendation and rationale

Persian uses Eastern Arabic-Indic digits (۰۱۲۳۴۵۶۷۸۹), each a distinct Unicode codepoint from
Western digits, with ۴/۵/۶ visually unlike their Western counterparts (real risk of misreading if a
reader assumes shape-similarity, per the Eastern Arabic numerals literature). Real-world Persian
practice is itself split: formal prose and government publications commonly use Persian digits;
financial/market data platforms (Tehran Stock Exchange terminals, most Persian-language brokerage
and central-bank statistical tables) commonly keep Western digits in tabular data even in fully
Persian-language UI, precisely because tabular/financial data needs to interoperate (copy-paste
into spreadsheets, match international tickers, avoid font-rendering ambiguity for ۴/۵/۶).

**Recommendation: Western digits everywhere a number is data — axis ticks, tooltips, data tables,
CSV/download output, chart values, year labels — in both languages.** Reserve Persian digits for
decorative/structural Persian UI text only (e.g., a Persian-language page listing "۱۲ مقاله" — "12
articles" — as prose), if at all; even that is optional polish, not a requirement. This avoids:
building/maintaining a second numeral-rendering path through every chart library and CSV exporter;
screen-reader mispronunciation risk (Persian digit-to-speech support is inconsistent across screen
readers); and the ۴/۵/۶ misread risk entirely. If user feedback later shows a strong public
preference for Persian digits in the prose layer only, that's a low-cost, purely-cosmetic follow-up
that never touches the data/export layer.

---

## 4. Font choice

**Vazirmatn** ([GitHub](https://github.com/rastikerdar/vazirmatn), [Google Fonts](https://fonts.google.com/specimen/Vazirmatn), [npm](https://www.npmjs.com/package/vazirmatn)):
SIL Open Font License 1.1 (free, commercial-safe, no attribution burden beyond keeping the license
file), variable font with a 100–900 weight axis, ships a Latin companion (built from Roboto) so
English and Persian text share visual weight/rhythm on the same page — important for a genuinely
mixed-script encyclopedia where a single sentence or chart title can carry both scripts (e.g. a
World Bank citation inside a Persian sentence). Actively maintained (project started 2015 as
"Vazir," relaunched as Vazirmatn), which matters for a long-lived public-good project versus a
one-off commercial Persian font (IRANSans, Yekan) that may lapse in support or carry a commercial
license per-project/per-seat. Estedad is a reasonable OFL-licensed alternative if Vazirmatn's
letterforms don't suit — same licensing category, less community adoption than Vazirmatn.

---

## 5. Language toggle design pattern

- **No flags.** Persian isn't a nation-flag language (spoken in Iran, Afghanistan, Tajikistan)
  and flags map to countries, not languages — a well-established anti-pattern per SimpleLocalize
  and the language-selector UX literature above.
- **Label each option in its own script/endonym**, not translated: "فارسی" and "English", never
  "Persian" / "انگلیسی". This is the USWDS and Smart Interface Design Patterns consensus.
- With exactly two languages, **skip the dropdown** — a direct toggle/pill in the header showing
  the *other* language's name is faster and matches the USWDS two-language pattern exactly.
- Persist the choice (localStorage + `?lang=` or `/fa/` path for shareable/indexable URLs — see the
  existing frontend memory note on `/en/` vs `/fa/` routing, which this research doesn't need to
  re-decide).
- Placement: top-right of the header in LTR/English mode; when the page flips to `dir="rtl"`, the
  entire header mirrors via logical CSS properties (§2, W3C reference) so the toggle lands top-left
  automatically — don't hardcode its position per language.

---

## 6. Three-calendar toggle design pattern

No major bilingual data site currently exposes three calendar systems simultaneously (Gregorian /
Jalali / Imperial is a niche specific to this project's Pahlavi-era focus), so there's no single
site to copy wholesale — but several adjacent patterns compose well:

- **Persian-market date pickers already solve the 2-calendar (Gregorian/Jalali) toggle cleanly**:
  the Azar Datepicker ([cssscript.com writeup](https://www.cssscript.com/persian-jalali-gregorian-date-picker-azar/))
  ships a `showCalendarToggle` control — a small inline switch inside the date-display component
  itself, not a separate settings page. MUI X's date pickers ([calendar-systems docs](https://mui.com/x/react-date-pickers/calendar-systems/))
  solve the underlying conversion with a pluggable "calendar adapter" (`AdapterDateFnsJalali`,
  `AdapterMomentJalaali`) — validates the memory note's recommendation to use a real Jalali-
  conversion library rather than hand-rolling it.
- **Extend that inline-switch pattern to three options** as a small segmented control or compact
  dropdown attached directly to every date/year label on a chart (axis ticks, tooltip dates, "as of"
  captions) — not a single global site-wide radio button buried in settings, because a user may want
  Imperial for a Pahlavi-era chart and Jalali for a post-1979 chart in the same browsing session.
  Still remember a *default* per language (Gregorian default in English mode, Solar Hijri default in
  Persian mode — Imperial is opt-in, never default, given it was only in official use 1976–1978 and
  most users won't recognize it unprompted).
  A good middle ground: **one global calendar preference control in the header (persisted), which
  every chart respects, plus a small unobtrusive "compare calendars" hover/tooltip on individual date
  labels** so a reader can see the other two systems without switching global state — this avoids
  forcing a mode switch just to sanity-check one date.
  This matches the constraint noted in project memory that calendar choice is a pure *display*
  transformation (no backend/data changes) — the UI should treat it exactly like the numeral or
  language toggle: a rendering preference, not a data query parameter.

---

## 7. Currency toggle (nominal vs. real-USD) design pattern

- This is a **per-chart interpretive decision** (does the reader want the number as reported, or
  inflation-adjusted?), not a global account setting — so it should live **next to each chart**, not
  in a site-wide settings menu, mirroring how the currency toggle is scoped in the backend (per-
  chart `variant_code`/`currency_display` fields, per the project's existing bookkeeping doc).
- Use a **two-state segmented control / pill**, not a checkbox or a dropdown: "Nominal" vs. "Real
  (2015 USD)" as mutually exclusive, always-visible labeled buttons — a dropdown hides the fact that
  a transformation is being applied at all, which matters for a research-grade encyclopedia where the
  reader needs to *notice* the adjustment basis, not just have a default silently applied.
  Default to "Real" per existing project convention; make the current state visually obvious (not
  just a settings-icon flyout) since it changes the y-axis values a reader might screenshot or cite.
- Keep this control's position and shape **identical between English and Persian modes** other than
  RTL text mirroring — currency toggle state, like numerals, is data-layer, not language-layer, and
  shouldn't invite a reader to think nominal/real differs by language.

---

## 8. Accessibility checklist for interactive charts in an encyclopedia

Consolidated from Smashing Magazine's WCAG-for-charts breakdown ([Amy Cesal / Smashing
Magazine, "How Accessibility Standards Can Empower Better Chart Visual Design"](https://www.smashingmagazine.com/2024/02/accessibility-standards-empower-better-chart-visual-design/)),
the A11Y Collective's chart checklist ([a11y-collective.com](https://www.a11y-collective.com/blog/accessible-charts/)),
and Tableau's accessible-views guidance ([help.tableau.com](https://help.tableau.com/current/pro/desktop/en-us/accessibility_best_practice.htm)) — the recurring, non-negotiable items for a
1,800-chart public-good encyclopedia, in priority order:

**Must-have (blocks WCAG 2.1 AA):**
1. **Every chart has a data-table alternative** reachable by keyboard/screen reader — not just an
   `alt` attribute; for anything beyond the simplest single-series chart, alt text alone is
   insufficient. Given this is an encyclopedia backed by real tabular source data already, exposing
   the underlying series as an actual `<table>` (visually hidden or in a "view data" expandable) is
   low-cost and directly reuses existing data.
2. **Color contrast**: chart marks (bars/lines/points) ≥ 3:1 against their background and against
   adjacent marks; all text (titles, labels, legends) ≥ 4.5:1. Verify against both light and dark
   themes and against the RTL-mirrored layout, not just the LTR default.
3. **Never encode meaning by color alone.** Every series needs a second encoding — direct labeling,
   distinct line-dash/marker-shape per series, or pattern fill for area/bar charts — critical for
   color-blind readers and for any reader viewing a printed/grayscale export.
4. **Color-blind-safe categorical palette**: avoid red/green as the sole distinguishing pair; favor
   blue/orange or teal/magenta-style palettes validated for deuteranopia/protanopia. With ~1,800
   charts sharing a design system, this should be one shared, tested palette token set, not a
   per-chart choice.
5. **Keyboard navigation** of any interactive element (tooltips, zoom, series toggle, calendar/
   currency toggles) — full tab-order reachability, visible focus rings meeting 3:1 contrast against
   the background, no keyboard traps.
6. **Reduced motion**: any animated transition (chart load-in, toggling nominal/real, switching
   calendars) must respect `prefers-reduced-motion` and any auto-playing/looping chart (e.g. an
   animated time-series) needs a pause/stop control, per WCAG 2.2.2.
7. **Meaningful screen-reader labels beyond the generic** — the IEEE RTL paper found only 52% of
   sampled Arabic-news charts had a *meaningful* (not generic "chart"/"image") screen-reader
   description; this project should exceed that bar given the research-reference use case: every
   chart's aria-label/description should state the metric, unit, date range, and source, not just a
   generic "line chart" label.

**Strongly recommended:**
8. Text summary / key-takeaway caption near each chart (not solely relying on the visual) — helps
   both screen-reader users and quick-scanning sighted users.
9. Focus-visible, distinguishable interaction states (hover/selected) that don't rely on color shift
   alone (e.g. add a stroke or size change too).
10. Verify RTL mirroring doesn't break any of the above — e.g., confirm focus order still follows
    logical (not visual) reading order in `dir="rtl"` mode, and that mirrored legends/axes retain
    their contrast and dual-encoding.

---

## Sources consulted

- Alebri, Rakotondravony & Harrison, "Design Patterns in Right-to-Left Visualizations: The Case of Arabic Content," IEEE VIS 2024 — https://discovery.ucl.ac.uk/10194127/1/Alebri_accessible-2024_VIS_RTL_short_paper.pdf / https://ieeexplore.ieee.org/document/10771109/
- Datawrapper Blog, "Support for right-to-left languages in all visualizations" — https://www.datawrapper.de/blog/right-to-left-visualizations/
- Nick Doiron, "Charts when you read right-to-left" (Medium) — https://mapmeld.medium.com/charts-when-you-read-right-to-left-614f0a2cf54d
- Nick Doiron, RTL Guide — https://mapmeld.com/rtl-guide/
- W3C, "Structural markup and right-to-left text in HTML" — https://www.w3.org/International/questions/qa-html-dir
- Material Design 3, "Bidirectionality & RTL" — https://m3.material.io/foundations/layout/bidirectionality-rtl
- U.S. Web Design System, "Select a language: two languages" — https://designsystem.digital.gov/patterns/select-a-language/two-languages/
- Smart Interface Design Patterns, "Language Selector UX" — https://smart-interface-design-patterns.com/articles/language-selector/
- SimpleLocalize, "Flags in language selectors: Why they may hurt UX" — https://simplelocalize.io/blog/posts/flags-as-language-in-language-selector/
- Vazirmatn font — https://github.com/rastikerdar/vazirmatn / https://fonts.google.com/specimen/Vazirmatn
- Eastern Arabic numerals — https://en.wikipedia.org/wiki/Eastern_Arabic_numerals
- Azar Datepicker (Jalali/Gregorian toggle) — https://www.cssscript.com/persian-jalali-gregorian-date-picker-azar/
- MUI X, "Date and Time Pickers — Calendar systems" — https://mui.com/x/react-date-pickers/calendar-systems/
- Smashing Magazine, "How Accessibility Standards Can Empower Better Chart Visual Design" — https://www.smashingmagazine.com/2024/02/accessibility-standards-empower-better-chart-visual-design/
- The A11Y Collective, "The Ultimate Checklist for Accessible Data Visualisations" — https://www.a11y-collective.com/blog/accessible-charts/
- Tableau, "Best Practices for Designing Accessible Views" — https://help.tableau.com/current/pro/desktop/en-us/accessibility_best_practice.htm
