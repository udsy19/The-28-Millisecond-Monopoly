# Case file (fictional), Challenge 03: The Quantum Trading Edge

You are a quantitative investment researcher. Your committee asks whether to invest $3M at a $25M pre-money valuation in a startup claiming entanglement lets two separated trading desks coordinate better than any classical strategy.

Protocol (CHSH game): each round a referee sends a uniform random bit x to desk A and y to desk B. Each answers one bit (a, b) without communicating after the inputs arrive; they may agree a strategy and share resources beforehand. They win if a XOR b = x AND y.

| Parameter | Value |
|---|---|
| Valuation | $25M pre-money; investment sought $3M |
| Quantum success, measured | 82% |
| Classical demo, run by startup | 74% |
| Trials | 1,000 per protocol |
| Payoff | +$100 win / −$100 loss per round |
| Operating cost | quantum $0.08/round; classical $0.001/round |
| Claimed annual opportunity | $50M |
| First service | block orders between a New York desk and a London desk |
| Customer infrastructure | desks already share a private low-latency line |
| Link | 40 km fibre test link; entangled-pair rate 1,000/s |
| Team | national-lab founders; three patents filed |

Brief: "Treat every number in a case file as a claim someone made." Phase 3 memo must (1) cite the experiment, (2) say whether the initial hypothesis survived, (3) say what to do next.
