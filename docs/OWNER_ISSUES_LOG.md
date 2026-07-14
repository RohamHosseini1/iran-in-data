# Owner issues log

Every complaint / instruction the project owner raised in the data-quality session
(2026-07-14), in the order raised. Kept in the repo so it survives a context reset.

Status key: **DONE** · **PARTIAL** · **OPEN** · **REVERTED** (owner later changed his mind)

---

## Round 1 — the original data-quality brief

| # | Issue | Status |
|---|---|---|
| 1 | Topical one-off charts must not exist (e.g. "Iraq's 1986 Debt Rescheduling Agreement", "Iran-Iraq Trade and Oil Export Revenue"). Apply the logic **across the board**, not just to the named examples. | DONE |
| 2 | No single-year / single-project charts (e.g. the 1960 multipurpose dam project). | DONE |
| 3 | Low-quality charts that show nothing (fermented beverages: imports ~nothing, exports ~nothing, domestic supply one flat line). Remove or improve. | DONE |
| 4 | The duck chart: most submeasures are bad/wrong. | DONE |
| 5 | If a chart tells you nothing: remove it, or better, **enrich it** — especially from **Iranian government sources** (we had essentially zero: parliament, ministries, CBI, SCI). | DONE |
| 6 | A valid chart = one specific clear **measure over time** (production of X, from earliest to latest data), with events/policies overlaid on it. | DONE (doctrine) |
| 7 | Enrich each measure with as many sources as possible; multi-source is the goal. | PARTIAL |
| 8 | Comparator countries: too many Europeans. Keep Spain + 1–2 (Italy/Greece), **add Iraq**, keep Russia/US/Argentina/Turkey/Saudi/Venezuela. ~5 on average. | DONE |
| 9 | Aquatic-plants chart: ~10 measures, all empty/illegible. Should not have 10 measures per chart. | DONE |
| 10 | Go through **all** the data: enrich, find gaps, trim excess measures, merge overlapping charts, delete nonsense charts. | PARTIAL |
| 11 | **Titles**: the measure must not be in the title. "GDP (current U.S. dollars)" → "GDP". "Official vs parallel black-market USD exchange rate and the gap" → "U.S. Dollar Exchange Rate". | DONE (then over-corrected, see #31) |

## Round 2 — "you didn't actually apply it"

| # | Issue | Status |
|---|---|---|
| 12 | The charts I named **by name** are still there (dam charts, CIA Iran/Iraq charts). You didn't apply the logic across the board. | DONE |
| 13 | Explain my logic back to me so I know you understand it. | DONE |

## Round 3 — new sources

| # | Issue | Status |
|---|---|---|
| 14 | Use the brsapi (TSETMC) + Navasan API keys and CBI. **Do not create a separate chart per source** — embed as an additional source on the EXISTING chart. Same measure ⇒ multi-source. | DONE |
| 15 | Keep enriching. **Longer timelines are better.** Primary Iranian government sources, especially back to the 1950s–60s. | PARTIAL |
| 16 | Three standing tasks: (1) clean up the data we already have, (2) find more sources to enrich existing measures, (3) find new sources / new measures. | ONGOING |
| 17 | The laws corpus (17.7k Persian files): work out which policies are relevant to which charts, with confidence + causation. | **REDO** (see #35–37) |

## Round 4 — annotation layers

| # | Issue | Status |
|---|---|---|
| 18 | Laws layer: low-opacity **grey**, non-invasive, hover for detail. **Persian-first**: use the original Persian text as-is; translate to English for the EN site. | DONE |
| 19 | Events layer: only ~5 events exist, most charts have none. Enrich massively (world + country-specific). Keep the golden-orange colour. Events are English-only and the Persian site shows English — **that is broken**. | DONE |
| 20 | Well-known periods (Revolution, war) could be timeline **zones** rather than markers. | **REVERTED** (#25) |
| 21 | Concern about too many laws per chart → show strongest, keep the rest in a list below. | **REVERTED** (#26) |

## Round 5 — deploy + comparators

| # | Issue | Status |
|---|---|---|
| 22 | Commit, push, deploy the newest version. | DONE |
| 23 | Do another data-quality check on the charts we have. | DONE |
| 24 | Comparator countries: pull **their economic data** so the comparison lines exist. **No laws/policy/timeline for comparators** — that layer is Iran-only. | DONE |

## Round 6 — annotation corrections

| # | Issue | Status |
|---|---|---|
| 25 | **Remove the era bands.** Not legible. | DONE |
| 26 | The 8-law marker cap is too few: a cluster of 1950s laws exhausts the budget and later ones never appear. **Do not limit at all** — it's not that many laws. | DONE |
| 27 | Honorific: neutral register is the right call, but apply it to **Islamic Republic** figures only, **not** pre-revolution. | DONE |
| 28 | The **events are not translated to Persian** on the Persian site. | DONE (titles/descriptions) |
| 29 | **Any event added must be bilingual.** | DONE |
| 30 | Events with confidence **5 are not on the map**, while confidence-**2** ones are. The selection logic is broken. | DONE (cap removed) |

## Round 7 — titles / empty measures / labels

| # | Issue | Status |
|---|---|---|
| 31 | **Titles over-stripped.** I asked you to remove the *unit* (tonnes, US$), not the *measure*. Now charts are just "Apples", "Plums", "Artichokes", and four different charts are all called "Bananas". | DONE |
| 32 | **Empty charts/measures**: selecting an alternative measure (e.g. Chillies → "FAO current") renders empty. Find the **root cause** — was data deleted? Either find the data, or delete the chart/measure. No empty charts. | DONE |
| 33 | Measure labels are unclear, e.g. "Producer Price Index (2014 to 2016 = 100)" — the parenthesis means nothing to a reader. Applies to many labels. | DONE |

## Round 8 — the annotation-quality failure

| # | Issue | Status |
|---|---|---|
| 34 | **English text inside the Persian site.** The law/event detail cards render `justification`, `caveats`, `lag`, and field labels in English on the FA page. | DONE |
| 35 | **Law→chart mapping coverage is bad.** The GDP chart has exactly **one** law attached across a century of Iranian legislation. That is not credible. | DONE (GDP: 1 -> 145) |
| 36 | **Confidence scoring is incoherent.** The White Revolution is scored confidence **1** ("context") against Iran's GDP. The scale is being applied inconsistently across the board. | DONE (two scores: relevance + attribution) |
| 37 | **META-RULE (applies to everything):** when the owner points out one bad instance, it is a **signal of a systemic failure**, not a request to patch that one chart. Re-do the whole class of work and verify it globally. | **STANDING** |

## Round 9 — annotation noise

| # | Issue | Status |
|---|---|---|
| 38 | **Comparator-country domestic events are annotating Iranian charts.** Argentina's peso peg, the 1994 Turkish lira crisis, appearing on Iran's inflation chart. Only events **directly related to Iran** (plus genuine global shocks) belong. | DONE |
| 39 | **Too many annotations to read.** "So many that I basically don't see the laws, and I don't see the chart either." | DONE |
| 40 | **Weak links must not be drawn.** Anything below confidence 2 belongs in the list at the bottom, not on the chart. | DONE |
| 41 | «انتساب علّی» is Arabic-flavoured; use a proper Persian term. | DONE (now «اطمینان از تأثیر») |

## Round 10 — markers invisible, zoom unusable, laws untranslated

| # | Issue | Status |
|---|---|---|
| 42 | **Law markers are invisible.** "It is just a gray bar, but it doesn't have the circle on top to indicate that there is something on this timeline." A 1px dashed grey line at 0.38 opacity with no symbol read as a gridline. | DONE (dot head, own bottom rail, opacity up) |
| 43 | **Laws must be drawn whenever relevance > 2.** The old gate also demanded attribution >= 3; laws are almost never attributable, so that gate deleted the grey layer from a third of the charts. Laws now gate on relevance alone; events keep the two-score gate. | DONE |
| 44 | **The chart is "fidgety".** Zoom jumps from a decade to a single year, drifts while zooming, and cuts at random places. Cause: ECharts' coarse per-tick wheel step, plus a snap-to-year timer that yanked the window 260ms after every gesture. | DONE (own eased, cursor-anchored zoom; snap timer removed) |
| 45 | **Chart must not zoom out past the data.** | DONE (hard-clamped to the data extent; verified) |
| 46 | **Law titles are not translated on the English site.** 491 of 970 linked laws had NO English title at all. | DONE (970/970 now) |
| 47 | **Still "dozens of events of random countries".** Genuine global shocks were being stapled to every chart in a category, so Iran's apple chart carried "China WTO accession", "Asian Financial Crisis" and "Russian default and LTCM". | DONE (global events reaching a chart only by category must clear relevance 3; 689 links dropped) |

## Round 10b — bugs found while fixing the above (not reported by the owner)

| # | Issue | Status |
|---|---|---|
| 48 | **Persian law titles were mangled.** The title was taken from the FILENAME, and the scraper had elided filenames to fit the 255-BYTE filesystem limit (Persian is 2 bytes/char), so 359 of 1,111 significant laws carried `head ... tail` with the middle missing. Recovered 165 by joining on the scraper's own ndjson dumps, verified head+tail so nothing is guessed. | PARTIAL |
| 49 | **194 law titles remain elided and CANNOT be recovered here.** The source (qavanin.ir) geoblocks non-Iranian IPs (403 via ArvanCloud), and those laws have no whole-law record in the local ndjson dumps. Needs a fetch from an Iranian IP. **Nothing was invented to paper over this.** | OPEN (blocked on network access) |
| 50 | **The same event appeared twice on one chart** ("US withdraws from the JCPOA" and "US withdraws from JCPOA", one from each timeline). | DONE (deduped on a loose title key; Iran's telling wins) |

---

## Standing rules extracted from the above

1. A chart = one clear **measure over time**. Events/laws overlay it; they are never charts themselves.
2. **Iran-first**: a measure with no Iran data is not a measure of Iran.
3. Same measure from several sources ⇒ **one chart, multiple cited sources**. Never a chart per source.
4. **Never fabricate.** If sources disagree, keep both labelled; if data is missing, say so.
5. **Longer timeline is always better.** Backward extension of an existing series beats a new short one.
6. **Bilingual is not optional.** Anything user-facing exists in EN and FA. Laws are Persian-first; events are English-first and must be translated.
7. **No em dashes** anywhere in site copy.
8. Comparators get **economic data only** — never the laws/policy layer.
9. When one defect is reported, **fix the class, not the instance** (#37).
10. **Iran-first annotations**: only Iran's own events and genuine global shocks annotate charts. A comparator's purely domestic event never does (#38).
11. **Markers are quality-gated, not count-capped**: draw an annotation only if relevance is top (5) or it is genuinely attributable (attribution >= 3), never below relevance 2. Everything else is still listed in full below the chart (#39, #40).
