# USGS Minerals Yearbook — Comparator Countries (2014–2023)

Extracted 2026-07-13 from `data/raw/usgs-minerals-yearbook/{arg,tur,sau,rus,usa}/` (immutable,
unchanged) into one combined tidy CSV, matching the column schema already used for Iran in
`data/processed/iran_mining_series/usgs_iran_mineral_production_1961_1980.csv` — the only
difference is the `unit` and `flag` columns per row instead of being folded into the header, and
the addition of a `country_iso3` column so all five countries share one file.

## File

`usgs_minerals_comparators_2014_2023.csv` — 4,112 rows, columns: `country_iso3, category,
commodity, unit, year, value, flag, source_yearbook_edition`.

| Country | Rows | Years covered | Source |
|---|---|---|---|
| Argentina | 545 | 2014–2021 | myb3 "country report" Table 1, editions 2017-18/2019/2020-21 |
| Türkiye | 1,191 | 2014–2022 | myb3 Table 1, editions 2017-18/2019/2020-21/2022 |
| Saudi Arabia | 694 | 2014–2023 | myb3 Table 1, editions 2017-18/2019/2020-21/2022/2023 |
| Russian Federation | 1,344 | 2014–2022 | myb3 Table 1, editions 2017-18/2019/2020-21/2022 |
| United States | 338 | 2017–2023 | Mineral Commodity Summaries (mcs) 2022/2023/2024, "Salient Statistics — Production" blocks |

## Method — efficiency note

For Argentina, Türkiye, Saudi Arabia, and Russia, USGS ships a companion **`.xlsx`** workbook
alongside every `myb3-*.pdf` country report (a "Table 1" sheet: commodity x 5 years, already
machine-readable). Parsing these structured spreadsheets directly is far more reliable and far
cheaper than PDF/OCR extraction, so that's what was used — `pdftotext -layout` on the matching
PDF was used only as a cross-check (Russia's 2018-2022 uranium series was spot-checked this way:
exact match, `2,904 / 2,911 / 2,846 / 2,635r / 2,508` metric tons). Each country's 2016-edition
`.xls` file is in the legacy Excel-97 binary format (not readable by the `openpyxl` library
available in this environment) and was skipped — it would only have added 2012-2013 data, already
superseded in value by the 2017-18-edition xlsx's overlapping 2014-2018 window. Multiple editions
per country were merged, with a later edition's value overwriting an earlier edition's for the
same (commodity, year) — i.e. the most-recently-published, most-revised figure wins.

The United States has **no country-report xlsx** in this raw folder — `usa/` instead holds three
annual **Mineral Commodity Summaries** booklets (global, organized one page per commodity, not
per-country), so extraction there means locating each commodity's "Salient Statistics — United
States" table and pulling its "Production" line-item(s) via `pdftotext -layout` text parsing (born
-digital PDF, no OCR needed). 19 major commodities were selected for breadth: Aluminum, Barite,
Cement, Chromium, Copper, Gold, Gypsum, Iron and Steel, Iron Ore, Lead, Manganese, Molybdenum,
Nickel, Phosphate Rock, Salt, Silver, Sulfur, Tin, Titanium Mineral Concentrates, Zinc — the same
mix of base metals and industrial minerals used in Iran's own extraction, so the two are directly
comparable commodity-by-commodity.

## Known limitations (not fabricated, just not extracted)

- Some USA line-wrapped table rows (where a "(e)stimated" flag pushed the final 1-2 year columns
  onto their own physical line in `pdftotext -layout` output) had those trailing years dropped
  rather than risk misattributing the wrapped fragment as a new commodity label — e.g. some
  Copper/Cement rows may be missing their most recent 1-2 years. Never guessed; just left out.
- USA commodity labels drift slightly in wording between MCS editions (e.g. "Mine, recoverable"
  in the 2024 edition vs. "Mine, recoverable copper content" in the 2022/2023 editions for the
  same underlying Copper series) — this creates two adjacent-but-not-identical `commodity` keys
  for what is conceptually one series, rather than a single continuous one. Left as-is (faithful
  to the source label text) rather than hand-harmonized; a downstream consumer building a single
  Copper-mine-production chart should treat these as one series.
- Manganese "mine" production for the USA is genuinely `0` every year 2019-2023 — this is a real
  fact (the US has not mined manganese ore since 1970), not a missing-data placeholder; the
  source explicitly uses "— Zero" (as opposed to "NA"/"W" for genuinely unavailable/withheld
  data, which were left blank here, never coerced to zero).
- Historical (pre-1990) USGS volumes for these five comparators were NOT touched here — Argentina
  and Türkiye already got a small 1968-1970 comparator slice inside
  `data/processed/iran_mining_series/usgs_comparator_argentina_turkey_metals_1968_1970.csv` from
  an earlier pass; this file's job was specifically the un-extracted modern-era (2014-2023)
  editions that were sitting as raw PDFs/spreadsheets.

## Headline commodities at a glance (most recent year available per country)

| Country | Notable 2022/2023 figures |
|---|---|
| Saudi Arabia | Cement, phosphate rock, and gold production feature heavily; large industrial-minerals base alongside its hydrocarbons sector (petroleum itself is out of scope for this mining-yearbook source) |
| Russia | Comprehensive metals + industrial minerals coverage (93 distinct commodity line items for Saudi Arabia alone illustrates the granularity — Russia's table is even larger at 1,344 rows) |
| Türkiye | Large boron/bauxite/chromite producer; strong industrial-minerals presence |
| Argentina | Lithium carbonate/chloride, cement, and construction aggregates dominate; copper mine production largely idle after 2018 (`--` = zero reported in several years) |
| United States | Copper mine production ~1.1-1.3 million t/yr; effectively zero domestic manganese, tin, and titanium-mineral-concentrate self-sufficiency (heavy import reliance, consistent with the source's own "net import reliance" framing) |
