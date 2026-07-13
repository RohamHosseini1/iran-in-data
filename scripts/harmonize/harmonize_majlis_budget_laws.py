"""Harmonize the 24 Majlis historical budget-law HTML texts (Persian primary legal documents,
data/raw/majlis-historical-budget-laws/lamtakam-mirror-1301-1363/) into tidy processed CSVs.

METHOD: every figure below was extracted by converting each raw HTML file to plain text
(BeautifulSoup, tags stripped) and closely reading the actual law text -- specifically the
"ماده واحده" (single article) clause that states the fiscal year's headline revenue/expenditure
figures, which Iranian budget laws print BOTH in spelled-out Persian words AND as a parenthetical
digit string (e.g. "... بالغ بر پنجاه و ... (50603905000) ریال ..."). The digit string is what was
transcribed; the spelled-out words were used as a cross-check, not the primary source of the
number. Every multi-level total that had two or more stated component figures was independently
summed and checked against the printed parent total -- where they matched exactly this is noted;
where they did NOT match exactly, BOTH the components and the printed parent total are kept and the
discrepancy is flagged in `notes`, never silently resolved to one number (this project's standing
no-fabrication / never-pick-a-winner policy). Where a sub-component (e.g. the state-enterprise
budget) was not itself printed in the single-article summary clause, its value here is computed as
(printed total) - (printed sub-parts) and explicitly labeled `value_source=implied residual` --
this is arithmetic on numbers that WERE printed, not a fabricated figure, but it is flagged
distinctly from figures that were themselves directly printed in the source.

GENUINE DATA-QUALITY FINDING: two of the three FY1301 single-ministry files have their filenames
SWAPPED relative to their actual body-text content (confirmed by reading the full law text, not
just the manifest's title metadata) -- see README.md "A mislabeling found in the raw files" section.
This script uses the CORRECT ministry attribution based on actual text content, not the raw
filename, while still citing the (mislabeled) raw filename for traceability.

Raw HTML files are never modified.
"""
import csv

OUT = "data/processed/majlis_budget_law_series"
RAWDIR = "data/raw/majlis-historical-budget-laws/lamtakam-mirror-1301-1363"

def ah_to_western_end_year(ah_year):
    """Iran's Solar Hijri fiscal year N runs ~21 March (N+621) to ~20 March (N+622).
    This project's convention (matching the Pahlavi-archival-series harmonization) maps a
    fiscal year to the LATER Western year, i.e. the year in which it ends."""
    return ah_year + 622


