# Iran specialty-goods monopoly/export series: tobacco, carpets, caviar, sugar, tea (1890–2025)

Hand-curated, citation-preserving extraction of Iran's historic state-monopoly commodities —
tobacco, handwoven carpets, caviar/sturgeon, sugar, and tea — none of which FAOSTAT covers pre-1961,
and several of which (carpets, caviar-as-roe, monopoly/fiscal structure) FAOSTAT never covers at any
date since it is a pure agricultural production/trade-quantity database. Harmonized 2026-07-13 from
four raw source folders (`data/raw/iran-tobacco-monopoly/`, `data/raw/iran-carpet-exports/`,
`data/raw/iran-caviar-exports/`, `data/raw/iran-sugar-tea-history/`; all immutable, unchanged) into
one combined folder, mirroring the `iran_data_portal_deep_series/` pattern of small, well-documented,
per-topic CSVs. Nothing was interpolated, estimated, or fabricated; every ambiguous or internally
inconsistent source value is preserved exactly as printed with the discrepancy flagged in its own
`notes` cell, never silently corrected.

## Files

### Tobacco

| File | Coverage | What it covers |
|---|---|---|
| `tobacco_monopoly_1890_1995.csv` | 1890–1995 (sparse) | 1890 Tobacco Régie concession terms, 1929 Dokhaniyat state-monopoly conversion, 1940 cultivation/output (pre-FAOSTAT), 1967 workforce (750,000), 1995 factory workforce |
| `tobacco_post_privatization_2018.csv` | 2018 (single snapshot) | Post-2012-privatization consumption, active smokers, import dependency (80% of leaf), Iranian Tobacco Company's collapsed market share (~17.5%) vs. Japan Tobacco International (>50%) |

### Carpets

| File | Coverage | What it covers |
|---|---|---|
| `carpet_exports_1960_1988.csv` | 1960–1986 (sparse) | Export value (rials/USD), Iran Carpet Company's state-monopoly share of national output |
| `carpet_exports_post1990.csv` | 1994–2024 (sparse) | Export value/volume compiled from news reporting on Iran National Carpet Center + UN Comtrade data; 1994 all-time peak ($2.132bn) through post-JCPOA-withdrawal collapse to tens of millions USD |

### Caviar / sturgeon

| File | Coverage | What it covers |
|---|---|---|
| `caviar_cites_quota_2006.csv` | 2006 (single data point) | CITES-authorized Persian-sturgeon caviar export **quota** (regulatory ceiling, not actual output) |
| `caviar_sturgeon_aquaculture_eumofa_2010_2018.csv` | 2010–2018 (continuous) | Whole-fish sturgeon aquaculture production (tonnes, NOT caviar/roe weight) — Iran's pivot from wild-catch to farming |
| `caviar_shilat_production_2013_2024.csv` | 2013/14, 2020–2024 (sparse) | Iran Fisheries Organization (Shilat) official caviar production/export/sturgeon-meat tonnage |

### Sugar & tea

| File | Coverage | What it covers |
|---|---|---|
| `sugar_1890_2000.csv` | 1890–2000 (sparse; near-continuous 1906/07–1913/14) | Tehran consumption, sugar-import-value-by-country-of-origin table (Russia/France/Belgium/etc.), 1932 state-monopoly founding, 1970s–1980s consumption growth, year-2000 ISO ranking |
| `tea_1895_1984.csv` | 1895–1984 (sparse) | Pre-cultivation import era, cultivation-area buildout (100 ha 1920 → 24,000+ ha 1968), state Iran Tea Organization/Company founding, production/import ranges |
| `trans_iranian_railway_financing_context.csv` | 1938–39 (single data point) | Cumulative Trans-Iranian Railway cost — fiscal context for the 1925 sugar/tea excise tax that substantially financed it |

## Schema

`year, metric, value, unit, source, notes, country_iso3` — one row per statistic (all files use this
exact schema, unlike the other series in this harmonization batch, since every raw source already
shipped a `notes` column). All rows are `country_iso3 = IRN`.
`caviar_sturgeon_aquaculture_eumofa_2010_2018.csv`'s source table also has China/Russia/USA/Vietnam/
Armenia/EU columns per the underlying EUMOFA report, but only Iran's column was extracted here (the
project is Iran-first; see raw manifest for the full country list if a future pass wants the
comparators).

## Caveats — read before charting

- **A raw-source quoting defect was fixed on the way into this folder, not left to corrupt the
  data.** 11 rows across three raw files (`carpet_exports_post1990.csv` x3,
  `caviar_cites_quota_2006.csv` x1, `tea_1895_1984.csv` x7) have a `metric` value containing an
  unescaped comma inside an unquoted CSV field (e.g. `Carpet export value (Q2 only, not annual)`),
  which caused a naive CSV parse to split it into an extra column and shift `value`/`unit` out of
  place. Per `docs/bookkeeping.md` ("raw data is immutable, fixes happen in `data/processed/`"), the
  raw files were left untouched and this was corrected here by rejoining the split `metric` text —
  no numeric values were altered, only column alignment. Verified: every file in this folder now has
  a uniform column count per row.
- **Every "sparse" series above is snapshot-based, not continuous.** Points land only where a
  citable source happened to give a number; do not interpolate between years on a chart without
  labeling the gap explicitly.
