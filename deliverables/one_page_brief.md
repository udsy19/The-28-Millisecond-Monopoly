# One-page brief: entanglement-based coordination for trading desks

**Recommendation: do not invest at this valuation.** Ask: $3M at $25M pre-money ($28M post-money, a 10.7% stake).

## Three numbers

*E1–E6 refer to sections of the analysis notebook.*

1. **64.1%.** Our modelled all-rounds win rate for the startup's 82% source on its own 40 km link (unheralded fibre; the company's denominator is unverified). The free classical rule wins 75%. A trading desk cannot discard rounds, so the product loses to doing nothing clever (E2).
2. **100%.** The win rate with one classical bit sent over the desks' existing private line; a bit crosses New York–London in about 29.5 ms one way, so with any time to communicate entanglement is beaten (E1, E4).
3. **−$21.82 per round.** The startup's own payoff model, redone with every-round accounting on the 40 km link: a desk would simply switch the photons off and take 75%, so on this link the product is worth nothing (used as sold, about $78M a year lost at the target volume). Even $50M would be 1.0% of the ~$5B a year global equities latency-arbitrage market, a generous comparator for block orders (E6).

## Why

- **Photon loss is the lead finding.** On 40 km only 40% of photons reach each desk and both arrive in only 16% of rounds, yet a desk must still answer. Under our unheralded fibre model, an 82% coincidence-level source would win about 64.1% of all attempted rounds on a 40 km link. The company's denominator and protocol remain unverified. A classical setup that drops rounds also scores exactly 82% (E2, E3).
- **The usable zone is tiny.** The modelled 82% unheralded strategy exceeds the classical baseline only below ~5.7 km, under idealized assumptions (8.2 km ideal; ~17.6 km with optimized partially entangled states). Where no bit can arrive, it is also capped at 19 µs (millionths of a second). Every route we checked is red or grey on our main figure (E4).
- **Signals must be balanced.** The edge vanishes unless each signal fires between 29% and 71% of the time. No trade has been named (E5).
- **IP risk.** An earlier patent (Szegedy, Ding & Shi) covers coordinating parties that cannot communicate. Whether the startup can sell without a licence ("freedom to operate") is unproven.

## What would reopen the deal

- Raw logs showing attempted, detected and discarded rounds, with a win rate above 75% over **all** attempted rounds.
- A named trade with a real payoff, balanced signals, and desks close enough for quantum to win (under 5.7 km).
- A credible plan for quantum memories with heralding (a stored photon plus an advance signal confirming both arrived). It keeps the win rate at or above 75% (E2b), but is not claimed and does nothing for New York–London.
- A freedom-to-operate opinion on the three filings, and a valuation that prices the company as an early hardware team, not a trading product.

## Pivot hypothesis (unproven)

The team's real asset is an entanglement source on deployed fibre. Certified randomness (provably unpredictable random numbers) and device-independent key distribution (keys secure even on untrusted hardware) value that without beating a classical bit, though both still need high detection efficiency. **We have not tested either market.**

*Sources:* Ding & Jiang, arXiv:2407.21723; Aquilina, Budish & O'Neill, QJE 137(1) (2022); Hibernia Express (2015); Szegedy, Ding & Shi, US Patent 11676104B2; Liu et al., Nature 640, 343 (2025).
