# The Photon That Didn't Show Up

*Investment memo, Challenge 03. Every number comes from `analysis.ipynb` via `results/results.json`.*

**Recommendation: do not invest {{investment}} at a {{pre_money}} pre-money valuation.** The physics is real, but the startup's two headline numbers, {{p_claim}} quantum success and a {{link_km}} fibre link, cannot both hold for a trading desk, and no one has named a trade that pays like the game being sold.

## What is being sold, and what we tested

The product is a coordination game: two desks each get a yes/no signal and must answer without talking. Entanglement (linked photon pairs shared in advance) lets them coordinate more often than any fixed rule. We rebuilt the game in code and tested every case-file number.

- **The physics checks out.** The best rule without communication wins {{classical_max}} of rounds; the ideal quantum strategy wins {{ideal_q}}. The startup's own classical demo ({{p_demo}}) is a fair baseline: statistically the same as {{classical_max}}.
- **But the desks already share a private line.** If there is time to send one bit, a simple classical rule wins {{one_bit}} of rounds. Quantum only matters when the decision must be made faster than light can travel between the desks.

## The finding: photons go missing, and a desk cannot skip rounds

A lab throws away rounds where a photon is lost. A trading desk must answer every round, and it cannot tell whether its partner's photon arrived. On the startup's own {{link_km}} link only about {{eta_40_pct}} of photons reach each desk, so both arrive in just {{both_share}} of rounds. Counting every round, a source of the startup's quality wins **{{win40_82}}**, which is *worse* than the free {{classical_max}} rule. To beat {{classical_max}}, each desk must receive {{eta_star_82}} of its photons, which caps the desks at **{{dmax_82}}** apart (an ideal source: {{dmax_ideal}}; the theoretical best case: {{dmax_floor}}).

So the {{p_claim}} was almost certainly counted only on rounds where both photons were detected. If so, its {{n_trials}} trials came from about {{attempted}} attempted rounds. A purely classical "cheater" that quietly discards some rounds scores exactly {{cheat_det}} with no quantum hardware at all, so the headline proves nothing without the discard count.

![](../figures/main_frontier.png)

*Figure. Distance between desks (across) vs time allowed to decide (up). Grey: one bit arrives in time and wins every round. Red: too many photons lost to beat the classical rule. Green, the only place the startup's quality wins, is under {{dmax_82}} apart and {{green_us}}. NYSE–Nasdaq scores {{nasdaq_win}} counting every round; New York–London is grey (a bit crosses existing cable in about {{hibernia_one_way}}).*

## The money does not add up either

On the startup's own numbers the edge is {{edge_claim}} per round, so {{target}} a year needs {{rounds}} rounds. Counting every round on the {{link_km}} link, the edge is **{{edge_all_82}} per round**; the same volume would lose about {{annual_loss}} a year. The ±{{payoff}} payoff is invented by the case, and {{target}} would be {{share_pool}} of the whole ~{{global_pool}} a year global latency-arbitrage market. The edge also vanishes unless each desk's signal fires between {{adv_lo_pct}} and {{adv_hi_pct}} of the time; no trade has been named, so nobody knows where a real signal sits.

## Did our hypothesis survive?

**Yes, but for a different reason.** We expected the shared private line to settle it: one classical bit beats entanglement whenever there is time to send it, and that rules out New York–London. True, but incomplete, because the founders could retreat to faster, closer trades. Photon loss closes that retreat: in the only window where the bit cannot arrive in time, the photons do not arrive either.

## Questions for the founders

1. How many attempted rounds produced the {{n_trials}} trials?
2. What is the end-to-end efficiency per desk (fibre, optics and detectors)?
3. Which real trade has this payoff, and how often is each signal seen?
4. What does the protocol do when one photon is missing?
5. Is there freedom to operate given the prior patent on this exact idea (Szegedy, Ding & Shi)?

## What would reopen the deal

- Logs of *every* attempted round showing better than {{classical_max}} between desks too far apart for a bit to arrive in time.
- Heralded delivery with quantum memories (stored photons plus a signal confirming both arrived): the win rate never drops below {{classical_max}}. Not claimed by the startup, and no help for New York–London.
- A named trade with signals inside the window and a payoff tied to real profit and loss, at a research-stage valuation.

## A pivot worth testing (unproven hypothesis)

The hardware may suit markets where entanglement *is* the product: certified randomness (provably unpredictable random numbers) or device-independent key distribution (encryption keys secure even on untrusted hardware). These still need high photon efficiency, but they do not have to beat a classical bit or match a trade. A hypothesis to test, not a proven market.

## Limitations

Our loss model is simple (a desk missing its photon plays a fixed answer); cleverer fallbacks lower the bar, but never past the best case we report ({{dmax_floor}}). Perfect detectors are generous to the startup. We modelled fibre only, not satellites. The payoff and the {{target}} claim are the case's own and could not be checked against a real trade.

## Sources

- Ding & Jiang, "Coordinating Decisions via Quantum Telepathy," arXiv:2407.21723: NYSE–Nasdaq hedging model, fibre insufficient, the 2/3 efficiency floor, nonuniform-input theorem.
- Szegedy, Ding & Shi, US Patent 11676104B2: coordinating decisions between non-communicating parties.
- Mermin (1986); Eberhard, Phys. Rev. A 47, R747 (1993): 82.8% and 66.7% detection-efficiency thresholds.
- Hibernia Express (2015): New York–London round trip under 58.95 ms.
- Aquilina, Budish & O'Neill, QJE 137(1), 2022: latency races last ~5–10 µs; ~$5B a year globally.
- Liu et al., Nature 640, 343 (2025): certified randomness, 71,313 bits.
