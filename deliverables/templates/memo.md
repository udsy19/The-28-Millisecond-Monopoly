# The Photon That Didn't Show Up

**Recommendation: do not invest {{investment}} at a {{pre_money}} pre-money valuation.** The physics is real, but the startup's two headline numbers, {{p_claim}} quantum success and a {{link_km}} fibre link, cannot both hold for a trading desk, and no one has named a trade that pays like the game being sold.

## What is being sold, and what we tested

The product is a coordination game: two desks each get a yes/no signal and must answer without talking. Entanglement (linked photon pairs shared in advance) lets them coordinate more often than any classical (ordinary, non-quantum) rule. We rebuilt the game in code and tested every case-file number.

- **The physics checks out.** The best rule without communication wins {{classical_max}} of rounds; the ideal quantum strategy wins {{ideal_q}}. The startup's own classical demo ({{p_demo}}) is a fair baseline, statistically consistent with {{classical_max}}.
- **But the desks already share a private line.** If there is time to send one bit, a simple classical rule wins {{one_bit}} of rounds. Quantum only matters when the decision must be made faster than light can travel between the desks.

## The finding: photons go missing, and a desk cannot skip rounds

A lab throws away rounds where a photon is lost. A trading desk must answer every round, and it cannot tell whether its partner's photon arrived. On the startup's own {{link_km}} link only about {{eta_40_pct}} of photons reach each desk, so both arrive in just {{both_share}} of rounds. Counting every round, a source of the startup's quality wins **{{win40_82}}**, which is *worse* than the free {{classical_max}} rule. To beat {{classical_max}}, each desk must receive {{eta_star_82}} of its photons, which caps the desks at **{{dmax_82}}** apart (an ideal source: {{dmax_ideal}}; the theoretical best case: {{dmax_floor}}).

So, if the {{p_claim}} was measured over this test link and a desk must act on every round (our two premises), it was most likely counted only on rounds where both photons were detected. If so, its {{n_trials}} trials came from about {{attempted}} attempted rounds. A purely classical "cheater" that quietly discards some rounds scores exactly {{cheat_det}} with no quantum hardware at all, so the headline proves nothing without the discard count.

![](../figures/main_frontier.png)

*Figure. Distance between desks (across) vs time allowed to decide (up). Grey: one bit arrives in time and wins every round. Red: too many photons lost to beat the classical rule. Green, the only place the startup's quality wins, is under {{dmax_82}} apart and {{green_us}} (millionths of a second). NYSE–Nasdaq scores {{nasdaq_win}} counting every round (slightly above the 40 km link: past about {{worst_km}} both photons are usually lost and the desks drift back toward the classical rule); New York–London is grey (a bit crosses existing cable in about {{hibernia_one_way}}).*

## The money does not add up either

On the startup's own numbers the edge is {{edge_claim}} per round, so {{target}} a year needs {{rounds}} rounds. Counting every round on the {{link_km}} link, the edge is **{{edge_all_82}} per round**: a desk would switch the photons off and take the free {{classical_max}}, so the product is worth nothing there (used as sold, it would lose about {{annual_loss}} a year). The ±{{payoff}} payoff is invented by the case, and {{target}} of profit would be {{share_pool}} of the ~{{global_pool}} a year global equities latency-arbitrage market (traders profiting from being microseconds faster), a generous comparator for block orders. The edge also vanishes unless each desk's signal fires between {{adv_lo_pct}} and {{adv_hi_pct}} of the time; no trade has been named, so nobody knows where a real signal sits.

## Did our hypothesis survive?

**Yes: the decision (pass) survived, but the reason changed.** We expected the shared private line to settle it: one classical bit beats entanglement whenever there is time to send it, which rules out New York–London. That alone leaves the founders a retreat to faster, closer trades. Photon loss closes it: in the only window where the bit cannot arrive in time, the photons do not arrive either.

## Questions for the founders

1. Over what link, and from how many attempted rounds, were the {{n_trials}} trials scored?
2. What is the end-to-end efficiency per desk (fibre, optics and detectors)?
3. Which real trade has this payoff, and how often is each signal seen?
4. What does the protocol do when one photon is missing?
5. Can you sell without licensing the earlier patent on coordinating non-communicating parties (Szegedy, Ding & Shi), i.e. do you have freedom to operate?

## What would reopen the deal

- Logs of *every* attempted round showing better than {{classical_max}} between desks too far apart for a bit to arrive in time.
- Heralded delivery with quantum memories (stored photons plus a signal confirming both arrived): the win rate never drops below {{classical_max}}. Not claimed by the startup, and no help for New York–London.
- A named trade with signals inside the window and a payoff tied to real profit and loss, at a research-stage valuation.

## A pivot worth testing (unproven hypothesis)

The hardware may suit markets where entanglement *is* the product: certified randomness (provably unpredictable random numbers, already shown on a quantum computer by Liu et al.) or device-independent key distribution (encryption keys secure even on untrusted hardware). These still need high photon efficiency, but they do not have to beat a classical bit or match a trade. A hypothesis to test, not a proven market.

## Limitations

Our loss model is simple (a desk missing its photon plays a fixed answer); cleverer fallbacks lower the bar, but never past the best case we report ({{dmax_floor}}). Perfect detectors are generous to the startup. We modelled fibre only, not satellites. Our headline rests on the two premises stated above. The payoff and the {{target}} claim are the case's own and could not be checked against a real trade.

## Sources

- Ding & Jiang, "Coordinating Decisions via Quantum Telepathy," arXiv:2407.21723: NYSE–Nasdaq hedging model, fibre insufficient, the 2/3 efficiency floor, nonuniform-input theorem.
- Szegedy, Ding & Shi, US Patent 11676104B2: coordinating decisions between non-communicating parties.
- Mermin (1986); Eberhard, Phys. Rev. A 47, R747 (1993): 82.8% and 66.7% detection-efficiency thresholds.
- Hibernia Express (2015): New York–London round trip under 58.95 ms.
- Aquilina, Budish & O'Neill, QJE 137(1), 2022: latency races last ~5–10 µs; ~$5B a year globally.
- Liu et al., Nature 640, 343 (2025): certified randomness on a quantum computer, 71,313 bits.

*Experiment: `analysis.ipynb` (executed copy `analysis_executed.html`), fixed seed {{seed}}, {{n_mc}} simulated rounds per Monte Carlo check; every number above is read from `results/results.json`.*
