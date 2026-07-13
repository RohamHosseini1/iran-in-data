# Declassified CIA economic assessments of Iran and the Iran-Iraq War economy (1973-1988)

Five declassified CIA analytical reports mined statistic-by-statistic, in two tidy long-format
CSVs sharing the same schema. All five source PDFs are FOIA-released scans with **zero PDF text
layer** (`pdftotext` returns ~0 characters on every one) — every row here was extracted by
rendering each page to a PNG at `pdftoppm -png -r 200` and reading the image directly, per this
project's established OCR-by-visual-read method. No sub-agents were used; raw PDFs in
`data/raw/cia-iran-economy/` were not modified.

The **NIS 33 "Iran: The Economy" (May 1973)** survey is kept in its own CSV,
`cia_nis33_iran_economy_survey_1973.csv`, rather than merged into the main
`cia_iran_iraq_economic_assessments_1974_1988.csv` file: it is a pre-revolution, pre-war, much
broader-scope economic survey (agriculture, oil/gas/electricity, mining, manufacturing,
government finance, money supply, labor force, balance of payments, trade) rather than a
war-economics assessment, and merging it would have diluted the other file's narrower Iran-Iraq
War focus. Both files share the identical schema below and can be concatenated freely if a
downstream user wants one combined table.

One other PDF in the same raw folder was checked and is **not** represented here:
- `islamic-economic-system-prospects-1987` (NESA*10050*86, "The Islamic Economic System and Its
  Prospects in Iran") — this FOIA release, as scanned, contains **only** its "ADHOC DISSEMINATION
  LIST" routing/distribution-log cover pages (confirmed by sampling pages 1, 6, 10, 20, and 30 —
  all five are pure recipient lists). No analytical report text is present to extract. Confirmed
  source-side gap, not a search failure.

## Schema

`date_label, year, category, subcategory, value, unit, notes, country_iso3, source_dataset, citation`

- **`date_label`** — the period as best characterized from context (a specific year, a named
  scenario like `"1987 scenario c ($15/bbl, 1.4m b/d)"`, or a range like `"1985-1987"`).
- **`year`** — single sortable integer for charting; for multi-year ranges or scenario labels this
  is the anchor/end year — always cross-check `date_label` before treating a row as a precise
  annual data point.
- **`category`** — a coarse economic topic tag (Oil production & trade, External debt, Foreign
  exchange, Trade, Military expenditure, Foreign aid, Demographics & Population, Macro / National
  Accounts, Prices, Labor & Employment, Balance of Payments, etc.) to make cross-file filtering
  easier; not a controlled vocabulary shared with other series in this project.
- **`subcategory`** — the specific line item, often with `-- Iran` / `-- Iraq` suffix for the many
  paired comparison rows.
- **`value`** — blank means the source was illegible, ambiguous, or (for two line/bar charts with
  no printed data labels) a value that would have required pixel-estimating a chart — never
  guessed or filled in. Some values are themselves ranges as printed by the source (e.g.
  `"20-25"` percent) — do not average these down to a point estimate.
- **`unit`**, **`notes`**, **`country_iso3`** (always `IRN`, even for Iraq-side comparison rows —
  this project's per-file convention; use `subcategory`'s `-- Iran`/`-- Iraq` suffix or `notes` to
  distinguish which country a row actually describes), **`source_dataset`**, **`citation`** (full
  document title/number, date, and PDF page for every row).

## The five source documents

