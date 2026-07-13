# CBI Annual Review — monetary & banking aggregates, FY1379-1401 (2000/01-2022/23)

Harmonized 2026-07-13 from `data/raw/cbi-iran/cbi-annual-review-wayback/` (23 English-language
PDFs, immutable/unchanged) via `scripts/harmonize/harmonize_cbi_annual_review.py`. Unlike the
Pahlavi-era archival PDFs elsewhere in this project, these are **native-text PDFs, not scans** —
`pdftotext -layout` extracts them cleanly with no OCR/visual-render step needed. Every figure was
read directly from the "Money and Banking" chapter's own narrative sentences (e.g. "Liquidity grew
by 29.3 percent... and reached Rls. 249,110.7 billion") cross-checked against the chapter's own
recurring summary table, using **that fiscal year's own report** as the source for that year's
figure (never a later year's retrospective restatement — see the revision note below).

## Coverage

**All 23 fiscal years (FY1379-1401) have a Liquidity (M2) level and growth rate — full coverage of
the single most important banking-sector aggregate.** Monetary base growth rate is covered for
19/23 years; monetary base level (billion rials) for 5/23 years (the narrative sometimes states
only the growth rate, not the absolute level, in a form legible enough to transcribe with
confidence within this pass's time budget). CPI/inflation growth is covered for 6/23 years — this
was a secondary target for this pass (the primary mission was money supply/banking aggregates) and
was not pursued exhaustively; **every miss is a genuine "not captured this pass," not a search
failure that was silently given up on** (see each row's `notes` for exactly what was tried).

| Metric | Years covered |
|---|---|
| Liquidity (M2) level + growth | 23 / 23 |
| Monetary base growth rate | 19 / 23 |
| Monetary base level | 5 / 23 (1379, 1380, 1383, 1384, 1385) |
| CPI/inflation growth | 6 / 23 (1379, 1380, 1382, 1383, 1385, 1390) |

## File

`monetary_banking_aggregates_1379_1401.csv` — one row per fiscal year:
`fiscal_year_ah, fiscal_year_western_end, liquidity_m2_billion_rials, liquidity_m2_growth_pct,
monetary_base_billion_rials, monetary_base_growth_pct, cpi_inflation_growth_pct, notes,
country_iso3, source_file`

`fiscal_year_western_end` uses the same `fiscal_year_ah + 622` convention as this project's other
Iranian-fiscal-year series (`pahlavi_government_finance_series/`, `majlis_budget_law_series/`).

## A raw-filename mislabeling found (FY1396)

**`cbi_annual_review_1396_2016-17.pdf`'s Western-year filename suffix is wrong.** Its actual text
content is explicitly and repeatedly dated "March 2018" (e.g. "Broad money (M2) amounted to Rls.
15,299.8 trillion in March 2018, showing 22.1 percent growth compared with the previous year-end
(March 2017)"), meaning this file covers Iranian fiscal year 1396 = **2017/18**, not "2016-17" as
its filename claims. FY1395 (2016/17) is correctly already covered by the adjacent file
`cbi_annual_review_1395_2016-17.pdf`, whose own text is genuinely dated "in 2016/17" throughout —
so the two filenames' Western-year suffixes are effectively duplicated, with FY1396's being wrong.
This is almost certainly a copy/paste error from the download round that assembled this collection
(both files are legitimate distinct PDFs — the sha256 hashes differ and the two `Annual Review`
editions have genuinely distinct content — only the *filename's Western-year label* on
`cbi_annual_review_1396_2016-17.pdf` is incorrect). Per `docs/bookkeeping.md` ("raw data is
immutable"), the raw filename was NOT renamed; this is flagged here and in every relevant row's
`notes` in the processed CSV, and this project's own AH-solar-year field (`fiscal_year_ah=1396`) is
what should be trusted for this row, not the raw filename's Western-year suffix.

## Inter-report revisions (a real phenomenon, not a project error)

**The same fiscal year's year-end statistic is sometimes restated slightly differently in the
FOLLOWING year's annual review** (each report includes a short table of the prior several years for
context). For example, FY1383's own report states year-end Liquidity (M2) as 685,697.5 billion
rials; FY1384's report restates the same FY1383 year-end figure as 685,867.2 billion rials — a
small (~0.02%) but real difference, consistent with normal central-bank data-revision practice
(preliminary vs. later-revised figures). **This CSV always uses each fiscal year's OWN report as the
source for that year's row**, per this project's policy of never picking a winner between two
legitimate vintages of the same figure — a systematic cross-report reconciliation of every year's
figure against every later restatement was not attempted (would require re-reading all 23 files
pairwise) and is flagged as a possible future refinement, not performed here.

## Units

- FY1379-1393 (2000/01-2014/15): figures in the source are stated in **billion rials**, transcribed
  directly.
- FY1394-1401 (2015/16-2022/23): the source switched to stating the same aggregate in **trillion
  rials** — this CSV converts these (×1000) back to billion rials for unit consistency with the
  earlier years, and the conversion is noted in each affected row.

## Caveats — read before charting

- **Monetary base and Liquidity (M2) are different aggregates** (monetary base = currency issued +
  bank reserves at the central bank; M2/Liquidity = a much broader money-supply measure including
  bank deposits) — do not treat them as interchangeable or plot them on the same implied scale
  without labeling.
- **Iran experienced significant currency redenomination discourse but no completed redenomination
  during this period** — the multi-order-of-magnitude growth in nominal rial figures across FY1379
  (249 billion) to FY1401 (63.4 quadrillion, i.e. 63,376,800 billion) reflects genuine nominal money
  growth (compounded by very high inflation, especially post-2018 sanctions reimposition) plus one
  unit-of-account change in how CBI itself reports the same concept (billion→trillion rials), NOT a
  currency redenomination event.
- **CPI/inflation figures captured here use different underlying measures across years where noted**
  — FY1379's `notes` column specifically flags that the source states BOTH an average-annual CPI
  growth (12.6%) and a distinct point-to-point year-end figure (20.1%); only the average-annual
  figure was put in the `cpi_inflation_growth_pct` column. Always read a row's `notes` before citing
  its CPI figure.
- **This is a headline-aggregate extraction, not a full transcription of each report's dozens of
  data tables.** Each 80-100-page report contains far more detail (deposit composition, sectoral
  credit allocation, exchange rate tables, national accounts, balance of payments, government
  budget execution, price indices by category) that was not extracted in this pass — this CSV
  covers only the two or three headline monetary/banking aggregates the harmonization task asked
  for. A future pass could mine considerably more from this same, now-proven-tractable, source.

## Sources

Central Bank of the Islamic Republic of Iran (CBI), Economic Research and Policy Department,
*Annual Review* (English edition), fiscal years 1379-1401. Retrieved via the Wayback Machine (direct
access to cbi.ir is blocked by an F5/TSPD bot-challenge from this project's IP, consistent with
every other Iran-domestic .ir site tried in this project — see `docs/bookkeeping.md`). Full
per-file citation chain (Wayback timestamps, source page IDs, SHA256):
`data/raw/cbi-iran/cbi-annual-review-wayback/manifest.json`.
