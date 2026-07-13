# Bridged series

Hand-curated files that stitch together two or more raw sources spanning different eras into one
chartable timeline, when the underlying category definitions don't line up cleanly enough for the
`scripts/harmonize/*.py` pipeline to do it mechanically. Each file documents its own seams honestly
rather than pretending the join is perfect.

## citrus_production_iran_1950_2024.csv

Bridges the newly-extracted 1950-1958 World Bank table (`Oranges & Tangerines` combined, `Other
Citrus` separate) with FAOSTAT's 1961-2024 series (`Oranges`, `Tangerines...`, `Other citrus fruit`,
`Citrus Fruit, Total` — all reported separately).

**Honest caveat**: WB's 1958 combined total (Oranges & Tangerines 45,000t + Other Citrus 65,000t =
110,000t) is noticeably higher than FAOSTAT's 1961 "Citrus Fruit, Total" (78,900t) three years later.
This could be a real production decline (crop years vary), a definitional difference between the two
source methodologies, or a revision — we don't know which, and didn't guess. Present both segments on
the same chart as clearly-labeled distinct series rather than forcing a single continuous line through
the gap.

**How to use**: this file only carries 1950-1958 (Pahlavi/WB) plus a 1961 anchor row per FAOSTAT
category (to show where the two segments meet). For the full 1961-2024 annual FAOSTAT series, join
against `data/processed/agriculture_qcl_production.csv` filtered to `country_iso3=IRN` and
`item` in `Oranges`/`Tangerines, mandarins, clementines`/`Other citrus fruit, n.e.c.`/`Citrus Fruit,
Total`.
