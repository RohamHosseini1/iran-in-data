# Iran Trade & Oil-Export Enrichment — CBI Annual Review, FY1375-1401 (1996/97-2022/23)

Harmonized 2026-07-14 from `data/raw/cbi-iran/cbi-annual-review-wayback/` (23 English-language
CBI Annual Review PDFs, already held by the project, immutable/unchanged) via
`scripts/harmonize/harmonize_cbi_trade_oil.py`. These are native-text PDFs (confirmed by a prior
harmonization pass, `scripts/harmonize/harmonize_cbi_annual_review.py`); `pdftotext -layout`
extracts them cleanly, no OCR needed. This pass mined the **Balance of Payments** table and the
**Export of Crude Oil** table — different tables from the prior pass's money/banking aggregates —
so this is new content from an already-held source, not a re-extraction.

## What this adds to the project

The project already has oil revenue back to 1910 (`pahlavi_oil_energy_series/`) and Pahlavi-era
oil/trade tables (1950s-70s, `pahlavi_agriculture_trade_extensions/`). This closes the gap for the
**Islamic Republic era (1996/97-2022/23)** with a genuinely continuous, Iranian-primary annual
series — the CBI's own Balance of Payments table, which itself sources onward to Iran's Customs
Administration (IRICA) for goods trade and the Ministry of Petroleum for oil.

## Files

- **`cbi_balance_of_payments_trade_oil_1375_1401.csv`** (189 rows) — one row per
  `(fiscal_year, indicator_id)`. Indicators: `iran_bop_current_account_musd`,
  `iran_bop_trade_or_goods_balance_musd`, `iran_bop_exports_total_fob_musd`,
  `iran_bop_exports_oil_musd`, `iran_bop_exports_nonoil_musd`, `iran_bop_imports_total_fob_musd`,
  `iran_bop_imports_oil_gas_musd` (FY1388-1401 only), `iran_bop_imports_other_nonoil_musd`
  (FY1388-1401 only). All in million *current* US dollars, as printed in the source (no inflation
  or FX adjustment applied here — see `docs/bookkeeping.md`'s currency-conversion convention if a
  real/USD-toggle variant is built from this later).
- **`cbi_crude_oil_export_volume_1375_1380.csv`** (18 rows) — crude oil, oil products, and total
  export volume in thousand barrels/day, FY1375-1380 (1996/97-2001/02) only. Source: CBI Annual
  Review Table 14, sourced onward to the Ministry of Petroleum.
- **`cbi_crude_oil_export_geographic_share_1376_1380.csv`** (25 rows) — % share of crude oil
  export value by destination region (Europe, Japan, Asia/Far East ex-Japan, Africa, Other),
  FY1376-1380 (1997/98-2001/02) only. Source: CBI Annual Review Table 20.

## Coverage

| Indicator | Fiscal years covered | Calendar-year span (fy_ah+622 convention) |
|---|---|---|
| Current account, trade/goods balance, total exports, oil exports, non-oil exports, total imports | FY1375-1401 (27/27) | 1997-2023 |
| Imports split oil/non-oil | FY1388-1401 (14/27) | 2010-2023 |
| Crude oil export VOLUME (thousand b/d) | FY1375-1380 (6 years only) | 1997-2002 |
| Crude oil export geographic share (%) | FY1376-1380 (5 years only) | 1998-2002 |

**`year` = `fiscal_year_ah + 622`**, the same Western-calendar-year-the-fiscal-year-ends-in
convention used by `cbi_annual_review_series/monetary_banking_aggregates_1379_1401.csv` and
`pahlavi_government_finance_series/`. Because the Iranian fiscal year runs ~21 March-20 March,
most of a fiscal year's economic activity actually falls in the CALENDAR year *before* `year`
(e.g. `year=2001` = FY1379 = 21 Mar 2000-20 Mar 2001, mostly calendar 2000) — always account for
this ~1-year offset before comparing to a calendar-year source like WDI (see Cross-Validation
below, which does this correctly).

## A genuine, notable gap: oil export VOLUME stops being published after 2001/02

