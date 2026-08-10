#!/usr/bin/env node

const fs = require("fs");
const path = require("path");

const repoRoot = path.resolve(__dirname, "..");
const analysisRoot = path.join(repoRoot, "analysis");
const requiredReference = "analysis/transcript-backed-concrete-speaking-approaches.md";
const exemptFiles = new Set([
  "transcript-backed-concrete-speaking-approaches.md",
]);

function walk(dir, files = []) {
  for (const child of fs.readdirSync(dir)) {
    const abs = path.join(dir, child);
    const stat = fs.statSync(abs);
    if (stat.isDirectory()) {
      walk(abs, files);
    } else if (abs.endsWith(".md")) {
      files.push(abs);
    }
  }
  return files;
}

if (!fs.existsSync(analysisRoot)) {
  console.error("analysis directory not found.");
  process.exit(1);
}

const files = walk(analysisRoot);
const missing = [];

for (const abs of files) {
  const name = path.basename(abs);
  if (exemptFiles.has(name)) continue;
  const text = fs.readFileSync(abs, "utf8");
  if (!text.includes(requiredReference)) {
    missing.push(path.relative(repoRoot, abs));
  }
}

if (missing.length > 0) {
  console.error(
    `Move-first validation failed. ${missing.length} analysis file(s) do not reference ${requiredReference}:`,
  );
  for (const rel of missing) {
    console.error(`- ${rel}`);
  }
  process.exit(1);
}

console.log(
  `Move-first validation passed. Checked ${files.length - exemptFiles.size} analysis markdown files.`,
);
