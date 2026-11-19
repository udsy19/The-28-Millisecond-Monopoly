#!/usr/bin/env bash
# Build the submission bundle: executed notebook (+HTML), PDFs, submission/ and submission.zip.
set -euo pipefail
cd "$(dirname "$0")/.."
python scripts/build_notebook.py
jupyter nbconvert --to notebook --execute analysis.ipynb --output analysis_executed.ipynb
jupyter nbconvert --to html analysis_executed.ipynb --output analysis_executed
python scripts/render_deliverables.py
python scripts/check_numbers.py
NODE_PATH="${NODE_PATH:-$(npm root -g)}" scripts/build_pdfs.sh
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
[ -f review/review.md ] && cp review/review.md submission/
find submission -name __pycache__ -prune -exec rm -rf {} +
(cd submission && zip -qr ../submission.zip .)
unzip -tq submission.zip
echo "submission.zip: $(unzip -l submission.zip | tail -1)"
