#!/usr/bin/env node

const fs = require("fs");
const path = require("path");
const vm = require("vm");

const repoRoot = path.resolve(__dirname, "..");
const siteDataPath = path.join(repoRoot, "site", "data.js");

const source = fs.readFileSync(siteDataPath, "utf8");
const context = { window: {} };
vm.createContext(context);
vm.runInContext(source, context, { filename: siteDataPath });

const data = context.window.SPEAKING_SITE_DATA;

if (!data || typeof data !== "object") {
  console.error("Failed to load window.SPEAKING_SITE_DATA");
  process.exit(1);
}

const collections = [
  "corpora",
  "concepts",
  "drills",
  "pathways",
  "examples",
  "sessions",
  "sources",
  "evidence",
  "matrix",
  "roadmap",
  "contrasts",
  "curriculum",
];

const slugIndexByCollection = new Map();
const errors = [];
const warnings = [];

for (const collectionName of collections) {
  const items = data[collectionName];
  if (!Array.isArray(items)) {
    errors.push(`Collection "${collectionName}" is missing or not an array`);
    continue;
  }

  const index = new Map();
  for (const item of items) {
    if (!item || typeof item !== "object") {
      errors.push(`Collection "${collectionName}" contains a non-object item`);
      continue;
    }
    if (!item.slug || typeof item.slug !== "string") {
      errors.push(`Collection "${collectionName}" contains an item without a string slug`);
      continue;
    }
    if (index.has(item.slug)) {
      errors.push(`Duplicate slug "${item.slug}" in collection "${collectionName}"`);
      continue;
    }
    index.set(item.slug, item);
  }
  slugIndexByCollection.set(collectionName, index);
}

const relationMap = {
  conceptSlugs: "concepts",
  corpusSlugs: "corpora",
  drillSlugs: "drills",
  pathwaySlugs: "pathways",
  exampleSlugs: "examples",
  sessionSlugs: "sessions",
  sourceSlugs: "sources",
  evidenceSlugs: "evidence",
  matrixSlugs: "matrix",
  roadmapSlugs: "roadmap",
  contrastSlugs: "contrasts",
  curriculumSlugs: "curriculum",
};

for (const collectionName of collections) {
  const items = data[collectionName] || [];
  for (const item of items) {
    if (!item || typeof item !== "object" || !item.slug) continue;

    for (const [property, targetCollection] of Object.entries(relationMap)) {
      if (!(property in item)) continue;
      if (!Array.isArray(item[property])) {
        errors.push(
          `${collectionName}:${item.slug} has non-array relation "${property}"`,
        );
        continue;
      }

      const targetIndex = slugIndexByCollection.get(targetCollection);
      for (const slug of item[property]) {
        if (typeof slug !== "string" || !slug) {
          errors.push(
            `${collectionName}:${item.slug} has invalid ${property} entry "${String(slug)}"`,
          );
          continue;
        }
        if (!targetIndex || !targetIndex.has(slug)) {
          errors.push(
            `${collectionName}:${item.slug} references missing ${targetCollection} slug "${slug}" via ${property}`,
          );
        }
      }
    }

    if ("linkedFiles" in item) {
      if (!Array.isArray(item.linkedFiles)) {
        errors.push(`${collectionName}:${item.slug} has non-array linkedFiles`);
      } else {
        for (const relFile of item.linkedFiles) {
          if (typeof relFile !== "string" || !relFile) {
            errors.push(
              `${collectionName}:${item.slug} has invalid linkedFiles entry "${String(relFile)}"`,
            );
            continue;
          }
          const absFile = path.join(repoRoot, relFile);
          if (!fs.existsSync(absFile)) {
            errors.push(
              `${collectionName}:${item.slug} references missing linked file "${relFile}"`,
            );
          }
        }
      }
    } else {
      warnings.push(`${collectionName}:${item.slug} has no linkedFiles`);
    }
  }
}

if (warnings.length > 0) {
  console.warn(`Warnings: ${warnings.length}`);
  for (const warning of warnings) {
    console.warn(`- ${warning}`);
  }
}

if (errors.length > 0) {
  console.error(`Errors: ${errors.length}`);
  for (const error of errors) {
    console.error(`- ${error}`);
  }
  process.exit(1);
}

console.log("Site data validation passed.");
for (const collectionName of collections) {
  const count = (data[collectionName] || []).length;
  console.log(`- ${collectionName}: ${count}`);
}
