# Decisions log

Every judgment call made while building this submission: the decision, the alternatives, and why.

| # | Decision | Alternatives considered | Why |
|---|---|---|---|
| D1 | Read the 82% as a win rate on rounds where **both** photons were detected | Read it as an all-rounds rate | On a 40 km link only ~16% of rounds have both photons; under our unheralded fibre model an all-rounds 82% is not reachable on the case's own link spec (E2); the company's denominator and protocol remain unverified (D25). The brief's priority note also says to use this reading unless logs show otherwise. |
| D2 | Read "1,000 trials" as 1,000 scored (coincidence) rounds | 1,000 attempted rounds | Consistent with D1; we report the implied attempted rounds (~6,310) and make it founder question 1. |
| D3 | Read "1,000 pairs/s" as pairs generated at the source | Pairs delivered to both desks | Literal reading of a source spec. Both readings are reported (1.0 h vs 6.3 h of generation for the claimed volume); neither changes the decision. |
| D4 | One-bit boundary uses the vacuum speed of light | Fibre speed (~c/1.47) | Best case for a microwave link and conservative for us (it shrinks the region where quantum could matter). Fibre would move the line by a constant factor; the red region is red on loss grounds regardless. |
| D5 | z-scores use the null-hypothesis standard error √(0.75·0.25/n) | Observed-rate SE | Standard for testing "is this above 75%?"; gives +5.1 and −0.7 as the brief expected. |
| D6 | Sub-ideal source modelled as a singlet mixed with white noise (visibility V = 0.905 for 82%) | Rotated angles, coloured noise | Simplest physically meaningful model that reproduces 82% exactly; the photon-loss result depends only on the 82%, not on the noise model. |
| D7 | Lost-photon fallback = fixed answer 0 (coin-flip rounds when one photon is missing) | Optimised non-maximally entangled states | This is the brief's model. We also report Eberhard's 2/3 floor as the best case for *any* fallback (17.6 km). |
| D8 | Default detector efficiency 1.0, with sensitivity at 0.9 and 0.8 | Use a realistic 0.8–0.9 default | Generous to the startup so our conclusion cannot be blamed on pessimistic hardware. |
| D9 | Heralded delivery (quantum memories) modelled as a founder-rescue scenario: win = h·p_q + (1−h)·0.75 | Ignore it | Priority note requires it. Shows the loss penalty can be removed in principle; the startup has not claimed memories. |
| D10 | Frontier-map colour rules: grey if window > d/c; else green if η > η*(82%), yellow if η > 2/3, red otherwise | Separate band for ideal maximally-entangled states (8.2 km) | Four regions as the brief specifies; the 8.2 km ideal limit is reported in the text and the E2 figure. |
| D11 | Main-figure title states the conclusion: photon loss or one classical bit beats entanglement on every route we checked (originally "every real route"; narrowed in review item 3 and the D25 audit) | Neutral descriptive title | Brief requires an executive to get the point without the caption. Memo leads with photon loss per the priority note. |
| D12 | Verified Theorem 10 independently: classical side by brute force over 16 rules with biased inputs; quantum side by optimising four CHSH angles on a maximally entangled state | Trust the closed form | XOR games achieve their quantum value with maximally entangled states and planar measurements (Tsirelson), so the optimiser gives the true value. Both match the closed form to < 1e-6. |
| D13 | Hand re-derivation cell checks the library with relative tolerance 1e-9 | Absolute tolerance 1e-9 | The first run failed on "rounds for $50M" (3.59 million): an absolute 1e-9 tolerance is below float rounding at that magnitude. Not a disagreement in value; the tolerance was the bug, so it was made relative. The pytest expected values were never changed. |
| D14 | All numbers in deliverables come from `results/results.json["display"]` via `scripts/render_deliverables.py`; `scripts/check_numbers.py` fails the build on any untraceable number | Hand-typed numbers | Brief requires writing to pull from results.json. The checker allowlists only citation details (years, volumes, patent and arXiv ids). |
| D15 | "$5B" global latency-arbitrage pool and the 5–10 µs race window are taken from Aquilina, Budish & O'Neill (2022) as given in the brief | Look for other estimates | Brief says cite only listed sources. |
| D16 | PDF route: pandoc → standalone HTML → headless Chromium print-to-PDF | pandoc + LaTeX | No LaTeX engine is installed (xelatex/pdflatex missing); Chromium is preinstalled. |
| D17 | Patent wording: we say US 11676104B2 *describes* the same idea and raise freedom to operate as a question | Assert infringement | We have not read the claims in legal detail; it is a diligence question, not a finding. |
| D18 | No existing PR template found; PR body follows a simple summary / tests layout | — | Nothing to mirror. |

