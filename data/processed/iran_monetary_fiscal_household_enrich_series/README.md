# Iran monetary / fiscal / household-consumption enrichment series

Harmonized 2026-07-14 by `scripts/harmonize/enrich_monetary_fiscal_household.py` from raw sources
that had been downloaded by earlier sessions but **never harmonized or registered** — this pass
found them via a systematic `data/raw` vs `CHART_REGISTRY.csv` gap audit before doing any new
hunting (per this project's "dig once" convention). Schema for every file:
`country_iso3, indicator_id, year, value, unit, source_dataset`.

## Files

### `money_supply_banking_national_accounts_imf_ifs_1937_1971.csv` (415 rows)

Money-supply/banking/national-accounts subset (22 of 54 metrics — trade/price-index/exchange-rate
metrics from the same source excluded as out-of-cluster) of
`data/raw/imf-ifs-historical/iran-annual-series-extracted/data.csv`, itself hand-transcribed by a
prior session from 15 IMF International Financial Statistics monthly-issue PDFs (1937-1971,
irregular annual coverage — see that folder's own manifest.json for the full transcription
methodology and cross-validation notes). Indicator IDs prefixed `imf_ifs_hist__`. Covers Iran's
earliest machine-readable M1/quasi-money/reserve-money/domestic-credit series in this database —
`imf_ifs_hist__money_supply_m1` has 21 annual points 1950-1971 (gap years: 1960, non-consecutive
per source availability, not a project omission). Also includes national-accounts aggregates
(`gross_domestic_product`, `gross_national_expenditure_gnp`, `national_income`,
`private_consumption_incl_stocks`, `government_consumption`, `gross_fixed_capital_formation`,
1961-1971) — `private_consumption_incl_stocks` is the earliest household-consumption-at-the-
national-accounts-level series in the project, directly relevant to this pass's household-
consumption mandate even though it is a top-line macro aggregate, not a household-budget-survey
line item.

### `government_debt_to_central_bank_quarterly_1978_2016.csv` (462 rows / 154 quarters x 3 metrics)

**The single biggest continuity win of this pass.** From
`data/raw/iran-data-portal/government-finance-tables/government_debt_to_central_bank_1978-2016_quarterly.xls`
(Iran Data Portal / Syracuse University, mirroring a Central Bank of Iran table; original filename
`Government-Debt-to-the-Central-Bank-1978-to-2016-Quarterly-1-1.xls`). Three metrics per quarter:
`iran_data_portal__govt_debt_to_cbi_total`, `..._excl_govt_corporations`, and
`iran_corporations_debt_to_cbi` (government-corporations-only sub-component), all in billion rials.
`year` field is a compound period string `<fiscal_year_ah><quarter_ah>_<year_western><quarter_western>`
(e.g. `1357Q1_1978Q2`) preserving both calendars exactly as the source table gives them — do not
assume `quarter_ah` and `quarter_western` are the same Q-number, they are offset (Iranian FY starts
~21 March). **This series directly bridges the 1971-2000 gap** between the IMF IFS historical money-
supply series (ends 1971) and the CBI Annual Review monetary-aggregates series
(`cbi_annual_review_series/monetary_banking_aggregates_1379_1401.csv`, starts FY1379=2000/01) — it
is not M1/M2 itself, but government debt to the central bank is a direct, standard proxy for the
government-financing channel of monetary-base creation, and is quarterly + essentially continuous
1978-2016 (154 of the possible ~156 quarters present), a genuinely rare thing for this era of Iran
data.

### `household_expenditure_detail_urban_rural_2001_2020.csv` (1088 rows)

Relabeled/retyped (schema-only change, no value changes) copy of
`data/raw/sci-amar/household-expenditure-detail-2001-2020/data.csv` (1089 source rows), itself a
prior-session extraction of Statistical Yearbook 1399 (2020/21) Chapter 21 (Household Expenditure
and Income) tables 21.1/21.2/21.3/21.10/21.11 — Statistical Centre of Iran's own Household
Expenditure & Income Survey (HEIS / آمارگیری هزینه و درآمد خانوار), urban and rural, SH1380/1385/
1390/1395-1399 (Gregorian 2001/2006/2011/2016-2020). **This file existed as raw data since
2026-07-13 but was never registered in `CHART_REGISTRY.csv` — confirmed via grep before this pass,
zero hits — so it was invisible to the chart catalog despite being real, sourced, extracted data.**
`indicator_id` is `sci_heis__<area>_<metric>` where `area` in {urban, rural} and `metric` covers
total net expenditure, food/non-food category breakdowns, and durable-goods/appliance and tea-
coffee-cocoa expenditure line items (see the underlying raw manifest for the full metric list).
Values are **nominal thousand rials per household per year** — heavily inflation-distorted across
2001-2020 and must be deflated (e.g. via `fx_cpi_lookup_irn.json`) before being read as a real-
consumption trend; not deflated in this pass, flagged for a future currency-variant pass same as
the raw file's own manifest already noted.

### `gdp_by_final_expenditure_component_1991_2005.csv` (42 rows)

From `data/raw/iran-data-portal/government-finance-tables/gdp_by_final_expenditure_components_1991-2005.xlsx`
(Iran Data Portal, mirroring an SCI/Plan & Budget Organization national-accounts table), SH1370/
1375/1380-1384 (Gregorian 1991/1996/2001-2005, irregular — matches exactly what the source table
itself publishes). Five components kept (of a longer original table; investment sub-breakdowns and
trade balance excluded as out-of-cluster): `iran_data_portal__gdp_expenditure_{private_final_
consumption_expenditure, household_final_consumption_expenditure, npish_final_consumption_
expenditure, government_final_consumption_expenditure, gross_fixed_capital_formation}`. Current-
price billion rials. `household_final_consumption_expenditure` is the direct national-accounts
counterpart to the HEIS household-budget-survey data above, for cross-validation (national-accounts
household consumption should track, at a much higher level of aggregation, the same broad trend as
the HEIS per-household averages scaled by household count — not cross-checked numerically in this
pass, flagged as a natural QA step for a future pass).

### `jhu_iae_haver_cbi_monetary_aggregates_quarterly_1998_2016.csv` (2059 rows / 29 indicators)

From `data/raw/jhu-iae-haver-iran-monetary/cbi-balance-sheet-quarterly-1998-2016/` — a fresh find this
pass, not a prior-session leftover. Johns Hopkins University Institute for Applied Economics (Steve H.
Hanke's institute) hosts a working file of Haver Analytics' Iran monetary database, every column
explicitly attributed to "Central Bank of the Islamic Republic of Iran". Retrieved via Wayback Machine
(direct fetch to the live URL returned HTTP 403). 29 quarterly metrics 1998-Q4 to 2016-Q2: monetary
base, currency in circulation, demand deposits, M1, quasi-money, M2, banking-system net foreign assets
(central-bank vs. banks split), banking-system claims on public/private sector (commercial vs.
specialized banks split), central-bank claims on government/public corporations, government/public-corp
deposits with the banking system, notes-and-coins issued vs. held at banks, banks' legal/demand
deposits at the central bank. **Cross-validated against `cbi_annual_review_series/` during this pass**:
2001-Q1 M2 = 249,110.7 billion rials here matches the existing FY1379 (2001) CBI Annual Review figure
exactly — real, not asserted, confirmation both are the same primary CBI data via independent routes.

### `heis_analysis_salehi_isfahani_2023_2025.csv` (12 rows)

From `data/raw/salehi-isfahani-heis-analysis/tyranny-of-numbers-blog-2024-2025/` — extends SCI HEIS
household-consumption coverage forward to SH1402-1403 (2023-2025) via Djavad Salehi-Isfahani's (Virginia
Tech economist) published analysis of SCI's own primary HEIS microdata, found because amar.org.ir
itself remains unreachable from this network. These are the AUTHOR's derived statistics (regional
real-per-capita-expenditure growth rates, a poverty rate against his own chosen poverty line — Iran has
no official one — and a Gini coefficient), not verbatim SCI-published figures; kept as a distinct
growth-rate/index chart rather than merged into the nominal-levels table above. Two figures spot-checked
directly against the raw saved HTML before transcribing.

