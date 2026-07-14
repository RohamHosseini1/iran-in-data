import "server-only";

import { init, type EChartsOption } from "echarts";

/**
 * Render a chart to an SVG string at build time. The markup ships in the
 * initial HTML — crawlers and LLM agents see real data points with zero JS —
 * then the client component hydrates it into an interactive chart.
 */
export function renderChartSvg(
  option: EChartsOption,
  { width = 800, height = 420 }: { width?: number; height?: number } = {}
): string {
  const chart = init(null, null, { renderer: "svg", ssr: true, width, height });
  chart.setOption({ ...option, animation: false });
  const svg = chart.renderToSVGString();
  chart.dispose();
  return svg;
}
