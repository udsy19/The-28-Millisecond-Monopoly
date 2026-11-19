# The Photon That Didn't Show Up

*Investment memo, Challenge 03. Every number comes from `analysis.ipynb` via `results/results.json`.*

**Recommendation: do not invest $3M at a $25M pre-money valuation.** The physics is real, but the startup's two headline numbers, 82% quantum success and a 40 km fibre link, cannot both hold for a trading desk, and no one has named a trade that pays like the game being sold.

## What is being sold, and what we tested

The product is a coordination game: two desks each get a yes/no signal and must answer without talking. Entanglement (linked photon pairs shared in advance) lets them coordinate more often than any fixed rule. We rebuilt the game in code and tested every case-file number.

- **The physics checks out.** The best rule without communication wins 75% of rounds; the ideal quantum strategy wins 85.4%. The startup's own classical demo (74%) is a fair baseline: statistically the same as 75%.
- **But the desks already share a private line.** If there is time to send one bit, a simple classical rule wins 100% of rounds. Quantum only matters when the decision must be made faster than light can travel between the desks.

## The finding: photons go missing, and a desk cannot skip rounds

A lab throws away rounds where a photon is lost. A trading desk must answer every round, and it cannot tell whether its partner's photon arrived. On the startup's own 40 km link only about 40% of photons reach each desk, so both arrive in just 16% of rounds. Counting every round, a source of the startup's quality wins **64.1%**, which is *worse* than the free 75% rule. To beat 75%, each desk must receive 87.7% of its photons, which caps the desks at **5.7 km** apart (an ideal source: 8.2 km; the theoretical best case: 17.6 km).

So the 82% was almost certainly counted only on rounds where both photons were detected. If so, its 1,000 trials came from about 6,310 attempted rounds. A purely classical "cheater" that quietly discards some rounds scores exactly 82% with no quantum hardware at all, so the headline proves nothing without the discard count.

![](../figures/main_frontier.png)

*Figure. Distance between desks (across) vs time allowed to decide (up). Grey: one bit arrives in time and wins every round. Red: too many photons lost to beat the classical rule. Green, the only place the startup's quality wins, is under 5.7 km apart and 19 µs. NYSE–Nasdaq scores 65.6% counting every round; New York–London is grey (a bit crosses existing cable in about 29.5 ms).*

## The money does not add up either

On the startup's own numbers the edge is $13.92 per round, so $50M a year needs 3.59 million rounds. Counting every round on the 40 km link, the edge is **−$21.82 per round**; the same volume would lose about $78M a year. The ±$100 payoff is invented by the case, and $50M would be 1.0% of the whole ~$5B a year global latency-arbitrage market. The edge also vanishes unless each desk's signal fires between 29% and 71% of the time; no trade has been named, so nobody knows where a real signal sits.

## Did our hypothesis survive?

**Yes, but for a different reason.** We expected the shared private line to settle it: one classical bit beats entanglement whenever there is time to send it, and that rules out New York–London. True, but incomplete, because the founders could retreat to faster, closer trades. Photon loss closes that retreat: in the only window where the bit cannot arrive in time, the photons do not arrive either.

## Questions for the founders

1. How many attempted rounds produced the 1,000 trials?
2. What is the end-to-end efficiency per desk (fibre, optics and detectors)?
3. Which real trade has this payoff, and how often is each signal seen?
4. What does the protocol do when one photon is missing?
5. Is there freedom to operate given the prior patent on this exact idea (Szegedy, Ding & Shi)?

## What would reopen the deal

- Logs of *every* attempted round showing better than 75% between desks too far apart for a bit to arrive in time.
- Heralded delivery with quantum memories (stored photons plus a signal confirming both arrived): the win rate never drops below 75%. Not claimed by the startup, and no help for New York–London.
- A named trade with signals inside the window and a payoff tied to real profit and loss, at a research-stage valuation.

## A pivot worth testing (unproven hypothesis)

The hardware may suit markets where entanglement *is* the product: certified randomness (provably unpredictable random numbers) or device-independent key distribution (encryption keys secure even on untrusted hardware). These still need high photon efficiency, but they do not have to beat a classical bit or match a trade. A hypothesis to test, not a proven market.

## Limitations

Our loss model is simple (a desk missing its photon plays a fixed answer); cleverer fallbacks lower the bar, but never past the best case we report (17.6 km). Perfect detectors are generous to the startup. We modelled fibre only, not satellites. The payoff and the $50M claim are the case's own and could not be checked against a real trade.

## Sources

- Ding & Jiang, "Coordinating Decisions via Quantum Telepathy," arXiv:2407.21723: NYSE–Nasdaq hedging model, fibre insufficient, the 2/3 efficiency floor, nonuniform-input theorem.
- Szegedy, Ding & Shi, US Patent 11676104B2: coordinating decisions between non-communicating parties.
- Mermin (1986); Eberhard, Phys. Rev. A 47, R747 (1993): 82.8% and 66.7% detection-efficiency thresholds.
- Hibernia Express (2015): New York–London round trip under 58.95 ms.
- Aquilina, Budish & O'Neill, QJE 137(1), 2022: latency races last ~5–10 µs; ~$5B a year globally.
- Liu et al., Nature 640, 343 (2025): certified randomness, 71,313 bits.