# ============================================================================
# FILE 1: National (whole-country) budget totals by fiscal year
# ============================================================================
NATIONAL_ROWS = [
    # --- FY1341 (first consolidated "whole country" law found in this collection) ---
    dict(fy=1341, law_type="main", hierarchy="Grand Total", revenue=86326243863, expenditure=90440043863,
         value_source="printed", notes="Sum of the 5 components below verified to match exactly (rev: 39503332000+17190714863+5074450000+8542747000+16015000000=86326243863; exp: 43617132000+17190714863+5074450000+8542747000+16015000000=90440043863).",
         approved="17 Aban 1343 AH solar (retroactive, ~2 years after FY end)", gazette="5839",
         source_file="budget-law-1341-whole-country.html"),
    dict(fy=1341, law_type="main", hierarchy="General revenue/expenditure (درآمد/هزینه عمومی)", revenue=39503332000, expenditure=43617132000,
         value_source="printed", notes="Component 1 of 5 in the law's own 'خلاصه بودجه' (budget summary) table.",
         approved="17 Aban 1343 AH solar", gazette="5839", source_file="budget-law-1341-whole-country.html"),
    dict(fy=1341, law_type="main", hierarchy="Earmarked revenue/expenditure (درآمد/هزینه اختصاصی)", revenue=17190714863, expenditure=17190714863,
         value_source="printed", notes="Component 2 of 5.", approved="17 Aban 1343 AH solar", gazette="5839",
         source_file="budget-law-1341-whole-country.html"),
    dict(fy=1341, law_type="main", hierarchy="Industrial & mining companies (شرکتهای صنعتی و معدنی)", revenue=5074450000, expenditure=5074450000,
         value_source="printed", notes="Component 3 of 5.", approved="17 Aban 1343 AH solar", gazette="5839",
         source_file="budget-law-1341-whole-country.html"),
    dict(fy=1341, law_type="main", hierarchy="National Iranian Oil Company (شرکت ملی نفت)", revenue=8542747000, expenditure=8542747000,
         value_source="printed", notes="Component 4 of 5. Law's own footnote 1: NIOC total including 375 million rials sourced from oil revenue already counted within general revenue/expenditure is 8,917,747,000 rials (not used here -- kept as printed component to avoid double count).",
         approved="17 Aban 1343 AH solar", gazette="5839", source_file="budget-law-1341-whole-country.html"),
    dict(fy=1341, law_type="main", hierarchy="Plan Organization (سازمان برنامه)", revenue=16015000000, expenditure=16015000000,
         value_source="printed", notes="Component 5 of 5.", approved="17 Aban 1343 AH solar", gazette="5839",
         source_file="budget-law-1341-whole-country.html"),

    # --- FY1343 (revised) ---
    dict(fy=1343, law_type="revised (اصلاحی)", hierarchy="Grand Total", revenue=140952677000, expenditure=144444162000,
         value_source="printed", notes="Deficit of 3,491,485,000 rials, entirely traceable to the General+Class-A-earmarked subset below (54,095,390,000-50,603,905,000=3,491,485,000, exact match) -- state-companies/Plan-Org components not itemized in the single-article clause read.",
         approved="4 Mordad 1343 AH solar (signed 8 Mordad, published 31 Mordad)", gazette="5682",
         source_file="budget-law-1343-revised-whole-country.html"),
    dict(fy=1343, law_type="revised (اصلاحی)", hierarchy="General + Class-A earmarked revenue/expenditure subset", revenue=50603905000, expenditure=54095390000,
         value_source="printed", notes="Explicitly printed subset of the grand total (general-treasury-financed portion only, excludes state companies/Plan Organization).",
         approved="4 Mordad 1343 AH solar", gazette="5682", source_file="budget-law-1343-revised-whole-country.html"),

    # --- FY1344 ---
    dict(fy=1344, law_type="main", hierarchy="Grand Total", revenue=175046000000, expenditure=176662000000,
         value_source="printed", notes="Deficit of 1,616,000,000 rials overall; the General+Class-A-earmarked subset below has a smaller deficit of 1,394,050,000 -- the two deficits do NOT match exactly (unlike FY1343), implying additional deficit-bearing components outside the subset that were not itemized in the clause read. Not reconciled, kept as printed.",
         approved="27 Esfand 1343 AH solar (signed 1 Farvardin 1344, published 30 Farvardin 1344)", gazette="5871",
         source_file="budget-law-1344-whole-country.html"),
    dict(fy=1344, law_type="main", hierarchy="General + Class-A earmarked revenue/expenditure subset", revenue=58301631000, expenditure=59695681000,
         value_source="printed", notes="Explicitly printed subset (general-treasury-financed portion only).",
         approved="27 Esfand 1343 AH solar", gazette="5871", source_file="budget-law-1344-whole-country.html"),

    # --- FY1346 ---
    dict(fy=1346, law_type="main", hierarchy="Grand Total", revenue=217231910000, expenditure=217231910000,
         value_source="printed", notes="Balanced on paper (revenue=expenditure), as were most FY laws through the mid-1350s.",
         approved="28 Esfand 1345 AH solar (signed 29 Esfand 1345, published 17 Farvardin 1346)", gazette="6444",
         source_file="budget-law-1346-whole-country.html"),
    dict(fy=1346, law_type="main", hierarchy="General + Class-A earmarked revenue/expenditure subset", revenue=73256131000, expenditure=73256131000,
         value_source="printed", notes="Explicitly printed subset, also balanced.",
         approved="28 Esfand 1345 AH solar", gazette="6444", source_file="budget-law-1346-whole-country.html"),

    # --- FY1352 (baseline just before the 1973-74 oil-price shock) ---
    dict(fy=1352, law_type="main", hierarchy="Grand Total", revenue=692731602000, expenditure=692731602000,
         value_source="printed", notes="Balanced on paper. Sum of the 4 lettered parts below verified exact: 470583786000+18163194000+196893219000+7091403000=692731602000.",
         approved="27 Esfand 1351 AH solar (signed 29 Esfand 1351, published 2 Ordibehesht 1352)", gazette="8225",
         source_file="budget-law-1352-whole-country.html"),
    dict(fy=1352, law_type="main", hierarchy="Part A: General government budget (بودجه عمومی دولت)", revenue=470583786000, expenditure=470583786000,
         value_source="printed", notes="", approved="27 Esfand 1351 AH solar", gazette="8225", source_file="budget-law-1352-whole-country.html"),
    dict(fy=1352, law_type="main", hierarchy="Part B: Ministries' earmarked-revenue budget", revenue=18163194000, expenditure=18163194000,
         value_source="printed", notes="", approved="27 Esfand 1351 AH solar", gazette="8225", source_file="budget-law-1352-whole-country.html"),
    dict(fy=1352, law_type="main", hierarchy="Part C: State companies & profit-making institutions", revenue=196893219000, expenditure=196893219000,
         value_source="printed", notes="", approved="27 Esfand 1351 AH solar", gazette="8225", source_file="budget-law-1352-whole-country.html"),
    dict(fy=1352, law_type="main", hierarchy="Part D: Other institutions", revenue=7091403000, expenditure=7091403000,
         value_source="printed", notes="", approved="27 Esfand 1351 AH solar", gazette="8225", source_file="budget-law-1352-whole-country.html"),

    # --- FY1353 (revised) & FY1354 (original), one combined law, direct evidence of the 1973-74 oil-shock windfall ---
    dict(fy=1353, law_type="revised (اصلاحی)", hierarchy="Grand Total", revenue=2082635827000, expenditure=2082635827000,
         value_source="printed", notes="Balanced on paper. More than triple FY1352's 692.7bn rial budget -- direct evidence of the 1973-74 oil-price-quadrupling windfall hitting the government's books.",
         approved="15 Aban 1353 AH solar (signed 19 Aban, published 14 Azar; combined law also covers FY1354 below)",
         gazette="8787", source_file="budget-law-1353-revised-and-1354-whole-country.html"),
    dict(fy=1353, law_type="revised (اصلاحی)", hierarchy="General government budget (بودجه عمومی دولت)", revenue=1604701558000, expenditure=1604701558000,
         value_source="printed", notes="Sub-broken into general revenue 1,580,720,770,000 + ministries' earmarked revenue 23,980,788,000 = 1,604,701,558,000 (exact).",
         approved="15 Aban 1353 AH solar", gazette="8787", source_file="budget-law-1353-revised-and-1354-whole-country.html"),
    dict(fy=1354, law_type="main", hierarchy="Grand Total", revenue=2447174330000, expenditure=2447174330000,
         value_source="printed", notes="Balanced on paper. Set in the same single-article clause as the FY1353 revision above (same law, two fiscal years).",
         approved="15 Aban 1353 AH solar", gazette="8787", source_file="budget-law-1353-revised-and-1354-whole-country.html"),
    dict(fy=1354, law_type="main", hierarchy="General government budget (بودجه عمومی دولت)", revenue=1790729484000, expenditure=1790729484000,
         value_source="printed", notes="Sub-broken into general revenue 1,765,991,677,000 + ministries' earmarked revenue 24,737,807,000 = 1,790,729,484,000 (exact).",
         approved="15 Aban 1353 AH solar", gazette="8787", source_file="budget-law-1353-revised-and-1354-whole-country.html"),

    # --- FY1355 (uses the short-lived Imperial 2535 calendar alongside AH-solar 1355) ---
    dict(fy=1355, law_type="main", hierarchy="Grand Total", revenue=2960248448000, expenditure=3105248448000,
         value_source="printed", notes="Deficit of exactly 145,000,000,000 rials -- same exact deficit amount recurs at every nested level below (General Government Budget level, and its own General-revenue-only sub-level), confirming the entire deficit sits in one clean traceable line, not spread/obscured across components. Law's title uses '2535' (Imperial/Shahanshahi calendar Mohammad Reza Shah introduced in 1355/1976, abandoned 1357/1978) alongside ordinary AH-solar 1355.",
         approved="21 Esfand 1354 AH solar (signed 27 Esfand, published 15 Farvardin 1355)", gazette="9102",
         source_file="budget-law-1355-whole-country.html"),
    dict(fy=1355, law_type="main", hierarchy="General government budget (بودجه عمومی دولت)", revenue=1911784286000, expenditure=2056784286000,
         value_source="printed", notes="Deficit of 145,000,000,000 rials again -- same amount as the grand-total deficit.",
         approved="21 Esfand 1354 AH solar", gazette="9102", source_file="budget-law-1355-whole-country.html"),
    dict(fy=1355, law_type="main", hierarchy="General government budget > general revenue/expenditure (الف)", revenue=1867728217000, expenditure=2012728217000,
         value_source="printed", notes="Deficit of 145,000,000,000 rials again -- the deficit's exact origin point; the sibling earmarked-revenue line (ب, 44,056,069,000) is separately balanced.",
         approved="21 Esfand 1354 AH solar", gazette="9102", source_file="budget-law-1355-whole-country.html"),
    dict(fy=1355, law_type="main", hierarchy="General government budget > earmarked revenue/expenditure (ب)", revenue=44056069000, expenditure=44056069000,
         value_source="printed", notes="Balanced (not part of the deficit).", approved="21 Esfand 1354 AH solar", gazette="9102",
         source_file="budget-law-1355-whole-country.html"),

    # --- FY1358 (two near-duplicate registrations found; see README on the discrepancy) ---
    dict(fy=1358, law_type="main (Official Gazette 52866)", hierarchy="Grand Total (headline, round figure as printed)", revenue=2463000000000, expenditure=2463000000000,
         value_source="printed", notes="Printed as a ROUND headline figure ('...بالغ بر دو هزار و چهارصد و شصت و سه ... میلیارد ریال...', i.e. exactly 2,463 billion with no finer digits) in the single-article's opening sentence -- but the two lettered components immediately below sum to 2,440,140,371,000, NOT 2,463,000,000,000 (discrepancy of 22,859,629,000). Both figures kept as printed; not reconciled.",
         approved="27 Mordad 1358 AH solar", gazette="52866", source_file="budget-law-1358-whole-country.html"),
    dict(fy=1358, law_type="main (Official Gazette 52866)", hierarchy="Part A: general revenue/expenditure", revenue=2358042371000, expenditure=2358042371000,
         value_source="printed", notes="", approved="27 Mordad 1358 AH solar", gazette="52866", source_file="budget-law-1358-whole-country.html"),
    dict(fy=1358, law_type="main (Official Gazette 52866)", hierarchy="Part B: earmarked revenue/expenditure of ministries", revenue=82098000000, expenditure=82098000000,
         value_source="printed", notes="", approved="27 Mordad 1358 AH solar", gazette="52866", source_file="budget-law-1358-whole-country.html"),
    dict(fy=1358, law_type="bill/companion registration (Official Gazette 10066)", hierarchy="Grand Total (duplicate of the above)", revenue=2463000000000, expenditure=2463000000000,
         value_source="printed", notes="This file (budget-bill-1358-whole-country.html, approved as law 25 Mordad 1358, published 22 Shahrivar, Gazette 10066) states IDENTICAL figures to budget-law-1358-whole-country.html (Gazette 52866) verbatim, word-for-word in its single-article clause -- almost certainly the same enactment registered/gazetted twice (an earlier legislative-process printing vs. the final law), not a second real FY1358 budget. Kept as a separate row for traceability but NOT summed as an additional FY1358 data point in any total.",
         approved="Approved as law 25 Mordad 1358 AH solar", gazette="10066", source_file="budget-bill-1358-whole-country.html"),

    # --- FY1360 through FY1363 (post-revolution, first elected-Majlis budgets, Iran-Iraq war) ---
    dict(fy=1360, law_type="main", hierarchy="Grand Total", revenue=3165981700000, expenditure=3165981700000,
         value_source="printed", notes="Balanced. Sum of A+B verified exact (3037000000000+128981700000=3165981700000). First budget passed by the newly elected Islamic Consultative Assembly rather than the Revolutionary Council. Opens with 'Bismillah al-Rahman al-Rahim.'",
         approved="7 Mordad 1360 AH solar", gazette="", source_file="budget-law-1360-whole-country.html"),
    dict(fy=1360, law_type="main", hierarchy="Part A: general revenue/expenditure", revenue=3037000000000, expenditure=3037000000000,
         value_source="printed", notes="", approved="7 Mordad 1360 AH solar", gazette="", source_file="budget-law-1360-whole-country.html"),
    dict(fy=1360, law_type="main", hierarchy="Part B: earmarked revenue/expenditure of ministries", revenue=128981700000, expenditure=128981700000,
         value_source="printed", notes="", approved="7 Mordad 1360 AH solar", gazette="", source_file="budget-law-1360-whole-country.html"),

    dict(fy=1361, law_type="main", hierarchy="Grand Total", revenue=3104626793000, expenditure=3104626793000,
         value_source="printed", notes="Balanced. Sum of A+B verified exact (2977394914000+127231879000=3104626793000). Roughly flat vs FY1360 despite Iran-Iraq war spending pressure.",
         approved="26 Esfand 1360 AH solar", gazette="", source_file="budget-law-1361-whole-country.html"),
    dict(fy=1361, law_type="main", hierarchy="Part A: general revenue/expenditure", revenue=2977394914000, expenditure=2977394914000,
         value_source="printed", notes="", approved="26 Esfand 1360 AH solar", gazette="", source_file="budget-law-1361-whole-country.html"),
    dict(fy=1361, law_type="main", hierarchy="Part B: earmarked revenue/expenditure of ministries", revenue=127231879000, expenditure=127231879000,
         value_source="printed", notes="", approved="26 Esfand 1360 AH solar", gazette="", source_file="budget-law-1361-whole-country.html"),

    dict(fy=1362, law_type="main", hierarchy="Grand Total", revenue=5816156938000, expenditure=5816156938000,
         value_source="printed", notes="Balanced. Nearly double FY1361 -- wartime spending growth and inflation. 'Part 1' (general govt) below is explicit; the remainder (Part 2, state companies, not itemized in the clause read) is a computed residual.",
         approved="26 Esfand 1361 AH solar", gazette="", source_file="budget-law-1362-whole-country.html"),
    dict(fy=1362, law_type="main", hierarchy="Part 1: general government budget", revenue=3727943094000, expenditure=3727943094000,
         value_source="printed", notes="Sub-broken: general revenue 3,555,108,289,000 + earmarked 172,834,805,000 = 3,727,943,094,000 (exact).",
         approved="26 Esfand 1361 AH solar", gazette="", source_file="budget-law-1362-whole-country.html"),
    dict(fy=1362, law_type="main", hierarchy="Part 2: state companies & profit-making institutions (implied)", revenue=2088213844000, expenditure=2088213844000,
         value_source="implied residual (Grand Total minus Part 1; not itself printed in the single-article clause)",
         notes="Computed as 5816156938000-3727943094000.", approved="26 Esfand 1361 AH solar", gazette="",
         source_file="budget-law-1362-whole-country.html"),

    dict(fy=1363, law_type="main", hierarchy="Grand Total", revenue=6550834894000, expenditure=6550834894000,
         value_source="printed", notes="Balanced. 'General government budget' portion (Part A) explicit; state-companies portion (Part B) not itemized in the clause read, computed as residual.",
         approved="30 Esfand 1362 AH solar", gazette="", source_file="budget-law-1363-whole-country.html"),
    dict(fy=1363, law_type="main", hierarchy="Part A: general government budget", revenue=4087830110000, expenditure=4087830110000,
         value_source="printed", notes="Sub-broken: general revenue 3,870,606,520,000 + earmarked 217,223,590,000 = 4,087,830,110,000 (exact).",
         approved="30 Esfand 1362 AH solar", gazette="", source_file="budget-law-1363-whole-country.html"),
    dict(fy=1363, law_type="main", hierarchy="Part B: state companies & profit-making institutions (implied)", revenue=2463004784000, expenditure=2463004784000,
         value_source="implied residual (Grand Total minus Part A; not itself printed)",
         notes="Computed as 6550834894000-4087830110000.", approved="30 Esfand 1362 AH solar", gazette="",
         source_file="budget-law-1363-whole-country.html"),

    # --- FY1365 (Iran-Iraq war ongoing) ---
    dict(fy=1365, law_type="main", hierarchy="Grand Total", revenue=7465265286000, expenditure=7465265286000,
         value_source="printed", notes="Balanced. Continued rapid nominal growth vs FY1363's 6.55tn rials (FY1364 general budget law itself was NOT located -- only the separate FX-allocation law survives, see forex file).",
         approved="26 Esfand 1364 AH solar", gazette="11969", source_file="budget-law-1365-whole-country.html"),
    dict(fy=1365, law_type="main", hierarchy="Part A: general government budget", revenue=4157827189000, expenditure=4157827189000,
         value_source="printed", notes="Sub-broken: general revenue 3,889,065,124,000 + earmarked 268,762,065,000 = 4,157,827,189,000 (exact). Note: the source's spelled-out Persian words for the expenditure side of the general-revenue sub-line are grammatically malformed ('سه هزار و سیصد و هشتصد و نه میلیارد...') -- almost certainly an OCR/transcription defect in the ORIGINAL lamtakam.com HTML text, not in this project's reading of it; the parenthetical digit string (3889065124000) is unambiguous and was used, not the malformed words.",
         approved="26 Esfand 1364 AH solar", gazette="11969", source_file="budget-law-1365-whole-country.html"),
    dict(fy=1365, law_type="main", hierarchy="Part B: state companies & profit-making institutions (implied)", revenue=3307438097000, expenditure=3307438097000,
         value_source="implied residual (Grand Total minus Part A; not itself printed)",
         notes="Computed as 7465265286000-4157827189000.", approved="26 Esfand 1364 AH solar", gazette="11969",
         source_file="budget-law-1365-whole-country.html"),

    # --- FY1368 (first full post-Iran-Iraq-War budget; Khomeini died mid-transition) ---
    dict(fy=1368, law_type="main", hierarchy="Grand Total", revenue=9741705403000, expenditure=9741705403000,
         value_source="printed", notes="Both Part A and Part B below are EXPLICITLY printed in full (unlike FY1362/1363/1365 where the state-companies portion had to be computed as a residual) -- but they sum to 10,192,843,881,000, which EXCEEDS the printed grand total by 451,138,478,000. All three figures kept exactly as printed; not reconciled. Plausibly reflects a consolidation/netting adjustment for inter-account transfers between the general budget and state companies that is not shown in the single-article summary clause (normal in consolidated government accounting), but this project does not assert that explanation as fact absent a legible reconciliation table.",
         approved="29 Esfand 1367 AH solar (signed 1 Farvardin 1368, published 21 Farvardin 1368)", gazette="12849",
         source_file="budget-law-1368-whole-country.html"),
    dict(fy=1368, law_type="main", hierarchy="Part A: general government budget", revenue=4734790137000, expenditure=4734790137000,
         value_source="printed", notes="Sub-broken: general revenue 4,309,727,041,000 + earmarked 425,063,096,000 = 4,734,790,137,000 (exact).",
         approved="29 Esfand 1367 AH solar", gazette="12849", source_file="budget-law-1368-whole-country.html"),
    dict(fy=1368, law_type="main", hierarchy="Part B: state companies, banks & profit-making institutions", revenue=5458053744000, expenditure=5458053744000,
         value_source="printed", notes="See Grand Total row notes re: the A+B-vs-total discrepancy.",
         approved="29 Esfand 1367 AH solar", gazette="12849", source_file="budget-law-1368-whole-country.html"),

    # --- FY1370 (bridges to the pre-existing iran-plan-budget-org collection starting FY1371) ---
    dict(fy=1370, law_type="main", hierarchy="Grand Total", revenue=20097297101000, expenditure=20097297101000,
         value_source="printed", notes="Part A + Part B below (explicitly printed in full) sum to 21,342,243,603,000, exceeding the printed grand total by 1,244,946,502,000 -- same pattern as FY1368, not reconciled, kept as printed. CRITICAL BRIDGE: FY1370 is the year immediately preceding data/raw/iran-plan-budget-org/annual-budget-laws/1371.pdf (a pre-existing, separately-sourced collection), closing the gap to give this database an effectively continuous Majlis budget-law record from FY1360 through FY1401 except for the still-missing FY1364(main)/FY1366/FY1367/FY1369(main) years.",
         approved="11 Bahman 1369 AH solar (signed 14 Bahman, published 6 Esfand 1369)", gazette="13394",
         source_file="budget-law-1370-whole-country.html"),
    dict(fy=1370, law_type="main", hierarchy="Part A: general government budget", revenue=9278506740000, expenditure=9278506740000,
         value_source="printed", notes="Sub-broken: general revenue 8,663,723,135,000 + earmarked 614,783,605,000 = 9,278,506,740,000 (exact).",
         approved="11 Bahman 1369 AH solar", gazette="13394", source_file="budget-law-1370-whole-country.html"),
    dict(fy=1370, law_type="main", hierarchy="Part B: state companies, banks & profit-making institutions", revenue=12063736863000, expenditure=12063736863000,
         value_source="printed", notes="See Grand Total row notes re: the A+B-vs-total discrepancy.",
         approved="11 Bahman 1369 AH solar", gazette="13394", source_file="budget-law-1370-whole-country.html"),
]

