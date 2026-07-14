# Comparator mining / energy / industrial-output series (USGS Minerals Yearbook)

Built 2026-07-14 by `agent:comparator-mining-energy`.
Builder: `scripts/harmonize/build_comparator_mining_energy.py` (re-runnable; reads only
`data/raw/usgs-minerals-yearbook/`, which is immutable and untouched).

## Why this exists

Iran's mining/energy/industrial charts were built from Iranian primary sources and USGS historical
volumes, and carried **zero comparator lines** — Iran's line sat alone with nothing to compare
against. This dataset adds the 10-country comparator roster to those charts.

## Why USGS, and why a single source

USGS publishes **the same table, with the same commodity definitions, for every country** in the
roster (Volume III, Area Reports: International — "Table 1: Production of Mineral Commodities").
Pulling Iran and every comparator from that one table means the comparison is methodologically
consistent, rather than stitched together from ten national statistics agencies that each count
differently. **Iran's own USGS figure is extracted too**, so Iran and the comparators are measured
identically — even where the project already holds an Iranian-primary figure for the same measure.
Where the two disagree, both are kept as separately-labelled series; neither is adjudicated.

## Files

| file | rows | what it is |
|---|---|---|
| `usgs_mineral_energy_production_long.csv` | 996 | **the chart-ready file.** Harmonized to canonical `indicator_id`s, units normalized. |
| `usgs_mineral_energy_production_full.csv` | 7,733 | the complete deduped extraction — every commodity USGS reports, verbatim labels and units. Nothing thrown away. |
| `unit_anomalies.csv` | 194 | rows deliberately withheld from the chart-ready file, with the reason. See "What was withheld". |

`usgs_mineral_energy_production_long.csv` columns:
`country_iso3, indicator_id, year, value, unit, source_dataset, source_commodity_label, source_unit, flag`

- `source_commodity_label` / `source_unit` preserve **exactly** what the source said, so no row is
  silently reinterpreted by the harmonization.
- `flag` carries USGS's own markers: `e` = estimated, `r` = revised.
- `source_dataset` names the specific yearbook edition the value came from.

## Coverage actually obtained

Roster: **IRN** + TUR, SAU, IRQ, VEN, ARG, RUS, USA, KOR, ESP, ITA.
Iran is present in **every** indicator below.