## Fixes from the independent review (`review/review.md`)

The reviewer re-derived 15 numbers from first principles; all matched `results.json`. Issues and what we did:

| Review item | Valid? | Fix |
|---|---|---|
| 1 [must] Steelman said the herald competes with the winning classical bit | Yes (physics error: the herald precedes the inputs) | Rewrote: heralding is sound physics; the obstacle is memories at trading volume |
| 2 [must] Patent wording ("this exact idea", "same idea") overstated | Yes | Now "titled for / covers coordinating non-communicating parties; claims not compared"; freedom to operate glossed and separated from the strength of the startup's own filings |
| 3 [must] "Every real trading route" rests on three routes | Yes | Figure title, brief, evidence register and steelman now say "every route we checked"; steelman notes we did not survey facilities within a few km |
| 4 [must] Headline premises unstated (82% measured over the 40 km link; desks act on every round) | Yes | Stated inline in the memo, in Limitations, as assumption A17; founder question 1 now asks over what link the 82% was measured |
| 5 [should] "$78M loss" is a straw man; $5B is equities latency arbitrage | Yes | Memo and brief now say the product is worth nothing on that link (a desk would switch the photons off); $78M framed as "used as sold"; $5B called a generous comparator |
| 6 [should] NY–London grey rests on unsourced block-order timing | Yes | Assumption A15 makes it explicit; with a shorter window the route is red and still has no edge |
| 7 [should] Memo first sentence was provenance; experiment cited loosely | Yes | Recommendation is now the first sentence; experiment line (notebook, seed, Monte Carlo size) moved to the end. Notebook filename was correct (`analysis.ipynb`; executed copy also named) |
| 8 [should] Figure: "6 km" vs 5.7 km; yellow mislabelled; red "below 75%"; µs axis label; race label crossed | Yes | All fixed; red now "cannot beat 75%", footnote notes long routes fall back to exactly 75% |
| 9 [should] Lower-loss fibre not considered | Yes | Notebook adds 0.17 dB/km (Ding & Jiang) and hypothetical 0.1 dB/km sensitivity; reported in steelman and assumption A16 |
| 10 [should] Jargon | Yes | Glossed classical, µs, latency arbitrage, freedom to operate, heralding, experiment codes; removed "green zone" from the brief |
| 11 [should] Brief sources omit Ding & Jiang; Liu et al. is computational, not photonic | Yes | Added Ding & Jiang; Liu et al. now described as certified randomness on a quantum computer everywhere |
| 12 [should] Ledger missing valuation and operating-cost rows | Yes | Rows added |
| 13–14 [nit] wording | Yes | "consistent with 75%"; hypothesis section now "the decision survived, the reason changed" |
| 15 [nit] Eberhard "proven lower bound"; NYSE–Nasdaq scoring above 40 km unexplained | Yes | A5 reworded to what Eberhard showed; notebook computes the worst distance (~36 km) and the memo caption explains the drift back toward 75% |
| 16 [nit] Unsourced 80–95% detector figure; landmark distances | Partly | Removed the 80–95% figure; distances remain approximate and are labelled so (A13) |
| Reviewer suggested 0.15 dB/km row | No (not from a listed source) | Used 0.17 dB/km, which Ding & Jiang use, plus an explicitly hypothetical 0.1 dB/km |
| Craddock / Yin pair-rate details | Not verifiable offline | Kept as cited in the brief's source list, without extra claims |

## Open-source release and website

