# Changelog

## 1.0.0 — 2026-11-19 (COMS 4995W Lab-to-Market hackathon, Challenge 03)

- CHSH model (`src/chsh.py`): brute-force classical limit, Born-rule singlet sampling, noisy-source model,
  non-heralded photon loss with a Monte Carlo that drops photons, heralded (quantum-memory) rescue case,
  classical detection-loophole cheater, frontier classification, Ding & Jiang Theorem 10 with independent
  brute-force and optimiser checks, economics.
- Notebook `analysis.ipynb` (E1–E6, E2b) writing every number to `results/results.json`; fixed seed.
- Main figure `figures/main_frontier.png` plus supporting figures at 300 dpi.
- Deliverables rendered from `results.json`: Phase 1 plan, executive memo (2 pages), claims ledger, assumptions,
  evidence register, steelman and rebuttal, one-page brief, 3-minute oral script; number-traceability checker.
- Independent reviewer report (`review/review.md`) and all fixes logged in `DECISIONS.md`.
- Interactive static website with Python–browser parity tests; CI and GitHub Pages deployment from `main`.
