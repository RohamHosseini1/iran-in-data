# Iran trade institutions, remittances & parallel-FX series (1960–2026)

Harmonized 2026-07-13 from ten raw source folders (all immutable, unchanged):
`data/raw/iran-opec-membership/`, `data/raw/iran-wto-gatt-accession/`,
`data/raw/imf-article-iv-iran/`, `data/raw/worldbank-knomad/`,
`data/raw/imf-iran-parallel-fx-history/`, `data/raw/fx-parallel-rate/`,
`data/raw/iran-handicrafts-non-carpet/`, `data/raw/iran-caviar-exports/`, plus two comparator
folders `data/raw/venezuela-parallel-fx-history/` and `data/raw/bcra-argentina/`.
**Extended 2026-07-13 (later, same day)** with an eleventh raw source folder,
`data/raw/iran-parallel-fx-1979-2010-research/`, a targeted gap-fill round that closes nearly all
of the 1979-2010 parallel-FX gap flagged in `docs/bookkeeping.md` (see `usd_irr_parallel_rate_1979_2011.csv`
below).

## Files

| File | Coverage | What it covers |
|---|---|---|
| `opec_quota_policy_history_1960_2025.csv` | 1960–2025, non-continuous (dated milestones) | OPEC founding (Iran a founding member), 1973 nationalization, 1982 first quota system, 1986 quota collapse, 1990/1992/1993 quota revisions, sanctions-era exemptions (2016 OPEC+ exemption, 2018 re-sanctioning), 2020 production trough (1.93M b/d), 2024 recovery |
| `wto_gatt_accession_timeline_1995_2026.csv` | 1995–2026, non-continuous | Iran has NEVER completed WTO accession: 1996 application, blocked 22× by 2001–2005, Working Party established 2005, still never held its first meeting as of this database's compilation |
| `imf_article_iv_consultation_history_2002_2025.csv` | 2002–2025, 8 completed consultations + a documented 2019–2024 gap | Dates and headline findings per consultation; 2018 is the last full consultation completed; 2025 saw only an informal Board briefing, not a full consultation |
| `mazarei_1995_parallel_fx_market_1978_1990.csv` | 1978–1990 (descriptive statistics, not a monthly series) | IMF Working Paper 95/69 (Mazarei): parallel-market rial/dollar rate volatility statistics, parallel-market premium reaching "among the highest ever observed internationally" (~2,000%+ by Dec 1990), oil/gas export earnings 1978/1986/1990, and the striking fact that "in certain periods over ten different exchange rates were in effect" |
| `usd_irr_parallel_rate_1979_2011.csv` | 1979–2011: monthly Jan 1979–Dec 2003 (300 months, complete), plus 11 annual/point anchors for 2001 and 2004–2011 | **Closes nearly the entire 1979-2010 parallel-FX gap.** Backbone is Bahmani-Oskooee (2005, Iranian Economic Review, University of Tehran) Table 4 — a complete monthly black-market rial/USD series sourced to the World Currency Yearbook (Pick's) through mid-1989 and directly to the Central Bank of Iran from mid-1989–2003; extracted from a scanned PDF via 300dpi visual read, cross-checked against a full tesseract OCR pass (exact match). 2004-2011 covered at annual granularity via Wikipedia's transcription of CBI Annual Review 2013/14 figures (one hop removed from the primary CBI document — cbi.ir and its Wayback mirror were both inaccessible this round) plus one World Bank (Nov-2001) and one PBS Frontline (mid-2005) point. See `data/raw/iran-parallel-fx-1979-2010-research/manifest.json` for full per-figure citations, cross-validation notes, and a list of conflicting/ambiguous figures found but deliberately excluded |
| `usd_irr_parallel_rate_daily_2011_2026.csv` | Daily, 2011-11-26 to 2026-07-11 (3,899 observations) | USD/IRR free-market (parallel/black-market) exchange rate — open/low/high/close + day-over-day change, parsed from raw TGJU.org JSON (previously un-parsed per its own manifest) |
| `gold_coin_bahar_azadi_price_daily_2013_2026.csv` | Daily, 2013-07-22 to 2026-07-11 (3,432 observations) | Bahar Azadi gold coin price (rial), Iran's classic inflation-hedge/informal-savings instrument |
| `gold_coin_emami_price_daily_2010_2026.csv` | Daily, 2010-04-04 to 2026-07-11 (4,237 observations) | Emami gold coin price (rial) |
| `knomad_remittances_migration_2000_2023.csv` | 2000–2023 (aggregate flows) + 2021 (bilateral matrix + diaspora stock) | World Bank KNOMAD aggregate remittance in/outflows (both reported as exactly 0 for Iran every year — see caveats), 2021 bilateral remittance *outflows* from Iran (to Afghanistan, Pakistan, Iraq, etc. — migrant workers resident in Iran sending earnings home), and 2021 Iranian-diaspora stock by host country (1,387,646 persons worldwide, largest in the US at 389,383) |
| `handicraft_export_and_institutional_history.csv` | 1930s–2025, non-continuous | Non-carpet handicraft export value (COVID collapse $427M→$120M, recovery to $400M by 2022/2025), 570,000 registered craftsmen, UNESCO Creative Cities (Isfahan, Bandar Abbas), 1930s Reza Shah-era craft-preservation schools |
| `cites_caviar_quota_trade_timeline_1998_2006.csv` | 1998–2006, non-continuous | Extends the specialty-goods caviar series (see `data/processed/specialty_goods_series/`): 1998 baseline exports (40t), 1998–2004 cumulative (480t+, largest global exporter), the June 2001 Paris Agreement exemption that made Iran the dominant legal exporter, Caspian-wide quota totals 2001–2003 |
| `venezuela_parallel_fx_rate_milestones_2003_2020.csv` | 2003–2020, non-continuous milestones | Venezuela official vs. black-market FX rate at each major devaluation/redenomination milestone — comparator for Iran's own official-vs-parallel FX gap |
| `argentina_fx_retail_rate_daily.csv`, `argentina_fx_wholesale_reference_rate_daily.csv` | Daily, 2010–2026 | Argentina (BCRA) retail and wholesale-reference ARS/USD exchange rates — comparator |
| `argentina_international_reserves_daily.csv` | Daily, back to 1996 (7,510 observations) | Argentina international reserves, millions USD — comparator |
| `argentina_badlar_interest_rate_daily.csv`, `argentina_monetary_policy_rate_daily.csv` | Daily | Argentina BADLAR private-bank deposit rate and monetary policy rate — comparator |

## Caveats — read before charting

- **`usd_irr_parallel_rate_daily_2011_2026.csv` and the two gold-coin files' `open`/`low`/`high`/
  `close` column labels follow TGJU's documented standard OHLC column order for this API
  endpoint family, but the raw JSON itself carries no column headers** (it is a bare 8-element
  array per row: 4 price fields, an HTML-wrapped change amount, an HTML-wrapped change percent,
  and two date formats). The mapping used here (open, low, high, close) is TGJU's standard
  convention for `summary-table-data` endpoints; if a future user needs certainty beyond this
  convention, cross-check a handful of known dates against tgju.org's own rendered table.
  `change_direction` (`high`/`low`/blank) reflects the CSS class TGJU used to color that day's
  move up/down/flat in its own UI, not an independent data point.
- **KNOMAD's own aggregate remittance in/outflow series is internally inconsistent**: both
  `WB_KNOMAD_MRI` (inflows) and `WB_KNOMAD_MRO` (outflows) report an explicit **0** for Iran
  every year 2000–2023 — consistent with WDI's `BX.TRF.PWKR.CD` being null for Iran (exclusion
  from formal SWIFT-based remittance channels under sanctions) — **but** the same KNOMAD product's
  2021 bilateral remittance matrix shows real, nonzero bilateral outflows from Iran (e.g. $53.1M
  to Pakistan, $123.4M to Afghanistan, $197.1M total). This contradiction is in KNOMAD's own
  published data, not introduced here; both the (zero) aggregate series and the (nonzero)
  bilateral matrix are preserved as printed, flagged rather than reconciled. The bilateral flows
  are outflows FROM Iran (most likely migrant/refugee workers, notably Afghans, resident in Iran
  sending earnings home) — no country reports a remittance corridor INTO Iran.
