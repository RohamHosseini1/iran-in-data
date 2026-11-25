import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // Prerendered App Router pages and `force-static` route handlers are stored
  // in Vercel's ISR cache. A CDN miss is an ISR read, which is what a crawler
  // burst bills. `output: "export"` writes every page, CSV, and JSON body
  // into `out/` and Vercel hosts that directory as plain CDN files.
  //
  // Redirects and the locale proxy cannot be emitted by a static export.
  // Unprefixed URLs are redirected in `vercel.json`.
  output: "export",
};

export default nextConfig;
