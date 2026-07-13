# Iran telecom & communications infrastructure series (1858–1990)

Hand-curated, citation-preserving extraction from a single Encyclopaedia Iranica article,
"COMMUNICATIONS in Persia" (Annabelle Sreberny-Mohammadi and Ali Mohammadi, 1992). Harmonized
2026-07-13 from `data/raw/iran-telecom-history/iranica-communications-in-persia/` (raw source
immutable, unchanged). Every row of every CSV here is a number stated explicitly in the article's
prose, most of which the article itself sources to specific editions of the Iran Statistical
Yearbook (Sal-nama-ye amari-e keshvar) or UNESCO reports — i.e. genuine primary/official Iranian
government statistics reached through a secondary narrative, not tertiary guesswork. Nothing was
interpolated, estimated, or fabricated; where the source's own citation was vague (e.g. a UNESCO
"late 1980s" figure with no exact year), the row's `source` text preserves that vagueness rather
than inventing precision.

This is the richest pre-1990 telecom source in the database: WDI's `IT.MLT.MAIN` (fixed telephone
subscriptions) only starts in 1960 with a flat, repeated 116,417 figure, and has no telegraph,
radio, or TV ownership series at all. These four files fill that gap back to 1858 (telegraph),
1913 (postal), 1914 (telephone), and 1924 (radio) / 1958 (TV).

## Files

| File | Coverage | What it covers |
|---|---|---|
| `postal_service_series.csv` | 1913, 1953, 1965, 1976, 1989 | Post office/box counts, domestic + foreign mail and parcel volumes |
| `telegraph_offices.csv` | 1914, 1953, 1975, 1989 | Telegraph cable length, cable/wireless office counts, telex stations |
| `telephone_series.csv` | 1914, 1953, 1975, 1979, 1988 | Subscriber counts, public/private telephone counts, waiting list, direct-dial share |
| `radio_tv_series.csv` | 1940–1989 | Radio-set ownership (urban/rural split), TV founding events, audience reach, programming-import share |

## Schema

`year, metric, value, unit, source[, medium], country_iso3` — one row per statistic. `radio_tv_series.csv`
carries an extra `medium` column (`radio` or `television`) since both series were combined in the
source article. All rows are `country_iso3 = IRN`.

## Caveats

- **Irregular snapshot years, not a continuous series.** Data points cluster at 1913/14, 1953,
  1965/66, 1975/76, 1979, and 1988/89 — whatever years the Statistical Yearbook editions the
  article cites happened to cover. Do not interpolate between points on a chart without labeling
  the gap.
- **Retrieval method:** iranicaonline.org blocks curl/WebFetch with a Cloudflare challenge (HTTP
  403); content was retrieved via an interactive browser tool instead. This is consistent with
  every other iranicaonline.org retrieval in this project.
- **Sibling dataset:** a fifth extract from this same article, covering newspaper/periodical counts
  and literacy rates, is filed under `data/processed/iran_media_history_series/press_periodicals_series.csv`
  instead (topic-scoped to media, not telecom), to avoid duplicating this article's full text in
  two places. The full article text lives once, at
  `data/raw/iran-telecom-history/iranica-communications-in-persia/communications-in-persia.txt`.
- **Cross-check:** the 1974 TV audience-reach figure here (15,000,000, `radio_tv_series.csv`) is
  not perfectly reconciled with a related 1978 TV-set figure in the companion
  `iran_media_history_series/cinema_theaters_and_attendance.csv` notes — both are kept as printed
  in their respective source articles, not adjusted to agree.

## Source

Encyclopaedia Iranica, "COMMUNICATIONS in Persia," https://www.iranicaonline.org/articles/communications-in-persia/
(article by Annabelle Sreberny-Mohammadi and Ali Mohammadi). Full manifest:
`data/raw/iran-telecom-history/iranica-communications-in-persia/manifest.json`.
