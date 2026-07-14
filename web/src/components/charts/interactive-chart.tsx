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
 * Zoom is ECharts' own inside-dataZoom, so wheel, trackpad, pinch and drag all work.
 * The window is bounded by the data extent, so it cannot pan past the first or last
 * observation.
 */
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

    // Zoom is ECharts' own inside-dataZoom (wheel, trackpad, pinch, drag). A custom
    // wheel handler that eased the window itself was tried and reverted: it is NOT
    // worth reimplementing a gesture the library already handles across every input
    // device. The jumping the owner reported came from the snap-to-year timer that
    // used to live here, which fired a dataZoom jump 260ms after every gesture
    // settled. That is gone. Sensitivity is tempered in line-option.ts instead.

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