| # | Decision | Alternatives considered | Why |
|---|---|---|---|
| D19 | MIT licence, CITATION.cff, CONTRIBUTING, SECURITY, CODE_OF_CONDUCT (Contributor Covenant 2.1 by reference), CHANGELOG, DISCLOSURE, issue/PR templates, Dependabot, pyproject with ruff + pytest config | Copy QMint's files verbatim | Mirrors the structure of the owner's QMint repository, adapted to this project (no secrets, no hardware, fictional case) |
| D20 | README is rendered from `docs/README.template.md` and checked by `check_numbers.py` | Hand-written README | The README quotes results; the same no-hand-typed-numbers rule applies |
| D21 | Website keeps a no-build static stack (HTML/CSS/vanilla JS) styled with QMint's design tokens, fonts and layout grammar | Port QMint's Next.js/Tailwind stack | Same look with no Node build in CI; `model.js` parity tests stay simple. Numbers load from `results.json` at runtime |
| D22 | Pages deploys from `main` via GitHub Actions (no `gh-pages` branch) | QMint's manual gh-pages publish | The owner asked for a single `main` branch |
| D23 | Single long-lived branch: PR #1 merged into `main`; the owner's earlier parallel attempts `build/autonomous-research` and `build/end-to-end-investigation` (unmerged, overlapping, conflicting) preserved as tags `archive/autonomous-research` and `archive/end-to-end-investigation`, then their branches deleted along with the merged feature branch | Merge them into main; delete without archiving | Merging would duplicate and conflict with the reviewed submission; tags keep every commit recoverable without extra branches |
| D24 | Committed PDFs under `reports/` (build/ stays ignored) | Build PDFs in the Pages workflow | PDF build needs pandoc + Chromium; committing three small PDFs keeps Pages fast and reproducible via `scripts/package.sh` |

## Audit fixes: wording and memo length (docs)

| # | Decision | Alternatives considered | Why |
|---|---|---|---|
| D25 | One fixed formulation for the 64.1% result everywhere: "Under our unheralded fibre model, an 82% coincidence-level source would win about 64.1% of all attempted rounds on a 40 km link. The company's denominator and protocol remain unverified." Replaces "the 82% must be coincidence-selected", "most likely counted only…", "cannot both hold" | Keep the stronger inference | The denominator is an inference from our model, not an observed fact; the claim is now conditional on the model and says what is unverified |
| D26 | One fixed formulation for the distance limit: "The modelled 82% unheralded strategy exceeds the classical baseline only below ~5.7 km, under idealized assumptions (8.2 km ideal; ~17.6 km with optimized partially entangled states)." Replaces "quantum only wins within 5.7 km" and variants | Unqualified "quantum only wins within 5.7 km" | The limit belongs to one modelled strategy under idealized assumptions; heralded strategies have no fixed cutoff |
| D27 | "Every real route" / "real trading route" removed everywhere, including the Phase 1 plan; "every route we checked" used instead | — | We checked three metro routes and New York–London, not every pair of facilities |
| D28 | Memo says the 5–10 µs race figure describes HFT latency arbitrage, not block-order coordination, and that slower block-order decisions favour the classical line (moved from Limitations into the money section) | Leave it only in Limitations | The race window is the most-cited timing in the pitch; the reader needs the caveat where the number is used |
| D29 | Assumption A19: the source-at-one-desk result (≈7.5 km maximally entangled, ≈15.1 km partially entangled, vs 8.2 / 17.6 km at the midpoint) is evidence that the midpoint assumption favours the startup; bound to `endpoint_source_max_km_max_ent` and `endpoint_source_max_km_partial` | State "midpoint favours the startup" without evidence | Turns an asserted "Favours" label into a computed one |
| D30 | README states the limit of the number checker: it traces numbers to `results.json` and binds templated numbers to named keys; it does not prove each number supports the right claim | Say nothing | Avoids overclaiming what CI verifies |
| D31 | Memo cut from 3 to 2 pages by cutting words, not sections: recommendation sentence no longer restates the finding; Limitations no longer repeats the race caveat; Sources condensed to three lines (citation details, not claims); founder questions, figure, hypothesis, reopen, pivot and Limitations sections all kept | Shrink the figure or the font | The brief caps the memo at two pages; the print CSS and figure are unchanged |

### Before / after: headline sentences

