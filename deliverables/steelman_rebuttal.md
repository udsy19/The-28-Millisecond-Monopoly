# Steelman and rebuttal

This is the strongest honest case the founders could make, argument by argument. After each one we give our rebuttal and the experiment behind it. Where part of their case survives, we say so.

The experiments are in `analysis.ipynb`. Every number is from `results/results.json`.

Terms used below:
- **CHSH game.** A two-desk coordination game. Without talking, the desks win at most 75% of rounds. Shared entangled photons can do better.
- **Every-round accounting.** Counting every round the desks play, including rounds where a photon got lost. A trading desk has to answer every round.
- **Heralding.** A signal that tells the desks a pair has arrived before they use it.

---

## "Our 82% is real. It is +5.1 standard errors above 75%."

**Steelman.** Over 1,000 trials, 82% cannot be luck. The classical demo scored 74%, so the comparison is honest. Real quantum correlation was seen on a real 40 km link.

**Rebuttal (E1, E2, E3).** We agree the number is unlikely to be luck (E1). The question is what was counted. On the 40 km link only 40% of photons reach each desk, and both arrive in only 16% of rounds. Under our unheralded fibre model, an 82% coincidence-level source would win about 64.1% of all attempted rounds on a 40 km link. The company's denominator and protocol remain unverified. That is below the free 75% rule (E2). If the 82% was counted only on rounds where both photons were detected, about 6,310 rounds were attempted to get the 1,000 that were scored (E2). A desk cannot throw rounds away like that. Also, a purely classical "cheater" that may drop rounds scores exactly 82% on the rounds it keeps (E3). So the headline alone cannot tell real entanglement from a classical trick.

**What survives.** The physics may be fine. If the raw logs show every attempted round, the 82% is good evidence of a working source. It is still not evidence of a trading product.

## "Detectors and fibre will get better."

**Steelman.** Detectors improve every year. Low-loss fibre is coming. The loss problem is an engineering problem, and engineering problems get solved.

**Rebuttal (E2, E4).** Fibre loss grows with distance, and better detectors cannot undo it. Even with perfect detectors, an 82% source needs each desk to receive 87.7% of its photons. A perfect source needs 82.8%. The modelled 82% unheralded strategy exceeds the classical baseline only below ~5.7 km, under idealized assumptions (8.2 km ideal; ~17.6 km with optimized partially entangled states). (E2) Every route we checked is further apart: Carteret–Secaucus scores 64.1% and NYSE–Nasdaq 65.6% on every-round accounting (E4). With realistic, slightly imperfect detectors the 82% limit falls to 1.1 km (E2). Improvements move the edge of the green zone on our map. They do not reach the 40 km test link.

**What survives.** Not on the routes we checked (32–56 km). Better fibre helps but slowly: at 0.17 dB/km (the figure Ding & Jiang use) the 82% source reaches 6.7 km and the best case 20.7 km; even a hypothetical 0.1 dB/km fibre only gets the best case to 35.2 km, just past Carteret–Secaucus, with near-perfect tuned states and perfect detectors. We did not survey every pair of facilities within a few kilometres of each other.

## "Quantum memories and heralding fix photon loss."

**Steelman.** Store each photon in a quantum memory. Send a signal confirming both arrived. Then the desks know in advance which rounds to play quantum. Lost pairs cost nothing.

**Rebuttal (E2b, E1, E4).** This is the best rescue argument, and our model agrees it works on paper. With heralding, the win rate never drops below 75%, and with every round heralded it reaches 82.0% (E2b). On the 40 km link that leaves about 158 confirmed pairs a second. But:
- The startup has not claimed quantum memories. They are not yet commercial at trading-desk scale.
- Heralding is real physics: the confirmation is sent *before* the inputs exist, so it does not compete with the race. But the desks then need memories that hold a photon until the round arrives, at trading volumes, and nobody sells that today.
- It does nothing for New York–London, the first product (E4).

**What survives.** Partly. Heralding changes *which* product could work. A future company with memories, on a short metro route, might have something. That is a different company from the one we are being asked to fund at $25M.

## "Forget London. Sell short metro links."

