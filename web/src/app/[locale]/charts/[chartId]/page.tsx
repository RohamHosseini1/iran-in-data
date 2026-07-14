import type { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";

import { getCatalog, getChartData, getChartEntry } from "@/lib/data/catalog";
import { getChartEvents } from "@/lib/data/events";
import { getChartLaws, getEras } from "@/lib/data/annotations";
import { pickDefaultVariant } from "@/lib/charts/variant-labels";
import { labelUnitText } from "@/lib/charts/unit-format";
import { toPersianDigits } from "@/lib/calendar";
import { buildChartPayload } from "@/lib/data/payload";
import { buildLineOption } from "@/lib/charts/line-option";
import { renderChartSvg } from "@/lib/charts/ssr";
import { LIGHT_CHROME } from "@/lib/charts/palette";
import { isLocale, locales, type Locale } from "@/lib/i18n/config";
import { ChartExplorer } from "@/components/charts/chart-explorer";
import { ChartStateProvider } from "@/components/charts/chart-state";
import { LatestReading } from "@/components/charts/latest-reading";
import { ScrambleText } from "@/components/delight/scramble-text";
import { Badge } from "@/components/ui/badge";

export function generateStaticParams() {
  const ids = getCatalog().map((e) => e.chart_id);
  return locales.flatMap((locale) =>
    ids.map((chartId) => ({ locale, chartId }))
  );
}

interface PageProps {
  params: Promise<{ locale: string; chartId: string }>;
}

function resolveChartId(raw: string): string {
  try {
    return decodeURIComponent(raw);
  } catch {
    return raw;
  }
}

export async function generateMetadata({ params }: PageProps): Promise<Metadata> {
  const { locale, chartId } = await params;
  const entry = getChartEntry(resolveChartId(chartId));
  if (!entry || !isLocale(locale)) return {};
  const title = locale === "fa" ? entry.title_fa : entry.title;
  return {
    title,
    description: entry.description || undefined,
    alternates: {
      languages: Object.fromEntries(
        locales.map((l) => [l, `/${l}/charts/${encodeURIComponent(entry.chart_id)}`])
      ),
    },
  };
}

const STRINGS = {
  en: {
    charts: "Charts",
    download: "Download CSV",
    latestReading: "Latest_Reading",
    seriesMeta: "Series_Meta",
    citations: "Citations",
    related: "Related_Charts",
    source: "Source",
    years: "Years",
    countries: "Countries",
    observations: "Observations",
    category: "Category",
    accessed: "Accessed",
    vsPrevYear: "vs. prior year",
    iranSeries: "IRN",
  },
  fa: {
    charts: "نمودارها",
    download: "دریافت CSV",
    latestReading: "آخرین مقدار",
    seriesMeta: "مشخصات سری",
    citations: "منابع",
    related: "نمودارهای مرتبط",
    source: "منبع",
    years: "بازه سال‌ها",
    countries: "کشورها",
    observations: "تعداد مشاهدات",
    category: "دسته",
    accessed: "تاریخ دسترسی",
    vsPrevYear: "نسبت به سال قبل",
    iranSeries: "ایران",
  },
};

export default async function ChartDetailPage({ params }: PageProps) {
  const { locale: rawLocale, chartId: rawChartId } = await params;
  if (!isLocale(rawLocale)) notFound();
  const locale = rawLocale as Locale;
  const chartId = resolveChartId(rawChartId);

  const entry = getChartEntry(chartId);
  if (!entry) notFound();

  const rows = getChartData(chartId);
  const payload = buildChartPayload(rows);
  const t = STRINGS[locale];
  const fa = locale === "fa";
  const title = fa ? entry.title_fa : entry.title;
  const category = fa ? entry.category_fa : entry.category;
  const yearDigits = (v: string | number) => (fa ? toPersianDigits(v) : String(v));
  // Some catalog rows carry a null/short year_range (a known data bug);
  // render an empty range instead of crashing the page.
  const yearRangeText = (range: unknown): string => {
    if (!Array.isArray(range) || range.length < 2) return "";
    return `${yearDigits(range[0])}–${yearDigits(range[1])}`;
  };

  // Initial view: default measure (black-market rate wins for FX charts),
  // Iran only (comparators are opt-in).
  const defaultVariant = pickDefaultVariant(payload.variants);
  const defaultVariantEntry = payload.variants.find(
    (v) => v.code === defaultVariant
  );
  const hasIran = payload.countries.some((c) => c.iso === "IRN");
  const initialCountries = hasIran
    ? ["IRN"]
    : payload.countries.map((c) => c.iso);
  const ssrSvg = renderChartSvg(
    buildLineOption({
      payload,
      variantCode: defaultVariant,
      countries: initialCountries,
      chrome: LIGHT_CHROME,
      animate: false,
      unit:
        defaultVariantEntry?.unit ||
        labelUnitText(defaultVariantEntry?.label) ||
        undefined,
      subYear: payload.subYear,
    }),
    { width: 860, height: 430 }
  );

  const events = getChartEvents(chartId);
  const laws = getChartLaws(chartId);
  const eras = getEras();

  const related = getCatalog()
    .filter((e) => e.category === entry.category && e.chart_id !== entry.chart_id)
    .slice(0, 6);

  const jsonLd = {
    "@context": "https://schema.org",
    "@type": "Dataset",
    name: entry.title,
    description: entry.description || entry.title,
    temporalCoverage:
      Array.isArray(entry.year_range) && entry.year_range.length >= 2
        ? `${entry.year_range[0]}/${entry.year_range[1]}`
        : undefined,
    spatialCoverage: entry.countries.join(", "),
    creator: entry.citations?.[0]?.source_org,
    url: `/${locale}/charts/${encodeURIComponent(entry.chart_id)}`,
    isAccessibleForFree: true,
  };

  return (
    <div className="mx-auto max-w-6xl px-4 py-8 sm:px-6">
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }}
      />

      {/* Header block */}
      <nav className="data-label flex flex-wrap items-center gap-2">
        <Link href={`/${locale}/charts`} className="hover:text-foreground">
          {t.charts}
        </Link>
        <span aria-hidden>/</span>
        <span className="text-foreground/70">{category}</span>
      </nav>

      <div className="mt-4 flex flex-wrap items-start justify-between gap-4">
        <div className="min-w-0 max-w-3xl">
          <div className="flex flex-wrap items-center gap-3">
            <span className="font-data border border-border/80 px-2 py-0.5 text-[11px] text-foreground/80">
              {entry.chart_id}
            </span>
            {yearRangeText(entry.year_range) ? (
              <Badge variant="outline" className="rounded-full font-data text-[10px]">
                {yearRangeText(entry.year_range)}
              </Badge>
            ) : null}
            <a
              href={`/api/charts/${encodeURIComponent(entry.chart_id)}/csv`}
              download={`${entry.chart_id}.csv`}
              className="data-label border border-border/80 px-2 py-1 transition-colors hover:border-foreground/40 hover:text-foreground"
            >
              ↓ {t.download}
            </a>
          </div>
          <h1 className="mt-3 text-2xl font-semibold tracking-tight sm:text-3xl">
            <ScrambleText text={title} duration={700} />
            <span aria-hidden className="blink-cursor">
              _
            </span>
          </h1>
          {/* Catalog descriptions are English-only; hidden on fa until the
              translation pass lands. */}
          {entry.description && !fa ? (
            <p className="mt-3 max-w-prose text-sm leading-relaxed text-muted-foreground">
              {entry.description}
            </p>
          ) : null}
        </div>
      </div>

      {/* Rail + visualizer, sharing the selected-measure state so the
          latest reading always describes what the chart is showing. */}
      <ChartStateProvider initialVariant={defaultVariant}>
      <div className="mt-8 grid gap-6 lg:grid-cols-[272px_minmax(0,1fr)]">
        <aside className="flex flex-col gap-4">
          <LatestReading payload={payload} locale={locale} measureFallback={title} />

          <section
            className="rise-in border border-border/60 bg-card/40 p-4"
            style={{ animationDelay: "90ms" }}
          >
            <h2 className="data-label">{t.seriesMeta}</h2>
            <dl className="mt-3 space-y-2 text-xs">
              <MetaRow label={t.source} value={entry.primary_source} mono />
              <MetaRow label={t.years} value={yearRangeText(entry.year_range)} mono />
              <MetaRow label={t.countries} value={String(entry.countries.length)} mono />
              <MetaRow label={t.observations} value={entry.row_count.toLocaleString("en-US")} mono />
              <MetaRow label={t.category} value={category} />
            </dl>
          </section>

          {entry.citations?.length ? (
            <section
              className="rise-in border border-border/60 bg-card/40 p-4"
              style={{ animationDelay: "180ms" }}
            >
              <h2 className="data-label">{t.citations}</h2>
              <ul className="mt-3 space-y-3">
                {entry.citations.map((c, i) => (
                  <li key={i} className="text-xs leading-relaxed">
                    <span className="text-foreground/90">{c.source_org}</span>
                    {c.source_url ? (
                      <>
                        {", "}
                        <a
                          href={c.source_url.split(" ; ")[0]}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="break-all text-muted-foreground underline decoration-border underline-offset-2 hover:text-foreground"
                        >
                          {shortUrl(c.source_url)}
                        </a>
                      </>
                    ) : null}
                    {c.access_date ? (
                      <div className="data-label mt-1">
                        {t.accessed}: {c.access_date}
                      </div>
                    ) : null}
                  </li>
                ))}
              </ul>
            </section>
          ) : null}
        </aside>

        <div className="rise-in min-w-0" style={{ animationDelay: "60ms" }}>
          <ChartExplorer
            payload={payload}
            locale={locale}
            ssrSvg={ssrSvg}
            events={events}
            laws={laws}
            eras={eras}
          />
        </div>
      </div>
      </ChartStateProvider>

      {/* Related */}
      {related.length ? (
        <section className="mt-10">
          <h2 className="data-label">{t.related}</h2>
          <ul className="mt-3 grid gap-2 sm:grid-cols-2 lg:grid-cols-3">
            {related.map((e, i) => (
              <li
                key={e.chart_id}
                className="rise-in"
                style={{ animationDelay: `${250 + i * 60}ms` }}
              >
                <Link
                  href={`/${locale}/charts/${encodeURIComponent(e.chart_id)}`}
                  className="block border border-border/60 bg-card/40 px-4 py-3 text-sm transition-colors hover:border-foreground/30 hover:bg-muted/40"
                >
                  <span className="line-clamp-2">
                    {locale === "fa" ? e.title_fa : e.title}
                  </span>
                  <span className="data-label mt-1 block">
                    {yearRangeText(e.year_range)}
                  </span>
                </Link>
              </li>
            ))}
          </ul>
        </section>
      ) : null}
    </div>
  );
}

function MetaRow({
  label,
  value,
  mono,
}: {
  label: string;
  value: string;
  mono?: boolean;
}) {
  return (
    <div className="flex items-baseline justify-between gap-3">
      <dt className="data-label shrink-0">{label}</dt>
      <dd className={`text-end ${mono ? "font-data" : ""}`}>{value}</dd>
    </div>
  );
}

function shortUrl(url: string): string {
  const first = url.split(" ; ")[0];
  try {
    const u = new URL(first);
    return u.hostname.replace(/^www\./, "");
  } catch {
    return first.slice(0, 40);
  }
}
