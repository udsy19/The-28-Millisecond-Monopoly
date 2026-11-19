# Modelling assumptions

Each assumption, why it is reasonable, and whom it favours. "Startup" means the assumption makes the startup look better than reality probably would; "us" means it strengthens our case against investing.

| # | Assumption | Why it is reasonable | Favours |
|---|---|---|---|
| A1 | The game is standard CHSH with uniform, independent input bits | That is how the case file defines it | Neutral (E5 relaxes it) |
| A2 | Ideal quantum win rate is 85.4% (Tsirelson bound); the startup's source quality is 82% when both photons arrive | Textbook physics; we read the 82% as a coincidence-only rate | Startup (we credit them the full 82%) |
| A3 | Source quality below ideal is modelled as white noise mixed into a perfect singlet | Standard, simple noise model; reproduces 82% exactly | Neutral |
| A4 | Photons reach each desk independently with efficiency η; a desk whose photon is lost plays the fixed answer 0 | A trading desk must answer every round and cannot see its partner's detector | Us, slightly: smarter fallbacks exist, so we also report the best-case floor |
| A5 | Best case for any fallback is Eberhard's 2/3 efficiency floor (17.6 km maximum separation) | Eberhard showed such tests can work down to 2/3 with specially tuned (non-maximally entangled) states and near-perfect hardware; we treat it as the floor | Startup (it is unreachable in practice) |
| A6 | Fibre loss 0.2 dB/km; source at the midpoint so each photon travels half the distance | Standard telecom fibre; midpoint placement minimises the worst arm | Startup (lowest-loss geometry) |
| A7 | Perfect detectors by default; sensitivity at efficiencies 1.0, 0.9, 0.8 | Real detectors are below perfect; at the middle level the green zone shrinks to 1.1 km | Startup |
| A8 | Three causal states for one classical bit: physically excluded below d/c (vacuum light), route-dependent up to a straight-line fibre route at c/1.468, arrives above it; New York–London uses half the Hibernia round-trip benchmark (29.5 ms) | Separates what physics forbids from what a particular route delivers; the Hibernia figure is a 2015 round-trip claim, not a measured one-way service | Startup (straight-line fibre is faster than any real cable, so the route-dependent band is as narrow as it can be) |
| A9 | The 5–10 µs window from Aquilina, Budish & O'Neill is shown only as the fastest documented decision timescale | It measures equity latency-arbitrage races, a different market from block orders; it does not establish demand for this product | Neutral |
| A10 | 1,000 pairs/s means pairs *generated* at the source; only the both-arrive share is usable | Literal reading of a source specification | Us (alternative reading: delivered pairs, 1.0 hours instead of 6.3 hours; neither changes the decision) |
| A11 | Payoff ±$100 per round, costs $0.08 and $0.001 per round, as given | The case defines them; we flag them as invented | Startup (no real trade is shown to pay like this) |
| A12 | Heralded delivery (quantum memories) is a founder-rescue scenario only | Not claimed by the startup; memories at trading-desk scale are not commercial | Startup (we model it anyway) |
| A13 | Distances are approximate straight-line figures (Carteret–Secaucus ~32 km, NYSE–Nasdaq ~56 km, New York–London ~5,570 km) | Real fibre routes are longer | Startup (longer routes lose more photons) |
| A14 | Fixed random seed 20261119; 1,000,000 Monte Carlo rounds per simulation | Reproducibility; Monte Carlo agrees with the formulas to within 0.02 percentage points | Neutral |
| A15 | No decision window is stated for New York–London block orders, so we report all three causal states | If the window exceeds 29.5 ms the bit wins; if it is shorter, direct-fibre loss leaves quantum at 75% | Neutral: no edge either way |
| A16 | Fibre loss sensitivity: 0.17 dB/km (Ding & Jiang) gives 6.7 km at 82% and 20.7 km best case; a hypothetical 0.1 dB/km fibre gives 11.4 km and 35.2 km | Shows how much better glass would buy | Neutral (reported, not assumed) |
| A18 | Heralded demand is the claimed volume spread over one trading year (252 days × 6.5 hours): 0.61 rounds per second | Converts the $50M claim into a rate the link must supply | Startup (perfect, lossless memories assumed) |
| A17 | The 82% was measured over the 40 km test link, and a trading desk must act on every round | The case file presents the link as the startup's test link; a desk cannot un-trade a round | Us (if the 82% came from a shorter bench setup, our link result still stands but the 82% says less about the link) |
