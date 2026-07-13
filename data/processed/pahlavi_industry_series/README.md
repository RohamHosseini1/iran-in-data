# Pahlavi-era industry & transport series (1954–1972)

Harmonized 2026-07-13 from eight raw World Bank Archives extraction folders under
`data/raw/pahlavi-era-primary-extraction/` (all immutable, unchanged) into one combined
folder, mirroring the `specialty_goods_series/` pattern. Seven of the eight files re-copy
already-transcribed raw `data.csv` tables through Python's `csv` module (normalizing quoting
only); one file (`industrial_production_1954_1959.csv`) is reshaped from the raw source's
wide commodity-by-year layout into a long (tidy) format for easier charting — no numeric
values were altered in that reshape, only the table's row/column orientation.

All raw source PDFs live in `data/raw/world-bank-archives-iran/historical-documents/`.

## Files

| File | Coverage | What it covers |
|---|---|---|
| `industrial_production_1954_1959.csv` | 1954/55–1958/59 | Annual output of 13 light-manufacturing commodities: tea, sugar, cement, cotton/woolen/jute/silk cloth, cigarettes, matches, soap, rubber shoes, glass, soft drinks. Reshaped from the source's wide table (commodity × 5 year-columns) into long format (`commodity, fiscal_year, unit, value`) — one row per commodity-year observation. |
| `industry_import_dependence_1970.csv` | circa 1969–1970 (single cross-sectional survey) | Share of imported inputs in sales value, by product, across 5 categories (light consumer goods, durable consumer goods, transport equipment, intermediate products, capital goods) — 33 products from sugar (2% import-dependent) to electric switchgear (80%). A genuinely rare pre-revolution import-substitution progress snapshot. |
| `isfahan_steel_idro_capital_goods_1972.csv` | 1972 report, describing construction staged through the late 1970s | Qualitative/narrative extraction (no time series) covering: Isfahan Steel Mill (Aryamehr/NISC) site selection, USSR barter financing, 3-stage capacity plan (750,000t by mid-1972 → 2–2.5M by 1975 → 4–5M by late 1970s), construction status; IDRO's 4 capital-goods plants (Arak aluminum/Reynolds, Arak heavy engineering/USSR, Tabriz machine tools/Czechoslovakia, Tabriz agricultural equipment/Romania); textile and automotive price-competitiveness context (mass-consumption textiles 25-40% above US import prices; Paykan only ~15% above an international competitive-tender price). |
| `gasoline_consumption_1955_1962.csv` | 1955/56–1961/62 | National gasoline consumption, million liters — a clean 7-year annual series (last 2 years flagged "tentative" in the source). |
| `railways_freight_passenger_traffic_1953_1961.csv` | 1953/54–1960/61 | Iranian State Railways freight (1000 tons, million ton-km) and passenger traffic (millions of passengers, million passenger-km) — shows a sharp passenger-traffic jump starting 1957/58 (2.69M passengers, up from 1.73M the prior year, more than doubling again by 1959/60). |
| `railways_income_expense_1953_1961.csv` | 1953/54–1960/61 | Iranian State Railways gross revenues, working expenses, and balance before depreciation (million rials) — the operating-balance margin compresses steadily across the period (from ~35% of revenue in 1953/54 to ~26% in 1960/61) as expenses grow faster than revenue. |
| `road_vehicle_registration_1955_56_vs_1960_61.csv` | 1955/56 vs. 1960/61 (two-point comparison) | Vehicle registrations by type (automobiles, buses, trucks, motorcycles) at both dates plus the source's own computed increase and percent-increase columns — motorcycles grew fastest (+240%), automobiles' share of the fleet rose from 53% to 63%. |
| `vehicle_registration_gasoline_1962_1972.csv` | 1962–1972 (continuous annual series) | Long-format (`year, metric, value, unit, note`) series: cars/buses/trucks registered (each split private vs. government where available), all-vehicles total, and gasoline consumption (million barrels) — bridges directly from `road_vehicle_registration_1955_56_vs_1960_61.csv`'s 1960/61 endpoint (148,375 all vehicles registered) to this file's 1962 starting point (149,900 all vehicles), a consistent join. Several truck figures are explicitly flagged in the source as "mission estimate (e)" since a private/government breakdown wasn't given — preserved as printed. |

