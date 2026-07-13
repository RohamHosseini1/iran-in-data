# Iran provincial poverty rates, 2011–2020 (World Bank Poverty Assessment)

Extracted from `data/raw/worldbank-poverty-equity/iran-poverty-assessment-2023/` (immutable,
unchanged): the World Bank's *Islamic Republic of Iran Poverty Assessment* (November 2023), which
draws on Iran's own Household Income and Expenditure Survey (HIES) — the same underlying survey
program as the IHEIS microdata tracked (registration-gated) in
`data/raw/iheis-microdata-metadata/`. This gives Iran's provincial/regional poverty trend, a
genuinely different angle from the GDP-by-province data elsewhere in this project (economic
output vs. household poverty specifically).

## File

`iran_poverty_rate_by_region_2011_2020.csv` — schema: `region, poverty_rate_2011_percent,
poverty_rate_2020_percent, percentage_point_change`. Eight macro-regions (Central, Tehran Metro,
Northwest, Zagros, Caspian, Persian Gulf, Northeast, Southeast) plus the National figure, digitized
from the report's Figure 24 (poverty rate by region, 2011 vs. 2020).

## Key figures

National poverty rate rose from 20% (2011) to 28% (2020) of the population. Regional detail:
Southeast is both the highest-poverty region and the only one to cross 50% (43%→52%); Northwest
saw the largest percentage-point jump (16%→36%, +20pp — attributed in the source to drought and
agriculture-dependence); Tehran Metro was the most resilient (14%→16%, +2pp, tied with Caspian for
smallest increase).

## Caveats — read before charting

- Figures were digitized from the report's Figure 24 chart (not a printed data table) — treat as
  accurate to the nearest whole percentage point, not exact-decimal precision.
- The source PDF (`iran-poverty-assessment-november-2023.pdf`) and two supporting figure images
  (`figure24-poverty-rate-by-region-2011-2020.png`, `figure25-26-poverty-rate-by-province-map-and-correlation.png`)
  remain in the raw folder; Figures 25–26 (province-level map + correlation plot) were captured as
  images but not digitized into a CSV this round — the map format doesn't cleanly reduce to a
  tidy table, and the 8-region breakdown here already gives usable regional resolution. A future
  pass reading the province-level map directly (all 31 provinces individually) would be a natural
  deepening of this series.
- Poverty line/methodology (national poverty line vs. an international $/day line) is defined in
  the source PDF's methodology section, not repeated here — consult the PDF directly before
  combining with a different poverty measure from another source.

## Sources

World Bank, *Islamic Republic of Iran Poverty Assessment* (November 2023),
documents1.worldbank.org, based on Iran's Household Income and Expenditure Survey (HIES) data.

Full manifest: `data/raw/worldbank-poverty-equity/iran-poverty-assessment-2023/manifest.json`.
