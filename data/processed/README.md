# Processed Data — the chart-feeding layer

Everything here is derived from `data/raw/` by scripts in `scripts/harmonize/`. Nothing here
is a primary source — if a number looks wrong, the fix goes in the harmonize script, and the
raw file stays untouched (per `docs/bookkeeping.md`: raw data is immutable).

## Schema (shared by every file except the FAOSTAT ones, which add a couple of fields)

| column | notes |
|---|---|
| `country_iso3` | ISO3, restricted to this project's country set (see `scripts/harmonize/country_crosswalk.py`) |
| `country_name` | display name |
| `indicator_id` | stable identifier — pass this straight to a chart's series key |
| `indicator_label` | human-readable label |
| `year` | integer |
| `date` | `YYYY-01-01`, for tools that want a real date column |
| `value` | numeric, as a string in the CSV (cast on load) |
| `unit` | where the source provides one |
| `source_dataset` | maps back to a `data/raw/<source_dataset>/` folder |
| `source_file` | the specific raw file this row came from |

FAOSTAT files additionally carry `item` and `element` (FAOSTAT's own two-level taxonomy —
e.g. item="Meat of chickens, fresh or chilled", element="Production") since collapsing those
into `indicator_label` alone would lose queryable structure.

## Files in this pass

| file | rows | source | covers |
|---|---|---|---|
| `macro_wdi.csv` | 714,025 | World Bank WDI | all ~1,600 WDI indicators, our countries, 1960– |
| `macro_imf_weo.csv` | 34,166 | IMF WEO Apr 2026 | macro aggregates + 5yr forecast, `is_actual` flag marks forecast vs actual |
| `owid_indicators.csv` | 52,103 | Our World in Data | 28 curated series (chicken/poultry, citrus, meat, energy, demographics, macro) |
| `agriculture_qcl_production.csv` | 372,396 | FAOSTAT QCL | crop & livestock production, ALL items, our countries, 1961– |
| `agriculture_fbs_food_balances.csv` | 397,647 | FAOSTAT FBS | per-capita food supply (consumption proxy), 2010– |
| `agriculture_fbsh_food_balances_historic.csv` | 972,688 | FAOSTAT FBSH | per-capita food supply, 1961–2013 |
| `agriculture_pp_producer_prices.csv` | 210,661 | FAOSTAT PP | farm-gate producer prices, 1991– |
| `agriculture_pa_prices_archive_pre1991.csv` | 27,231 | FAOSTAT PA | farm-gate producer prices, 1966–1990 (fills the PP gap) |
| `food_cpi_faostat.csv` | 15,666 | FAOSTAT CP | food consumer price indices, 2000– |
| `macro_maddison.csv` | 9,018 | Maddison Project 2023 | GDP per capita + population, **year 1 AD–2022** — the deepest series in the project |

**~2.8 million rows total, 690MB.** To find Iran's chicken production: filter
`agriculture_qcl_production.csv` to `country_iso3=IRN` and `item` containing "chicken".

## What's NOT harmonized yet

This is a first pass covering the 4 richest, most-structured sources (WDI, IMF WEO, OWID,
FAOSTAT) — roughly 9 of the ~68 raw source folders. **Not yet harmonized**, in rough priority
order for a follow-up pass:

- **USDA PSD, WFP food prices** — the other core food-micro sources (already tidy-ish, should be a quick add)
- **BIS, UNSD AMA, ILOSTAT, OECD, WID.world, SWIID** — multilateral aggregators, mostly SDMX/CSV, straightforward
- **Comparator national sources** (SAMA, TurkStat, KOSIS, BCV, CBI, SCI, INDEC, BCRA) — each has its own format, needs one parser per source
- **Energy** (JODI, OPEC ASB, Energy Institute) — mixed formats, JODI especially will need real work (51 per-year CSVs)
- **PDF-only sources** (CIA reports, FRUS, Encyclopaedia Iranica, GAIN reports, policy docs) — these feed the *narrative*, not chartable series; not really harmonize-pipeline candidates, better used for direct citation
- **Historical pre-1991 sources** (Maddison, Clio Infra, Bharier/Issawi-era, Soviet yearbooks) — will need bespoke handling given inconsistent formats and, for the Soviet yearbooks, OCR/manual extraction from scanned PDFs
- **Owid energy/co2 "panel" files** — wide-by-indicator shape, deliberately skipped by `harmonize_owid.py`, need their own script

## Hand-curated narrative series (separate from the big-melt files above)

Alongside the large indicator-melt CSVs, this folder also holds small, per-topic, hand-curated
series extracted from narrative/citation-heavy sources (Encyclopaedia Iranica articles, trade press,
compiled news reporting) that don't fit the "melt one big source CSV" pattern above. Each has its
own README documenting exact provenance, retrieval method, and caveats:

- `iran_data_portal_deep_series/` — inflation, employment, housing (Iran Data Portal / CBI / SCI / MPO)
- `iran_telecom_communications_series/` — post, telegraph, telephone, radio, TV (1858–1990)
- `iran_media_history_series/` — cinema, press/periodicals (1898–1988)
- `iran_aviation_history_series/` — Iran Air / civil aviation (1913–2007)
- `iran_white_revolution_corps_series/` — Literacy/Health/Extension corps (1920–2003)
- `specialty_goods_series/` — tobacco, carpets, caviar, sugar, tea state-monopoly/export series (1890–2025)

See `DATA_INVENTORY.md` for the complete ledger (including what's still raw-only, marked **[R]**).

## Re-running

Each `scripts/harmonize/harmonize_*.py` is idempotent (safe to re-run; it overwrites its own
output file). Run from the project root: `python3 scripts/harmonize/harmonize_wdi.py`, etc.
All country-set logic lives in `scripts/harmonize/country_crosswalk.py` — add a country there
once and it's picked up everywhere (add its FAOSTAT Area-name mapping too, since FAOSTAT uses
full names, not ISO3, in its raw files).
