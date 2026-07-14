"use client";

import * as React from "react";
import { init, type ECharts, type EChartsOption } from "echarts";
import { useTheme } from "next-themes";

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
 * Wheel zoom is ours (see below); pinch and drag-to-pan stay ECharts'. The window is
 * bounded by the data extent, so it cannot travel past the first or last observation.
 */

/**
 * Wheel delta -> zoom.
 *
 * This has to serve two very different devices. A mouse notch arrives as ONE event of
 * deltaY ~100. A macOS trackpad arrives as a STREAM of ~30 events of deltaY ~2-5. A
 * value tuned for the mouse (0.0009) moves the window 0.36% per trackpad event, so a
 * whole flick did nothing and the chart felt dead. This value is tuned for the
 * trackpad instead, and the MAX_STEP cap below is what keeps the mouse usable.
 */
const ZOOM_SENSITIVITY = 0.004;
/**
 * Hard ceiling on how far ONE wheel event may scale the window. This is what lets a
 * single sensitivity serve both devices: a mouse notch would otherwise scale by 1.49x
 * and slam to a stop, and it also stops trackpad momentum from running away. A fast
 * gesture sends MORE events, so it zooms further, but never faster per event.
 */
const MAX_STEP = 1.06;

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

  React.useEffect(() => {
    const host = hostRef.current;
    if (!host) return;
    const chart = init(host, undefined, { renderer: "svg" });
    chartRef.current = chart;
    setLive(true);

    // ---- wheel zoom ------------------------------------------------------------
    // ECharts scales its own zoom step by the RAW wheel delta and exposes no
    // sensitivity option, so a trackpad's burst of large deltas compounds to full
    // zoom in a single flick. We take the wheel instead. There is no animation loop
    // here on purpose: each event maps to one bounded, synchronous window update.
    const minSpan = () => (timeAxisRef.current ? 7 * 864e5 : 3);

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

    const onWheel = (ev: WheelEvent) => {
      const bounds = zoomExtentRef.current;
      const win = currentWindow();
      if (!bounds || !win) return;
      ev.preventDefault();

      // Normalise: a mouse wheel reports ~100 per notch, a trackpad a stream of small
      // deltas, and deltaMode 1 counts LINES not pixels.
      let delta = ev.deltaY;
      if (ev.deltaMode === 1) delta *= 16;
      else if (ev.deltaMode === 2) delta *= 400;

      // The cap is the whole point: no single wheel event may move the window by more
      // than MAX_STEP, so a fast flick zooms FURTHER, never FASTER-per-event, and can
      // never slam to the innermost or outermost stop.
      const raw = Math.exp(delta * ZOOM_SENSITIVITY);
      const factor = Math.min(Math.max(raw, 1 / MAX_STEP), MAX_STEP);

      // Anchor under the cursor so the point you are pointing at stays put.
      const px = chart.convertFromPixel({ xAxisIndex: 0 }, [
        ev.offsetX,
        ev.offsetY,
      ]) as unknown as number[] | number;
      const cursor = Array.isArray(px) ? px[0] : px;
      const anchor =
        typeof cursor === "number" && Number.isFinite(cursor)
          ? Math.min(Math.max(cursor, win[0]), win[1])
          : (win[0] + win[1]) / 2;

      const full = bounds[1] - bounds[0];
      const rawSpan = (win[1] - win[0]) * factor;
      const span = Math.min(Math.max(rawSpan, minSpan()), full);
      const frac = (anchor - win[0]) / (win[1] - win[0] || 1);

      let start = anchor - frac * span;
      let end = start + span;
      if (start < bounds[0]) {
        start = bounds[0];
        end = start + span;
      }
      if (end > bounds[1]) {
        end = bounds[1];
        start = end - span;
      }
      chart.dispatchAction({ type: "dataZoom", startValue: start, endValue: end });
    };
    host.addEventListener("wheel", onWheel, { passive: false });

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