## What this pass did NOT find (honest gaps, not silently skipped)

- **1972-1999 M1/M2 gap**: still open. The IMF IFS historical extraction ends 1971 (its source PDF
  archive tops out at `ifs_1974-03.pdf`, which turned out to be a special supplement with no Iran
  data — see that folder's manifest). CBI's own Annual Review series starts FY1379 (2000/01). CBI's
  own live time-series database (`tsd.cbi.ir`) — which per an in-repo download-log note "annual data
  available from 1959" — was NOT reachable this pass (see download log: connect-timeout, consistent
  with every other prior-session attempt at this exact host). The government-debt-to-CBI quarterly
  series above (1978-2016) is a genuine partial bridge for this window but is a financing-flow proxy,
  not M1/M2 itself.
- **HEIS/household-expenditure data for 2021-2025**: SCI's amar.org.ir itself remains geo-blocked from
  this network for both direct and Wayback-Machine routes (reconfirmed this pass — see download log).
  Partially closed via an indirect route: Djavad Salehi-Isfahani's published analysis of SCI's own HEIS
  microdata gives real-expenditure-growth/poverty/Gini figures for SH1402-1403 (2023-2025) — see
  `heis_analysis_salehi_isfahani_2023_2025.csv` above — but this is growth-rate/index data, not the
  same absolute-levels table as 2001-2020; the underlying microdata/absolute levels for 2021-2025 are
  still not directly in hand.
- **CBI Annual Review FY1402+ (2023/24 onward)**: not found this pass — the existing
  `cbi-annual-review-wayback` folder tops out at FY1401 (2022/23); no newer Wayback snapshot was
  located.
