import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

// One chart id contains a slash ("Swine / pigs"). Next writes that segment
// with a literal "%2F" in the filename. The sitemap URL encodes the slash
// once (%2F), and Vercel does not map that request onto the "%2F" filename.
//
// Vercel's Next builder snapshots `out/` during `next build`. Files added
// afterwards are not deployed. This script copies the aliases into `public/`
// and the build command runs `next build` a second time so they are part of
// that snapshot. The public URL stays the encoded sitemap URL.
const webRoot = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const outDir = path.join(webRoot, "out");
const publicDir = path.join(webRoot, "public");

function walk(dir, found = []) {
  for (const ent of fs.readdirSync(dir, { withFileTypes: true })) {
    const full = path.join(dir, ent.name);
    if (ent.name.includes("%2F")) found.push(full);
    if (ent.isDirectory()) walk(full, found);
  }
  return found;
}

if (!fs.existsSync(outDir)) {
  console.error("alias-encoded-slashes: out/ is missing, run next build first");
  process.exit(1);
}

let copied = 0;
for (const src of walk(outDir)) {
  const rel = path.relative(outDir, src);
  for (const relDest of [
    rel.replaceAll(" %2F ", "_").replaceAll("%2F", "_"),
    rel.replaceAll("%2F", "/"),
  ]) {
    if (relDest === rel) continue;
    const dest = path.join(publicDir, relDest);
    if (fs.existsSync(dest)) continue;
    fs.mkdirSync(path.dirname(dest), { recursive: true });
    fs.cpSync(src, dest, { recursive: true });
    copied += 1;
  }
}
console.log(`alias-encoded-slashes: staged ${copied} path(s) into public/`);
