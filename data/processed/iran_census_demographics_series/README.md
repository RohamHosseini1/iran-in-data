# Iran census & demographics series (1868–2016)

Harmonized 2026-07-13 from four raw source folders (all immutable, unchanged):
`data/raw/world-bank-archives-iran/census-demographic-citations-1956-1982/`,
`data/raw/iran-census/iranica-census-demography-narrative-series-1868-1998/`,
`data/raw/iran-census/iran-census-historical/` (2011/2016 census bulletins + spreadsheets), and
`data/raw/un-demographic-yearbook-historical/` (already processed in a prior round — see below,
verified here rather than redone).

## Files produced this round

| File | Coverage | What it covers |
|---|---|---|
| `wb_archives_population_demographic_citations_1956_1982.csv` | 1956–1982 (sparse, narrative citations) | Population, birth/death rates, urbanization, labor-force participation, fertility, from three World Bank Iran economic reports (1962, 1971, 1974) |
| `provincial_population_1956_1972.csv` | 1956, 1966 (census) + 1967–1972 (intercensal estimates) | Province/governorate population from the 1974 WB Statistical Appendix Table 1.1 — reshaped wide→long |
| `iranica_census_demography_narrative_1868_1998.csv` | 1868–1998 (sparse) | Pre-modern census attempts (1868 Tehran, 1883/84 Shiraz), all 8 national censuses' organizational/headline detail (1956–1986), fertility/family-planning, marriage, migration, nomadic population, literacy — Encyclopaedia Iranica's CENSUS and DEMOGRAPHY articles |
| `provincial_age_sex_residence_2011_census.csv` | 2011 census, single cross-section | Full 31-province population by 5-year age band × sex × residence (Total/Urban/Rural/Unsettled) — 7,548 rows, extracted from 31 separate provincial `.xls` files |
| `provincial_population_households_2016_census.csv` | 2016 census, single cross-section | National + 31-province population, sex, households, urban/rural/unsettled breakdown |
| `provincial_age_sex_2016_census.csv` | 2016 census, single cross-section | Full 31-province population by 5-year age band × sex (1,440 rows) |
| `national_and_provincial_summary_2011_census.csv` | 2006 vs. 2011, national + 31-province | Hand-transcribed SCI bulletin tables: population change, urban/rural indicators, religion, citizenship, age groups, housing tenure type (national); population & growth, density, sex ratio, urbanization rate, household size (by province) |
| `national_summary_2016_census.csv` | 1986–2016 trend + 2006/2011/2016 cross-sections | Population/household trends, growth by period, age structure, mean/median age, marital status, nationality, housing tenure, literacy rate (national + by province), provincial growth rate 2011–2016 |

## Added 2026-07-13: 1996 census OCR'd (7 more files)

