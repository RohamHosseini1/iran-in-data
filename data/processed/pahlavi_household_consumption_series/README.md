# Pahlavi-era household expenditure & consumption series (1955–1982)

Harmonized 2026-07-13 from six raw World Bank archival extractions in
`data/raw/pahlavi-era-primary-extraction/` (all immutable, unchanged). These are the earliest
known Iran household-budget-survey tables in this project — they predate the digital
HEIS/IHEIS microdata era (`data/raw/iheis-microdata-metadata/`, registration-gated and not
directly accessible) and give genuine urban/rural, item-level detail on how Iranian households
spent money and what they ate in the decade before the oil-boom mid-1970s.

## Files

| File | Coverage | What it covers |
|---|---|---|
| `expenditure_composition_shares_1965_1971.csv` | 1965–1971, urban & rural | Household budget survey: expenditure by category (food/tobacco, housing, clothing, education, recreation, etc.) as a **% share of total expenditure**, plus households-surveyed sample sizes |
| `expenditure_levels_rials_1965_1971.csv` | 1965–1971, urban & rural | Same category breakdown as absolute **rials/month/household** (companion table to the shares file, same survey) |
| `expenditure_distribution_by_bracket_1971.csv` | 1971, urban/rural/total | % of households falling into each monthly-expenditure bracket (Rls <2,000 to Rls 30,000+) — a direct household-level inequality proxy, distinct from WID.world's top-income-share series in `data/processed/inequality_wid_world.csv` |
| `dairy_consumption_supply_1972_1977.csv` | 1972 (actual) & 1977 (projected) | Dairy products split into high-value (fresh milk, urban yogurt, cream, powdered milk) vs. low-value (rural yogurt, cheese, butter, butter-oil), each converted to a common fat-equivalent basis, plus the livestock supply side (cow/goat/sheep/buffalo head counts) |
| `food_demand_actual_and_projected_1972_1982.csv` | 1972 (actual), 1977 & 1982 (projected, low/high scenarios) | Rural/urban/total demand for wheat, red/white meat, rice, sugar, vegetable oil, eggs, pulses, dairy products, and feedgrains |
| `per_capita_consumption_index_1955_1958.csv` | 1955/56–1957/58 (Iranian solar years), reshaped long | Per-capita consumption **index** (1954/5=100) for agricultural products, wheat, sugar, tea, tobacco, textiles, cement, electricity, kerosene — the earliest consumption series in this project's Pahlavi-era archival material |

## Schema

Each file keeps close to its raw source's own column structure (these tables have genuinely
different shapes — expenditure shares vs. absolute levels vs. distribution brackets vs.
commodity-demand projections — flattening them into one common schema would have destroyed
information). Every file has `source` and `country_iso3` columns; all rows are `country_iso3 =
IRN`. `per_capita_consumption_index_1955_1958.csv` was reshaped from the raw file's wide
per-solar-year-row format into tidy long format (`solar_year, gregorian_year_approx, item,
index_value, unit, source, notes, country_iso3`) for consistency with the rest of this project's
long-format convention.

## Caveats — read before charting

- **`expenditure_levels_rials_1965_1971.csv` (Table 9.1) and `expenditure_composition_shares_1965_1971.csv`
  (Table 9.2) are companion tables from the same 1974 World Bank statistical appendix but their
  underlying households-surveyed counts do NOT always match exactly** (e.g. 1969 rural: 7,408 in
  the food/non-food levels table vs. 4,708 in the raw dairy/food-demand source used for the
  composition-shares households-surveyed rows). This is a genuine inconsistency in the 1974 World
  Bank source document itself, not an error introduced here — both are preserved exactly as
  printed, per `docs/bookkeeping.md` ("raw data is immutable... no fabricated data").
- **`expenditure_levels_rials_1965_1971.csv`: 1965–1967 urban figures are Bank Markazi Iran (BMI)
  data, not Statistical Centre of Iran (SCI) data** — a methodological break flagged in the
  source's own footnote 1 and carried into this file's `notes` column for those rows.
- **`expenditure_distribution_by_bracket_1971.csv` is labeled "Mission estimates" in the source**
  — i.e. a World Bank mission's own tabulation from underlying SCI survey microdata, not a
  directly-published SCI table. Treat as a credible but once-removed-from-primary estimate.
- **`dairy_consumption_supply_1972_1977.csv`: 1977 figures are the 1974 report's own projections
  for that year (made 3 years ahead), not necessarily realized outcomes** — the report itself
  frames 1972 as actual and 1977 as short-range projection; no later source was cross-checked to
  confirm whether 1977 actually landed at these levels.
- **`food_demand_actual_and_projected_1972_1982.csv`: only the 1972 column is actual demand
  (assuming constant prices). The 1977 and 1982 (low/high) columns are explicit World Bank
  mission demand *forecasts* made in 1974** under stated per-capita-expenditure and population
  growth assumptions (recorded per-row in the `note` column) — do not chart 1977/1982 rows as
  historical fact. Directly complements FAOSTAT Food Balance Sheets
  (`data/processed/agriculture_fbs_food_balances.csv`,
  `data/processed/agriculture_fbsh_food_balances_historic.csv`) which begin only in 1961 (FBSH)
  and don't carry Iran-specific demand-projection scenarios at all.
- **`per_capita_consumption_index_1955_1958.csv` values are index numbers (1954/5=100), not
  absolute quantities** — do not treat as physical consumption levels. Per the source's own
  footnote: "domestic production plus imports minus exports, without allowance for change of
  stocks. Population increase assumed to be 2.4 per cent per annum." `gregorian_year_approx` is
  a convenience column added here (Iranian solar year → approximate Gregorian range); the
  authoritative year field is `solar_year`, exactly as printed in the source.

## Sources

- World Bank, *Economic Development of Iran* (1974), Statistical Appendix — Tables 9.1
  (expenditure levels), 9.2 (expenditure shares), 9.3 (expenditure distribution), plus the dairy
  and food-demand-projection tables — retrieved via World Bank Archives
  (openknowledge.worldbank.org, Iran country documents).
- World Bank, *Current Economic Position and Prospects of Iran* (1960), Table 7 p.42 — source
  cited therein: Economic Bureau, Plan Organization (Iran).

Full manifests and extraction methods (including OCR/visual-verification notes where applicable):
`data/raw/pahlavi-era-primary-extraction/wb1974-household-expenditure-*/manifest.json`,
`data/raw/pahlavi-era-primary-extraction/wb1974-dairy-consumption-patterns-1972-1977/manifest.json`,
`data/raw/pahlavi-era-primary-extraction/wb1974-food-demand-projections-1972-1982/manifest.json`,
`data/raw/pahlavi-era-primary-extraction/wb1960-per-capita-consumption-1955-1958/manifest.json`.
