# Iran Ministry of Industry, Mine and Trade (MIMT) series

Harmonized 2026-07-13 from `data/raw/mimt-iran/statistics-reports/` (6 raw PDFs, unchanged).
This ministry's downloadable archive (recovered via Wayback Machine, live site geo-blocked) is
thin compared to other sources in this project — see honest scope notes below.

## Files

| File | Coverage | What it covers |
|---|---|---|
| `mimt_daily_bulletin_panel_1399.csv` | 5 consecutive business days, 14-21 Bahman 1399 (2-9 Feb 2021) | MIMT's "Daily Bulletin of Important Economic Indicators" — administrative/operational counts: industrial establishment permits, operation licenses, mining exploration/discovery/operation licenses, guild (صنف) permits, e-signature certificates, e-trust-mark issuances, government e-procurement (STAD) system transactions and value, industrial-park land usufruct contracts and area. **This is genuinely thin, single-day operational data, not a macro time series** — included honestly as 5 real observations, not padded or extrapolated. |
| `unido_cip_iran_subindicators_2010_2014.csv` | 2010-2014 | Iran's UNIDO Competitive Industrial Performance (CIP) composite rank/score plus all 8 official sub-indicators (manufacturing value-added per capita, manufacturing export per capita, medium/high-tech share of MVA, MVA share of GDP, medium/high-tech share of manufactured exports, manufactured-exports share of total exports, share of world MVA, share of world manufactured trade) — plus the total number of countries ranked each year (135 in 2010, rising to 144 by 2014), since Iran's *rank* is only meaningful relative to a changing denominator. |
| `unido_cip_regional_comparison_2010_2014.csv` | 2010-2014 | The same CIP rank/score for 11 regional/selected economies as tabulated by MIMT alongside Iran: Israel, Turkey, Saudi Arabia, UAE, Bahrain, Kuwait, Oman, Kazakhstan, Qatar, Iran, Egypt — see Caveats on the Israel country label. |

## Extraction method

All 6 PDFs were checked with `pdftotext -layout` first; **the digit output was found to be
unreliable for this specific source** (a real, load-bearing finding, not a stylistic choice): a
side-by-side comparison of the `pdftotext` output against a `pdftoppm -r 150` visual render of
the same page showed genuine digit corruption beyond simple RTL reversal — e.g. one bulletin's
"operation licenses" cell visually reads 28 but `pdftotext` extracted "82"; a guild-permit count
visually reads 3255 but extracted as "3833" (not a simple transposition, i.e. not fixable by a
mechanical un-reversal rule). **Every number in this folder was therefore read directly from a
`pdftoppm -png -r 150-170` page render with the Read tool, never from `pdftotext` digit output**,
for both the daily bulletins and the Competitive Industrial Performance report.

## Caveats — read before charting

- **`mimt_daily_bulletin_panel_1399.csv` is operational/administrative data, not economic output
  data** — permit and license counts reflect bureaucratic processing volume, which is affected by
  weekday/workload patterns as much as by underlying economic activity. Do not treat day-to-day
  changes as a business-cycle signal.
- **One field visibly did not update between two consecutive reports**: the "industrial park land
  usufruct contracts" count and area are identical (27 contracts, 54,923 sqm) in both the 20 and
  21 Bahman bulletins, with the same "as of 19 Bahman" timestamp printed in both — reproduced
  exactly as printed (a stale/uncorrected source figure, not a transcription duplicate).
- **The MIMT bulletins' commodity/currency-price section and full stock-market section were not
  extracted** — the price section is a chart image with no accompanying data table, and the
  stock-market section only lists each day's top-3 gaining/losing stocks (not the aggregate TSE
  index level itself), which was judged too idiosyncratic/thin relative to extraction effort to
  include as a "series." A future pass wanting daily TSE top-mover data could still mine it from
  these same 5 PDFs.
- **Only 5 of the ~99 archived `statistics_report` PDFs on Wayback were downloaded** (per the raw
  folder's own manifest) — all from one consecutive business-day window in Feb 2021. This is a
  narrow sample, not representative of any broader trend; a future pull of more of the ~99
  archived editions (IDs 390-2162, spanning ~2014-2021 per the manifest) would substantially
  deepen this specific angle if wanted.
- **UNIDO CIP data is externally sourced** (UNIDO's own CIP report/database, republished by MIMT
  as a "Report No. 38" bilingual bulletin) — the underlying manufacturing value-added and export
  figures conceptually overlap with WDI's own manufacturing-value-added-share-of-GDP series
  already in this project, but the **composite CIP rank/score and its full 8-component breakdown
  are not otherwise in this database** and are kept as a genuinely additive, UNIDO-specific
  measure (not a WDI duplicate).
- **`unido_cip_regional_comparison_2010_2014.csv` country label note**: the source PDF labels one
  country row "رژیم اشغالگر قدس" ("the Jerusalem-occupying regime") rather than a neutral country
  name — this is the Islamic Republic's own official diplomatic-nonrecognition terminology for
  Israel, reproduced verbatim in the `country_label_source_fa` column for source fidelity (per
  this project's principle of preserving official-source text as printed), with a neutral
  `country_common_name` column ("Israel") added alongside for usability. This is a labeling
  choice by the original government source, not an editorial judgment made by this project.
- **CIP scores across all countries trend downward 2010→2014** (Iran: 0.054→0.043; most regional
  peers show a similar decline) — this is very likely a denominator effect (countries-ranked grew
  from 135 to 144 over the same period, mechanically diluting every country's world-share-based
  sub-scores) rather than genuine performance decline; the source's own narrative text (reproduced
  in the extraction notes) attributes Iran's *rank* improvement in 2013-2014 despite falling
  *score* to other countries' performance declining even faster. Chart rank and score separately;
  do not read a falling score alone as evidence of declining competitiveness without checking rank.

## Sources

Ministry of Industry, Mine and Trade of Iran (وزارت صنعت، معدن و تجارت), Deputy for Planning,
Statistics and Data Processing Office:
- `data/raw/mimt-iran/statistics-reports/statistics_report_{2157,2159,2160,2161,2162}.pdf` (Daily Bulletins, 2-9 Feb 2021)
- `data/raw/mimt-iran/statistics-reports/industrial_competition_report.pdf` (Competitive Industrial Performance Report 2016, citing UNIDO CIP data through 2014)

Full manifest (recovered via Wayback Machine, live mimt.gov.ir geo-blocked):
`data/raw/mimt-iran/statistics-reports/manifest.json`.
