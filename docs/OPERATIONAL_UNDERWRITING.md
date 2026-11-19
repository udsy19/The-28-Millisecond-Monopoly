# Operational underwriting: try to make the founders right

**Status:** optimistic scenario analysis, not a validated customer, transatlantic service, or trading return.

## Why this is a hard test
We first assume (1) the startup really wins 82% of fully scored uniform CHSH rounds, (2) each successful *usable* distributed pair powers one independent customer decision, (3) every pair surviving the ideal direct optical channel works at the claimed win rate, (4) the customer needs up to four million decisions per year, and (5) all 31,536,000 seconds of the year can be used. These generous concessions ignore detector loss, heralding, storage, network outages and capital costs. For rounds with no available pair, the customer can still use the optimal classical no-message policy.

This reveals an important distinction. A pair *sent* through fibre is not automatically an actionable CHSH decision. The simulated rate and conditional dollars are **ceilings on an artificial game**, not the realised opportunity.

## What would make the business real?
A trading desk would need to prove:
- Two genuinely independent local inputs become known only after any shared resource is established, with a binding deadline and meaningful joint payoff.
- The outputs may be computed locally without later communication, and the action can be committed without defeating the trading/settlement constraints.
- The market payoff is equivalent to (or provably bounded by) the CHSH-style payoff and survives the best pre-shared-randomness and fastest-communication classical alternatives.
- Usable quantum pairs have been delivered, heralded, validated and held **before** the live inputs, with adequate lifetime, throughput and uptime.
- The chosen route is compared against the fastest possible alternative, not merely a particular 2015 cable.

## Experiment
Run `make check`. Inspect `artifacts/underwriting.json`, `artifacts/tables/operational_scenarios.csv`, and `artifacts/OPERATIONS_APPENDIX.md`. The sensitivity includes 40, 160, 200 and 5,600 km, with both source-rate interpretations. An approximately 197 km best-case unrepeated optical distance can support *the hypothetical pair volume* for the $50M referee-game claim under the 1,000/s source scenario; it **does not** guarantee any profit or viable causality window.

## How the founder could rescue the claim
A quantum-memory inventory, repeater chain, satellite network or nearer paired market may change the engineering math. The simple direct-fibre loss bound cannot rule those out. Ask for deployed usable-pair logs, independent Bell certification, availability distributions, full capex/opex and an actual customer contract. We would actively revise the decision if all three independent physics, network and market gates were satisfied.

## Further research leads
- MIT Quantum Index Report 2026, Chapter 9 (technology and application-specific readiness): https://qir.mit.edu/networking/
- Nature, 2026, long-lived 10 km ion-memory entanglement: https://www.nature.com/articles/s41586-026-10177-4
- PRL 2023, twin-field QKD over 1002 km fibre (a different task and security model, **not** a 1002 km live Bell-pair trading channel): https://pubmed.ncbi.nlm.nih.gov/37295116/
- RFC 9340, no entanglement-only faster-than-light communication: https://www.rfc-editor.org/rfc/rfc9340.html

The other important lesson: **even a demonstrated QKD link is not interchangeable with a validated CHSH nonlocal-game service**.
