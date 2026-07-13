# FAO GIEWS Country Brief — Iran, 2010–2026 (2026-07-13)

Extracted from `data/raw/fao-giews/giews-iran-brief/` (both files, immutable, unchanged): the
current brief (`giews-iran-brief_2026-07-12.pdf`, reference date 10-June-2026) and a 40-page
**archive of 21 prior briefs** spanning 03-September-2010 to 24-November-2025
(`giews-iran-brief-archive_2026-07-12.pdf`). Both are born-digital PDFs (Word/Acrobat exports),
fully `pdftotext -layout` extractable, no OCR needed. Unlike most FAO/UN statistical sources in
this project, GIEWS briefs are narrative prose (crop-condition assessments, not structured data
tables) — every figure below was manually located and transcribed from running text, each row
tagged with its exact source brief's reference date so a reader can trace any number back to its
paragraph.

## Files

| File | Coverage | What it covers |
|---|---|---|
| `cereal_production_estimates_2010_2025.csv` | 25 rows, crop years 2010–2025 (uneven — only years GIEWS reported a specific tonnage) | Wheat, rice, and total-cereal production estimates/forecasts, each tagged with its status (estimated/forecast/preliminary) and the exact brief it came from |
| `cereal_import_requirements_2010_2027.csv` | 17 rows, marketing years (April/March) 2010/11–2026/27 | Total cereal + maize/wheat/barley/rice import requirement forecasts |
| `food_price_fx_context_2012_2026.csv` | 15 rows, 2012–2026 | Food-price inflation (YoY), general inflation, and the dual-tier subsidized/market exchange rate, as FAO's own GIEWS analysts reported them (citing Iran's Central Bank) |
| `wheat_guaranteed_purchase_price_2013_2026.csv` | 8 rows, crop years 2013–2026 | Government-guaranteed wheat procurement price (common/durum), a direct farm-gate policy lever distinct from retail/market prices |

## Why this source is valuable despite being narrative, not tabular

This is the **only source in this project with a continuous, dated 2010–2026 read on Iran's
cereal harvest, food-import needs, and food-price/FX stress**, assessed independently by FAO's
own analysts rather than sourced from Iranian official statistics alone (GIEWS cross-references
satellite crop-monitoring, ministry announcements, and market reporting). It directly complements
FAOSTAT's own production series (`data/processed/agriculture_qcl_production.csv`) with a
higher-frequency, policy-context-rich narrative layer, and gives an independent read on Iran's
exchange-rate/inflation trajectory alongside the project's TGJU-sourced parallel-market series
and the SCI-sourced CPI series in `data/processed/sci_yearbook_1399_series/cpi_by_group_1390_1399.csv`
(built earlier in this same round).

## Caveats — read before charting

- **This is narrative prose, not an official statistical release** — every value here is FAO
  GIEWS's own analytical estimate/forecast at the time of writing, not a primary Iranian
  government statistic (even where the brief cites a government announcement, e.g. procurement
  prices). Treat as a secondary, expert-assessed source, not primary data.
- **Multiple within-year revisions are preserved, not reconciled** — several crop years have
  two or more GIEWS estimates that materially disagree because later briefs had better
  information (e.g. 2015 wheat: 13.0 Mt FAO forecast in the June-2015 brief vs. 11.5 Mt
  Government-sourced estimate in the February-2016 brief for the SAME crop year; 2015/16 cereal
  import forecast: 14.9 Mt in June-2015 vs. 10.0 Mt in February-2016 as the harvest outlook
  improved). Every such case is flagged in the `notes` column of the affected rows — do not
  average or pick one arbitrarily; the "later" brief is not automatically "more correct" for
  charting purposes, just more informed at that point in time.
- **`wheat_guaranteed_purchase_price_2013_2026.csv`'s 2026 row required a unit conversion**: the
  source brief states the 2026 price in **tomans** (49,650 tomans/kg) while every other row in
  this file is in rials as printed in ITS OWN brief — converted to IRR (496,500 IRR/kg, at the
  fixed 1 toman = 10 rials relationship) for column consistency, with the original toman figure
  preserved in the `notes` column. This is the only cross-unit conversion performed in this
  extraction; every other value is transcribed exactly as printed.
- **Reference dates, not calendar years, are the true index** for the FX/inflation file — Iran's
  Central Bank publishes inflation on the Iranian solar calendar, and GIEWS briefs report
  whichever period was most recently available at writing time (sometimes a single month,
  sometimes a period spanning parts of two Gregorian years) — the `date` column records what the
  brief itself specifies (a month, or a period), not a normalized annual figure.
- **Total cereal production figures and wheat-only production figures are DIFFERENT metrics** in
  `cereal_production_estimates_2010_2025.csv` — Iran's total cereal figure (which includes wheat,
  barley, rice, and maize) is roughly 1.5–2x the wheat-only figure in most years; the `crop`
  column disambiguates every row, but do not sum wheat + cereal_total rows together.
- **The archive PDF contains one duplicated brief** (20-July-2020, appearing twice in the source
  document, identical content both times) — only extracted once here.
- Both raw PDFs' full manifests: `data/raw/fao-giews/giews-iran-brief/manifest.json`.

## Sources

FAO GIEWS (Global Information and Early Warning System on Food and Agriculture), *Country Brief:
Iran (Islamic Republic of)*, all available editions 2010–2026 —
`data/raw/fao-giews/giews-iran-brief/giews-iran-brief_2026-07-12.pdf` (current) and
`giews-iran-brief-archive_2026-07-12.pdf` (21-edition historical archive). Extraction method:
`pdftotext -layout` (clean, born-digital PDF text; no OCR needed).
