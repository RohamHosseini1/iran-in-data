"use client";

import * as React from "react";
import { useTheme } from "next-themes";

import { InteractiveChart } from "./interactive-chart";
import { useChartVariant } from "./chart-state";
import {
  buildLineOption,
  dataExtent,
  subYearExtent,
  seriesColor,
} from "@/lib/charts/line-option";
import {
  readChromeFromCss,
  LIGHT_CHROME,
  DARK_CHROME,
} from "@/lib/charts/palette";
import {
  friendlyVariantLabel,
  pickDefaultVariant,
} from "@/lib/charts/variant-labels";
import { formatFull, labelUnitText } from "@/lib/charts/unit-format";
import {
  formatYearFor,
  calendarLabels,
  toPersianDigits,
  type CalendarSystem,
} from "@/lib/calendar";
import { countryNameFa } from "@/lib/i18n/countries-fa";
import { usePref } from "@/lib/use-pref";
import type { ChartPayload, SubYearSeries } from "@/lib/data/payload";
import type { ChartEventDetail } from "@/lib/data/types";
import type { Locale } from "@/lib/i18n/config";

import { Switch } from "@/components/ui/switch";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";

interface ChartExplorerProps {
  payload: ChartPayload;
  locale: Locale;
  ssrSvg?: string;
  events?: ChartEventDetail[];
}

const STRINGS = {
  en: {
    chart: "Chart",
    table: "Table",
    line: "Line",
    bar: "Bars",
    style: "Style",
    comparators: "Comparators",
    all: "All",
    calendar: "Calendar",
    measure: "Measure",
    year: "Year",
    period: "Period",
    unit: "Unit",
    visualizer: "Visualizer_Mode",
    projection: "Projection",
    eventLog: "Event_Log",
    association: "Association",
    lag: "Lag",
    caveat: "Caveat",
    why: "Why this link",
    source: "Source",
  },
  fa: {
    chart: "نمودار",
    table: "جدول",
    line: "خطی",
    bar: "میله‌ای",
    style: "سبک",
    comparators: "کشورهای مقایسه",
    all: "همه",
    calendar: "تقویم",
    measure: "سنجه",
    year: "سال",
    period: "دوره",
    unit: "واحد",
    visualizer: "حالت نمایش",
    projection: "پیش‌بینی",
    eventLog: "رویدادها",
    association: "قوت ارتباط",
    lag: "تأخیر اثر",
    caveat: "ملاحظه",
    why: "چرایی این پیوند",
    source: "منبع",
  },
};

const FA_DATA_FONT = "var(--font-yekan), ui-sans-serif, sans-serif";
const EVENT_COLOR = "#CA8A04";
// Computed at load so projection boundaries roll forward on their own each
// year; nothing here needs a manual New Year's update.
const NOW_YEAR = new Date().getFullYear();

const pad2 = (n: number) => String(n).padStart(2, "0");