- **`sugar_1890_2000.csv`** contains one preserved-not-corrected arithmetic discrepancy (the 1906/07
  country-breakdown rows sum to ~0.3% more than the printed total) and one year-typo correction
  ("1656-57" → 1956, explained in that row's `notes` — chronologically impossible otherwise since no
  sugar mills existed in 1650s Iran).
- **`carpet_exports_1960_1988.csv`** flags a likely million/billion-rial unit error in the printed
  source for 1982 and 1983 (values transcribed exactly as printed, not corrected — see each row's
  `notes`).
- **`carpet_exports_post1990.csv`** has one state-media-attributed row (Tehran Times, 2024 figure),
  labeled per `docs/bookkeeping.md` source-reliability rule 4, with no independent corroboration
  found for that specific most-recent figure. Two rows are explicitly sub-annual (Q2 2020, 11-month
  1401/1400) and flagged — do not chart alongside full-year totals without labeling.
- **`caviar_shilat_production_2013_2024.csv`** has three Tehran-Times-sourced rows, labeled
  state-media-attributed; all are on-the-record quotes from a named Iran Fisheries Organization
  official, not anonymous claims. The Financial Tribune 2022 figures come from a headline/lede only
  (full article body was un-retrievable — a redirect stub) but are direct quotes, not paraphrased.
- **`caviar_cites_quota_2006.csv` measures a regulatory ceiling, not actual production or exports** —
  do not conflate with the Shilat production figures in the sibling file; they measure different
  things (permitted volume vs. reported output) roughly a decade apart.
- **`caviar_sturgeon_aquaculture_eumofa_2010_2018.csv` measures whole-fish live weight**, not
  extracted caviar/roe weight (roe is typically ~10–15% of a mature female sturgeon's weight) — not
  directly comparable, tonne-for-tonne, to the caviar-specific figures in
  `caviar_shilat_production_2013_2024.csv`. Table was visually verified via `pdftoppm -r 200` render
  against the raw PDF text extraction (which used European `.`-as-thousands-separator formatting that
  could otherwise be misread).
- **`trans_iranian_railway_financing_context.csv` is total project cost, not tax revenue** — a
  year-by-year or commodity-disaggregated (sugar-only vs. tea-only) sugar/tea excise **revenue**
  series was specifically sought and NOT found in freely accessible sources; logged as a real gap
  (see raw manifest `failures`), not silently dropped. A primary-source lead (Majlis budget-law
  archives, already in this project at `data/raw/majlis-historical-budget-laws/`) is noted for a
  future pass.
- **Retrieval methods vary by file** — Encyclopaedia Iranica articles (tobacco, carpets both eras,
  sugar, tea) were retrieved via an interactive browser tool since iranicaonline.org blocks
  curl/WebFetch with a Cloudflare challenge (HTTP 403); `sugar_1890_2000.csv`'s Table 1 was
  additionally visually verified against its own source table image
  (`data/raw/iran-sugar-tea-history/iranica-sugar-narrative-and-table1/sugar_table_1.jpg`), not OCR'd.
  CITES's own quota-document archive was blocked by a CAPTCHA and — per this project's safety
  rules — not bypassed; the 2006 quota figure was instead sourced via a UN News report of the same
  CITES Secretariat announcement.

## Not harmonized (too thin to be worth a standalone series)

None of the 10 raw sub-datasets in this group were skipped — every one had at least one genuine,
citable, non-fabricated data point, so every raw file here has a corresponding processed file. Two
files (`caviar_cites_quota_2006.csv`, `trans_iranian_railway_financing_context.csv`) are intentionally
single-row files: each is a single point-in-time data point (a regulatory quota, a cumulative cost
figure) rather than a series, but both are kept as standalone files because they are genuinely useful
context/cross-check anchors for their respective sibling series, and combining them into another
file would obscure their very different nature (a ceiling vs. an output; a cumulative cost vs. a
revenue flow).

## Sources

- Encyclopaedia Iranica: "DOKĀNĪYĀT" (tobacco), "CARPETS xii" (Pahlavi period) & "CARPETS xiii"
  (post-Pahlavi period), "SUGAR", "TEA" — all iranicaonline.org, Willem M. Floor / P.R. Jim Ford /
  Daniel Balland & Marcel Bazin as credited per article.
- UK Parliament historic Hansard, 23 May 1892 Commons debate on the Persian Tobacco Concession.
- Tobacco Asia trade press, "Iran in Focus" (16 July 2018).
- Radio Farda (RFE/RL), Iran International, Tehran Times [state-media-attributed], tradingeconomics.com
  (UN Comtrade), farahancarpet.com — carpet post-1990 compilation.
- UN News (CITES Secretariat announcement, April 2006).
- EUMOFA (European Commission DG MARE), "The Caviar Market — 2021 Edition" (sourced to FAO).
- Tehran Times [state-media-attributed], Financial Tribune, Mehr News Agency — Shilat caviar figures.
- Wikipedia, "Trans-Iranian Railway" (citing Mikiya Koyagi's research).

Full manifests and extraction methods: `data/raw/iran-tobacco-monopoly/*/manifest.json`,
`data/raw/iran-carpet-exports/*/manifest.json`, `data/raw/iran-caviar-exports/*/manifest.json`,
`data/raw/iran-sugar-tea-history/*/manifest.json`.