with open(f"{OUT}/national_budget_totals_by_fiscal_year.csv", "w", newline="", encoding="utf-8") as f:
    fieldnames = ["fiscal_year_ah", "fiscal_year_western_end", "law_type", "hierarchy_level",
                  "revenue_rials", "expenditure_rials", "value_source", "notes",
                  "approved_date_ah", "gazette_issue_no", "country_iso3", "source_file"]
    w = csv.DictWriter(f, fieldnames=fieldnames)
    w.writeheader()
    for r in NATIONAL_ROWS:
        w.writerow({
            "fiscal_year_ah": r["fy"], "fiscal_year_western_end": ah_to_western_end_year(r["fy"]),
            "law_type": r["law_type"], "hierarchy_level": r["hierarchy"],
            "revenue_rials": r["revenue"], "expenditure_rials": r["expenditure"],
            "value_source": r["value_source"], "notes": r["notes"],
            "approved_date_ah": r["approved"], "gazette_issue_no": r["gazette"],
            "country_iso3": "IRN", "source_file": r["source_file"],
        })
print(f"national_budget_totals_by_fiscal_year.csv: {len(NATIONAL_ROWS)} rows")

# ============================================================================
# FILE 2: FY1301 ministry-level appropriations (pre-consolidated-budget era; unit = Tomans, not Rials)
# ============================================================================
MINISTRY_1301_ROWS = [
    dict(ministry="Public Works (وزارت فوائد عامه)", article="Article 1", item="Administrative budget", amount=53640, unit="tomans",
         notes="", raw_file="budget-law-1301-foreign-ministry.html (MISLABELED -- see README: this file's body text is actually the Public Works Ministry law, not Foreign Ministry)"),
    dict(ministry="Public Works (وزارت فوائد عامه)", article="Article 1", item="Pension/retirement pay for ministry staff", amount=3000, unit="tomans",
         notes="", raw_file="budget-law-1301-foreign-ministry.html (MISLABELED, see note above)"),
    dict(ministry="Justice (وزارت عدلیه)", article="Article 1", item="9-month appropriation (1 Farvardin - end Azar 1301)", amount=300000, unit="tomans",
         notes="", raw_file="budget-law-1301-justice-ministry.html (correctly labeled)"),
    dict(ministry="Justice (وزارت عدلیه)", article="Article 2", item="3-month appropriation for remainder of year (per attached schedule, 3 chapters/23 articles)", amount=191213.5, unit="tomans (191,213 tomans 5 qeran; 1 toman=10 qeran, so .5=5 qeran)",
         notes="", raw_file="budget-law-1301-justice-ministry.html"),
    dict(ministry="Foreign Affairs (وزارت امور خارجه)", article="Article 1", item="Ministry proper + League of Nations dues (609,000 + 31,000)", amount=640000, unit="tomans",
         notes="", raw_file="budget-law-1301-public-works-ministry.html (MISLABELED -- see README: this file's body text is actually the Foreign Ministry law, not Public Works)"),
    dict(ministry="Foreign Affairs (وزارت امور خارجه)", article="Article 2", item="Special commissions/delegations (Khorasan boundary commission 60,750 + Caucasus/Ankara delegation 30,000 + League of Nations representatives 6,000 + Moscow trade delegation 21,000)", amount=117750, unit="tomans",
         notes="", raw_file="budget-law-1301-public-works-ministry.html (MISLABELED, see note above)"),
    dict(ministry="Foreign Affairs (وزارت امور خارجه)", article="Article 4", item="Salary arrears for 5 named individuals from the prior year", amount=3288, unit="tomans",
         notes="Names given in source: Moayyed od-Dowleh, Moazzed os-Saltaneh, Mirza Es'hagh Khan, Mirza Hassan Khan Akhtar, Meftah od-Dowleh -- not reproduced here (personal names of historical officials, not aggregated data).",
         raw_file="budget-law-1301-public-works-ministry.html (MISLABELED)"),
]
with open(f"{OUT}/ministry_level_appropriations_1301.csv", "w", newline="", encoding="utf-8") as f:
    fieldnames = ["fiscal_year_ah", "ministry", "article", "item", "amount", "unit", "notes", "country_iso3", "raw_file"]
    w = csv.DictWriter(f, fieldnames=fieldnames)
    w.writeheader()
    for r in MINISTRY_1301_ROWS:
        w.writerow({"fiscal_year_ah": 1301, "ministry": r["ministry"], "article": r["article"],
                     "item": r["item"], "amount": r["amount"], "unit": r["unit"], "notes": r["notes"],
                     "country_iso3": "IRN", "raw_file": r["raw_file"]})
