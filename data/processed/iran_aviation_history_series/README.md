# Iran civil aviation / Iran Air history series (1913–2007)

Hand-curated, citation-preserving extraction from two sources: an Encyclopaedia Iranica narrative
history of Iranian civil aviation, and an Encyclopedia.com "International Directory of Company
Histories" profile of Iran Air specifically. Harmonized 2026-07-13 from
`data/raw/iran-aviation-history/` (raw sources immutable, unchanged). Nothing was interpolated,
estimated, or fabricated.

## Files

| File | Source raw folder | Coverage | What it covers |
|---|---|---|---|
| `iranair_passengers_employees_revenue.csv` | `encyclopedia-com-iranair-company-history` | 1950–2003 | Annual passengers, employees, revenue (USD), 1958 fleet composition |
| `aviation_events_and_fleet.csv` | `iranica-aviation-history` | 1952–1988 | Iran Air founding capital/workforce, predecessor airline (Iranian Airways) fleet, major accidents, fleet size |

## Schema

`year, metric, value, unit, source, country_iso3` — one row per statistic. All rows are
`country_iso3 = IRN`.

## Key finding preserved in the data

Iran Air passengers: ~142,000 (1961, the merger year immediately preceding Iran Air's Feb 1962
founding) → ~403,000 (1967) → ~800,000 (1972) → 9,500,000 (2000). This fills a genuine pre-1970 gap
in WDI's `IS.AIR.PSGR` series, which only starts in 1970 (715,600, Iran-wide, not Iran-Air-specific).
The 1972 Iran Air figure (~800,000) is broadly consistent with WDI's 1972 Iran-wide figure (894,800)
as a rough cross-check, since Iran Air was the dominant/near-monopoly carrier at the time.

The Iranica article documents the same "boom then rupture" arc seen elsewhere in this harmonization
batch: workforce 700 (1962) → 12,000+ (by 1978/79) and fleet reaching 35 all-jet aircraft carrying
"close to five million passengers a year" by approximately 1978, followed by a sharp post-1979
institutional decline — the 1988 Iran Air Flight 655 shootdown (290 deaths) is the starkest single
data point in the post-revolution rows.

## Caveats

- **`iranair_passengers_employees_revenue.csv` is a tertiary business-reference source** (not a
  primary Iran Air annual report or government statistical yearbook) — flagged as order-of-magnitude
  reliable rather than exact, per `docs/bookkeeping.md` guidance on tertiary sources. Figures are
  transcribed exactly as printed.
- **Sparse, irregular years**, not a continuous annual series (roughly decadal snapshots: 1961, 1967,
  1972, 1975, 1990, 2000–2003).
- **One date is imprecise on purpose:** the "close to five million passengers a year" / 35-jet fleet
  figure in `aviation_events_and_fleet.csv` has no exact year stated in the source; it is placed at
  approximately 1978 and flagged as such in the row's `source` text — do not treat as an exact-year
  data point.
- **Retrieval method:** iranicaonline.org blocks curl/WebFetch (HTTP 403, Cloudflare); the Iranica
  file was retrieved via an interactive browser tool, consistent with other iranicaonline.org
  sources in this project. The Encyclopedia.com file was retrieved directly.

## Sources

- Encyclopedia.com, "IranAir" (International Directory of Company Histories),
  https://www.encyclopedia.com/books/politics-and-business-magazines/iranair — manifest:
  `data/raw/iran-aviation-history/encyclopedia-com-iranair-company-history/manifest.json`
- Encyclopaedia Iranica, "AVIATION" (Abbas Atrvash), https://www.iranicaonline.org/articles/aviation-history/
  — manifest: `data/raw/iran-aviation-history/iranica-aviation-history/manifest.json`