| Where | Before | After |
|---|---|---|
| Memo, first sentence | **Recommendation: do not invest $3M at a $25M pre-money valuation.** The physics is real, but under our model of the startup's own setup (photons sent unheralded over fibre, a desk that must act on every round), its two headline numbers, 82% quantum success and a 40 km fibre link, cannot both hold for a trading desk, and no one has named a trade that pays like the game being sold. | **Recommendation: do not invest $3M at a $25M pre-money valuation.** The physics is real, but the evidence does not establish a usable, profitable coordination service for trading desks, and no one has named a trade that pays like the game being sold. |
| Memo, 64.1% sentence | Counting every round, a source of the startup's quality wins **64.1%**, which is *worse* than the free 75% rule. | **Under our unheralded fibre model, an 82% coincidence-level source would win about 64.1% of all attempted rounds on a 40 km link. The company's denominator and protocol remain unverified.** |
| Memo, 5.7 km sentence | To beat 75%, each desk must receive 87.7% of its photons, so the modelled 82% strategy only wins below about **5.7 km** under idealized assumptions (an ideal source: 8.2 km; specially tuned states at Eberhard's floor: 17.6 km). | To beat the free 75% rule each desk needs 87.7% of its photons: **the modelled 82% unheralded strategy exceeds the classical baseline only below ~5.7 km, under idealized assumptions (8.2 km ideal; ~17.6 km with optimized partially entangled states).** |
| Memo, race window | (Limitations) The 5–10 µs race window comes from equity latency arbitrage, a different market from block orders; we use it only as the fastest documented decision time. | (Money section) The 5–10 µs race figure describes HFT latency arbitrage, not block-order coordination; slower block-order decisions favour the classical line. |
| Memo, figure caption lead | *Figure. Distance between desks (across) vs time allowed to decide (up).* | *Figure. On every route we checked, photon loss or one classical bit beats entanglement. Distance between desks (across) vs time to decide (up).* |
| README, recommendation | **Recommendation: do not invest at this valuation.** … Under our specified unheralded fibre and fallback model, an 82% coincidence-level source would achieve about 64.1% across all attempted rounds on a 40 km link, below the free 75% classical rule; the company's measurement denominator and actual protocol remain unverified. The modelled 82% unheralded strategy only exceeds the classical baseline below approximately 5.7 km, under idealized assumptions, and whenever one classical bit can arrive over the desks' line it wins every round. | **Recommendation: do not invest at this valuation.** … Under our unheralded fibre model, an 82% coincidence-level source would win about 64.1% of all attempted rounds on a 40 km link. The company's denominator and protocol remain unverified. That is below the free 75% classical rule. The modelled 82% unheralded strategy exceeds the classical baseline only below ~5.7 km, under idealized assumptions (8.2 km ideal; ~17.6 km with optimized partially entangled states). Whenever one classical bit can arrive over the desks' line it wins every round. |
| Brief, number 1 | **64.1%.** That is the win rate of the startup's 82% source on its own 40 km link, counting every round. | **64.1%.** Our modelled all-rounds win rate for the startup's 82% source on its own 40 km link (unheralded fibre; the company's denominator is unverified). |
| Brief, photon-loss bullet | Under our unheralded fibre model the 82% headline and the 40 km link cannot both hold for a trading desk: an 82% rate on both-photon rounds fits the link, an all-rounds 82% does not, and the startup's denominator is unverified; … | Under our unheralded fibre model, an 82% coincidence-level source would win about 64.1% of all attempted rounds on a 40 km link. The company's denominator and protocol remain unverified. … |
| Brief, usable-zone bullet | The modelled 82% strategy only beats 75% below about 5.7 km and, where no bit can arrive, 19 µs (millionths of a second), under idealized assumptions. Every trading route we checked is red or grey … | The modelled 82% unheralded strategy exceeds the classical baseline only below ~5.7 km, under idealized assumptions (8.2 km ideal; ~17.6 km with optimized partially entangled states). Where no bit can arrive, it is also capped at 19 µs (millionths of a second). Every route we checked is red or grey … |
| Brief, recommendation | **Recommendation: do not invest at this valuation.** | Unchanged |

## Model changes from the external audit

| # | Decision | Why |
|---|---|---|
| D32 | Causality has three states: physically excluded (window < d/c), route-dependent (d/c ≤ window < route latency), classical arrives (window ≥ route latency); default route is straight-line fibre at c/1.47; New York–London uses half the 2015 Hibernia round-trip benchmark (29.5 ms) | The old grey test used d/c, the earliest possible arrival, not the arrival on any real route |
| D33 | Fibre group index changed from 1.468 to 1.47 to match the shared spec; boundaries inclusive at d/c and at route latency | No landmark classification changed (checked before/after) |
| D34 | Heralded fraction capped by link supply (`heralded_supply_fraction`); demand = claimed volume over 252 trading days × 6.5 h | Stops the heralded scenario implying unlimited range; direct transatlantic fibre supplies ~1e-108 |
| D35 | Source-at-one-desk sensitivity (E4b): 7.5 km ideal, 5.4 km at 82%, 15.1 km partially entangled, all below the midpoint figures | The midpoint assumption favours the startup |
| D36 | Agent worktree branches merged into the PR branch; PR left unmerged as instructed; the owner's older `build/*` branches left in place pending a decision | Merge to `main` and branch cleanup were deferred |
