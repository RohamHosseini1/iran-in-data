import fs from "node:fs";
import path from "node:path";

import { getCatalog } from "@/lib/data/catalog";

export const dynamic = "force-static";

export function generateStaticParams() {
  return getCatalog().map((e) => ({ chartId: e.chart_id }));
}

const DATA_ROOT = process.env.IRAN_DATA_ROOT ?? path.resolve(process.cwd(), "..");

export async function GET(
  _request: Request,
  { params }: { params: Promise<{ chartId: string }> }
) {
  const { chartId: raw } = await params;
  let chartId = raw;
  try {
    chartId = decodeURIComponent(raw);
  } catch {}

  // Only serve files that exist in the catalog — no path traversal.
  const entry = getCatalog().find((e) => e.chart_id === chartId);
  if (!entry) return new Response("Not found", { status: 404 });

  const csv = fs.readFileSync(
    path.join(DATA_ROOT, "data", "charts", entry.chart_id, "data.csv"),
    "utf-8"
  );
  return new Response(csv, {
    headers: {
      "content-type": "text/csv; charset=utf-8",
      "content-disposition": `attachment; filename="${entry.chart_id.replace(/[^\w.-]+/g, "_")}.csv"`,
      "cache-control": "public, max-age=3600",
    },
  });
}
