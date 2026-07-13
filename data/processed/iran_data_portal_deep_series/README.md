# Iran Data Portal deep-history series

These sat downloaded and unopened in `data/raw/iran-data-portal/` until 2026-07-12, when a
systematic sweep found they cover far more history than their folder-level manifests implied.
All four are genuine (verified by reading each file's own title row, after an initial naive
digit-scan produced false positives on a housing-rentals file that turned out to be 1996-2005
despite containing 4-digit numbers that looked like Persian years — those were rial price values,
not years; corrected before trusting anything here).

| File | Coverage | Source |
|---|---|---|
| `inflation_rate_1937_2014.csv` | **1937–2014, annual, 78 years** | Central Bank of Iran |
| `employment_by_sector_1956_2011.csv` | **1956–2011**, 14 sectors (agriculture, oil, mining, industry, construction, trade, services, etc.) | Statistical Centre of Iran (via Iran Data Portal) |
| `employment_by_gender_1966_2011.csv` | **1966–2011**, male/female/total + female labor share | Management and Planning Organization of Iran |
| `housing_units_by_household_census_1966_2006.csv` | **5 census points only**: 1966, 1976, 1986, 1996, 2006 — not annual | Statistical Centre of Iran |

The inflation and employment-by-sector series are now the deepest continuous Iran-specific
economic series in the database outside of Maddison's GDP/population reconstruction — both cover
essentially the entire Second Pahlavi era (1941–79) plus the full Islamic Republic period in one
unbroken run, straight from primary Iranian institutions (CBI, SCI, MPO), not a foreign secondary
source.