| `source_dataset` | Document | Rows | File |
|---|---|---|---|
| `cia-shah-economy-overview-1974` | CIA/OER, "Iran: An Overview of the Shah's Economy" (S-6549), 16 Oct 1974 | 18 | `cia_iran_iraq_economic_assessments_1974_1988.csv` |
| `cia-iran-iraq-economic-balance-1986` | CIA NESA M 86-20082, "Iran-Iraq: The Economic Balance", 6 Jun 1986 | 37 | `cia_iran_iraq_economic_assessments_1974_1988.csv` |
| `cia-iran-iraq-war-weary-economies-1988` | CIA NESA 88-10067, "Iran-Iraq: A Comparison of Two War-Weary Economies" (info as of 10 Nov 1988, post-ceasefire) | 165 | `cia_iran_iraq_economic_assessments_1974_1988.csv` |
| `cia-iran-iraq-gloomy-economic-prospects-1987` | CIA NESA 87-10025, "Iran-Iraq: Gloomy Economic Prospects" (info as of 1 Apr 1987), May 1987 | 263 | `cia_iran_iraq_economic_assessments_1974_1988.csv` |
| `cia-nis33-iran-economy-1973` | National Intelligence Survey 33, "Iran: The Economy" (33/GS/E), May 1973 (research completed Jan 1973) | 1,307 | `cia_nis33_iran_economy_survey_1973.csv` |

**483 rows** in `cia_iran_iraq_economic_assessments_1974_1988.csv` + **1,307 rows** in
`cia_nis33_iran_economy_survey_1973.csv` = **1,790 rows total** across both files.

## Why these matter for this project

This is the project's first primary-source coverage of the **economic cost of the Iran-Iraq War**
on both combatants simultaneously — military-spending burden, war damage, foreign-debt buildup,
and the relative economic strain on Iran vs. Iraq 1980-88 — a gap flagged explicitly in this
project's source-hunt notes. The 1988 and 1987 documents in particular carry rich side-by-side
Iran/Iraq comparison tables (full country-comparison Table 1 in the 1988 doc; current-account
tables for both countries under multiple 1987 oil-price scenarios in the 1987 doc) not available
from any other source in this database.

## Notable content by document

- **shah-economy-overview-1974**: pre-revolution boom-era snapshot — GNP growth (33%/1973,
  40%/1974 expected), Fifth Development Plan spending expansion ($23bn planned -> $45bn actual),
  ~$20bn/year expected oil-revenue outlook, $8bn in 1974 foreign lending/investment commitments,
  $8bn cumulative 1967-73 arms spending, inflation acceleration (6% 1972 -> 11% 1973 -> 16%
  annualized Q1 1974), and top/bottom-20%-income-share inequality figures.
- **iran-iraq-economic-balance-1986**: a snapshot taken as both economies were being squeezed by
  the 1986 oil-price collapse — Iran's 50-55% real FX-earnings drop, $8.5bn 1986 FX-revenue
  estimate, "false employment" + unemployment estimated at 39% of a 12.3m labor force; Iraq's
  FX earnings falling from $11.7bn (1985) to $7.4bn (1986), a first-ever missed $120m payment to
  France, up to $1bn in L/C defaults, and $25bn in cumulative Saudi/Kuwait aid since the war began.
- **iran-iraq-war-weary-economies-1988**: the richest single document — the full Table 1
  side-by-side country comparison (19 line items: demographics, GDP per capita, inflation,
  unemployment, trade, debt, foreign assets, current account), Table 2 (Iraq's projected 1988
  financing sources/requirements), Figures 9/10/13 pie charts with printed percentages (civilian
  import sources, military import sources, Iraq's debt-by-creditor-type), Iraq's $40bn non-Arab
  debt vs. $35bn Gulf-Arab soft debt (kept as separate figures per the source, never summed into
  one "total debt" number), Iran's oil-production-capacity halving (~6m -> ~3m b/d, 1978-88) and
  population surge (37m -> 52m), and the US-Iran trade collapse ($4bn/1978 -> $60m/1987 exports).
- **iran-iraq-gloomy-economic-prospects-1987**: four full data tables — Table 1 (Iran current
  account balance 1984-87 across three 1987 oil-price scenarios: $18/$15/$10 per barrel), Table 2
  (Iraq's 1986 debt-rescheduling agreements with 11 individual creditors, full 1987-92 repayment
  schedule), Table 3 (Iraq current account balance 1984-87, same three-scenario structure), and
  Table 4 (Iraq's full 1987 foreign-payments balance: requirements vs. revenues vs. the resulting
  $3.85bn financing gap). Also: Iraq's $33bn cumulative Arab war aid (of which $27bn from Saudi
  Arabia/Kuwait alone), Iraq's OPEC quota dispute (Baghdad rejecting its assigned 1.46m b/d quota
  in favor of parity with Iran's 2.25m b/d), and Iran's Tehran-ghetto housing statistics (two-thirds
  of families in single-room housing, 6,000 fires/year).
