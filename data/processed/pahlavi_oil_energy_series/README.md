# Pahlavi-era oil, gas & electric-power sector series (1910–1972)

Twelve archival tables — World Bank reports (1960/1962/1971/1974) and the US Bureau of Mines'
*The Petroleum Industry of Iran* (Information Circular 8203, 1963) — already hand-extracted and
visually verified (rendered to PNG via `pdftoppm -r 150`/`-r 200` and read directly off the page
image; the USBM source has no usable text layer at all, so it was read entirely from rendered
images) to `data/raw/pahlavi-era-primary-extraction/*/data.csv`, reshaped here into one uniform
tidy long format. **No value was recalculated, interpolated, unit-converted, or fabricated in this
reshaping step** — every cell is copied through exactly as it sits in the raw `data.csv`; the only
transformations applied are melting year/metric columns into rows and attaching a sortable `year`
integer. Raw files are untouched. Built by
`scripts/harmonize/harmonize_pahlavi_agri_trade_oil_energy.py` (same script, same schema, as the
companion `pahlavi_agriculture_trade_extensions/` folder).

## Schema (uniform across all 12 files)

`fiscal_year_label, year, category, subcategory, value, unit, notes, country_iso3, source_dataset`

- **`fiscal_year_label`** — the period exactly as printed in the source (`"1958/59"`, `"1963_64"`
  reformatted to `"1963/64"`, `"1910-32"` for a genuinely multi-year aggregate row, `"Sub-total
  (actuals)"` for a printed subtotal row).
- **`year`** — a single sortable integer. Dual-year labels map to the LATER Western year (matches
  this project's established convention). **Multi-year aggregate rows and printed subtotal/TOTAL
  rows get `year=""` (blank)** — e.g. `"1910-32"`, `"1952-54"`, `"1910-1951 TOTAL"`,
  `"Sub-total (actuals)"` — since they are not a single point in time and were never guessed or
  midpoint-averaged into one.
- **`category`/`subcategory`** — preserves each source table's own row hierarchy (recipient/company/
  product/fuel-type/prime-mover, etc.).
- **`value`** — blank means the source cell was blank, "n.a.", or a dash — never filled in. Rows
  that were entirely blank across every metric in the source (e.g. 1950 and 1952–54 in the oil-
  employment table, the 1951–54 nationalization-crisis data gap) are **omitted entirely** rather
  than written as empty rows, to keep the file's row count meaningful.
- **`unit`**, **`notes`**, **`country_iso3`** (always `IRN`), **`source_dataset`**.

## Files

| File | Coverage | Topic | Raw source dataset |
|---|---|---|---|
| `oil_revenues_by_allocation_1955_63.csv` | FY1955/56–1962/63 (1959/60–1962/63 are Plan-Organization estimates) | Oil revenue split across Budget / NIOC / Plan Organization / B.P.C. | `wb1960-table1-oil-revenues` |
| `oil_exports_revenues_by_company_1963_71.csv` | FY1963/64–1970/71 (last year preliminary estimate) | Export volume (crude/products) + revenue by paying company (Consortium/NIOC/Other) + average $/ton | `wb1971-table9-oil-exports-and-revenues` |
| `domestic_oil_consumption_by_product_1964_69.csv` | 1964–1969 | Domestic consumption by product: fuel oil, gas oil, kerosene, gasoline, other | `wb1971-table8.8-domestic-consumption-of-oil-products` |
| `petroleum_statistics_1956_58.csv` | 1956–1958 (calendar years) | Drilling activity, production, internal sales, exports, posted crude price | `wb1960-table2-petroleum-statistics` |
| `gas_production_consumption_1965_69.csv` | 1965–1969 | Natural gas production/consumption/flaring, Oil Operating Companies + NIOC | `wb1971-table8.9-production-and-consumption-of-gas` |
| `electric_power_generation_by_use_1968_72.csv` | 1968, 1970–1972 (selected years) | Electric power generation by end-use (industrial/agricultural/street-lighting/domestic/other), by regional company + national totals | `wb1974-table15.3-electric-power-generation-by-plant-and-use` |
| `power_generating_capacity_1970_71.csv` | 1970–1971 | Installed generating capacity by prime mover (diesel/steam/gas/hydro), by regional company + named dams | `wb1974-table15.2-power-generating-capacity` |
| `aioc_profits_uk_taxes_iran_royalties_1910_51.csv` | 1910–1951 | Anglo-Iranian Oil Company net profit, UK tax payments, Iran royalty payments (pre-nationalization era) | `usbm1963-aioc-profits-royalties-1910-1951` |
| `consortium_disbursements_1954_62.csv` | 1954–1962 | Post-nationalization Consortium payments: oil-agreement cash+in-kind, income tax, wages/salaries, social insurance, contractor payments + GNP/forex/govt-expenditure share ratios | `usbm1963-consortium-disbursements-1954-1962` |
| `oil_industry_employment_by_nationality_1939_60.csv` | 1939–1949, 1951, 1955–1960 (1950, 1952–54 not available) | Oil-sector employment split by Iranian / Non-Iranian / Not-specified | `usbm1963-oil-industry-employment-1939-1960` |
| `oil_industry_personnel_by_company_category_1955_61.csv` | 1955–1961 | Oil-sector personnel by employer (Consortium/NIOC/Others) × category (Labor/Iranian staff/Non-Iranian staff) | `usbm1963-oil-industry-personnel-by-category-1955-1961` |
| `oil_revenue_distribution_1957_59.csv` | 1957–1959 | Oil revenue % share to Plan Organization / Ministry of Finance / NIOC | `usbm1963-oil-revenue-distribution-1957-1959` |