export function ChartExplorer({
  payload,
  locale,
  ssrSvg,
  events = [],
}: ChartExplorerProps) {
  const t = STRINGS[locale];
  const fa = locale === "fa";
  const { resolvedTheme } = useTheme();

  const [variantCode, setVariantCode] = useChartVariant(
    pickDefaultVariant(payload.variants)
  );
  const [calendar, setCalendar] = usePref<CalendarSystem>(
    "calendar",
    "gregorian"
  );
  const [comparatorsDefault, setComparatorsDefault] = usePref(
    "comparators",
    false
  );
  const [view, setView] = React.useState<"chart" | "table">("chart");
  const [chartType, setChartType] = usePref<"line" | "bar">(
    "chartType",
    "line"
  );
  const [mounted, setMounted] = React.useState(false);

  const hasIran = payload.countries.some((c) => c.iso === "IRN");

  // Only countries with actual data for the selected measure exist as chips.
  const comparators = React.useMemo(() => {
    const values = payload.values[variantCode] ?? {};
    return payload.countries.filter(
      (c) => c.iso !== "IRN" && values[c.iso]?.some((v) => v != null)
    );
  }, [payload, variantCode]);

  const [selected, setSelected] = React.useState<Set<string>>(new Set());
  const [touched, setTouched] = React.useState(false);

  React.useEffect(() => setMounted(true), []);
  React.useEffect(() => {
    if (!touched) {
      setSelected(
        comparatorsDefault ? new Set(comparators.map((c) => c.iso)) : new Set()
      );
    }
  }, [comparatorsDefault, comparators, touched]);

  // The switch reflects reality: on as soon as any comparator is plotted.
  const anyOn = selected.size > 0;

  const toggleCountry = (iso: string) => {
    setTouched(true);
    setSelected((prev) => {
      const next = new Set(prev);
      if (next.has(iso)) next.delete(iso);
      else next.add(iso);
      return next;
    });
  };

  const toggleAll = (on: boolean) => {
    setTouched(true);
    setComparatorsDefault(on);
    setSelected(on ? new Set(comparators.map((c) => c.iso)) : new Set());
  };

  const activeCountries = React.useMemo(() => {
    const base = hasIran ? ["IRN"] : [];
    const chosen = comparators
      .filter((c) => selected.has(c.iso))
      .map((c) => c.iso);
    return hasIran ? [...base, ...chosen] : payload.countries.map((c) => c.iso);
  }, [hasIran, comparators, selected, payload.countries]);

  const formatYear = React.useMemo(
    () => formatYearFor(calendar, { persianDigits: fa }),
    [calendar, fa]
  );

  // Sub-year (time-axis) mode: real daily/monthly detail for this measure.
  // Tick labels stay Gregorian below year level (converting month/day into
  // other calendar systems would claim dates we haven't computed).
  const subValues =
    chartType === "line" ? payload.subYear?.values[variantCode] : undefined;
  const timeMode = !!subValues && Object.keys(subValues).length > 0;

  const formatTime = React.useMemo(() => {
    return (ms: number, detail?: boolean) => {
      // ECharts places time-axis ticks in local time; read local parts so a
      // year boundary renders as "2013", not "2012/12/31".
      const d = new Date(ms);
      const y = d.getFullYear();
      const mo = d.getMonth() + 1;
      const day = d.getDate();
      let s: string;
      if (detail) s = `${y}/${pad2(mo)}/${pad2(day)}`;
      else if (mo === 1 && day === 1) s = String(y);
      else if (day === 1 || day === 15) s = `${y}/${pad2(mo)}`;
      else s = `${y}/${pad2(mo)}/${pad2(day)}`;
      return fa ? toPersianDigits(s) : s;
    };
  }, [fa]);

  const displayNames = React.useMemo(() => {
    if (!fa) return undefined;
    return Object.fromEntries(
      payload.countries.map((c) => [c.iso, countryNameFa(c.iso, c.name)])
    );
  }, [fa, payload.countries]);

  const variant = payload.variants.find((v) => v.code === variantCode);
  const variantDisplay = variant
    ? friendlyVariantLabel(variant.label, locale)
    : "";

  const option = React.useMemo(() => {
    const chrome = mounted
      ? readChromeFromCss()
      : resolvedTheme === "dark"
        ? DARK_CHROME
        : LIGHT_CHROME;
    return buildLineOption({
      payload,
      variantCode,
      countries: activeCountries,
      chrome,
      formatYear,
      dataFont: fa ? FA_DATA_FONT : undefined,
      chartType,
      unit: variant?.unit || labelUnitText(variant?.label) || undefined,
      displayNames,
      nowYear: NOW_YEAR,
      projectionLabel: t.projection,
      events: events.map((e) => ({ year: e.year, title: e.title })),
      subYear: payload.subYear,
      formatTime,
    });
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [payload, variantCode, activeCountries, formatYear, resolvedTheme, mounted, fa, chartType, variant, displayNames, events, formatTime]);

  const zoomExtent = React.useMemo(
    () =>
      timeMode
        ? subYearExtent(payload.subYear!, variantCode, activeCountries)
        : dataExtent(payload, variantCode, activeCountries),
    [timeMode, payload, variantCode, activeCountries]
  );

  // Event hover card (Overwatch-style: marker hover → details beside chart).
  const [hoverEvent, setHoverEvent] = React.useState<number | null>(null);
  const hoverTimer = React.useRef<ReturnType<typeof setTimeout> | null>(null);
  const handleEventHover = React.useCallback((idx: number | null) => {
    if (hoverTimer.current) clearTimeout(hoverTimer.current);
    if (idx == null) {
      hoverTimer.current = setTimeout(() => setHoverEvent(null), 150);
    } else {
      setHoverEvent(idx);
    }
  }, []);
  const hovered = hoverEvent != null ? events[hoverEvent] : null;

  const chipName = (iso: string, fallback: string) =>
    fa ? countryNameFa(iso, fallback) : fallback;

  return (
    <section className="corner-frame bg-dotgrid panel-boot relative border border-border/60 bg-card/40">
      {/* Panel header: identity left; view switcher with style beneath it */}
      <div className="flex items-start justify-between gap-4 border-b border-border/60 px-4 py-2.5">
        <span className="data-label pt-1.5">{t.visualizer}</span>
        <div className="flex flex-col items-end gap-2">
          <div
            role="tablist"
            className="flex overflow-hidden rounded-none border border-border/60"
          >
            {(["chart", "table"] as const).map((mode) => (
              <button
                key={mode}
                role="tab"
                aria-selected={view === mode}
                onClick={() => setView(mode)}
                className={`data-label px-3 py-1.5 transition-colors ${
                  view === mode
                    ? "bg-primary text-primary-foreground"
                    : "hover:bg-muted"
                }`}
              >
                {t[mode]}
              </button>
            ))}
          </div>
          {view === "chart" ? (
            <div
              role="tablist"
              aria-label={t.style}
              className="flex overflow-hidden rounded-none border border-border/50"
            >
              {(["line", "bar"] as const).map((type) => (
                <button
                  key={type}
                  role="tab"
                  aria-selected={chartType === type}
                  onClick={() => setChartType(type)}
                  className={`data-label px-2.5 py-1 text-[9px] transition-colors ${
                    chartType === type
                      ? "bg-secondary text-secondary-foreground"
                      : "text-muted-foreground hover:bg-muted"
                  }`}
                >
                  {t[type]}
                </button>
              ))}
            </div>
          ) : null}
        </div>
      </div>

      {/* Settings: measure and calendar only — style lives with the view. */}
      <div className="flex flex-wrap items-end gap-x-10 gap-y-4 border-b border-border/60 px-4 py-3.5">
        {payload.variants.length > 1 && (
          <div className="flex flex-col gap-1.5">
            <span className="data-label">{t.measure}</span>
            <Select
              value={variantCode}
              onValueChange={(v) => v && setVariantCode(v as string)}
            >
              <SelectTrigger size="sm" className="max-w-72 text-xs">
                <SelectValue>{variantDisplay}</SelectValue>
              </SelectTrigger>
              <SelectContent>
                {payload.variants.map((v) => (
                  <SelectItem key={v.code} value={v.code} className="text-xs">
                    {friendlyVariantLabel(v.label, locale)}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>
        )}
        <div className="flex flex-col gap-1.5">
          <span className="data-label">{t.calendar}</span>
          <Select
            value={calendar}
            onValueChange={(v) => v && setCalendar(v as CalendarSystem)}
          >
            <SelectTrigger size="sm" className="text-xs">
              <SelectValue>{calendarLabels[calendar][locale]}</SelectValue>
            </SelectTrigger>
            <SelectContent>
              {(Object.keys(calendarLabels) as CalendarSystem[]).map((c) => (
                <SelectItem key={c} value={c} className="text-xs">
                  {calendarLabels[c][locale]}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
        </div>
      </div>

      {/* Comparators: master switch + per-country chips */}
      {hasIran && comparators.length > 0 ? (
        <div className="flex flex-wrap items-center gap-x-3 gap-y-2 border-b border-border/60 px-4 py-2.5">
          <label className="flex cursor-pointer items-center gap-2">
            <span className="data-label">{t.comparators}</span>
            <Switch checked={anyOn} onCheckedChange={toggleAll} />
          </label>
          <span className="mx-1 h-4 w-px bg-border/70" aria-hidden />
          <CountryChip
            name={chipName("IRN", payload.countries.find((c) => c.iso === "IRN")?.name ?? "Iran")}
            color={seriesColor("IRN", payload)}
            active
            pinned
          />
          {comparators.map((c) => (
            <CountryChip
              key={c.iso}
              name={chipName(c.iso, c.name)}
              color={seriesColor(c.iso, payload)}
              active={selected.has(c.iso)}
              onClick={() => toggleCountry(c.iso)}
            />
          ))}
        </div>
      ) : null}

      {/* Body */}
      {view === "chart" ? (
        <div className="relative px-2 py-3">
          <InteractiveChart
            option={option}
            ssrSvg={ssrSvg}
            height={430}
            zoomExtent={zoomExtent}
            timeAxis={timeMode}
            onEventHover={events.length ? handleEventHover : undefined}
          />
          {hovered ? (
            <div
              className="rise-in pointer-events-none absolute top-4 z-10 w-72 max-w-[70%] border bg-card/95 p-3 shadow-lg backdrop-blur-sm"
              style={{
                insetInlineEnd: 16,
                borderColor: "color-mix(in oklch, #CA8A04 45%, transparent)",
              }}
              dir={fa ? "rtl" : "ltr"}
              role="status"
            >
              <div className="flex items-baseline gap-2">
                <span
                  className="font-data text-[10px]"
                  style={{ color: EVENT_COLOR }}
                >
                  {String((hoverEvent ?? 0) + 1).padStart(2, "0")}
                </span>
                <span className="font-data text-[11px] text-muted-foreground" dir="ltr">
                  {fa ? toPersianDigits(hovered.year) : hovered.year}
                </span>
                <ConfidenceBars score={hovered.confidence} />
              </div>
              <p className="mt-1.5 text-sm font-medium leading-snug">
                {hovered.title}
              </p>
              {hovered.description || hovered.justification ? (
                <p className="mt-1.5 line-clamp-4 text-xs leading-relaxed text-muted-foreground">
                  {hovered.description || hovered.justification}
                </p>
              ) : null}
              {hovered.caveats ? (
                <p className="mt-1.5 line-clamp-2 text-xs leading-relaxed">
                  <span className="data-label" style={{ color: EVENT_COLOR }}>
                    {t.caveat}:{" "}
                  </span>
                  <span className="text-muted-foreground">{hovered.caveats}</span>
                </p>
              ) : null}
            </div>
          ) : null}
        </div>
      ) : (
        <DataTable
          payload={payload}
          variantCode={variantCode}
          countries={activeCountries}
          formatYear={formatYear}
          yearLabel={payload.subYear ? t.period : t.year}
          unitLabel={t.unit}
          unit={variant?.unit || labelUnitText(variant?.label)}
          fa={fa}
          subYear={payload.subYear}
          displayNames={displayNames}
        />
      )}

      {/* Event log: numbered to match the chart markers */}
      {events.length ? (
        <div className="border-t border-border/60 px-4 py-4">
          <h3 className="data-label">{t.eventLog}</h3>
          <ol className="mt-3 space-y-2">
            {events.map((e, i) => (
              <li key={`${e.date}-${i}`}>
                <details className="group border border-border/50 bg-background/40">
                  <summary className="flex cursor-pointer flex-wrap items-baseline gap-x-3 gap-y-1 px-3 py-2 transition-colors hover:bg-muted/40">
                    <span className="font-data text-[10px] text-[#CA8A04]">
                      {String(i + 1).padStart(2, "0")}
                    </span>
                    <span className="font-data text-[11px] text-muted-foreground" dir="ltr">
                      {fa ? toPersianDigits(e.year) : e.year}
                    </span>
                    <span className="min-w-0 flex-1 text-sm">{e.title}</span>
                    <ConfidenceBadge
                      score={e.confidence}
                      label={t.association}
                    />
                  </summary>
                  <div className="space-y-2 border-t border-border/40 px-3 py-3 text-xs leading-relaxed text-muted-foreground">
                    {e.description ? <p>{e.description}</p> : null}
                    <p>
                      <span className="data-label">{t.why}: </span>
                      {e.justification}
                    </p>
                    {e.caveats ? (
                      <p>
                        <span className="data-label text-[#CA8A04]">
                          {t.caveat}:{" "}
                        </span>
                        {e.caveats}
                      </p>
                    ) : null}
                    <div className="flex flex-wrap gap-x-6 gap-y-1">
                      {e.lag ? (
                        <span className="data-label">
                          {t.lag}: {e.lag}
                        </span>
                      ) : null}
                      {e.sourceUrl ? (
                        <a
                          href={e.sourceUrl.split(" ; ")[0]}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="data-label underline decoration-border underline-offset-2 hover:text-foreground"
                        >
                          {t.source}: {e.sourceName || "link"}
                        </a>
                      ) : null}
                    </div>
                  </div>
                </details>
              </li>
            ))}
          </ol>
        </div>
      ) : null}
    </section>
  );
}

function ConfidenceBars({ score }: { score: number }) {
  return (
    <span className="flex gap-0.5" dir="ltr" aria-label={`${score}/5`}>
      {[1, 2, 3, 4, 5].map((n) => (
        <span
          key={n}
          className="inline-block h-2.5 w-1"
          style={{
            backgroundColor:
              n <= score
                ? EVENT_COLOR
                : "color-mix(in oklch, currentColor 15%, transparent)",
          }}
        />
      ))}
    </span>
  );
}

function ConfidenceBadge({ score, label }: { score: number; label: string }) {
  return (
    <span
      className="flex items-center gap-1.5"
      title={`${label}: ${score}/5`}
      aria-label={`${label}: ${score}/5`}
    >
      <span className="data-label">{label}</span>
      <ConfidenceBars score={score} />
    </span>
  );
}

function CountryChip({
  name,
  color,
  active,
  pinned,
  onClick,
}: {
  name: string;
  color: string;
  active: boolean;
  pinned?: boolean;
  onClick?: () => void;
}) {
  return (
    <button
      type="button"
      onClick={onClick}
      disabled={pinned}
      aria-pressed={active}
      className={`flex items-center gap-1.5 rounded-full border px-2.5 py-1 text-[11px] transition-all ${
        active
          ? "border-foreground/25 bg-muted/60 text-foreground"
          : "border-border/60 text-muted-foreground opacity-55 hover:opacity-90"
      } ${pinned ? "cursor-default" : "cursor-pointer"}`}
    >
      <span
        className="inline-block size-2 rounded-full transition-opacity"
        style={{ backgroundColor: color, opacity: active ? 1 : 0.4 }}
      />
      {name}
    </button>
  );
}

function DataTable({
  payload,
  variantCode,
  countries,
  formatYear,
  yearLabel,
  unitLabel,
  unit,
  fa,
  subYear,
  displayNames,
}: {
  payload: ChartPayload;
  variantCode: string;
  countries: string[];
  formatYear: (y: number) => string;
  yearLabel: string;
  unitLabel: string;
  unit: string;
  fa: boolean;
  subYear?: SubYearSeries;
  displayNames?: Record<string, string>;
}) {
  const nameOf = new Map(payload.countries.map((c) => [c.iso, c.name]));

  // Sub-year series show every observation (daily/monthly), newest first.
  const subVals = subYear?.values[variantCode];
  const useSub = !!subVals && Object.keys(subVals).length > 0;

  const values = useSub ? subVals! : (payload.values[variantCode] ?? {});
  const cols = countries.filter((iso) => values[iso]);
  const rows = useSub
    ? subYear!.labels
        .map((label, i) => ({ key: label, i }))
        .filter(({ i }) => cols.some((iso) => values[iso][i] != null))
        .reverse()
    : payload.years
        .map((y, i) => ({ key: formatYear(y), i }))
        .filter(({ i }) => cols.some((iso) => values[iso][i] != null))
        .reverse();

  return (
    <div>
      {/* What the numbers ARE — nobody should wonder "42,000 what?" */}
      {unit ? (
        <p className="data-label border-b border-border/40 px-4 py-2">
          {unitLabel}: <span className="normal-case">{unit}</span>
        </p>
      ) : null}
      <div className="max-h-[480px] overflow-auto" dir="ltr">
        <table className="w-full text-xs">
          <thead className="sticky top-0 bg-card">
            <tr className="border-b border-border/60">
              <th className="data-label px-4 py-2 text-start">{yearLabel}</th>
              {cols.map((iso) => (
                <th key={iso} className="data-label px-4 py-2 text-end">
                  {displayNames?.[iso] ?? nameOf.get(iso) ?? iso}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {rows.map(({ key, i }) => (
              <tr
                key={key}
                className="border-b border-border/40 transition-colors hover:bg-muted/50"
              >
                <td className="font-data px-4 py-1.5">
                  {fa && useSub ? toPersianDigits(key) : key}
                </td>
                {cols.map((iso) => (
                  <td
                    key={iso}
                    className="font-data px-4 py-1.5 text-end tabular-nums"
                  >
                    {values[iso][i] != null ? formatFull(values[iso][i]!) : "–"}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
