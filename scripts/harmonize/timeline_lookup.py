"""The mechanical link between a chart and its policy-timeline overlay events.

Given a country + one or more economic-domain tags (+ optionally a year range), returns the
matching rows from timeline/*.csv, ready to render as annotation markers. Add a domain tag to a
timeline row once and every chart tagged with that domain picks it up automatically -- no
hand-maintained chart-to-event mapping to keep in sync.

Usage (as a library):
    from timeline_lookup import get_events
    events = get_events(country="IRN", domains=["oil", "fiscal"], year_start=1950, year_end=1979)

Usage (from the command line, for a quick look):
    python3 scripts/harmonize/timeline_lookup.py IRN oil fiscal --start 1950 --end 1979
"""
import csv
import glob
import sys

TIMELINE_DIR = "timeline"


def _load_all_events():
    events = []
    for fpath in glob.glob(f"{TIMELINE_DIR}/*.csv"):
        with open(fpath, encoding="utf-8", newline="") as f:
            for row in csv.DictReader(f):
                row["_source_file"] = fpath
                events.append(row)
    return events


def get_events(country=None, domains=None, year_start=None, year_end=None):
    """Filter timeline events by country (ISO3 or 'GLOBAL'), domain tags (any-match), and year range.

    country: ISO3 string, or None to include all countries (still respects domain/year filters).
             Pass a list to match multiple countries (e.g. ["IRN", "GLOBAL"] to get Iran-specific
             events plus world-level shocks in the same call).
    domains: list of domain strings (fx, inflation, oil, trade, housing, food, banking, fiscal,
             labor) -- an event matches if ANY of its own domains overlap this list. None = all.
    year_start / year_end: inclusive year bounds, inferred from the event's `date` column.
    """
    if isinstance(country, str):
        country = [country]
    domains = set(domains) if domains else None

    results = []
    for row in _load_all_events():
        if country and row["country"] not in country:
            continue
        if domains:
            row_domains = {d.strip() for d in row.get("economic_domains", "").split(";") if d.strip()}
            if not (row_domains & domains):
                continue
        date = row.get("date", "")
        year = None
        if date:
            try:
                year = int(date[:4])
            except ValueError:
                pass
        if year_start is not None and year is not None and year < year_start:
            continue
        if year_end is not None and year is not None and year > year_end:
            continue
        results.append(row)

    results.sort(key=lambda r: r.get("date", ""))
    return results


def _main():
    if len(sys.argv) < 2:
        print(__doc__)
        return
    country = sys.argv[1]
    args = sys.argv[2:]
    domains = [a for a in args if not a.startswith("--") and a not in ("--start", "--end")]
    year_start = year_end = None
    if "--start" in args:
        year_start = int(args[args.index("--start") + 1])
    if "--end" in args:
        year_end = int(args[args.index("--end") + 1])

    for e in get_events(country=country, domains=domains or None, year_start=year_start, year_end=year_end):
        print(f"{e['date']}  [{e['event_type']:<18}]  {e['title']}  ({e['economic_domains']})")


if __name__ == "__main__":
    _main()
