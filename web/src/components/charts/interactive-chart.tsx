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

    // Gentle, cursor-anchored wheel zoom (~10% per tick; trackpad pinch
    // scales with gesture delta). Scrolling outside the plot area is left
    // to the page.
    const onWheel = (e: WheelEvent) => {
      const rect = host.getBoundingClientRect();
      const px = e.clientX - rect.left;
      const py = e.clientY - rect.top;
      if (!chart.containPixel({ gridIndex: 0 }, [px, py])) return;
      e.preventDefault();
      const win = currentWindow();
      const full = zoomExtentRef.current;
      if (!win || !full) return;
      const [start, end] = win;
      const span = end - start;
      const fullSpan = full[1] - full[0];
      if (span <= 0 || fullSpan <= 0) return;

      const delta = Math.max(-40, Math.min(40, e.deltaY));
      const factor = Math.exp(delta * 0.0035); // ±100 deltaY ≈ ±15%
      const minSpan = timeAxisRef.current ? 7 * 864e5 : 3;
      const newSpan = Math.max(minSpan, Math.min(fullSpan, span * factor));
      if (newSpan === span) return;

      const converted = chart.convertFromPixel({ gridIndex: 0 }, [px, py]) as
        | number[]
        | null;
      const anchor = converted?.[0] ?? (start + end) / 2;
      const ratio = Math.max(0, Math.min(1, (anchor - start) / span));
      let newStart = anchor - ratio * newSpan;
      let newEnd = newStart + newSpan;
      if (newStart < full[0]) {
        newStart = full[0];
        newEnd = newStart + newSpan;
      }
      if (newEnd > full[1]) {
        newEnd = full[1];
        newStart = Math.max(full[0], newEnd - newSpan);
      }
      chart.dispatchAction({
        type: "dataZoom",
        startValue: newStart,
        endValue: newEnd,
      });
    };
    host.addEventListener("wheel", onWheel, { passive: false });

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
