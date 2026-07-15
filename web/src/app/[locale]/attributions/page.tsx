import type { Metadata } from "next";
import { notFound } from "next/navigation";

import { isLocale, type Locale } from "@/lib/i18n/config";

const STRINGS = {
  en: {
    title: "License & Attribution",
    faNote: "",
  },
  fa: {
    title: "مجوز و انتساب",
    faNote:
      "متن رسمی سیاست مجوز و انتساب وبگاه داده‌های اقتصادی ایران به زبان انگلیسی است و در ادامه آمده است.",
  },
};

export async function generateMetadata({
  params,
}: {
  params: Promise<{ locale: string }>;
}): Promise<Metadata> {
  const { locale } = await params;
  return { title: locale === "fa" ? STRINGS.fa.title : STRINGS.en.title };
}

export default async function AttributionsPage({
  params,
}: {
  params: Promise<{ locale: string }>;
}) {
  const { locale: rawLocale } = await params;
  if (!isLocale(rawLocale)) notFound();
  const locale = rawLocale as Locale;
  const t = STRINGS[locale];

  return (
    <div className="mx-auto max-w-3xl px-4 py-10 sm:px-6">
      <h1 className="text-2xl font-semibold tracking-tight">{t.title}</h1>
      {locale === "fa" ? (
        <p className="mt-3 text-sm leading-relaxed text-muted-foreground">
          {t.faNote}
        </p>
      ) : null}

      <div dir="ltr" className="mt-8 space-y-6 text-sm leading-relaxed">
        <section className="rise-in border border-border/60 bg-card/40 p-5">
          <h2 className="data-label">Dual license</h2>
          <ul className="mt-3 list-disc space-y-2 ps-5">
            <li>
              <strong>Code</strong> (pipeline scripts and this website), MIT
              License.
            </li>
            <li>
              <strong>Data</strong> (the harmonized, deduplicated, chart-ready
              compilation: per-chart data and metadata, the chart registry, the
              policy timeline, and generated catalog/download packages),{" "}
              <a
                href="https://creativecommons.org/licenses/by/4.0/"
                target="_blank"
                rel="noopener noreferrer"
                className="underline decoration-border underline-offset-2 hover:decoration-foreground"
              >
                Creative Commons Attribution 4.0 International (CC BY 4.0)
              </a>
              .
            </li>
          </ul>
        </section>

        <section className="rise-in border border-border/60 bg-card/40 p-5">
          <h2 className="data-label">You are free to</h2>
          <ul className="mt-3 list-disc space-y-2 ps-5">
            <li>
              <strong>Share</strong>, copy and redistribute the material in any
              medium or format.
            </li>
            <li>
              <strong>Adapt</strong>, remix, transform, and build upon the
              material, for any purpose, even commercially.
            </li>
          </ul>
        </section>

        <section className="rise-in border border-border/60 bg-card/40 p-5">
          <h2 className="data-label">Under the following terms</h2>
          <ul className="mt-3 list-disc space-y-2 ps-5">
            <li>
              <strong>Attribution</strong>: give appropriate credit to{" "}
              <a
                href="https://rohamhosseini.com"
                target="_blank"
                rel="noopener noreferrer"
                className="underline decoration-border underline-offset-2 hover:decoration-foreground"
              >
                Roham Hosseini
              </a>{" "}
              / Iran in Data (iranindata.org), provide a link to the license,
              and indicate if changes were made. You may do so in any
              reasonable manner, but not in any way that suggests the licensor
              endorses you or your use.
            </li>
            <li>
              <strong>No additional restrictions</strong>: you may not apply
              legal terms or technological measures that legally restrict
              others from doing anything the license permits.
            </li>
          </ul>
        </section>

        <section className="rise-in border border-border/60 bg-card/40 p-5">
          <h2 className="data-label">Upstream sources</h2>
          <p className="mt-3">
            This compilation license does <strong>not</strong> override the
            terms of the original upstream sources the data was harmonized
            from. Every chart carries its own citations pointing to the
            original source organization (World Bank, FAOSTAT, IMF, national
            statistical agencies, declassified US government documents,
            academic papers, and others). Some upstream sources have their own
            license or usage terms, for example a specific attribution format,
            or restrictions on commercial redistribution of the original,
            unmodified dataset. Before redistributing data from a specific
            chart at scale, check that chart&apos;s own citation and the
            original source&apos;s terms. The CC BY 4.0 license covers this
            project&apos;s own compilation, harmonization, deduplication, and
            derived-value work (such as the real/USD currency conversions),
            not a re-licensing of upstream sources that may carry different
            terms.
          </p>
        </section>
      </div>
    </div>
  );
}