- **nis33-iran-economy-1973**: by far the largest and broadest-scope document in this folder (44pp,
  1,307 rows) — a full pre-revolution economic survey of Pahlavi-era Iran as of research-cutoff
  January 1973. Covers, with complete data tables for nearly every topic: land use and irrigation
  (Figure 4's two land-utilization pie charts), crop production 1961/62-1971/72 (Figure 10, 11
  commodities), opium poppy cultivation by province (Figure 12 — Iran was one of three major legal
  opium producers alongside India and the USSR) and its 1969-1972 output ramp-up after the
  1955-1969 ban, livestock population (Figure 13), crude oil production by operator 1960-1971
  (Figure 17), petroleum revenue 1959/60-1971/72 (a clean, complete 13-year annual series), direction
  of petroleum exports by region (Figure 19), natural gas and electric power buildout (IGAT pipeline
  to the USSR, TAVANIR), metals/minerals production 1962/63-1970/71 (Figure 22, including the newly
  discovered Sar Cheshmeh copper deposit), manufactured-goods output 1965/66-1970/71 (Figure 24,
  passenger cars/TVs/refrigerators/cement etc.), a complete government finance table 1965/66-1971/72
  draft budget (Figure 28: revenue by oil/nonoil/tax type, expenditure, deficit financing), government
  expenditure by function including defense (Figure 29), Third vs. Fourth Development Plan investment
  by sector (Figure 30), money supply 1964/65-1971/72 (Figure 31), labor force by sector (Figure 34),
  a complete balance-of-payments table 1965/66-1971/72 (Figure 35), and full import/export tables by
  commodity and by geographic partner (Figures 36-39). This single document essentially gives the
  project a base-year (1973) cross-section against which the later Iran-Iraq War-era documents'
  economic decline can be measured.

## Charts/figures explicitly skipped (not fabricated around)

Several bar/line charts in these documents show only gridlines with no printed per-year data
labels — extracting exact figures from these would require pixel-estimating bar/line heights,
which this project's no-guessing rule forbids. Skipped:
- war-weary-economies-1988: Figures 1-4 (foreign-assets/imports/debt/aid bar charts), Figures 11-12
  (trade-with-US line charts) — the same underlying trends are captured via the extracted
  narrative-text figures instead.
- gloomy-economic-prospects-1987: Figure 6 (Iran-Iraq oil export revenues 1978-87 line chart —
  the four 1987 scenario endpoints ARE captured via Tables 1/3's current-account exports rows
  instead), Figure 7 (nonoil export revenues line chart), Figure 13 (Iran real GDP per capita
  line chart, 1979-87).
- gloomy-economic-prospects-1987 Figure 12 (Iran share of foreign trade pie charts, 1983 and
  Jan-Jun 1986): only the "Islamic" segment's printed percentage (10.0% / 16.0%) was legible on
  the rendered scan; the East Bloc / Non-Islamic LDCs / West segments were not clearly legible and
  are left out rather than estimated.
- nis33-iran-economy-1973: Figure 1 (international GNP-growth index comparison, 1963=100) and
  Figure 2 (selected economic indicators index, 1959/60=100) — both are index line/bar charts with
  only axis gridlines and no printed per-year numeric labels; skipped for the same pixel-estimation
  reason as above. Figure 3 (GNP distribution, two stacked columns for 1960/61 and 1971/72) — only
  the bottom "Agriculture" row's values (33.1% / 16.2%) were confidently legible against the
  rotated, low-resolution category labels on the rest of the chart; the other rows (public
  services, private services, banking/insurance, transport/communication, water/power,
  construction, industry/mines) were not transcribed rather than risk a mislabeled row. Figure 18
  (consortium ownership organization chart) — an org chart of parent/subsidiary companies with
  percentage ownership shares that did not cleanly sum to 100% on re-reading (scan artifacts around
  small print), so it was skipped entirely rather than publish an internally inconsistent
  breakdown; the consortium's existence and structure are covered in the extracted narrative text
  instead. Figure 32 (labor force by age and sex population pyramid) — a chart with no printed
  numeric labels per age band.

