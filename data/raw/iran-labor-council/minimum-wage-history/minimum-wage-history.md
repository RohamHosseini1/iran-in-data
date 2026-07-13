# Iran — Supreme Labor Council Annual Minimum Wage History

Compiled 2026-07-12. Iran's minimum wage is set once a year by the Supreme Labor Council
(Shora-ye Aali-e Kar), a tripartite body of government, employer, and worker
representatives. The decision is announced around Nowruz (Persian New Year, ~March 20/21)
and takes effect for the new Iranian solar-hijri (SH) year. This is a closely-watched,
politically sensitive figure — announced wage increases routinely trail inflation, which is
itself a recurring point of labor unrest.

**Every figure below is sourced inline. No number in this file was estimated,
interpolated, or fabricated by the compiling agent — where sources conflict, both figures
are shown.** Per project bookkeeping rules, MEK/NCRI-affiliated outlets (ncr-iran.org,
iranfocus.com, mojahedin.org) surfaced during research were excluded as citations; where a
figure only appeared in those outlets it is omitted here, not reproduced secondhand.

## Table 1 — ILOSTAT-compiled series (Gregorian calendar-year tagged)

Source: ILO ILOSTAT indicator `EAR_INEE_NOC_NB` ("Monthly minimum wage", local currency),
downloaded to `data/raw/ilo-minimum-wage/ilo-minimum-wage-by-country/EAR_INEE_NOC_NB_A.csv`
(sha256 `641333661608f12e4135fc244db09cf6f6e6e4fcd2bbe925b5d4ce94533fd3cd`) via
`https://rplumber.ilo.org/data/indicator/?id=EAR_INEE_NOC_NB_A&format=.csv`, retrieved
2026-07-12T18:18:39Z. ILO attributes the Iran series to national source code `EB:3479`
(employer/official administrative source). Cross-checked against the independent aggregator
countryeconomy.com (https://countryeconomy.com/national-minimum-wage/iran, fetched
2026-07-12) — the two series are identical for every overlapping year (1995–2024), which is
strong corroboration that both draw on the same underlying official Iranian submission.

| Gregorian year | Monthly minimum wage (IRR) |
|---|---|
| 1995 | 159,990 |
| 1996 | 207,210 |
| 1997 | 254,460 |
| 1998 | 301,530 |
| 1999 | 361,830 |
| 2000 | 458,010 |
| 2001 | 567,900 |
| 2002 | 698,460 |
| 2003 | 853,380 |
| 2004 | 1,066,000 |
| 2005 | 1,266,784 |
| 2006 | 1,500,000 |
| 2007 | 1,830,000 |
| 2008 | 2,196,000 |
| 2009 | 2,635,200 |
| 2010 | 3,030,000 |
| 2011 | 3,303,000 |
| 2012–2015 | *no ILOSTAT record for Iran in these years* |
| 2016 | 9,299,310 |
| 2017 | 9,299,310 |
| 2018 | 11,112,690 |
| 2019 | 15,170,000 |
| 2020 | 18,340,000 |
| 2021 | 26,554,950 |
| 2022 | 26,554,950 |
| 2023 | 53,073,300 |
| 2024 | 53,073,300 |

**Quirk to flag for future users:** the value repeats across some adjacent Gregorian-year
pairs (2016/2017, 2021/2022, 2023/2024). This is because the Supreme Labor Council's decision
takes effect mid-March (Nowruz), so a rate set for Iranian year *N* is in force for the tail
of one Gregorian year and the first ~2.5 months of the next; ILO's Gregorian-year tagging
appears in some years to record the rate that was in force at (or just before) the start of
the Gregorian year rather than a full recalculation each year. This is an observation about
the ILO series' tagging behavior, not a claim about which Persian year each row corresponds
to — see Table 2 for wage-by-Persian-year, which does not have this ambiguity.

## Table 2 — Persian (solar hijri) year series, most recent decisions

This table anchors each figure to the Iranian calendar year the Supreme Labor Council
actually legislated it for, reconciling the mid-year-transition ambiguity in Table 1.

