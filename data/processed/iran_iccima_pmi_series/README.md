# Iran ICCIMA Purchasing Managers' Index (PMI) and Business Environment series (FY1403-1405 / 2024-2026)

**New category for this project — a real-time, monthly, forward-looking Iranian economic
indicator.** Harmonized 2026-07-13 from `data/raw/iccima-iran/pmi-and-reports/` (6 raw PDFs,
unchanged). ICCIMA (Iran Chamber of Commerce, Industries, Mines & Agriculture) runs a monthly
survey-based Purchasing Managers' Index modeled on the international ISM/S&P Global PMI
methodology (50 = no-change threshold) — this is the only genuinely high-frequency, forward-
looking indicator in this entire database; almost everything else is annual.

## Files

| File | Coverage | What it covers |
|---|---|---|
| `pmi_yearbook_fy1403_by_sector.csv` | Iranian FY1403 (Farvardin-Esfand 1403 ≈ March 2024-March 2025), all 12 months | **The richest find: 14 separate monthly PMI tables** (whole economy + Manufacturing sector aggregate + 12 individual manufacturing sub-sectors: rubber & plastics, petroleum & gas products, textiles, machinery & household appliances, non-metallic minerals, basic metals, food, chemicals, wood/paper/furniture, motor vehicles & transport equipment, apparel & leather, other manufacturing), each with the full 13-component PMI breakdown (headline + Output, New Orders, Suppliers' Delivery Times, input/raw-material inventories, Employment, Input Prices, stocks of finished goods, Exports, Output Prices, Energy Consumption, Quantity of Purchases, Business Expectations). Sourced from the ICCIMA Statistical Yearbook 1403's dedicated PMI chapter (chapter 3, tables 3-11 through 3-24) — a bilingual (Persian/English) publication with clean embedded digit text, extracted programmatically (see method below), not visually transcribed. 2,184 data points, effectively 14 parallel monthly time series for FY1403. |
| `pmi_monthly_series.csv` | Aban 1404-Ordibehesht 1405 (≈ Oct 2025-May 2026), 7 months | Whole-economy PMI only, but with **both seasonally-adjusted and not-seasonally-adjusted** cuts (the yearbook table above only gives non-adjusted), extracted from the 4 individual monthly PMI bulletin PDFs (`pmi-1404-09-period87.pdf` etc.), each of which republishes a 2-month "current + prior" comparison table — cross-validated where months overlap between consecutive bulletins (Farvardin 1405 appears identically in both the period91 and period92 reports: 26.3 non-adjusted / 38.5 seasonally-adjusted in both). **This file picks up almost exactly where the yearbook file's coverage ends** (Esfand 1403 = year-end March 2025 vs. this file starting Aban 1404 = Oct/Nov 2025), leaving a real ~7-month gap (Farvardin-Mehr 1404, April-Oct 2025) not covered by any downloaded report. |
| `business_environment_national_index.csv` | FY1398-1404 annual (7 points) + 3 quarterly points (Winter 1403, Fall 1404, Winter 1404) | ICCIMA's separate **National Business Environment Monitoring Index** (شاخص ملی پایش محیط کسب‌وکار ایران) — a *worse-is-higher* 1-10 survey-based obstacle index (10 = worst possible business climate), published quarterly since 1396 SH (2017/18) but only these 8 clean tabulated points were extracted (see Caveats). |

## Extraction method

The 4 individual monthly PMI bulletins (`pmi-1404-09-period87.pdf`, `pmi-1404-11-period89.pdf`,
`pmi-1405-01-period91.pdf`, `pmi-1405-02-period92.pdf`) are Persian-only, and `pdftotext`
mis-renders their tables (reversed/reshaped Arabic-presentation-form glyphs) — their headline
table (page 4 of each PDF, "Table 1: PMI of the whole economy in the two months ending X") was
read via `pdftoppm -png -r 250/300` page/region renders and cross-verified: the column order
(seasonally-adjusted current month, seasonally-adjusted prior month, non-adjusted current month,
non-adjusted prior month) was confirmed by re-rendering a high-resolution crop of just the header
row before transcribing all 13 rows x 4 reports.

The Statistical Yearbook 1403's PMI chapter (pages 124-137 of `statistical-yearbook-1403.pdf`)
turned out to have a genuinely clean, complete embedded text layer for its numeric table cells
(the Persian narrative text renders reversed/garbled like the bulletins, but the plain Latin-
digit numbers extract perfectly via `pdftotext -layout`) — confirmed by comparing a
`pdftotext`-derived set of values against an independent visual transcription of the same page,
which matched exactly to 2 decimal places. Built a small parser
(kept in this session's scratch area) that, per page: (1) locates the bilingual sector-table
title, (2) collects the 13 ordered English row labels (which vary slightly in wording between
the whole-economy table and the sector tables — e.g. "Input inventories" vs. "Raw Materials
Inventories" — preserved exactly as printed per table rather than force-normalized), (3) extracts
all `\d+\.\d+`-pattern numbers from the page (always exactly 13 x 12 = 156, one dense block with
no stray decimal numbers elsewhere on the page), and reshapes them in reading order. Applied to
all 14 tables (pages 124-137) with 100% clean extraction after two small regex fixes (a curly
left-quote character in "Suppliers' Delivery Times" initially broke the label filter; one page's
title line used a different bidi-marker nesting requiring a hardcoded fallback).

## Caveats — read before charting

- **A ~7-month gap exists between the two PMI files**: the yearbook covers through Esfand 1403
  (March 2025) and the bulletin-derived file starts at Aban 1404 (Oct/Nov 2025) — Farvardin
  through Mehr 1404 (April-October 2025) is not covered by any of the 6 downloaded PDFs. This is
  a genuine gap in what was downloaded, not a source gap (ICCIMA publishes monthly, every one of
  those months' bulletins almost certainly exists on iccima.ir) — flagged for a future download
  pass rather than filled with any assumption.
- **The yearbook's sectoral tables are not seasonally adjusted**; the bulletin-derived file has
  both cuts for the whole economy only. Do not compare a yearbook sector value against a
  bulletin seasonally-adjusted whole-economy value without noting this.
- **A striking data point, reported factually, not interpreted**: the bulletins show the
  whole-economy headline PMI collapsing to 22.0 (non-adjusted) / 24.9 (seasonally-adjusted) in
  Esfand 1404 (≈ Feb/March 2026) before rebounding to 26.3/38.5 in Farvardin 1405 — by far the
  lowest reading in either file (everything else sits in the 40s-50s range). The source PDF's own
  narrative attributes the Farvardin-1405 rebound context to "the war" and sharp exchange-rate/
  price volatility (اثر شوک جنگ, referenced in the period91 bulletin's own text) but this project
  makes no independent causal claim here — worth cross-referencing against `timeline/iran.csv`
  for a nearby event in a future pass, not done in this one.
- **`business_environment_national_index.csv` is a small, clean subset of a much richer source**:
  both the yearbook and the Winter-1404 monitoring report show a *quarterly* trend chart running
  continuously from 1396 (2017/18) through Winter 1404 (2025/26) — roughly 36 quarterly points —
  but only the chart's own printed reference-table values (8 points: 5 annual averages + 3 named
  quarters) were transcribed here; the remaining ~28 quarterly points exist only as data-labels on
  a compressed line chart in the source PDF and were not digit-read individually, to avoid
  transcription-error risk on small chart text. A future pass could attempt this with a
  higher-resolution crop per chart segment.
- **This index is worse-is-higher** (10 = worst-rated business environment component score) —
  do not chart it alongside PMI (where higher = expansion/better) without labeling the inverted
  scale.
- **The Winter-1404 monitoring report itself** (`business-environment-monitoring-winter-1404.pdf`,
  54 pages, Persian-only) contains much more granularity not extracted here — provincial index,
  index by economic-activity type, index by firm size/age/knowledge-based-company status,
  Schein-entrepreneurship-model breakdown — a real, logged incompleteness, flagged as a natural
  next-pass target given its narrative structure closely mirrors the yearbook chapter 3 tables
  already mined.
- **The ICCIMA Statistical Yearbook's other 3 chapters** (Chamber's own internal performance
  statistics; private-sector industrial/mining/agriculture workshop-level statistics by
  activity/province; Iran's international standing on Doing Business/competitiveness/HDI/gender-
  gap indices vs. other countries) were reviewed via table-of-contents but **not extracted** this
  pass — chapter 2 (private-sector workshop statistics) in particular looked genuinely valuable
  (industrial workshop counts/value-added/investment by province and activity) but was
  deprioritized given this task's specific PMI focus; flagged as a good candidate for a future
  ICCIMA-yearbook-specific harmonization pass.

## Sources

Iran Chamber of Commerce, Industries, Mines & Agriculture (ICCIMA), Statistics & Economic
Information Center (SEIC):
- `data/raw/iccima-iran/pmi-and-reports/statistical-yearbook-1403.pdf` (Statistical Yearbook 1403, chapter 3)
- `data/raw/iccima-iran/pmi-and-reports/pmi-1404-09-period87.pdf`, `pmi-1404-11-period89.pdf`, `pmi-1405-01-period91.pdf`, `pmi-1405-02-period92.pdf` (monthly PMI bulletins)
- `data/raw/iccima-iran/pmi-and-reports/business-environment-monitoring-winter-1404.pdf` (National Business Environment Monitoring report, round 38)

Full manifest: `data/raw/iccima-iran/pmi-and-reports/manifest.json`.
