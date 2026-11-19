# Review: Challenge 03, "The Photon That Didn't Show Up"

Reviewer stance: skeptical grader. Inputs reviewed: `case_file.md`, `analysis_executed.ipynb` (markdown and outputs), `results/results.json`, `deliverables/*.md` (not the templates), and `figures/main_frontier.png`. I re-ran every check below with plain Python and `math`, not the repo's code.

**Overall verdict.** The numbers are right and the core physics argument is sound. The recommendation follows from the evidence. The weak spots are in the wording, not the arithmetic:
- generalisations from three landmarks ("every real trading route"),
- legal claims about the patent,
- one physics error in the heralding rebuttal,
- an economics framing ("loses $78M a year") that a founder can easily call a straw man,
- a few consistency and formatting gaps against the Phase 3 checklist.

---

## (a) Independent re-derivation

| # | Quantity | My calculation | Repo value | Match? |
|---|---|---|---|---|
| 1 | Per-desk efficiency, 40 km, midpoint source, 0.2 dB/km | Each arm is 20 km, so 4 dB of loss: η = 10^(−0.4) = **0.39811** | 0.3981 | Yes |
| 2 | Share of rounds where both photons arrive | η² = **0.15849** | 0.1585 ("16%") | Yes |
| 3 | All-rounds win rate at q = 0.82 | W = η²q + 2η(1−η)·½ + (1−η)²·¾ = 0.12996 + 0.23961 + 0.27171 = **0.64129** | 0.6413 ("64.1%") | Yes |
| 3b | Same, ideal source (q = cos²(π/8) = 0.85355) | **0.64660** | 64.7% | Yes |
| 4 | Break-even efficiency | Setting W = ¾ gives η*(q − ¼) = ½, so η* = 0.5/(q − 0.25). At q = 0.82: **0.87719**. At the ideal source: **0.82843** = 2(√2 − 1), the Garg–Mermin value | 87.7% / 82.8% | Yes |
| 5 | Maximum desk separation | d = −100·log10(η*). This gives **5.690 km** (q = 0.82), **8.175 km** (ideal) and **17.609 km** (η = 2/3) | 5.7 / 8.2 / 17.6 km | Yes |
| 6 | Light time at d_max | 5.690 km ÷ c = **18.98 µs**; 17.61 km ÷ c = 58.7 µs | 19 µs / 59 µs | Yes |
| 7 | Classical cheater (always answer 0; A says "no photon" with probability 0.4375 when x = 1) | Rounds kept = 1 − 0.5·0.4375 = **0.78125**. Kept losses = 0.25·0.5625 = 0.140625. Win on kept rounds = 1 − 0.140625/0.78125 = **0.8200**. Win on all rounds = 0.75 | 82% / 78.1% / 75% | Yes |
| 8 | z-scores (null standard error √(0.75·0.25/1000) = 0.013693) | z(82%) = 0.07/0.013693 = **+5.112**; z(74%) = **−0.730**. 95% interval for 74%: **71.28%–76.72%** | +5.1 / −0.7 / 71.3–76.7% | Yes |
| 9 | Edge per round (on the startup's claim) | [100(2·0.82 − 1) − 0.08] − [100(2·0.75 − 1) − 0.001] = 63.92 − 49.999 = **$13.921** | $13.92 | Yes |
| 10 | Rounds needed for $50M | 50e6 / 13.921 = **3,591,696** | 3.59 million | Yes |
| 11 | Hours of pair generation | 3.59M / 1000 = 3,592 s = **1.00 h**; divided by η² gives **6.30 h** | 1.0 h / 6.3 h | Yes |
| 12 | Edge counting every round, and the annual result | 100(2·0.64129 − 1) − 0.08 − 49.999 = **−$21.822**. Times 3.59M rounds = **−$78.38M** | −$21.82 / −$78M | Yes |
| 13 | Attempted rounds if the 1,000 trials were post-selected | 1000/η² = **6,309.6** | 6,310 | Yes |
| 14 | Window of signal bias where quantum keeps an edge (my own brute-force classical search plus a 2-D XOR-game quantum optimisation) | The gap is above zero only for 0.293 < p < 0.707. Gap = 0.1036 at p = 0.5 and 0.0079 at p = 0.35 | 29%–71%, 10.4 points | Yes |
| 15 | Light time New York–London | 5570 km ÷ c = **18.58 ms**; Hibernia round trip 58.95 ms ÷ 2 = 29.48 ms | 18.6 / 29.5 ms | Yes |

**Is the model physically sound?** Mostly yes.

- **Classical maximum of 75%.** Correct. This is the local bound of the CHSH game. A brute force over all 16 deterministic rules confirms it (8 of them reach 75%), and shared randomness cannot do better than the best deterministic rule.
- **One photon missing gives a 50% coin flip.** Correct for a maximally entangled (or Werner-noise) state. The desk that still has its photon gets an outcome whose marginal is uniform. That outcome is independent of the other desk's fixed fallback, so a⊕b is uniform and the win rate is exactly ½, whatever the fallback. This is the standard Garg–Mermin analysis.
- **Both photons missing gives 75%.** Correct: both desks answer 0, so they win whenever xy = 0. It is also the best any deterministic fallback can do.
- **The model behind the 82.8% threshold is the textbook one.** The Eberhard 2/3 floor is the right best case for this two-input, two-output game, because each desk must output a bit. Two caveats:
  1. Eberhard (1993) showed that 2/3 is *sufficient* as η→2/3, using non-maximally entangled states. The fact that nothing below 2/3 works in the 2-input, 2-output case is a separate known result, and none of the cited sources proves it. Assumption A5 ("Proven lower bound for any CHSH-type test") overstates what the cited source shows. Suggested wording: "the best known threshold for two-setting tests (Eberhard 1993)".
  2. The advantage near the floor tends to zero. The 17.6 km figure is therefore a limit where the edge is effectively nil, not a usable operating point. The memo partly says this already ("theoretical best case").
- **An unstated feature of the model: the win curve is not monotone in distance.** The minimum is at η = 0.25/(q − 0.25) = 0.4386, about 35.8 km, where W = 0.6404. Beyond that the curve climbs back toward 75% as the desks mostly play the classical fallback. This is why NYSE–Nasdaq at 56 km (65.6%) "beats" the 40 km link (64.1%), and why Carteret at 32 km (64.13%) is slightly *below* 40 km. A sharp reader will ask why. The answer also shows that 64.1% comes from a strategy no rational desk would choose. A desk that ignores the photons gets 75%. See (e)3.
- **Source placement.** A source at one end instead of the midpoint gives W = 0.158·0.82 + 0.842·0.5 = **55.1%**. That is worse for the startup, so the midpoint choice is indeed generous to the startup.
- **Speed of light.** Using vacuum c for the bit is correctly labelled as favouring "us" (A8). The figure and memo then cite Hibernia's 29.5 ms cable. Between 18.6 and 29.5 ms, New York–London is drawn grey, yet that bit could not physically arrive over the cable the desks actually have. This does not change the result, because the area would be red anyway with η ≈ 10⁻⁵⁶.

---

## (b) Claims not backed by results.json or the allowed sources

**Legal and patent claims (overstated):**
1. memo.md l.38: "the prior patent on this exact idea (Szegedy, Ding & Shi)". "This exact idea" is unsupported. Nobody compared the patent's *claims* with the startup's three filings, whose content is unknown. Patent scope is set by the claims, not by the title or subject. Suggested wording: "a prior patent on closely related subject matter".
2. one_page_brief.md l.19: "describes the same idea". Same problem.
3. claims_ledger.md l.15: "is titled for coordinating decisions between non-communicating parties, the same idea". The title is not verified here, and "same idea" is unsupported.
4. Freedom to operate (FTO) is mixed up with patentability:
   - steelman l.61 says "raises a freedom-to-operate question for all three filings";
   - the brief l.26 says "A freedom-to-operate opinion on the three filings".

   A prior patent raises two separate questions: (i) FTO, whether the startup can *practise* its product without infringing; and (ii) prior art against the *validity or patentability* of its own filings. FTO is not "on filings". None of the deliverables checks whether the patent is in force, who the assignee is, or which jurisdiction applies (US only, while the first product is New York–London).

**Claims about "every real route" (overstated):**
5. figures/main_frontier.png title: "Photon loss or one classical bit beats entanglement on **every real trading route**". Only three real routes were checked (32, 56 and 5,570 km).
6. evidence_register.md B5: "Every real trading route is further apart." This is unqualified. B10: "No real route is green."
7. steelman l.28: "Nothing, for fibre between real trading sites."
8. The green band is not empty in principle. In a 5–10 µs race window, green covers separations from **1.5–3.0 km** (where the light time equals the window) up to **5.7 km**. Facilities within the same metro area that are a few km apart were not checked. The brief's "every real trading route *we checked*" (l.17) is the correct wording, and the other places should match it.
9. The landmark distances are not sourced: Carteret–Secaucus ~32 km, and New York–London 5,570 km (A13 calls them "approximate straight-line"). Only NYSE–Nasdaq (~56.3 km) comes from Ding & Jiang.

**Timing assumptions presented as fact:**
10. claims_ledger l.12: "block-order windows are far longer [than 18.6 ms], so grey region". No source supports this. memo l.22 says "New York–London is grey" as fact. On the computed map, New York–London is grey only if the decision window is longer than 18.6 ms. results.json records `region_at_1ms: 1` (red) for New York–London. The conclusion holds either way: grey means one bit wins; red means W = 75% exactly, with no edge. The memo should say "grey or red; no edge in either case".
11. The memo, brief, oral script and steelman all assume the startup's "private low-latency line" *is* Hibernia Express. The case file only says "private low-latency line". Hibernia is evidence of what is achievable, not a description of the customer's line.
12. "Real single-photon detectors are 80–95% efficient" (notebook, cell 9) has no source. The steelman's "realistic, slightly imperfect detectors" leans on it.

**Interpretive overstatements:**
13. memo l.18: "the 82% was **almost certainly** counted only on rounds where both photons were detected". The other documents say "most likely", and evidence register B7 rates it "Moderate (an inference, not a fact)". The case never says the 82% was measured *over* the 40 km link: the 40 km link and the 82% are separate rows. The memo should match "most likely" and name the alternative (measured over a short or local link).
14. memo l.11: "statistically the same as 75%". Failing to reject is not equality. Suggested wording: "consistent with 75% (95% interval 71.3%–76.7%)".
15. oral_script l.11: "Over 1,000 trials, that is real." This contradicts the script's own cheater segment. Suggested wording: "unlikely to be luck".
16. one_page_brief l.10: "With any time to communicate, entanglement is beaten." This only holds when the window is at least the one-way latency of the line.
17. memo l.26, brief l.11, ledger l.11 and evidence B13: "would lose about $78M a year". This assumes a customer keeps running a strategy that loses to a free alternative. The defensible claim is "the product is worth nothing (and costs $0.08 a round) on every-round accounting". See (e)3.
18. "$5B global latency-arbitrage market" (memo l.26, brief l.11). Aquilina et al. estimate this for **global equity markets**, and the notebook (cell 27) says "equities". The product's first use, block orders, is not latency arbitrage at all, so the 1%-of-pie comparison is a category mismatch. Also, 1% of a market is not "implausible" in itself (ledger l.11).
19. evidence_register A6 calls $50M a "revenue target"; claims_ledger l.11 reads it as "Net profit". The notebook treats it as the per-round edge over classical. Pick one reading.

**Steelman physics error:**
20. steelman l.36: "The herald is itself a classical signal. It has to arrive before the round. On any route where there is time for that, there is usually time for one classical bit." This is **wrong**. With quantum memories, the herald is exchanged *before the inputs exist*: pairs are stored and confirmed in advance. The winning classical bit must be sent *after* the inputs arrive and within the decision window. Heralding does not imply that the post-input bit can arrive in time; that is the whole point of memories. Delete this bullet. The remaining bullets (memories not claimed, not commercial, no help for New York–London) carry the argument.

**Sources:**
21. Liu et al., Nature 640, 343 (2025) is cited as support for pivoting an *entangled-photon* team to certified randomness. That result is computational certified randomness (random-circuit sampling on a trapped-ion processor), not randomness from a photonic Bell test. It shows demand for certified randomness, not a fit for this team's hardware. The memo hedges ("unproven"), but evidence register C9 should say this.
22. steelman l.24 raises "Low-loss fibre is coming", and the rebuttal answers only about detectors. Lower fibre loss *does* move the frontier:

    | Fibre loss | d_max at q = 82% | d_max at the 2/3 floor |
    |---|---|---|
    | 0.15 dB/km | 7.6 km | 23.5 km |
    | 0.10 dB/km | 11.4 km | **35.2 km** |

    35.2 km is beyond Carteret–Secaucus (32 km). "What survives: Nothing" is therefore overstated. Add a line saying that even 0.1 dB/km fibre keeps the 82% source under 12 km, and that the floor case has a vanishing edge.
23. one_page_brief Sources omits Ding & Jiang, although the brief's 29%–71% result (Theorem 10) and the fibre verdict depend on it. Eberhard and Mermin are also missing; the 5.7 km threshold uses Garg–Mermin-type reasoning.
24. evidence_register C4 (Craddock et al., "~5×10⁵ pairs/s over 34 km") and C3 (Yin et al., "~1.1 pairs/s") are allowed sources. I could not verify the exact figures from the inputs given; check them against the papers. Craddock's rate is probably a *generated* or source rate, not a delivered rate; state which.
25. Minor: memo l.3 and the steelman cite `analysis.ipynb`, but the executed file reviewed is `analysis_executed.ipynb`.

---

## (c) Jargon an executive would not follow without a gloss

**memo.md**
- "classical rule" / "classical bit" (l.11–12, throughout): "classical" is never glossed as "ordinary, non-quantum".
- "the free 75% rule" (l.16): it is unclear what "free" means. Suggested wording: "the 75% you get with no quantum hardware".
- "ideal source" / "a source of the startup's quality" (l.16): "source" is not glossed (the device that makes the photon pairs).
- "the theoretical best case: 17.6 km" (l.16): it is unclear whose best case and why.
- "µs" (l.22): add "millionths of a second".
- "latency-arbitrage market" (l.26): gloss it as "profits from being microseconds faster than other traders".
- "freedom to operate" (l.38): gloss it as "the right to sell without infringing someone else's patent".
- "fallbacks" (l.52, Limitations).
- The ±$100 payoff "round" is never explained as one coordinated decision.
- The figure caption uses colour regions without saying the colours are the figure's.
- Sources line: "nonuniform-input theorem", "2/3 efficiency floor", "detection-efficiency thresholds". These are acceptable in a sources list, but "Mermin (1986); Eberhard" should say what they are for in plain words.

**one_page_brief.md**
- "E1, E2, E4, E5, E6, E2b": experiment codes appear in a one-page brief that has no key.
- "heralding" (l.25) and "quantum-memory" are not glossed in the brief; only the steelman glosses them.
- "green zone" (l.24) and "red or grey on our main figure" (l.17): the brief contains no figure.
- "freedom to operate" (l.19, 26); "pre-money / post-money" (fine for a committee); "detection efficiency" (l.30); "device-independent key distribution" (glossed, fine); "classical setup", "classical bit" (not glossed); "µs" (l.17).

---

## (d) Phase 3 requirements and checklist for memo.md

| Requirement | Status | Note |
|---|---|---|
| (1) Cites the experiment | **Partly** | It cites "analysis.ipynb via results.json" and the figure. It never names the experiment the decision rests on (E2 photon-loss Monte Carlo: 1,000,000 simulated rounds, seed 20261119, matching the formula within 0.02 points), nor E3 by name. Add one sentence. The filename is also wrong (`analysis_executed.ipynb`). |
| (2) Says whether the hypothesis survived | **Yes** | "Did our hypothesis survive? Yes, but for a different reason." The phrasing contradicts itself: the next lines say the original reason is "True, but incomplete". It is the same reason, strengthened by a second one. Suggested wording: "Yes, and on stronger grounds." |
| (3) Says what to do next | **Yes** | "Questions for the founders" and "What would reopen the deal". There is no owner, deadline or ask amount for the next step (for example "send the five questions; revisit only if the logs show >75% on all rounds"). |
| Recommendation in the first sentence | **Not quite** | The first sentence of the body is the italic provenance line ("*Investment memo… Every number comes from…*"). Move it to the end or into a footnote. |
| ≤ 2 pages | **Borderline** | About 970 words plus a full-width figure. At normal type that is likely just over two pages. Render it to PDF and check; trimming the "pivot" section or the figure size would fix it. |
| Sources listed | **Yes** | 6 sources. The 17.6 km and 2/3 reasoning cites Eberhard, which is fine. |
| Limitations paragraph | **Yes** | It is good. It should add the "must answer every round" assumption and the unknown measurement distance of the 82% (see (e)1). |

**Internal consistency (contradictions found):**
- **5.7 km vs "6 km"**: the memo and brief say 5.7 km; the evidence register B10, steelman l.45, oral script l.20 and figure title say 6 km. These are the same number rounded differently. Use one everywhere.
- **"almost certainly" (memo) vs "most likely" (brief, steelman, oral) vs "Moderate (an inference)" (evidence B7).** These contradict each other on certainty.
- **$50M as "revenue" (evidence A6) vs "net profit" (ledger) vs per-round edge (notebook).**
- **Heralding:** the memo says it "never drops below 75%… no help for New York–London", which is consistent. The steelman adds the faulty "herald implies time for a bit" argument, which the memo does not make.
- **The claims ledger says "one row per case-file number" but has no rows for the valuation ($25M / $3M) or the operating costs ($0.08 / $0.001).** The costs are used in E6 but never assessed as claims.
- **The ledger's "Link" row** reports "all-rounds win 64.7% even with an ideal source" next to "break-even needs 87.7%", which is the threshold for the 82% source. Two source qualities are mixed in one cell.
- **The steelman** says satellites "would also need memories and heralding". The memo's Limitations says satellites were not modelled. That is fine, but the steelman's verdict "Nothing for trading" is stronger than a non-modelled case supports.
- Otherwise the headline numbers (64.1%, 16%, 6,310, 87.7%, 5.7/8.2/17.6 km, −$21.82, $13.92, 3.59M, 29–71%) are consistent across all documents and with results.json.

---

## (e) The three weakest points

1. **The 82% is assumed to have been measured over the 40 km link, with desks forced to answer every round.** The case file lists "Quantum success, measured: 82%" and "Link: 40 km fibre test link" as separate rows. The whole "the two numbers cannot both hold" punchline depends on joining them.

   A founder will answer: "The 82% was a local or short-fibre characterisation. We never said it was an all-rounds figure on 40 km, and the product's whole design is around how we deploy." The "must answer every round" premise is also a modelling choice, not a fact about trading. A real desk can often *abstain*: not trade, zero payoff.

   Abstention cannot be coordinated, because each desk does not know whether its partner received a photon, so the result is probably robust. But the deliverables never argue this; they assert it. Fix: state both assumptions in Limitations, add "where was the 82% measured?" to the founder questions, and spend one sentence on why unilateral abstention does not rescue the product.

2. **The scope claims are broader than the analysis.**
   - "Every real trading route" rests on three landmarks.
   - New York–London is "grey" only under an unsourced assumption about block-order windows.
   - The patent is "this exact idea" with no claims comparison.
   - The steelman's heralding rebuttal contains a real physics error. The herald is exchanged before the inputs, so it does not imply time for the post-input bit.

   A physics-literate committee member will find the heralding error, and it undermines trust in the rest. Fix: delete it, hedge the route and patent language, and add the low-loss-fibre numbers (0.1 dB/km gives an 11.4 km break-even, 35 km at the floor).

3. **The economics framing.**
   - "Loses $78M a year" assumes the customer keeps running a strategy that is worse than a free alternative. A rational desk ignores the photons and gets 75%, so the product's value is about $0 minus $0.08 a round, not −$78M.
   - Comparing $50M to the ~$5B *equities latency-arbitrage* pie is a category mismatch for a block-order product.
   - Under the case's own payoff, plain classical play already earns $50 a round, and one bit earns $100. That shows the ±$100 payoff is meaningless as a revenue model, which would be a stronger point to make.

   A founder can call the −$78M a straw man and score a point. Fix: lead with "zero incremental value on every-round accounting" and keep −$21.82 as a footnote showing what happens if the customer naively uses the photons.

(Runner-up: the biased-signal result compares against 75%, but with biased inputs the classical baseline itself rises, for example to 91% at p = 0.3. The text correctly says "edge" but sometimes reads as if 75% stays the benchmark.)

---

## (f) Main figure (`figures/main_frontier.png`)

- **The title states the conclusion on its own.** Yes: "Photon loss or one classical bit beats entanglement on every real trading route / Quantum only pays within 6 km and under 19 µs — the startup's own 40 km link is red." It is strong. "Every real trading route" overclaims (three routes checked), and "6 km" conflicts with the legend's "< 5.7 km". Suggested wording: "…on every trading route we checked".
- **The yellow label is misleading.** The in-plot label says "YELLOW ideal source only". The legend says "ideal source near 2/3 floor only (< 17.6 km)". But an *ideal maximally entangled* source only beats 75% out to **8.2 km**. From 8.2 to 17.6 km, only Eberhard's non-maximally entangled states reach the limit, and only with a vanishing edge. Either split yellow at 8.2 km, or relabel it "best case in theory (Eberhard 2/3 floor); edge ≈ 0 near the edge".
- **The y-axis label** reads "Time allowed to make the decision (µs, log scale)", but the ticks mix µs and ms. Drop "µs" from the label.
- **Overlaps and legibility.**
  - The race-band text "typical latency-arbitrage race (5–10 µs)" is crossed by the one-bit line and runs across the green/yellow boundary.
  - The translucent blue band over red produces a mauve colour that appears in no legend entry.
  - The landmark labels sit inside the grey region near the top and are legible.
  - "New York–London (~5,570 km)" is rotated and legible.
  - The footnote is small and will be hard to read on a slide.
  - Otherwise there are no collisions.
- **Other misleading points.**
  - Red is defined as "quantum below 75%". At New York–London the computed value is exactly 75.0% (results.json `win_all_rounds_82: 0.75`), so the label should read "no better than 75%".
  - The red band from 18.6 to 29.5 ms at New York–London is drawn grey because the boundary uses vacuum c, while the memo caption quotes the 29.5 ms cable. This does not affect the conclusion; mention it in the footnote or move the line.
  - No markers show where each landmark sits *at the race window*. A dot at 5–10 µs on each vertical line would make "red" visible at a glance.
  - The figure shows no non-monotonicity, but the text quotes NYSE–Nasdaq as 65.6% versus 64.1% for the closer links without explaining why. A one-line note would help.

---

## Issues to fix (prioritised)

1. **[must-fix]** Remove the heralding argument in steelman_rebuttal.md l.36 ("The herald is itself a classical signal… there is usually time for one classical bit"). It is physically wrong: the herald comes before the inputs, while the winning bit must be sent after them.
2. **[must-fix]** Tone down the patent claims: memo l.38 "this exact idea", brief l.19 "the same idea", ledger l.15 "the same idea". Separate freedom to operate (practising the product) from prior art against the startup's filings (steelman l.61, brief l.26). Note that the patent's claims, status and jurisdiction were not examined.
3. **[must-fix]** Replace "every real trading route" / "No real route is green" / "Every real trading route is further apart" with "every route we checked (three)". This applies to the figure title, evidence B5 and B10, and steelman l.28. Note that green spans about 1.5–5.7 km in a 5–10 µs window and that facilities within one metro area were not checked.
4. **[must-fix]** State the two premises behind the headline in the memo's Limitations: (i) the 82% is assumed to have been measured over the 40 km link, and (ii) desks must answer every round. Add "Where and over what distance was the 82% measured?" to the founder questions. Change "almost certainly" (memo l.18) to "most likely", to match the other documents.
5. **[should-fix]** Reframe the economics: the product is worth about $0 on every-round accounting, because a rational desk falls back to 75%. Present −$21.82 a round / −$78M as the result of naive use, not as the expected loss. Call the $5B an *equities* latency-arbitrage figure and note the mismatch with a block-order product. Settle on one reading of $50M (revenue, profit or edge) across the evidence register and the claims ledger.
6. **[should-fix]** New York–London: say "grey if the decision window is longer than ~18.6–29.5 ms, red otherwise; no edge either way". Stop asserting "block-order windows are far longer" (ledger l.12) without a source. Treat Hibernia as what is achievable, not as the customer's line.
7. **[should-fix]** Memo: make the recommendation the first sentence (move the italic provenance line). Name the experiment (E2 Monte Carlo, 1,000,000 rounds, seed 20261119; E3 cheater). Fix the notebook filename. Render to PDF to confirm it fits in 2 pages.
8. **[should-fix]** Figure: relabel yellow (an ideal source stops at 8.2 km; 8.2–17.6 km is the Eberhard best case only); "6 km" to "5.7 km"; red to "no better than 75%"; drop "µs" from the y-axis label; keep the race-band label from crossing the line.
9. **[should-fix]** Steelman "low-loss fibre": add the 0.15 and 0.10 dB/km numbers (7.6 and 11.4 km break-even; 23.5 and 35.2 km at the floor). Soften "Nothing survives".
10. **[should-fix]** Gloss the jargon in the memo and brief: "classical", "source", "µs", "latency arbitrage", "freedom to operate", "heralding" (brief), and the experiment codes and "green zone" (brief has no figure). Change "the free 75% rule" to "the 75% you get without quantum hardware".
11. **[should-fix]** Add Ding & Jiang (and Eberhard) to the brief's Sources. Clarify in evidence C9 that Liu et al. is computational certified randomness, not Bell-test or photonic. Check the Craddock (5×10⁵ pairs/s; generated or delivered?) and Yin (1.1 pairs/s) figures against the papers.
12. **[should-fix]** Claims ledger: add rows for the valuation and the operating costs, to honour "one row per case-file number". Do not mix ideal-source and 82%-source numbers in the Link row.
13. **[nit]** memo l.11 "statistically the same as 75%" to "consistent with 75%". oral_script l.11 "that is real" to "unlikely to be luck". brief l.10 "With any time to communicate" to "with time for one bit over the line".
14. **[nit]** memo "Yes, but for a different reason" to "Yes, and on stronger grounds" (the original reason still holds).
15. **[nit]** assumptions.md A5: "Proven lower bound for any CHSH-type test" to "best known threshold for two-setting tests (Eberhard 1993)". Add a sentence explaining why NYSE–Nasdaq (65.6%) scores above the 40 km link (64.1%): the curve has its minimum at about 36 km and recovers toward 75% as the desks mostly play the classical fallback.
16. **[nit]** Unsourced figures: Carteret–Secaucus 32 km, New York–London 5,570 km, and "detectors are 80–95% efficient" (notebook). Source them or mark them as estimates.
