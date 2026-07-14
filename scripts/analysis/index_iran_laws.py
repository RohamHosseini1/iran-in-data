#!/usr/bin/env python3
"""
index_iran_laws.py -- parse + economically screen the Iranian laws corpus.

Input: ~17.7k scraped Persian law/regulation .txt files (majlis/dotic corpus).
Each file carries a title, a Jalali enactment date ("مصوب ۱۳۸۳ / ۰۳ / ۱۶ <body>"),
site-chrome boilerplate, subject/topic codes, and the legal text.

Most of the corpus is irrelevant to economic charts (court rulings, appointments,
council memberships). This does the CHEAP filtering first -- no LLM -- so agent
effort is only spent on plausibly chart-relevant policy.

Outputs (data/processed/laws/):
  laws_index.csv            -- every file parsed: id, title, jalali/gregorian date, body, path
  laws_economic_shortlist.csv -- the screened subset, with matched keywords + score

Read-only w.r.t. the corpus.
"""
import csv, os, re, sys, hashlib
from collections import Counter
from concurrent.futures import ThreadPoolExecutor

# The corpus lives under ~/Documents, which is cloud-synced: files are dataless
# placeholders and each read costs a ~0.6s round-trip (17.7k files => ~3h serially).
# Reads are LATENCY-bound, not CPU-bound, so a fat thread pool collapses that to
# minutes. Do not "optimize" this back to a serial loop.
READ_WORKERS = 64

CORPUS = "/Users/rohamhosseini/Documents/scraper simple/laws_clean"
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUTDIR = os.path.join(ROOT, "data", "processed", "laws")
csv.field_size_limit(sys.maxsize)

# Court-ruling folders: administrative/supreme-court votes, not policy. Deprioritized.
COURT_DIRS = {"Divan_edalat_edari_votes", "Divan_aali_votes"}

FA_DIGITS = str.maketrans("۰۱۲۳۴۵۶۷۸۹", "0123456789")
DATE_RE = re.compile(r"مصوب\s*([۰-۹0-9]{4})\s*/\s*([۰-۹0-9]{1,2})\s*/\s*([۰-۹0-9]{1,2})")
BODY_RE = re.compile(r"مصوب\s*[۰-۹0-9/\s]+([^\n]*)")

# Scraped site chrome to drop when extracting real text
BOILER = {
    "اطلاعات پایه", "متن", "تصویر", "کدهای موضوعی", "اطلاعات تنقیحی",
    "قوانین ومقررات مرتبط", "درختواره", "جستجو", "عنوان", "تطبیق",
    "همه واژه‌ها", "عین عبارت", "بخشی از واژه‌ها", "یکی از واژه‌ها",
    "تطبیق متن با جستجو", "تطبیق متن با موضوع", "راهنمای رنگ‌بندی",
    "معتبر، تنفیذ", "تفسیر", "پرده زمانی", "نمایش تفاسیر", "مرحله تصویب",
    "متن تفسیر", "منسوخه، موقوف الاجرا",
}

# Persian economic-policy vocabulary. A law must plausibly MOVE an economic measure.
KEYWORDS = [
    # fiscal / tax / budget
    "مالیات", "مالیات بر ارزش افزوده", "بودجه", "گمرک", "حقوق گمرکی", "تعرفه", "عوارض",
    # money / banking / FX
    "بانک", "بانکی", "تسهیلات", "اعتبار", "وام", "نرخ ارز", "ارز", "نقدینگی", "تورم",
    "سود بانکی", "بهره", "بیمه", "بورس", "سهام",
    # subsidies / prices / welfare
    "یارانه", "هدفمند", "قیمت‌گذاری", "قیمت گذاری", "نرخ‌گذاری", "سهمیه", "کوپن",
    # trade
    "صادرات", "واردات", "بازرگانی", "تجارت", "مناطق آزاد", "ممنوعیت واردات",
    # energy / oil
    "نفت", "گاز", "پتروشیمی", "بنزین", "سوخت", "برق", "انرژی", "پالایش",
    # industry / mining / privatization / investment
    "صنعت", "صنایع", "معدن", "معادن", "خصوصی‌سازی", "خصوصی سازی", "اصل ۴۴", "اصل44",
    "سرمایه‌گذاری", "سرمایه گذاری", "ملی شدن", "واگذاری",
    # agriculture / land
    "کشاورزی", "گندم", "اصلاحات ارضی", "زمین", "آب", "دام", "خرید تضمینی",
    # labor / housing
    "دستمزد", "حداقل دستمزد", "کار", "اشتغال", "بیکاری", "مسکن", "اجاره",
    # planning
    "برنامه توسعه", "برنامه پنج‌ساله", "خصوصی",
]
# Strong signals (weight more) -- these almost always mean a real economic policy
STRONG = {"یارانه", "هدفمند", "نرخ ارز", "مالیات بر ارزش افزوده", "خصوصی‌سازی", "اصل ۴۴",
          "اصلاحات ارضی", "خرید تضمینی", "تعرفه", "حقوق گمرکی", "برنامه توسعه", "ملی شدن",
          "قیمت‌گذاری", "حداقل دستمزد", "نقدینگی", "بورس"}

# Obvious non-policy noise in titles
NOISE = ["عضويت", "عضویت", "انتصاب", "شورای فرهنگی", "تفسيري", "تفسیری", "شکایت", "ابطال"]