## Note on the brief's folder-name reference

The task brief that commissioned this harmonization pass referenced a raw folder
"wb1971-vehicle-registration-gasoline-1962-1972". The actual folder in this archive is
`wb1974-vehicle-registration-gasoline-1962-1972` — its underlying World Bank source document
is the *1974* statistical appendix (Table 14.7), not a 1971 document; same content the brief
was pointing at, just a dating correction (the report is from 1974 even though its data
series runs 1962-1972).

## Schema note

Each file keeps its source table's natural shape except `industrial_production_1954_1959.csv`,
which was melted from wide to long specifically because it is a genuine multi-year time series
better suited to that format for charting (consistent with how the other machine-readable
series in this project, e.g. WDI/FAOSTAT, are stored long-format). The other files here are
either two-point comparisons, single-year cross-sections, or narrative extractions where the
source's native wide/tabular shape is already the clearest presentation — reshaping them would
not add value (this mirrors the same judgment call documented in
`iran_dams_water_infrastructure_series/README.md`).

## Caveats — read before charting

- **`industry_import_dependence_1970.csv`** has several source-flagged data-quality notes
  preserved in the `notes` column, not silently resolved: Refrigerators' 40% figure is
  source-annotated "(understated?)"; Buses' import-dependence is `n.a.` in the source with an
  annotation "probably as trucks" (~48%); Synthetic Fibres is `n.a.` annotated "(above 50?)";
  Steel Wire/Nails/Screws' 30% figure carries a source "(?)" doubt marker. None of these were
  resolved to a single number — left exactly as the source presented the uncertainty.
- **`isfahan_steel_idro_capital_goods_1972.csv`** is narrative/qualitative, not a numeric time
  series — do not attempt to chart it directly; it is included here as documentary context for
  the Isfahan Steel Mill capacity figures that DO appear as numbers in
  `data/processed/iran_mining_series/usgs_iran_commodity_narrative_highlights_1965_1980.csv`
  (which independently corroborates the 750,000t first-stage target) and in the mining series'
  main production table. The 1972 report explicitly states it was "impossible accurately to
  assess the investment" for the first-stage Isfahan plant alone (town/infrastructure costs
  were commingled with plant costs in the accounts) — so no all-in dollar cost figure exists
  for this project in this archive; a real, logged gap rather than an omission.
- **Fiscal-year convention**: Iranian fiscal years in this era ran approximately 21 March to 20
  March (Nowruz-aligned), hence the "1954/55" style labels throughout `industrial_production_
  1954_1959.csv`, `gasoline_consumption_1955_1962.csv`, and the two railways files — do not
  conflate with the Gregorian calendar year when joining against other series in this project
  that use plain Gregorian years (e.g. `vehicle_registration_gasoline_1962_1972.csv`, which
  uses plain Gregorian years per its own source table).
- **`vehicle_registration_gasoline_1962_1972.csv`**: several `trucks_total` values across
  multiple years share the identical note "mission estimate (e), private/government breakdown
  not given in source" — this is not a copy-paste artifact, it is the source table's own
  repeated footnote marker for every year where that specific breakdown was unavailable.

## Sources

- World Bank Archives (`openknowledge.worldbank.org`), Iran country documents:
  `1960_current_economic_position_and_prospects.pdf` (Table 6, industrial production),
  `1970_industrialization_record_problems_prospects.pdf` (import-dependence survey),
  `1972_industrial_policies_and_priorities.pdf` (Isfahan Steel/IDRO/textile/automotive),
  `1962_economic_development_program.pdf` (Chapter 4: gasoline consumption Table 2, railways
  Tables 5-6, road vehicle registration Table 1), `1974_economic_development_vol4_statistical_
  appendix.pdf` (Table 14.7: vehicle registration & gasoline 1962-1972).

Full manifests and extraction methods (including exact PDF/printed page numbers and the visual-
verification method used for each): `data/raw/pahlavi-era-primary-extraction/wb1960-*/manifest.json`,
`wb1970-*/manifest.json`, `wb1972*/manifest.json`, `wb1962-*/manifest.json`,
`wb1974-vehicle-registration-gasoline-1962-1972/manifest.json`.
