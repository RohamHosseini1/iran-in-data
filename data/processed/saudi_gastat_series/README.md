# Saudi Arabia — GASTAT National Accounts & CPI

Extracted 2026-07-13 from `data/raw/gastat-saudi/{national-accounts,cpi-series}/` (immutable,
unchanged) — Saudi Arabia's General Authority for Statistics (GASTAT), the kingdom's official
statistics authority.

## `gastat_national_accounts_2018_2024.csv` (1,116 rows)

Source: `Annual_National_Accounts_Publication_2024_EN.xlsx` — a 27-sheet workbook already
provided alongside the PDF in the raw folder; used directly (far more reliable than PDF
extraction — no OCR/text-parsing needed). Four of the 27 tables were selected for breadth:

| Table | Title | Rows |
|---|---|---|
| 1 | GDP by Main Economic Activity at Current Prices (ISIC-coded sector detail) | 749 |
| 5 | Gross Fixed Capital Formation by Type of Capital Asset | 210 |
| 6 | Gross National Income (factor-income decomposition) | 56 |
| 8 | National Accounts Aggregates (GDP → GNI → National Income → Disposable Income → Saving, the single headline summary table) | 91 |
| 12 | Various Economic Indicators (tourism GVA/GDP contribution, household saving rate, SME contribution to GDP, trade-to-GDP ratio — single-year 2024 snapshot) | 10 |

Columns: `country_iso3, source_table, table_title, code, indicator, unit, year, value`. All
values in SAR (Saudi Riyal) million except Table 12 (mixed % and SAR million, noted per row).
Years covered: 2018-2024 (2024 marked "preliminary" in the source). The other 22 sheets in this
workbook (detailed sub-account tables, quarterly total-economy accounts for each year 2018-2024,
SNA matrix sub-accounts, the goods-and-services account) were left unextracted — available for a
future deeper pass.

**Verification**: GDP, 2024 = SAR 4,703,029 million; matches GASTAT's own published 2024
preliminary GDP figure.

## `gastat_cpi_series.csv` (68 rows)

Two short GASTAT CPI bulletins, both single-page infographic-style releases (chart-heavy, one
real data table each):

- `Annual_Average_CPI_2025-EN.pdf` — Table 1: annual-average CPI index level (2025 vs. 2024) and
  % change, for the general index and all 13 COICOP-style sections. Text-extracted via
  `pdftotext -layout` and independently cross-checked against a 200dpi PNG render of the actual
  table — exact match on every cell.
- `CPI_May_2026-EN.pdf` — two line/bar charts read as data: Figure 1 (year-over-year % change in
  the general CPI, monthly, May 2025 - May 2026 — 13 points) and Figure 2 (year-over-year %
  change by division for May 2026 specifically — 13 divisions). Because chart-label data carries
  real misread risk, both were verified against a 300dpi PNG crop of the chart region (zoomed in
  on the exact pixel area) before transcription, not read from `pdftotext` text order alone.

Columns: `country_iso3, series_type, section, period, metric, value, base_period`. A companion
monthly month-over-month chart (Figure 4 in the May 2026 bulletin) was deliberately **not**
extracted — 17 densely-packed near-zero data points with real transcription risk, and the
year-over-year series above is the more standard headline comparator metric already captured.

**Verification**: General Index annual-average % change, 2025 = 2.0% (matches the bulletin's own
headline sentence, "Annual average inflation... increases by 2.0% in 2025").
