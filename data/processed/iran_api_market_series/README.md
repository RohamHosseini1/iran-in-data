# Iran Market APIs — Harmonized Series (navasan.tech + brsapi.ir + CBI)

Built 2026-07-14 by agent:iran-market-apis to corroborate and extend three existing charts with
independent market-data sources, per the project owner's instruction: enrich existing charts with
additional source lines rather than spawning duplicate charts for the same measure.

The headline result: **all three target charts previously rested on a single source (TGJU). They now
have a genuinely independent second daily source covering 2019–2026**, and the two providers agree
to within ~0.5% at the median across ~2,000 overlapping days — mutual validation of both.

## Files

| File | Rows | Covers |
|---|---|---|
| `usd_irr_navasan_brsapi_cbi_2026.csv` | 2,530 | USD/IRR **parallel** rate, daily 2019-02-16 → 2026-07-14 (navasan ohlcSearch) + navasan/brsapi latest points; plus one CBI **official**/NIMA anchor (2026-07-14) |
| `gold_coin_bahar_azadi_navasan_brsapi_2026.csv` | 2,564 | Bahar Azadi coin, daily 2019-06-09 → 2026-07-14 + brsapi latest |
| `gold_coin_emami_navasan_brsapi_2026.csv` | 2,564 | Emami coin, daily 2019-06-09 → 2026-07-14 + brsapi latest |
| `global_commodities_brsapi_2026-07-14.csv` | 14 | Global USD spot prices — gold/silver/platinum/palladium oz, Cu/Al/Zn/Pb/Ni, Brent/WTI/gas/RBOB/gasoil. **Reference data only — see below** |

`chart_registry_staging/enrichment_iran_apis.csv` maps the first three onto their target charts
(all `status=extends`; no new charts proposed).

### The commodities file is NOT a chart proposal

brsapi's free tier is latest-snapshot-only, so those 14 rows are **a single point in time each, not
a series**. A chart must be a measure over time — a one-point chart is exactly the kind of thing this
project is culling. They are kept here as reference/seed data: once
`scripts/collect_iran_market_daily.py` (below) has been running for a while they accumulate into real
series and can be revisited then. Nothing in the registry should reference them today.

## Schema

`country_iso3, indicator_id, date, year, value, unit, source_dataset, notes`

`source_dataset` tags every row with its origin (`navasan_ohlcSearch_*`, `navasan_latest_*`,
`brsapi_*`, `cbi_*`) so each source can be shown, filtered, or tracked separately on the chart.

`date` is Gregorian ISO. The APIs report Jalali dates; conversion uses a standard public-domain
algorithm (verified: Jalali 1405-04-23 → 2026-07-14, matching the retrieval date).

## Units — READ THIS BEFORE REUSING THESE FILES

All Iran-side values are in **RIAL**, matching project convention. Getting here required **three
different scale factors**, one of which is a genuine trap:

| Source | Raw unit | × to rial |
|---|---|---|
| navasan `/latest/` — FX fields (`harat_naghdi_sell/buy`, `usd_usdt`) | plain toman | **× 10** |
| navasan `/latest/` — **coin fields** (`bahar`, `sekkeh`) | **thousands of toman** | **× 10,000** |
| navasan `/ohlcSearch/` — **same `bahar`/`sekkeh` field names** | plain toman | **× 10** |
| brsapi (all items with `unit: "تومان"`) | plain toman | **× 10** |
| CBI exrates | already rial | **× 1** |

**navasan uses different scales for the same field name depending on which endpoint you call.** This
is documented nowhere; it was reverse-engineered and then verified empirically.

**Verification (not assumption).** The ×10 scale on the ohlcSearch backfill was checked against the
project's own independent TGJU series across the entire overlap:

| Series | Overlapping days | Median navasan/TGJU | Within ±5% |
|---|---|---|---|
| USD/IRR parallel | 2,006 | **1.0002** | 97.7% |
| Bahar Azadi coin | 1,961 | **0.9955** | 90.8% |
| Emami coin | 1,964 | **0.9999** | 96.1% |

A 10× unit error would have shown up as a ratio of 0.1 or 10. It did not. (The coins' slightly wider
dispersion is expected — coin prices carry a volatile dealer premium over melt value and diverge more
between quoting venues than FX does.)

## Coverage limits — what these sources can and cannot do

- **navasan's archive starts in 2019** (USD: 2019-02-15; both coins: 2019-06-09). Requesting back to
  1380/2001 returns rows beginning only at those dates — that is the true start of coverage, not a
  paging truncation. So navasan **cannot** backfill the Emami chart's 2010–2019 era or the Bahar
  Azadi chart's 2013–2019 era; those remain TGJU-only.
- **navasan `/ohlcSearch/` requires Jalali dates.** Gregorian `start`/`end` silently return an empty
  array `[]` — a success status with no data, not an error. Easy to mistake for "no coverage".
- **brsapi's free tier has no history at all.** `Gold_Currency_Pro.php?history=1|2` returns
  **HTTP 402 payment_required**. Its free endpoints are latest-snapshot-only. This is why the daily
  collector exists.
- **CBI's page is scrapeable but defended.** It renders every number in Persian digits
  (`۱,۳۵۹,۷۱۲`), so ASCII-digit regexes find nothing, and it sits behind an F5/TSPD JavaScript
  bot-challenge that fires intermittently — a bare User-Agent gets challenged, a full browser header
  set passes. Both are handled in the collector. Contrary to expectation it is **not** geo-blocked,
  which means a fuller CBI official-rate history is probably buildable in a future pass.

## Keeping this current: `scripts/collect_iran_market_daily.py`

Polls navasan `/latest/`, brsapi (gold/currency + commodities), and CBI exrates once, and appends a
dated row per (indicator, source) to the CSVs here. **Idempotent** — a `(date, indicator_id,
source_dataset)` triple already present is skipped, so re-running is a no-op and a missed day leaves
a gap rather than corrupting data. Reads keys from `secrets/iran_api_keys.env` (gitignored); keys are
never hardcoded, printed, or written to any file — every URL it logs has the key replaced with
`REDACTED`.

```
python3 scripts/collect_iran_market_daily.py --dry-run   # show what would be appended
python3 scripts/collect_iran_market_daily.py             # collect today
```

Suggested cron (weekdays, after the Tehran market closes):
```
30 12 * * 0-4  cd "/path/to/Iran Economic database" && python3 scripts/collect_iran_market_daily.py >> logs/downloads/iran-market-apis.log 2>&1
```

This is the only route by which brsapi's latest-only data — including the 14 global commodities —
ever becomes a real time series.

## Provenance

Raw API responses backing every row are under `data/raw/navasan-currency/`,
`data/raw/iran-brsapi-tsetmc/`, and `data/raw/cbi-reference-rates/`, each with a `manifest.json`
(source_org, endpoint URL **with the API key redacted**, retrieved_at_utc, sha256, coverage, unit
notes). API keys were read only from `secrets/iran_api_keys.env` and never written to any other file
in this repository.
