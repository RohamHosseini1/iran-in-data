# Bookkeeping Conventions — Iran Economic Database

Every byte of data in this repository must be traceable back to where it came from,
when it was retrieved, and by whom. These rules are mandatory for every download,
whether done by a human or an agent.

## Folder layout

```
Iran Economic database/
├── README.md                  # project overview
├── SOURCES.md                 # master source catalog (the hunt log — every source ever found)
├── data/
│   ├── raw/                   # files EXACTLY as downloaded. Never edited, never renamed after landing.
│   │   └── <source-slug>/     # one folder per source organization/database
│   │       └── <dataset-slug>/
│   │           ├── <original files>
│   │           └── manifest.json
│   └── processed/             # cleaned/derived data (later phase; always references raw inputs)
├── catalog/
│   ├── MANIFEST.jsonl         # merged master index — one JSON line per downloaded file
│   └── manifests/             # per-agent manifest shards: <source-slug>.jsonl (merged into MANIFEST.jsonl)
├── timeline/                  # curated policy/event datasets (CSV + citations)
├── logs/
│   └── downloads/             # one log file per download agent/session
└── docs/
    └── bookkeeping.md         # this file
```

## Source slugs (kebab-case, stable forever)

Examples: `worldbank-wdi`, `worldbank-pinksheet`, `imf-weo`, `imf-ifs`, `faostat`,
`usda-fas-psd`, `wfp-vam`, `maddison-project`, `penn-world-table`, `owid`,
`cbi-iran` (Central Bank of Iran), `sci-amar` (Statistical Centre of Iran),
`iran-open-data`, `iran-data-portal`, `energy-institute`, `opec-asb`, `jodi`,
`ilostat`, `unsd`, `eurostat`, `kosis-korea`, `turkstat`, `sama-saudi`, `gastat-saudi`,
`bcv-venezuela`, `ovf-venezuela`, `un-comtrade`, `bis`, `sanctions-timeline`.

## Rules for raw data (`data/raw/`)

1. **Immutable.** Once a file lands in `data/raw/`, it is never edited, reformatted, or renamed.
   Fixes happen in `data/processed/`.
2. **Original filenames** are kept. If the server gives a meaningless name (e.g. `download.php`),
   rename AT DOWNLOAD TIME to `<dataset-slug>_<yyyy-mm-dd>.<ext>` and record the original name
   in the manifest.
3. **One `manifest.json` per dataset folder** (schema below). No dataset folder without a manifest.
4. **No fabricated data.** If a download fails, the failure is logged; nothing is hand-created
   inside `data/raw/`.
5. Curated/hand-compiled datasets (e.g. policy timelines) live in `timeline/` or
   `data/processed/`, never in `data/raw/`, and every row must carry a source citation.

## `manifest.json` schema (one per dataset folder)

```json
{
  "dataset_id": "faostat-qcl-production",
  "title": "FAOSTAT Production — Crops and Livestock Products",
  "source_org": "FAO",
  "source_url": "https://www.fao.org/faostat/en/#data/QCL",
  "download_url": "https://bulks-faostat.fao.org/production/....zip",
  "retrieved_at_utc": "2026-07-12T18:30:00Z",
  "retrieved_by": "agent:faostat-download",
  "files": [
    {"name": "....csv", "original_name": null, "sha256": "…", "bytes": 12345678}
  ],
  "countries": ["IRN", "KOR", "TUR", "SAU", "VEN", "DEU", "FRA", "..."] ,
  "time_coverage": "1961–2024",
  "frequency": "annual",
  "topics": ["agriculture", "production", "chicken", "citrus"],
  "units": "described in file / codebook",
  "license_terms": "CC BY-NC-SA 3.0 IGO (FAO)",
  "notes": "Anything a future user must know: quirks, filters applied, API params.",
  "failures": []
}
```

## Per-file catalog shards (`catalog/manifests/<source-slug>.jsonl`)

