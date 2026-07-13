# Iran dams & water infrastructure (1937–1978)

Harmonized 2026-07-13 from seven raw World Bank Archives extraction folders under
`data/raw/pahlavi-era-primary-extraction/` (all immutable, unchanged) into one combined
folder, mirroring the `specialty_goods_series/` pattern: small, well-documented, per-topic
CSVs, one row per statistic/component, nothing interpolated or fabricated. Every raw source
had already been manually transcribed with visual verification (`pdftoppm -r 200/300` render
+ Read-tool comparison against the raw OCR text layer) by an earlier round of this project;
this pass only re-copies each table through Python's `csv` module (normalizing quoting) and
adds this README — no numeric values were touched.

All seven raw source PDFs live in `data/raw/world-bank-archives-iran/historical-documents/`.

## Files

| File | Coverage | What it covers |
|---|---|---|
| `major_dams_specifications_1971.csv` | up to end of 1971 | The "Dams of Iran" annex — technical/economic specs for 19 reservoir dams: 12 constructed (Amir Kabir/Karaj, Shahbanu Farah/Sefid Rud, Dez, Latian, Shah Abbas-e-Kabir/Zayandehrud, Voshmgir, Aras, and others), 2 under construction (Karun-1/Reza Shah-e-Kabir, Taleqan), 5 under study. Columns: dam type, river, location, height, reservoir capacity, regulated annual capacity, generator capacity, irrigated area, year operational, cost of dam, cost of irrigation, consultants. |
| `diversion_dams_specifications_1937_1967.csv` | 1937–1967 | 15 smaller-scale diversion dams (crest length, height, cultivated area, utilization date) — distinct from the major reservoir dams above; these are low-head irrigation-diversion structures, not hydropower/storage dams. |
| `reservoir_water_control_forecast_4th_5th_plan.csv` | 4th Plan (1968–72) end-point + 5th Plan (1973–77) forecast | Water controlled by reservoir dams and public-sector water supply (cities/industry vs. agriculture), broken out by 10 regional zones (Khuzestan, Fars, Azarbayejan, Tehran, Esfahan, etc.) plus national total. |
| `dez_dam_key_parameters_1960_appraisal.csv` | 1957 (conception)–1974 (full-scheme target) | Dez Multipurpose Project's engineering/investment/schedule parameters at World Bank appraisal: dam height (190m), reservoir capacity (3,350 Mm³), installed hydro capacity (520 MW ultimate / 130 MW initial), irrigation targets (110,000 ha full scheme), total investment ($83M pilot + $82M full-scheme addition), consultants (Development & Resources Corporation, Electroconsult, Nederlandsche Heidemaatschappij). |
| `dez_dam_cost_estimate_by_component_1960.csv` | 1960 appraisal, Section D to 1984 | Line-item cost breakdown (foreign currency / local currency / total, million rials) for the Dez Dam and power facilities: dam & common works, powerhouse + first two 65MW units, transmission plant, and planned additions (3rd–6th generating units) through 1984. |
| `ghazvin_project_appraisal_cost_parameters_1967.csv` | 1967 appraisal | Ghazvin (Qazvin) area development project's cost estimate, IBRD financing plan (5-year expenditure schedule), and key irrigation/population parameters at appraisal (443,000 ha total project area, 250,000 people, 273 villages). |
| `ghazvin_project_completion_audit_1978.csv` | 1962 (conception)–1977 (audit) | Project Performance Audit: original plan vs. actual outcomes for the same Ghazvin project — loan disbursed ($9.2M of $22M approved, $12.8M cancelled), actual cost ($32.5M vs. $50.9M appraised, 64%), and the economic rate of return **collapsing from an appraised 10% to ~0%**, attributed to overestimated water supplies and a rejected private-well-expropriation understanding. |

## Schema note

Each file keeps the column structure native to its source table (a wide, cross-tabulated
engineering/cost table reads far more usefully in its original shape than force-melted into a
generic `year,metric,value` schema — e.g. `major_dams_specifications_1971.csv`'s 16 columns
are all properties of the *same* dam-row, not a time series). This mirrors how
`specialty_goods_series/` also kept each file's own natural schema rather than imposing one
schema project-wide.

## Two-project narrative arc worth noting for chart-planning

