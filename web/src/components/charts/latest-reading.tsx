"use client";

import * as React from "react";

import { useChartVariant } from "./chart-state";
import { friendlyVariantLabel, pickDefaultVariant } from "@/lib/charts/variant-labels";
import { unitInline } from "@/lib/charts/unit-format";
import { toPersianDigits } from "@/lib/calendar";
import type { ChartPayload } from "@/lib/data/payload";
import type { Locale } from "@/lib/i18n/config";
import { CountUp } from "@/components/delight/count-up";

const STRINGS = {
  en: {
    latestReading: "Latest_Reading",
    vsPrevYear: "vs. prior year",
    vsPrev: "vs. prior reading",
    iranSeries: "IRN",
  },
  fa: {
    latestReading: "آخرین مقدار",
    vsPrevYear: "نسبت به سال قبل",
    vsPrev: "نسبت به مقدار قبلی",
    iranSeries: "ایران",
  },
};

interface Latest {
  /** Display label for when the reading is from: year or period label. */
  when: string;
  value: number;
  delta: number | null;
  subYear: boolean;
}

/**
 * Iran's most recent value for the CURRENTLY SELECTED measure (shared state
 * with the visualizer). Number and unit render inline at the same size:
 * "42.1%", "2.5B USD", «۲٫۵ میلیارد دلار آمریکا». Sub-year series surface
 * their true latest observation (e.g. the latest daily FX print), not the
 * annual collapse.
 */
export function LatestReading({
  payload,
  locale,
  measureFallback,
}: {
  payload: ChartPayload;
  locale: Locale;
  /** Localized chart title: shown as the measure when the chart has a single
      variant (the raw dataset label would just repeat the title in English). */
  measureFallback?: string;
}) {
  const t = STRINGS[locale];
  const fa = locale === "fa";
  const [variantCode] = useChartVariant(pickDefaultVariant(payload.variants));
  const variant = payload.variants.find((v) => v.code === variantCode);

  const latest = React.useMemo<Latest | null>(() => {
    // Prefer the sub-year series when it carries this measure: its last
    // observation is the real latest reading.
    const sub = payload.subYear?.values[variantCode]?.["IRN"];
    if (sub && payload.subYear) {
      for (let i = sub.length - 1; i >= 0; i--) {
        if (sub[i] != null) {
          let prev: number | null = null;
          for (let j = i - 1; j >= 0; j--) {
            if (sub[j] != null) {
              prev = sub[j];
              break;
            }
          }
          return {
            when: payload.subYear.labels[i],
            value: sub[i]!,
            delta:
              prev != null && prev !== 0
                ? ((sub[i]! - prev) / Math.abs(prev)) * 100
                : null,
            subYear: true,
          };
        }
      }
    }
    const arr = payload.values[variantCode]?.["IRN"];
    if (!arr) return null;
    for (let i = payload.years.length - 1; i >= 0; i--) {
      if (arr[i] != null) {
        let prev: number | null = null;
        for (let j = i - 1; j >= 0; j--) {
          if (arr[j] != null) {
            prev = arr[j];
            break;
          }
        }
        return {
          when: String(payload.years[i]),
          value: arr[i]!,
          delta:
            prev != null && prev !== 0
              ? ((arr[i]! - prev) / Math.abs(prev)) * 100
              : null,
          subYear: false,
        };
      }
    }
    return null;
  }, [payload, variantCode]);

  if (!latest || !variant) return null;

  const unit = unitInline(variant.unit, fa ? "fa" : "en");
  const measureLabel =
    payload.variants.length === 1 && measureFallback
      ? measureFallback
      : friendlyVariantLabel(variant.label, locale);

  return (
    <section className="corner-frame rise-in border border-border/60 bg-card/40 p-4">
      <h2 className="data-label flex items-center gap-2">
        <span className="pulse-dot" style={{ color: "#2140E3" }} aria-hidden />
        {t.latestReading}
      </h2>
      {/* Number + unit inline, same size: the unit IS part of the reading. */}
      <div
        className="mt-3 font-data text-3xl font-light leading-tight tracking-tight"
        dir={fa ? "rtl" : "ltr"}
      >
        <CountUp
          value={latest.value}
          format="reading"
          locale={fa ? "fa" : "en"}
        />
        {unit ? (unit.tight && !fa ? unit.text : ` ${unit.text}`) : null}
      </div>
      {/* The measure is what the number means — second in hierarchy. */}
      <p className="mt-2 text-sm leading-snug text-foreground/90">
        {measureLabel}
      </p>
      <p className="font-data mt-1 text-xs text-muted-foreground" dir="ltr">
        {fa ? toPersianDigits(latest.when) : latest.when}
      </p>
      <div className="mt-2 flex items-center gap-2 opacity-80">
        <span className="data-label">{t.iranSeries}</span>
        {latest.delta != null ? (
          <>
            <span
              className="font-data text-[11px]"
              style={{
                color:
                  latest.delta >= 0 ? "oklch(0.596 0.145 163.225)" : "#E32128",
              }}
              dir="ltr"
            >
              {latest.delta >= 0 ? "+" : ""}
              {latest.delta.toFixed(1)}%
            </span>
            <span className="data-label">
              {latest.subYear ? t.vsPrev : t.vsPrevYear}
            </span>
          </>
        ) : null}
      </div>
    </section>
  );
}
