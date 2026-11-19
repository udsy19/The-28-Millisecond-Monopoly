# Evidence register

**Decision:** should we invest $3M at a $25M pre-money valuation ($28M post-money, a 10.7% stake)?
**Our answer:** no, not at this valuation.

How to read this table:
- **Source type.** *Case file* means a claim the startup made to us. *E#* means one of our own experiments in `analysis.ipynb`. All their outputs are in `results/results.json`. *External* means published work.
- **Strength.** This is how far we trust the item *for the investment question*, not whether the science is right.
- **Effect on the decision.** Supports means it helps the startup's case. Against means it hurts it.

Terms used below:
- **CHSH game.** A two-player coordination game. Two desks that cannot talk to each other win at most 75% of rounds with any fixed rule. Shared entangled photons can push that to about 85.4%.
- **Photon loss.** Photons fade in fibre. A desk whose photon never arrived still has to answer that round.
- **Post-selection.** Counting only the rounds where both photons were detected.

## A. Claims in the case file

| # | Claim or evidence item | Source type | What it shows | Strength | Effect on the decision |
|---|---|---|---|---|---|
| A1 | Quantum strategy wins 82% of rounds | Case file | A score above the 75% classical ceiling over 1,000 trials. The file does not say whether lost-photon rounds were counted. | Moderate as physics, weak as a product claim | Neutral until the counting rule is disclosed. See E1, E2, E3. |
| A2 | Classical demo wins 74% | Case file | The startup's own classical baseline. | Strong | Mildly supportive of their honesty: 74% is a fair baseline, not a straw man (E1). |
| A3 | 40 km test link | Case file | The distance their demo ran over. | Strong (a plain fact) | **Strongly against.** At this distance, counting every round, quantum wins less than 75% (E2). |
| A4 | 1,000 entangled pairs per second | Case file | The pair-generation rate. | Moderate | Neutral. The rate is not the bottleneck (E6). |
| A5 | $100 payoff per round won or lost; costs of $0.08 (quantum) and $0.001 (classical) per round | Case file | The startup's own unit economics. | Weak. The payoff is invented and tied to no named trade. | Against. The numbers only work if the 82% holds on every round (E6). |
| A6 | $50M a year revenue target | Case file | Ambition, sized against a $5B pie. | Weak | Against. It is 1.0% of the whole global latency-arbitrage pie (E6). |
| A7 | First product: New York ↔ London (5,570 km) | Case file | The launch route. | Strong (a plain fact) | **Strongly against.** One classical bit over the existing line wins 100% (E1, E4). |
| A8 | Three patent filings | Case file | Claimed intellectual property. | Weak (filings, not grants) | Slightly against. There is a freedom-to-operate question over US Patent 11676104B2 (external, B6). |
| A9 | $3M at $25M pre-money | Case file | Price: 10.7% for $3M. | Strong (a plain fact) | The price assumes a product the evidence does not support. |

## B. Our experiments

| # | Claim or evidence item | Source type | What it shows | Strength | Effect on the decision |
|---|---|---|---|---|---|
| B1 | The classical ceiling is 75% | E1 | We tried every fixed rule. None beats 75%. | Strong (exhaustive check) | Confirms the startup's benchmark is the right one. |
| B2 | 82% is statistically real | E1 | 82% over 1,000 trials sits +5.1 standard errors above 75%. The 74% demo sits -0.7 standard errors from 75% (range 71.3%–76.7%). | Strong, *if* every round was counted | Supports the startup on the lab result only. |
| B3 | One classical bit wins 100% | E1 | If one desk can send a single bit before the other answers, they win every round. | Strong (exact) | **Kills any route where the decision window is longer than the light-travel time**, including New York–London. |
| B4 | **Photon loss on the 40 km link** | E2 | Only 40% of photons reach each desk. Both arrive in only 16% of rounds. Counting every round, the startup's 82% source wins 64.1%; even a perfect source wins 64.7%. Both are below 75%. | Strong. A Monte Carlo that really drops photons matches the formula. | **Lead finding. Strongly against.** The 82% headline and the 40 km link cannot both hold for a trading desk. |
| B5 | Break-even distance | E2 | Each desk needs 87.7% of its photons (82% source) or 82.8% (perfect source). That means desks within 5.7 km or 8.2 km. Even the best-case 2/3 floor allows only 17.6 km. | Strong | Against. Every real trading route is further apart. |
| B6 | Detector sensitivity | E2 | With realistic, slightly imperfect detectors the 82% break-even distance shrinks to 1.1 km. | Strong | Against. Our base case is generous to the startup. |
| B7 | How the 82% was probably counted | E2 | If the 1,000 trials were only rounds where both photons were detected, about 6,310 rounds were attempted. | Moderate (an inference, not a fact) | Against. It is the most likely way to report 82% from this link. We need the raw logs. |
| B8 | Founder rescue: heralding with quantum memories | E2b | If memories store photons and a signal confirms arrival before the round, lost pairs cost nothing. The win rate never drops below 75%, and reaches 82.0% if every round is heralded. On 40 km that leaves about 158 confirmed pairs a second. | Moderate (a model of technology the startup does not have) | Partly supportive in principle. But memories are not claimed, and it does nothing for New York–London. |
| B9 | A classical cheater scores 82% | E3 | With no entanglement, desks that are allowed to drop rounds score 82% on the rounds they keep. They keep 78.1% of rounds and win 75% over all rounds. | Strong (exact) | Against. An 82% alone proves nothing without the count of attempted and discarded rounds. |
| B10 | Frontier map | E4 (`figures/main_frontier.png`) | Quantum only pays within 6 km and under 19 µs. Carteret–Secaucus scores 64.1% and NYSE–Nasdaq 65.6% on every-round accounting. New York–London has 18.6 ms of light-travel time, so a bit gets there first. | Strong | **Strongly against.** No real route is green. |
| B11 | Signals must be balanced | E5 | The edge is 10.4 percentage points at best, with 50/50 signals. It vanishes if a signal fires less than 29% or more than 71% of the time. | Strong (checked against brute force and a numerical optimiser) | Against. No trade has been named, so we cannot check this. |
| B12 | Economics on the startup's terms | E6 | At 82% the edge is $13.92 a round. $50M needs 3.59 million rounds, which is 1.0 hours of delivered rounds or 6.3 hours of generated pairs. | Moderate (payoff invented) | Neutral. Volume and rate are not the problem. |
| B13 | Economics on every-round accounting | E6 | On the 40 km link the edge is −$21.82 a round. At the target volume that is a loss of about $78M a year. | Moderate (payoff invented) | **Strongly against.** |

