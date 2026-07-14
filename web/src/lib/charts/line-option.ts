import type { EChartsOption, SeriesOption } from "echarts";

import {
  COMPARATOR_COLORS,
  COMPARATOR_OPACITY,
  IRAN_COLOR,
  type ChartChrome,
} from "./palette";
import type { ChartPayload, SubYearSeries } from "@/lib/data/payload";

export interface ChartEventMarker {
  year: number;
  title: string;
}

export interface LineOptionInput {
  payload: ChartPayload;
  variantCode: string;
  /** ISO3 codes to plot; Iran is always drawn on top. */
  countries: string[];
  chrome: ChartChrome;
  zoomSlider?: boolean;
  /** Year → display label (calendar-system transform). */
  formatYear?: (year: number) => string;
  animate?: boolean;
  /**
   * Font stack for axis labels, tooltips and slider text. Latin mode uses the
   * mono stack; Persian mode passes Yekan Bakh (no Persian mono exists).
   */
  dataFont?: string;
  /** Mark type: smoothed glow lines (default) or lit gradient bars. */
  chartType?: "line" | "bar";
  /** Measurement unit, shown as the y-axis title. */
  unit?: string;
  /** Display names per ISO3 (e.g. Persian country names). */
  displayNames?: Record<string, string>;
  /** Years after this render dashed/faded as projections. */
  nowYear?: number;
  /** Label for the projection region ("Projection" / «پیش‌بینی»). */
  projectionLabel?: string;
  /** Confidence-scored policy/event markers. */
  events?: ChartEventMarker[];
  /** Sub-year observations: switches the x-axis to a real time axis. */
  subYear?: SubYearSeries;
  /** Formats an epoch-ms tick/tooltip label in time mode. */
  formatTime?: (ms: number, detail?: boolean) => string;
}

const DEFAULT_DATA_FONT =
  "var(--font-reddit-mono), ui-monospace, SFMono-Regular, Menlo, monospace";

const EVENT_COLOR = "#CA8A04";

/** Year window where the given series actually have data. */
export function dataExtent(
  payload: ChartPayload,
  variantCode: string,
  countries: string[]
): [number, number] | undefined {
  const variantValues = payload.values[variantCode] ?? {};
  let min = Infinity;
  let max = -Infinity;
  for (const iso of countries) {
    const arr = variantValues[iso];
    if (!arr) continue;
    for (let i = 0; i < payload.years.length; i++) {
      if (arr[i] != null) {
        if (payload.years[i] < min) min = payload.years[i];
        if (payload.years[i] > max) max = payload.years[i];
      }
    }
  }
  return Number.isFinite(min) && Number.isFinite(max)
    ? [min, max]
    : undefined;
}

/** Epoch-ms window where the given series actually have sub-year data. */
export function subYearExtent(
  sub: SubYearSeries,
  variantCode: string,
  countries: string[]
): [number, number] | undefined {
  const variantValues = sub.values[variantCode] ?? {};
  let min = Infinity;
  let max = -Infinity;
  for (const iso of countries) {
    const arr = variantValues[iso];
    if (!arr) continue;
    for (let i = 0; i < sub.times.length; i++) {
      if (arr[i] != null) {
        if (sub.times[i] < min) min = sub.times[i];
        if (sub.times[i] > max) max = sub.times[i];
      }
    }
  }
  return Number.isFinite(min) && Number.isFinite(max) ? [min, max] : undefined;
}

/** Stable color per comparator so toggling others never recolors a series. */
export function seriesColor(iso: string, payload: ChartPayload): string {
  if (iso === "IRN") return IRAN_COLOR;
  const comparators = payload.countries.filter((c) => c.iso !== "IRN");
  const idx = comparators.findIndex((c) => c.iso === iso);
  return COMPARATOR_COLORS[Math.max(idx, 0) % COMPARATOR_COLORS.length];
}

