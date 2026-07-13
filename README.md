# Iran in Data

*Compiled by [Roham Hosseini](https://rohamhosseini.com)* · [iranindata.org](https://iranindata.org)

An encyclopedia-grade collection of Iranian macro- and micro-economic data — from GDP and
inflation down to the price and consumption of chicken and citrus fruit, down further to
household appliance ownership and specific food-item retail prices — spanning as far back as
data exists, from the Pahlavi era through the present, benchmarked against 16 comparator
countries: South Korea, Turkey, Saudi Arabia, Venezuela, the United States, the Soviet Union/
Russia, Spain, Portugal, Greece, Argentina, Germany, France, the United Kingdom, Italy, the
Netherlands, and Sweden. A curated policy/event timeline overlays political and economic shocks
on top of the data.

**End goal:** an interactive, chart-after-chart landing page for researchers, and a dataset that
is just as easy for a script or an AI agent to consume as it is for a person to browse — this is
built as a public good, not a walled garden.

## Start here

- **Looking for a specific chart?** Fetch [`catalog/CHARTS_INDEX.json`](catalog/CHARTS_INDEX.json)
  — a single JSON array covering every chart in the database (~1,790 entries and growing), each
  with its title, category, one-line description, year range, countries, source, citations, and
  the path to its data file. This is the one file a frontend or an AI agent needs to discover
  everything else without crawling thousands of folders.
- **Browsing by topic?** [`catalog/CATEGORIES.json`](catalog/CATEGORIES.json) groups every
  chart_id by category (89 categories — Macro / National Accounts, Agriculture Production,
  Energy, Health, and so on) for a sidebar/nav or a topic-scoped agent query.
- **An AI agent crawling this repo?** Read [`llms.txt`](llms.txt) first — it's a short map of
  the whole project, written for exactly that purpose.
- **Want the methodology?** [`docs/bookkeeping.md`](docs/bookkeeping.md) is the full, mandatory
  set of conventions every download and every chart follows (provenance, source-reliability
  rules, currency/inflation-adjustment methodology, CSV-writing discipline, size limits).

## Directory structure

```
Iran Economic database/
├── README.md              # this file
├── llms.txt                # short AI-agent-readable summary of the whole project
├── SOURCES.md              # the master hunt log — every data source ever found, by round
├── docs/
│   └── bookkeeping.md      # full methodology: provenance rules, source reliability,
│                            # currency/inflation conventions, CSV discipline, size limits
├── data/
│   ├── raw/                 # IMMUTABLE primary sources, exactly as downloaded.
│   │   └── <source-slug>/<dataset-slug>/    # original files + a manifest.json each
│   ├── processed/            # harmonized intermediate data — one row per
│   │   │                      # country/indicator/year, derived from data/raw/ by
│   │   │                      # scripts/harmonize/, never hand-edited
│   │   ├── CHART_REGISTRY.csv    # the master flat index of every chart (~1,790 rows)
│   │   ├── DATA_INVENTORY.md     # human-readable ledger of everything collected
│   │   └── CHART_CATALOG.md      # the content plan, with Pahlavi-era coverage ratings
│   └── charts/               # the FINAL, chart-ready output — one folder per chart_id:
│       └── <chart_id>/
│           ├── data.csv      # country_iso3, country_name, year, value, unit, variant, source
│           └── meta.json     # title, category, sources, n_rows, year_range, countries, citations
├── timeline/                 # curated policy/event CSVs (one per country + a global file),
│                              # each row tagged with economic_domains (fx, oil, trade, ...) so
│                              # it can be mechanically overlaid on the matching chart
├── catalog/
│   ├── CHARTS_INDEX.json     # <-- the master machine-readable index (see "Start here")
│   ├── CATEGORIES.json       # chart_ids grouped by category
│   ├── MANIFEST.jsonl        # file-level download manifest (provenance, not chart content)
│   └── manifests/            # per-source-agent manifest shards, merged into MANIFEST.jsonl
├── downloads/                 # pre-built zip archives for bulk download (see below)
├── scripts/
│   ├── harmonize/             # data/raw/ -> data/processed/ (one script per source)
│   ├── analysis/              # data/processed/ -> CHART_REGISTRY.csv -> data/charts/
│   ├── build_catalog_index.py # data/processed/ + data/charts/ -> catalog/*.json (this layer)
│   └── build_downloads.py     # catalog/*.json -> downloads/*.zip
└── logs/downloads/            # one plain-text log per download/build session, incl. failures
```

**How the three data layers relate:** `data/raw/` is the primary source, never touched again.
`data/processed/` harmonizes it into long, tidy CSVs (one row per country/indicator/year) plus
`CHART_REGISTRY.csv`, the master list of every distinct chart concept. `data/charts/` is the
final materialization of that registry — one small, self-contained folder per chart, ready to
hand directly to a frontend chart component. `catalog/` sits on top of all of it as the
discovery layer described above.

## Finding a chart

Two equivalent ways:

1. **Machine-readable:** fetch `catalog/CHARTS_INDEX.json`, filter by `category`, `primary_source`,
   `countries`, or search `title`/`description`, then follow that entry's `data_path` to load the
   actual `data.csv`.
2. **By hand:** browse `data/charts/<chart_id>/` directly — chart_ids are namespaced by source
   (`wdi__...`, `faostat__...`, `owid__...`, `pahlavi__...`, `iran_census__...`, etc.), so
   `data/charts/wdi__NY.GDP.PCAP/` is Iran-and-comparators GDP per capita from the World Bank's
   WDI, for example. Every chart folder has exactly two files: `data.csv` (the data) and
   `meta.json` (title, category, source, year range, countries, row count, citations).

As of this catalog build, `catalog/CHARTS_INDEX.json` covers every row in
`data/processed/CHART_REGISTRY.csv`; entries whose `data/charts/<chart_id>/` folder doesn't
exist yet (an archival-source materialization pass was still landing at build time) are marked
`"materialized": false` with `data_path`/`row_count`/`year_range`/`countries` left `null` rather
than guessed — re-run `scripts/build_catalog_index.py` to pick up newly materialized charts.

## Bulk download

- **Everything:** `downloads/iran-economic-database-all-charts.zip` — every materialized chart's
  `data.csv` + `meta.json`, one zip.
- **By category:** `downloads/by-category/<category-slug>.zip` — e.g. `energy.zip`,
  `health.zip`, `agriculture-production.zip`. See `downloads/MANIFEST.json` for the full list
  with chart counts and sizes.
- **One chart:** no packaging needed — `data/charts/<chart_id>/` is already a self-contained
  folder of two small files; download it directly (e.g. via GitHub's "download folder" or a
  raw-file fetch) without needing a zip at all.

Regenerate all of the above any time with `python3 scripts/build_downloads.py` (reads
`catalog/CHARTS_INDEX.json` / `CATEGORIES.json`, so run `scripts/build_catalog_index.py` first
if the registry or `data/charts/` has changed).

## Country set

Primary: Iran (IRN). Comparators: South Korea (KOR), Turkey (TUR), Saudi Arabia (SAU),
Venezuela (VEN), United States (USA), Soviet Union/Russia (SUN/RUS), Spain (ESP), Portugal (PRT),
Greece (GRC), Argentina (ARG), Germany (DEU), France (FRA), UK (GBR), Italy (ITA),
Netherlands (NLD), Sweden (SWE).

## Provenance & citation conventions

Nothing enters this repository without a manifest recording where it came from, when it was
retrieved, and its SHA-256 (`data/raw/<source>/<dataset>/manifest.json`). Raw data is never
edited — fixes happen downstream in `data/processed/`. Every chart in `data/charts/` carries its
real source(s) in `meta.json`'s `citations` array (`source_org`, `source_url`, `access_date`),
copied through unmodified into `catalog/CHARTS_INDEX.json`'s `citations` field — a consumer of
the catalog never has to go hunting for where a number came from. Full conventions, including
the source-reliability/neutrality policy and the currency & inflation-adjustment methodology,
are in `docs/bookkeeping.md`.

## Source reliability

See `docs/bookkeeping.md` § "Source reliability & neutrality principles" for the full policy.
Short version: no viewpoint-based filtering of legitimate statistics — government agencies,
central banks, and multilateral institutions are used regardless of perceived political lean.
A small number of outlets with documented records of political fabrication (MEK/NCRI-affiliated
outlets, regime-serving IRGC propaganda sites, and historical militant-party outlets) are
excluded as *data sources* specifically, on fabrication grounds, not politics. Contested
estimates (e.g. bonyad share of GDP) are recorded as a full range with each source attributed,
never resolved to one cherry-picked number.

## License & attribution

This project is dual-licensed:

- **Code** (`scripts/` and other source files) — [MIT License](LICENSE).
- **Data** (`data/`, `catalog/`, `timeline/`, `downloads/` — the harmonized, deduplicated,
  chart-ready compilation itself) — [Creative Commons Attribution 4.0 International (CC BY 4.0)](LICENSE-DATA).
  Free to use, share, and adapt, including commercially, with attribution to
  [Roham Hosseini](https://rohamhosseini.com) / Iran in Data ([iranindata.org](https://iranindata.org)).

The underlying data is pulled from many original sources that carry their own terms (World Bank
WDI, FAOSTAT, IMF, OECD, national statistical agencies, declassified US government documents,
academic papers, and others — see `SOURCES.md` and each dataset's own `manifest.json` /
`meta.json` citations for the specific source). This project's CC BY 4.0 license covers the
compilation, harmonization, deduplication, and derived-value work (e.g. the real/USD currency
conversions) — it does not re-license the original upstream data. Check a chart's own citation
before redistributing it at scale if the upstream source has its own restrictions.
