#!/usr/bin/env python3
"""
Daily collector for Iran market data (navasan.tech + brsapi.ir + Central Bank of Iran).

WHY THIS EXISTS
---------------
brsapi's free tier is latest-snapshot-only (its historical endpoint,
Gold_Currency_Pro.php?history=, returns HTTP 402 payment_required), and CBI's exrates page
shows only the current day. Running this script on a schedule is therefore the ONLY way those
sources ever become a time series. navasan does have a free historical endpoint
(/ohlcSearch/), already backfilled to the start of its archive (2019) --
see data/raw/navasan-currency/ohlc-backfill-2019-2026/ -- but appending its daily close here
keeps all three sources moving forward in lockstep.

WHAT IT DOES
------------
One poll per source, appending one dated row per (indicator, source) to the CSVs in
data/processed/iran_api_market_series/. Idempotent: a (date, indicator_id, source_dataset)
triple that is already present is skipped, so re-running on the same day is a no-op and a
missed day simply leaves a gap rather than corrupting anything.

USAGE
-----
    python3 scripts/collect_iran_market_daily.py            # collect today
    python3 scripts/collect_iran_market_daily.py --dry-run  # show what would be appended

Suggested cron (weekdays, after Tehran market close ~ 15:00 Iran time = 11:30 UTC):
    30 12 * * 0-4  cd "/path/to/Iran Economic database" && python3 scripts/collect_iran_market_daily.py >> logs/downloads/iran-market-apis.log 2>&1

SECRETS
-------
API keys are read from secrets/iran_api_keys.env (gitignored) at runtime. They are NEVER
hardcoded here, never printed, and never written to any output file -- every URL this script
logs or records has its key replaced with the literal string REDACTED. The repo is public.

UNITS -- THE ONE THING TO GET RIGHT
-----------------------------------
Everything is emitted in RIAL. Iranian sites quote in Toman (= 10 rial), and navasan is
inconsistent about the scale ACROSS ITS OWN ENDPOINTS:
  * navasan /latest/  FX fields  (harat_naghdi_sell/buy, usd_usdt) -> plain toman     -> x10
  * navasan /latest/  COIN fields (bahar, sekkeh)                  -> THOUSANDS toman -> x10,000
  * navasan /ohlcSearch/ coin fields (bahar, sekkeh)               -> plain toman     -> x10
  * brsapi  (all toman-denominated items, unit field == "تومان")   -> plain toman     -> x10
  * CBI exrates                                                    -> already rial    -> x1
These factors were verified empirically against the project's own TGJU series across ~2,000
overlapping days (median ratio ~1.00). Do not "simplify" them without re-verifying.
"""

import argparse
import csv
import json
import os
import re
import sys
import urllib.parse
import urllib.request

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SECRETS = os.path.join(REPO, "secrets", "iran_api_keys.env")
OUTDIR = os.path.join(REPO, "data", "processed", "iran_api_market_series")

FIELDS = ["country_iso3", "indicator_id", "date", "year", "value", "unit",
          "source_dataset", "notes"]

USD_CSV = os.path.join(OUTDIR, "usd_irr_navasan_brsapi_cbi_2026.csv")
BAHAR_CSV = os.path.join(OUTDIR, "gold_coin_bahar_azadi_navasan_brsapi_2026.csv")
EMAMI_CSV = os.path.join(OUTDIR, "gold_coin_emami_navasan_brsapi_2026.csv")
COMMODITY_CSV = os.path.join(OUTDIR, "global_commodities_brsapi_2026-07-14.csv")

TOMAN_TO_RIAL = 10
LATEST_COIN_TO_RIAL = 10_000

TIMEOUT = 30
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"

#: cbi.ir sits behind an F5/TSPD bot-check that intermittently serves a JavaScript challenge
#: page instead of the real one. A bare User-Agent is NOT enough -- the full browser-like header
#: set below gets through reliably, and collect_cbi() additionally detects the challenge page
#: (marker: "bobcmn") and retries. brsapi's docs likewise require a real browser User-Agent.
BROWSER_HEADERS = {
    "User-Agent": UA,
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9,fa;q=0.8",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
}


# ---------------------------------------------------------------- secrets