- **`usd_irr_parallel_rate_1979_2011.csv`'s 2004-2011 annual anchors are one hop removed from
  their primary source.** They were read from Wikipedia's own transcription of Central Bank of
  Iran "Annual Review 2013/14" + CIA World Factbook figures, not independently re-fetched from
  cbi.ir (geo-blocked from this project's environment, consistent with every other direct
  CBI/domestic-Iran-site access attempt across this project) or its Wayback Machine mirror
  (inaccessible this round because this session's browser tool specifically blocked read access
  to the web.archive.org domain). Every affected row's `source_confidence`/`citation`/`notes`
  fields flag this explicitly. The 1979-2003 monthly backbone does NOT have this caveat — it was
  read directly from the primary academic PDF (`data/raw/iran-parallel-fx-1979-2010-research/
  bahmani_oskooee_2005_history_of_rial_fx_policy_iran.pdf`), visually verified page-by-page.
- **`mazarei_1995_parallel_fx_market_1978_1990.csv` contains only descriptive statistics
  (mean, min/max, standard deviation, skewness/kurtosis of monthly rate changes), not a
  month-by-month parallel-rate series** — the source IMF working paper's Table 1 and Chart 1
  data points were not transcribed into machine-readable form by the extracting agent; the PDF
  itself remains in the raw folder for a future deeper-extraction pass if the monthly series is
  wanted.
