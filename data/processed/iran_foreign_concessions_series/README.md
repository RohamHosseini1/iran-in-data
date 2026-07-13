# Iran pre-1979 foreign concessions & industrial joint ventures

Harmonized 2026-07-13 from `data/raw/iran-foreign-concessions-pre1979/` (two raw sub-datasets,
immutable, unchanged) via `scripts/harmonize/harmonize_banking_concessions.py`. Covers two of
Iran's landmark foreign-capital concession structures under the Qajar/Pahlavi monarchies: the 1901
D'Arcy oil concession (the origin of the Anglo-Persian/Anglo-Iranian/BP lineage) and the
1956-1979 wave of automotive licensing/assembly joint ventures.

## Files

| File | Coverage | What it covers |
|---|---|---|
| `darcy_oil_concession_1901_terms.csv` | 1901 (single contract's terms, 17 rows) | Signing date, 60-year duration, ~1,242,000 sq km territory (excluding the 5 northernmost provinces bordering Russia), £20,000 upfront cash + £20,000 in shares, royalty structure |
| `automotive_joint_ventures_1956_1979.csv` | 1956–2005 (start/end years per venture; 5 ventures) | Jeep Iran Trading Co. (Willys-Overland/Kaiser, 1956), Iran National/Rootes-Chrysler-Peugeot Paykan licence (1966-2005, 2.2M+ units), Iran National/Daimler-Benz bus-truck licence (1966-1979), Khawar Industrial Group/Daimler-Benz truck licence (1966→merged into Iran Khodro Diesel 1999), General Motors Iran Ltd. (1972-1980, Chevrolet Royale/Opel Commodore under license) |

## Schema

- `darcy_oil_concession_1901_terms.csv`: `term, value, unit, notes` — one row per contract term
  (not a time series).
- `automotive_joint_ventures_1956_1979.csv`: `venture_name, foreign_partner,
  foreign_partner_country, iranian_partner, start_year, end_year_or_status, notes, source`.

## A CSV-quoting defect fixed on the way in (raw untouched)

**`automotive_joint_ventures_1956_1979.csv`, the Iran National/Peykan-Rootes row**: the raw file's
`foreign_partner` field `"Rootes Group (UK; became Chrysler UK 1967, then Talbot/Peugeot 1978)"` had
an unescaped comma and was not quoted in the original raw CSV, splitting it into two extra columns
on a naive parse. Per `docs/bookkeeping.md`, `data/raw/iran-foreign-concessions-pre1979/
automotive-joint-ventures-1956-1979/data.csv` was left untouched; this processed copy rejoins the
split text with the comma restored. No content altered beyond column alignment. Verified: every row
now has a uniform column count.

## Caveats — read before charting

- **These are two distinct, unrelated instruments** (a natural-resource concession vs. later
  industrial-licensing joint ventures) grouped in one folder only because both are pre-1979
  foreign-capital-in-Iran case studies of the same general "concessions/FDI" type, not because they
  connect economically — do not chart them on the same axis without labeling.
- **`darcy_oil_concession_1901_terms.csv` is contract TERMS as signed, not a performance/output
  series** — it does not show how much oil was actually produced or what royalties were actually
  paid over the concession's life (that belongs to the separate oil-revenue Pahlavi-era tables
  already in `data/processed/pahlavi_government_finance_series/` and the earlier-round USBM
  AIOC-profits/royalties extraction at
  `data/raw/pahlavi-era-primary-extraction/usbm1963-aioc-profits-royalties-1910-1951/`).
- **`automotive_joint_ventures_1956_1979.csv`'s `end_year_or_status` column mixes hard end dates
  (1979, 1980) with ongoing/renamed-successor status** (e.g. the Khawar Industrial Group venture
  continued past 1979 via merger into Iran Khodro Diesel in 1999) — read each row's `notes` before
  treating `end_year_or_status` as a clean nationalization cutoff; not every venture ended cleanly
  in 1979/80 the way the banking sector did.
- Only 5 automotive ventures were captured this round (Jeep/Pars Khodro lineage, Rootes/Paykan,
  two parallel Daimler-Benz licences held by Iran National, and GM Iran) — this is not represented
  as an exhaustive census of all pre-1979 industrial joint ventures, only the ones with citable
  primary/secondary documentation found this round.

## Sources

- UK Parliament / historical accounts of the 1901 D'Arcy Concession terms (as previously compiled
  in this project's raw extraction; see manifest for exact citation chain).
- Encyclopaedia Iranica, "IRAN NATIONAL COMPANY."
- Wikipedia: "Paykan," "Pars Khodro," "Iran Khodro Diesel," "General Motors Iran."
- aronline.co.uk (Rootes/Chrysler/Peugeot corporate lineage detail).

Full manifests and extraction methods:
`data/raw/iran-foreign-concessions-pre1979/darcy-concession-1901-terms/manifest.json`,
`data/raw/iran-foreign-concessions-pre1979/automotive-joint-ventures-1956-1979/manifest.json`.