Each agent appends ONE JSON line per downloaded file to its OWN shard file
(never to a shared file — avoids interleaved writes):

```json
{"path": "data/raw/faostat/qcl-production/x.csv", "source": "faostat", "dataset_id": "faostat-qcl-production", "download_url": "…", "retrieved_at_utc": "…", "sha256": "…", "bytes": 123, "topics": ["agriculture"]}
```

Shards are merged into `catalog/MANIFEST.jsonl` by the coordinator.

## Download logs (`logs/downloads/<agent-name>.log`)

Plain-text, timestamped (UTC) log of every attempt: URL tried, HTTP status, bytes,
outcome, and any errors or blocks (e.g. geo-restrictions on Iranian government sites).
Failures are data too — log them.

## Source reliability & neutrality principles

1. **No viewpoint-based filtering of legitimate statistical sources.** Government statistics
   agencies, central banks, multilateral institutions (World Bank/IMF/FAO/UN/OECD/BIS/ILO), and
   peer-reviewed academic economic history are used regardless of any perceived political lean —
   a chicken-production number in FAOSTAT is not ideologically inflected, and treating it as if it
   were would make the database *less* trustworthy, not more.
2. **Excluded as data sources:** organizations with documented records of political fabrication
   or propaganda in their factual output, from any point on the spectrum. Currently: MEK/NCRI and
   its outlets (ncr-iran.org, iranfocus.com, mojahedin.org, and similar); Islamic Republic
   regime/IRGC-affiliated propaganda outlets when the claim is regime-serving rather than a
   routine official statistic (Fars News/Tasnim editorializing, IRGC-run "news" sites); and
   historical militant-party outlets — Tudeh Party and Fadaian (Cherikha-ye Fadai-ye Khalq)
   affiliated publications. This is source hygiene, not a left/right screen — the same standard
   applies to any outlet, of any political stripe, with a comparable record of fabrication or
   advocacy-driven numbers. It does NOT extend to a party's or movement's own documented history
   (e.g. Tudeh's role in 1940s-53 labor organizing is fine as *narrative* history from independent
   historians) — the exclusion is specifically about using their own outlets as a *data source*.
   If a claim from any excluded outlet seems important, verify it independently via a primary/
   official source before it enters the database; never cite the advocacy outlet directly.
3. **For the policy-timeline / narrative layer specifically** (where interpretation genuinely
   varies among historians), prefer primary documents and contemporaneous official reporting —
   government texts, laws, IMF/World Bank staff reports, State Department FRUS volumes,
   declassified CIA economic assessments — over secondary ideological narrative. Where an estimate
   is genuinely contested (e.g. bonyad share of GDP, ranging 4%–65% across sources), record the
   full range with each source attributed rather than picking one number.
4. State-controlled media (PressTV, Tehran Times, etc.) may be used for official figures/quotes
   but must be labeled as state-media-attributed and cross-checked against WDI/FAOSTAT/independent
   data wherever an independent series exists.

## CSV-writing discipline

Multiple independent agents across the 2026-07-13 final-round batch each independently discovered
and fixed the *same* bug class in files written by earlier agents: unescaped commas/quotes inside a
`metric`/`title`/`source_name` field, written by hand-built string concatenation instead of Python's
`csv` module, silently misaligning columns on read. **Always write CSV/TSV output via `csv.writer` or
`csv.DictWriter`** (or an equivalent library in another language) — never build a comma-joined string
by hand, even for a "simple" one-off file. This has now caused real, silent data corruption more than
once; treat it as a hard rule, not a style preference.

## Currency & inflation-adjustment conventions

Per the project owner's explicit instruction (2026-07-13): every currency chart should be displayable
in **US dollars**, with a toggle between **inflation-adjusted (real, default) and nominal (not
adjusted)**. The raw/nominal recorded value is NEVER overwritten — real and USD-converted values are
always computed as ADDITIONAL variant series alongside the original, never a replacement.

