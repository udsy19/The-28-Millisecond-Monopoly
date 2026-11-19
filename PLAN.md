# Build plan — "The Photon That Didn't Show Up"

## Tasks
- [x] Plan written
- [x] Environment: `.venv`, Python 3.13, pinned requirements
- [x] `src/chsh.py` pure functions (E1–E6) with docstrings
- [x] `tests/test_chsh.py` expected-value tests
- [x] `analysis.ipynb` (E1–E6 + hand re-derivations) → `results/results.json`
- [x] Figures at 300 dpi, visually inspected
- [x] Deliverables: phase1, claims_ledger, memo, assumptions
- [x] Number-check script (`scripts/check_numbers.py`) memo ↔ results.json
- [x] Independent review → `review/review.md`
- [x] Fixes from review logged in DECISIONS.md; Limitations in memo
- [x] Packaging: executed notebook + HTML, PDFs, `submission/`, `submission.zip`
- [x] Final verification

## Definition of done
- [x] `pytest` passes, no tests weakened
- [x] Notebook executes top to bottom from clean kernel, fixed seed
- [x] `results/results.json` exists; every number in memo matches it (script)
- [x] Figures 300 dpi, inspected, no overlaps, main title states conclusion
- [x] Memo ≤ 2 pages PDF; recommendation first; hypothesis section; sources
- [x] Phase 1 ≤ 1 page
- [x] Reviewer report exists, valid points addressed
- [x] DECISIONS.md lists every judgment call
- [x] submission.zip contains everything and opens cleanly
- [x] Final message

## Tier status (priority note)
- [x] Tier 1: Phase 1, reproducible notebook, main figure, memo, assumptions — committed and pushed
- [x] Tier 2: evidence register, steelman/rebuttal, one-page brief, oral script
- [x] Tier 3: interactive exhibit in `site/` with Python–browser parity tests
- [x] Tier 4: CI (green on PR), Pages workflow (deploys from `main` only, so not live until merged), draft PR
- [ ] Section 7 (automation framework): skipped as instructed
