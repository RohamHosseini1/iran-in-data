import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

// One chart id contains a slash ("Swine / pigs"). Next writes that segment
// with a literal "%2F" in the filename. The sitemap URL encodes the slash
// once (%2F), and Vercel does not map that request onto the "%2F" filename.
//
// Vercel's Next builder copies `out/` into its deploy directory during
// `next build`, before this script runs. Copies that only land in `out/`
// never ship. Write the alias into every static root that already exists,
// including the builder output.
const webRoot = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");

function existingRoots() {
  const candidates = [
    path.join(webRoot, "out"),
    path.join(webRoot, ".vercel", "output", "static"),
    "/vercel/output/static",
  ];
  return candidates.filter((dir) => fs.existsSync(dir));
}

function walk(dir, found = []) {
  for (const ent of fs.readdirSync(dir, { withFileTypes: true })) {
    const full = path.join(dir, ent.name);
    if (ent.name.includes("%2F")) found.push(full);
    if (ent.isDirectory()) walk(full, found);
  }
  return found;
}

function safePath(src, root) {
  const rel = path.relative(root, src);
  return path.join(root, rel.replaceAll(" %2F ", "_").replaceAll("%2F", "_"));
}

// "Swine / pigs" decoded into a directory separator, which is what a host
// does when it turns %2F into a slash before the file lookup.
function decodedPath(src, root) {
  const rel = path.relative(root, src);
  return path.join(root, rel.replaceAll("%2F", "/"));
}

const roots = existingRoots();
if (roots.length === 0) {
  console.error("alias-encoded-slashes: no static output directory found");
  process.exit(1);
}

let copied = 0;
for (const root of roots) {
  console.log(`alias-encoded-slashes: scanning ${root}`);
  for (const src of walk(root)) {
    for (const dest of [safePath(src, root), decodedPath(src, root)]) {
      if (dest === src || fs.existsSync(dest)) continue;
      fs.mkdirSync(path.dirname(dest), { recursive: true });
      fs.cpSync(src, dest, { recursive: true });
      copied += 1;
    }
  }
}
console.log(`alias-encoded-slashes: copied ${copied} path(s)`);