**CBI's own "Export of Crude Oil" table (thousand barrels/day) appears in only the two earliest
reports held (FY1379, FY1380) and was not found in any of the other 21 reports** — confirmed by
`grep -i "export of crude oil"` across all 23 plain-text extractions, zero hits in FY1381-1401.
Meanwhile, oil export **REVENUE** (via the Balance of Payments table) continues to be published
every single year through FY1401 without a gap. This is a real, structural feature of CBI's own
disclosure practice, not a project extraction failure: Iran's own central bank publishes what it
earned from oil exports every year, but stopped publishing how much oil (in barrels) it actually
shipped after 2001/02 — plausibly connected to the sanctions-era sensitivity of exact export
volumes (unconfirmed inference, not asserted as fact; stated here only as the visible pattern).
The project's OPEC ASB-derived `opec_asb_2025_series/iran_opec_crude_production_historical_1980_2024.csv`
gives sparse anchor-year PRODUCTION (not export) volumes for 1980/1990/2000/2010 as a partial
substitute — production and exports are different quantities (production minus domestic
refining/consumption ≈ exports, but that arithmetic was not attempted here to avoid a
project-computed pseudo-series standing in for a real one). **A genuine, currently-unfilled gap.**

## Format changes in the source — three eras, never spliced

- **Era A (FY1375-1386 / 1996/97-2007/08):** "Trade balance / Exports / Oil and gas [and oil
  products] / Others / Imports". No oil-vs-non-oil split on the IMPORT side in this era.
- **Era B (FY1387/2008-09 only, transitional):** the source itself changed presentation mid-stream
  to "Exports (FOB) / Oil and gas / Exports of goods in trade statistics / Adjustments" with no
  single "non-oil exports" line item that year. This CSV computes `iran_bop_exports_nonoil_musd`
  for FY1387 as `Exports(FOB) − Oil and gas` (=18,716), flagged in that row's `notes` — the ONLY
  computed (non-verbatim) figure in this dataset, clearly marked as such.
- **Era C (FY1388-1401 / 2009/10-2022/23):** clean "Exports (FOB) / Oil exports / Non-oil
  exports / Imports (FOB) / Gas and oil products / Other goods (non-oil imports)" split, present
  every year.

**A real mid-series methodology break, not a project error**: the source's own footnote states
"Balance of Payments data for 1997/98-2009/10 have been revised based on the fifth edition of the
IMF Balance of Payments Manual (BPM5)." FY1387's own report gives 2008/09 Oil-and-gas exports as
81,855 and total exports 100,571; FY1388's NEXT report retroactively restates the SAME year
(2008/09) as Oil exports 86,619 / Non-oil exports 14,670 / total 101,289 under BPM5 — genuinely
different numbers for the same year, not an error in either vintage. Per this project's
never-pick-a-winner convention (already established in `cbi_annual_review_series/README.md` for
the M2/monetary-base series), **this CSV always uses each fiscal year's OWN report** as that
year's row, so a future user comparing rows across this series is seeing each year's
contemporaneous vintage, not a silently blended composite.

## Inter-report revisions (confirmed present, same phenomenon as the monetary series)

Example: FY1379's own report states 2000/01 current account as $12,645mn; FY1380's report
restates the SAME year as $12,500mn. FY1384's own report states 2005/06 current account as
$14,037mn; FY1385's report restates it as $16,637mn. Both kept as each year's own contemporaneous
figure, per convention — see each row's `notes` for the specific alternate vintage found.

## Cross-validation against World Bank WDI (this project's existing `macro_wdi.csv`)

WDI's `TX.VAL.MRCH.CD.WT` (merchandise exports, calendar year) and `TM.VAL.MRCH.CD.WT`
(merchandise imports) for Iran, compared against this series with the ~1-year fiscal-to-calendar
offset applied (CBI `year` = fiscal-year-end; WDI calendar year ≈ CBI `year` − 1):

