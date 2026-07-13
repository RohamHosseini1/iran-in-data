# Pahlavi-era agriculture production/value, foreign trade & cost-of-living series (1950–1960)

Seven archival tables — already hand-extracted and visually verified (rendered to PNG via
`pdftoppm -r 200` and read directly off the page image, per this project's established method for
scanned World Bank reports) to `data/raw/pahlavi-era-primary-extraction/*/data.csv` — reshaped here
from each source's own wide (one column per year) layout into one uniform tidy long format.
**No value was recalculated, interpolated, unit-converted, or fabricated in this reshaping step** —
every cell is copied through exactly as it sits in the raw `data.csv`; the only transformations
applied are melting year/metric columns into rows and attaching a sortable `year` integer. Raw files
are untouched. Built by `scripts/harmonize/harmonize_pahlavi_agri_trade_oil_energy.py`.

## Schema (uniform across all 7 files, matches `pahlavi_government_finance_series/`'s convention)

`fiscal_year_label, year, category, subcategory, value, unit, notes, country_iso3, source_dataset`

- **`fiscal_year_label`** — the period exactly as the source printed it (e.g. `"1956/57"`,
  `"1950/51"`, `"Dec 1956"`, `"(fixed basket weight)"` for the one time-invariant metadata row type).
- **`year`** — a single sortable integer. Dual-year labels (`"1958/59"`) map to the LATER Western
  year (1959), matching this project's established convention. The cost-of-living index's basket-
  weight rows (time-invariant, not a yearly observation) get `year=""`.
- **`category`/`subcategory`** — preserves each source table's own row hierarchy (commodity name,
  metric type, etc.).
- **`value`** — blank means the source cell was blank, "n.a.", or a dash — never filled in.
- **`unit`**, **`notes`**, **`country_iso3`** (always `IRN`), **`source_dataset`** (the raw
  dataset_id, for tracing back to the manifest with full extraction/verification method).

## Files

| File | Coverage | Topic | Raw source dataset |
|---|---|---|---|
| `agricultural_production_1950_1958.csv` | 1950–1958 | Production quantity, 24 crops (citrus excluded — see below) | `wb1960-table5-agricultural-production` |
| `crop_land_production_value_1960.csv` | 1960 (single year) | Area harvested, production quantity, and gross value (Rls) by crop group | `wb1962-agriculturetable1-crop-land-production-value` |
| `livestock_production_value_1960.csv` | 1960 (single year) | Quantity and gross value (Rls) by livestock product | `wb1962-agriculturetable2-livestock-production-value` |
| `exports_by_commodity_1956_59.csv` | FY1956/57–1958/59 | Export value (US$m) and % share of total exports, 14 commodities (oil excluded) | `wb1960-table16-exports-by-commodities` |
| `imports_by_commodity_1956_59.csv` | FY1956/57–1958/59 | Import value (US$m) and % share of total imports, 19 commodities | `wb1960-table17-imports-by-commodities` |
| `ocean_trade_tonnage_1950_60.csv` | FY1950/51–1959/60 | Ocean-borne export/import/total tonnage, excl. petroleum products | `wb1962-transporttable7-ocean-trade` |
| `cost_of_living_index_1955_59.csv` | Dec 1955–Sept 1959 | Bank Melli 7-major-city cost-of-living index (Dec 1955=100), 5 categories + basket weights | `wb1960-table9-cost-of-living-index` |

## Citrus deliberately excluded from `agricultural_production_1950_1958.csv`

The raw source table's "Oranges & Tangerines" and "Other Citrus" rows are **not** reproduced here —
they were already bridged into FAOSTAT's 1961–2024 citrus series in
`data/processed/bridged_series/citrus_production_iran_1950_2024.csv` by an earlier round of this
project. Reproducing them here would create a duplicate, disconnected copy of that same series.
Every other commodity in the source table (24 of 26 rows) **is** included here, unlike the citrus
bridge.

## How this batch relates to `data/processed/CHART_REGISTRY.csv` — read before charting

`CHART_REGISTRY.csv` currently covers only the six machine-readable sources (WDI, FAOSTAT, IMF WEO,
OWID, Maddison, WID) — none of these Pahlavi-archival tables are folded in yet (that is a later
consolidation pass; this batch only stages the classification in
`data/processed/chart_registry_staging/agriculture_trade_oil_energy.csv`). Key findings from that
classification pass, useful context for anyone charting this folder:

