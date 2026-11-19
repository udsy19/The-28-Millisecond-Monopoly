# Decisions log

Every judgment call made while building this submission: the decision, the alternatives, and why.

| # | Decision | Alternatives considered | Why |
|---|---|---|---|
| D1 | Read the 82% as a win rate on rounds where **both** photons were detected | Read it as an all-rounds rate | On a 40 km link only ~16% of rounds have both photons; an all-rounds 82% is impossible under the case's own link spec (E2). The brief's priority note also says to use this reading unless logs show otherwise. |
| D2 | Read "1,000 trials" as 1,000 scored (coincidence) rounds | 1,000 attempted rounds | Consistent with D1; we report the implied attempted rounds (~6,310) and make it founder question 1. |
| D3 | Read "1,000 pairs/s" as pairs generated at the source | Pairs delivered to both desks | Literal reading of a source spec. Both readings are reported (1.0 h vs 6.3 h of generation for the claimed volume); neither changes the decision. |
| D4 | One-bit boundary uses the vacuum speed of light | Fibre speed (~c/1.47) | Best case for a microwave link and conservative for us (it shrinks the region where quantum could matter). Fibre would move the line by a constant factor; the red region is red on loss grounds regardless. |
| D5 | z-scores use the null-hypothesis standard error √(0.75·0.25/n) | Observed-rate SE | Standard for testing "is this above 75%?"; gives +5.1 and −0.7 as the brief expected. |
| D6 | Sub-ideal source modelled as a singlet mixed with white noise (visibility V = 0.905 for 82%) | Rotated angles, coloured noise | Simplest physically meaningful model that reproduces 82% exactly; the photon-loss result depends only on the 82%, not on the noise model. |
| D7 | Lost-photon fallback = fixed answer 0 (coin-flip rounds when one photon is missing) | Optimised non-maximally entangled states | This is the brief's model. We also report Eberhard's 2/3 floor as the best case for *any* fallback (17.6 km). |
| D8 | Default detector efficiency 1.0, with sensitivity at 0.9 and 0.8 | Use a realistic 0.8–0.9 default | Generous to the startup so our conclusion cannot be blamed on pessimistic hardware. |
| D9 | Heralded delivery (quantum memories) modelled as a founder-rescue scenario: win = h·p_q + (1−h)·0.75 | Ignore it | Priority note requires it. Shows the loss penalty can be removed in principle; the startup has not claimed memories. |
| D10 | Frontier-map colour rules: grey if window > d/c; else green if η > η*(82%), yellow if η > 2/3, red otherwise | Separate band for ideal maximally-entangled states (8.2 km) | Four regions as the brief specifies; the 8.2 km ideal limit is reported in the text and the E2 figure. |
| D11 | Main-figure title states the conclusion: photon loss or one classical bit beats entanglement on every real route | Neutral descriptive title | Brief requires an executive to get the point without the caption. Memo leads with photon loss per the priority note. |
| D12 | Verified Theorem 10 independently: classical side by brute force over 16 rules with biased inputs; quantum side by optimising four CHSH angles on a maximally entangled state | Trust the closed form | XOR games achieve their quantum value with maximally entangled states and planar measurements (Tsirelson), so the optimiser gives the true value. Both match the closed form to < 1e-6. |
| D13 | Hand re-derivation cell checks the library with relative tolerance 1e-9 | Absolute tolerance 1e-9 | The first run failed on "rounds for $50M" (3.59 million): an absolute 1e-9 tolerance is below float rounding at that magnitude. Not a disagreement in value; the tolerance was the bug, so it was made relative. The pytest expected values were never changed. |
| D14 | All numbers in deliverables come from `results/results.json["display"]` via `scripts/render_deliverables.py`; `scripts/check_numbers.py` fails the build on any untraceable number | Hand-typed numbers | Brief requires writing to pull from results.json. The checker allowlists only citation details (years, volumes, patent and arXiv ids). |
| D15 | "$5B" global latency-arbitrage pool and the 5–10 µs race window are taken from Aquilina, Budish & O'Neill (2022) as given in the brief | Look for other estimates | Brief says cite only listed sources. |
| D16 | PDF route: pandoc → standalone HTML → headless Chromium print-to-PDF | pandoc + LaTeX | No LaTeX engine is installed (xelatex/pdflatex missing); Chromium is preinstalled. |
| D17 | Patent wording: we say US 11676104B2 *describes* the same idea and raise freedom to operate as a question | Assert infringement | We have not read the claims in legal detail; it is a diligence question, not a finding. |
| D18 | No existing PR template found; PR body follows a simple summary / tests layout | — | Nothing to mirror. |
