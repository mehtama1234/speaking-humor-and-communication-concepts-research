#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

cd "${REPO_ROOT}"

node scripts/validate_site_data.js
node scripts/validate_markdown_refs.js
node scripts/validate_analysis_move_first.js
node --check site/data.js
node --check site/app.js

echo "All validation checks passed."
