"use client";

import * as React from "react";
import { init, type ECharts, type EChartsOption } from "echarts";
import { useTheme } from "next-themes";

import { nextZoomWindow } from "@/lib/charts/zoom";

interface InteractiveChartProps {
  /** Serializable option; chrome colors are patched in client-side. */
  option: EChartsOption;
  /** Build-time SVG shown until the interactive chart mounts. */
  ssrSvg?: string;
  height?: number;
  className?: string;
  /** X-window to zoom to after each option apply (start/end axis values). */
  zoomExtent?: [number, number];
  /** True when the x-axis is a time axis (sub-year data): no year snapping. */
  timeAxis?: boolean;
  /** Fired with the event marker index on markLine hover, null on leave. */
  onEventHover?: (index: number | null) => void;
  /** Same, for the separate grey law-marker layer. */
  onLawHover?: (index: number | null) => void;
}

/**
 * Hydrating ECharts host. Renders the server-generated SVG for first paint
 * (and for crawlers), then swaps in a live SVG-renderer chart. Re-themes on
 * light/dark switch and resizes with its container.
 *
 * ZOOM is ours, not ECharts'. Its inside-dataZoom applies a coarse step per wheel
 * tick, so a trackpad flick would leap from a decade to a single year; a snap-to-year
 * timer then yanked the window again after the gesture settled. Both are gone. Here a
 * wheel gesture nudges a TARGET window and a rAF loop eases the live window toward it,
 * anchored under the cursor and hard-clamped to the data extent, so zoom is continuous
 * and cannot travel past the first or last observation.
 */

