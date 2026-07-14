# Progress log: variant-labels-fa

- [2026-07-14T09:02:13Z] Read _shared-context.md and persian-title-quality.md; loaded
  input file (600 unique variant labels, tab-separated n_charts/n_rows/label).
- [2026-07-14T09:02:13Z] Built translation in layers rather than strictly sequential
  50-label batches, since ~440 of the 600 labels are highly patterned (WDI/FAOSTAT
  style) and warranted regex-family handlers for consistency; all layers completed
  and merged in a single pass before writing output. Layers:
  - Layer 0 (exact dict): 158 labels - FAOSTAT/USGS commodity & mineral names,
    insurance snake_case series, monetary aggregates, Iran national-accounts
    rial series with em dashes, gold-coin & FX OHLC series, Spanish BCRA series,
    income-share percentiles (p0p100/p90p100/p99p100).
  - Layer 1 (regex): 57 labels - Population age-band family (UN/WDI demographic
    breakdowns by sex and 5-year age band).
  - Layer 2 (regex): 52 labels - Merchandise imports/exports by partner region;
    greenhouse-gas emissions by gas x sector.
  - Layer 3 (regex): 67 labels - Labor force participation / employment-to-
    population ratio / employment by sector / vulnerable employment / wage
    workers / self-employed / employers / contributing family workers, all
    crossed with sex, age band, and (national estimate | modeled ILO estimate).
  - Layer 4 (regex): 64 labels - mortality rate & deaths by age/sex, probability
    of dying, school enrollment (GPI, preprimary by sex), electricity production
    by source, sector value added, adjusted savings, service-trade categories.
  - Layer 5 (regex): 32 labels - resource rents, value added in manufacturing,
    freshwater withdrawals, education pupils/teachers, trade-volume % change.
  - Layer 6 (exact dict): 170 labels - remaining WDI/IMF/FAO singleton
    indicators (GDP/GNI/PPP family, fiscal/tax/revenue, energy, water,
    demographics, trade structure).
- [2026-07-14T09:02:13Z] QA pass: 600/600 labels present, 0 missing, 0 extra
  keys, 0 em/en dashes, 0 Arabic ي/ك, 0 duplicate fa strings, 0 stray Persian
  digits (fixed 16 entries that had crept in via percentile/mortality
  handlers), 0 unexpected leftover Latin text except legitimate chemical
  notation (CO2, CH4, N2O, P2O5) and the untranslatable acronym "DEC" (World
  Bank Development Economics group indicator name), both accompanied by full
  Persian context. Pruned 7 redundant "en" fields that just echoed the
  original label unchanged.
- [2026-07-14T09:02:13Z] Wrote web/src/lib/charts/variant-labels-map.json
  (600/600 labels, valid JSON, UTF-8). Task complete.
