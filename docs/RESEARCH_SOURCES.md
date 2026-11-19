# Research sources and claim register
**Research snapshot:** 2026-11-19. These are external contextual sources; the hackathon case itself is explicitly fictional. Links are provided so a skeptical reviewer can independently inspect each claim. Consult original sources rather than copying text.

## Course source (not redistributed)
**Columbia University COMS 4995W, Lab-to-Market: Quantum and AI Innovation, Session 11, Nov 19, 2026, Challenge 03, page 4.** The instructor's supplied fictional case is the canonical origin of the valuation, rates, game, payouts and 40km demonstration. The user-supplied Session 6 Bell/CHSH lecture slides are conceptual background, especially the classical bound, quantum game, and detector loopholes. Do not upload private course slides into this public repository.

## Primary and high-quality external sources
1. **Loophole-free Bell experiments** — NIST, Shalm et al. (2015), 'A strong loophole-free test of local realism.' https://www.nist.gov/publications/strong-loophole-free-test-local-realism . Supports need for independent spacelike measurements, high efficiency, no fair-sampling assumption; does not validate fictional startup.
2. **Additional loophole-free photonic Bell work** — NIST, Giustina et al. (2015), 'A significant-loophole-free test of Bell's theorem with entangled photons.' https://www.nist.gov/publications/significant-loophole-free-test-bells-theorem-entangled-photons . Relevant to detection/locality loopholes.
3. **Detection loophole overview** — Stanford Encyclopedia of Philosophy, 'Bell's Theorem', section on detection loophole. https://plato.stanford.edu/archives/spr2024/entries/bell-theorem/ . Explains why conditioning on detected pairs changes the inferential assumptions.
4. **Real-world optical attenuation** — 'Quantum networks with neutral atom processing nodes' (npj Quantum Information, 2023). https://www.nature.com/articles/s41534-023-00759-9 . Explicitly reports approximately 0.2 dB/km for telecom fibre around 1550nm; the project uses it as a sensitivity input, not guaranteed installed-route loss.
5. **NASA quantum networking overview** — NASA, 'Workshop on Space Quantum Communications and Networks' (2020 report). https://www.nasa.gov/wp-content/uploads/2022/04/2020_quantum_workshop_report.pdf . Describes exponential fibre attenuation and free-space alternatives. Never infer a deployed, usable transatlantic Bell service.
6. **Historical classical link benchmark** — Equinix press release, Nov 3, 2015, 'Equinix Connects Hibernia Express Sub-Sea Cable between New York and London.' https://investor.equinix.com/news-events/press-releases/detail/417/equinix-connects-hibernia-express-sub-sea-cable-between-new . Reports under 58.95ms round-trip between named data centres, not guaranteed current fastest link or measured one-way latency; dated 2015.
7. **State of quantum networks (contemporary)** — MIT Quantum Index Report 2026, Quantum Networking, published October 2026. https://qir.mit.edu/networking/ . Draws a technology/readiness gap, including long-haul quantum repeaters and satellite architectures; does NOT conclude no possible future transatlantic network.
8. **Device-independent randomness requirements** — 'Device-independent quantum random-number generation', Nature 562 (2018). https://www.nature.com/articles/s41586-018-0559-3 . Highlights a loophole-free Bell test, high efficiency, independent setting selection, and rigorous extraction/security analysis. The fictional 82% alone cannot establish such guarantees.
9. **2026 independent quantum-networking view** — CNAS, 'The Entanglement Edge' (May 26, 2026). https://www.cnas.org/publications/reports/the-entanglement-edge . Distinguishes early quantum networking products from more advanced research architectures.
10. **Recent scientific scaling analysis** — 'Practical limitations on robustness and scalability of quantum Internet' (Quantum Information Processing, 2026). https://link.springer.com/article/10.1007/s11128-026-05312-z . Provides a research discussion of continental-scale device-independent/network deployment constraints, without establishing what a particular startup built.

## Exact-source distinction
- Mathematical calculations from CHSH and optics are in src/monopoly/ and their tests. They do not require trusting an outside marketing slide.
- The source supports 0.2 dB/km as a useful value, **not** the actual attenuation of a hypothetical NY–London quantum fibre.
- The source supports a historical under-58.95ms RTT, **not** the assertion that 28ms is a universal current latency. The project title is a rhetorical reference to an idealized one-way fibre timescale.
- The source supports the possibility of device-independent randomness under strong assumptions, **not** that one has been demonstrated by the fictional startup.
- Financial payoff data are **fictional inputs**, not cited from any trading market.

## Research backlog requiring further verification
- Actual 2026 best physically realizable one-way NY–London classical route and contract-specific latency, with reliable measurement methodology.
- Availability and fidelity of pre-distributed entanglement with storage over ocean-scale separation.
- Loss-tolerant/DI Bell protocols with full timing and no-click records.
- Signed, customer-approved CHSH-like payoff structure in a real block-order problem.
- Real deployment pricing, risk capital and payment willingness for a separate verifier/randomness product.

Any new empirical claim must include source URL, date, and whether it is a direct result, third-party report or engineering assumption.
