# Iran Prices & Inflation — deep series (2026-07-14 pass)

Mission: deepen the project's Iran CPI/WPI/PPI/urban-rural CPI layer from Iranian
primary sources, extending/corroborating (never replacing) the existing
`data/processed/iran_data_portal_deep_series/inflation_rate_1937_2014.csv` and
`data/processed/sci_yearbook_1399_series/cpi_by_group_1390_1399.csv`.

## Files

| File | Measure | Coverage | Source |
|---|---|---|---|
| `cbi_cpi_urban_general_and_groups_1996_2023.csv` | Consumer Price Index, Urban Areas, general index + Goods/Services special groups + ~12 major groups | SH1375-1401 (1996/97-2022/23), 27 continuous fiscal years across 6 base-year vintages | CBI Annual Review (6 editions: 1379, 1384, 1389, 1394, 1399, 1401) |
| `cbi_ppi_general_and_special_groups_1996_2023.csv` | Producer Price Index, general + Agriculture/Manufacturing/Services sectors | SH1375-1401 (1996/97-2022/23), same 27 years | CBI Annual Review (same 6 editions) |
| `cbi_wpi_general_and_special_groups_1996_2008.csv` | Wholesale Price Index, general + Domestic/Imported/Exported goods-flow groups | SH1375-1386 (1996/97-2007/08), 12 fiscal years — CBI discontinued this table after 1386 | CBI Annual Review (1379, 1384, 1386 editions) |
| `sci_cpi_urban_vs_rural_general_index_1385_1399.csv` | CPI general index, Urban vs Rural households | SH1385, 1390, 1395-1399 (7 points, not fully annual) | SCI Iran Statistical Yearbook 1399, Ch.22, Tables 22.4 & 22.7 |
| `sci_cpi_national_monthly_snapshots_2022_2025.csv` | CPI index level / MoM / YoY point-to-point / 12-month rolling inflation, national + urban + rural | 5 non-contiguous months, Mar 2022 - Feb 2025 | SCI monthly press releases, via Wayback Machine |

## Method

All CBI figures were transcribed by hand from `pdftotext -layout` output of the 23
CBI Annual Review PDFs already on disk at `data/raw/cbi-iran/cbi-annual-review-wayback/`
(native PDF text, no OCR needed — verified clean extraction on every file used). Each
Annual Review edition carries a 5-year rolling statistical-appendix table; a
non-overlapping "ladder" of 6 editions was selected so SH1375-1401 (1996/97-2022/23)
is covered with **zero gaps**, using only the small amount of edition-to-edition
overlap needed to cross-check transcription accuracy (e.g. the 1384 and 1386 editions'
WPI figures for 2003/04-2005/06 match to the decimal).

**Base-year discipline**: CBI rebased these indices five times across the period
covered (1997/98=100, then rebased again at unknown intermediate points, landing on
2004/05=100 by the 1389 edition, 2011/12=100 by 1394, 2016/17=100 by 1399, and
2021/22=100 by 1401). Per this project's standing convention, values are **never
rescaled or spliced across a base-year boundary** — each row carries its own
`base_year_sh` column, and `pct_change_yoy` is computed only from adjacent values
*within* the same vintage/base-year segment (marked `computed` in `pct_change_source`
vs. the handful of values the source table states directly).

## Cross-validation

- **Against the existing `inflation_rate_1937_2014.csv` (Iran Data Portal /
  CBI)**: computed YoY figures for SH1391-1393 (30.5%, 34.8%, 15.5%) match that
  file's values (30.5%, 34.7%, 15.6%) almost exactly — strong corroboration between
  two independently-obtained, both CBI-attributed series.
- **One genuine discrepancy, reported honestly, not adjudicated**: CBI's own 1384
  Annual Review states SH1384 (2005/06) inflation as **12.1%** — both printed directly
  in the table's "percentage change" column and reproducible from its own adjacent
  index values (307.6 / 274.5). The existing `inflation_rate_1937_2014.csv` gives
  **10.4%** for the same year. Both are nominally CBI-sourced; kept as two
  disagreeing values in two separate files per project policy (never silently
  reconcile contested official figures).
- **Against WDI**: `wdi__FP.CPI` / `FP.CPI.TOTL` for Iran runs continuously
  1960-2025 (rescaled to 2010=100) and broadly tracks this file's segments.
  `wdi__FP.WPI` / `FP.WPI.TOTL` for Iran runs **exactly** 1960-2007 — stopping in
  the identical year this project's CBI-sourced WPI table was discontinued, which is
  near-certain confirmation that WDI's Iran WPI figure is itself sourced from this
  same CBI table lineage rather than an independent World Bank construction.
- **PPI has no WDI counterpart for Iran** (WDI's Price Indices category only has
  CPI and WPI/wholesale codes) — the CBI PPI series here is a genuinely new measure
  for this project, not a corroboration of anything already present.

## Honest gaps

- **WPI ends at SH1386 (2007/08)** because CBI itself stopped publishing this
  specific goods-flow-classified table after that edition (confirmed: the 1387
  edition's table-of-contents lists only CPI and PPI, no WPI). PPI (sectoral
  classification) continued and is fully covered through SH1401.
- **Post-1401 (2023 onward) coverage is thin.** amar.org.ir (Statistical Centre of
  Iran's own domain) is unreachable from this sandbox on every method tried — direct
  `curl` returns no HTTP response at all, and the `WebFetch` tool returns
  `ECONNRESET` / "Socket is closed" on every URL, including the plain homepage.
  `cbi.ir/Inflation/Inflation_en.aspx` (CBI's live inflation dashboard) is reachable
  but sits behind an Incapsula JS bot-challenge — even its own most recent Wayback
  snapshot (2026-05-30) only captured the challenge page, not real data. Worked
  around by querying the Wayback Machine's CDX API for archived amar.org.ir monthly
  CPI press-release pages, which yielded 5 real, dated, primary-sourced snapshots
  spanning Mar 2022 - Feb 2025 (`sci_cpi_national_monthly_snapshots_2022_2025.csv`)
  — genuinely useful bridge data, but sparse monthly points, not a continuous or
  annual-average series. A future agent with different network access (a live
  browser session, a proxy, or simply a fresh Wayback crawl closer to the present)
  could very likely fill 1402-1405 (2023-2026) properly using the same CDX-search
  method (see `data/raw/sci-amar/cpi-monthly-pointintime-wayback/manifest.json` for
  the exact query and every URL attempted, including failures).
- **Pre-1996 CPI index LEVELS (as opposed to the existing 1937-2014 inflation
  RATE series) were not pursued this pass** — recovering actual index values back to
  the 1930s-50s (Bank Melli era, base year 1315 SH / 1936-37 per the SCI yearbook's
  own institutional history, transcribed in the yearbook PDF's introduction) would
  require locating and mining actual Bank Melli bulletins or CBI's earliest Annual
  Reviews (pre-1996, i.e. before the oldest edition already on disk), which this
  project does not currently have downloaded. Flagged as a genuine, high-value
  target for a future source-hunting pass — the task brief's own framing ("a CPI
  series reaching back to the 1930s-50s is far more valuable than another recent
  one") is not yet satisfied at the index-level, only at the inflation-rate level
  (via the pre-existing 1937-2014 file).
- **Rural CPI is sparse (7 points) and CBI-side has none at all** — SCI is the only
  compiler of a rural CPI in Iran; CBI's own Annual Reviews were confirmed (full-text
  search, all 23 editions) to carry an Urban CPI only.
