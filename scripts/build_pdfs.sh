#!/usr/bin/env bash
# Markdown -> standalone HTML (pandoc) -> PDF (headless Chromium). No LaTeX needed.
set -euo pipefail
cd "$(dirname "$0")/.."
mkdir -p build
# page limits from the brief: memo <= 2, Phase 1 <= 1, one-page brief <= 1
declare -A LIMIT=([memo]=2 [phase1]=1 [one_page_brief]=1)
for doc in memo phase1 one_page_brief; do
  [ -f "deliverables/$doc.md" ] || continue
  pandoc "deliverables/$doc.md" -f markdown -t html5 --standalone --embed-resources \
    --resource-path=deliverables --css scripts/print.css \
    --metadata pagetitle="$doc" -o "build/$doc.html"
  node scripts/html_to_pdf.js "build/$doc.html" "build/$doc.pdf"
  pages=$(python3 -c "import re,sys; d=open(sys.argv[1],'rb').read(); print(len(re.findall(rb'/Type\s*/Page[^s]', d)))" "build/$doc.pdf")
  echo "$doc: $pages page(s) (limit ${LIMIT[$doc]})"
  if [ "$pages" -gt "${LIMIT[$doc]}" ]; then echo "ERROR: $doc.pdf exceeds its page limit" >&2; exit 1; fi
done
