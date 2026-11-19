#!/usr/bin/env bash
# Markdown -> standalone HTML (pandoc) -> PDF (headless Chromium). No LaTeX needed.
set -euo pipefail
cd "$(dirname "$0")/.."
mkdir -p build
for doc in memo phase1 one_page_brief; do
  [ -f "deliverables/$doc.md" ] || continue
  pandoc "deliverables/$doc.md" -f markdown -t html5 --standalone --embed-resources \
    --resource-path=deliverables --css scripts/print.css \
    --metadata pagetitle="$doc" -o "build/$doc.html"
  node scripts/html_to_pdf.js "build/$doc.html" "build/$doc.pdf"
  echo "$doc: $(pdfinfo build/$doc.pdf | awk '/^Pages/{print $2}') page(s)"
done