The 1996 census bulletin (`data/raw/iran-census/iran-census-historical/1996-census-data.pdf`) was
previously flagged as a confirmed scanned image PDF with no text layer, not extracted. Per this
project's "any source needing OCR, do it" directive, it was extracted this round via `pdftoppm
-png -r 200`–`400` page renders read directly with the Read tool (no OCR software — the source
is Perso-Arabic numerals throughout, hand-verified digit by digit), cross-checked against
`pdftotext` (confirmed empty, as expected). All 7 tables in the "Selected Findings" section
(pages 1–10 of the 16-page PDF) were extracted; the remaining pages (migration-by-previous-
residence detail, employment-by-economic-sector detail, and several bar-chart figures with no
reliable digit-to-bar mapping) were not — a scoped future addition from the same PDF.

| File | What it covers |
|---|---|
| `census1996_admin_units_by_province.csv` | Shahrestan/bakhsh/shahr/dehestan/populated-village counts by province, Table A (الف) |
| `census1996_population_by_sex_residence.csv` | Population by sex × urban/rural-resident/non-resident, Table B (ب) |
| `census1996_population_by_age_group.csv` | Population by 8 broad age bands, with sex ratio, Table P (پ) |
| `census1996_population_by_religion.csv` | Population share by religion (Muslim/Zoroastrian/Christian/Jewish/Other), Table T (ت) — partial, see caveats |
| `census1996_literacy_by_age_group.csv` | Literacy rate by age group × sex × urban/rural/non-resident, Table H (ح) |
| `census1996_school_enrollment_by_age_group.csv` | In-education share among population 6–24 by age group × sex × residence, Table Kh (خ) |
| `census1996_activity_status_by_residence_sex.csv` | Employed/unemployed/student/homemaker/other distribution × sex × residence, Table D (د) |

### Caveats specific to the 1996 OCR pass

- **`census1996_admin_units_by_province.csv` has 5 genuinely illegible cells**, all from the same
  physical ink-blot/scan-damage region covering the Kurdistan and Kerman rows (shahr and dehestan
  for both) and the Hamedan row (shahrestan and populated-abadi). These were NOT guessed — each
  was checked against the printed national-total row via column-sum arithmetic (e.g. the bakhsh
  column sums to exactly 680 including Kurdistan=21 and Kerman=31, confirming those two cells;
  but the shahr/dehestan/abadi columns only reconcile when the damaged cells are excluded from
  the sum, confirming genuine illegibility, not just visual uncertainty). Per this project's
  standing rule (illegible values stay blank, never back-filled from an accounting identity even
  when mathematically recoverable), the arithmetic-implied values are noted in `notes` for a
  future re-scan but not recorded as data.
- **`census1996_population_by_religion.csv` is deliberately incomplete**: only Total/Muslim/
  Zoroastrian have all 4 columns (national/urban/rural/non-resident) legible; Christian and
  "Other/not stated" have only the national-total column legible; Jewish is blank entirely (heavy
  ink smudging on that specific row). Do not treat the missing cells as zero.
- **`census1996_activity_status_by_residence_sex.csv` has a hierarchy, not 9 flat categories**:
  "previously employed" and "never previously employed" are sub-splits of "Unemployed, seeking
  work" (their values sum to it exactly: 0.84+2.37=3.21), not additional independent categories —
  summing all rows naively would double-count the unemployed. Flagged in `notes` on the Total row.
- **`census1996_population_by_age_group.csv`: the 8 age-band populations sum to 60,055,888,
  which differs from the printed national total of 60,055,488 by 400** — a minor rounding/
  transcription artifact already present in the 1996 source table itself (each individual row
  visually re-verified against the page render; the ~0.0007% discrepancy was not chased further).
- This 1996 extraction is a genuine bridge point between the Pahlavi-era archival tables and the
  modern `sci_yearbook_1399_series/` (2001–2020) — e.g. `census1996_activity_status_by_residence_sex.csv`'s
  32.10% national employment share and `sci_yearbook_1399_series/labor_force_indicators_1380_1399.csv`'s
  1380 (2001) economic participation rate of 37.2% are DIFFERENT concepts (employed share of total
  population vs. labor-force participation rate of population 10+) — do not chart them as the same
  series without adjusting definitions.

## Already processed (verified, not redone)

`data/processed/un-demographic-yearbook-iran/` (4 files: annual population/vital rates
1948–1997, census population by sex/urban-rural 1956–1996, full age pyramid at each census
1956–1996, life expectancy 1950–1995) was built in a prior harmonization round from the UN
Demographic Yearbook Historical Supplement. Verified present, correctly documented, and its key
census totals (1956: 18,954,704; 1976: 33,708,744; 1986: 49,445,010) cross-check exactly against
this round's `wb_archives_population_demographic_citations_1956_1982.csv` and
`iranica_census_demography_narrative_1868_1998.csv` — three independent sources agreeing to the
exact digit. Registered in the chart-registry staging file as `status=new` (not re-extracted).

## Cross-validation performed

- `provincial_age_sex_residence_2011_census.csv`: summing all 31 provinces' "All Age Groups /
  Total / Both" population gives **75,149,669** — the exact national 2011 census total from
  `national_and_provincial_summary_2011_census.csv` Table 1 and Table 9. Zanjan province's total
  (1,015,734) also matches Table 9 to the digit.
- `provincial_population_households_2016_census.csv`: summing all 31 provinces' population and
  households both reconcile exactly to the national totals (79,926,270 persons; 24,196,035
  households).
- 2011→2016 province growth-rate cross-check caught and fixed a raw-source labeling defect (see
  Caveats below).

## Caveats — read before charting

- **Raw-source defect fixed on the way in, not left to corrupt the data**: the raw file
  `Population-by-Age-and-Sex-provincial-level.xlsx` labels **both** the Kerman and Kermanshah
  rows "Kermanshah" (a copy-paste error in the source spreadsheet itself, confirmed by direct
  cell inspection — no merged-cell artifact). Identified by cross-checking each row's population
  value against the independently-published 2011→2016 provincial growth-rate table: the row
  showing 3,164,718 matches Kerman's 2011 population (2,938,988) grown at Kerman's own
  published +1.49%/yr rate almost exactly, while 1,952,434 matches Kermanshah's 2011 population
  (1,945,227) grown at Kermanshah's own +0.07%/yr rate. The second "Kermanshah" occurrence was
  relabeled "Kerman" in `provincial_age_sex_2016_census.csv`; the raw `.xlsx` was left
  untouched per `docs/bookkeeping.md`.
- **Raw-source duplication, not an extraction bug**: `Population-and-Households.xlsx` lists Qom
  province's entire block (population, households, urban/rural/unsettled) twice in immediate
  succession — once as the province header, once again as its own sole shahrestan ("Qom" city),
  with identical numbers both times. This was deduplicated (kept once) when building
  `provincial_population_households_2016_census.csv`; verified the resulting province-level
  sums reconcile exactly to the national total, confirming the dedup was correct and no other
  province suffered a similar collision.
- **`provincial_population_households_2016_census.csv` deliberately excludes shahrestan
  (sub-province) rows** — the raw file has ~1,800 rows of county-level detail nested under each
  province; only province-level and national totals were extracted this round. The shahrestan
  detail remains available, untouched, in the raw `.xlsx` for a future deeper-dive pass.
- **`provincial_age_sex_residence_2011_census.csv` uses 5-year age bands, not single years of
  age** — the raw 31 provincial `.xls` files carry full single-year-of-age detail (128 rows each
  including every individual age 0–99+); only the "All Age Groups" total and 5-year age-group
  subtotal rows were extracted, to keep this a chart-ready summary rather than a ~30,000-row
  micro-detail dump. One raw file (`Zanjan-1.xls`) has its age-group labels in Persian rather
  than English (unlike the other 30 provincial files) — handled by applying a canonical,
  position-verified row-index → age-band label map common to all 31 files (all share an
  identical 128-row layout), rather than by text-matching a bilingual label.
- **A grouped bar chart in the 2016 "Selected Results" bulletin ("Average Annual Population
  Growth Rate," Total/Urban/Rural × 8 periods, 1956–2016) was deliberately NOT extracted.**
  `pdftotext -layout` recovers a bar chart's value labels only as a loose stream of numbers with
  no reliable position-to-bar mapping. A trial reconstruction produced a rural 1996–2006 figure
  (-0.44) that did not match the same statistic's unambiguous, table-sourced value elsewhere in
  this same census bulletin series (-0.40, from Table 1 of the 2011 bulletin, in
  `national_and_provincial_summary_2011_census.csv`). Rather than risk silently wrong data, the
  chart was dropped; the equivalent total-population growth rate by period is still fully
  covered, unambiguously, by the "Population increase by period" table (prose-table-sourced) and
  by Table 1's urban/rural/total splits for the two periods it covers.
- **1996 census (`1996-census-data.pdf`) could not be extracted — confirmed a scanned image PDF
  with no text layer** (`pdfinfo` shows "Creator: Book ScanCenter 5022"; `pdftotext` returns zero
  characters across all 16 pages), the same issue documented elsewhere in this project for CIA's
  NIS-33 (see `data/raw/cia-iran-economy/`). This is a genuine, confirmed gap, not a search
  failure — the 1996 national total (60,055,488) and household count (12,398,235 / avg. size 4.8)
  are still available via the 2016 bulletin's trend table (`national_summary_2016_census.csv`),
  but the 1996 bulletin's own detailed tables (age structure, religion, tenure, etc. for that
  specific census) remain unextracted. A future pass could OCR this file using the
  `pdftoppm -r 200` + visual-verification method already proven on the Pahlavi-era World Bank
  documents elsewhere in this project (see `data/processed/pahlavi_era_tables_index.md`).
- **Iran's 1956/1966/1976 census micro-detail (age-sex pyramids, provincial breakdowns) is not
  independently available from `iran-census-historical/`** — that granularity for those three
  censuses comes only from the UN Demographic Yearbook extraction
  (`data/processed/un-demographic-yearbook-iran/`), which stops at the 1996 census. There is a
  real, still-unresolved gap in provincial/age-sex detail for the 1986 census specifically (UN
  DYB has national age pyramid for 1986, but this project has no province-level 1986 breakdown).
- All Encyclopaedia Iranica citations were retrieved via an interactive browser tool since
  iranicaonline.org blocks curl/WebFetch with a Cloudflare challenge (HTTP 403) — consistent with
  the retrieval method already documented for this source elsewhere in the project.

## Sources

- World Bank, *Economic Development Program for Iran* (1962), *Economic Development of Iran*
  (1971, 1974) — Iran country documents, World Bank Archives (openknowledge.worldbank.org).
- Encyclopaedia Iranica: "CENSUS i. In Iran" and "DEMOGRAPHY" (iranicaonline.org).
- Statistical Centre of Iran (SCI) via Iran Data Portal (Syracuse University, irandataportal.syr.edu):
  *National Population and Housing Census 2011 (1390): Selected Findings* (unofficial English
  translation); *Iran National Population and Housing Census 2016: Selected Results*;
  `Population-and-Households.xlsx`; `Population-by-Age-and-Sex-provincial-level.xlsx`; 31
  provincial 2011 census `.xls` tables.
- UN Statistics Division, Demographic Yearbook Historical Supplement 1948-1997 (see
  `data/processed/un-demographic-yearbook-iran/README.md` for that extraction's own detail).

Full manifests: `data/raw/world-bank-archives-iran/census-demographic-citations-1956-1982/manifest.json`,
`data/raw/iran-census/iranica-census-demography-narrative-series-1868-1998/manifest.json`,
`data/raw/iran-census/iran-census-historical/manifest.json`.