def load_keys():
    """Read API keys from the gitignored secrets file. Never logged, never written out."""
    if not os.path.exists(SECRETS):
        sys.exit(f"ERROR: {SECRETS} not found. Cannot run without API keys.")
    keys = {}
    with open(SECRETS, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            keys[k.strip()] = v.strip().strip('"').strip("'")
    missing = [k for k in ("BRSAPI_KEY", "NAVASAN_KEY") if not keys.get(k)]
    if missing:
        sys.exit(f"ERROR: missing key(s) in {SECRETS}: {', '.join(missing)}")
    return keys


def redact(url):
    """Strip any api key from a URL before it is printed or stored."""
    return re.sub(r"((?:api_)?key=)[^&]+", r"\1REDACTED", url, flags=re.I)


def fetch(url, as_json=True):
    req = urllib.request.Request(url, headers=BROWSER_HEADERS)
    with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
        raw = resp.read()
    return json.loads(raw) if as_json else raw.decode("utf-8", errors="replace")


# ---------------------------------------------------------------- calendar

def jalali_to_iso(jdate):
    """Jalali 'YYYY-MM-DD' (or with slashes) -> Gregorian ISO 'YYYY-MM-DD'."""
    jy, jm, jd = (int(x) for x in jdate.replace("/", "-").split("-"))
    jy += 1595
    days = -355668 + (365 * jy) + ((jy // 33) * 8) + (((jy % 33) + 3) // 4) + jd
    days += (jm - 1) * 31 if jm < 7 else ((jm - 7) * 30) + 186
    gy = 400 * (days // 146097)
    days %= 146097
    if days > 36524:
        days -= 1
        gy += 100 * (days // 36524)
        days %= 36524
        if days >= 365:
            days += 1
    gy += 4 * (days // 1461)
    days %= 1461
    if days > 365:
        gy += (days - 1) // 365
        days = (days - 1) % 365
    gd = days + 1
    leap = gy % 4 == 0 and (gy % 100 != 0 or gy % 400 == 0)
    months = [0, 31, 29 if leap else 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    gm = 0
    for i in range(1, 13):
        if gd <= months[i]:
            gm = i
            break
        gd -= months[i]
    return f"{gy:04d}-{gm:02d}-{int(gd):02d}"


# ---------------------------------------------------------------- csv io

def existing_keys(path):
    """Set of (date, indicator_id, source_dataset) already in the file -- for idempotency."""
    if not os.path.exists(path):
        return set()
    with open(path, newline="", encoding="utf-8") as f:
        return {(r["date"], r["indicator_id"], r["source_dataset"]) for r in csv.DictReader(f)}


def append_rows(path, rows, dry_run=False):
    """Append only rows whose (date, indicator, source) key is not already present."""
    have = existing_keys(path)
    new = [r for r in rows
           if (r["date"], r["indicator_id"], r["source_dataset"]) not in have]
    if not new:
        print(f"  {os.path.basename(path)}: nothing new (already have today's rows)")
        return 0
    if dry_run:
        for r in new:
            print(f"  [dry-run] {os.path.basename(path)} += {r['date']} {r['indicator_id']} "
                  f"{r['value']:,} {r['unit']} ({r['source_dataset']})")
        return len(new)

    need_header = not os.path.exists(path) or os.path.getsize(path) == 0
    with open(path, "a", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        if need_header:
            w.writeheader()
        w.writerows(new)
    for r in new:
        print(f"  {os.path.basename(path)} += {r['date']} {r['indicator_id']} "
              f"{r['value']:,} {r['unit']} ({r['source_dataset']})")
    return len(new)


def row(indicator_id, date, value, unit, source_dataset, notes, country="IRN"):
    return dict(country_iso3=country, indicator_id=indicator_id, date=date, year=date[:4],
                value=value, unit=unit, source_dataset=source_dataset, notes=notes)


# ---------------------------------------------------------------- collectors

def collect_navasan(key):
    """navasan /latest/ -- FX (plain toman) and coins (THOUSANDS of toman)."""
    url = f"http://api.navasan.tech/latest/?api_key={urllib.parse.quote(key)}"
    print(f"navasan: GET {redact(url)}")
    d = fetch(url)
    usd, bahar, emami = [], [], []

    for field, tag, label in [
        ("harat_naghdi_sell", "navasan_latest_harat_naghdi_sell", "Herat-market free-market USD sell rate"),
        ("harat_naghdi_buy", "navasan_latest_harat_naghdi_buy", "Herat-market free-market USD buy rate"),
        ("usd_usdt", "navasan_latest_usd_usdt", "USD/USDT-referenced free-market rate"),
    ]:
        rec = d.get(field)
        if not rec:
            print(f"  WARN: navasan field '{field}' missing from response; skipped")
            continue
        iso = jalali_to_iso(rec["date"].split(" ")[0])
        usd.append(row("usd_irr_parallel_rate", iso,
                       round(float(rec["value"]) * TOMAN_TO_RIAL, 2), "rial per USD", tag,
                       f"{label}, navasan /latest/ (plain toman x10). Timestamp {rec['date']} Tehran. "
                       f"Collected by scripts/collect_iran_market_daily.py."))

    for field, tag, target, name in [
        ("bahar", "navasan_latest_bahar", bahar, "Bahar Azadi"),
        ("sekkeh", "navasan_latest_sekkeh", emami, "Emami"),
    ]:
        rec = d.get(field)
        if not rec:
            print(f"  WARN: navasan field '{field}' missing from response; skipped")
            continue
        iso = jalali_to_iso(rec["date"].split(" ")[0])
        ind = "gold_coin_bahar_azadi_price" if field == "bahar" else "gold_coin_emami_price"
        target.append(row(ind, iso,
                          round(float(rec["value"]) * LATEST_COIN_TO_RIAL, 2), "rial per coin", tag,
                          f"{name} coin, navasan /latest/ -- field is in THOUSANDS of toman, x10,000 "
                          f"for rial (NOT x10 like ohlcSearch). Timestamp {rec['date']} Tehran. "
                          f"Collected by scripts/collect_iran_market_daily.py."))
    return usd, bahar, emami


def collect_brsapi(key):
    """brsapi Gold_Currency.php + Commodity.php -- both plain toman / plain USD."""
    usd, bahar, emami, commodities = [], [], [], []

    url = f"https://Api.BrsApi.ir/Market/Gold_Currency.php?key={urllib.parse.quote(key)}"
    print(f"brsapi: GET {redact(url)}")
    d = fetch(url)

    for item in d.get("currency", []):
        if item["symbol"] in ("USD", "USDT_IRT"):
            iso = jalali_to_iso(item["date"])
            usd.append(row("usd_irr_parallel_rate", iso,
                           round(float(item["price"]) * TOMAN_TO_RIAL, 2), "rial per USD",
                           f"brsapi_currency_{item['symbol']}",
                           f"BrsAPI {item['name_en']}, unit field='{item['unit']}' (toman) x10. "
                           f"Time {item['time']} Tehran ({item['date']}). "
                           f"Collected by scripts/collect_iran_market_daily.py."))

    for item in d.get("gold", []):
        if item["symbol"] not in ("IR_COIN_BAHAR", "IR_COIN_EMAMI"):
            continue
        iso = jalali_to_iso(item["date"])
        is_bahar = item["symbol"] == "IR_COIN_BAHAR"
        (bahar if is_bahar else emami).append(row(
            "gold_coin_bahar_azadi_price" if is_bahar else "gold_coin_emami_price", iso,
            round(float(item["price"]) * TOMAN_TO_RIAL, 2), "rial per coin",
            f"brsapi_gold_{item['symbol']}",
            f"BrsAPI {item['name_en']}, unit field='{item['unit']}' (toman) x10. "
            f"Time {item['time']} Tehran ({item['date']}). "
            f"Collected by scripts/collect_iran_market_daily.py."))

    # Global commodities: latest-only on the free tier, so appending daily is what
    # eventually turns these single points into a real series.
    url = f"https://Api.BrsApi.ir/Market/Commodity.php?key={urllib.parse.quote(key)}"
    print(f"brsapi: GET {redact(url)}")
    c = fetch(url)
    UNITS = {"XAUUSD": "USD per troy ounce", "XAGUSD": "USD per troy ounce",
             "XPTUSD": "USD per troy ounce", "XPDUSD": "USD per troy ounce",
             "Cu": "USD per metric ton", "Al": "USD per metric ton", "Zn": "USD per metric ton",
             "Pb": "USD per metric ton", "Ni": "USD per metric ton", "BRENT": "USD per barrel",
             "WTI": "USD per barrel", "GAS": "USD per mmBtu", "RBOB": "USD per gallon",
             "GASOIL": "USD per metric ton"}
    NAMES = {"XAUUSD": "gold_ounce_spot_usd", "XAGUSD": "silver_ounce_spot_usd",
             "XPTUSD": "platinum_ounce_spot_usd", "XPDUSD": "palladium_ounce_spot_usd",
             "Cu": "copper_spot_usd", "Al": "aluminum_spot_usd", "Zn": "zinc_spot_usd",
             "Pb": "lead_spot_usd", "Ni": "nickel_spot_usd", "BRENT": "brent_crude_spot_usd",
             "WTI": "wti_crude_spot_usd", "GAS": "natural_gas_spot_usd",
             "RBOB": "rbob_gasoline_spot_usd", "GASOIL": "gasoil_spot_usd"}
    for group in ("metal_precious", "metal_base", "energy"):
        for item in c.get(group, []):
            sym = item["symbol"]
            iso = jalali_to_iso(item["date"])
            commodities.append(row(NAMES.get(sym, sym), iso, item["price"],
                                   UNITS.get(sym, "USD"), f"brsapi_commodity_{sym}",
                                   f"BrsAPI {item['name']} ({sym}), global USD spot price. "
                                   f"Time {item['time']} Tehran ({item['date']}). "
                                   f"Collected by scripts/collect_iran_market_daily.py.",
                                   country="GLOBAL"))
    return usd, bahar, emami, commodities


#: CBI renders every number in Persian (Extended Arabic-Indic) digits, e.g. "۱,۳۵۹,۷۱۲".
#: An ASCII-digit regex finds NOTHING on that page -- translate first, then parse.
FA_DIGITS = str.maketrans("۰۱۲۳۴۵۶۷۸۹٠١٢٣٤٥٦٧٨٩", "01234567890123456789")


def collect_cbi():
    """Scrape today's official/NIMA-weighted USD rate from CBI's own exrates page.

    Page structure (verified against the 2026-07-14 snapshot in
    data/raw/cbi-reference-rates/exrates-2026-07-14/):
        <span id="...lblDate">۱۴۰۵/۰۴/۲۳</span>
        <tr><td>USD</td><td>دلار آمريکا</td><td>۱,۳۵۹,۷۱۲</td>...
    """
    url = "https://www.cbi.ir/exrates/rates_fa.aspx"
    print(f"cbi: GET {url}")

    html = None
    for attempt in range(1, 4):  # the F5/TSPD bot-check fires intermittently -- retry
        try:
            candidate = fetch(url, as_json=False)
        except Exception as e:  # CBI is occasionally unreachable; a missed day is just a gap
            print(f"  WARN: CBI fetch failed on attempt {attempt} ({e})")
            continue
        if "bobcmn" in candidate:  # marker of the JS bot-challenge interstitial
            print(f"  note: CBI served its bot-challenge page on attempt {attempt}; retrying")
            continue
        html = candidate
        break

    if html is None:
        print("  WARN: CBI unreachable or bot-blocked after 3 attempts; skipping CBI this run")
        return []

    html = html.translate(FA_DIGITS)  # Persian digits -> ASCII

    # The USD row: a <td> holding exactly "USD", then the Persian name, then the rate.
    m = re.search(r"<td[^>]*>\s*USD\s*</td>\s*<td[^>]*>.*?</td>\s*<td[^>]*>\s*([\d,]+)\s*</td>",
                  html, re.S)
    if not m:
        print("  WARN: could not locate the USD row in CBI's page (layout may have changed); "
              "skipping CBI this run")
        return []
    value = float(m.group(1).replace(",", ""))

    dm = re.search(r'lblDate[^>]*>\s*(\d{4}/\d{2}/\d{2})', html)
    if not dm:
        print("  WARN: could not locate the rate date on CBI's page; skipping CBI this run")
        return []
    iso = jalali_to_iso(dm.group(1))

    # Guard: if the layout shifts and we grab the wrong cell, fail loudly rather than
    # writing a garbage number into the database.
    if not (100_000 <= value <= 100_000_000):
        print(f"  WARN: CBI USD value {value:,.0f} is outside the sane range for rial/USD; "
              f"skipping (the page layout has probably changed -- check it)")
        return []

    return [row("usd_irr_official_rate", iso, value, "rial per USD",
                "cbi_exrates_official_nima_weighted",
                f"CBI official/NIMA volume-weighted rate, scraped from cbi.ir/exrates/rates_fa.aspx "
                f"({dm.group(1)} Jalali). Already in rial, no conversion. "
                f"Collected by scripts/collect_iran_market_daily.py.")]


# ---------------------------------------------------------------- main

def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--dry-run", action="store_true",
                    help="fetch and show what would be appended, but write nothing")
    args = ap.parse_args()

    keys = load_keys()
    os.makedirs(OUTDIR, exist_ok=True)

    usd, bahar, emami, commodities = [], [], [], []

    try:
        n_usd, n_bahar, n_emami = collect_navasan(keys["NAVASAN_KEY"])
        usd += n_usd
        bahar += n_bahar
        emami += n_emami
    except Exception as e:
        print(f"  WARN: navasan collection failed ({e}); continuing with other sources")

    try:
        b_usd, b_bahar, b_emami, b_com = collect_brsapi(keys["BRSAPI_KEY"])
        usd += b_usd
        bahar += b_bahar
        emami += b_emami
        commodities += b_com
    except Exception as e:
        print(f"  WARN: brsapi collection failed ({e}); continuing with other sources")

    usd += collect_cbi()

    total = 0
    total += append_rows(USD_CSV, usd, args.dry_run)
    total += append_rows(BAHAR_CSV, bahar, args.dry_run)
    total += append_rows(EMAMI_CSV, emami, args.dry_run)
    total += append_rows(COMMODITY_CSV, commodities, args.dry_run)

    verb = "would append" if args.dry_run else "appended"
    print(f"done: {verb} {total} new row(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
