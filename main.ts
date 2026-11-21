// news-image-20261121-cand-a: builds entry.png with the Python generator
// (build_entry.py, PIL, deterministic) and copies it to the output dir.
import { execFileSync } from "node:child_process";
import { copyFileSync, mkdirSync, statSync } from "node:fs";
import { join } from "node:path";
import { fileURLToPath } from "node:url";

const here = fileURLToPath(new URL(".", import.meta.url));

execFileSync("python3", [join(here, "build_entry.py")], { stdio: "inherit" });

const sourcePath = join(here, "entry.png");
const size = statSync(sourcePath).size;
if (size === 0) {
  throw new Error(`entry.png is empty (0 bytes) at ${sourcePath}`);
}
if (size > 1048576) {
  throw new Error(
    `entry.png too large: ${size} bytes exceeds 1 MiB limit (1048576 bytes)`,
  );
}

const outDir = process.env.MAKEFUN_OUTPUT_DIR || "/output";
mkdirSync(outDir, { recursive: true });
copyFileSync(sourcePath, join(outDir, "entry.png"));
console.log(`entry.png ${size} bytes -> ${join(outDir, "entry.png")}`);
