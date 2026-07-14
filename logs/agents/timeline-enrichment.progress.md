# Timeline enrichment agent — progress log

Task: add new dated point events to timeline/new_events/<country>.csv (Iran, Iraq, global,
and thin comparators), without duplicating timeline/*.csv or timeline/eras.csv.

Read first: timeline/iran.csv (113 rows, already dense — covers most Pahlavi-era items listed
in the brief), timeline/global.csv (25 rows), timeline/eras.csv (long periods, skip),
timeline/{turkey,saudi-arabia,venezuela,argentina}.csv (all already dense per README: Turkey ~19,
Saudi ~22, Venezuela ~32, Argentina ~37). Iraq has NO existing file — highest-value gap.

Plan: prioritize (1) Iraq new file from scratch, (2) genuine Iran gaps not already in iran.csv,
(3) genuine global gaps not already in global.csv, (4) comparator thin spots if time allows.

- [2026-07-14T14:20Z] IRAQ: wrote timeline/new_events/iraq.csv, 26 new events, 1927-2023
  (Baba Gurgur/Red Line/independence/50-50 deal/1958 revolution+land reform/Law 80/INOC/
  1968 Ba'ath coup/1972 IPC nationalization/1980 invasion of Iran (Gulf war-debt financing
  angle)/1990 Kuwait invasion/UNSC 661 sanctions/Oil-for-Food 986/2003 Central Bank $1bn
  withdrawal, CPA Order 2 army dissolution, CPA Order 39 FDI liberalization, new dinar/
  2004 Paris Club 80% debt write-off/2009 first oil licensing round (Rumaila)/2014 ISIS
  captures Mosul + Kurdish Kirkuk takeover/2016 IMF SBA/2017 Kirkuk retaken from KRG/2020
  dinar devaluation/2021 UNCC reparations completed/2023 Fed dollar-restriction crisis).
  Every row has a verified real source_url (state.gov, Britannica, IMF, UN, CPA primary
  docs, Washington Post, CBS News, etc.) and Persian title_fa/description_fa. No em dashes.

- [2026-07-14T14:45Z] IRAN: wrote timeline/new_events/iran.csv, 11 new events filling genuine
  pre-1925 constitutional/fiscal-history gaps and 1980s-2020s gaps NOT in the existing
  113-row timeline/iran.csv (which already covers nearly all Pahlavi-era items the brief
  called out): 1907 first Majlis budget, 1911 Morgan Shuster mission, 1919 Anglo-Persian
  Agreement, 1921 coup, 1983 usury-free banking law, 1993 external-debt moratorium, 2007
  Mehr housing scheme, 2016 Boeing-Iran Air deal, 2017 unlicensed credit-institution
  collapse/depositor protests, 2020 TSE bubble/crash, 2021 Iran-China 25-year deal.
  Sources: Britannica, Encyclopaedia Iranica, Iran Data Portal, NPR, Axios, Radio Farda
  (RFE/RL — legitimate, not MEK/NCRI), Center for Human Rights in Iran. Avoided
  mojahedin.org/ncr-iran.org hits that surfaced in searches on the 2017 credit-institution
  story per bias policy. Note: iran.csv is SO dense already that most brief examples
  (Consortium Agreement, Bank Melli/Markazi, 1957-62 IMF program, 1993/2002 unifications,
  2010 subsidy law, 2012 SWIFT, 2018 collapse, 2019 protests, redenomination, earthquakes)
  were already present — did not duplicate.

- [2026-07-14T15:05Z] GLOBAL: wrote timeline/new_events/global.csv, 5 new events not in the
  existing 30-row global.csv: 1944 Bretton Woods (IMF/World Bank founding), 1995 WTO
  founding, 2003-2008 commodity super-cycle, 1998 Russian default/LTCM global contagion,
  2022-23 fastest Fed tightening cycle since the 1980s (explicit EM-currency tie-in to
  Turkey/Argentina comparators). Sources: Federal Reserve History, WTO official history
  page, EIA, BIS (Committee on Global Financial System), Dallas Fed.

- [2026-07-14T15:05Z] SUMMARY / SIGN-OFF: 42 new events added across 3 files (26 Iraq new
  file, 11 Iran, 5 Global). Verified: (1) no duplicate titles against existing
  timeline/iran.csv or timeline/global.csv, (2) every row has all 10 schema columns
  populated with a real, checkable source_url, (3) em dashes appear only in source_name
  citation fields — matching the pre-existing convention in timeline/iran.csv,
  timeline/global.csv etc. — never in title/description/title_fa/description_fa prose,
  (4) economic_domains uses semicolon separators to match the established convention in
  ALL existing timeline/*.csv files and the timeline/README.md schema doc (the task brief's
  own "oil|trade|fx" example uses pipes, but every existing file and its own README use
  semicolons — followed "matching those already used in existing files" literally).
  Did NOT touch: turkey.csv, saudi-arabia.csv, venezuela.csv, argentina.csv — all four are
  already dense (19-37 rows each per README) and a scan of each found no obvious
  high-value gaps worth adding in the time available; if the owner wants deeper
  comparator coverage, a follow-up agent should specifically audit those four against the
  same research depth applied to Iraq/Iran/global here. Also did not add eras.csv material
  (out of scope — periods, not point events) and made no edits to any existing
  timeline/*.csv (per instructions, only new_events/ shards were written).