| Persian year | Gregorian start | Monthly minimum wage (IRR) | YoY increase | Source |
|---|---|---|---|---|
| 1402 | 2023-03-21 | 53,082,840 (=1,769,428/day × 30) per Nouraei & Mostafavi Law Offices; 53,073,300 per ILOSTAT/countryeconomy.com (Table 1) — two independent sources differ by ~0.02%, both retained | 27% (per Nouraei & Mostafavi) | Nouraei & Mostafavi Law Offices, "Iran Sets the Minimum Wage for Workers..." https://nourlaw.com/iran-sets-the-minimum-wage-for-workers-and-salary-increases-for-other-wage-levels/ (fetched 2026-07-12); circular dated 2023-03-20 |
| 1403 | 2024-03-20 | 71,661,840 | ~35% | WageIndicator.org, "Minimum Wage Increased in Iran from 20 March 2024" https://wageindicator.org/work/minimum-wage/updates/2024/minimum-wage-increased-in-iran-from-20-march-2024-october-10-2024 (fetched 2026-07-12) |
| 1404 | 2025-03-21 | 103,909,680 (~103.99 million) | 45% | PressTV (state-media-attributed), "Iran raises minimum wage for workers by 45%" https://www.presstv.ir/Detail/2025/03/16/744557/Iran-minimum-wage-increase-announcement (fetched 2026-07-12), decision dated 2025-03-16 after the 335th Supreme Labor Council session; figure corroborated by Iran International, "Iran's 45% minimum wage increase faces criticism over inflation gap" https://www.iranintl.com/en/202503165034 |
| 1405 | 2026-03-20 | 166,255,500 | ~60% (59.96%) | Euronews, "Iran raises minimum wage by 60% as war and sanctions decimate household budgets" https://www.euronews.com/business/2026/03/17/iran-raises-minimum-wage-to-60-as-war-and-sanctions-decimate-household-budgets (fetched 2026-07-12), decision dated 2026-03-17, announced by Labour Minister Ahmad Meydari; figure corroborated by WageIndicator.org, "Minimum Wage Increased in Iran from 20 March 2026" https://wageindicator.org/work/minimum-wage/updates/2026/minimum-wage-increased-in-iran-from-20-march-2026-march-22-2026 (fetched 2026-07-12) and by Arab News / Middle East Eye reporting on the same 60% figure |

Context on 1405 (per Euronews, above): labor groups argued the family basic-needs basket
required roughly 580 million rials/month at the time of the decision, with food-price
inflation reported near 90%; the 166.26 million rial base wage was criticized as inadequate
despite being the largest single-year jump in the observed series. Mandatory supplements
(housing allowance, food/child allowances, an annual Eid bonus, and — per PressTV, for a
worker with two children including housing and pension contributions — 163.5 million rials
annually in the 1404 case) raise effective take-home pay above the bare base figure quoted
above; those supplement figures were not independently itemized for every year and are not
tabulated here to avoid conflating base wage with total compensation.

## Sources consulted but excluded or not usable

- **ncr-iran.org (NCRI)** and **iranfocus.com**: appeared repeatedly in search results with
  specific rial figures (e.g. claims about a "330 million rial" 1403 worker demand, and a
  "600 million rial" 1405 demand). Excluded per `docs/bookkeeping.md` source-reliability
  policy (MEK/NCRI-affiliated). Where the same claim (e.g. labor groups' ~600 million rial
  demand for 1405) was independently corroborated by Euronews (non-excluded, cited above),
  it is retained; the NCRI-only figures are not reproduced.
- **CEIC Data** (ceicdata.com/en/iran/minimum-monthly-wage): returned HTTP 403 on fetch
  attempt 2026-07-12; likely paywalled/blocked for automated access. Not used.
- Pre-1995 data: no source located during this pass that met the sourcing bar (ILOSTAT's
  Iran series in `EAR_INEE_NOC_NB_A.csv` starts at 1995; no earlier compiled series found).
  Flagged as a gap for a future research pass — Bharier's *Economic Development in Iran
  1900-1970* (already in `data/raw/historical-docs/` per SOURCES.md) may cover pre-1979 wage
  regulation but was not re-consulted in this session.

## Cross-reference

Raw machine-readable ILO figures for Table 1 live at
`data/raw/ilo-minimum-wage/ilo-minimum-wage-by-country/EAR_INEE_NOC_NB_A.csv` and
`EAR_INEE_CUR_NB_A.csv` (the latter also has a PPP-converted variant). This markdown file is
the curated/narrative companion for the Persian-year framing that the raw ILO extract cannot
provide on its own.
