# Disclosure: case file, sources and AI assistance

**Case file.** The startup, its numbers and the ±$100 payoff are fictional, set by the COMS 4995W Lab-to-Market
Challenge 03 brief (`case_file.md`). Every case-file number is treated as a claim and tested
(`deliverables/claims_ledger.md`).

**Sources.** Published works are cited, not reproduced verbatim: Ding & Jiang (arXiv:2407.21723); Szegedy, Ding &
Shi (US Patent 11676104B2); Mermin (1986); Eberhard (1993); Yin et al. (2017); Craddock et al. (2024); Neumann
et al. (2022); Hibernia Express (2015); Aquilina, Budish & O'Neill (2022); Liu et al. (2025). Distances between
trading sites are approximate. We did not read the patent claims in legal detail.

**AI assistance.** The code, tests, documents and website were written by Anthropic's Claude (Claude Code), acting
as a lead agent with parallel sub-agents (website, tier-2 documents) and a separate reviewer agent that had not
seen the lead's reasoning, under the direction of the human author (Udaya Tejas). Commits carry a
`Co-Authored-By: Claude` trailer. Every numerical claim is produced by executed code and traceable to
`results/results.json`; judgment calls are logged in `DECISIONS.md`.

**Dependencies** (installed, not vendored): NumPy, SciPy, Matplotlib, Jupyter/nbconvert, pytest, ruff; pandoc and
Playwright/Chromium for PDFs. Fonts used by the website keep their own licences (see `site/fonts/`).