## C. External sources

| # | Claim or evidence item | Source type | What it shows | Strength | Effect on the decision |
|---|---|---|---|---|---|
| C1 | Ding & Jiang, "Coordinating Decisions via Quantum Telepathy" (preprint) | External (preprint) | A toy NYSE–Nasdaq hedging model at about 56 km. It finds fibre insufficient and gives the 2/3 efficiency floor and the uneven-signals result (Theorem 10) we use in E5. | Moderate (one preprint, not peer reviewed) | Against. Independent authors reach the same fibre conclusion. |
| C2 | Mermin (1986); Eberhard (1993) | External (peer reviewed) | Detection-efficiency thresholds of 82.8% (standard strategy) and 2/3 (best case). | Strong (textbook) | Against. These set the break-even distances in E2. |
| C3 | Yin et al. (2017), Micius satellite | External (peer reviewed) | Entanglement over more than a thousand kilometres, at about 1.1 pairs per second. | Strong | Against for trading. Long distance is possible, but the rate is tiny, and the bit problem (E1) still applies. |
| C4 | Craddock et al. (2024) | External (peer reviewed) | About 5×10⁵ pairs per second over a New York City fibre link close to the startup's distance (see Sources). | Strong | Mixed. Metro rates are fine, but rate does not fix loss on every-round accounting (E2). |
| C5 | Neumann et al. (2022) | External (peer reviewed) | Entanglement distributed over hundreds of kilometres of deployed fibre (see Sources). | Strong | Neutral. It is a distribution result. It does not answer the every-round problem. |
| C6 | Szegedy, Ding & Shi, US patent (see Sources) | External (patent) | An earlier patent on coordinating decisions between parties that cannot communicate. | Moderate | Against. A freedom-to-operate risk for the startup's three filings. |
| C7 | Hibernia Express (2015) | External (industry) | A New York (NY4) to London (LD4) round trip under 58.95 ms, about 29.5 ms one way. | Strong | Against. The desks already have a fast private line, so one bit wins (E1, E4). |
| C8 | Aquilina, Budish & O'Neill (2022) | External (peer reviewed) | Latency races last about 5–10 µs. Latency arbitrage is worth about $5B a year globally. | Strong | Against. The race window sits on our map, but no real route is green at that height (E4). The $50M target is 1.0% of the whole pie (E6). |
| C9 | Liu et al. (2025) | External (peer reviewed) | Certified randomness produced on real hardware (see Sources). | Moderate (as a market signal) | Supports a possible pivot, not this product. |

## Net reading

The lab result may be real. The trading product is not supported. The decisive item is B4: on the startup's own 40 km link, counting every round, quantum loses to the free 75% rule. Everything else (B3, B9, B10, B11, B13) points the same way.

## Sources

- Ding, Y. & Jiang, L. "Coordinating Decisions via Quantum Telepathy." arXiv:2407.21723. NYSE–Nasdaq hedging toy model at 56.3 km; finds fibre insufficient; η ≥ 2/3 floor; Theorem 10 on nonuniform inputs; cites US Patent 11676104B2.
- Szegedy, M., Ding, Y. & Shi, Y. US Patent 11676104B2, coordinating decisions between non-communicating parties.
- Mermin, N. D. (1986); Eberhard, P. H., Phys. Rev. A 47, R747 (1993). Detection-efficiency thresholds of 82.8% and 66.7%.
- Yin, J. et al., Science 356, 1140 (2017). Micius satellite, 1,203 km, ~1.1 pairs/s.
- Craddock, A. N. et al., PRX Quantum 5, 030330 (2024). ~5×10⁵ pairs/s over 34 km of New York City fibre.
- Neumann, S. P. et al. (2022). Entanglement distribution over 248 km of deployed fibre.
- Hibernia Express (2015). NY4–LD4 round trip under 58.95 ms.
- Aquilina, M., Budish, E. & O'Neill, P., QJE 137(1) (2022). Races ~5–10 µs; ~$5B/yr globally.
- Liu, M. et al., Nature 640, 343 (2025). Certified randomness, 71,313 bits.
