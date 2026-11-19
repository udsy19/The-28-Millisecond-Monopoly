<!-- Generated from docs/README.template.md by scripts/render_deliverables.py. Edit the template, not README.md. -->
# The Photon That Didn't Show Up

[![ci](https://github.com/udsy19/The-28-Millisecond-Monopoly/actions/workflows/ci.yml/badge.svg)](https://github.com/udsy19/The-28-Millisecond-Monopoly/actions/workflows/ci.yml)
[![pages](https://github.com/udsy19/The-28-Millisecond-Monopoly/actions/workflows/pages.yml/badge.svg)](https://github.com/udsy19/The-28-Millisecond-Monopoly/actions/workflows/pages.yml)
[![license: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![python 3.13](https://img.shields.io/badge/python-3.13-blue.svg)](pyproject.toml)

**Website:** https://udsy19.github.io/The-28-Millisecond-Monopoly/ ·
**Memo (PDF):** [`reports/memo.pdf`](reports/memo.pdf) ·
**Case file:** [`case_file.md`](case_file.md)

An open, reproducible investment-diligence study. A (fictional) startup asks for {{investment}} at a {{pre_money}}
pre-money valuation to sell entanglement-based coordination, the CHSH game, to trading desks, starting with New York and
London. We treat every number in its case file as a claim, test each one in code, and ask one question carefully:
*is there any place where entangled photons beat the classical alternative a trading desk already has?* Built for
Columbia COMS 4995W *Lab-to-Market: Quantum and AI Innovation*, Challenge 03 ("The Quantum Trading Edge").

> **Research and teaching material, not investment advice.** The startup and its numbers are fictional. Nothing
> here executes trades or certifies any device.

## Key results

| Result | Value | Evidence |
|---|---|---|
| Best classical rule without communication (all 16 deterministic strategies) | {{classical_max}} | `EXACT` brute force |
| Ideal quantum strategy (Born-rule singlet sampling, {{n_mc}} rounds) | {{ideal_q}} | `EXACT` + `MONTE-CARLO` |
| One classical bit over the desks' existing line | {{one_bit}} | `EXACT` |
| Startup's claimed {{p_claim}} vs {{classical_max}}, n = {{n_trials}} | z = {{z_82}} (classical demo {{p_demo}}: z = {{z_74}}) | `CASE-FILE CLAIM` |
| Per-desk photon efficiency, {{link_km}} link ({{fibre_loss}}, midpoint source) | {{eta_40}}; both photons arrive in {{both_share}} of rounds | `MODEL` + `MONTE-CARLO` |
| **All-rounds win rate on the startup's own {{link_km}} link** | **{{win40_82}}** ({{p_claim}} source), {{win40_ideal}} (ideal) | `MODEL` + `MONTE-CARLO` |
| Break-even efficiency → max separation, unheralded strategies | {{eta_star_82}} → {{dmax_82}} (ideal source {{dmax_ideal}}; Eberhard tuned states {{dmax_floor}}; heralded: no fixed cutoff, supply-limited) | `MODEL` |
| Classical cheater that discards rounds (detection loophole) | {{cheat_det}} on kept rounds, {{cheat_all}} overall, {{cheat_kept}} kept | `EXACT` + `MONTE-CARLO` |
| Edge per round: claimed vs every-round accounting | {{edge_claim}} vs {{edge_all_82}} | `MODEL` (payoff invented by the case) |
| Quantum edge with biased signals (Ding & Jiang Thm 10) | only when signals fire {{adv_lo_pct}}–{{adv_hi_pct}} of the time | `PUBLISHED` + independent check |

**Recommendation: do not invest at this valuation.** The physics is real, but the evidence does not establish a usable,
profitable coordination service. Under our unheralded fibre model, an {{p_claim}} coincidence-level source
would win about {{win40_82}} of all attempted rounds on a {{link_km}} link. The company's denominator and protocol remain
unverified. That is below the free {{classical_max}} classical rule. The modelled {{p_claim}} unheralded strategy exceeds
the classical baseline only below ~{{dmax_82}}, under idealized assumptions ({{dmax_ideal}} ideal; ~{{dmax_floor}} with
optimized partially entangled states). Whenever one classical bit can arrive over the desks' line it wins every round. Heralded delivery with quantum memories has
no fixed distance cutoff but is limited by pair supply; across the Atlantic, direct fibre supplies essentially none.

![Main figure: where entanglement could pay](figures/main_frontier.png)

### Negative results, limitations and corrections (kept deliberately)

1. The lost-photon fallback is a simple model (a desk without its photon plays a fixed answer). Smarter fallbacks lower
   the bar, but never past Eberhard's best case ({{dmax_floor}}), which we report.
2. Heralded delivery with quantum memories removes the photon-loss penalty in principle (win rate never below
   {{classical_max}}). The startup has not claimed memories, and it does nothing for New York–London.
3. Perfect detectors are assumed (generous to the startup). Lower-loss fibre helps slowly: at {{loss_017}} the {{p_claim}} source
   reaches {{dmax_82_017}}; a hypothetical {{loss_010}} fibre gives {{dmax_82_010}}.
4. We checked three metro routes (32–56 km) and New York–London, not every pair of facilities within a few kilometres.
   The one-bit boundary has three states (physically excluded / route-dependent / arrives on the modelled route);
   New York–London's ~{{hibernia_one_way}} is derived from a 2015 round-trip benchmark, not a measured one-way service.
5. The ±{{payoff}} payoff and the {{target}} claim are the case's own and were not matched to a real trade.

Full record: [`DECISIONS.md`](DECISIONS.md) (every judgment call and every fix) ·
independent review: [`review/review.md`](review/review.md) · assumptions: [`deliverables/assumptions.md`](deliverables/assumptions.md).

## What is in the repository

| Path | Contents |
|---|---|
| `src/chsh.py` | Pure, documented model: classical brute force, singlet sampling, photon loss, heralding, cheater, frontier, biased inputs, economics |
| `analysis.ipynb` | Experiments E1–E6 and E2b, generated by `scripts/build_notebook.py`; executed copy `analysis_executed.ipynb` |
| `results/results.json` | Every computed value (`values`) and the exact strings the writing uses (`display`) |
| `figures/` | Main figure and supporting figures at 300 dpi (generated, never hand-edited) |
| `deliverables/` | Phase 1 plan, memo, claims ledger, assumptions, evidence register, steelman/rebuttal, one-page brief, oral script — rendered from `deliverables/templates/` |
| `reports/` | PDFs of the memo, Phase 1 plan and one-page brief |
| `site/` | Static website; `site/model.js` is a line-for-line port of `src/chsh.py` |
| `tests/` | Expected values (`test_chsh.py`), Python–browser parity (`test_parity.py`), site integrity (`test_site.py`) |
| `scripts/` | Notebook builder, renderer, number checker, PDF build, site build, packaging |
| `review/`, `DECISIONS.md`, `PLAN.md` | Independent review, judgment calls, build checklist |

## Quick start

Requirements: Python 3.13; Node 22 for the parity tests, PDFs and screenshots; `pandoc` for PDFs.

```bash
git clone https://github.com/udsy19/The-28-Millisecond-Monopoly && cd The-28-Millisecond-Monopoly
python3.13 -m venv .venv && . .venv/bin/activate
pip install -r requirements.txt
python -m pytest -q                      # expected values, parity, site integrity
scripts/package.sh                       # notebook → results.json → deliverables → PDFs → submission.zip
```

Fixed seed {{seed}}: re-running produces a byte-identical `results/results.json`. Preview the website locally:

```bash
python scripts/build_site.py --out _site && python -m http.server -d _site 8000
```

## How a number reaches the memo

`src/chsh.py` → `analysis.ipynb` → `results/results.json` → `deliverables/templates/*.md` (each double-brace placeholder is
filled by `scripts/render_deliverables.py`) → `scripts/check_numbers.py` (fails CI on any number it cannot trace) →
PDFs and website. The website reads the same `results.json` at runtime. The number checker only traces numbers to
`results.json` and binds templated numbers to named keys; it does not prove each number supports the right claim.

## Citing, contributing, security

- Cite with [`CITATION.cff`](CITATION.cff); please also cite Ding & Jiang (arXiv:2407.21723) and the other sources in the memo.
- Contributions: [`CONTRIBUTING.md`](CONTRIBUTING.md) · conduct: [`CODE_OF_CONDUCT.md`](CODE_OF_CONDUCT.md) ·
  security: [`SECURITY.md`](SECURITY.md) · changes: [`CHANGELOG.md`](CHANGELOG.md).
- Disclosure of the case file and sources: [`DISCLOSURE.md`](DISCLOSURE.md).

## License

MIT — see [`LICENSE`](LICENSE). Cited papers, the patent and website fonts keep their own licences.
