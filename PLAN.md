# Build plan — "The Photon That Didn't Show Up"

## Tasks
- [x] Plan written
- [x] Environment: `.venv`, Python 3.13, pinned requirements
- [ ] `src/chsh.py` pure functions (E1–E6) with docstrings
- [ ] `tests/test_chsh.py` expected-value tests
- [ ] `analysis.ipynb` (E1–E6 + hand re-derivations) → `results/results.json`
- [ ] Figures at 300 dpi, visually inspected
- [ ] Deliverables: phase1, claims_ledger, memo, assumptions
- [ ] Number-check script (`scripts/check_numbers.py`) memo ↔ results.json
- [ ] Independent reviewer subagent → `review/review.md`
- [ ] Fixes from review logged in DECISIONS.md; Limitations in memo
- [ ] Packaging: executed notebook + HTML, PDFs, `submission/`, `submission.zip`
- [ ] Final verification

## Definition of done
- [ ] `pytest` passes, no tests weakened
- [ ] Notebook executes top to bottom from clean kernel, fixed seed
- [ ] `results/results.json` exists; every number in memo matches it (script)
- [ ] Figures 300 dpi, inspected, no overlaps, main title states conclusion
- [ ] Memo ≤ 2 pages PDF; recommendation first; hypothesis section; sources
- [ ] Phase 1 ≤ 1 page
- [ ] Reviewer report exists, valid points addressed
- [ ] DECISIONS.md lists every judgment call
- [ ] submission.zip contains everything and opens cleanly
- [ ] Final message
