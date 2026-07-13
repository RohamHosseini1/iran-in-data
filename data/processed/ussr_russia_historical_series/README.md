# USSR / Russia historical series (1858–1990)

Extracted 2026-07-13 from a previously-downloaded-but-unmined PDF trove at
`data/raw/ussr-russia-historical/` (27 files, 3 dataset folders — all
immutable, unchanged by this pass). Method: `pdftoppm -png -r 200..400`
render of target pages, read visually, cross-checked against
`pdftotext -layout` where a text layer existed; illegible or ambiguous
digits are left **blank**, never guessed. This is a comparator-country-only
addition (USSR/Russia is one of this project's core comparators for the
Iranian command-economy and Cold-War-era comparisons) — there is no Iran
data in this folder.

## The three eras — read this before charting anything

This folder deliberately spans three methodologically incompatible regimes.
**Do not merge series across the `era` boundary without noting it**:

1. **Tsarist / Imperial Russia (`imperial_russia_*.csv`, 1858–1910)** —
   pre-Soviet baseline. Official statistics of the Central Statistical
   Committee, Ministry of Internal Affairs, Imperial Russia. Population,
   trade. Genuinely rare pre-1917 comparator data.
2. **Soviet Union (`narkhoz_*.csv` and `cia_soviet_*.csv`, 1913–1990)** —
   two independent and *known-to-diverge* measurement traditions, both kept
   here as separate series per this project's neutrality policy
   (`docs/bookkeeping.md` §"Source reliability & neutrality principles"),
   never resolved to one cherry-picked number:
   - `narkhoz_*` = **official Soviet statistics** (Narodnoe khozyaistvo SSSR,
     published by the state statistical agency TsSU/Goskomstat). Soviet
     planned-price/index-number methodology is well documented to inflate
     real growth relative to Western reconstructions — a measurement issue,
     not a claim of dishonesty.
   - `cia_soviet_*` = **CIA/US-government dollar-and-ruble-cost
     reconstructions** of the same Soviet economy, using Western national-
     accounts (GNP) methodology. Directly analogous to this project's
     existing CIA Iran assessments (NIS-33 etc.) and the project's stated
     preferred source type for this purpose.
   Where the two measure the same concept for an overlapping year (e.g.
   national-income/GNP growth in the mid-1980s), **both are recorded, not
   merged** — see `cia_soviet_gnp_growth_and_defense_narrative.csv` for an
   explicit Soviet-official-vs-CIA side-by-side.
3. **Modern Russia (post-1991)** — **already covered** by this project's
   existing WDI/IMF WEO/Maddison macro series (`data/processed/macro_wdi.csv`
   etc., country code RUS). Nothing in this folder duplicates that; nothing
   post-1991 is in this folder at all.

## Files

### CIA reconstructions of the Soviet economy (`cia_soviet_*.csv`)

Source: `data/raw/ussr-russia-historical/cia-soviet-economy-assessments/` (6 PDFs).

