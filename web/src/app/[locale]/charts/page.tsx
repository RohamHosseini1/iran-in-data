import type { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";

import { getCatalog, getCategories } from "@/lib/data/catalog";
import { isLocale, type Locale } from "@/lib/i18n/config";
import { ChartBrowser } from "@/components/browse/chart-browser";

const STRINGS = {
  en: {
    title: "Chart Directory",
    records: "records",
    fullIndex: "Full index by category",
  },
  fa: {
    title: "فهرست نمودارها",
    records: "رکورد",
    fullIndex: "فهرست کامل بر اساس دسته",
  },
};

export async function generateMetadata({
  params,
}: {
  params: Promise<{ locale: string }>;
}): Promise<Metadata> {
  const { locale } = await params;
  return {
    title: locale === "fa" ? STRINGS.fa.title : STRINGS.en.title,
  };
}

export default async function ChartsPage({
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

  return (
    <div className="mx-auto max-w-6xl px-4 py-10 sm:px-6">
      <div className="flex flex-wrap items-baseline justify-between gap-3">
        <h1 className="text-2xl font-semibold tracking-tight">{t.title}</h1>
        <span className="data-label">
          {catalog.length.toLocaleString("en-US")} {t.records}
        </span>
      </div>

      <div className="mt-6">
        <ChartBrowser locale={locale} categories={categories} />
      </div>

      {/* Crawlable full index — grouped, collapsed by default */}
      <section className="mt-12">
        <h2 className="data-label">{t.fullIndex}</h2>
        <div className="mt-3 divide-y divide-border/50 border border-border/60">
          {categories.map((cat) => (
            <details key={cat.name} className="group">
              <summary className="flex cursor-pointer items-baseline justify-between gap-4 px-4 py-3 transition-colors hover:bg-muted/40">
                <span className="text-sm">
                  {locale === "fa" ? cat.nameFa : cat.name}
                </span>
                <span className="font-data text-[10px] text-muted-foreground">
                  {cat.count}
                </span>
              </summary>
              <ul className="grid gap-x-6 px-4 pb-4 sm:grid-cols-2">
                {catalog
                  .filter((e) => e.category === cat.name)
                  .map((e) => (
                    <li key={e.chart_id}>
                      <Link
                        href={`/${locale}/charts/${encodeURIComponent(e.chart_id)}`}
                        className="block truncate py-1 text-xs text-muted-foreground transition-colors hover:text-foreground"
                      >
                        {locale === "fa" ? e.title_fa : e.title}
                      </Link>
                    </li>
                  ))}
              </ul>
            </details>
          ))}
        </div>
      </section>
    </div>
  );
}
