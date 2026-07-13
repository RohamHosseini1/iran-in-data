# Iran disasters, regional & social series (1956–2023)

Harmonized 2026-07-13 from six raw source folders (all immutable, unchanged):
`data/raw/noaa-ncei-hazards/`, `data/raw/academic-gender-economics/`,
`data/raw/iran-data-portal/marriage-and-settlement-tables/`, and
`data/raw/iran-data-portal/labor-tables/`. (Poverty-by-region and nomad-population/pastoral-
economy material — also part of this "regional/social/disaster" bucket — live in their own
existing sibling folders, `data/processed/worldbank_poverty_equity/` and
`data/processed/nomadic_pastoral_economy/`, each newly given a README this round; see those.)

## Files

| File | Coverage | What it covers |
|---|---|---|
| `significant_earthquakes_1956_2023.csv` | 1956–2023, 36 events | NOAA NCEI Significant Earthquake Database: location, magnitude, depth, deaths, injuries, houses destroyed, and economic damage (millions USD) for every quantified-damage Iran earthquake, including all five well-known major events (Buin Zahra 1962, Tabas 1978, Manjil-Rudbar 1990, Bam 2003, Kermanshah 2017) |
| `gold_price_divorce_rate_study.csv` | 1980–2014 (descriptive statistics, not a year-by-year series) | Academic econometric study's descriptive statistics on divorce rate, real gold-coin price (Mehrieh/dowry link), female literacy, social globalization index, GDP-per-capita growth; plus the narrative marriage-age-rise fact (24→27 years, 1986–2011) |
| `mean_age_at_first_marriage_1966_2006.csv` | 6 census years, 1966–2006 | Mean age at first marriage by sex, urban/rural/total (Hajnal's method) |
| `registered_marriages_divorces_1991_2006.csv` | National annual 1991–2006 + all 30 provinces for 2006 | Registered marriages & divorces, urban/rural/total |
| `registered_births_by_sex_1991_2006.csv` | National annual 1991–2006 + all 30 provinces for 2006 | Registered births by sex, urban/rural/total |
| `settled_unsettled_population_by_province_2006.csv` | 2006 census, single cross-section | Settled-urban / settled-rural / unsettled population & households, all 30 provinces + national (sums reconcile exactly to the national 2006 census total, 70,495,782) |
| `labor_force_participation_rate_2005_2014.csv` | Annual, 2005–2014 | LFP rate by sex, urban/rural/total |
| `labor_force_by_occupation_and_gender_2005_2013.csv` | Annual, 2005–2013 | Employed persons by 11 occupation categories × sex × urban/rural/total (891 rows) |
| `employed_persons_by_sector_1956_2011.csv` | Annual, 1956–2011 | Employed persons by 13 economic sectors (agriculture, oil, mining, industry, construction, transport, trade, services, etc.) — one of the longest continuous annual employment series in this project |
| `employed_population_by_gender_1966_2011.csv` | Annual, 1966–2011 | Employed persons by sex + women's share of total employment (13.3% in 1966, tracked annually) |
| `ssi_pensioners_and_amounts_paid_1991_2006.csv` | 8 years, 1991–2006 | Social Security Organization pensioners and amounts paid, by category (retirees, work-related disabled, other-cause disabled, survivors) |

## Cross-validation performed

- `settled_unsettled_population_by_province_2006.csv`: summing all 30 provinces' total population
  gives exactly 70,495,782 — the national 2006 census total also confirmed independently in
  `data/processed/iran_census_demographics_series/national_and_provincial_summary_2011_census.csv`
  (Table 1, "2006" row).
- `labor_force_by_occupation_and_gender_2005_2013.csv` and `employed_persons_by_sector_1956_2011.csv`:
  spot-checked national "Total" cells against the raw spreadsheet's own printed totals — exact match.

## Caveats — read before charting

- **`gold_price_divorce_rate_study.csv` is NOT a year-by-year time series** — the source paper
  (an econometric regression study) presents its underlying 1980–2014 divorce-rate/gold-price
  data only as a chart (Figure 1, not text-extractable) and as summary descriptive statistics
  (Table 1, mean/min/max), which is what's captured here. For an actual annual divorce-rate
  series, see `registered_marriages_divorces_1991_2006.csv` in this same folder (narrower window,
  1991–2006, but genuine year-by-year figures).
- **`registered_marriages_divorces_1991_2006.csv` and `registered_births_by_sex_1991_2006.csv`
  both carry a "Revised figures" footnote flag on several years** (marked `(1)` in the raw source
  for 1370/1991, 1380/2001, and 1384/2005) — the raw spreadsheets do not specify what was revised
  or why; flagged here for transparency, not resolved.
- **Province-level rows in the marriage/divorce and births tables are for 2006 only** (the raw
  source tables give a national annual time series 1991–2006 but provincial breakdown only for
  the final year) — do not expect a province-level time series from these files.
- **`labor_force_by_occupation_and_gender_2005_2013.csv` covers only 9 years (2005–2013)**, one
  year short of the sibling LFP-rate file's 2005–2014 — the raw source spreadsheet itself stops
  one year earlier for the occupation breakdown; not an extraction gap.
- **`employed_persons_by_sector_1956_2011.csv` is Iran's longest continuous sectoral-employment
  series in this project (55 years, national level only)** — no urban/rural or sex breakdown is
  available at this length; for gender-disaggregated employment over a similarly long span, use
  `employed_population_by_gender_1966_2011.csv` (starts 10 years later, national totals only, no
  sectoral breakdown).
- All Iran Data Portal tables note "Source: Statistical Centre of Iran" or "Civil Registration
  Organization" or "Ministry of Cooperatives Labour and Social Welfare" per their own printed
  source lines; Iran Data Portal (irandataportal.syr.edu) itself was directly reachable (HTTP 200)
  with no bot-challenge or geo-block, consistent with this project's established pattern that
  foreign-hosted mirrors of Iranian official statistics are far more reliably reachable than
  Iran's own domestic government sites.

## Sources

- NOAA National Centers for Environmental Information (NCEI), Significant Earthquake Database
  (ngdc.noaa.gov/hazel).
- Farzanegan, M.R. & Gholipour, H.F. (2018), "Does Gold Price Matter for Divorce Rate in Iran?",
  MACIE Discussion Paper 2018/05, Philipps-Universität Marburg.
- Statistical Centre of Iran (SCI), Civil Registration Organization, and Ministry of Cooperatives
  Labour and Social Welfare, all via Iran Data Portal (Syracuse University Moynihan Institute,
  irandataportal.syr.edu).

Full manifests: `data/raw/noaa-ncei-hazards/iran-significant-earthquakes/manifest.json`,
`data/raw/academic-gender-economics/farzanegan-gholipour-2018-gold-divorce/manifest.json`,
`data/raw/iran-data-portal/marriage-and-settlement-tables/manifest.json`,
`data/raw/iran-data-portal/labor-tables/manifest.json`.