| File | Coverage | What it covers / provenance |
|---|---|---|
| `cia_soviet_gnp_by_sector_1950_1987.csv` | annual, 1950–1987 | USSR GNP by sector of origin (industry, construction, agriculture, transportation, communications, trade, services, military personnel, other, total GNP, GNP in established prices), billion 1982 rubles at factor cost. From **`JEC-Measures-Soviet-GNP-1982-Prices.pdf`**, Table A-1 (Joint Economic Committee, 101st Congress, S.Prt. 101-123, "Measures of Soviet Gross National Product in 1982 Prices," Nov. 1990, study prepared by CIA analyst Laurie Kurtzweg). Text-native PDF; spot-checked against a 200dpi page-64 image render — exact match. |
| `cia_soviet_gnp_by_end_use_1950_1987.csv` | annual, 1950–1987 | Same source, Table A-6: GNP by end use (Consumption, Investment, Other government expenditures incl. defense/R&D/administration, GNP). Top-level rows only — the source table's sub-line detail (food/soft goods/durables, new fixed investment vs. capital repair, etc.) is in the raw PDF but not transcribed here. |
| `cia_soviet_consumption_population_1950_1987.csv` | annual, 1950–1987 | Same source, Table A-13: consumer goods / consumer services / total consumption per capita (1982 established-price rubles) and USSR population (million persons). |
| `cia_soviet_gnp_growth_and_defense_narrative.csv` | assorted years/periods, 1951–1989 | Long-format table of every citable growth-rate, defense-burden, and GNP-comparison figure found in the narrative text of the CIA English-language documents (`CIA-Assessments-Soviet-Union.pdf`, `4-AssessingSovietEconomicPerformance-documents31-41.pdf`, `Watching-the-Bear-2-Chap2-TheEconomy.pdf`, plus the intro of the JEC print). Includes the explicit **Soviet-official-vs-CIA GNP/NMP growth comparison for 1981–85/1986/1987**, the defense-share-of-GNP trajectory (24% in 1951 → 14% in 1959 → 14–16% range 1960–1990), the 1976 CIA defense-spending reassessment (ruble estimates revised up ~50%), and multiple vintage-specific GNP growth projections (1954, 1977, 1979, 1986 memos) each cited with its originating document and approximate page. |
| `cia_soviet_gnp_pct_of_us_gnp_1960_1983.csv` | 1960, 65, 70, 75, 80, 83 | "Figure 1" from `DOC_0000498181_ComparisonSovietUSGNP.pdf` ("A Comparison of Soviet and US Gross National Products, 1960-83," CIA SOV84-10114, Aug. 1984) — Soviet GNP as % of US GNP, **geometric mean of ruble-valuation and dollar-valuation comparisons**. Image-only PDF (no text layer); read directly off the printed bar chart. |
| `cia_soviet_us_gnp_ruble_valuation_1960_1981.csv` | annual, 1960–1981 | Same source, Appendix D Table 5: USSR and US total GNP, **ruble valuation only** (billion 1970 rubles), plus the USSR/US ratio row as printed. **Not directly comparable** to the geometric-mean series above — ruble-only valuation is well known to show a lower USSR/US ratio (the "index-number relativity"/Gerschenkron-effect issue the source document's own Appendix A discusses) — e.g. 1970 ratio is 43.9% here vs. 55% in the geometric-mean Figure 1. Extracted via iterative high-resolution (400dpi) crops of a dense 22-column table; digit-by-digit re-verified against the US GNP series' known recession years (1970, 1974–75, 1980) as an internal-consistency check. |
| `cia_soviet_us_defense_spending_ruble_valuation_1960_1981.csv` | annual, 1960–1981 | Same Table 5, Defense row: USSR and US defense spending (billion 1970 rubles) and ratio. Shows the well-documented crossover — Soviet defense spending (ruble-valuation) overtakes the US from the early 1970s (ratio >100%). One cell (**USSR 1966**) left blank — ambiguous between 36.3 and 34.3 on the scan even at 3x zoom, not guessed. |

### Official Soviet statistics (`narkhoz_*.csv`)

Source: `data/raw/ussr-russia-historical/narodnoe-khozyaistvo-yearbooks/` (5 editions: 1932 journal [4 parts], 1956, 1965, 1975, 1989).

| File | Coverage | What it covers / provenance |
|---|---|---|
| `narkhoz_national_economy_index_1913_1989.csv` | 1913–1989, several overlapping index bases | **The core headline panel.** "Key Indicators of National Economy Development" tables from all 4 fixed-yearbook editions, kept in long/tidy format with an `edition_and_source_page` column so each row's exact PDF+page provenance is preserved: (a) 1956 ed. p.34, base 1913=100, years 1913/28/40/50/55/56; (b) 1956 ed. p.42/51, annual detail for national income (1913–1956) and industrial output (1913–1956, most complete annual run); (c) 1965 ed. p.55-56, base 1940=100, years 1940–1965; (d) **1975 ed. p.47, base 1913=1 — the single best long-run panel, spanning the full Stalin-to-Brezhnev era in one consistent table** (1913, 1940, 1945, 1950, 1965, 1970–1975); (e) 1975 ed. p.49, base 1960=100, fills the 1955/1960 gap through 1975; (f) 1989 ed. pp.8-9, year-on-year % change 1985–1989 and 5-year-period average growth 1976-80/1981-85/1986-89 — **the last full official Soviet statistics published before the USSR's collapse**, directly showing the deceleration (GNP growth 4.8%→3.7%→3.7% by period) that the CIA documents above independently corroborate. |
| `narkhoz_population_1913_1956.csv` | 1913, 1926, 1939, 1940, 1956 | USSR population (total/urban/rural), 1956 ed. p.17. Two 1913 rows reflect two different border definitions (current USSR borders vs. pre-Sept-1939 borders) as printed. |
| `narkhoz_grain_harvest_index_1950_1956.csv` | annual, 1950–1956 | Gross grain/technical-crop harvest index (wheat, corn, sunflower, sugar beet, raw cotton, flax), base 1950=100. 1956 ed. p.107. |
| `narkhoz_livestock_products_index_1950_1956.csv` | annual, 1950–1956 | Meat/milk/wool/egg production index, base 1950=100. Same page. |
| `narkhoz_livestock_headcount_1916_1956.csv` | 1916–1956 (irregular annual) | Cattle/cows/pigs/sheep+goats, million head, all-farm-category. 1956 ed. p.128. **Vividly documents the 1930–33 collectivization-era livestock collapse** — cattle fell from 50.6M (1930) to 33.5M (1933), pigs from 14.2M to 9.9M — a real, official-statistics-confirmed data point on a historically contested episode. |
| `narkhoz_1932_five_year_plan_farm_machinery.csv` | 1928/29–1932 (1932 = plan target) | Agricultural-machinery production (seeders, cultivators, harrows, binders, combines, threshers) from the First Five-Year Plan. Source: `nar_khoz_1932_01_02.pdf` — this is issue 1-2 of *Narodnoe khoziaistvo SSSR*, a **journal**, not a fixed statistical yearbook like the other 4 editions (its own foreword frames it as launching "at the threshold of the second five-year plan," claiming completion of the first in four years). Only this one representative table was extracted; parts 03_04/05_06/07_08 of the same 1932 journal run were downloaded but not opened this round (see caveats below). |

### Imperial (Tsarist) Russia (`imperial_russia_*.csv`)

Source: `data/raw/ussr-russia-historical/imperial-russia-statistical-yearbook/` (13 years, 1904–1916; only **1904 and 1910** deep-mined this round — see caveats).

| File | Coverage | What it covers / provenance |
|---|---|---|
| `imperial_russia_population_by_region_1858_1910.csv` | 1858, 1897, 1904, 1910 | Population of the Russian Empire by region (European Russia, Vistula/Congress-Poland governorates, Caucasus, Siberia, Central Asian oblasts, Finland), with 1858 (10th Revision/tax-census) and 1897 (first modern Imperial census) given as historical comparison points inside the 1910 edition's own table. `StatisticalYearbookOfRussia_1904.pdf` p.82-83 and `StatisticalYearbookOfRussia_1910.pdf` p.60-61 — both image-verified at 250dpi (this caught and corrected an initial OCR misread of the 1910 grand total as 168,778.8 instead of the correct **163,778.8**). |
| `imperial_russia_international_population_comparison.csv` | 1904, 1910 (dated national censuses) | Russia vs. USA/Germany/Austria-Hungary/England/France/Italy/Belgium/Netherlands/Denmark/Norway/Sweden/Romania/Bulgaria/Switzerland/Japan — the Empire's own published international ranking ("by population, Russia holds first place among the civilized countries of the world"). Same two source pages. |
| `imperial_russia_population_density_comparison.csv` | 1904, 1910 | Persons per square verst, Russia vs. same country set — illustrates Russia's very low population density relative to Western Europe despite its large total population. |
| `imperial_russia_foreign_trade_1897_1908.csv` | 1897–1902 (clean annual + 5yr avg), 1908 (by border section) | Total Imperial Russian foreign trade (imports/exports, rubles). 1897-1902 rows are printed grand totals (`StatisticalYearbookOfRussia_1904.pdf` p.322-323); 1908 rows are the European/Finnish/Asian border subtotals as printed (`StatisticalYearbookOfRussia_1910.pdf` p.554-555), with an "all borders" total computed by us as their sum since no single printed grand-total cell was captured in the page crop used — flagged in the `notes` column, not presented as a directly-quoted figure. |

## Caveats — read before charting

- **Imperial Russia: only 2 of 13 downloaded years deep-mined.** Each volume
  is 200–470 pages of pre-reform-orthography Cyrillic (ѣ, і, ъ) table
  matter, often with a poor OCR text layer requiring page-by-page visual
  search. 1904 and 1910 were chosen as representative early/mid-run points
  and mined to a genuine standard (multiple tables, image-verified,
  cross-checked against each other for internal consistency). The other 11
  years (1905–1909, 1911–1916) are sitting in `data/raw/` untouched and
  ready for a focused follow-up pass — this is a real, logged
  incompleteness, not a claim that nothing more is extractable.
- **1932 narodnoe khozyaistvo edition: 1 of 4 downloaded parts opened, 1
  representative table extracted.** This edition is a journal, structurally
  different from the other 4 (fixed yearbook) editions in this folder — it
  does not have one clean "key indicators" summary table like 1956/65/75/89
  do; its content is narrative articles with embedded tables scattered
  throughout ~270 pages per part. The agricultural-machinery table
  extracted here is illustrative of the "Five-Year-Plan targets/actuals"
  ask in the task brief but is not a comprehensive digitization of the
  issue, let alone all 4 parts.
- **The 1966 USSR defense-spending cell** in
  `cia_soviet_us_defense_spending_ruble_valuation_1960_1981.csv` is blank —
  genuinely ambiguous on the source scan even under 3x digital zoom.
- **CIA-RDP92M00732R000300110001-2_MeasuresSovietGNP.pdf (189pp, scanned, no
  text layer)** was spot-checked, not independently transcribed page by
  page: its cover memo ("Here's the GNP paper... Date 24 Aug. 1989,"
  addressed to Richard Kaufman — the same JEC economist who supervised the
  1990 published print) and its introductory section structure confirm it
  is the internal CIA draft underlying `JEC-Measures-Soviet-GNP-1982-Prices.pdf`,
  which we extracted in full from the cleaner, text-native published
  version. Re-transcribing all 189 scanned pages by hand would have
  duplicated the same tables at much higher effort and higher transcription
  risk.
- **One CIA document could not be retrieved at all** (see
  `data/raw/ussr-russia-historical/cia-soviet-economy-assessments/manifest.json`
  `failures[]`): CIA-RDP85T01058R000507850001-1, "Soviet Statistical
  Falsification" — blocked by cia.gov/readingroom's bot wall with no
  Wayback Machine snapshot available. Directly relevant to this folder's
  subject matter (a whole CIA paper on the reliability of Soviet official
  statistics) but genuinely unobtainable in this environment.
- **`imperial_russia_foreign_trade_1897_1908.csv`'s 1908 "all borders"
  totals are computed by us**, not directly quoted — see notes column.
- Figures spanning the 1917 revolution/civil war (1913 as a base year
  appearing in both the Tsarist-era-adjacent 1904/1910 tables and the
  Soviet-era `narkhoz_*` 1913-based index tables) are **not the same
  underlying survey** — the Soviet-era tables' "1913" column is a
  retrospective Soviet-era reconstruction of the pre-revolutionary economy
  for comparison purposes, not a re-use of the Imperial statistical
  apparatus's own 1913 figures (which in any case predate the last
  downloaded Imperial yearbook, 1916). Do not treat "1913=100" in the
  Soviet tables as literally sourced from the Imperial Russia folder.
