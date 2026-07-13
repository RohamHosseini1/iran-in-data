# IHEIS / HEIS Microdata — Human Action Item (Registration Required)

**Status:** NOT downloaded. This is a ready-to-execute human task, analogous to the Maddison/BEA
manual-download items elsewhere in this project. Agents are barred from registering accounts
(see project rules), and `amar.org.ir` is unreachable directly from this agent's network anyway
(`curl` exit 35 / `SSL_ERROR_SYSCALL`; confirmed again on 2026-07-12, consistent with prior
sessions' findings recorded in `SOURCES.md`). A human, browsing from a normal residential/Iranian
IP with a real browser, will very likely succeed where this agent could not.

## What this dataset is

The **Household Expenditure and Income Survey (HEIS / HIES)**, run by the Statistical Centre of
Iran (SCI, مرکز آمار ایران), is Iran's household budget survey:

- Rural coverage since 1342 SH (1963); urban coverage since 1347 SH (1968).
- Income questions added to the questionnaire in 1353 SH (1974).
- Three-stage stratified cluster sample; ~18,700 urban + ~19,600 rural households in the 2010
  round alone. Cumulative microdata across rounds run into roughly a million observations over
  1991-2021 (per project brief).
- Four questionnaire parts: (1) member characteristics, (2) household facilities, (3) expenditure,
  (4) income.
- Designed to produce province-level and national estimates of household income/expenditure
  composition, consumption patterns/COICOP weights, poverty lines, and inequality measures.

Source: SCI English metadata page (retrieved via Wayback Machine snapshot, since the live page is
unreachable from this network):
`https://web.archive.org/web/20240205115704/https://www.amar.org.ir/english/Metadata/Statistical-Survey/Household-Expenditure-and-Income`

## How to actually get the microdata (step-by-step for a human)

### Option A — SCI's own portal (primary, authoritative, free registration)

1. Go to `https://www.amar.org.ir` (Persian) or the English mirror `https://www.amar.org.ir/english`.
2. Navigate: **Data & Statistical Information → Household, Expenditure and Income**, or use the
   site search for "ریزداده" (microdata) / "هزینه و درآمد خانوار" (household expenditure and income).
   A recent live path observed via web search: `https://amar.org.ir/cost-and-income` (Persian) and
   `https://amar.org.ir/دادهها-و-اطلاعات-آماری/هزینه-و-درامد-خانوار/هزینه-و-درامد-خانوارهای-شهری` (urban)
   and the `-روستایی` (rural) sibling page. These paths shift over time as SCI periodically
   restructures its DNN-based CMS, so search-navigate rather than assuming any single URL is stable.
3. Look for a "microdata" / "ریزداده" section or request form — SCI's own repo documentation
   (`github.com/IPRCIRI/IRHEIS`, see below) points to `https://www.amar.org.ir/Default.aspx?tabid=111`
   as "Official page for SCI HIES microdata downloads," but this DNN tab ID may no longer resolve
   after subsequent site redesigns — verify live.
4. **Historical direct-download pattern (now defunct, do not rely on it):** the IRHEIS README states
   that raw microdata for years 1363-1394 SH (1984-2015) used to be directly downloadable, no login,
   from `http://www.amar.org.ir/Portals/0/amarmozuii/hazinedaramad/XX.rar` (XX = 2-digit Persian
   year, e.g. `92` for 1392). This agent checked the Wayback Machine CDX index for this exact path
   and found **zero archived snapshots** — the path is gone, most likely superseded by whatever
   registration-gated system SCI now runs. A human should check whether SCI has a modern equivalent
   (the survey years needed are 1370-1400 SH / 1991-2021 per the project brief) before concluding
   it's registration-only.
5. Registration on SCI's portal is reported (per project brief) to be free — create an account,
   then request/download the microdata files (historically distributed as MS Access `.mdb`/`.accdb`
   or `.rar`-compressed flat files, one archive per survey year, separately for urban and rural).

### Option B — ERF Open Access Microdata Portal (secondary, free registration)

`http://erfdataportal.com` (Economic Research Forum, Cairo) hosts harmonized MENA household
surveys, including multiple rounds of Iran's HEIS, standardized into a common format across
countries. Free registration; request access per survey/round; approval is typically not
instantaneous. Useful if cross-country MENA harmonization matters more than getting SCI's own
untouched microdata.

### Option C — International Household Survey Network (IHSN) catalog (metadata only, then redirect)

`https://catalog.ihsn.org` has metadata-only catalog entries for individual HEIS rounds, e.g.:
- 2019 round: `https://catalog.ihsn.org/catalog/10336` (reference ID `IRN_2019_HEIS_v01_M`)
- 2017 round: `https://catalog.ihsn.org/catalog/10338`

These pages document sampling/questionnaire metadata and a "Get Microdata" link, but (checked by
this agent) do not host the actual files or state clear access terms — they most likely bounce
back to SCI's own national system. Use these primarily to confirm survey-round identifiers and
citation format, not as a shortcut around registration.

## After you have the raw files: processing tools already identified (not downloaded — code only)

- **`m-hoseini.github.io/HEIS/`** — full methodology guide, ALREADY DOWNLOADED into this repo at
  `data/raw/iheis-microdata-metadata/heis-codebook-mhoseini/` (9 chapters as static HTML: survey
  design, questionnaire structure, R code for importing raw Access files, step-by-step cleaning
  procedures for all 4 questionnaire parts, and results chapters with embedded trend tables/charts
  including a poverty analysis of the November 2019 gas price reform). Start here once you have
  raw files in hand — it tells you exactly how to turn them into usable item/individual/household
  -level datasets.
- **`github.com/IPRCIRI/IRHEIS`** — companion R codebase (not mirrored here; it's code, not data/
  documentation, and is reference-only per project scope). Clone directly if implementing the
  cleaning pipeline: `git clone https://github.com/IPRCIRI/IRHEIS`.

## What NOT to do

Per project rules, do not attempt to create an SCI account, an ERF Data Portal account, or submit
any registration/consent form on the user's behalf. This file exists so a human can do that step
themselves and then hand the resulting raw files back to a future download/processing pass.