export function buildLineOption(input: LineOptionInput): EChartsOption {
  const {
    payload,
    variantCode,
    countries,
    chrome,
    zoomSlider = true,
    formatYear,
    animate = true,
    dataFont = DEFAULT_DATA_FONT,
    chartType = "line",
    unit,
    displayNames,
    nowYear,
    projectionLabel = "Projection",
    events = [],
    subYear,
    formatTime,
  } = input;

  const variantValues = payload.values[variantCode] ?? {};
  const nameOf = new Map(payload.countries.map((c) => [c.iso, c.name]));
  const displayName = (iso: string) =>
    displayNames?.[iso] ?? nameOf.get(iso) ?? iso;

  // Real time axis when sub-year observations exist for this measure:
  // daily/monthly detail instead of a lossy annual collapse.
  const subValues =
    subYear && chartType === "line" ? subYear.values[variantCode] : undefined;
  const timeMode = !!subValues && Object.keys(subValues).length > 0;

  const ordered = [
    ...countries.filter((c) => c !== "IRN"),
    ...(countries.includes("IRN") ? ["IRN"] : []),
  ];
  const active = ordered.filter((iso) =>
    timeMode ? subValues![iso] : variantValues[iso]
  );

  const extent = dataExtent(payload, variantCode, active);
  const hasProjection =
    !timeMode && nowYear != null && extent != null && extent[1] > nowYear;

  const soloIran = active.length === 1 && active[0] === "IRN";

  // Anchor the y-axis at zero for non-negative data so a floor of "7" never
  // reads as zero, and zooming never dips the axis below zero.
  let seriesMin = Infinity;
  for (const iso of active) {
    const arr = timeMode ? subValues![iso] : variantValues[iso];
    if (!arr) continue;
    for (const v of arr) if (v != null && v < seriesMin) seriesMin = v;
  }
  const yMin = Number.isFinite(seriesMin) && seriesMin >= 0 ? 0 : undefined;

  const series: SeriesOption[] = [];

  for (const iso of active) {
    const isIran = iso === "IRN";
    const color = seriesColor(iso, payload);
    const opacity = isIran ? 1 : COMPARATOR_OPACITY;
    const name = displayName(iso);

    if (timeMode) {
      const sub = subValues![iso];
      const data: [number, number | null][] = [];
      for (let i = 0; i < subYear!.times.length; i++) {
        data.push([subYear!.times[i], sub[i]]);
      }
      series.push({
        name,
        type: "line" as const,
        data,
        connectNulls: true,
        showSymbol: false,
        sampling: "lttb" as const,
        z: isIran ? 10 : 2,
        itemStyle: { color, opacity },
        lineStyle: {
          width: isIran ? 1.75 : 1.25,
          color,
          opacity,
          ...(isIran
            ? { shadowColor: fade(color, 0.4), shadowBlur: 12, shadowOffsetY: 7 }
            : {}),
        },
        emphasis: {
          focus: "series" as const,
          lineStyle: { width: isIran ? 2.5 : 2, opacity: 1 },
        },
        blur: { lineStyle: { opacity: 0.12 } },
        ...(isIran && soloIran
          ? {
              areaStyle: {
                color: {
                  type: "linear" as const,
                  x: 0,
                  y: 0,
                  x2: 0,
                  y2: 1,
                  colorStops: [
                    { offset: 0, color: fade(color, 0.22) },
                    { offset: 1, color: fade(color, 0) },
                  ],
                },
              },
            }
          : {}),
      });
      continue;
    }

    const arr = variantValues[iso];

    const actualData: [number, number | null][] = [];
    const projectionData: [number, number | null][] = [];
    for (let i = 0; i < payload.years.length; i++) {
      const y = payload.years[i];
      const v = arr[i];
      if (!hasProjection || y <= nowYear!) {
        actualData.push([y, v]);
        // Anchor the projection segment at the last actual point.
        if (hasProjection && y === nowYear) projectionData.push([y, v]);
      } else {
        projectionData.push([y, v]);
      }
    }

    if (chartType === "bar") {
      series.push({
        name,
        type: "bar" as const,
        data: payload.years.map((y, i) => {
          const future = hasProjection && y > nowYear!;
          return {
            value: [y, arr[i]] as [number, number | null],
            itemStyle: future ? { opacity: opacity * 0.45 } : undefined,
          };
        }),
        z: isIran ? 10 : 2,
        barMaxWidth: 14,
        itemStyle: {
          opacity,
          color: {
            type: "linear" as const,
            x: 0,
            y: 0,
            x2: 0,
            y2: 1,
            colorStops: [
              { offset: 0, color: lighten(color) },
              { offset: 0.12, color },
              { offset: 1, color: fade(color, 0.55) },
            ],
          },
          shadowColor: fade(color, isIran ? 0.5 : 0.2),
          shadowBlur: isIran ? 10 : 4,
          shadowOffsetY: 4,
        },
        emphasis: { focus: "series" as const },
        blur: { itemStyle: { opacity: 0.2 } },
      });
      continue;
    }

    const base = {
      name,
      type: "line" as const,
      connectNulls: true,
      smooth: 0.35,
      // Never let smoothing overshoot the data range (no phantom negatives).
      smoothMonotone: "x" as const,
      showSymbol: false,
      symbol: "circle",
      symbolSize: isIran ? 7 : 5,
      z: isIran ? 10 : 2,
      itemStyle: { color, opacity },
      emphasis: {
        focus: "series" as const,
        lineStyle: { width: isIran ? 3.5 : 2.5, opacity: 1 },
      },
      blur: { lineStyle: { opacity: 0.12 } },
    };

    series.push({
      ...base,
      data: actualData,
      lineStyle: {
        width: isIran ? 2.5 : 1.5,
        color,
        opacity,
        ...(isIran
          ? {
              shadowColor: fade(color, 0.45),
              shadowBlur: 14,
              shadowOffsetY: 8,
            }
          : {}),
      },
      ...(isIran && soloIran
        ? {
            areaStyle: {
              color: {
                type: "linear" as const,
                x: 0,
                y: 0,
                x2: 0,
                y2: 1,
                colorStops: [
                  { offset: 0, color: fade(color, 0.22) },
                  { offset: 1, color: fade(color, 0) },
                ],
              },
            },
          }
        : {}),
    });

    if (hasProjection && projectionData.length > 1) {
      series.push({
        ...base,
        data: projectionData,
        lineStyle: {
          width: isIran ? 2 : 1.25,
          color,
          opacity: opacity * 0.75,
          type: "dashed" as const,
        },
      });
    }
  }

  // Invisible helper series carrying event markers + the projection band.
  if (events.length || hasProjection) {
    series.push({
      name: "__annotations__",
      type: "line" as const,
      data: [],
      silent: false,
      tooltip: { show: false },
      markLine: events.length
        ? {
            silent: false,
            symbol: ["none", "circle"],
            symbolSize: 6,
            animation: false,
            lineStyle: {
              color: EVENT_COLOR,
              width: 1,
              type: [3, 5] as unknown as "dashed",
              opacity: 0.75,
            },
            label: {
              show: true,
              position: "start" as const,
              formatter: (p: { dataIndex?: number }) =>
                String((p.dataIndex ?? 0) + 1),
              color: EVENT_COLOR,
              fontFamily: dataFont,
              fontSize: 9,
              distance: 4,
            },
            emphasis: {
              lineStyle: { opacity: 1, width: 1.5 },
              label: { show: true },
            },
            // Details appear in the hover card beside the chart, not a tooltip.
            tooltip: { show: false },
            data: events.map((e) => ({
              xAxis: timeMode ? Date.UTC(e.year, 0, 1) : e.year,
              name: e.title,
            })),
          }
        : undefined,
      markArea: hasProjection
        ? {
            silent: true,
            itemStyle: {
              color: fade("#888888", 0.06),
            },
            label: {
              show: true,
              position: "insideTop" as const,
              color: chrome.mutedForeground,
              fontFamily: dataFont,
              fontSize: 9,
            },
            data: [
              [
                { xAxis: nowYear!, name: projectionLabel.toUpperCase() },
                { xAxis: extent![1] },
              ],
            ],
          }
        : undefined,
    });
  }

  return {
    animation: animate,
    animationDuration: 900,
    animationEasing: "cubicOut",
    grid: {
      left: 8,
      right: 20,
      top: unit ? 42 : 24,
      bottom: zoomSlider ? 64 : 32,
      containLabel: true,
    },
    tooltip: {
      trigger: "axis",
      backgroundColor: chrome.tooltipBackground,
      borderColor: chrome.border,
      borderWidth: 1,
      padding: [8, 12],
      textStyle: { color: chrome.foreground, fontSize: 12 },
      axisPointer: {
        type: "line",
        lineStyle: { color: chrome.mutedForeground, width: 1, type: "dashed" },
      },
      order: "valueDesc",
      formatter: (params) => {
        const items = Array.isArray(params) ? params : [params];
        if (!items.length) return "";
        const first = items[0] as { axisValue?: number | string };
        const axisValue = Number(first.axisValue);
        const headerText = timeMode
          ? (formatTime?.(axisValue, true) ?? new Date(axisValue).toISOString().slice(0, 10))
          : formatYear
            ? formatYear(Math.round(axisValue))
            : Math.round(axisValue);
        const header = `<div style="font-family:${dataFont};font-size:10px;letter-spacing:0.08em;opacity:0.65;margin-bottom:4px">${headerText}</div>`;
        const seen = new Set<string>();
        const rows = items
          .map((p) => {
            const item = p as {
              marker?: string;
              seriesName?: string;
              value?: [number, number | null];
            };
            const v = item.value?.[1];
            if (v == null) return "";
            if (item.seriesName === "__annotations__") return "";
            if (seen.has(item.seriesName ?? "")) return "";
            seen.add(item.seriesName ?? "");
            return `<div style="display:flex;align-items:center;gap:8px;justify-content:space-between"><span>${item.marker ?? ""}${
              item.seriesName ?? ""
            }</span><span style="font-family:${dataFont};font-weight:600">${formatCompact(
              v
            )}</span></div>`;
          })
          .join("");
        return header + rows;
      },
    },
    xAxis: timeMode
      ? {
          type: "time" as const,
          axisLine: { lineStyle: { color: chrome.border } },
          axisTick: { show: false },
          splitLine: { show: false },
          axisLabel: {
            color: chrome.mutedForeground,
            fontFamily: dataFont,
            fontSize: 10,
            hideOverlap: true,
            formatter: (value: number) => formatTime?.(value) ?? "",
          },
        }
      : {
          type: "value" as const,
          min: "dataMin" as const,
          max: "dataMax" as const,
          axisLine: { lineStyle: { color: chrome.border } },
          axisTick: { show: false },
          splitLine: { show: false },
          axisLabel: {
            color: chrome.mutedForeground,
            fontFamily: dataFont,
            fontSize: 10,
            formatter: (value: number) => {
              if (!Number.isInteger(value)) return "";
              return formatYear ? formatYear(value) : String(value);
            },
          },
        },
    yAxis: {
      type: "value",
      // Anchor at zero: a floor of "7" must not read as zero, and zooming
      // must never swing the axis below zero on non-negative data.
      scale: false,
      min: yMin,
      name: unit || undefined,
      nameTextStyle: {
        color: chrome.mutedForeground,
        fontFamily: dataFont,
        fontSize: 10,
        align: "left" as const,
        padding: [0, 0, 4, 0],
      },
      axisLine: { show: false },
      axisTick: { show: false },
      splitLine: { lineStyle: { color: chrome.border, type: [2, 4] } },
      axisLabel: {
        color: chrome.mutedForeground,
        fontFamily: dataFont,
        fontSize: 10,
        formatter: (value: number) => formatCompact(value),
      },
    },
    dataZoom: [
      {
        type: "inside",
        throttle: 60,
        minValueSpan: timeMode ? 7 * 864e5 : 3,
        // Wheel zoom is handled by InteractiveChart's slow custom handler;
        // the built-in per-tick step is far too aggressive.
        zoomOnMouseWheel: false,
        moveOnMouseWheel: false,
        moveOnMouseMove: true,
      },
      ...(zoomSlider
        ? [
            {
              type: "slider" as const,
              height: 26,
              bottom: 10,
              left: 50,
              right: 24,
              borderColor: "transparent",
              backgroundColor: "rgba(128,128,128,0.07)",
              fillerColor: "rgba(128,128,128,0.14)",
              minValueSpan: timeMode ? 7 * 864e5 : 3,
              dataBackground: {
                lineStyle: { color: chrome.mutedForeground, opacity: 0.4 },
                areaStyle: { color: chrome.mutedForeground, opacity: 0.08 },
              },
              selectedDataBackground: {
                lineStyle: { color: IRAN_COLOR, opacity: 0.6 },
                areaStyle: { color: IRAN_COLOR, opacity: 0.08 },
              },
              handleStyle: {
                color: chrome.background,
                borderColor: chrome.mutedForeground,
              },
              moveHandleStyle: { color: chrome.mutedForeground },
              textStyle: {
                color: chrome.mutedForeground,
                fontFamily: dataFont,
                fontSize: 9,
              },
              labelFormatter: (value: number) =>
                timeMode
                  ? (formatTime?.(value) ?? "")
                  : formatYear
                    ? formatYear(Math.round(value))
                    : String(Math.round(value)),
            },
          ]
        : []),
    ],
    series,
  };
}

