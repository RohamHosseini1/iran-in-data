# The Billion Prices Project / PriceStats — Reference Notes

Curated reference notes on the Billion Prices Project (BPP), captured because it is a methodology
touchstone for this database's "verify official statistics, prefer independent trackers" approach —
and because it is directly upstream of the Cavallo-Bertolotto Argentina 1943-2016 inflation
reconstruction (see `data/raw/argentina-inflation-reconstruction/cavallo-bertolotto-inflation-1943-2016/`).
This is a reference/methodology capture, not a bulk data download: per its own homepage, the project
"is no longer active" as an independent research initiative, and its live successor (current daily
inflation tracking) is the commercial PriceStats platform under State Street, which does not offer a
public bulk-data download.

## What it is

The Billion Prices Project (BPP) was an academic research initiative founded in 2008 by
**Alberto Cavallo** (then a PhD student at Harvard, later MIT Sloan/NBER) and
**Roberto Rigobon** (MIT Sloan). Its purpose was to test whether prices scraped daily from online
retailers could substitute for, or independently check, official government CPI statistics — at
higher frequency (daily vs. monthly) and shorter lag (about 3 days vs. several weeks) than most
national statistical agencies. Source: [The Billion Prices Project — Home](https://www.thebillionpricesproject.com/).

## Origin story and direct link to Argentina

Cavallo's original motivation, per multiple secondary/academic accounts, was **Argentina
specifically**: in 2007 he began building a daily online-price inflation tracker for a handful of
Latin American countries as part of his PhD thesis, in direct response to the credibility collapse
of INDEC's official CPI after the government began intervening in the agency's statistical
methodology in January 2007. Rigobon joined roughly a year later and the effort scaled to ~50
countries, becoming the Billion Prices Project. The Argentina-specific offshoot of this work was
published separately as **"Inflación Verdadera"** ("True Inflation"), which tracked Argentina
(2007-2015) and later Venezuela (2017-2018) — the same site (`inflacionverdadera.com`) that hosted
the raw CSV later used in the Cavallo & Bertolotto (2016) paper "Filling the Gap in Argentina's
Inflation Data" already captured in this database.
Source: [Central Banking — "Economics in central banking: Alberto Cavallo and Roberto Rigobon"](https://www.centralbanking.com/awards/3346716/economics-in-central-banking-alberto-cavallo-and-roberto-rigobon-billion-prices-projectpricestats).

## Scale and methodology

By around 2010 the project was collecting roughly 5 million prices per day from 300+ online
retailers across 50 countries, using automated web-scraping software that tracks individual SKUs,
detects new/discontinued products, and builds a matched-price index comparable in spirit to a
traditional CPI basket but updated continuously. The core academic reference for the methodology is:

- Cavallo, Alberto, and Roberto Rigobon. **"The Billion Prices Project: Using Online Prices for
  Measurement and Research."** *Journal of Economic Perspectives* 30, no. 2 (Spring 2016): 151-178.
  Also circulated as NBER Working Paper No. 22111.
  [AEA/JEP page](https://www.aeaweb.org/articles?id=10.1257%2Fjep.30.2.151) ·
  [NBER working paper PDF](https://www.nber.org/system/files/working_papers/w22111/w22111.pdf)

## PriceStats and the State Street acquisition

**PriceStats** was spun out in 2010 as the commercial vehicle to fund and scale the underlying data
collection — both a for-profit business and a way to keep the academic project running. PriceStats
data has since been used by central banks and financial institutions as a real-time inflation
nowcasting tool. PriceStats was subsequently acquired and is now operated as part of **State
Street's Data Intelligence / State Street Global Markets** business line. The original
thebillionpricesproject.com site is now maintained mainly as a legacy/reference page; it explicitly
states the academic project itself is inactive and points visitors to the State Street PriceStats
product for current data, which is a subscription/institutional commercial service, not a public
bulk-download dataset.
Source: [The Billion Prices Project — Home](https://www.thebillionpricesproject.com/) (self-description);
[Central Banking profile](https://www.centralbanking.com/awards/3346716/economics-in-central-banking-alberto-cavallo-and-roberto-rigobon-billion-prices-projectpricestats).

## BPP Datasets page — what is actually downloadable

The site does retain a `/datasets/` page with historical academic replication data hosted on
Harvard Dataverse (checked directly during this project's research, 2026-07-12). None of these are
Argentina-1943-2016-specific (that series lives with the Cavallo-Bertolotto paper instead — already
captured separately in this database), but they are listed here for completeness / future reference:

| Dataset | Coverage | Dataverse link |
|---|---|---|
| Price Indices (the JEP-2016 companion data) | 8 countries + US sectors + global aggregates, 2007/2008-2015 | https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/6RQCRS |
| Online Micro Price Data (Latin America) | Argentina, Brazil, Chile, Colombia, Venezuela, US; 2007-2010 | https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/UYX11A |
| Online Micro Price Data (incl. US retailers) | same period | https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/IAH6Z6 |
| Global Retailers Data | 85 countries, 2008-2013 | https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/NV26Z6 |
| Online-Offline Price Comparison | 10 countries, 2014-2016 | https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/XXOUHF |
| PPP Data | 11 countries, 2010-2017 | https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/RGWZJG |

Note: the "Online Micro Price Data (Latin America)" entry does include raw Argentina micro-price
observations for 2007-2010, which is a narrower/earlier slice than the full chained 1943-2016 index
already captured under `argentina-inflation-reconstruction`. Not downloaded in this session (out of
scope for this reference-notes task; flagged here for a future round if granular micro-price data
is wanted).

## Why this matters for this database's methodology

The BPP/PriceStats/Inflación Verdadera lineage is the clearest real-world precedent for this
project's own operating principle (`docs/bookkeeping.md` — "Source reliability & neutrality
principles" and the instruction to prefer primary/independent data when an official series is
compromised): when INDEC's official CPI became unreliable for political reasons (2007-2015,
formally censured by the IMF in 2013 — see `timeline/argentina.csv`), independent researchers built
a parallel, methodologically transparent measurement system rather than either (a) uncritically
accepting the compromised official number or (b) discarding measurement entirely. The same logic
underlies this database's use of TGJU alongside CBI for Iran, and OVF alongside BCV for Venezuela.

## Access notes / limitations

- No bulk "download everything" option exists for current PriceStats data — it is now a commercial
  State Street product behind an institutional paywall.
- The historical BPP academic datasets that ARE public live on Harvard Dataverse (table above), not
  on thebillionpricesproject.com itself, which functions as an index/landing page.
- The `/research/` sub-path tested during this session (`https://www.thebillionpricesproject.com/research/`)
  returned HTTP 404 — no longer live as a distinct page.
