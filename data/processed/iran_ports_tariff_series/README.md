# Iran port and maritime tariffs (Ports & Maritime Organization, 2024)

**Honest scope note, carried over from the raw folder's own manifest**: the task that sourced
this data was looking for cargo-throughput/annual-performance statistics (tons handled, TEU
counts, ship calls by port and year) — PMO publishes these on `en.pmo.ir/en/statistics`, but
none of that specific content was ever archived by the Wayback Machine (checked and confirmed;
see `data/raw/iran-ports-maritime-org/statistics/manifest.json`). What **was** recoverable is
PMO's 2024 Tariff Booklet for Southern Ports — genuine, current, official port-cost data, useful
for port-infrastructure-economics context and cross-country port-cost benchmarking, but **not**
a throughput time series. Harmonized 2026-07-13 from
`data/raw/iran-ports-maritime-org/statistics/` (2 raw PDFs, unchanged).

## Files

| File | What it covers |
|---|---|
| `thc_container_handling_charges_2024.csv` | Terminal Handling Charge (THC) per container, the standard internationally-comparable port-cost benchmark: $177 (20ft) / $266 (40ft) for full export/import/returned containers, $97 (20ft) / $133 (40ft) for empty containers. |
| `ship_port_dues_2024.csv` | Per-gross-tonnage (GT) port dues and charges for commercial (non-tanker) ships vs. oil tankers/STS operations: entrance dues, loading/discharge dues, light dues, pilotage, dredging/channel-safety, tug operation, marine-safety charges — all in US cents per GT (or per ton for loading/discharge), reflecting Iran's dollar-denominated port-tariff structure even though invoices are typically settled in Rials. |
| `container_storage_charges_2024.csv` | Progressive (demurrage-style) container storage charges in Rials by dwell-time band (free for days 1-5, rising through day-90+), split by 20ft/40ft and full/empty — shows PMO's incentive structure to discourage container dwell time. |

## Extraction method

Both PDFs have clean, fully text-extractable content (modern digitally-produced English-language
tariff schedules, no OCR needed) — extracted via `pdftotext -layout` and manually transcribed
into tidy CSVs.

## Caveats — read before charting

- **This is a tariff/cost schedule, not a volume or throughput series** — there is exactly one
  time point (tariffs effective 21/23 May 2024) for each table; nothing here can be charted as a
  trend without future editions of the same booklet to compare against. If PMO publishes updated
  tariff booklets in future years, re-running this same extraction on the new booklet would create
  a genuine cost-inflation time series — worth revisiting.
- **Only 3 of the source's ~6 major tariff tables were transcribed** (THC, ship port dues,
  container storage) — the booklet also contains a large non-containerized-cargo storage matrix
  (multiple cargo categories × 7 dwell-time bands, `Table 10` in the source), a Container Freight
  Station storage table (`Table 25`), and a rail-services tariff section (`Section 6`), none of
  which were transcribed this pass — a real, logged incompleteness, prioritized against this
  project's broader remaining backlog; flagged as a natural next-pass target if port-cost detail
  is ever specifically prioritized.
- **THC and port-dues rates are stated in USD/US cents** but actual invoices in Iran are typically
  settled in Rials at whatever exchange rate regime applies at payment time (the booklet's own
  "General Conditions" section, not transcribed here, specifies exchange-rate-determination rules
  for late payment) — do not treat the USD figures as a literal Rial-equivalent price without
  accounting for Iran's multi-tier exchange rate system (see this project's parallel-market FX
  series elsewhere in `data/processed/` for context).
- **"Southern Ports" only** — this tariff booklet explicitly covers PMO's southern (Persian
  Gulf/Gulf of Oman) ports; a separate northern-ports (Caspian Sea) tariff booklet likely exists
  but was not part of this download.

## Sources

Ports and Maritime Organization of Iran (PMO), Ministry of Roads and Urban Development,
Directorate General of Transit, Logistics and International Agreements:
- `data/raw/iran-ports-maritime-org/statistics/pmo_southern_ports_tariff_booklet_2024.pdf` (63pp, effective 21 May 2024)
- `data/raw/iran-ports-maritime-org/statistics/pmo_tariff_table10_storage_charges_2024.pdf` (3pp excerpt, effective 23 May 2024)

Full manifest (recovered via Wayback Machine, live en.pmo.ir unreachable from this network):
`data/raw/iran-ports-maritime-org/statistics/manifest.json`.