## How this batch relates to `data/processed/CHART_REGISTRY.csv` — read before charting

`CHART_REGISTRY.csv` currently covers only the six machine-readable sources (WDI, FAOSTAT, IMF WEO,
OWID, Maddison, WID) — **none of them track oil revenue, oil-sector employment, natural gas, or
electric-power generation/capacity for Iran at any date**, so every file in this folder is staged
`status=new` in `data/processed/chart_registry_staging/agriculture_trade_oil_energy.csv`, with one
important exception/caveat:

- **`petroleum_statistics_1956_58.csv`'s "Production" row (physical volume, million m³, Consortium
  + NIOC) genuinely OVERLAPS in time and concept with the already-registered
  `owid__oil_production_volume` chart** — OWID's Iran oil-production series already runs
  continuously from 1900, so this is NOT a gap to extend, it's an alternate/cross-check source for
  years OWID already covers. Flagged in the row's own `notes` and in the staging file; per this
  project's reconciliation policy, keep both as separate labeled lines if ever charted together,
  never averaged or silently reconciled to one number.
- The rest of `petroleum_statistics_1956_58.csv` (drilling wells/meters, internal sales volume,
  export volume, posted crude price) has no OWID/WDI equivalent at all and is genuinely new.

## Relationships between these files — read before charting

**Four different oil-revenue "angles" exist across this batch and `pahlavi_government_finance_series/`,
spanning 1910–1971, from different classification systems that do NOT reconcile to one number and
were deliberately NOT spliced together:**
1. `aioc_profits_uk_taxes_iran_royalties_1910_51.csv` — pre-nationalization AIOC profit/tax/royalty,
   1910–1951 (company-side accounting, GBP).
2. `oil_revenues_by_allocation_1955_63.csv` — post-nationalization revenue split by RECIPIENT
   (Budget/NIOC/Plan Org/B.P.C.), 1955/56–1962/63 (USD).
3. `oil_exports_revenues_by_company_1963_71.csv` — revenue split by PAYING COMPANY
   (Consortium/NIOC/Other), 1963/64–1970/71 (USD).
4. `oil_revenue_distribution_1957_59.csv` — revenue split by recipient as a PERCENT SHARE (not
   absolute value), 1957–1959 — a third classification again, overlapping years with #2 but
   reporting shares rather than dollar amounts; the percentages here are broadly consistent with,
   but not arithmetically derived from, #2's dollar figures.
There is a genuine ~3-year data gap (1951–1954, the nationalization crisis) between #1 and #2/#4 —
the source narrative itself states foreign-sale income was "negligible" in this period; not filled
with any estimate.

