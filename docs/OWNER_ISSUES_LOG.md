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

## Round 8 — the annotation-quality failure (CURRENT)

| # | Issue | Status |
|---|---|---|
| 34 | **English text inside the Persian site.** The law/event detail cards render `justification`, `caveats`, `lag`, and field labels in English on the FA page. | **OPEN** |
| 35 | **Law→chart mapping coverage is bad.** The GDP chart has exactly **one** law attached across a century of Iranian legislation. That is not credible. | **OPEN** |
| 36 | **Confidence scoring is incoherent.** The White Revolution is scored confidence **1** ("context") against Iran's GDP. The scale is being applied inconsistently across the board. | **OPEN** |
| 37 | **META-RULE (applies to everything):** when the owner points out one bad instance, it is a **signal of a systemic failure**, not a request to patch that one chart. Re-do the whole class of work and verify it globally. | **STANDING** |

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
