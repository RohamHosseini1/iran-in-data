# Comparator series — Money, Prices, Fiscal & Financial-Sector cluster

Built 2026-07-14 by agent:comparator-monetary-prices, to supply comparator lines (TUR, SAU,
IRQ, VEN, ARG, RUS, USA, KOR, ESP, ITA) for Iranian-primary charts in the Money/Prices/Fiscal/
Financial-sector cluster that currently have Iran's line standing alone. Iran is included in
every file too (same source, so Iran and comparators are measured identically).

Schema (all files): `country_iso3, country_name, indicator_id, indicator_label, year, value,
unit, source_dataset`.

## Files and provenance

| File | Indicator(s) | Source | Re-downloaded? |
|---|---|---|---|
| `broad_money_pct_gdp.csv` | `FM.LBL.BMNY.GD.ZS` — Broad money (% of GDP) | World Bank WDI | No — pulled from already-harmonized `data/processed/macro_wdi.csv` |
| `claims_on_central_government_pct_gdp.csv` | `FS.AST.CGOV.GD.ZS` — Claims on central government, etc. (% GDP) | World Bank WDI | No |
| `credit_to_private_sector_pct_gdp.csv` | `FD.AST.PRVT.GD.ZS` — Domestic credit to private sector by banks (% of GDP) | World Bank WDI | No |
| `cpi_inflation_annual_pct.csv` | `FP.CPI.TOTL.ZG` — Inflation, consumer prices (annual %) | World Bank WDI | No |
| `government_revenue_pct_gdp.csv` | `GC.REV.XGRT.GD.ZS` — Revenue, excluding grants (% of GDP) | World Bank WDI | No |
| `government_expense_pct_gdp.csv` | `GC.XPN.TOTL.GD.ZS` — Expense (% of GDP) | World Bank WDI | No |
| `gfdd_banking_depth.csv` | `GFDD.DI.01`, `GFDD.DI.04`, `GFDD.OI.02`, `GFDD.SI.04` | World Bank Global Financial Development Database (GFDD), pulled live via `api.worldbank.org/v2` | **Yes** — new raw data, see `data/raw/worldbank-gfdd/comparators-monetary-prices-2026-07-14/` |
| `insurance_premiums_pct_gdp.csv` | `GFDD.DI.09` (life), `GFDD.DI.10` (non-life), `GFDD.DI.11` (insurance company assets) | World Bank GFDD, same pull as above | **Yes** |

## Why these indicators

- **Money supply / M2 / monetary base** → `FM.LBL.BMNY.GD.ZS` (broad money, % of GDP) is the
  best cross-country-comparable proxy. WDI does not publish a separate "monetary base" series
  for most countries, so monetary base itself has NO comparator in this pass — only the broad
  money (M2-equivalent) half of `iran_monetary__liquidity_m2_monetary_base_2000_2023` gets a
  comparator line. Levels (Iran's own chart is in billion rials / real 2015 US$) are NOT
  comparable across countries with wildly different economy sizes and currencies, so the
  comparator series is intentionally in a different, normalized unit (% of GDP) — this is
  standard practice, not a fabricated equivalence.
- **Credit to the private sector** → `FD.AST.PRVT.GD.ZS` (WDI) and `GFDD.DI.01` (GFDD) are the
  same underlying concept from two World Bank databases; both included since the existing
  `gfdd__gfdd_di_01` chart specifically cites GFDD as its source and should extend from the
  same database family, not swap to WDI's re-derivation.
- **Government debt to the central bank** → WDI has no indicator specific to "central-bank-only"
  claims. `FS.AST.CGOV.GD.ZS` ("Claims on central government, etc.") is IMF/WDI's broader
  monetary-survey concept — claims on central government held by the WHOLE banking system
  (central bank + deposit money banks), not the central bank alone. This is the closest
  available multi-country proxy but is NOT the same measurement as Iran's CBI-only chart. The
  staging proposal notes this caveat explicitly so it is never presented as an apples-to-apples
  match.
- **Central-government budget revenue/expenditure** → `GC.REV.XGRT.GD.ZS` and
  `GC.XPN.TOTL.GD.ZS` are the IMF Government Finance Statistics (GFS) concepts WDI republishes;
  "Expense" is the standard GFS name for current + capital expenditure (excludes net acquisition
  of nonfinancial assets in some vintages — treat as "total government expenditure" in spirit,
  not a perfectly identical line item to Iran's own Plan & Budget Organization "expenditure/uses"
  classification, which is broader for the SCI "Total Country Budget" chart, see below).
- **CPI / PPI** → `FP.CPI.TOTL.ZG` (headline, all-items CPI inflation) is the only inflation
  series with usable modern coverage across all 11 countries. It is used as a general-inflation
  comparator for BOTH `iran_sci__cpi_urban_vs_rural_general_index_1385_1399` (urban-vs-rural
  split) and `iran_sci1399__cpi_by_coicop_group_1390_1399` (COICOP group split) — clearly
  labeled as all-items headline inflation, NOT a matching urban/rural or COICOP-group breakdown,
  because no source was found publishing a comparable sub-index breakdown for all 10 comparator
  countries. **Producer Price Index (PPI) comparators were NOT obtainable in this pass** — see
  `logs/downloads/comparator-monetary-prices.log` for the IMF/OECD API attempts that failed or
  returned insufficient coverage. WDI's `FP.WPI.TOTL` (wholesale price index) was evaluated and
  rejected as a substitute: coverage is missing entirely for USA/RUS/ARG and stops in the 1990s
  or 2000s for most others, decades before Iran's own PPI chart's 2023 endpoint.
- **Insurance-sector premiums** → `GFDD.DI.09` / `GFDD.DI.10` (life / non-life insurance premium
  volume, % of GDP) directly answer the brief's ask. Genuine World Bank data, newly pulled (not
  previously in this project). `GFDD.DI.11` (insurance company assets, % of GDP) is included as
  a bonus — a related but distinct measure (stock, not premium flow).

## Known gaps (real, not fabricated)

- **Monetary base**: no WDI/GFDD equivalent found for any comparator — chart's monetary-base
  variant stays comparator-less.
- **ESP, ITA**: `FM.LBL.BMNY.GD.ZS` (broad money) has zero WDI observations for these two
  Eurozone members — confirmed via a direct live API re-query (not a harmonization-pull bug).
- **SAU**: `GFDD.DI.04` has zero observations at all (confirmed live).
- **IRQ**: `GFDD.DI.09` / `DI.10` / `DI.11` (all insurance-sector GFDD indicators) have zero
  observations for Iraq (confirmed live) — Iraq gets no insurance-premium comparator line.
- **VEN**: `GC.REV.XGRT.GD.ZS` / `GC.XPN.TOTL.GD.ZS` (government revenue/expense) — zero WDI
  observations.
- **PPI**: unreachable this pass for ALL comparators (see above) — genuinely no comparator line
  proposed for `iran_cbi__ppi_general_and_sectors_1996_2023`.

## Raw source for the two new GFDD pulls

`data/raw/worldbank-gfdd/comparators-monetary-prices-2026-07-14/` (7 raw JSON API responses +
`manifest.json` with sha256 checksums). Fetched directly from `api.worldbank.org/v2`, the same
REST API family already used for this project's WDI harmonization — no scraping, no
third-party mirror.