**Employment/personnel has two granularities that should not be merged**:
`oil_industry_employment_by_nationality_1939_60.csv` (by nationality only, all companies combined)
vs. `oil_industry_personnel_by_company_category_1955_61.csv` (by employer AND labor-category, for
the overlapping 1955-1960 years). The two were cross-checked against each other at extraction time
(5 of 6 overlapping years' grand totals matched exactly; **1958 has a genuine 5-unit source-internal
discrepancy — 62,033 printed total vs. 62,028 from summing the three reported components —
preserved as-is, not silently reconciled**, per this project's no-fabrication rule).

**`consortium_disbursements_1954_62.csv`'s "Wages and salaries" rows are an aggregate annual wage
bill paid by the Consortium (GBP 15.6M in 1955 rising to GBP 28.3M in 1962), NOT a per-worker wage
rate.** A future harmonization pass could divide this by
`oil_industry_personnel_by_company_category_1955_61.csv`'s Consortium employment counts to derive
an implied average annual wage per Consortium worker — **deliberately not computed here** (mixing
two tables into a derived statistic belongs in an explicit, separately-flagged step, not silently in
a raw-shaped reshape).

**Domestic oil consumption (`domestic_oil_consumption_by_product_1964_69.csv`, product-level, 1964-
69) is a companion to `data/raw/pahlavi-era-primary-extraction/wb1962-gasoline-consumption-1955-1962/`
(gasoline only, million liters, 1955/56-1961/62)** — NOT harmonized into this batch (outside the
assigned raw-folder list for this round) — together the two give a near-continuous 1955-1969
gasoline-consumption picture across two different units; reconciliation left to a future pass.

## Caveats — read before charting

- **AIOC-era war-years royalty guarantees (1939-1943)**: the source's `notes` column, preserved
  verbatim in this file, records BOTH the guaranteed-minimum royalty actually paid AND the lower
  counterfactual figure that would have applied without the wartime guarantee — only the paid
  figure is in `value`; the counterfactual is text-only in `notes`, never a second numeric row.
- **`oil_revenues_by_allocation_1955_63.csv`**: rows tagged `[estimate]` (FY1959/60 onward) are
  Plan-Organization projections based on the Government's March-1959 statement to the Bank,
  assuming an 8%/year increase after 1959/60 — not actuals; filter or style distinctly before
  treating this series as "actuals only."
- **`oil_exports_revenues_by_company_1963_71.csv`**: the source itself notes export volumes are
  tabulated by calendar year while revenue figures are by Iranian fiscal year, both under the same
  year-column headers in the original — reproduced as-is (not split into two separate year bases).
- **`electric_power_generation_by_use_1968_72.csv`'s unit ("million kWh (GWh)") is INFERRED, not
  printed on the source page** — cross-checked plausible against Iran's independently-known ~7.2 TWh
  total generation c.1971 (the Grand Total row is 7,244, consistent with million-kWh units) — flagged
  explicitly in every row's `unit` text as inferred, never silently presented as certain. This file's
  "domestic" (residential) rows are this project's first direct sector-disaggregated measure of
  Iranian household electricity consumption — WDI's per-capita consumption series only starts 1990
  and is never sector-split.
- **Units differ table to table and are NOT interchangeable without conversion**: oil revenue in
  `oil_revenues_by_allocation_1955_63.csv`/`oil_exports_revenues_by_company_1963_71.csv` is **US
  dollars**; `aioc_profits_uk_taxes_iran_royalties_1910_51.csv`/`consortium_disbursements_1954_62.csv`
  are **GBP (pounds sterling)**; oil/gas physical volumes are **million cubic meters** (petroleum) or
  **million cubic meters** (gas) — always check the `unit` column per row before comparing across
  files.

## Sources

- International Bank for Reconstruction and Development (World Bank), *Current Economic Position
  and Prospects of Iran* (1960) — Tables 1, 2.
- World Bank, *Economic Development of Iran* (1971) — Petroleum Sector report, Table 9; Statistical
  Annex (Vol. VII, Report No. SA-23a, 1971) Tables 8.8, 8.9.
- World Bank (1974) — Statistical Appendix (Vol. 4), Tables 15.2, 15.3.
- US Bureau of Mines, *The Petroleum Industry of Iran*, Information Circular 8203 (1963) — Tables
  1, 2, 4, 5, and an unlabeled revenue-distribution table (p.19), sourced via
  mohammadmossadegh.com's hosted copy of the US Department of the Interior original.

Full manifests and extraction methods:
`data/raw/pahlavi-era-primary-extraction/wb1960-oil-revenues-1955-1963/manifest.json`,
`.../wb1971-oil-exports-and-revenues-1963-1971/manifest.json`,
`.../wb1971-domestic-oil-consumption-1964-1969/manifest.json`,
`.../wb1960-petroleum-statistics-1956-1958/manifest.json`,
`.../wb1971-gas-production-consumption-1965-1969/manifest.json`,
`.../wb1974-electric-power-generation-by-use-1968-1972/manifest.json`,
`.../wb1974-power-generating-capacity-1970-1971/manifest.json`,
`.../usbm1963-aioc-profits-royalties-1910-1951/manifest.json`,
`.../usbm1963-consortium-disbursements-1954-1962/manifest.json`,
`.../usbm1963-oil-industry-employment-1939-1960/manifest.json`,
`.../usbm1963-oil-industry-personnel-by-category-1955-1961/manifest.json`,
`.../usbm1963-oil-revenue-distribution-1957-1959/manifest.json`.
