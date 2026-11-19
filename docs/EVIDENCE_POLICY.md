# Evidence standard and error taxonomy

## Five evidence levels
1. **Mathematical theorem (T)**: CHSH local optimum, Tsirelson ideal bound, light-speed lower bound, simple loss formulas. Give derivation, exact code and validity conditions.
2. **Case claim (C)**: fictional 82%, 74%, 1,000 trials, 40km, 1,000 pairs/s, $50M, $25M pre-money. Reported but not independently verified.
3. **External benchmark (E)**: peer-reviewed fibre attenuation, real historical subsea cable latency, detection-loophole research. URL, publication date, what precisely is supported.
4. **Computational scenario (S)**: Monte Carlo, 0.2dB/km direct-fibre sensitivity, selected route multiplier, detection filtering, 1 pair/s threshold, payoff bias scenario. No fabricated measurement uncertainty or market outcome.
5. **Business hypothesis (H)**: hypothetical product, demand, trade payoff mapping, willingness to pay, customer needs. Never convert into revenue without buyer data.

Every figure/caption should name its level. The role prompts and code flags use this scheme.

## Scientific nonnegotiables
- CHSH classical 75% is **only** for uniform independent x,y and no post-input communication. Nonuniform settings or communication change the classical strategy class.
- Quantum 85.355% is the ideal Tsirelson CHSH bound, **not** this startup's 82% claimed measurement.
- No signalling: correlation cannot transmit a chosen bit between desks before a classical signal arrives.
- A physical light cone excludes communication only below the straight-line vacuum limit; the region between it and the modelled fibre arrival is route-dependent, not physically impossible.
- The cited real cable benchmark is a historical round-trip claim; one half is only an illustrative one-way equivalent, not a measured NY–London one-way route latency.
- Pair-rate ambiguity: the 40km '1,000/s' could refer to emitted pairs, received pairs, or other quantity. Show two hypothetical reconstructions. A loss bound is not a quantum network design; do not claim the classical line can transport entanglement.
- Direct unrepeated fibre loss: 0.2 dB/km applies to a specified telecom optical path. Engineering losses, wavelength, detectors, storage, synchronization, weather, error correction, satellites and repeaters are out of scope unless separately parameterized.
- Coincidence-selected counts are not a loophole-free Bell result. The 82% local counterfeit model is a **falsification attempt of insufficient reporting**, not proof the case used postselection.
- 820/1,000 binomial significance presumes that all 1,000 trials were independently selected and included with the requisite scoring rules. Never attach an unconditional p-value to the reported 82%.
- Device-independent randomness and DI-QKD require much more than an arbitrary Bell-like win rate. No security guarantee from this case alone.
- The ±$100 payoff is artificial and cannot be treated as profit per real trade without a validated mapping. Don't multiply across actual seconds and imply a real $50M business.

## Reproducibility protocol
- All random runs must have fixed seeds and recorded issued-round denominators.
- All inputs should be committed as text, with SHA-256 in outputs.
- Core mathematics uses a standard-library-only Python package and independent tests.
- Tests must assert caveats as well as numbers; numeric success without correct qualifications fails.
- Tables/figures must be generated from the same computational library that drives the memo.
- The interactive site must use formulas equivalent to the tested Python library; where state differs, document it.
- Reviewers should reproduce from a clean clone with Makefile: make check.
- No external API access is required to reproduce.

## Independent reviewer questions
Is every number traceable? What did the input denominator count? Which alternative was optimized? Is 'physical impossibility' distinguished from 'assumed route delay'? Is there a real economic counterfactual? Which finding would make us change our mind?

## Reporting null results
A negative result is useful if it is reproducible. Do not manufacture a profitable region by silently lowering an unverified service threshold. If a model is too simplified to support a decision, say what missing datum is most valuable.