**Steelman.** Most exchange data centres sit tens of kilometres apart. Latency races last 5–10 µs (Aquilina, Budish & O'Neill, 2022). In that window no classical bit can cross. That is where quantum wins.

**Rebuttal (E4, E2).** The 5–10 µs figure describes HFT latency arbitrage, not block-order coordination; slower block-order decisions favour the classical line. Even taking the window as given, the distances are wrong. On our main figure (`figures/main_frontier.png`) the race band is mostly red. The modelled 82% unheralded strategy exceeds the classical baseline only below ~5.7 km, under idealized assumptions (8.2 km ideal; ~17.6 km with optimized partially entangled states). Where no bit can arrive, the green zone is also capped at 19 µs (E4). Carteret–Secaucus scores 64.1% and NYSE–Nasdaq 65.6% on every-round accounting. Both are below 75%. Ding & Jiang reach the same verdict for NYSE–Nasdaq at about 56 km: fibre is not enough. The startup's own 40 km link is red too.

**What survives.** A green zone exists, but it is a few kilometres wide. We know of no pair of competing trading sites inside it. Naming two such venues whose desks must coordinate without communicating is a question for the founders.

## "Real trading signals give a bigger edge than the textbook game."

**Steelman.** The textbook game uses 50/50 inputs. Ding & Jiang (Theorem 10) show the game generalises to uneven inputs. Real trades might be a better fit.

**Rebuttal (E5).** Uneven inputs make the edge smaller, not bigger. The quantum edge is largest with perfectly balanced signals: 10.4 percentage points. It disappears completely if a signal fires less than 29% or more than 71% of the time (E5). We checked this against a brute-force classical search and a numerical quantum optimiser. The startup has not named a trade, so we cannot say where a real signal falls.

**What survives.** If a real trade has balanced signals, the edge is there, *before* photon loss. Photon loss (E2) still applies on top.

## "We have patents, and the team built a working link."

**Steelman.** Three patent filings and a running 40 km demo. That is a rare asset and a moat.

**Rebuttal (E2, and item C6 in the evidence register).** Filings are not grants. US Patent 11676104B2 (Szegedy, Ding & Shi) describes coordinating decisions between parties that cannot communicate. That raises a freedom-to-operate question for all three filings. And the demo link is the one where every-round accounting loses (E2).

**What survives.** The team is real and the hardware skill is real. That has value, but in a different product (see the pivot in `one_page_brief.md`).

## "Satellites solve distance."

**Steelman.** Micius distributed entanglement over more than a thousand kilometres (Yin et al., 2017). Satellites skip fibre loss. That is the route to New York–London.

**Rebuttal (E1, E4, E6).** Micius delivered about 1.1 pairs a second. More importantly, distance is not the only problem. New York–London has 18.6 ms of light-travel time, and the existing private line delivers a bit in about 29.5 ms one way (Hibernia Express). Any decision window longer than that lets one bit win 100% (E1, E4). A satellite moves photons, not the speed of light, so it does not change the one-bit problem. The startup would also need memories and heralding (see the heralding argument above) to cope with the low pair rate.

**What survives.** Nothing for trading.

## "$50M a year is modest."

**Steelman.** At $13.92 a round, $50M needs only 3.59 million rounds a year. That is 1.0 hours of delivered rounds. The rate is not a constraint.

**Rebuttal (E6).** We agree the rate is fine (E6). But $50M is 1.0% of the whole global latency-arbitrage pie of about $5B a year, won by a game whose payoff is tied to no named trade. And on every-round accounting on the 40 km link, the edge is −$21.82 a round. At the same volume that loses about $78M a year (E6).

**What survives.** The arithmetic holds only if the 82% holds on every round. It does not on the startup's own link.

---

## Bottom line

The strongest surviving argument is heralding with quantum memories. It is real physics, but the startup has not claimed it and it does not save the first product. Everything else falls to photon loss (E2), the one-bit argument (E1), or both.

## Sources

- Ding & Jiang, "Coordinating Decisions via Quantum Telepathy," arXiv:2407.21723 (NYSE–Nasdaq toy model at 56.3 km; Theorem 10).
- Szegedy, Ding & Shi, US Patent 11676104B2.
- Eberhard, Phys. Rev. A 47, R747 (1993) (66.7% threshold).
- Yin et al., Science 356, 1140 (2017) (Micius, 1,203 km, ~1.1 pairs/s).
- Hibernia Express (2015) (NY4–LD4 round trip under 58.95 ms).
- Aquilina, Budish & O'Neill, QJE 137(1) (2022) (races ~5–10 µs; ~$5B/yr).
