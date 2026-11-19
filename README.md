# The 28-Millisecond Monopoly
### A quantum-investment investigation, not a quantum marketing deck

**Challenge:** COMS 4995W Lab-to-Market: Quantum & AI Innovation, Columbia University, Fall 2026; Session 11 / Challenge 03. The case describes a fictional startup asking for **$3M at a $25M pre-money valuation**, reporting an **82%** CHSH-style coordination success rate against its own **74%** classical demonstration. The ultimate business claim is **$50M/year**. Our question is not merely whether the measurement is exciting, but **whether a real paying customer can exploit it across the Atlantic**.

The argument is deliberately adversarial and fair: make the best possible case for the startup, find the only causal regime where quantum correlations could help, test whether the physical network could supply them, then audit the validity of the 82% measurement and the revenue claim.

**Scientific caution:** The assignment's case data are fictional. All calculations use specified case assumptions and transparent what-if choices. No actual trading returns, deployed transatlantic entanglement service, or loophole-free quantum result is claimed.

## One-command reproducible project

Requires Python 3.11+; the scientific core uses **only the Python standard library**.

    git clone https://github.com/udsy19/The-28-Millisecond-Monopoly.git
    cd The-28-Millisecond-Monopoly
    python -m pip install -e .
    make check

Or without installation:

    python scripts/run_all.py --out artifacts
    python scripts/verify_deliverables.py --dir artifacts

The build produces these independently checkable deliverables:

- artifacts/metrics.json — machine-readable case comparison with explicit uncertainty flags and input SHA-256s.
- artifacts/tables/frontier.csv — deadline × fibre-distance comparison.
- artifacts/tables/payoff_surgery.csv — sensitivity to input distribution.
- artifacts/figures/frontier.svg — visual causal × optical sensitivity frontier.
- artifacts/figures/optical_loss.svg — quantum fibre attenuation sensitivity plot.
- artifacts/figures/payoff_surgery.svg — toy-game advantage versus biased referee inputs.
- artifacts/EXECUTIVE_MEMO.md — generated investment decision memo.
- artifacts/RUN_MANIFEST.md — exact reproducibility assumptions.

Notebook: notebooks/01_investment_investigation.ipynb (runs through the same library, not an independent unmaintained calculation).

## The research, in five acts

| Act | Hypothesis | Experiment | Decision relevance |
|---|---|---|---|
| I. The genuine advantage | Uniform CHSH with no communication has local maximum 75%; ideal quantum reaches ~85.36%. | Enumerate all 16 deterministic local strategies; verify a one-bit classical win. | A reported 82% may be scientifically interesting; 74% is not the relevant classical optimum. |
| II. The light cone | A genuine non-communication regime exists for deadlines shorter than signal flight. | NYC–London geodesic, vacuum and fibre bounds, route uncertainty. | Quantum cannot signal faster than light; it might supply advance correlations. |
| III. The loss wall | Direct unrepeated fibre collapses exponentially with distance. | 0.2 dB/km sensitivity and two interpretations of the case's 1,000 pairs/s. | The 40 km demo is not a transatlantic product. |
| IV. The forensic reveal | Coincidence filtering can make a purely local strategy report 82%. | Exact analytical construction + seeded Monte Carlo; distinguish issued from retained rounds. | Ask about detectors, randomization, denominators and loopholes. |
| V. The financial autopsy | The incremental edge is $13.921, not $63.92, per fictional round against the best classical strategy. | Unit economics, reverse-engineered 3.59M rounds, biased input sensitivity. | Neither round volume nor payoff mapping to real block orders is validated. |

At least two alternatives are compared computationally across several experimental tracks. The recommendation may change if the company demonstrates all three independent gates: scientifically valid quantum correlation, deployable delivery at relevant rates, and incremental real-market returns relative to the **best possible classical alternative**.

## Interactive investment war room

    make serve

Then open http://localhost:8000 in a browser. The site under site/ has sliders for separation, deadline, assumed photon-pair source rate, detection-loophole filtering and input odds. Every interactive value is a **model**. It must not be marketed as measured hardware or market performance.

## Autonomous agent development

This repository is structured to support Claude Code or Codex agents working on isolated worktrees, tasks and review gates.

**Start here:** AGENTS.md, CLAUDE.md, docs/AUTONOMY.md, docs/ROADMAP.md, automation/tasks.json and agents/ (role briefs). The local runner is scripts/autopilot.py; it requires the relevant agent CLI and a local git clone, and is opt-in for executing commands. No one must put tokens or API keys in the repository.

## Repository map

- data/ — canonical fictional case, separate explicit model assumptions.
- src/monopoly/ — pure math and scenario engines; no network access.
- tests/ — independently reproducible regressions and claims gates.
- notebooks/ — demonstration notebook reusing the tested library.
- site/ — standalone responsive interactive storytelling exhibit.
- docs/ — scientific methods, strategy, external source register, creative direction, plan and decision policy.
- agents/ — self-contained research/implementation prompts with file ownership.
- automation/ — dependency-aware autonomous task manifest.
- scripts/ — evidence validator, build shortcut and autonomous local agent launcher.
- .github/workflows/ — offline scientific CI.

## Start with primary sources, not founders' claims

See docs/RESEARCH_SOURCES.md, docs/CASE_LEDGER.md and docs/EVIDENCE_POLICY.md. The course's full PDF and slides are deliberately **not redistributed** in this public repo: you must use your own authorized copy and cite the case appropriately.

## Grading handoff

**Phase 1 — Investigate:** deliverables/PHASE_1_HYPOTHESIS.md and docs/EXPERIMENT_PLAN.md.

**Phase 2 — Experiment:** code + notebook + generated figures/tables + explicit assumptions + automated tests.

**Phase 3 — Recommend:** generated artifacts/EXECUTIVE_MEMO.md and docs/DECISION_SCORECARD.md.

Everything in this repository is a fictional academic study, not financial advice or an operational trading protocol.