**Dez Dam (appraised 1960, operational 1963) and Ghazvin (appraised 1967, audited 1978) are a
matched pair of "before and after" World Bank irrigation projects** — Dez's appraisal
documents ambitious multipurpose (power+irrigation+flood control) targets with a proposed but
unstated-amount Bank loan; Ghazvin's *completion audit* (the only one of the two projects for
which a completion audit was found in this archive) shows the gap between appraisal-stage
projections and reality: economic rate of return collapsed from 10% (appraised) to
approximately 0% (actual), driven mainly by overestimated groundwater well-field yield
(~10% below appraisal) and a financing/expropriation dispute. This is a genuinely useful,
citable data point about Pahlavi-era development-project execution risk, not just input
statistics — worth flagging explicitly on any chart or narrative built from this file, since
it is one of the few instances in this project's holdings of an *audited actual-vs-planned*
outcome rather than a plan or a snapshot.

## Caveats — read before charting

- **`major_dams_specifications_1971.csv`** has two flagged transcription ambiguities
  preserved exactly as printed in the source (not corrected): a footnote-marker
  placement issue on the Shah Esmail row's cultivation-area column, and a footnote-marker
  layout ambiguity on the Dez ("Mohammad Reza Shah-e-Pahlavi") row — see each row's `notes`
  cell. The dam named after the Shah ("Mohammad Reza Shah-e-Pahlavi") is what is universally
  known today as the **Dez Dam**; "Shahbanu Farah" = **Sefid Rud Dam**; "Reza Shah-e-Kabir" =
  **Karun-1 / Shahid Abbaspour Dam**; "Dariyush-e-Kabir" has no listed modern-name equivalent
  in the source but is on the Kor river at Dorudzan (a name still in modern use). These
  Pahlavi-era honorific names were retained exactly as printed since renaming them would be an
  editorial change to primary-source content; the `common_or_modern_name` column supplies the
  post-1979 name where the source itself provided one.
- **`dez_dam_key_parameters_1960_appraisal.csv`**: the reservoir's "useful life" figure is
  illegible/cut off in the source at the exact point the number should appear — left blank
  with a note rather than guessed. The exact World Bank loan amount is likewise not stated on
  the appraisal summary pages that were extracted (the appraisal confirms a loan was "suitable"
  but the dollar figure itself is on a page not captured in this extraction round) — a real,
  logged gap, not a silent omission.
- **`ghazvin_project_completion_audit_1978.csv`**: the "Follow-on works cost" row mixes an
  original-estimate cell (left blank, illegible/not given in rials at that point in the
  source) against an actual/revised figure (Rls 8 billion, footnoted as a large cost
  escalation) — preserved as printed, not reconciled.
- **Currency/units differ between files by design of the underlying reports**: Dez Dam figures
  are given in both million rials and million USD at the report's stated 75 Rials = US$1
  convenience rate; Ghazvin's 1967 appraisal is in USD millions throughout; Ghazvin's 1978
  audit gives both the appraisal-date rate (75.75 Rials/US$1) and the actual-period average
  rate (73.00 Rials/US$1) — do not assume a single fixed FX rate applies across all files in
  this folder.
- **Dam-count note**: the project brief that commissioned this harmonization pass referenced
  "18 dams" in the water-supply-sewerage annex; the actual table has 19 rows (12 constructed +
  2 under construction + 5 under study) — likely a rounding/miscount in the brief, not a data
  problem; all 19 rows from the source table are included here.

## Sources

- World Bank Archives (`openknowledge.worldbank.org`), Iran country documents, all already
  present in `data/raw/world-bank-archives-iran/historical-documents/`:
  - `1975_water_supply_sewerage_vol2_annexes.pdf` — Volume II Annex 4, Tables 4.1 (major dams),
    4.2 (diversion dams), 4.3 (reservoir/water-control forecast by zone).
  - `1960_dez_multipurpose_project_appraisal.pdf` — Annex 1 (cost estimate) + Summary and
    Conclusions / Introduction sections (key parameters).
  - `1967_ghazwin_development_project_appraisal.pdf` — paras 3.04–3.10, 4.02, 4.21–4.24.
  - `1978_ghazwin_development_project_completion.pdf` — Project Performance Audit Basic Data
    Sheet (Sections A–D) + Highlights.

Full manifests and extraction methods (including exact PDF page numbers and the visual-
verification cross-checks performed, e.g. Dez height/reservoir figures matched against known
published values): `data/raw/pahlavi-era-primary-extraction/wb1975water-*/manifest.json`,
`wb1960dez-*/manifest.json`, `wb1967ghazvin-*/manifest.json`, `wb1978ghazvin-*/manifest.json`.
