# UN Demographic Yearbook Historical Supplement — Iran extraction

Iran-only convenience extractions from the UN Statistics Division's Demographic Yearbook 1997
Historical Supplement (raw multi-country source files in
`data/raw/un-demographic-yearbook-historical/dyb-historical-supplement-1948-1997/`). These are
**derived** files (country-filtered, reshaped from the original wide/merged-cell CSV layout into
tidy long/wide tables) — the immutable originals remain in `data/raw/`.

This extraction directly resolves the project's previously-confirmed gap that Iran's 1956, 1966,
and 1976 national census originals are not directly downloadable (Iran Data Portal has only
navigation stubs for these years; IPUMS-International starts at 2006). The UN's own compiled
Historical Supplement carries Iran's exact enumerated counts, transcribed from Iran's own official
submissions to the UN Statistics Division.

| File | Coverage | Source table |
|---|---|---|
| `iran_annual_population_vital_rates_1948_1997.csv` | **Annual, 1948-1997** — mid-year population, live births, crude birth rate, deaths, crude death rate, natural increase rate, and (sporadic ~5-year) infant mortality rate | DYB Historical Supplement Table 1 |
| `iran_census_population_by_sex_urban_rural_1956_1996.csv` | **Each census/survey: 1956, 1959(survey), 1966, 1976, 1986, 1991, 1996** — total/male/female population, intercensal growth rate, urban/rural split | DYB Historical Supplement Table 2 |
| `iran_census_age_sex_urban_rural_1956_1996.csv` | **Full age pyramid at each actual census (1956, 1966, 1976, 1986, 1991, 1996)** — by sex (Total/Male/Female) and residence (Total/Urban/Rural), 5-year age bands | DYB Historical Supplement Table 3 (sample-survey years 1959/1971/1975/1981/1984/1994 excluded from this file — see notes below) |
| `iran_life_expectancy_at_birth_1950_1995.csv` | **Period estimates, 1950-1995**, by sex | DYB Historical Supplement Table 9a |

## Key figures (exact enumerated census counts, from Table 2)

| Census date | Total population | Male | Female | Urban % | Source code |
|---|---|---|---|---|---|
| 1 Nov 1956 | **18,954,704** | 9,644,944 | 9,309,760 | 31.4% | Cdf (census, de facto) |
| Oct 1959 | 19,745,582 | 10,142,586 | 9,602,996 | 30.5% | Sdf (sample survey, not a census) |
| 1 Nov 1966 | **25,785,210** | — | — | — | Cdf |
| Nov 1976 | **33,708,744** | 17,356,347 | 16,352,397 | 47% | Cdf |
| 22 Sep 1986 | 49,445,010 | 25,280,961 | 24,164,049 | — | Cdf |
| 1 Oct 1991 | 55,837,163 | 28,768,450 | 27,068,713 | 57% | Cdf |
| Oct 1996 | 60,055,488 | 30,515,159 | 29,540,329 | — | Cdj (census, de jure) |

**Cross-validation**: the 1956 (18,954,704), 1976 (33,708,744), and 1986 (49,445,010) totals match
— to the exact digit — both the World Bank archival-PDF citations
(`data/raw/world-bank-archives-iran/census-demographic-citations-1956-1982/`) and the
Encyclopaedia Iranica "CENSUS i. In Iran" narrative
(`data/raw/iran-census/iranica-census-demography-narrative-series-1868-1998/`) obtained
independently in the same research pass. Three independent sources agreeing to the exact digit
gives high confidence these are the correct definitive counts.

**1966 note**: Table 3 (age pyramid) reports a *settled-population-only* total of 25,078,923 for
1966, footnoted as excluding an unsettled population of 244,141 and nomadic tribes of 462,146.
244,141 + 462,146 = 706,287, and 25,078,923 + 706,287 = 25,785,210 — exactly Table 2's all-inclusive
total. This is a clean internal check, not a discrepancy.

## Vital statistics (Table 1) not previously in `data/processed/`

Checked `data/processed/owid_indicators.csv` and `data/processed/macro_wdi.csv` before building
this extraction: OWID carries Iran `child-mortality`, `fertility-rate-complete-gapminder`, and
`life-expectancy`, but **no crude birth rate or crude death rate series**; WDI has no Iran
demographic-vital-rate indicators at all in this project's extract. The annual crude birth/death
rate and sporadic infant-mortality-rate series in `iran_annual_population_vital_rates_1948_1997.csv`
therefore is new coverage, not a duplicate.

Infant mortality rate (per 1000 live births), from the sporadic UN-flagged data points: 190 (1953),
175 (1958), 163 (1963), 145 (1968), 122 (1973), 100 (1978), 78 (1983), 52 (1988), 30.9 (1994).

## Scope note on the age-pyramid file

Table 3 collapses age bands differently for different row types: the 4 actual full-population
censuses with a standard 85+ terminal bucket (1956, 1966, 1976) use a 19-band template; 1991 and
1996 break out age all the way to "100+" individually (22-band template); and the 1956 census's
*urban/rural* (as opposed to national-total) breakdown collapses into 5-year-pair buckets
(25-34, 35-44, etc., 13-band template). All three templates were detected and applied correctly
(verified: male + female "All ages" sums to the "Total" "All ages" value for every census date
present). Sample-survey/estimate years (1959, 1971, 1975, 1981, 1984, 1994 — source codes `Sdf`/`Edj`
rather than `Cdf`/`Cdj`) were deliberately EXCLUDED from this file because they use yet more
irregular collapsing patterns not worth reconciling for a non-census data point; their raw rows
remain available in the original source file in `data/raw/` if ever needed.