/** rgba fade for hex colors like #2140E3. */
function fade(hex: string, alpha: number): string {
  const n = parseInt(hex.slice(1), 16);
  const r = (n >> 16) & 255;
  const g = (n >> 8) & 255;
  const b = n & 255;
  return `rgba(${r},${g},${b},${alpha})`;
}

/** Lightened top-edge highlight for lit bars. */
function lighten(hex: string): string {
  const n = parseInt(hex.slice(1), 16);
  const r = Math.min(255, ((n >> 16) & 255) + 70);
  const g = Math.min(255, ((n >> 8) & 255) + 70);
  const b = Math.min(255, (n & 255) + 70);
  return `rgb(${r},${g},${b})`;
}

export function formatCompact(value: number): string {
  const abs = Math.abs(value);
  if (abs >= 1e12) return trim(value / 1e12) + "T";
  if (abs >= 1e9) return trim(value / 1e9) + "B";
  if (abs >= 1e6) return trim(value / 1e6) + "M";
  if (abs >= 1e3) return trim(value / 1e3) + "K";
  if (abs > 0 && abs < 0.01) return value.toExponential(1);
  return trim(value);
}

/**
 * Headline-number format: full digits below a billion (12 → "12",
 * 4,238,190 → "4,238,190"), compact above (3.37T).
 */
export function formatReading(value: number): string {
  const abs = Math.abs(value);
  if (abs >= 1e12) return trim(value / 1e12) + "T";
  if (abs >= 1e9) return trim(value / 1e9) + "B";
  if (abs >= 100) return Math.round(value).toLocaleString("en-US");
  return trim(value).toString();
}

function trim(n: number): string {
  return String(Math.round(n * 100) / 100);
}
