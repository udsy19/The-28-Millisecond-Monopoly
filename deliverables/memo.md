# The Photon That Didn't Show Up

**Recommendation: do not invest $3M at a $25M pre-money valuation.** The physics is real, but the evidence does not establish a usable, profitable coordination service for trading desks, and no one has named a trade that pays like the game being sold.

## What is being sold, and what we tested

The product is a coordination game: two desks each get a yes/no signal and must answer without talking. Entanglement (linked photon pairs shared in advance) lets them coordinate more often than any classical (non-quantum) rule. We rebuilt it in code and tested every case-file number.

- **The physics checks out.** The best rule without communication wins 75% of rounds; the ideal quantum strategy wins 85.4%. The startup's classical demo (74%) is statistically consistent with 75%.
- **But the desks already share a private line.** If there is time to send one bit, a simple classical rule wins 100% of rounds. Quantum only matters when the decision must be faster than light between the desks.

## The finding: photons go missing, and a desk cannot skip rounds

A lab discards rounds where a photon is lost; a trading desk must answer every round and cannot tell whether its partner's photon arrived. On the 40 km link only about 40% of photons reach each desk, so both arrive in just 16% of rounds. **Under our unheralded fibre model, an 82% coincidence-level source would win about 64.1% of all attempted rounds on a 40 km link. The company's denominator and protocol remain unverified.** To beat the free 75% rule each desk needs 87.7% of its photons: **the modelled 82% unheralded strategy exceeds the classical baseline only below ~5.7 km, under idealized assumptions (8.2 km ideal; ~17.6 km with optimized partially entangled states).** Heralded (stored, pre-confirmed) pairs avoid the cutoff but need memories and pair supply the startup has not claimed.

If the 1,000 trials were both-photon rounds, about 6,310 rounds were attempted. A purely classical "cheater" that quietly discards rounds scores exactly 82% with no quantum hardware, so the headline proves nothing without the discard count.

![](../figures/main_frontier.png)

*Figure. On every route we checked, photon loss or one classical bit beats entanglement. Distance between desks (across) vs time to decide (up). Grey: one bit arrives over straight fibre and wins every round; hatched: physics allows a bit but that route is too slow. Red: too many photons lost to beat 75%. Green, where the modelled 82% strategy wins: under 5.7 km and, where no bit can arrive, under 19 µs (millionths of a second). NYSE–Nasdaq scores 65.6% over every round; New York–London is grey above ~29.5 ms (half the Hibernia round trip), route-dependent down to 18.6 ms, red below.*

## The money does not add up either

On the startup's numbers the edge is $13.92 per round, so $50M a year needs 3.59 million rounds. Counting every round on the 40 km link it is **−$21.82 per round**: a desk would switch the photons off and take the free 75%, so the product is worth nothing there (used as sold, it would lose about $78M a year). The ±$100 payoff is the case's invention, and $50M would be 1.0% of the ~$5B a year global equities latency-arbitrage market. The 5–10 µs race figure describes HFT latency arbitrage, not block-order coordination; slower block-order decisions favour the classical line. The edge also vanishes unless each signal fires 29%–71% of the time; no trade has been named.

## Did our hypothesis survive?

**Yes: the decision (pass) survived, but the reason changed.** We expected the shared line to settle it: one bit beats entanglement whenever it can arrive, which rules out New York–London. That leaves a retreat to faster, closer trades; under our unheralded model photon loss closes it, because where the bit cannot arrive the photons do not either. The evidence does not show a usable service, nor disprove every version of one.

## Questions for the founders

1. Over what link, and from how many attempted rounds, were the 1,000 trials scored?
2. What is the end-to-end efficiency per desk (fibre, optics and detectors)?
3. Which real trade has this payoff, and how often is each signal seen?
4. What does the protocol do when one photon is missing?
5. Do you have freedom to operate against the earlier Szegedy, Ding & Shi patent on coordinating non-communicating parties?

## What would reopen the deal

- Logs of *every* attempted round beating 75% between desks too far apart for a bit to arrive in time.
- Heralded delivery with quantum memories and pair supply for the route (not claimed; no help over transatlantic fibre).
- A named trade with signals inside the window and a real P&L payoff, at a research-stage valuation.

## A pivot worth testing (unproven hypothesis)

Entanglement could be the product itself: certified randomness (provably unpredictable numbers, shown on a quantum computer by Liu et al.) or device-independent key distribution. Both still need high photon efficiency but need not beat a classical bit or match a trade. A hypothesis to test, not a proven market.

## Limitations

Our loss model is simple (a desk missing its photon plays a fixed answer); cleverer fallbacks lower the bar, but not past the best case we report (17.6 km). Perfect detectors and a midpoint source are generous to the startup. We modelled fibre only, not satellites. The payoff and $50M claim are the case's own, unchecked against any real trade.

## Sources

- Ding & Jiang, "Coordinating Decisions via Quantum Telepathy," arXiv:2407.21723 (2024).
- Szegedy, Ding & Shi, US Patent 11676104B2; Mermin (1986); Eberhard, Phys. Rev. A 47, R747 (1993).
- Hibernia Express (2015); Aquilina, Budish & O'Neill, QJE 137(1), 2022; Liu et al., Nature 640, 343 (2025).

*Experiment: `analysis.ipynb`, seed 20261119, 1,000,000 Monte Carlo rounds; all numbers from `results/results.json`.*
