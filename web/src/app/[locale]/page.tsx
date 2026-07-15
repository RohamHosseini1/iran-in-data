import Link from "next/link";
import { notFound } from "next/navigation";

import { getCatalog, getCategories, getChartEntry } from "@/lib/data/catalog";
import { isLocale, type Locale } from "@/lib/i18n/config";
import { ChartBrowser } from "@/components/browse/chart-browser";
import { CountUp } from "@/components/delight/count-up";
import { ScrambleText } from "@/components/delight/scramble-text";
import { Button } from "@/components/ui/button";

const STRINGS = {
  en: {
    eyebrow: "Open data archive · 1800–2026",
    tagline: "A narrative of Iran's economic history, told in facts and figures",
    description:
      "Iran in Data is the open, cited encyclopedia of Iran's economy. Every chart traces Iran's economic and social record, currency and trade, industry and agriculture, demographics and public finance. Sourced, cited, and free.",
    browse: "Browse the charts",
    charts: "Charts",
    categories: "Categories",
    yearsOfRecord: "Sources",
    featured: "Featured_Series",
    directory: "Record_Queue",
  },
  fa: {
    eyebrow: "بایگانی داده باز · ۱۸۰۰–۲۰۲۶",
    tagline: "روایتی از تاریخ اقتصادی ایران با آمار و ارقام",
    description:
      "هر نمودار روایتی از کارنامه اقتصادی و اجتماعی ایران است، ارز و تجارت، صنعت و کشاورزی، جمعیت و مالیه عمومی. مستند، با ذکر منبع و رایگان.",
    browse: "مرور نمودارها",
    charts: "نمودار",
    categories: "دسته",
    yearsOfRecord: "منبع",
    featured: "سری‌های برگزیده",
    directory: "فهرست رکوردها",
  },
};

const FEATURED_IDS = [
  "wdi__NY.GDP.MKTP",
  "fx__official_vs_parallel_gap_irn",
  "wdi__FP.CPI.TOTL",
  "wdi__SP.POP",
  "weo__ppp_share_world_gdp",
  "iran_fx__usd_irr_parallel_rate_daily_2011_2026",
];

export default async function HomePage({
  params,
}: {
  params: Promise<{ locale: string }>;
}) {
  const { locale: rawLocale } = await params;
  if (!isLocale(rawLocale)) notFound();
  const locale = rawLocale as Locale;
  const t = STRINGS[locale];

  const catalog = getCatalog();
  const categories = getCategories();
  const sourceCount = new Set(catalog.map((e) => e.primary_source)).size;

  const featured = FEATURED_IDS.map((id) => getChartEntry(id)).filter(
    (e): e is NonNullable<typeof e> => Boolean(e)
  );

  return (
    <div>
      {/* Hero — minimal, half-viewport, straight to the point */}
      <section className="bg-dotgrid border-b border-border/60">
        <div className="mx-auto flex min-h-[55svh] max-w-6xl flex-col items-center justify-center px-4 py-16 text-center sm:px-6">
          <p className="data-label">
            <ScrambleText text={t.eyebrow} duration={900} />
          </p>
          <h1 className="mt-4 text-4xl font-semibold tracking-tight sm:text-6xl">
            {locale === "fa" ? "داده‌های اقتصادی ایران" : "Iran in Data"}
          </h1>
          <p className="mt-3 text-lg text-muted-foreground sm:text-xl">
            {t.tagline}
          </p>
          <p className="mt-5 max-w-2xl text-sm leading-relaxed text-muted-foreground">
            {t.description}
          </p>

          {/* Stat strip */}
          <dl className="mt-10 grid grid-cols-3 gap-8 sm:gap-14" dir="ltr">
            <Stat label={t.charts} value={catalog.length} />
            <Stat label={t.categories} value={categories.length} />
            <Stat label={t.yearsOfRecord} value={sourceCount} />
          </dl>

          <Button
            nativeButton={false}
            render={<Link href={`/${locale}/charts`} />}
            className="mt-10 rounded-none px-6"
            size="lg"
          >
            {t.browse}
          </Button>
        </div>
      </section>

      {/* Featured series */}
      <section className="mx-auto max-w-6xl px-4 py-12 sm:px-6">
        <h2 className="data-label">{t.featured}</h2>
        <ul className="mt-4 grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
          {featured.map((e) => (
            <li key={e.chart_id}>
              <Link
                href={`/${locale}/charts/${encodeURIComponent(e.chart_id)}`}
                className="corner-frame group block h-full border border-border/60 bg-card/40 p-4 transition-colors hover:border-foreground/30 hover:bg-muted/40"
              >
                <span className="line-clamp-2 text-sm font-medium">
                  {locale === "fa" ? e.title_fa : e.title}
                </span>
                <span className="data-label mt-2 block">
                  {locale === "fa" ? e.category_fa : e.category}
                </span>
                <span className="font-data mt-1 block text-[10px] text-muted-foreground" dir="ltr">
                  {e.year_range[0]}–{e.year_range[1]} · {e.countries.length}{" "}
                  {locale === "fa" ? "کشور" : (e.countries.length === 1 ? "country" : "countries")}
                </span>
              </Link>
            </li>
          ))}
        </ul>
      </section>

      {/* Record queue — search + directory inline */}
      <section className="mx-auto max-w-6xl px-4 pb-16 sm:px-6" id="browse">
        <h2 className="data-label">{t.directory}</h2>
        <div className="mt-4">
          <ChartBrowser locale={locale} categories={categories} />
        </div>
      </section>
    </div>
  );
}

function Stat({ label, value }: { label: string; value: number }) {
  return (
    <div className="text-center">
      <dd className="font-data text-3xl font-light tracking-tight sm:text-4xl">
        <CountUp value={value} />
      </dd>
      <dt className="data-label mt-1">{label}</dt>
    </div>
  );
}