- **Handicraft export figures are Tehran Times (state-media-attributed)** per
  `docs/bookkeeping.md` source-reliability rule 4 — routine trade statistics quoted from a named
  government official, not independently cross-checked against a non-state source this round.
- **Argentina BCRA comparator files are daily raw central-bank data with no curation applied**
  beyond JSON→CSV conversion — per this project's Iran-first priority, comparator depth here is
  intentionally just "whatever the same-format API already provided," not independently
  deepened. `argentina_international_reserves_daily.csv` extends back to 1996, well before the
  other four BCRA series (which start 2010) — a genuine difference in each series' own history
  length, not a truncation on this project's side.

## Sources

- Wikipedia (OPEC, Petroleum industry in Iran), MERIP, Oil & Gas Journal, EIA, RUSI, Stimson
  Center, GIS Reports, AGSI (OPEC quota history — secondary-source synthesis, cross-checked
  where multiple sources cited).
- WTO official accession-status page (wto.org), USTR, Wikipedia, IRFA Journal (Khodakarami 2015).
- IMF (Public Information Notices, press releases, mission concluding statements) — Article IV
  consultation history.
- Mazarei, A. (1995), "Iran's Financial System: An Assessment of Structural Features," IMF
  Working Paper 95/69 — parallel-market FX statistics.
- Bahmani-Oskooee, M. (2005), "History of the Rial and Foreign Exchange Policy in Iran," Iranian
  Economic Review Vol.10 No.14 — complete monthly black-market rial/USD series 1947-2003.
  World Bank Report No. 22953-IRN (2001), "Iran: Trade and Foreign Exchange Policies in Iran."
  Wikipedia "Iranian rial" (transcribing CBI Annual Review 2013/14 + CIA World Factbook) and PBS
  Frontline/Tehran Bureau (2012) — 2004-2011 annual/point anchors.
- TGJU.org (Iranian financial data aggregator) — parallel USD/IRR rate, Bahar Azadi and Emami
  gold coin prices.
- World Bank KNOMAD (Global Knowledge Partnership on Migration and Development) — remittances
  and migration data.
- Tehran Times (state-media-attributed), Encyclopaedia Iranica, UNESCO Creative Cities Network —
  handicrafts.
- CITES Animals Committee, UN press releases, academic literature (sturgeon/paddlefish trade) —
  caviar quota/trade timeline.
- CADIVI/CENCOEX/DICOM official releases and parallel-market trackers — Venezuela FX comparator.
- BCRA (Banco Central de la República Argentina) statistics API — Argentina FX/rates comparator.

Full manifests: `data/raw/iran-opec-membership/*/manifest.json`,
`data/raw/iran-wto-gatt-accession/*/manifest.json`, `data/raw/imf-article-iv-iran/*/manifest.json`,
`data/raw/imf-iran-parallel-fx-history/*/manifest.json`, `data/raw/fx-parallel-rate/*/manifest.json`,
`data/raw/worldbank-knomad/*/manifest.json`, `data/raw/iran-handicrafts-non-carpet/*/manifest.json`,
`data/raw/iran-caviar-exports/cites-quota-trade-timeline-1998-2006-retry/manifest.json`,
`data/raw/venezuela-parallel-fx-history/*/manifest.json`, `data/raw/bcra-argentina/*/manifest.json`,
`data/raw/iran-parallel-fx-1979-2010-research/manifest.json`.