print(f"ministry_level_appropriations_1301.csv: {len(MINISTRY_1301_ROWS)} rows")

# ============================================================================
# FILE 3: Supplementary budget laws (delta appropriations added mid-year -- NOT full-year totals)
# ============================================================================
SUPPLEMENT_ROWS = [
    dict(fy=1357, item="Salary/pension reform payments (civil service law reform, military/judicial pay, university faculty, etc.)",
         amount=145000000000, notes="Largest of 3 quantified items in this supplement.",
         approved="16 Esfand 1357 AH solar (7 Mar 1979 CE)", source_file="budget-supplement-law-1357-whole-country.html"),
    dict(fy=1357, item="Other necessary expenses (per list prepared by Plan & Budget Org + Finance Ministry)",
         amount=15000000000, notes="", approved="16 Esfand 1357 AH solar",
         source_file="budget-supplement-law-1357-whole-country.html"),
    dict(fy=1357, item="Foreign loan repayments due in-year (from budget line 801000)",
         amount=6000000000, notes="Total quantified supplement across the 3 items above: 166,000,000,000 rials. A 4th item (treasury-bond issuance authorization, interest-free) has no stated ceiling amount. Enacted by the Revolutionary Council (Shoraye Enghelab) as interim legislature 3 weeks after the 11 Feb 1979 revolution -- the ORIGINAL FY1357 main budget law (passed by the last Pahlavi Majlis) was NOT located in this collection.",
         approved="16 Esfand 1357 AH solar", source_file="budget-supplement-law-1357-whole-country.html"),
    dict(fy=1358, item="Utility-price compensation (water/electricity subsidy for low-consumption customers) + Supreme Labour Council wage increase",
         amount=285000000000, notes="Single combined ceiling for both purposes, added to the original FY1358 budget's current+capital-investment appropriations. The ORIGINAL FY1358 main budget law itself is separately found in this collection (see national_budget_totals_by_fiscal_year.csv, Gazette 52866) -- this is the amendment on top of it.",
         approved="5 Dey 1358 AH solar (~26 Dec 1979 CE)", source_file="budget-supplement-law-1358-whole-country.html"),
    dict(fy=1369, item="General addition to FY1369 approved revenues/appropriations (largely veterans/POW 'Azadegan' resettlement, housing and employment provisions per the law's own tables 1-2)",
         amount=435630000000, notes="The ORIGINAL FY1369 main budget law was NOT located in this collection (a confirmed gap, along with FY1366 and FY1367 in full) -- this supplement is the only FY1369 primary-source figure available.",
         approved="27 Azar 1369 AH solar (~18 Dec 1990 CE)", source_file="budget-supplement-law-1369-whole-country.html"),
]
with open(f"{OUT}/supplementary_budget_additions.csv", "w", newline="", encoding="utf-8") as f:
    fieldnames = ["fiscal_year_ah", "fiscal_year_western_end", "item", "amount_rials", "notes",
                  "approved_date_ah", "country_iso3", "source_file"]
    w = csv.DictWriter(f, fieldnames=fieldnames)
    w.writeheader()
    for r in SUPPLEMENT_ROWS:
        w.writerow({"fiscal_year_ah": r["fy"], "fiscal_year_western_end": ah_to_western_end_year(r["fy"]),
                     "item": r["item"], "amount_rials": r["amount"], "notes": r["notes"],
                     "approved_date_ah": r["approved"], "country_iso3": "IRN", "source_file": r["source_file"]})
