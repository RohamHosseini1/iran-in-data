# Data Inventory — everything we have, exactly what years it covers

This is the complete ledger, not a curated subset. Nothing here has been stripped or deprioritized
— every source the project has ever collected is listed, including full Islamic Republic-era
coverage. **Nothing is discarded.** The Pahlavi era gets extra narrative attention in
`CHART_CATALOG.md` because that's the stated focus for *new* hunting effort, but everything below
stays in the database regardless of era.

Legend: **[P]** = already harmonized into `data/processed/*.csv` (query-ready); **[R]** = collected
in `data/raw/` but not yet harmonized (still usable, just needs a parser). Iran year range is
always given first; comparator range noted only when it differs meaningfully.

---

## 1. Macro & national accounts

| Dataset | Iran coverage | Comparators | Notes |
|---|---|---|---|
| **[P]** World Bank WDI (~1,600 indicators) | 1960–2025 | same, all 17 countries | the macro backbone |
| **[P]** IMF WEO | 1980–2031 | same (Russia from 1989) | includes 5yr-ahead forecasts, flagged |
| **[P]** Maddison Project 2023 (GDP/capita, population) | annual 1950–2022, sparse benchmarks to year 1 | varies — some countries (Spain, France, UK, Germany, USA) have data to year 1; others (Korea, Saudi, Russia, Argentina) start 1800s | deepest series in the project |
| **[R]** Penn World Table 10.01 | 1950–present (user guide only downloaded; data file still pending) | same | |
| **[R]** Clio Infra (GDP, inflation, life expectancy, population, real wages) | GDP: Roman times–2016; inflation 1500–2010; life exp. 1800–2010; population 1500–2000; wages 1820–2000 | all 17 countries | |
| **[R]** UNSD National Accounts (AMA) | 1970–latest | all UN-reporting countries | |
| **[R]** WID.world (income/wealth inequality) | full coverage, ~1900–2025 (900/3280 requested cells populated) | varies — **USSR itself has no income/wealth-share series** (only average income from 1950); Russia has full series via Novokmet-Piketty-Zucman reconstruction | genuine surprise: Iran's coverage is *better* than expected for an oil state |
| **[R]** SWIID (Gini coefficients) | 55 years, 1969–2023 | 1960–2023, all 17 | |

## 2. Pahlavi-era primary-source extraction

Hand-transcribed from scanned World Bank reports (plus one Encyclopaedia Iranica narrative series
and one academic paper), every number visually verified against the source page image (not trusted
from raw OCR). All Iran-only, all 1920s–1970s. 33 dataset folders now exist in
`data/raw/pahlavi-era-primary-extraction/` (up from the 21 first recorded); the master index is
`data/processed/pahlavi_era_tables_index.md`.

