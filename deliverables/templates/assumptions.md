# Modelling assumptions

Each assumption, why it is reasonable, and whom it favours. "Startup" means the assumption makes the startup look better than reality probably would; "us" means it strengthens our case against investing.

| # | Assumption | Why it is reasonable | Favours |
|---|---|---|---|
| A1 | The game is standard CHSH with uniform, independent input bits | That is how the case file defines it | Neutral (E5 relaxes it) |
| A2 | Ideal quantum win rate is {{ideal_q}} (Tsirelson bound); the startup's source quality is {{p_claim}} when both photons arrive | Textbook physics; we read the {{p_claim}} as a coincidence-only rate | Startup (we credit them the full {{p_claim}}) |
| A3 | Source quality below ideal is modelled as white noise mixed into a perfect singlet | Standard, simple noise model; reproduces {{p_claim}} exactly | Neutral |
| A4 | Photons reach each desk independently with efficiency η; a desk whose photon is lost plays the fixed answer 0 | A trading desk must answer every round and cannot see its partner's detector | Us, slightly: smarter fallbacks exist, so we also report the best-case floor |
| A5 | Best case for any fallback is Eberhard's 2/3 efficiency floor ({{dmax_floor}} maximum separation) | Proven lower bound for any CHSH-type test; needs near-perfect non-maximally entangled states | Startup (it is unreachable in practice) |
| A6 | Fibre loss 0.2 dB/km; source at the midpoint so each photon travels half the distance | Standard telecom fibre; midpoint placement minimises the worst arm | Startup (lowest-loss geometry) |
| A7 | Perfect detectors (efficiency 1.0) by default; sensitivity at 0.9 and 0.8 | Real detectors are below 1; at 0.9 the green zone shrinks to {{dmax_82_det09}} | Startup |
| A8 | One classical bit travels at the vacuum speed of light | Best case for a line-of-sight microwave link; fibre is about a third slower | Us, slightly (fibre would widen the region where quantum could matter) — but that region is already red on loss grounds |
| A9 | The 5–10 µs window from Aquilina, Budish & O'Neill is the relevant race timescale | Only published measurement of latency-race duration | Neutral |
| A10 | {{pair_rate}} pairs/s means pairs *generated* at the source; only the both-arrive share is usable | Literal reading of a source specification | Us (alternative reading: delivered pairs, {{hours_delivered}} instead of {{hours_generated}}; neither changes the decision) |
| A11 | Payoff ±{{payoff}} per round, costs {{cost_q}} and {{cost_c}} per round, as given | The case defines them; we flag them as invented | Startup (no real trade is shown to pay like this) |
| A12 | Heralded delivery (quantum memories) is a founder-rescue scenario only | Not claimed by the startup; memories at trading-desk scale are not commercial | Startup (we model it anyway) |
| A13 | Distances are approximate straight-line figures (Carteret–Secaucus ~32 km, NYSE–Nasdaq ~56 km, New York–London ~5,570 km) | Real fibre routes are longer | Startup (longer routes lose more photons) |
| A14 | Fixed random seed {{seed}}; {{n_mc}} Monte Carlo rounds per simulation | Reproducibility; Monte Carlo agrees with the formulas to within {{mc_err}} | Neutral |