**Methodology (mirrors the World Bank's own "constant US$" convention, for consistency with the WDI
data we already have — don't invent a different one):**
1. Deflate in LOCAL currency first, using that country's own CPI/GDP-deflator, to a fixed base year.
   Do NOT deflate by US inflation after converting to USD — that conflates domestic inflation with
   exchange-rate movements, which for Iran especially (large gap between domestic CPI and rial
   depreciation, multi-tier FX system) would badly distort the result.
2. Convert the deflated (real, base-year) local-currency value to USD using the exchange rate **at
   the base year**, not the exchange rate in the value's original year. (Converting at the original
   year's rate, then deflating, is a different and NOT-equivalent calculation — don't mix the two.)
3. **Base year: 2015** — matches WDI's own "constant 2015 US$" vintage already present throughout our
   WDI pull, so project-computed real series are directly comparable to WDI's native ones rather than
   introducing a second, incompatible base year.
4. **Exchange rate source, Iran — CORRECTED 2026-07-13 per explicit user instruction**: the official
   rate is only used for the **Pahlavi era (pre-1979)**, when it was genuinely close to the market
   rate (convertible economy, no sanctions/capital controls). **For the Islamic Republic era
   (1979-present), use the PARALLEL/BLACK-MARKET rate, never the official rate** — the user's own
   words: "the government official tiers are not really applicable cause they are scarce and never
   available to most of public and any of the private sector." Multi-tier official rates
   (sometimes 10+ concurrent rates) are a real thing in Iran's post-1979 system but they don't
   reflect what an ordinary transaction actually costs.
   - Pre-1979: WDI `PA.NUS.FCRF` (1960-1978) + IMF IFS `exchange_rate_official` (1937-1949).
     **1950-1959 remains a known gap** — do not fabricate; leave blank.
   - 1979-present: parallel-market rate **wherever the official and market rates genuinely diverged**
     — which is most of this era, but not literally 100% of it (see the 2002-2010 exception below).
     **1979-2003 (monthly) is CLOSED**: Bahmani-Oskooee (2005, Iranian Economic Review Vol.10 No.14,
     Table 4) is a single peer-reviewed academic source giving a complete monthly black-market
     rial/USD series January 1947-December 2003, sourced to the World Currency Yearbook (through
     mid-1989) and directly to the Central Bank of Iran itself (mid-1989 onward) —
     `data/raw/iran-parallel-fx-1979-2010-research/`. **2004-2010 (annual) is CLOSED AND
     PRIMARY-SOURCED**, updated 2026-07-13: originally filled via a Wikipedia transcription of CBI's
     own "Annual Review 2013/14" (one hop removed); a follow-up round found CBI's own daily
     "Exchange Rates Statistics" page (cbi.ir/ExRates) via 40 Wayback Machine snapshots (Dec
     2005-Oct 2010) plus 6 IMF Article IV Consultation/Statistical Appendix reports, and
     cross-validated both against this project's own WDI/IMF-IFS official-rate series for the
     genuinely-unified window below. Result: 2005/2006/2009/2010 confirmed as originally recorded;
     **2004, 2007, and 2008 were corrected** (2004: 8,885→8,615; 2007: 9,408→9,280; 2008:
     9,143→9,421) — the 2008 error in particular had produced a nonsensical *negative* black-market
     premium (parallel rate below official) in `fx__official_vs_parallel_gap_irn`, the tell that
     first flagged it. See `data/raw/iran-cbi-imf-fx-verification-2004-2010/manifest.json` for the
     full year-by-year evidence. **2011-2026**: daily TGJU parallel-market data, verified correctly
     denominated in Rial (not Toman — TGJU's own page states "واحد پولی: ریال" and the live rate
     cross-checked against a fresh web search matched our file's most recent entries almost exactly).
   - **2002-2010 exception**: the March 2002 unification reform genuinely merged the official and
     market rates for this window — confirmed by multiple sources describing it as a single
     "unified, market-driven" rate with no separate black-market rate reported, and by the
     2026-07-13 verification round finding the official and CBI-primary parallel rates agree within
     0.1-0.5% every year 2004-2010. Using WDI's official `PA.NUS.FCRF` for this window reflects what
     people actually paid, not a shortcut around the black-market rule. Real divergence resumes
     ~2010-2011 as sanctions escalate (our own 2011 TGJU data already sits above the pre-2010 trend,
     consistent with this).
   - **Rial vs. Toman**: Iran's official currency is the Rial; colloquially and in much day-to-day
     market quoting (street exchanges, some financial sites) prices are given in **Toman = 10 Rials**.
     Verify which unit a source actually uses before trusting a number — check the source's own
     stated unit (e.g. TGJU explicitly labels "ریال" vs "تومان") rather than assuming from context,
     and sanity-check the magnitude against a known reference point. Getting this wrong silently
     produces a value off by exactly 10x.
   - Never blend official and parallel rates into one series — if both exist for an overlapping
     period, keep them as clearly labeled separate series (the divergence between them is itself
     meaningful data, e.g. the multi-tier system's actual premium).
5. **CPI/deflator source, Iran**: WDI `FP.CPI.TOTL` (2010=100) for 1960-2025; the Bank Melli/CBI-
   sourced `data/processed/iran_data_portal_deep_series/inflation_rate_1937_2014.csv` for earlier
   years. Different eras' price indices use different base years/methodologies and are NOT rescaled
   into one continuous index (same "present as labeled segments, never force-splice" rule already
   used for the CPI chart itself) — the deflation math still works fine year-by-year even though the
   underlying index isn't one continuous series, since only year-over-year ratios matter for deflating
   a single value to the 2015 base.
6. **Comparator countries**: use each country's own WDI `PA.NUS.FCRF`-equivalent and `FP.CPI.TOTL`
   for the WDI-covered era (this comes for free — the "constant US$" variant already exists on most
   WDI currency charts). Pre-WDI-era comparator currency data (Tsarist rubles, pre-EU escudos/
   pesetas, etc.) is NOT converted unless a real, sourced historical exchange-rate + price-index pair
   is found — do not fabricate a rate for eras where we don't have one. Flag as a known gap instead.
   **IMPLEMENTED 2026-07-13**: `build_fx_cpi_lookup.py`'s `main_comparators()` builds one
   `data/processed/fx_cpi_lookup_<iso3>.json` per comparator (KOR, TUR, SAU, VEN, USA, RUS, ARG,
   ESP, PRT, GRC, DEU, FRA, GBR, ITA, NLD, SWE), and `build_currency_variants.py`'s `process_wdi()`
   now loops every country, not just Iran. Three real nuances found and handled, not glossed over:
   - **Venezuela and Argentina** get the same "prefer a real parallel/black-market rate over the
     official one" treatment Iran gets, because a genuine, well-documented divergence exists and
     this project already has real sourced data for it — Venezuela's CADIVI/CENCOEX/DICOM official
     tiers vs. a black-market rate that reached ~100x official at points (2012-2020, from
     `venezuela_parallel_fx_rate_milestones_2003_2020.csv`); Argentina's "cepo cambiario"
     capital-control-era official/"blue" gap (2011-2026, from a previously-unparsed ArgentinaDatos
     raw JSON dump). All other comparators use WDI's official rate outright — no equivalent
     documented problem for them in this project. Argentina also needed a CPI substitute (WDI's
     `FP.CPI.TOTL` has zero ARG rows) built from the independent Cavallo-Bertolotto academic CPI
     reconstruction chained onto IMF WEO's actual PCPI; Venezuela's WDI CPI (2008-2016 only) was
     likewise replaced by IMF WEO's much more complete actual-PCPI series rather than spliced.
   - **Eurozone comparators (DEU, FRA, ITA, ESP, PRT, NLD, GRC)**: WDI's `PA.NUS.FCRF` is NOT
     retroactively restated across each country's Euro changeover (confirmed by inspection — e.g.
     Germany's own series jumps from ~1.76 Deutsche-Mark-per-US$ in 1998 to ~0.94 EUR-per-US$ in
     1999 with no rescale). Left as-is, this would silently divide a pre-Euro-national-currency
     figure by a Euro figure in the base-year ratio formula — a real correctness bug, not a gap.
     Fixed by rescaling every pre-Euro year to EUR-equivalent using the EU's own permanently fixed
     (irrevocable) national-currency-per-EUR conversion rates — exact historical facts, not an
     estimate. (Venezuela's and Russia's own currency redenominations, by contrast, WDI already
     restates continuously on inspection — no equivalent fix needed there.)
   See `logs/downloads/currency-extension-comparators-archival.log` for the full trail.
7. Every computed (non-source-native) real/USD variant gets a `computed: true` flag and a `notes`
   field naming the exact exchange-rate and CPI series used, so it's auditable — never presented as
   if it were itself a primary-sourced number.

## Size discipline

- Skip any single file > 500 MB unless explicitly approved; note it in the log + SOURCES.md instead.
- Prefer country-filtered API extracts over "all data" monster dumps when the filtered
  extract covers our countries fully.
- Target set of countries (ISO3): IRN (primary) · KOR, TUR, SAU, VEN, USA, RUS/SUN (USSR), ESP, PRT, GRC
  (core comparators) · DEU, FRA, GBR, ITA, NLD, SWE (broader European reference)
  (keep world/all-country files when they are the natural download unit — they enable adding comparators later).

## Integrity

- `sha256` computed at download time (`shasum -a 256`).
- `retrieved_at_utc` from `date -u +%Y-%m-%dT%H:%M:%SZ`.
- Nothing is deleted. Superseded downloads get a new dataset folder with a date suffix.

## Chart-ID stability policy

Once this project is public (git history exists, CC BY 4.0 license is live, iranindata.org is a real
domain), `chart_id` values in `CHART_REGISTRY.csv` and `data/charts/<chart_id>/` must be treated as
**stable public identifiers** — the same status as a URL. External citations, bookmarks, embeds, and
any AI agent that fetched `catalog/CHARTS_INDEX.json` may reference a `chart_id` directly.

- **Never rename or delete a `chart_id`** once it has appeared in a committed/published state, even if
  a later pass finds a better title or a cleaner category for it. Fix the `title`/`category`/`notes`
  fields freely — those are metadata, not identity.
- If a chart genuinely needs to be split (e.g. a bundled multi-commodity table found to actually be
  several distinct series) or merged (a duplicate discovered later), do NOT just delete the old
  `chart_id` — add a `superseded_by` / `merged_into` field pointing at the replacement(s), and keep the
  old chart_id's folder as a redirect-style stub (a `meta.json` with a pointer, not a 404). This is the
  same principle as an HTTP redirect: cheap to do right, expensive to fix after the fact once external
  links exist.
- New `chart_id`s can always be added freely — this policy only constrains renaming/removing ones that
  already exist.

## Versioning & changelog

- `CHANGELOG.md` at the repo root (create if missing) tracks changes that matter to a re-user or
  citer: new chart categories, methodology changes (e.g. the 2026-07-13 FX-rate policy correction —
  official vs. parallel-market rate by era), major data-quality fixes (e.g. the citation-accuracy
  audit), and schema changes to `CHART_REGISTRY.csv` or the `data/charts/` format. Routine new-data
  additions within an existing category/methodology don't need a changelog entry — this is for
  changes that could affect how someone interprets or re-uses already-published data, not a running
  commit log (git history already covers that).
- Each `data/charts/<chart_id>/meta.json` should carry a `last_updated` date (the date its data.csv
  was last regenerated) once the materializer scripts are next touched — not required retroactively
  for the current batch, but add it going forward so a re-user can tell freshness at a glance without
  cross-referencing git history.
- Tag meaningful public milestones in git (e.g. `v1.0` for the first public release) once this repo
  has a remote and the frontend work begins — not needed yet for the local-only repo.