| Table | Years | Source document |
|---|---|---|
| Agricultural production (wheat, citrus, cotton, etc.) | 1950–1958 | 1960 WB "Current Economic Position" |
| Cost-of-living index, 7 major cities | 1955–1959 | same |
| Industrial production | 1954/55–1958/59 | same |
| Oil revenues | 1955/56–1962/63 | same |
| Per-capita consumption | 1955/56–1957/58 | same |
| Petroleum statistics | 1956–1958 | same |
| Actual budget revenues | 1958–1959 | same |
| Actual treasury expenditures | 1958–1959 | same |
| Budgeted expenditures | 1955–1960 | same |
| Changes in money supply | 1957–1959 | same |
| Banking statistics, private sector (credit/deposits) | June 1957–June 1959 | same |
| Exports by commodities | 1956/57–1958/59 | same |
| Imports by commodities | 1956/57–1958/59 | same |
| International transactions (balance of payments precursor) | 1953–1959 | same |
| External public debt summary + service schedule | debt stock Sept 1959; service projected 1960/61–1973/74 | same |
| Crop land/production/value | 1960 | 1962 WB "Economic Development Program" |
| Livestock production/value | 1960 | same |
| Road vehicle registration | 1955/56 & 1960/61 | same |
| Gasoline consumption | 1955/56–1961/62 | same |
| Railways income/expense | 1953/54–1960/61 | same |
| Railways freight/passenger traffic | 1953/54–1960/61 | same |
| Ocean trade (non-petroleum) | 1950/51–1959/60 | same |
| Industry import-dependence | ~1969–1970 | 1970 WB "Industrialization" |
| Balance of payments summary | 1963/64–1969/70 | 1971 WB "Foreign Trade/BOP" (one cell left blank — ink smudge on the scan obscured 1964/65 "errors and omissions"; the accounting identity implies −14 but that wasn't entered as data) |
| Oil exports and revenues | 1963/64–1970/71 | 1971 WB "Petroleum Sector" |
| Government revenue summary | 1962/63–1971/72 | 1971 WB "Current Economic Position" Vol.7 Statistical Annex (Table 5.2) |
| Ordinary budget, central govt. current expenditure | 1962/63–1971/72 | same (Table 5.1) |
| Monetary survey (stock levels) | 1963/64–1969/70 | same (Table 6.1) |
| Changes in money & quasi-money (flow/factors) | 1964/65–1970/71 | same (Table 6.2) |
| Summary of central government operations (revenue/expenditure/deficit/financing) | 1962–1973 | 1974 WB "Economic Development" Vol.4 Statistical Appendix (Table 6.1) — reaches into the 1972 prelim actuals and 1973 budget estimate, i.e. the opening of the oil-price-shock years |
| Movements in monetary aggregates | 1963–1973 | same (Table 7.1) — extends the money-supply flow series 3 years past the 1971-vintage table above, capturing the post-1973 oil-boom monetary expansion |
| Iranica fiscal-system narrative (taxation, budget, oil revenue) | 1921–1979 (irregular: single years, periods, decade-averages as stated in the source) | Encyclopaedia Iranica |
| Iran development indicators, 1900 vs. 2006 (population, income, urbanization, life expectancy, literacy, ag. share of GDP, trade/GDP) | **1900 and 2006** — a genuine century-bridging single table | Esfahani & Pesaran (2008) |

**Extraction status**: 33 datasets total, all verified against source page images, zero fabricated
cells (illegible values left blank and noted, never guessed — including cases where a value could
have been back-calculated from an accounting identity and deliberately wasn't entered as data; several
sign ambiguities in faint print were instead resolved by testing which reading makes a documented
internal identity close exactly). A handful of documents (a Figure-only GDP/oil chart in Esfahani-
Pesaran with no underlying table, most of the 1970 Industrialization report beyond one
import-dependence table) were confirmed to have no further extractable tabular data, not skipped
for lack of effort. Several companion tables in the same source PDFs are flagged in their sibling
manifests as known follow-up candidates (e.g. 1974 report's Tables 6.2–6.5, 7.2–7.3 covering revenue
detail, expenditure functional breakdown, and banking-system balance sheets) — a good next batch for
the same proven methodology.

## 3. Agriculture & food (the founding theme)

| Dataset | Iran coverage | Comparators |
|---|---|---|
| **[P]** FAOSTAT QCL (production, all items) | 1961–2024 | 1961–2024 (Russia from 1992) |
| **[P]** FAOSTAT FBS (food balances / consumption proxy) | 2010–2023 | same |
| **[P]** FAOSTAT FBSH (food balances, historic) | 1961–2013 | same (Russia from 1992) |
| **[P]** FAOSTAT PP (producer prices) | 1991–2025 | same |
| **[P]** FAOSTAT PA (producer prices archive) | 1966–1990 | same |
| **[P]** FAOSTAT CP (food consumer price indices) | 2000–2025 | same |
| **[R]** FAOSTAT TI (trade indices) | 1961–2024 | same |
| **[R]** USDA FAS PSD (production/supply/distribution) | 1960–present | all |
| **[R]** WFP food prices (market-level retail) | varies by market | Turkey, Venezuela also covered |
| **[R]** FAO GIEWS Iran country brief | current + historical archive | Iran only |
| **[R]** USDA GAIN reports | — | **Turkey only (2018)** — Iran poultry reports don't exist in the public GAIN archive, a sanctions-related absence, not a search failure |

## 4. Prices, wages & cost of living

| Dataset | Iran coverage | Comparators |
|---|---|---|
| **[R]** ILOSTAT CPI | confirmed present, 1914–2025 range for the indicator overall | all |
| **[P/R]** BLS full CPI bulk (USA) | — | 1913–2026, USA |
| **[P/R]** FRED micro item prices (eggs, oranges, gasoline, electricity, whole chicken) | — | 1976–2026, USA |
| **[R]** Banco de España CPI | — | long-run historical, Spain |
| **[R]** INE Spain CPI | — | 1961–2026, Spain |
| **[R]** ELSTAT Greece CPI | — | **1959–2026**, Greece |
| **[R]** TurkStat CPI | — | 2003-base series, Turkey |
| **[R]** GASTAT CPI | — | monthly bulletin + annual, Saudi |
| **[R]** BCV Venezuela INPC | — | since 2007, Venezuela |
| **[R]** INDEC Argentina CPI | — | post-Dec-2016 rebuild (credible series), Argentina |
| **[R]** KOSIS Korea CPI | — | 1965–2025, Korea |
| **[R]** Argentina inflation reconstruction (Cavallo & Bertolotto) | — | **1943–2018 monthly, Argentina** — the real underlying dataset, not just the paper |

## 5. Energy & oil

| Dataset | Iran coverage | Comparators |
|---|---|---|
| **[P]** OWID oil production | **1900–2024, continuous** | same |
| **[P]** OWID energy (broader) | 1750–2025 | same |
| **[R]** JODI oil (primary + secondary) | 2002–2026 | all reporting countries |
| **[R]** JODI gas | 2007–present | all |
| **[R]** OPEC Annual Statistical Bulletin 2025 | historical to 2024 | Iran, Saudi, Venezuela, OPEC-wide |
| Pahlavi-era oil revenue/exports (see §2) | 1955/56–1970/71 | Iran only |
| **[R]** Energy Institute Statistical Review | — | **not secured** — Cloudflare-blocked every attempt, incl. browser-based; genuine gap |

## 6. Trade

| Dataset | Iran coverage | Comparators |
|---|---|---|
| **[R]** Harvard Atlas (complexity rankings, total trade) | 1995–2024 | all, country-level |
| **[R]** WITS appliance trade (HS 8418/8450) | 2021–2023 | all 17, via UN Comtrade preview API (some rows capped at 500 due to free-tier limits) |
| **[R]** UNCTAD Maritime Profiles | 2024 snapshot | all 17 — same-source multi-country win |
| **[P]** OWID trade share of GDP | 1960–2024 | same |
| Pahlavi-era ocean trade, BOP (see §2) | 1950/51–1969/70 | Iran only |

## 7. Finance, banking & markets

| Dataset | Iran coverage | Comparators |
|---|---|---|
| **[R]** BIS (policy rates, credit, property prices, USD FX) | Iran included in BIS-reporting economies | all, long historical runs |
| **[R]** CBI Annual Review (via Wayback) | fiscal years 1396–1400 (2017/18–2021/22) | Iran only |
| **[R]** CBI policy rates (via Wayback) | weekly, 2021–2025 | Iran only |
| **[R]** TGJU parallel USD/IRR rate | 2011–2026 | Iran only |
| **[R]** TGJU gold coin prices (Bahar Azadi, Emami) | 2013–2026 | Iran only |
| **[R]** TEDPIX (Tehran Stock Exchange index, via TGJU) | 2014–2026 | Iran only |
| **[R]** Bimeh Markazi (Central Insurance) annual reports | fiscal years 1384–1391 (2005/06–2012/13) | Iran only |
| **[R]** SAMA monthly bulletin | latest + historical series | Saudi only |
| **[R]** BCRA (Argentina) reserves, FX, policy rate | — | 1996–2026, Argentina; **no parallel/blue-dollar rate exists in official data**, confirmed absent not just unfound |
| **[R]** Banco de Portugal (BPstat) | — | GDP since 1977, interest rates from **1965**, Portugal |
| **[R]** Bank of Greece monetary/financial series | — | Greece |

## 8. Fiscal, budget & government

| Dataset | Iran coverage | Comparators |
|---|---|---|
| **[R]** Iran Plan & Budget Org — 7 Five-Year Development Plans | 1368–1406 SH / 1989–2028 CE — **Islamic-Republic-era plans only; no Pahlavi-era plans were directly linked on the source portal despite being sought** | Iran only |
| **[R]** Iran annual budget laws | SH 1371–1401 / 1992–2023 | Iran only |
| **[R]** World Bank Archives — Iran historical documents | **1950–1978**, fully open access | Iran only — 39 PDF reports now in `data/raw/world-bank-archives-iran/historical-documents/` (grew from an initial 8 via the WDS search API; this is the source pool §2's extraction tables are drawn from, and only a fraction of it has been hand-transcribed so far) |
| Pahlavi-era budget/oil-revenue/monetary tables (see §2) | 1953–1974, near-continuous for budget & money supply from 1955 | Iran only |
| **[R]** IMF Article IV staff reports | 2015–2025 | Iran, Saudi, Korea, Turkey |
| **[R]** Iran Data Portal — government finance tables | **1937–2017** | Iran only — one of the deepest single tables in the project |
| **[R]** Majlis historical budget-law texts (lamtakam.com mirror) | FY1301, 1341, 1357–1363 (~1922/23, 1962/63, 1978/79–1984/85) — **not continuous**, real gap years 1302–1340, 1342–1356, 1359, 1364–1370 | Iran only — primary Persian legal texts, not summaries; complements `iran-plan-budget-org/annual-budget-laws` (1371–1401) |
| **[R]** Stanford Iran 2040 "Government Budget" dashboard (Azadi & Mirramezani 2022) | ~1996/98–2018, revenue/expenditure/tax composition, by presidential administration | Iran only — captured as a static image (source Tableau viz gates its data-export button behind a CAPTCHA) |

## 9. Demographics & census

| Dataset | Iran coverage | Comparators |
|---|---|---|
| **[P]** UN World Population Prospects 2024 | 1950–2100 | all + regional aggregates |
| **[R]** UN Demographic Yearbook | 2005–2024 | Iran, Saudi confirmed present |
| **[R]** Iran national censuses | **only 1996, 2011, 2016 secured** — 1956/1966/1976/1986/2006 confirmed genuinely unavailable via Iran Data Portal or IPUMS International (IPUMS starts at 2006) | Iran only |
| **[R]** Barro-Lee education attainment | 1950–2015 | all |
| **[P]** OWID demographics (population, life expectancy, child mortality, schooling) | -10000–2025 | same |

## 10. Labor

| Dataset | Iran coverage | Comparators |
|---|---|---|
| **[R]** ILO minimum wage by country | Iran: 2001, then coverage gaps; wider range 1980–2025 depending on country | all |
| **[R]** ILOSTAT (unemployment, labor force, informal employment) | unemployment confirmed present (1,692 rows); mean nominal wages **NOT present for Iran**; informal employment **zero rows under either ILO definition** — real, confirmed gaps | all |
| **[R]** Iran minimum wage history (hand-compiled from Supreme Labor Council decisions) | 1995–2026 | Iran only |
| **[R]** OECD (wages, union density, collective bargaining, social expenditure) | — | Korea, Turkey, Spain, Portugal, Greece, USA + broader EU (Iran not OECD, not applicable) |
| **[R]** Iran Data Portal labor tables | **1956–2014** | Iran only |

## 11. Health

| Dataset | Iran coverage | Comparators |
|---|---|---|
| **[R]** WHO health expenditure | 2000–2023 | all 10 core comparators |
| **[R]** WHO health indicators (infant/maternal mortality, physicians, etc.) | 1949–2023 (varies by indicator) | same |

## 12. Industry & mining

| Dataset | Iran coverage | Comparators |
|---|---|---|
| **[R]** USGS Minerals Yearbook | 2016–2023 (modern digital archive; older editions not yet checked) | Saudi, Turkey, Russia, Argentina (matched via same source); USA via Mineral Commodity Summaries instead |
| **[R]** ICCIMA (Chamber of Commerce) — PMI, statistical yearbook | recent months + Statistical Yearbook 1403 | Iran only |
| **[R]** MIMT (Ministry of Industry, Mine & Trade) | Feb 2021 daily bulletins (via Wayback) | Iran only |
| **[R]** IMIDRO (mining) | 2012–2022 | Iran only |
| **[R]** Eurostat Prodcom (domestic appliances) | — | 2020–2024, EU countries |
| **[R]** APPLiA statistical reports (appliance industry) | — | 2018–2024, EU countries |
| Pahlavi-era industrial production, gasoline, railways (see §2) | 1953–1962 | Iran only |

## 13. Housing

| Dataset | Iran coverage | Comparators |
|---|---|---|
| **[R]** OECD house prices | — | **1959–2026**, comparator countries |
| **[R]** CBI/SCI housing data | modern decades (via Annual Review, Iran Data Portal housing tables 1966–2006) | Iran only |
| Note | no housing price index found for the Pahlavi era specifically — housing price indices are a late-20th-century statistical practice worldwide, not an Iran-specific gap | |

## 14. Historical/narrative primary sources (feed the timeline, not chart series directly)

| Dataset | Iran coverage |
|---|---|
| CIA declassified economic assessments (incl. NIS-33) | ~1950s–1996, spanning both Pahlavi and Islamic Republic eras |
| FRUS Iran volumes | 1951–54, 1958–60, 1973–76 |
| Encyclopaedia Iranica economy/fiscal articles | 1921–1994 (Pahlavi + early Islamic Republic) |
| USAID/Point Four Program reports | 1948–1963 |
| Esfahani-Pesaran (2008) | 1900–2008 narrative + data, century-spanning |
| USSR: CIA Soviet-economy assessments, Narodnoe khozyaistvo yearbooks, imperial Russia yearbook | 1904–1996 |

## 15. Competitiveness & business environment

| Dataset | Iran coverage | Comparators |
|---|---|---|
| **[R]** WEF Global Competitiveness Index (historical) | 2010–2017 (Iran added in the 2010-11 edition) | 2007–2017, all |
| **[R]** World Bank Enterprise Surveys | **zero coverage — confirmed, Iran was never surveyed** | Turkey, Saudi, Venezuela, Korea, USA, Russia, Spain, Portugal, Greece, Germany |

## 16. Contested/qualitative estimates (documented as ranges, not point facts)

| Item | Status |
|---|---|
| Bonyad/IRGC share of Iran's GDP | 7 attributed estimates, 4.2%–65%, sources ranging from state media to advocacy-adjacent outlets — deliberately NOT resolved to one number |
| Iran car ownership | CEIC preview 2005–2020 + one 2020 household-survey snapshot |
| Iran bread subsidy reform | narrative notes, 2018–2022 context |

## 17. Modernization & infrastructure ("before and after" indicators)

All sourced from Encyclopaedia Iranica narrative articles (citing Iran's own Statistical Yearbook
editions 1953/1965/1976/1988/89 and UNESCO), Wikipedia (citations preserved), GFRAS, and
Encyclopedia.com — filling pre-1970 gaps that WDI's own series (fixed telephones, air passengers)
don't reach. Harmonized 2026-07-13 into small per-topic tidy CSVs (mirroring the
`iran_data_portal_deep_series/` pattern) — now **[P]**, Iran only:

| Dataset | Iran coverage | Notes |
|---|---|---|
| Telecom (telegraph, telephone, radio, TV, postal) | 1858–1990, concentrated at 1913/14, 1953, 1965, 1975/76, 1979, 1988/89 | **[P]** `data/processed/iran_telecom_communications_series/` (from `data/raw/iran-telecom-history/`) |
| Cinema (theaters, attendance, film production) | 1932–1988 | **[P]** `data/processed/iran_media_history_series/` — movie houses 142 (1959)→453 (1975)→255 burned/closed pre-1979→198 (1979) |
| Press/newspapers, periodicals, literacy rate | 1898–1988 | **[P]** `data/processed/iran_media_history_series/press_periodicals_series.csv` |
| Aviation — Iran Air passengers/employees/revenue | 1946–2003 | **[P]** `data/processed/iran_aviation_history_series/iranair_passengers_employees_revenue.csv` |
| Aviation — full civil-aviation history (fleet, founding, events) | 1913–2007 | **[P]** `data/processed/iran_aviation_history_series/aviation_events_and_fleet.csv` |
| White Revolution — Literacy Corps (Sepah-e Danesh) | 1958–1979 (program ran 1963–79) | **[P]** `data/processed/iran_white_revolution_corps_series/` — illiteracy 67.2%/87.8% (m/f, 1966) → 44.2%/53% (1979) |
| White Revolution — Health Corps (Sepah-e Behdasht) | 1920–1978 | **[P]** `data/processed/iran_white_revolution_corps_series/health_expenditure_series.csv` — govt health spending Rls 0.9M (1920) → Rls 116.5bn (1974) |
| White Revolution — Extension/Development Corps | 1964–1979 | **[P]** `data/processed/iran_white_revolution_corps_series/extension_corps_stats.csv` |
| White Revolution — all 3 corps, consolidated stats | 1963–1978 | **[P]** `data/processed/iran_white_revolution_corps_series/white_revolution_corps_stats.csv` — some figures flagged "unverified" (uncited in source) |

## 18. Specialty-export & consumption goods

FAOSTAT's trade/crops-livestock domain has zero caviar/sturgeon and zero carpet coverage at any
date (confirmed, not a search gap) — these categories exist only via Encyclopaedia Iranica narrative
extraction and modern trade-press/official compilations. Harmonized 2026-07-13 into
`data/processed/specialty_goods_series/` — now **[P]**, Iran only unless noted:

| Dataset | Iran coverage | Notes |
|---|---|---|
| Tobacco monopoly (Tobacco Régie → Dokhaniyat) | 1890–1995, non-continuous | **[P]** `data/processed/specialty_goods_series/tobacco_monopoly_1890_1995.csv` |
| Tobacco market, post-privatization snapshot | 2018 | **[P]** `data/processed/specialty_goods_series/tobacco_post_privatization_2018.csv` — Iranian Tobacco Co. share collapsed to 15–20% after 2012 privatization |
| Carpet exports, Pahlavi & early post-Pahlavi | 1960–1988 (fiscal years 1339–1367 SH) | **[P]** `data/processed/specialty_goods_series/carpet_exports_1960_1988.csv` |
| Carpet export value/volume, post-1990 | 1994–2025, non-continuous (headline/peak years only) | **[P]** `data/processed/specialty_goods_series/carpet_exports_post1990.csv` — 1994 peak $2.132bn → 2019 trough $69M → FY2025 $39.7M |
| Caviar/sturgeon — CITES export quota | 2006 (single year, 44,370 kg) | **[P]** `data/processed/specialty_goods_series/caviar_cites_quota_2006.csv` |
| Caviar — EU market report, sturgeon aquaculture | 2010–2018 | **[P]** `data/processed/specialty_goods_series/caviar_sturgeon_aquaculture_eumofa_2010_2018.csv` — Iran column only extracted; raw PDF also has CHN/ARM/RUS/USA/VNM/EU comparators |
| Caviar — Shilat (state fisheries org) production/exports | FY2013/14–2024/25, non-continuous | **[P]** `data/processed/specialty_goods_series/caviar_shilat_production_2013_2024.csv` |
| Sugar — consumption, imports by country, state monopoly | 1890–2002, non-continuous | **[P]** `data/processed/specialty_goods_series/sugar_1890_2000.csv` — incl. one real embedded 1906/07–1913/14 import table by origin country |
| Tea — cultivation area, production, imports, state org | 1895–1984, non-continuous | **[P]** `data/processed/specialty_goods_series/tea_1895_1984.csv` |
| Trans-Iranian Railway financing (sugar/tea excise context) | single cumulative figure through FY1938/39 | **[P]** `data/processed/specialty_goods_series/trans_iranian_railway_financing_context.csv` |
| FAOSTAT trade, Iran+comparators filtered (tobacco, tea, sugar, pistachio) | 1961–2024 | **[R]** `data/raw/faostat/tcl-trade-crops-livestock/filtered_iran_and_comparators.csv` — the properly-sized, Iran-filtered companion to FAOSTAT's raw trade dump; still needs a harmonize script |

## 19. Land reform, transportation infrastructure, TSE structural history, foreign-educated students, malaria, tourism & housing depth (new this round)

Six new source folders, all **[R]** (raw tidy CSVs, not yet harmonize-scripted into `data/processed/`).
Pre-flight checks before each hunt confirmed genuine gaps: WDI already covers school-enrollment
RATIOS (1971+), literacy RATE (1976+), hospital beds/physicians per capita (1960+), and tourism
arrivals/receipts (1995-2020) continuously — none of those were re-hunted; these datasets add
ABSOLUTE counts, pre-1971/pre-1995 Pahlavi-era anchors, and topics with zero prior coverage.

| Dataset | Iran coverage | Notes |
|---|---|---|
| Land reform (White Revolution, 1962-78) | 1950-1978 | **[R]** `data/raw/iran-land-reform/white-revolution-land-redistribution-statistics/` — hectares redistributed (2 contested estimates recorded as a range), farm corporations (89, 813 villages), rural cooperatives (2,942 societies, 3.01M members), provincial landholding variation. Landlord cash/bond compensation totals NOT found (genuine gap) |
| Transportation infrastructure (rail/road/port network history) | 1886-2024, core narrative 1922-1979 | **[R]** `data/raw/iran-transportation-infrastructure/rail-road-port-network-history/` — Trans-Iranian Railway (1,392-1,394km, 1927-1938), road-ministry institutional history, Bandar Abbas port throughput. Complements (does not duplicate) the Pahlavi-extraction railway income/freight tables in §2. Khorramshahr tonnage and Mehrabad airport-level traffic: not found |
| Tehran Stock Exchange structural history | 1967-2024 | **[R]** `data/raw/tsetmc/tehran-stock-exchange-founding-to-present-history/` — founding, 1979-1988 closure, listed-company counts, market cap, shareholder base. Complements (does not duplicate) the existing TEDPIX daily-index feed in §7 (2014-2026) |
| Foreign-educated Iranian students + domestic school system buildout | 1925-2023 (schooling); 1975-2016 (students in US) | **[R]** `data/raw/iran-education-history/foreign-educated-students-and-school-system-buildout/` — Iran was the #1 foreign-student-sending country to the US 1974/75-1982/83 (peak 51,310 in 1979/80); domestic school/teacher/student ABSOLUTE counts from 1925 (earliest schooling anchor in the whole database) |
| Malaria eradication campaign | 1945-1990 | **[R]** `data/raw/iran-health-history/malaria-eradication-campaign/` — narrative + CSV, institutional milestones + one order-of-magnitude estimate (~5M cases/year peak burden, late 1950s). Thinnest dataset this round — no continuous annual case-count series located, flagged for a future pass |
| Tourism (Pahlavi golden age + post-2020 recovery) | 1962-2024, flanking the WDI 1995-2020 window | **[R]** `data/raw/iran-tourism-history/pahlavi-era-and-modern-tourist-arrivals/` — 1962: <80,000 arrivals → 1977: ~700,000 (8.75x); 2024: 7M+ (post-WDI-cutoff recovery anchor) |
| Housing construction & density history | 1966-2000 | **[R]** `data/raw/iran-housing-urbanization/housing-construction-and-density-history/` — households-per-unit 1.29 (1966)→1.14 (1996); Fourth Plan 1968-73 (300K units built, density still rose 7.7→8.5 persons/dwelling); 1986 census material/amenity composition |

See SOURCES.md Round 36 for full source attribution and dead-ends.

## 20. International-institution membership history, oil-consortium wages/royalties, handicrafts, CITES (new this round)

Wildcard-hunt round targeting international-economic-institution relationships (OPEC, WTO/GATT,
IMF) and a genuine primary-source find on oil-consortium wages. All **[R]** (raw tidy CSVs, not
yet harmonize-scripted into `data/processed/`).

| Dataset | Iran coverage | Notes |
|---|---|---|
| OPEC quota/policy history | 1960-2025, non-continuous (dated milestones) | **[R]** `data/raw/iran-opec-membership/opec-quota-policy-history-1960-2025/` — founding, nationalization, quota-system introduction/suspension/revisions, sanctions-era exemptions. Granular year-by-year Iran quota-in-barrels series NOT found (OPEC ASB confirmed to contain no quota data at all) |
| WTO/GATT accession timeline | 1995-2026, non-continuous | **[R]** `data/raw/iran-wto-gatt-accession/wto-accession-timeline-1996-2025/` — Iran has NEVER completed WTO accession; 1996 application → blocked 22× → 2005 Working Party established → still never held its first meeting |
| IMF Article IV consultation history | 2002-2025, 8 completed consultations + documented 2019-2024 gap | **[R]** `data/raw/imf-article-iv-iran/consultation-history-2002-2025/` — dates + headline findings per consultation; Iran's cycle has not completed since 2018 |
| **Oil-consortium wages, AIOC royalties, oil-industry employment (US Bureau of Mines IC 8203, 1963)** | 1910-1962 | **[R]** 6 folders under `data/raw/pahlavi-era-primary-extraction/usbm1963-*` — a genuinely new 130-page primary source (previously unmined by this project). Includes an AGGREGATE ANNUAL WAGES/SALARIES bill paid by the oil Consortium (£15.6M 1955 → £28.3M 1962), AIOC net profits/UK tax/Iran royalty payments 1910-1951 (extends the project's oil-revenue series 45 years earlier than any prior dataset), oil-revenue distribution to Plan Organization/Finance Ministry/NIOC 1957-59, and oil-industry employment by nationality (1939-60) and by company+category (1955-61) |
| Handicrafts beyond carpets | 1930s-2025, non-continuous | **[R]** `data/raw/iran-handicrafts-non-carpet/handicraft-export-value-and-institutional-history/` — aggregate (carpet-excluded) export-value series showing COVID collapse/recovery (1398: $427M → 1399: $120M → 1401: $400M); pottery/ceramics/metalwork/miniature-painting confirmed to have NO embedded economic statistics anywhere (Iranica art-historical articles only), unlike carpets/sugar/tea/tobacco |
| CITES/caviar quota-trade timeline (expanded) | 1998-2006, non-continuous | **[R]** `data/raw/iran-caviar-exports/cites-quota-trade-timeline-1998-2006-retry/` — extends Round 35's single 2006 data point: 1998 baseline, 1998-2004 cumulative (Iran = largest global caviar exporter), June 2001 Paris Agreement exemption, Caspian-wide quota totals 2001-2003 |

See SOURCES.md Round 41 for full source attribution and dead-ends (newspaper cover-price history
and postal-savings history remain confirmed gaps).

---

## Reading this inventory for chart decisions

- Anything marked **[P]** can be charted today with a simple filter — open the file, filter to
  `country_iso3` and a year range, done.
- Anything marked **[R]** exists and is real, but needs a harmonize script (or, for the Pahlavi
  primary-extraction tables, is already clean CSV — see `data/raw/pahlavi-era-primary-extraction/`)
  before it's query-ready the same way.
- **Post-1979 coverage is comprehensive across nearly every theme** — this inventory is not
  understating it. The Pahlavi-era rows are simply thinner because less was measured at the time,
  everywhere in the world, not because anything was left out of this search.
