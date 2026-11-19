#!/usr/bin/env bash
# Build the submission bundle: executed notebook (+HTML), PDFs, submission/ and submission.zip.
#
# Fails loudly (ERROR: ... on stderr, non-zero exit) if any PDF exceeds its page limit,
# if submission.zip is missing any required file, or if the archive fails its integrity test.
#
# Usage:
#   scripts/package.sh                    full build + all checks
#   scripts/package.sh --check-pages DIR  only check page limits of DIR/{memo,phase1,one_page_brief}.pdf
#   scripts/package.sh --check-zip ZIP    only check ZIP's integrity and required-file manifest
set -euo pipefail
cd "$(dirname "$0")/.."

# Page limits from the brief (checked here independently of build_pdfs.sh).
declare -A PAGE_LIMIT=([memo]=2 [phase1]=1 [one_page_brief]=1)

# Every entry that must be present in submission.zip (paths relative to the archive root).
REQUIRED_FILES=(
  phase1.pdf
  memo.pdf
  one_page_brief.pdf
  claims_ledger.md
  assumptions.md
  evidence_register.md
  steelman_rebuttal.md
  oral_script.md
  main_frontier.png
  analysis_executed.html
  review.md
  code/src/chsh.py
  code/tests/test_chsh.py
  code/analysis.ipynb
  code/requirements.txt
  code/README.md
  code/results/results.json
)

err() { echo "ERROR: $*" >&2; }

pdf_pages() {
  # Prefer poppler's pdfinfo; fall back to counting /Type /Page objects (not /Pages).
  if command -v pdfinfo >/dev/null 2>&1; then
    pdfinfo "$1" 2>/dev/null | awk '/^Pages:/ {print $2}'
  else
    python3 -c "import re,sys; d=open(sys.argv[1],'rb').read(); print(len(re.findall(rb'/Type\s*/Page(?![a-zA-Z])', d)))" "$1"
  fi
}

check_pages() {
  local dir=$1 fail=0 doc pdf pages
  for doc in memo phase1 one_page_brief; do
    pdf="$dir/$doc.pdf"
    if [ ! -s "$pdf" ]; then err "$pdf is missing or empty"; fail=1; continue; fi
    pages=$(pdf_pages "$pdf")
    if ! [[ "$pages" =~ ^[0-9]+$ ]] || [ "$pages" -lt 1 ]; then
      err "could not count pages in $pdf (got '$pages')"; fail=1; continue
    fi
    if [ "$pages" -gt "${PAGE_LIMIT[$doc]}" ]; then
      err "$doc.pdf has $pages pages; limit is ${PAGE_LIMIT[$doc]}"; fail=1
    else
      echo "ok: $doc.pdf $pages page(s) (limit ${PAGE_LIMIT[$doc]})"
    fi
  done
  return "$fail"
}

check_zip() {
  local zip=$1 missing
  if [ ! -s "$zip" ]; then err "$zip is missing or empty"; return 1; fi
  if ! unzip -tq "$zip"; then err "$zip failed its integrity test (unzip -tq)"; return 1; fi
  missing=$(python3 - "$zip" "${REQUIRED_FILES[@]}" <<'PY'
import sys, zipfile
names = {n[2:] if n.startswith("./") else n for n in zipfile.ZipFile(sys.argv[1]).namelist()}
print("\n".join(f for f in sys.argv[2:] if f not in names))
PY
)
  if [ -n "$missing" ]; then
    err "$zip is missing required file(s):"
    sed 's/^/  - /' <<<"$missing" >&2
    return 1
  fi
  echo "ok: $zip passes integrity test and contains all ${#REQUIRED_FILES[@]} required files"
}

case "${1:-}" in
  --check-pages) check_pages "${2:?usage: --check-pages DIR}"; exit ;;
  --check-zip)   check_zip "${2:?usage: --check-zip ZIP}"; exit ;;
  "") ;;
  *) err "unknown argument: $1"; exit 2 ;;
esac

python scripts/build_notebook.py
jupyter nbconvert --to notebook --execute analysis.ipynb --output analysis_executed.ipynb
jupyter nbconvert --to html analysis_executed.ipynb --output analysis_executed
python scripts/render_deliverables.py
python scripts/check_numbers.py

rm -f build/memo.pdf build/phase1.pdf build/one_page_brief.pdf   # never check stale PDFs
pdf_rc=0
NODE_PATH="${NODE_PATH:-$(npm root -g)}" scripts/build_pdfs.sh || pdf_rc=$?
pages_rc=0
check_pages build || pages_rc=$?
if [ "$pdf_rc" -ne 0 ] || [ "$pages_rc" -ne 0 ]; then
  err "PDF build or page-limit check failed (build_pdfs.sh exit $pdf_rc); not packaging"
  exit 1
fi

if [ ! -f review/review.md ]; then err "review/review.md is required for the submission"; exit 1; fi

mkdir -p reports && cp build/phase1.pdf build/memo.pdf build/one_page_brief.pdf reports/   # committed, served by the site
rm -rf submission submission.zip
mkdir -p submission/figures submission/code
cp build/phase1.pdf build/memo.pdf build/one_page_brief.pdf submission/
cp deliverables/claims_ledger.md deliverables/assumptions.md deliverables/evidence_register.md \
   deliverables/steelman_rebuttal.md deliverables/oral_script.md submission/
cp figures/main_frontier.png submission/
cp figures/*.png submission/figures/
cp analysis_executed.html submission/
cp -r src tests scripts site analysis.ipynb requirements.txt README.md DECISIONS.md case_file.md submission/code/
mkdir -p submission/code/results && cp results/results.json submission/code/results/
cp review/review.md submission/
find submission -name __pycache__ -prune -exec rm -rf {} +
(cd submission && zip -qr ../submission.zip .)

check_zip submission.zip
echo "submission.zip: $(unzip -l submission.zip | tail -1)"