/** Per-frame approach to the target window. Lower = smoother, laggier. */
const ZOOM_EASE = 0.22;
/** Below this the window is close enough to stop the rAF loop. */
const ZOOM_EPSILON = 1e-4;
export function InteractiveChart({
  option,
  ssrSvg,
  height = 420,
  className,
  zoomExtent,
  timeAxis = false,
  onEventHover,
  onLawHover,
}: InteractiveChartProps) {
  const hostRef = React.useRef<HTMLDivElement>(null);
  const chartRef = React.useRef<ECharts | null>(null);
  const { resolvedTheme } = useTheme();
  const [live, setLive] = React.useState(false);

  // Refs so the once-only init effect always sees current values.
  const zoomExtentRef = React.useRef(zoomExtent);
  zoomExtentRef.current = zoomExtent;
  const timeAxisRef = React.useRef(timeAxis);
  timeAxisRef.current = timeAxis;
  const onEventHoverRef = React.useRef(onEventHover);
  onEventHoverRef.current = onEventHover;
  const onLawHoverRef = React.useRef(onLawHover);
  onLawHoverRef.current = onLawHover;
  /** Set by the init effect; clears the wheel-zoom animation state. */
  const resetZoomRef = React.useRef<(() => void) | null>(null);

  React.useEffect(() => {
    const host = hostRef.current;
    if (!host) return;
    const chart = init(host, undefined, { renderer: "svg" });
    chartRef.current = chart;
    setLive(true);

    const currentWindow = (): [number, number] | null => {
      const opt = chart.getOption() as {
        dataZoom?: { startValue?: number; endValue?: number }[];
      };
      const dz = opt.dataZoom?.[0];
      if (dz?.startValue != null && dz?.endValue != null) {
        return [dz.startValue, dz.endValue];
      }
      return zoomExtentRef.current ?? null;
    };

    // ---- smooth, clamped wheel zoom -------------------------------------------
    // The bounds ARE the data extent, so zooming out stops exactly at the first and
    // last observation and never reveals empty gutter.
    const minSpan = () => (timeAxisRef.current ? 7 * 864e5 : 3);

    let target: [number, number] | null = null;
    // The window WE are animating. It must be our own state, never read back from the
    // chart: ECharts clamps what it applies, so an easing loop that re-reads the chart
    // can chase a target it will never reach and spin rAF forever, re-rendering every
    // frame until the renderer wedges. (It did.)
    let cur: [number, number] | null = null;
    let raf: number | null = null;

    const step = () => {
      raf = null;
      if (!target || !cur) return;
      const next: [number, number] = [
        cur[0] + (target[0] - cur[0]) * ZOOM_EASE,
        cur[1] + (target[1] - cur[1]) * ZOOM_EASE,
      ];
      const span = Math.max(target[1] - target[0], 1);
      const done =
        Math.abs(next[0] - target[0]) / span < ZOOM_EPSILON &&
        Math.abs(next[1] - target[1]) / span < ZOOM_EPSILON;
      cur = done ? target : next;
      chart.dispatchAction({
        type: "dataZoom",
        startValue: cur[0],
        endValue: cur[1],
      });
      if (done) target = null;
      else raf = requestAnimationFrame(step);
    };

    const onWheel = (ev: WheelEvent) => {
      const bounds = zoomExtentRef.current;
      if (!bounds) return;
      ev.preventDefault();

      // Re-sync from the chart only when idle: mid-gesture the chart lags our target.
      const win = target ?? cur ?? currentWindow();
      if (!win) return;

      // Trackpad pinch arrives as ctrl+wheel; it is already a deliberate zoom
      // gesture, so it gets a firmer factor than an incidental scroll.
      const delta = ev.deltaY * (ev.ctrlKey ? 2.2 : 1);

      // Anchor at the cursor so the point under the pointer stays put.
      const px = chart.convertFromPixel({ xAxisIndex: 0 }, [
        ev.offsetX,
        ev.offsetY,
      ]) as unknown as number[] | number;
      const cursor = Array.isArray(px) ? px[0] : px;
      const anchor =
        typeof cursor === "number" && Number.isFinite(cursor)
          ? cursor
          : (win[0] + win[1]) / 2;

      if (!cur) cur = [win[0], win[1]];
      target = nextZoomWindow({
        win: [win[0], win[1]],
        bounds,
        delta,
        anchor,
        minSpan: minSpan(),
      });
      if (raf == null) raf = requestAnimationFrame(step);
    };
    host.addEventListener("wheel", onWheel, { passive: false });

    // A new measure / country set means a new window: drop the animation state so a
    // stale one cannot leak across and fight the fresh zoomExtent.
    resetZoomRef.current = () => {
      if (raf != null) cancelAnimationFrame(raf);
      raf = null;
      target = null;
      cur = null;
    };

    // Marker hover → detail card beside the chart. Events (amber) and laws (grey)
    // are separate markLine series, so route by seriesName.
    chart.on("mouseover", (params) => {
      const p = params as {
        componentType?: string;
        dataIndex?: number;
        seriesName?: string;
      };
      if (p.componentType !== "markLine" || p.dataIndex == null) return;
      if (p.seriesName === "__laws__") onLawHoverRef.current?.(p.dataIndex);
      else onEventHoverRef.current?.(p.dataIndex);
    });
    chart.on("mouseout", (params) => {
      const p = params as { componentType?: string; seriesName?: string };
      if (p.componentType !== "markLine") return;
      if (p.seriesName === "__laws__") onLawHoverRef.current?.(null);
      else onEventHoverRef.current?.(null);
    });

    const observer = new ResizeObserver(() => chart.resize());
    observer.observe(host);
    return () => {
      if (raf != null) cancelAnimationFrame(raf);
      host.removeEventListener("wheel", onWheel);
      observer.disconnect();
      chart.dispose();
      chartRef.current = null;
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  React.useEffect(() => {
    const chart = chartRef.current;
    if (!chart) return;
    resetZoomRef.current?.();
    chart.setOption(option, { notMerge: true });
    if (zoomExtent) {
      chart.dispatchAction({
        type: "dataZoom",
        startValue: zoomExtent[0],
        endValue: zoomExtent[1],
      });
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [option, resolvedTheme]);

  return (
    <div className={className} style={{ position: "relative" }}>
      {!live && ssrSvg ? (
        <div
          aria-hidden
          className="chart-ssr"
          style={{ height, overflow: "hidden" }}
          dangerouslySetInnerHTML={{ __html: ssrSvg }}
        />
      ) : null}
      <div
        ref={hostRef}
        dir="ltr"
        style={{ height, display: live ? undefined : "none" }}
      />
    </div>
  );
}