- **Most commodities in `agricultural_production_1950_1958.csv` genuinely extend an existing
  FAOSTAT production chart_id** (e.g. `faostat__Wheat__production`, `faostat__Barley__production`)
  — this table's 1950–1958 span sits entirely before FAOSTAT's 1961 start, so splicing the two
  (1950–1958 WB + 1961–present FAOSTAT, exactly like the citrus bridge) is a natural follow-on task
  for whoever consolidates the registry, not performed in this file itself (per this project's rule
  that raw-shaped extraction and cross-source splicing are separate, explicitly-flagged steps).
  A few commodities (Almonds, Pistachios, Walnuts, Hazelnuts vs. FAOSTAT's "…, in shell" naming;
  Sugar vs. "Raw cane or beet sugar (centrifugal only)"; Tea vs. "Tea leaves"; Cotton vs. "Cotton
  lint, ginned") were matched by **judgment call, not an exact name match** — magnitude/trend
  cross-checked against each FAOSTAT series' 1961 starting value where the classification was
  genuinely ambiguous (see script comments and the staging file's `notes` column for the specific
  reasoning per commodity). Several commodities (Other Grains, Vegetables & Melons, Fresh Fruits
  non-citrus, Dried Apricots, Raisins, Other Dried Fruits, Animal Fats) have **no** matching FAOSTAT
  chart at any date — these are WB-specific aggregations/products FAOSTAT doesn't track for Iran at
  all, staged as `status=new`.
- **`cost_of_living_index_1955_59.csv` extends `wdi__FP.CPI`** (WDI's Iran CPI series starts exactly
  in 1960, the year immediately after this table ends) — but the two indices use **different base
  years and almost certainly different basket methodologies** (Bank Melli's Dec-1955=100, 7-major-
  city basket vs. WDI's global 2010=100 CPI construction). Present as two separate labeled segments
  on any chart, never rescaled/spliced into one continuous index number.
- **`exports_by_commodity_1956_59.csv` and `imports_by_commodity_1956_59.csv` are staged as `new`**,
  not extensions — FAOSTAT's own trade charts (`faostat__X__trade`) track export/import *quantity*,
  never *value*, so there is no existing value-by-commodity chart_id for these to extend, even for
  commodities FAOSTAT does cover (e.g. Rice, Wool, Cotton appear in both tables but measure a
  different thing). One commodity worth a manual cross-reference for a future pass: the "Carpets"
  export-value row here (1956/57–1958/59) sits chronologically right before
  `data/processed/specialty_goods_series/carpet_exports_1960_1988.csv` (1960 onward) — a real
  splice opportunity once specialty-goods series are themselves folded into the chart registry.
- **`crop_land_production_value_1960.csv` and `livestock_production_value_1960.csv` are staged as
  `new`** as whole tables (their unique, registry-uncovered contribution is the **gross value in
  Rials** dimension), even though their Area/Production sub-columns for matching commodities
  (Wheat, Barley, Rice, Cotton, Sugar beet, Tobacco, Tea, Pulses) would *also* individually extend
  the same 1960 gap as `agricultural_production_1950_1958.csv`'s commodities — not double-staged as
  separate extends rows to avoid registry clutter; noted here instead.
- **`ocean_trade_tonnage_1950_60.csv` is `new`** — no WDI logistics/trade-tonnage indicator reaches
  back this far for Iran (WDI's Logistics Performance Index only starts in 2007).

## Caveats — read before charting

- **`agricultural_production_1950_1958.csv`'s "Rice" row is explicitly labeled "(milled)" in the
  1950-58 WB source**, while FAOSTAT's "Rice" production item is a paddy/rough-rice-equivalent basis
  — the two are NOT directly comparable tonne-for-tonne (milled rice is typically ~65-70% of paddy
  weight). The apparent near-doubling from 1958 (320,000t milled) to FAOSTAT's 1961 value
  (600,000t paddy-equivalent) is very plausibly this unit-basis difference plus three years of real
  growth combined, not a data error — not reconciled here, flagged for whoever builds the eventual
  chart.
- **The "Dates" row shows an unexplained jump** from 125,000t (1958, this table) to FAOSTAT's
  300,000t (1961) — more than double in three years. Could be a genuine production surge, a
  definitional change, or a revision between sources; not investigated further here, per this
  project's rule to flag rather than silently smooth over discontinuities (same treatment as the
  citrus bridge's own honest gap).
- **`exports_by_commodity_1956_59.csv` and `imports_by_commodity_1956_59.csv`**: oil/petroleum is
  explicitly excluded from both tables (handled separately in `pahlavi_oil_energy_series/`); the
  source itself notes these customs-based figures are "not fully comparable" with the banking-
  statistics-based trade figures in `pahlavi_government_finance_series/`'s balance-of-payments
  tables — different methodology, don't force them onto the same line.
- **`cost_of_living_index_1955_59.csv`**: the Sept-1959 "Total" figure is printed in the source as
  "137 (provisional)" — the numeric value (137) is used in the `value` column with the provisional
  flag preserved in `notes`; all other Sept-1959 category-level cells were blank in the source
  (index not yet compiled by category at that date) and are left blank here, not back-filled from
  the Total.
- **Units**: production quantities in `agricultural_production_1950_1958.csv` and
  `crop_land_production_value_1960.csv` are in **1000 metric tons**; livestock quantities in
  `livestock_production_value_1960.csv` are in **tons unless the row's own unit says "number"**
  (i.e. a head/piece count, not a weight) — always check the `unit` column per row, never assume.
  Trade values are **US dollar millions** (customs-return basis); gross agricultural/livestock
  values are **Rls million**; do not mix currencies without an explicit FX-rate citation.

## Sources

- International Bank for Reconstruction and Development (World Bank), *Current Economic Position
  and Prospects of Iran* (1960) — Tables 5, 9, 16, 17.
- World Bank, *Economic Development Program of Iran, 1961-64 and Beyond* (1962) — Chapter 1
  (Agriculture) Tables 1–2, Chapter 4 (Transport and Communications) Table 7.

Full manifests and extraction methods:
`data/raw/pahlavi-era-primary-extraction/wb1960-agricultural-production-1950-1958/manifest.json`,
`.../wb1962-crop-land-production-value-1960/manifest.json`,
`.../wb1962-livestock-production-value-1960/manifest.json`,
`.../wb1960-exports-by-commodities-1956-1959/manifest.json`,
`.../wb1960-imports-by-commodities-1956-1959/manifest.json`,
`.../wb1962-ocean-trade-1950-1960/manifest.json`,
`.../wb1960-cost-of-living-index-1955-1959/manifest.json`.
