# Iran insurance sector series (Bimeh Markazi Iran annual reports, FY1379-1391 / 2000-2013)

**New category for this project.** Harmonized 2026-07-13 from
`data/raw/bimeh-markazi-iran/annual-reports/` (8 English-language annual reports, raw PDFs
unchanged). Bimeh Markazi Iran (Central Insurance of the Islamic Republic of Iran) is the
insurance regulator/supervisor and sole domestic reinsurer; each annual report contains both
(a) whole-market Iranian insurance industry statistics and (b) Bimeh Markazi's own financials
as the reinsurer. Both are captured here, kept in separate files.

## Files

| File | Coverage | What it covers |
|---|---|---|
| `market_earned_premium_incurred_loss_1379_1391.csv` | FY1379-1391 (2000-2013), 13 years | **Headline market-wide series.** Total Iranian insurance market earned premium, incurred loss, and loss ratio, one row per (year, edition) — 5 of the 8 reports each publish a rolling "past five/six years" table, so most years appear 2-4 times across editions (see Caveats on revisions). |
| `market_direct_premium_1379_1384.csv` | FY1379-1384 (2000-2005) | Market-wide direct premium (gross premium written, a distinct accounting concept from "earned" premium) and year-on-year growth rate. Only in the earliest (2005/06) edition — later editions do not repeat this specific cut. |
| `market_premium_loss_by_insurance_class.csv` | FY1383-1384 and FY1388-1389 (two 2-year clusters) | Branch-wise (insurance-class) earned premium, incurred loss and loss ratio for Fire, Marine Cargo/Hull, Accident, Motor (P.D. and T.P.L.), Aviation, Engineering, Health, Life, Liability, Credit, Oil & Energy, and Others. Class-name labels are exactly as printed per edition (naming/grouping shifted slightly between 2005/06 and 2011 editions — e.g. "Marine Cargo" vs. "Cargo", a standalone "Liability"/"Credit"/"Oil & Energy" split only appears from the 2011 edition on). |
| `sales_network_by_year.csv` | FY1382-1391 (2003-2013), 10 years | Number of insurance companies, branches, brokers, agents, life-insurance agents, loss adjusters, policies in force, and claims filed — market-wide, one row per (year, edition). |
| `companies_by_ownership_type.csv` | FY1385-1391 (2006-2013) | State-owned vs. private insurance companies and their employee counts — visible structural shift from a state-dominated market (4 state / 15 private in 1385) to an almost fully privatized one (1 state / 26 private by 1391), consistent with Iran's mid-2000s insurance-sector privatization drive mentioned in the source narrative. |
| `bmi_own_financial_highlights.csv` | FY1386-1391 (2007-2013) | Bimeh Markazi Iran's own balance sheet and P&L as the reinsurer (gross/retained/earned premium, incurred loss, net claim, investment income, general expenses, profit, total assets, shareholders' equity, technical reserves, catastrophic risk reserve). **Not the same scale as the market-wide files** — BMI's own gross premium (~35.6 billion IRR in 1391) is roughly one-third of the whole market's earned premium (~99.9 billion IRR in 1391) since BMI only handles compulsory local reinsurance plus its own inward/outward reinsurance business, not primary insurance. |

## Extraction method

4 of the 8 reports (FY1388/89-1391, i.e. `annualreport20092010.pdf`, `annualreport2011.pdf`,
`annualreport2012.pdf`, `annualreport_1391_2012-2013.pdf`) have genuine embedded text layers —
extracted via `pdftotext -layout` and parsed directly (per the raw folder's own manifest,
confirmed `has_extractable_text: true`). The earliest report (`annualreport20052006.pdf`,
FY1384/85, `has_extractable_text: false`) is a scanned/image-only PDF — its three key tables
(Direct Premium 1379-1384, Earned Premium/Incurred Loss/Loss Ratio 1379-1384, branch-wise
premium/loss 1383-1384, and Sales Network 1382-1384) were transcribed visually via
`pdftoppm -png -r 250` page renders (PDF pages 20, 24, 25; note a **printed-page-number offset
of -1 from PDF page number** in this specific file, i.e. PDF page 20 = printed page "19" —
confirmed empirically before transcribing, do not assume 1:1). The other 3 scanned editions
(`annualreport20062007.pdf` FY1385/86, `annualreport20072008.pdf` FY1386/87,
`annualreport20082009.pdf` FY1387/88, all `has_extractable_text: false`) were **not** visually
transcribed this pass — a real, logged incompleteness: their headline figures are already
substantially covered by the overlapping "past five years" tables in the later text-extractable
editions (e.g. FY1386-1388 earned premium/loss appears in the 2010, 2011, and 2012 editions'
own retrospective tables), so the marginal new information from fully mining these 3 middle
editions is low; a future pass could still extract their branch-wise and BMI-own-financials
detail tables for those specific years if wanted.

## Caveats — read before charting

- **Minor cross-edition revisions exist and are preserved, not reconciled**, per this project's
  standing policy: FY1389 earned premium appears as 52,368,591 million IRR in the 2011 edition
  but 52,347,521 million IRR in the 2012 and 1391 editions (a ~21,000 million IRR, <0.1%,
  restatement) — both kept as separate rows tagged by `edition`, never silently picked one.
  Similarly FY1390 loss-ratio figures differ slightly between the 2012 edition (76.58%) and the
  1391 edition (76.3%, rounded to 1 decimal in that edition's own table).
- **"Direct premium" and "earned premium" are different accounting concepts**, both used by the
  source across different tables — direct premium is gross premium written in the period;
  earned premium adjusts for unearned-premium reserve carryover (see the `bmi_own_financial_highlights.csv`
  definitions reproduced from the source itself). Do not conflate the two files.
- **Class/branch naming is inconsistent across editions** (see file description above) — this is
  the source's own presentational change, not a transcription error; kept exactly as printed per
  edition rather than force-normalized.
- **BMI's own financial highlights are reinsurer-scale, not market-scale** — see file description
  above; a common charting mistake would be plotting `bmi_own_financial_highlights.csv`'s gross
  premium against `market_earned_premium_incurred_loss_1379_1391.csv`'s earned premium as if
  they measured the same thing.
- **4 of 8 raw annual reports not yet mined** (FY1385/86-1387/88 editions, all scanned/no-text-
  layer) — see Extraction method above for why this is a reasoned, logged scope decision rather
  than an oversight.

## Sources

Bimeh Markazi Iran (Central Insurance of the Islamic Republic of Iran), English-language Annual
Reports, 5 of 8 editions used this pass:
- `data/raw/bimeh-markazi-iran/annual-reports/annualreport20052006.pdf` (FY1384/85, scanned, visually transcribed)
- `data/raw/bimeh-markazi-iran/annual-reports/annualreport20092010.pdf` (FY1388/89, text layer)
- `data/raw/bimeh-markazi-iran/annual-reports/annualreport2011.pdf` (FY1389/90, text layer)
- `data/raw/bimeh-markazi-iran/annual-reports/annualreport2012.pdf` (FY1390/91, text layer)
- `data/raw/bimeh-markazi-iran/annual-reports/annualreport_1391_2012-2013.pdf` (FY1391, text layer)

Full manifest (all 8 files, retrieved via Wayback Machine since centinsur.ir is geo-blocked from
this network): `data/raw/bimeh-markazi-iran/annual-reports/manifest.json`.