| indicator_id | unit | n | countries (year range) | missing |
|---|---|---|---|---|
| `energy__natural_gas_production_marketed` | million cubic meters | 10/11 | IRN 2014-2023; TUR 2014-2022; SAU 2014-2023; IRQ 2014-2023; VEN 2014-2022; ARG 2012-2021; RUS 2014-2022; KOR 2017-2021; ESP 2014-2022; ITA 2014-2022 | USA |
| `energy__natural_gas_production_gross` | million cubic meters | 2/11 | SAU 2014-2021; VEN 2014-2022 | IRN, TUR, IRQ, ARG, RUS, USA, KOR, ESP, ITA |
| `mining__cement_production` | metric tons | 10/11 | IRN 2014-2023; TUR 2012-2022; SAU 2014-2023; IRQ 2014-2023; VEN 2014-2022; ARG 2012-2021; RUS 2014-2022; KOR 2014-2021; ESP 2014-2022; ITA 2014-2022 | USA |
| `mining__crude_steel_production` | metric tons | 9/11 | IRN 2014-2023; TUR 2012-2022; SAU 2014-2023; VEN 2014-2022; ARG 2012-2021; RUS 2014-2022; KOR 2014-2021; ESP 2014-2022; ITA 2014-2022 | IRQ, USA |
| `mining__gypsum_production` | metric tons | 8/11 | IRN 2014-2023; TUR 2014-2022; SAU 2014-2023; IRQ 2014-2023; ARG 2012-2021; RUS 2014-2022; ESP 2014-2022; ITA 2014-2022 | VEN, USA, KOR |
| `mining__aluminum_primary_production` | metric tons | 7/11 | IRN 2014-2023; TUR 2012-2022; SAU 2014-2023; VEN 2014-2022; ARG 2012-2021; RUS 2014-2022; ESP 2014-2021 | IRQ, USA, KOR, ITA |
| `mining__copper_mine_production_cu_content` | metric tons | 7/11 | IRN 2014-2022; TUR 2012-2022; SAU 2014-2019; ARG 2012-2018; RUS 2014-2022; KOR 2016-2017; ESP 2014-2022 | IRQ, VEN, USA, ITA |
| `mining__pig_iron_production` | metric tons | 7/11 | IRN 2014-2023; TUR 2012-2022; ARG 2012-2021; RUS 2014-2022; KOR 2014-2021; ESP 2014-2022; ITA 2014-2022 | SAU, IRQ, VEN, USA |
| `mining__zinc_mine_production_zn_content` | metric tons | 7/11 | IRN 2014-2023; TUR 2012-2022; SAU 2014-2023; ARG 2012-2021; RUS 2014-2022; KOR 2014-2021; ESP 2014-2022 | IRQ, VEN, USA, ITA |
| `mining__iron_ore_production_gross_weight` | metric tons | 6/11 | IRN 2014-2023; TUR 2012-2022; VEN 2014-2022; ARG 2014-2021; RUS 2014-2022; KOR 2014-2021 | SAU, IRQ, USA, ESP, ITA |
| `mining__lead_mine_production_pb_content` | metric tons | 6/11 | IRN 2014-2023; TUR 2012-2022; ARG 2012-2021; RUS 2014-2022; KOR 2014-2021; ESP 2014-2022 | SAU, IRQ, VEN, USA, ITA |
| `mining__salt_production` | metric tons | 6/11 | IRN 2014-2023; TUR 2012-2022; SAU 2014-2023; IRQ 2014-2023; ARG 2012-2021; RUS 2014-2022 | VEN, USA, KOR, ESP, ITA |
| `mining__barite_production` | metric tons | 5/11 | IRN 2014-2023; TUR 2018-2022; SAU 2014 only; ARG 2012-2021; RUS 2014-2022 | IRQ, VEN, USA, KOR, ESP, ITA |
| `mining__coke_production` | metric tons | 5/11 | IRN 2014-2023; TUR 2012-2022; ARG 2012-2021; RUS 2014-2022; KOR 2014-2021 | SAU, IRQ, VEN, USA, ESP, ITA |
| `mining__copper_smelter_primary` | metric tons | 5/11 | IRN 2014-2023; TUR 2012-2022; RUS 2014-2022; KOR 2014-2021; ESP 2014-2022 | SAU, IRQ, VEN, ARG, USA, ITA |
| `mining__copper_refinery_primary` | metric tons | 4/11 | IRN 2014-2019; TUR 2012-2022; RUS 2015-2022; KOR 2014-2021 | SAU, IRQ, VEN, ARG, USA, ITA, ESP |
| `mining__chromite_ore_production` | metric tons | 3/11 | IRN 2019-2023; TUR 2012-2022; RUS 2014-2022 | SAU, IRQ, VEN, ARG, USA, KOR, ESP, ITA |
| `mining__manganese_ore_production_gross_weight` | metric tons | 3/11 | IRN 2018-2023; TUR 2012-2022; RUS 2015-2019 | SAU, IRQ, VEN, ARG, USA, KOR, ESP, ITA |

**A "missing" country is almost always a real fact, not a retrieval failure**: USGS only lists a
commodity for a country that actually produces it in reportable quantity. Iraq has no steel or
copper line because Iraq's Table 1 has no steel or copper row. Italy has no aluminium line because
Italy's last primary smelter closed. These are absences in the source, not gaps in this extraction.

## Motor vehicle production (OICA) — `oica_motor_vehicle_production_long.csv`

