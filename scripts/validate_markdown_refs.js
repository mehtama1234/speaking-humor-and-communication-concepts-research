#!/usr/bin/env node

const fs = require("fs");
const path = require("path");

const repoRoot = path.resolve(__dirname, "..");
const scanRoots = [
  path.join(repoRoot, "README.md"),
  path.join(repoRoot, "analysis"),
  path.join(repoRoot, "raw-material", "README.md"),
];

const allowedExtensions = new Set([
  ".md",
  ".json",
  ".txt",
  ".html",
  ".js",
  ".py",
  ".css",
]);

const filesToScan = [];

for (const entry of scanRoots) {
  if (!fs.existsSync(entry)) continue;
  const stat = fs.statSync(entry);
  if (stat.isFile()) {
    filesToScan.push(entry);
    continue;
  }
  walk(entry);
}

function walk(dir) {
  for (const child of fs.readdirSync(dir)) {
    const abs = path.join(dir, child);
    const stat = fs.statSync(abs);
    if (stat.isDirectory()) {
      walk(abs);
    } else if (abs.endsWith(".md")) {
      filesToScan.push(abs);
    }
  }
}

const candidateRegex =
  /`((?:analysis|concepts|site|scripts|raw-material)\/[^`\n]+?\.(?:md|json|txt|html|js|py|css))`/g;

const errors = [];
let checked = 0;

for (const file of filesToScan) {
  const content = fs.readFileSync(file, "utf8");
  for (const match of content.matchAll(candidateRegex)) {
    const rel = match[1];
    const ext = path.extname(rel);
    if (!allowedExtensions.has(ext)) continue;
    checked += 1;
    const abs = path.join(repoRoot, rel);
    if (!fs.existsSync(abs)) {
      errors.push(`${path.relative(repoRoot, file)} references missing path "${rel}"`);
    }
  }
}

if (errors.length > 0) {
  console.error(`Broken markdown references: ${errors.length}`);
  for (const error of errors) {
    console.error(`- ${error}`);
  }
  process.exit(1);
}

console.log(`Markdown reference validation passed. Checked ${checked} references across ${filesToScan.length} markdown files.`);
