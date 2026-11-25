import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

// One chart id contains a slash ("Swine / pigs"). Static export writes that
// segment with a literal %2F in the filename, and Vercel does not serve that
// filename at the sitemap's encoded URL. Copy each of those outputs to a
// single safe segment, faostat__Swine_pigs__production. vercel.json rewrites
// the original URL onto that file. The public URL does not change.
const out = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "../out");

function walk(dir) {
  const found = [];
  for (const ent of fs.readdirSync(dir, { withFileTypes: true })) {
    const full = path.join(dir, ent.name);
    if (ent.name.includes("%2F")) found.push(full);
    if (ent.isDirectory()) found.push(...walk(full));
  }
  return found;
}

if (!fs.existsSync(out)) {
  console.error("alias-encoded-slashes: out/ is missing, run next build first");
  process.exit(1);
}

let copied = 0;
for (const src of walk(out)) {
  // "Swine / pigs" is written as "Swine %2F pigs". A safe single segment
  // (no slash, space, or percent) is what the CDN rewrite below serves
  // for the original encoded URL.
  const dest = src.replaceAll(" %2F ", "_").replaceAll("%2F", "_");
  if (dest === src || fs.existsSync(dest)) continue;
  fs.mkdirSync(path.dirname(dest), { recursive: true });
  fs.cpSync(src, dest, { recursive: true });
  copied += 1;
}
console.log(`alias-encoded-slashes: copied ${copied} path(s)`);
