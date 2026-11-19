# Phase 1: Decision hypothesis and experiment plan

**Decision.** Should we invest {{investment}} at a {{pre_money}} pre-money valuation (about {{stake}} of the company) in a startup selling entanglement-based coordination between trading desks, starting with block orders between New York and London?

**Initial hypothesis: pass.** The two desks already share a private low-latency line. If one desk sends a single bit over it before answering, a simple classical rule wins every round of the game, beating any quantum strategy. Entanglement can only help when the decision must be made faster than that bit can travel, and New York–London is the slowest possible place to need that.

**The uncertainty that matters most.** Is there any regime where the bit *cannot* arrive in time *and* entangled photons *can* be delivered there with enough efficiency? If such a regime exists and contains real trades, the startup has a product (just not the one it is pitching). If not, the case closes.

**Plan (each experiment is a notebook section with code and tests).**

| # | Experiment | Question it answers |
|---|---|---|
| E1 | Brute-force all 16 classical rules; z-scores for the {{p_claim}} and {{p_demo}} claims; simulate the quantum strategy; check the one-bit rule | Is the physics claim real and the demo statistically meaningful? |
| E2 | Photon-loss model on fibre, with a Monte Carlo that actually drops photons; detector sensitivity; heralded-delivery rescue case | Does the advantage survive when a desk must answer every round? |
| E3 | Classical "cheater" that discards rounds | Can a quantum-looking score be faked without quantum hardware? |
| E4 | Frontier map: desk distance × decision window (main figure) | Where, if anywhere, can quantum pay? Where do the routes we check fall? |
| E5 | Biased signals (Ding & Jiang, Theorem 10) | Does the edge survive signals that aren't 50/50? |
| E6 | Economics of the claimed {{target}} | Does the business case hold on the startup's own numbers? |

**Evidence that would change my mind.**
- A logged all-rounds win rate (no discarded rounds) above {{classical_max}}, at a desk separation where one bit cannot arrive in time.
- Measured end-to-end photon efficiency per desk high enough to clear the break-even level E2 computes.
- A named trade whose payoff and signal frequencies resemble the game, or a credible quantum-memory roadmap that removes the photon-loss penalty.
