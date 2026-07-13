# Iran automotive & textile industry (1923–2018)

Harmonized 2026-07-13 from two raw source folders (`data/raw/iran-automotive-industry/`,
`data/raw/iran-textile-industry/`; both immutable, unchanged) into one combined folder,
mirroring the `specialty_goods_series/` pattern. Both files re-copy already-transcribed raw
`data.csv` tables through Python's `csv` module (normalizing quoting only, no numeric changes).

Unlike the Pahlavi archival material in `pahlavi_industry_series/`, both sources here are
mostly **secondary** (Wikipedia, an Iranica-mirroring trade site) rather than primary World
Bank documents — flagged explicitly per file below, consistent with this project's source-
reliability conventions (`docs/bookkeeping.md`). Both are cross-referenced against genuine
primary-source data already in this archive (the World Bank's 1972 industrial report) where
that overlap exists.

## Files

| File | Coverage | What it covers |
|---|---|---|
| `automotive_paykan_national_production_1967_2018.csv` | 1967-2018 (milestone events, sparse) + 1970/1980/1990/2000/2005/2015 (production-count data points) | Iran Khodro / Paykan production history: 1967 launch (Hillman Hunter CKD kits from Rootes Group UK, ~6,000 units/year initial rate) through 2005 sedan-line closure (2.3 million cumulative Paykans) and 2015 pickup-variant end; national total motor-vehicle-production counts at 6 points from 1970 (35,000) to 2005 (817,200), showing the Iran-Iraq War-era collapse (1990: 44,665, down from 1980's 161,000) and subsequent recovery. |
| `textile_sector_pahlavi_to_2002.csv` | 1923-2002 | Textile-sector buildout across the entire Pahlavi era and into the Islamic Republic: factory count (26 in 1931 → 51 companies by 1955), spindle count (nearly doubled 1950-62, then to 900,000 by 1972, 1.5 million by 1993), employment (24,500 modern-mill workers by 1940 → ~420,000 total sector employment by 1993), the 1966 import-substitution milestone (Iran stopped importing cotton fabric entirely), and cotton production's 1975 peak (716,000 metric tons) followed by a ~71% collapse by 1981. |

## Schema

`year, metric, value, unit, notes[, source]` — both files use a variant of this schema (the
automotive file's 5th column is `source` per-row since its provenance mixes Wikipedia and a
primary World Bank cross-reference within the same table; the textile file's schema is
`year, metric, value, unit, notes` with a single blended source cited in this README instead,
since virtually every row traces to the same Iranica article).

## Caveats — read before charting

- **`automotive_paykan_national_production_1967_2018.csv` contains one explicitly flagged
  unresolved discrepancy, preserved rather than resolved**: a secondary-source synthesis
  estimate of ~100,000 Paykan-specific units for 1979 is NOT reconcilable with the 1980
  all-vehicle-industry total of 161,000 in the same file (different scope — single model vs.
  whole industry — and different, lower-confidence source lineage: bestsellingcarsblog.com /
  aronline.co.uk web-search synthesis, vs. the Wikipedia production-by-year table for the
  official industry-wide figures). Do not chart these two numbers as directly comparable
  points on the same series.
- **Most of this file is Wikipedia-sourced** (`en.wikipedia.org/wiki/Paykan`,
  `en.wikipedia.org/wiki/Automotive_industry_in_Iran`), a secondary source — used here because
  no primary Iranian industrial-statistics source with a comparable multi-decade production
  count was found in this project's holdings (flagged in the raw manifest's `failures` field:
  Iran Khodro's own investor-relations archive, and SCI Iran Statistical Yearbook automotive
  tables, were not checked in the original download round — a real gap for a future pass, not
  a dead end). The one point independently corroborated by a primary source (Paykan's
  market-leading, internationally price-competitive position as of 1972) is cross-cited to
  `data/processed/pahlavi_industry_series/isfahan_steel_idro_capital_goods_1972.csv`.
- **`textile_sector_pahlavi_to_2002.csv`**: the canonical source
  (iranicaonline.org/articles/textile-industry-in-iran/) blocks direct fetch with a Cloudflare
  403, consistent with this domain's well-documented blocking pattern elsewhere in this
  project (see `specialty_goods_series/README.md`'s tobacco/carpet/sugar/tea files, which used
  an interactive browser tool for the same domain instead). This file instead used a working
  mirror (iranyarn.ir, an Iranian textile trade site reproducing the same Iranica article),
  cross-checked against an independent WebSearch synthesis of the original Iranica text that
  returned matching 1972/1975 figures — increasing confidence the mirror is faithful, though
  it remains a secondary reproduction rather than the primary article itself.
- **`textile_sector_pahlavi_to_2002.csv`** has one explicitly flagged units caveat: the 1995
  cotton-production figure (150,000 metric tons) is on a "beaten/processed cotton" basis,
  different from the unginned-cotton basis used for the 1975/1981/1997 figures in the same
  file — not directly comparable year-over-year across that boundary.
- **Many rows in both files are qualitative milestones with blank `value`/`unit` cells**
  (e.g. "Paykan pickup variant production begins", "Import ban lifted") — these are
  intentionally kept as zero-value narrative rows (year + description, no number) rather than
  dropped, since they provide essential interpretive context for the numeric rows around them;
  do not attempt to plot them as data points.

## Sources

- Wikipedia: "Paykan", "Automotive industry in Iran" (cross-referenced against World Bank
  Archives `1972_industrial_policies_and_priorities.pdf`, already in this project — see
  `data/processed/pahlavi_industry_series/isfahan_steel_idro_capital_goods_1972.csv`).
- Encyclopaedia Iranica, "Textile Industry in Iran" (Willem M. Floor / successor authorship per
  standard Iranica attribution), retrieved via iranyarn.ir mirror; cross-checked via
  independent WebSearch synthesis of the same article.

Full manifests and extraction methods:
`data/raw/iran-automotive-industry/khodro-paykan-production-history/manifest.json`,
`data/raw/iran-textile-industry/pahlavi-era-textile-sector-overview/manifest.json`.