def jalali_to_gregorian(jy, jm, jd):
    """Standard Jalali->Gregorian conversion (no external deps)."""
    jy += 1595
    days = -355668 + (365 * jy) + ((jy // 33) * 8) + (((jy % 33) + 3) // 4) + jd
    days += (jm - 1) * 31 if jm < 7 else ((jm - 7) * 30 + 186)
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
    sal_a = [0, 31, 29 if (gy % 4 == 0 and gy % 100 != 0) or (gy % 400 == 0) else 28,
             31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    gm = 0
    for gm in range(1, 13):
        if gd <= sal_a[gm]:
            break
        gd -= sal_a[gm]
    return gy, gm, gd


def read_one(args):
    path, folder = args
    try:
        return path, folder, open(path, encoding="utf-8", errors="replace").read()
    except Exception:
        return path, folder, None


def parse(path, folder, raw):
    if raw is None:
        return None
    lines = [l.strip() for l in raw.splitlines() if l.strip()]
    if not lines:
        return None

    m = DATE_RE.search(raw)
    jy = jm = jd = None
    gy = ""
    if m:
        jy, jm, jd = (int(g.translate(FA_DIGITS)) for g in m.groups())
        if 1200 < jy < 1500 and 1 <= jm <= 12 and 1 <= jd <= 31:
            gy, _, _ = jalali_to_gregorian(jy, jm, jd)
        else:
            jy = None

    bm = BODY_RE.search(raw)
    enacting = (bm.group(1).strip() if bm else "")[:60]

    # title: filename is the most reliable (site chrome pollutes line 1)
    title = os.path.splitext(os.path.basename(path))[0]
    title = re.sub(r"_?\d{8,}$", "", title)          # strip trailing scrape id
    title = title.replace("_", " ").strip()
    if not title or title.replace(" ", "").isdigit():
        cand = [l for l in lines[:3] if not l.startswith("مصوب") and l not in BOILER]
        title = cand[0] if cand else "(untitled)"

    text = "\n".join(l for l in lines if l not in BOILER)
    return dict(
        law_id=hashlib.md5(path.encode()).hexdigest()[:12],
        folder=folder, title=title[:300],
        jalali_year=jy or "", jalali_date=(f"{jy}/{jm:02d}/{jd:02d}" if jy else ""),
        gregorian_year=gy, enacting_body=enacting,
        text_len=len(text), path=path, _text=text,
    )


def main():
    os.makedirs(OUTDIR, exist_ok=True)
    jobs = []
    for folder in sorted(os.listdir(CORPUS)):
        d = os.path.join(CORPUS, folder)
        if not os.path.isdir(d):
            continue
        for fn in os.listdir(d):
            if fn.endswith(".txt"):
                jobs.append((os.path.join(d, fn), folder))

    print(f"reading {len(jobs)} files with {READ_WORKERS} threads "
          f"(cloud-synced corpus: reads are latency-bound)...", flush=True)
    rows = []
    done = 0
    with ThreadPoolExecutor(max_workers=READ_WORKERS) as ex:
        for path, folder, raw in ex.map(read_one, jobs):
            done += 1
            if done % 2000 == 0:
                print(f"  read {done}/{len(jobs)}", flush=True)
            r = parse(path, folder, raw)
            if r:
                rows.append(r)

    # ---- economic screen ----
    short = []
    for r in rows:
        if r["folder"] in COURT_DIRS:
            continue  # court rulings: not policy
        hay = r["title"] + "\n" + r["_text"][:6000]
        hits = [k for k in KEYWORDS if k in hay]
        title_hits = [k for k in KEYWORDS if k in r["title"]]
        strong_hits = [k for k in hits if k in STRONG]
        if not title_hits and not strong_hits:
            continue  # needs an economic term in the TITLE or a strong signal
        if any(n in r["title"] for n in NOISE) and not strong_hits:
            continue
        score = 3 * len(strong_hits) + 2 * len(title_hits) + len(hits)
        r2 = dict(r)
        r2["matched"] = "|".join(sorted(set(title_hits + strong_hits))[:8])
        r2["score"] = score
        short.append(r2)

    cols = ["law_id", "folder", "title", "jalali_date", "gregorian_year", "enacting_body",
            "text_len", "path"]
    with open(os.path.join(OUTDIR, "laws_index.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        for r in rows:
            w.writerow({k: r[k] for k in cols})

    short.sort(key=lambda x: -x["score"])
    cols2 = ["score", "matched"] + cols
    with open(os.path.join(OUTDIR, "laws_economic_shortlist.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cols2)
        w.writeheader()
        for r in short:
            w.writerow({k: r[k] for k in cols2})

    print(f"parsed: {len(rows)} files")
    print(f"  with a usable enactment date: {sum(1 for r in rows if r['gregorian_year'])}")
    print(f"economic shortlist: {len(short)}")
    dec = Counter()
    for r in short:
        gy = r["gregorian_year"]
        if gy:
            dec[f"{(int(gy)//10)*10}s"] += 1
    print("shortlist by decade:", dict(sorted(dec.items())))
    print("top folders in shortlist:", dict(Counter(r["folder"] for r in short)))


if __name__ == "__main__":
    main()
