# Iran banking-sector history: depth indicators, branch network, nationalization, private re-entry

Harmonized 2026-07-13 from four raw source folders (`data/raw/worldbank-gfdd/
iran-banking-sector-depth-1960-2016/`, `data/raw/iran-banking-history/branch-network-timeseries/`,
`.../nationalization-1979-consolidation/`, `.../private-bank-reentry-2000-2015/`; all immutable,
unchanged) via `scripts/harmonize/harmonize_banking_concessions.py`. Together these span Iran's
banking system from its early 20th-century foreign-concession-bank era through 1979 nationalization
to the post-2000 private-bank re-entry wave.

## Files

| File | Coverage | What it covers |
|---|---|---|
| `worldbank_gfdd_banking_depth_1960_2016.csv` | 1960/61–2016, annual (7 indicators, some starting later) | World Bank Global Financial Development Database (via FRED): private credit/GDP, deposit-money-bank vs. central-bank asset share, liquid liabilities/GDP, central bank assets/GDP, bank deposits/GDP, liquid liabilities level (constant 2000 USD), bank credit/deposits ratio |
| `branch_network_timeseries_1919_2016.csv` | 9 sparse anchor points: 1919, 1940, 1954, 1977, 1978, 1982, 2004, 2005, 2016 | Bank/branch counts, branches-per-million-population, foreign branches |
| `nationalization_1979_consolidation_events.csv` | 1979–1984 (event log, 16 rows) | The 28 May 1979 nationalization decree, Oct 1979 five-bank consolidation (Bank Ma'dan va San'at, Maskan, Keshavarzi, Tejarat, Mellat), which banks continued unmerged (Melli/Sepah/Refah-e Kargaran/Saderat), the sole non-nationalized bank (Bank Iran o Rus), and the 1983-84 Islamic (usury-free) banking law |
| `private_bank_reentry_2000_2025.csv` | 2000–2025 (13 named banks + 2 summary rows for unidentified cohorts) | Post-privatization private bank founding/licensing dates, ending with Ayandeh Bank's 2025 CBI-ordered dissolution/merger into Bank Melli |

## Schema

- `worldbank_gfdd_banking_depth_1960_2016.csv`: `country_iso3, country_name, indicator_id,
  indicator_label, fred_series_id, year, date, value, unit, source_dataset` — standard long format
  matching this project's `macro_wdi.csv` convention. `value` was rounded to 4 decimal places from
  the raw FRED extract's floating-point noise (e.g. `14.218349999999999` → `14.2183`) — no digit of
  actual precision was discarded, this only strips a binary-float representation artifact.
- `branch_network_timeseries_1919_2016.csv`: `year, bank_count, commercial_bank_count,
  specialized_bank_count, branch_count, branches_per_million_population, foreign_branches, notes,
  source` — passed through unchanged (already tidy in the raw file).
- `nationalization_1979_consolidation_events.csv`: `event_date, event_type, description,
  entity_names, source` — event-log format, not a numeric time series.
- `private_bank_reentry_2000_2025.csv`: `bank_name, persian_name_transliteration,
  establishment_year, license_operations_date, notes, source`.

All files' `country_iso3`-equivalent scope is Iran-only (GFDD file has an explicit column; the other
three are Iran-only datasets without the column, since they are event/entity logs, not standard
cross-country indicator series).

## A CSV-quoting defect fixed on the way in (raw untouched)

**`nationalization_1979_consolidation_events.csv`, row for `1982`**: the raw file's `entity_names`
field `"9 banks / 6,581 branches"` had an unescaped comma and was NOT quoted in the original raw
CSV, splitting it into two extra columns on a naive parse. Per `docs/bookkeeping.md` ("raw data is
immutable, fixes happen in `data/processed/`"), `data/raw/iran-banking-history/
nationalization-1979-consolidation/data.csv` was left untouched; this processed copy rejoins the
split text back into one `entity_names` field with the comma restored. No numeric value was altered,
only column alignment. Verified: every row in the processed file now has a uniform column count.

## Caveats — read before charting

- **GFDD is distinct from WDI**: `worldbank_gfdd_banking_depth_1960_2016.csv`'s `GFDD.*` indicator
  codes do NOT appear in this project's `macro_wdi.csv` (WDI's bulk file does not carry Global
  Financial Development Database series) — confirmed via direct check at extraction time, so this
  is genuinely new content, not a duplicate. GFDD Iran coverage stops at 2016 (confirmed a real
  data-availability cutoff, not a download failure — no further updates exist for Iran in this
  database).
- **`branch_network_timeseries_1919_2016.csv` is sparse, snapshot-based, not continuous** — 9 points
  across 97 years. Do not interpolate between them on a chart without labeling the gaps. The
  1977→1982 span brackets the nationalization shock (36 banks/8,275 branches → 9 banks/6,581
  branches) — a real discontinuity, not a data gap, worth annotating explicitly if charted.
  Sourced from Encyclopaedia Iranica's "BANKING i" narrative article
  (`data/raw/encyclopaedia-iranica/banking-i-history-of-banking-in-iran/`), which itself flags a
  confirmed digitization gap: six data tables referenced in the article's prose (Tables 25-30,
  covering Imperial Bank branch/asset detail to 1951, Bank Melli branch counts to ~1940, 1941-44
  money-supply/cost-of-living data, a full 1976 commercial-bank roster, 1954-78 aggregate financial
  data, and special/development banks) were never digitized in either the live HTML or the site's
  own PDF export — only the narrative-prose figures (captured here) survive online. This is a
  genuine source-side gap, not a search failure on this project's part.
- **`nationalization_1979_consolidation_events.csv`** preserves one explicit date discrepancy
  without resolving it: Encyclopaedia Iranica cites the nationalization decree as 28 May 1979, while
  contemporaneous Western press (Washington Post archive, Iran1400.org) reports the takeover
  occurring 8-9 June 1979 — both dates kept, flagged in the row's own description, per this
  project's never-pick-a-winner policy for disagreeing sources.
- **`private_bank_reentry_2000_2025.csv`** has two rows that are explicitly summary placeholders,
  not individual banks (`"(seven unspecified banks)"`, `"(eight unspecified banks)"`) — the 2011
  cohort of 8 new private banks in particular is a confirmed real gap (source states the fact but
  not the individual bank names) — flagged as an open lead for a future continuation pass, not
  fabricated.

## Sources

- World Bank Global Financial Development Database, mirrored via Federal Reserve Bank of St. Louis
  (FRED), release 381.
- Encyclopaedia Iranica, "BANKING i. History of Banking in Iran" (Vahid Basseer),
  iranicaonline.org.
- Wikipedia, "Banking and insurance in Iran."
- Bank Markazi Iran Annual Report 1978 (p.106) and 1980 (publ. 1982, pp.81-82), as cited by Iranica.
- Washington Post archive (1979-06-09 headline); Iran1400.org.
- Al Jazeera, "Corruption, mismanagement in spotlight as Iran dissolves major private bank"
  (2025-10-27, on Ayandeh Bank).
- Individual-bank Wikipedia articles (EN Bank, Karafarin, Parsian, Pasargad, Sarmayeh, Ayandeh) for
  `private_bank_reentry_2000_2025.csv`.

Full manifests and extraction methods: `data/raw/worldbank-gfdd/*/manifest.json`,
`data/raw/iran-banking-history/*/manifest.json`,
`data/raw/encyclopaedia-iranica/banking-i-history-of-banking-in-iran/manifest.json`.