| CBI fiscal year (year field) | WDI calendar year | WDI exports ($bn) | CBI exports ($bn) | WDI imports ($bn) | CBI imports ($bn) |
|---|---|---|---|---|---|
| 2001 (FY1379) | 2000 | 28.74 | 28.35 | 13.90 | 15.21 |
| 2006 (FY1384) | 2005 | 56.25 | 60.01 | 40.04 | 40.97 |
| 2011 (FY1389) | 2010 | 101.32 | 108.61 | 65.40 | 68.45 |
| 2016 (FY1394) | 2015 | 70.28 | 64.60 | 44.94 | 52.42 |
| 2021 (FY1399) | 2020 | 46.92 | 49.85 | 38.76 | 46.61 |
| 2023 (FY1401) | 2022 | 97.85 | 97.66 | 58.78 | 75.41 |

**Broadly consistent (same order of magnitude, same trend, exports typically within 5-10%),
confirming both series are measuring approximately the same real-world flows** — expected, since
WDI's own merchandise-trade series is itself substantially built from IMF/national-central-bank
reporting that traces back to the same underlying customs data CBI cites. **Imports show a
persistently larger gap than exports, especially in the most recent years** (CBI $75.4bn vs. WDI
$58.8bn for the 2022/23 vs. 2022 comparison, a ~28% gap) — plausibly the calendar/fiscal-year
misalignment (a single volatile sanctions-era year straddling the boundary can shift the
comparison significantly), a coverage difference (CBI's imports figure may include categories WDI
excludes, e.g. certain government or military procurement), or genuine reporting-basis differences
between Iran's own central bank and the World Bank's harmonized aggregation. **Per this project's
policy on contested/diverging figures: both series are kept as separate, clearly labeled sources
— this divergence is not adjudicated or averaged here.**

## What was NOT extracted this pass (genuine scope decisions, not silent gaps)

- **Imports/exports by broad commodity group** — the source contains a detailed by-commodity
  breakdown every year (e.g. "VALUE OF EXPORTS (excluding oil, gas and electricity)" table,
  itself broken into carpets, fresh/dried fruits, agricultural goods, industrial goods, etc., and
  a parallel imports-by-commodity table sourced explicitly to "Iran's Customs Administration").
  Confirmed present in every report inspected but NOT transcribed across all 23 years this pass —
  a genuinely tractable future extension of this same source, not attempted here due to time
  budget (each year's commodity table has 20-40 line items; a full 23-year transcription is a
  substantially larger task than the headline BOP series done here).
- **Trade by partner country** — the only multi-year series found (`Table 20`, geographic %
  share of crude oil exports) covers just 5 years (1997/98-2001/02) before CBI stopped publishing
  it, included here as a bonus dataset but explicitly NOT proposed as a standalone chart per the
  owner's rule that a chart must be a measure over time, not a short fragment.
- **IRICA (Iran Customs Administration, irica.ir) direct access**: unreachable from this
  environment (connection failure, both https and http). A Wayback Machine CDX search surfaced
  ~30 archived PDFs under opaque CMS-generated filenames with no evident "foreign trade
  statistics yearbook" page found within this pass's time budget — flagged as an unexplored lead
  for a future pass, not a confirmed dead end. See `logs/downloads/iran-trade-oil.log` for the
  full attempt trail.
- **SCI (amar.org.ir) Statistical Yearbook foreign-trade chapter**: not attempted this pass
  (amar.org.ir also failed to connect on a preliminary check); time budget went to the
  already-tractable CBI PDFs instead.
- **cbi.ir direct access**: confirmed still blocked (F5/TSPD bot-challenge "Request Rejected"
  page), consistent with every prior finding in `docs/bookkeeping.md` for this domain.

## Sources

Central Bank of the Islamic Republic of Iran (CBI), Economic Research and Policy Department,
*Annual Review* (English edition), fiscal years 1379-1401, "Balance of Payments" and "Export of
Crude Oil" / "Geographical Distribution of Crude Oil Exports" tables. Per the tables' own source
lines: goods-trade figures sourced onward to Iran's Customs Administration (IRICA) and the
Ministry of Petroleum for oil-sector figures. Retrieved via the Wayback Machine (direct cbi.ir
access blocked — see above). Full per-file citation chain (Wayback timestamps, source page IDs,
SHA256): `data/raw/cbi-iran/cbi-annual-review-wayback/manifest.json` (already existed; no new
raw download this pass).