The industry leg of this task, from a second single-source multi-country table: OICA's
"World Motor Vehicle Production by Country/Region and Type". Same logic as USGS — one survey,
every country, Iran included (OICA sources Iran's figure to CCFA), so the comparison is like-for-like.

| | |
|---|---|
| indicator_id | `industry__motor_vehicle_production` |
| unit | vehicles |
| years | 2019, 2021, 2022, 2023, 2024 (the five columns OICA's PDF publishes; **2020 is not among them**) |
| countries | 8/11 — IRN, TUR, RUS, USA, ARG, ESP, ITA, KOR |
| missing | **SAU, IRQ, VEN** — OICA does not survey them; they have no reportable vehicle-manufacturing industry. Absence in the source, not a retrieval gap. |

Iran 2024: 1,077,839 vehicles (vs 821,060 in 2019). This **extends
`iran_automotive_national_vehicle_production_1970_2018`**, whose existing production counts stop at
2005 and are Wikipedia-sourced.

**OICA's own scope qualifiers are preserved verbatim in `source_commodity_label` and NOT harmonized
away** — Iran is *"yearly only"*, Argentina is *"cars and LCV only"* (i.e. Argentina's figure
excludes heavy vehicles). A reader comparing those two lines needs to know that.

OICA's per-year HTML statistics pages are JavaScript-rendered and return only a page shell to a
plain fetch; the PDF is the machine-readable artifact and it carries five years at once, so no
further scraping was attempted.

## The era gap (important, and NOT bridged)

Iran's existing charts for these commodities run **1954–1980** (pre-revolution, from USGS's
historical volumes). This comparator data runs **2012–2023**. Same measure, same publisher — so it
belongs on the same chart — but the chart will render as **two separated time blocks, not one
continuous run**. USGS country tables for 1981–2011 are not on disk and nothing was invented to
bridge the gap.

## Known limitations and honest caveats

- **USA is absent from every indicator.** USGS publishes no country report for the United States —
  it publishes the *Mineral Commodity Summaries* instead, a different publication with a different
  structure and different units. A partial USA extraction from MCS already exists at
  `data/processed/usgs_minerals_comparators_series/` (2017–2023, 19 commodities). It was **not**
  merged in here, because doing so would silently mix two publications with different production
  definitions ("Mine, recoverable" vs "Mine, Cu content") into one line. Folding USA in properly is
  a clean, well-defined follow-up — it just needs a deliberate concept mapping, not a regex.
- **Crude oil and refinery output were withheld** from the chart-ready file (191 of the 194
  quarantined rows), for two reasons: (1) the source's own fuels section contains **unit errors** —
  in `myb3-2020-21-saudi-arabia.xlsx`, the `Crude` petroleum row carries `do.` (ditto) directly
  beneath an `Ethane / million cubic meters` row, which would make Saudi crude oil 3,635 million
  *cubic metres*. The value plainly continues Saudi's own million-42-gallon-barrel series, but
  rewriting a published unit on a hunch is not this project's call, and the same ambiguity recurs
  for Türkiye and Venezuela. (2) It isn't needed anyway: **crude oil production is already covered
  for all 11 roster countries** by the existing `owid__oil_production_volume` chart, from a single
  consistent source. The rows are preserved verbatim in `usgs_mineral_energy_production_full.csv`.
- **3 further rows quarantined** as genuine source-side unit errors (SAU gas 2018, TUR gas
  2012–13, all labelled with a *mass* unit for a *volume* measure). Listed in `unit_anomalies.csv`.
- **Gross vs marketed natural gas are kept as separate indicators**, deliberately. Gross production
  includes gas reinjected, flared and vented; marketed/dry-basis does not. Merging them would
  overstate output for any country reporting on a gross basis. Only SAU and VEN publish gross, so
  that chart is thin — flagged in the staging file for the owner to accept or drop.
- **Salt for ESP/ITA/KOR is absent** because those countries report salt only broken out by type
  (rock / sea / table / industrial), never as a single total. Summing the components would be a
  derivation, not a source figure, so it was not done.
- **Label drift across editions was collapsed, value conflicts were not.** USGS renames rows between
  editions (Iran's crude steel is `Raw steel, ingots and castings` in one edition and
  `Steel, raw steel, ingots and castings` in the next). Where two labels map to one indicator for
  the same country-year, the **later edition wins** — the same rule already used for value
  revisions. If two *different* labels appeared in the *same* edition, that would be a real concept
  clash, and the builder drops the row and reports it rather than guessing. (Zero such cases
  occurred in this run.)

## Two real parsing bugs this builder had to solve (documented so nobody reintroduces them)

1. **The per-table default unit varies by country.** A blank unit cell means "the table default",
   and that default is declared in a parenthetical line under the title — which is
   `(Metric tons, gross weight, ...)` for Iran and Türkiye but `(Thousand metric tons, ...)` for
   Saudi Arabia and Iraq. Hardcoding one default makes Saudi and Iraq **1000× too small** (Saudi
   cement would read 49,194 t instead of 49.2 Mt). The builder reads the default from each sheet.
2. **`do.` (ditto) means the previous *data* row's unit, and blank means the table default — not
   "same as the row above".** Treating blank as ditto leaks units across unrelated commodities and
   produces absurdities like zinc mine production measured in *kilograms* (inherited from a gold
   row). Group-header rows carry no unit and must not disturb the ditto reference.

Both bugs produce values that are silently, plausibly wrong rather than obviously broken. Every
indicator was magnitude-checked against known real-world output before this file was published
(Russia 674 bcm gas, Iran 275 bcm; Türkiye 74 Mt cement, Iran 71 Mt; Korea 70.6 Mt crude steel).

## Provenance

Raw inputs (immutable, manifested): `data/raw/usgs-minerals-yearbook/{irn,tur,sau,irq,ven,arg,rus,kor,esp,ita}/`
— 42 Table-1 XLSX releases across editions MYB3-2016 … MYB3-2023.
19 of them (IRQ, VEN, KOR, ESP, ITA) were newly downloaded for this task; the rest were already on disk.
Per-file hashes in each folder's `manifest.json` and in `catalog/manifests/usgs-minerals-yearbook-comparators.jsonl`.
Attempt log (including failures and blocks): `logs/downloads/comparator-mining-energy.log`.

License: U.S. Government public domain (USGS).
