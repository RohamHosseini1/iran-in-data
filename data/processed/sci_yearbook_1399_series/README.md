# SCI Iran Statistical Yearbook 1399 (2020/21) — remaining chapters (2026-07-13)

Extracted from the 5 previously-unmined chapter PDFs in `data/raw/sci-amar/sci-cpi-yearbook/`
(all immutable, unchanged). The 6th PDF in that folder,
`sci_yearbook_1399_ch21_household-expenditure-income.pdf`, was already extracted in a prior
session into `data/raw/sci-amar/household-expenditure-detail-2001-2020/data.csv` (1,088 rows) —
verified present, not redone. `sci_yearbook_1399_ch00_preliminary-pages.pdf` is the yearbook's
preface, table of contents and table-of-tables list only (no data tables of its own) — used here
to identify table numbers/pages in the other chapters, not extracted as its own dataset.

All 5 source PDFs are born-digital text (Microsoft Word 2016 exports, not scans) — `pdftotext
-layout` is fully reliable here, unlike the scanned Pahlavi-era archival PDFs elsewhere in this
project. One anomalous cell was visually cross-checked against a `pdftoppm -r 200` page render
per `docs/bookkeeping.md`'s method anyway (see Caveats) and confirmed to match the text layer
exactly — no OCR was needed for this source.

Each chapter has many more tables than were extracted here (see Table of Contents notes in
`data/raw/sci-amar/sci-cpi-yearbook/sci_yearbook_1399_ch00_preliminary-pages.pdf`) — this pass
extracted the flagship, genuinely time-series, chart-ready table(s) per chapter, following the
same scoping precedent set by the ch21 extraction (5 of 18 tables). Remaining tables (regional/
provincial cross-sections for a single year, government-employee headcounts by law/education,
producer price indices, export/import price indices, balance of payments, production accounts,
etc.) are a scoped future addition from the same already-downloaded PDFs.

## Files

| File | Source table | Coverage | What it covers |
|---|---|---|---|
| `labor_force_indicators_1380_1399.csv` | Ch.4 Manpower, Table 4.2 | 1380, 1385, 1390, 1395–1399 SH (~2001–2020), by national/urban/rural × sex | Economic participation rate, unemployment rate, youth unemployment (15–24 and 15–29), underemployment share, and employment share by agriculture/manufacturing/services |
| `government_budget_summary_1385_1400.csv` | Ch.20 Government Budget, Table 20.1 | 1385, 1390, 1395–1400 SH (~2006–2021) | Full total-country-budget resources/uses breakdown (general budget vs. public corporations/banks/for-profit institutions, current expenditure vs. non-financial/financial asset acquisition), billion rials |
| `cpi_by_group_1390_1399.csv` | Ch.22 Price Indices, Table 22.2 | 1390, 1395–1399 SH (~2011, 2016–2020), 1395=100 base | Consumer price index by ~35 major/minor/special groups including the durable/semi-durable/non-durable goods split and "Household furnishings and appliances" — the appliance/durable-goods CPI angle this project specifically tracks |
| `gdp_value_added_by_sector_1390_1397.csv` | Ch.23 National Accounts, Table 23.1 | 1390, 1393–1397 SH (~2011, 2014–2018), current AND constant-1390 prices | Value added by 18 economic-activity sectors + GDP/GNP/national-income aggregation, billion rials |
| `gdp_by_expenditure_1390_1397.csv` | Ch.23 National Accounts, Table 23.6 | 1390, 1393–1397 SH (~2011, 2014–2018), current AND constant-1390 prices | GDP by final expenditure component (consumption, GFCF by machinery/construction/public/private, net exports, stock changes) + same GDP/GNP/national-income aggregation |

`gregorian_year_approx` = Iranian solar year + 621 (start-year approximation; Iranian year begins
in March, so it spans two Gregorian years — this column is a convenience join key, the
authoritative year is `solar_year`).

## Caveats — read before charting