print(f"supplementary_budget_additions.csv: {len(SUPPLEMENT_ROWS)} rows")

# ============================================================================
# FILE 4: FY1364 foreign-exchange budget law (a distinct, specialized companion law -- USD, not rials)
# ============================================================================
FOREX_ROWS = [
    dict(fy=1364, item="Maximum foreign-currency allocation ceiling for the fiscal year", amount=15000000000, unit="USD",
         notes="War-economy-era FX rationing/allocation law (Iran-Iraq war ongoing). Allocated across sectoral priority tables attached to the law (medicine/medical equipment first priority; then agriculture, power generation, defense industries, petrochemicals/steel, gas injection, refinery construction, railway rehabilitation, R&D, mining, export-linked and private-sector industrial needs, in the priority order stated in the law's own tabsare 3). This is SEPARATE FROM (and narrower in scope than) the general rial-denominated FY1364 national budget law, which was NOT located in this collection -- a confirmed remaining gap.",
         approved="2 Mehr 1364 AH solar (signed 14 Mehr, published 25 Mehr 1364)", gazette="11836",
         source_file="budget-forex-law-1364-whole-country.html"),
]
with open(f"{OUT}/forex_budget_law_1364.csv", "w", newline="", encoding="utf-8") as f:
    fieldnames = ["fiscal_year_ah", "fiscal_year_western_end", "item", "amount", "unit", "notes",
                  "approved_date_ah", "gazette_issue_no", "country_iso3", "source_file"]
    w = csv.DictWriter(f, fieldnames=fieldnames)
    w.writeheader()
    for r in FOREX_ROWS:
        w.writerow({"fiscal_year_ah": r["fy"], "fiscal_year_western_end": ah_to_western_end_year(r["fy"]),
                     "item": r["item"], "amount": r["amount"], "unit": r["unit"], "notes": r["notes"],
                     "approved_date_ah": r["approved"], "gazette_issue_no": r["gazette"],
                     "country_iso3": "IRN", "source_file": r["source_file"]})
print(f"forex_budget_law_1364.csv: {len(FOREX_ROWS)} rows")

print("\nAll Majlis budget-law files written.")
print("FY1356 (budget-amendment-note85-law-1356-whole-country.html) produced NO quantitative row:")
print("  its text is a narrow, non-monetary eligibility-rule amendment to pension-calculation note 85")
print("  of the (not-located) FY1356 main budget law -- no rial figures appear anywhere in the text.")
