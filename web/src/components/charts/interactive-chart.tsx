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
}

/**
 * Hydrating ECharts host. Renders the server-generated SVG for first paint
 * (and for crawlers), then swaps in a live SVG-renderer chart. Re-themes on
 * light/dark switch and resizes with its container.
 *
 * Wheel zoom is implemented here rather than via ECharts' built-in handler:
 * the built-in step (~40% per tick) is what made zooming feel snappy and
 * jumpy. This one moves ~10% per wheel tick, anchored on the cursor.
 */
export function InteractiveChart({
  option,
  ssrSvg,
  height = 420,
  className,
  zoomExtent,
  timeAxis = false,
  onEventHover,
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

    // Trackpad/mouse zoom & pan, cursor-anchored and gentle:
    //  - vertical scroll / mouse wheel over the plot = zoom
    //  - pinch (Chrome sends ctrl+wheel, Safari sends gesture events) = zoom
    //  - horizontal two-finger scroll = pan
    const insidePlot = (px: number, py: number, rect: DOMRect) => {
      try {
        return chart.containPixel({ gridIndex: 0 }, [px, py]);
      } catch {
        // Geometry fallback: anywhere above the bottom slider strip.
        return px >= 0 && px <= rect.width && py >= 0 && py <= rect.height - 60;
      }
    };

    const clampWindow = (
      newStart: number,
      newEnd: number,
      full: [number, number]
    ): [number, number] => {
      const span = newEnd - newStart;
      if (newStart < full[0]) {
        newStart = full[0];
        newEnd = newStart + span;
      }
      if (newEnd > full[1]) {
        newEnd = full[1];
        newStart = Math.max(full[0], newEnd - span);
      }
      return [newStart, newEnd];
    };

    const zoomBy = (factor: number, px: number, py: number) => {
      const win = currentWindow();
      const full = zoomExtentRef.current;
      if (!win || !full) return;
      const [start, end] = win;
      const span = end - start;
      const fullSpan = full[1] - full[0];
      if (span <= 0 || fullSpan <= 0) return;
      const minSpan = timeAxisRef.current ? 7 * 864e5 : 3;
      const newSpan = Math.max(minSpan, Math.min(fullSpan, span * factor));
      if (newSpan === span) return;
      let anchor = (start + end) / 2;
      try {
        const converted = chart.convertFromPixel({ gridIndex: 0 }, [px, py]) as
          | number[]
          | null;
        if (converted && Number.isFinite(converted[0])) anchor = converted[0];
      } catch {
        /* keep center anchor */
      }
      const ratio = Math.max(0, Math.min(1, (anchor - start) / span));
      const [newStart, newEnd] = clampWindow(
        anchor - ratio * newSpan,
        anchor - ratio * newSpan + newSpan,
        full
      );
      chart.dispatchAction({
        type: "dataZoom",
        startValue: newStart,
        endValue: newEnd,
      });
    };

    const panBy = (frac: number) => {
      const win = currentWindow();
      const full = zoomExtentRef.current;
      if (!win || !full) return;
      const [start, end] = win;
      const span = end - start;
      if (span >= full[1] - full[0]) return;
      const shift = frac * span;
      const [newStart, newEnd] = clampWindow(start + shift, end + shift, full);
      chart.dispatchAction({
        type: "dataZoom",
        startValue: newStart,
        endValue: newEnd,
      });
    };

    const onWheel = (e: WheelEvent) => {
      const rect = host.getBoundingClientRect();
      const px = e.clientX - rect.left;
      const py = e.clientY - rect.top;
      if (!insidePlot(px, py, rect)) return;
      e.preventDefault();
      if (!e.ctrlKey && Math.abs(e.deltaX) > Math.abs(e.deltaY)) {
        panBy((e.deltaX / Math.max(rect.width, 1)) * 1.4);
        return;
      }
      // Pinch (ctrl+wheel) sends small continuous deltas; boost its scale.
      const scale = e.ctrlKey ? 0.01 : 0.004;
      const delta = Math.max(-60, Math.min(60, e.deltaY));
      zoomBy(Math.exp(delta * scale), px, py);
    };
    host.addEventListener("wheel", onWheel, { passive: false });

    // Safari trackpad pinch (proprietary gesture events, no wheel emitted).
    let lastGestureScale = 1;
    const onGestureStart = (e: Event) => {
      e.preventDefault();
      lastGestureScale =
        (e as unknown as { scale?: number }).scale ?? 1;
    };
    const onGestureChange = (e: Event) => {
      e.preventDefault();
      const g = e as unknown as {
        scale?: number;
        clientX?: number;
        clientY?: number;
      };
      const s = g.scale ?? 1;
      if (!s || !lastGestureScale) return;
      const factor = lastGestureScale / s;
      lastGestureScale = s;
      const rect = host.getBoundingClientRect();
      zoomBy(
        factor,
        (g.clientX ?? rect.left + rect.width / 2) - rect.left,
        (g.clientY ?? rect.top + rect.height / 2) - rect.top
      );
    };
    host.addEventListener("gesturestart", onGestureStart, { passive: false });
    host.addEventListener("gesturechange", onGestureChange, { passive: false });

    // Snap the zoom window to whole years once a gesture settles, so annual
    // charts tick between years instead of landing on fractions.
    let snapTimer: ReturnType<typeof setTimeout> | null = null;
    let snapping = false;
    chart.on("datazoom", () => {
      if (snapping || timeAxisRef.current) return;
      if (snapTimer) clearTimeout(snapTimer);
      snapTimer = setTimeout(() => {
        const win = currentWindow();
        if (!win) return;
        const start = Math.round(win[0]);
        const end = Math.round(win[1]);
        if (Math.abs(start - win[0]) < 0.01 && Math.abs(end - win[1]) < 0.01)
          return;
        snapping = true;
        chart.dispatchAction({
          type: "dataZoom",
          startValue: start,
          endValue: Math.max(end, start + 1),
        });
        snapping = false;
      }, 260);
    });

    // Event markers → hover card beside the chart (Overwatch-style).
    chart.on("mouseover", (params) => {
      const p = params as { componentType?: string; dataIndex?: number };
      if (p.componentType === "markLine" && p.dataIndex != null) {
        onEventHoverRef.current?.(p.dataIndex);
      }
    });
    chart.on("mouseout", (params) => {
      const p = params as { componentType?: string };
      if (p.componentType === "markLine") {
        onEventHoverRef.current?.(null);
      }
    });

    const observer = new ResizeObserver(() => chart.resize());
    observer.observe(host);
    return () => {
      if (snapTimer) clearTimeout(snapTimer);
      host.removeEventListener("wheel", onWheel);
      host.removeEventListener("gesturestart", onGestureStart);
      host.removeEventListener("gesturechange", onGestureChange);
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
