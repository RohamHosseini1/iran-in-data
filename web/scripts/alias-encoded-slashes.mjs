import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

// One chart id contains a slash ("Swine / pigs"). Static export writes that
// segment with a literal %2F in the filename. Some hosts decode %2F into a
// directory separator before the file lookup. Copy those outputs onto the
// decoded path so both lookups hit the same bytes. URLs stay the same.
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
  const dest = src.replaceAll("%2F", "/");
  if (dest === src || fs.existsSync(dest)) continue;
  fs.mkdirSync(path.dirname(dest), { recursive: true });
  fs.cpSync(src, dest, { recursive: true });
  copied += 1;
}
console.log(`alias-encoded-slashes: copied ${copied} path(s)`);