- **`labor_force_indicators_1380_1399.csv`: one value visually verified against the source
  image.** National/Male/1399 "share of under-employment" is printed exactly as `4.10` in the
  source table (breaks the pattern of neighboring values, which run 7–12) — rendered PDF p.8
  (printed p.182) at `pdftoppm -r 200` and read directly to confirm this is genuinely what SCI
  printed, not a `pdftotext` misparse. Preserved exactly as printed; flagged as a possible SCI
  publication typo, not resolved or guessed.
- **`labor_force_indicators_1380_1399.csv`: methodology break at 1398/1399** — the source's own
  footnote states these two years cover population aged 15-and-over vs. aged-10-and-over for all
  earlier years; 1380 relates specifically to the month of Aban (pre-dates the annual Labour
  Force Survey adopted from 1384). Both breaks are preserved in the `notes` column per row, not
  silently smoothed over.
- **`government_budget_summary_1385_1400.csv`: 1400 is an approved/projected budget, not an
  actual outturn** — the chapter's own "Selected information" text describes 1400 figures as
  what "were projected to form," unlike 1385–1399 which are realized. Flagged per-row in `notes`.
  This complements (does not duplicate) the more granular `majlis_budget_law_series/` and
  `pahlavi_government_finance_series/` — this table gives the single clean total-budget
  time series in one place across the fiscal-1385–1400 span.
- **Genuine cross-table disagreement within the SAME source PDF, preserved not resolved**:
  Table 23.1 (value added by sector) and Table 23.6 (GDP by expenditure) report DIFFERENT
  current-price "consumption of fixed capital" and (therefore) "national income" figures for
  1393 and 1394 specifically (e.g. 1393: 1,823,026 in Table 23.1 vs. 1,931,385 in Table 23.6,
  bln rials) — all other years and the constant-price columns agree exactly between the two
  tables. Both values are kept, each in its own file, flagged in `notes` on the affected rows.
  Per this project's overlapping-disagreeing-sources rule, no winner was picked.
- **Years 1393–1396 in both GDP tables are marked "(1) Revised figures"** in the source; 1390
  and 1397 are not — preserved in `notes`, not stripped.
- **`cpi_by_group_1390_1399.csv`: several special-group breakdowns (Durable/Non-durable/
  Semi-durable goods; Fresh/Other foods; Public goods and services) have no 1390 figure** — the
  source prints "–" for these cells (these special-group splits were introduced after the 1395
  rebasing), left blank here, not fabricated or back-filled.
- **Nominal rial figures throughout** (budget, GDP, and implicitly CPI weights) are NOT
  inflation-adjusted — Iran's 1390–1399 period includes severe currency depreciation and high
  inflation (`cpi_by_group_1390_1399.csv`'s own General index shows nominal prices roughly
  6x higher in 1399 than 1395). Do not chart nominal GDP/budget levels as if they were real
  growth without deflating first; `cpi_by_group_1390_1399.csv` provides the deflator series
  needed for exactly this purpose, same caveat pattern as `pahlavi_household_consumption_series/`.
- **Table 20.1's `budget_line` values include both parent totals and their sub-components**
  (e.g. "Total budget resources" already includes "Government general budget resources" +
  "Resources of public corporations, banks..." beneath it) — do not sum all rows for a given
  year, that would double-count. Treat each row as its own labeled series; the hierarchy is
  encoded only in the label text, matching how it's printed in the source table.

## Sources

Statistical Centre of Iran (SCI), *Iran Statistical Yearbook 1399* (2020/21), English edition,
Chapters 4 (Manpower), 20 (Government Budget), 22 (Price Indices), 23 (National Accounts) —
`data/raw/sci-amar/sci-cpi-yearbook/sci_yearbook_1399_ch{4,20,22,23}.pdf`, retrieved via Wayback
Machine (amar.org.ir direct access blocked, see that folder's `manifest.json`).

Extraction method: `pdftotext -layout` (clean, born-digital PDF text layer; no OCR needed) with
one anomalous-value spot-check via `pdftoppm -png -r 200` page render + visual read, per
`docs/bookkeeping.md`.