## Caveats — read before charting

- **`country_iso3` is always `IRN`** in this file, including for rows that describe Iraq (via the
  `subcategory` `-- Iraq` suffix). This project's per-file raw-data convention did not add an IRQ
  country code; filter/relabel by `subcategory` text if you need an Iraq-only cut.
- **Every 1987 dollar figure from the gloomy-economic-prospects-1987 document is scenario-
  dependent** on an assumed oil price ($18/$15/$10 per barrel) and export volume — check
  `date_label` for which scenario a given row belongs to before comparing across rows.
  `date_label` values starting with `"1987 (estimate)"` or a plain `"1987"` for narrative-text
  figures use the document's own single "expected case" narrative language, not a table-scenario
  column.
- **Iraq's foreign debt is reported inconsistently across the two 1987/1988 documents' own
  internal framing**: the 1988 doc's Key Judgments cite "$40 billion non-Arab...debt" as the
  headline figure with the $35bn Gulf-Arab soft debt kept explicitly separate; the 1987 doc's
  Table 2 only covers a $6.24bn subset (the specific 1986 rescheduling agreements with 11 named
  creditors) — these are different scopes of "Iraqi debt," not competing measurements of the same
  quantity, and should not be summed or averaged together.
- Some values are ranges exactly as the source printed them (e.g. `"1.6-1.7"` million barrels/day,
  `"20-25"` percent) — the `value` column holds the literal printed string in these cases, not a
  midpoint; downstream charting code should decide how to handle these explicitly rather than
  assuming a clean numeric parse.
- One row (Figure 6 scenario-notes placeholder, `cia-iran-iraq-gloomy-economic-prospects-1987`,
  PDF p.10) has a blank `value` by design — it documents which chart was skipped and why, not a
  missing data point that should be filled in later.
- **`cia_nis33_iran_economy_survey_1973.csv` contains 41 comparator rows for other countries**
  (Iraq/Afghanistan/Turkey agricultural-land shares; Israel/Egypt foreign-debt-to-GNP ratios;
  United Kingdom insurance-receipts share) sitting alongside Iran rows — these are flagged in
  `notes` as "Comparator figure printed alongside Iran's" and still carry `country_iso3 = IRN`
  per this file's convention; filter by `notes`/`subcategory` text, not by country code, if you
  need an Iran-only cut.
- **One narrative/table cross-check discrepancy was preserved, not resolved**, in the NIS-33 file:
  the source's own running text (PDF p.35, printed p.27) states the government's overall deficit
  "rose over 700% to about 61 million rials in 1970/71," while Figure 28 on the same page (PDF
  p.34) tabulates the 1970/71 overall deficit as 60.9 *billion* rials. This is almost certainly a
  typo in the original 1973 document (billion vs. million) — both the narrative row and the
  Figure 28 row are kept as printed, with the discrepancy called out in the narrative row's `notes`
  field, rather than silently "fixed."
- A handful of NIS-33 Figure 38 (nonoil export commodities) cells for 1970/71 were only partially
  legible on the rendered scan (a soap/detergents cell and the nontraditional-exports subtotal);
  where a value could be confirmed via column-sum arithmetic against the other printed cells in the
  same row/column, it was used and the arithmetic cross-check is noted in `notes` — never a freehand
  pixel estimate.
- The NIS-33 Figure 10 (major crops) 1967/68 Barley cell had one partially obscured digit on the
  scan (printed roughly as "1,0?0"); transcribed as 1,030 per best visual read and flagged in
  `notes` — treat this single cell with light caution relative to the rest of the fully legible
  table.
