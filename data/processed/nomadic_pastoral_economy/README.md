# Iran nomadic/pastoral economy series (1884–2015)

## Files

| File | Coverage | What it covers |
|---|---|---|
| `iran_nomad_population_estimates_1884_2008.csv` | 1884–2008 (sparse) | National nomad population estimates across multiple methodologies — pre-census foreign-researcher estimates (1884–1908), 1986 Library of Congress broad-tribal estimate, three dedicated SCI Nomad (Ashayeri) Censuses (1987, ~1998, 2008), and the 2006 general-census "unsettled population" count (a structurally different, smaller measure — see caveats) |
| `nomad_pastoral_livestock_economy.csv` | 2012–2015 fieldwork (2014 national reference year) | National nomad share of Iran's sheep/goat population (58.5% / 39.7%), plus a Kerman-province field-study snapshot: typical flock size and composition, Raeini cashmere-goat and Kermani wool-sheep yield statistics |

`iran_nomad_population_estimates_1884_2008.csv` was built in a prior harmonization round (verified
present and correctly structured here, not redone — schema: `year, estimate_type, population,
pct_of_national_population, notes, source`). `nomad_pastoral_livestock_economy.csv` is new this
round, extracted from `data/raw/academic-nomadic-pastoral-economy/ansari-renani-2016-organic-nomad-livestock/`
(immutable, unchanged) — a peer-reviewed, open-access (CC BY 4.0) field study, the only genuinely
new nomadic/pastoral raw material found in this pass beyond the already-processed population
series.

## Caveats — read before charting

- **`iran_nomad_population_estimates_1884_2008.csv`'s figures are NOT directly comparable across
  rows** — three different measurement methodologies appear: (1) dedicated SCI Nomad Censuses
  (1987: 1,152,099; 2008: 1,186,398), which specifically enumerate migrating pastoral households;
  (2) the ordinary national census's "unsettled population" category (2006: 104,717), which
  structurally undercounts true nomadic population since it only captures persons enumerated
  while actively migrating on census day; and (3) broad tribal-affiliation estimates (1986 Library
  of Congress: 1.8 million nomads within a ~4 million broader tribally-organized population),
  which use self-identified tribal affiliation rather than active pastoral-household status. Do
  not plot these three measures as one continuous line without labeling the methodology break.
- **Most pre-1987 figures in that file are secondary citations of a paywalled academic source**
  (Amani/Sheikh-Hosseini et al. 2010, *Asian Population Studies* 6(3)) — the primary article was
  not directly accessed; treat as reliable-secondary rather than primary-verified.
- **`nomad_pastoral_livestock_economy.csv` is a single field study of 30 households in one
  district (Baft, Kerman province), not a national time series** — the Kerman-specific rows
  (flock size/composition, Raeini goat and Kermani sheep yield statistics) describe one local
  pastoral system in the Siahjel sub-tribe of the Raen tribe, and should not be generalized to
  nomadic pastoralism nationwide. Only the national sheep/goat population-share figures (58.5%,
  39.7%) are genuinely national-level statistics (FAO 2014, cited within the paper).
- This is a genuinely thin topic in freely accessible sources — Iran's own SCI Nomad Census raw
  reports were not directly reachable (amar.org.ir confirmed geo-blocked from this network,
  consistent with the pattern documented throughout this project for Iran-domestic government
  sites); all SCI-census figures here are via reliable secondary citation, not the primary SCI
  document.

## Sources

- Amani, M. & Sheikh-Hosseini (secondary citation), "Demographic changes of nomadic communities
  in Iran (1956–2008)," *Asian Population Studies* 6(3), 2010, DOI 10.1080/17441730.2010.512764.
- Library of Congress Country Studies, "Iran: Nomadic Society" (US government, public domain),
  countrystudies.us/iran/51.htm.
- Statistical Centre of Iran (SCI) 1987/2008 Nomad (Ashayeri) Censuses (via secondary citation).
- Iran Data Portal (Syracuse University), Table 12, "Settled and Unsettled Population and
  Households of Ostans, 1385 (2006) Census."
- Ansari-Renani, H.R. (2016), "An investigation of organic sheep and goat production by nomad
  pastoralists in southern Iran," *Pastoralism: Research, Policy and Practice* 6:8, DOI
  10.1186/s13570-016-0056-y (CC BY 4.0, Springer Open Access).

Full manifest: `data/raw/academic-nomadic-pastoral-economy/ansari-renani-2016-organic-nomad-livestock/manifest.json`.
(The population-estimates file's original raw-source manifest, if one exists from the prior
harmonization round, was not re-located in this pass — flagged for a future bookkeeping check,
not a blocker for this round's work.)
