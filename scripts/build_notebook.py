"""Generate analysis.ipynb from the cell list below.

Keeping the notebook as code here makes diffs readable; the .ipynb is the artefact a
grader opens. Run: python scripts/build_notebook.py
"""
from pathlib import Path

import nbformat as nbf

ROOT = Path(__file__).resolve().parents[1]
cells = []


def md(text):
    cells.append(nbf.v4.new_markdown_cell(text.strip()))


def code(text):
    cells.append(nbf.v4.new_code_cell(text.strip()))


md("""
# The Photon That Didn't Show Up — analysis notebook

Investment question: should we put **$3M at a $25M pre-money valuation** into a startup that
sells entanglement-based coordination (the CHSH game) to trading desks?

Every number used in the memo is computed here and written to `results/results.json`.
All randomness uses one fixed seed. The pure functions live in `src/chsh.py` and are
tested in `tests/test_chsh.py`.
""")

code(r'''
import json, math, sys
from pathlib import Path

import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from matplotlib.patches import Patch

ROOT = Path.cwd()
if not (ROOT / "src").exists():          # allow running from a sub-folder
    ROOT = ROOT.parent
sys.path.insert(0, str(ROOT))
from src import chsh

SEED = 20261119                           # fixed seed: every run gives identical numbers
rng = np.random.default_rng(SEED)
N_MC = 1_000_000

(ROOT / "figures").mkdir(exist_ok=True)
(ROOT / "results").mkdir(exist_ok=True)

R = {}   # raw numbers  -> results.json["values"]
D = {}   # display strings used verbatim by the written deliverables -> results.json["display"]

def pct(x, nd=1):
    return f"{100 * x:.{nd}f}%"

# Chart styling: quiet axes, readable type, one palette everywhere.
INK, INK2, GRID = "#0b0b0b", "#52514e", "#e4e3de"
BLUE, ORANGE = "#2a78d6", "#eb6834"
plt.rcParams.update({
    "figure.facecolor": "#fcfcfb", "axes.facecolor": "#fcfcfb", "savefig.facecolor": "#fcfcfb",
    "axes.edgecolor": INK2, "axes.labelcolor": INK, "xtick.color": INK2, "ytick.color": INK2,
    "axes.spines.top": False, "axes.spines.right": False, "font.size": 10,
    "axes.titlesize": 12, "axes.titleweight": "bold", "lines.linewidth": 2,
})

def save(fig, name):
    fig.savefig(ROOT / "figures" / name, dpi=300, bbox_inches="tight")
    print("saved figures/" + name)
''')

md("""
## Case-file inputs (claims, not facts)

These are the numbers the startup gave us. We treat each one as a claim; the claims ledger
records how we read it and what we tested.
""")

code(r'''
CASE = dict(pre_money=25e6, investment=3e6, p_quantum_claim=0.82, p_classical_demo=0.74,
            n_trials=1000, payoff=100.0, cost_quantum=0.08, cost_classical=0.001,
            target_annual=50e6, link_km=40.0, pair_rate=1000.0, global_hft_pool=5e9,
            ny_london_km=5570.0)
R["inputs"] = CASE
R["post_money"] = CASE["pre_money"] + CASE["investment"]
R["stake"] = CASE["investment"] / R["post_money"]
D.update(pre_money="$25M", investment="$3M", post_money="$28M", stake=pct(R["stake"]),
         p_claim="82%", p_demo="74%", n_trials="1,000", payoff="$100",
         target="$50M", link_km="40 km", pair_rate="1,000", global_pool="$5B",
         cost_q="$0.08", cost_c="$0.001", seed=f"{SEED}", n_mc=f"{N_MC:,}",
         ny_lon_km="5,570 km", carteret_km="32 km", nasdaq_km="56 km", fibre_loss="0.2 dB/km",
         det_levels="1.0, 0.9, 0.8", race_window="5–10 µs", eberhard_floor="2/3",
         herald_rtt="58.95 ms")
CASE
''')

md("""
## E1 — The classical limit, checked by brute force

Without any shared quantum resource, the two desks can only agree on a fixed rule in advance.
There are just 16 such rules; we try them all and confirm none wins more than 75% of rounds.
We then ask whether the startup's 82% and 74% are statistically distinguishable from 75%, and
simulate the textbook quantum strategy to confirm it reaches about 85.4%.
""")

code(r'''
strategy_rates = {s: chsh.strategy_win_rate(s) for s in chsh.deterministic_strategies()}
R["classical_max"] = chsh.classical_max()
R["n_strategies"] = len(strategy_rates)
R["n_strategies_at_max"] = sum(abs(v - 0.75) < 1e-12 for v in strategy_rates.values())
R["one_bit_win"] = chsh.one_bit_strategy_win_rate()

n = CASE["n_trials"]
R["z_82"] = chsh.z_score(0.82, n=n)
R["z_74"] = chsh.z_score(0.74, n=n)
# 95% confidence intervals (normal approximation) for what the startup measured
for key, p in (("ci_82", 0.82), ("ci_74", 0.74)):
    half = 1.96 * math.sqrt(p * (1 - p) / n)
    R[key] = (p - half, p + half)

R["quantum_exact"] = chsh.exact_quantum_win()
R["quantum_mc"] = chsh.simulate_quantum(N_MC, rng)
R["tsirelson"] = chsh.IDEAL_QUANTUM_WIN
# Is 82% consistent with an ideal source? (SE under the ideal rate)
R["z_82_vs_ideal"] = (0.82 - R["tsirelson"]) / math.sqrt(R["tsirelson"] * (1 - R["tsirelson"]) / n)

D.update(classical_max="75%", one_bit="100%", z_82=f"{R['z_82']:+.1f}", z_74=f"{R['z_74']:+.1f}",
         ideal_q=pct(R["tsirelson"]), ci_level="95%", ci_74=f"{pct(R['ci_74'][0])}–{pct(R['ci_74'][1])}")
for k in ("classical_max", "n_strategies_at_max", "one_bit_win", "z_82", "z_74", "ci_74",
          "quantum_exact", "quantum_mc", "z_82_vs_ideal"):
    print(f"{k:22s} {R[k]}")
''')

md("""
**Reading E1.** The 16-rule search confirms the 75% ceiling (8 of the 16 rules hit it).
The 82% is about 5 standard errors above 75% — real, if it was counted honestly. The startup's
own classical demo (74%) is statistically indistinguishable from the 75% ceiling, so it is a
fair baseline, not a straw man. And with one classical bit of communication the desks win
every round, which is the bar a trading desk with a shared private line actually faces.
""")

md("""
## E2 — The missing-photon problem (centrepiece)

In a lab, rounds where a photon is lost are thrown away. A trading desk cannot do that: it has
to answer every round, and it cannot tell whether its partner's photon arrived. We model each
desk receiving its photon with probability η; a desk without a photon plays the best fixed
classical answer. We then compute the win rate over **all** rounds on the startup's own 40 km
link, and the efficiency (and hence distance) at which quantum stops beating 75%.

*Simplification:* the "coin-flip" fallback (one photon missing → 50%) is our simple model.
Smarter fallbacks using non-maximally entangled states can push the required efficiency down
toward Eberhard's 2/3 floor; that floor is the **best case** for the startup, so we report it too.
""")

code(r'''
P_LEVELS = {"ideal": chsh.IDEAL_QUANTUM_WIN, "p82": 0.82}
L = CASE["link_km"]
e2 = {}
for name, p_q in P_LEVELS.items():
    eta40 = chsh.fibre_eta(L)
    e_star = chsh.eta_threshold(p_q)
    e2[name] = dict(p_q=p_q, eta_40=eta40, win_40=chsh.all_rounds_win(eta40, p_q),
                    both_share_40=eta40**2, eta_star=e_star,
                    d_max_km=chsh.max_separation_km(e_star))
e2["floor_d_max_km"] = chsh.max_separation_km(chsh.EBERHARD_FLOOR)
e2["light_time_us_at_floor"] = e2["floor_d_max_km"] / chsh.SPEED_OF_LIGHT_KM_S * 1e6
e2["light_time_us_at_p82"] = e2["p82"]["d_max_km"] / chsh.SPEED_OF_LIGHT_KM_S * 1e6

# Monte Carlo that actually drops photons, to validate the formula
for name, p_q in P_LEVELS.items():
    v = chsh.visibility_for_win(p_q)
    all_w, coinc_w, both = chsh.simulate_lossy(N_MC, chsh.fibre_eta(L), rng, visibility=v)
    e2[name].update(mc_all=all_w, mc_coincidence=coinc_w, mc_both=both,
                    mc_abs_error=abs(all_w - e2[name]["win_40"]))

# If the 1,000 trials were coincidence rounds only, how many rounds were attempted?
e2["attempted_rounds_if_postselected"] = CASE["n_trials"] / e2["p82"]["both_share_40"]
# What the 82% source would score on ALL rounds over 40 km, and how far below 75% that is
e2["z_all_rounds_82"] = chsh.z_score(e2["p82"]["win_40"], n=CASE["n_trials"])
R["e2"] = e2
D["mc_err"] = f"{100 * max(e2[k]['mc_abs_error'] for k in P_LEVELS):.2f} percentage points"

D.update(eta_40=f"{e2['ideal']['eta_40']:.3f}", eta_40_pct=pct(e2["ideal"]["eta_40"], 0),
         win40_ideal=pct(e2["ideal"]["win_40"]), win40_82=pct(e2["p82"]["win_40"]),
         both_share=pct(e2["ideal"]["both_share_40"], 0),
         eta_star_ideal=pct(e2["ideal"]["eta_star"]), eta_star_82=pct(e2["p82"]["eta_star"]),
         dmax_ideal=f"{e2['ideal']['d_max_km']:.1f} km", dmax_82=f"{e2['p82']['d_max_km']:.1f} km",
         dmax_floor=f"{e2['floor_d_max_km']:.1f} km",
         attempted=f"{round(e2['attempted_rounds_if_postselected'], -1):,.0f}",
         light_us_82=f"{e2['light_time_us_at_p82']:.0f} µs",
         light_us_floor=f"{e2['light_time_us_at_floor']:.0f} µs")
json.dumps(e2, indent=1)[:1500]
''')

md("""
**Detector-efficiency sensitivity.** The table above assumes perfect detectors, which is generous
to the startup. Real single-photon detectors are below 100% efficient; any loss there multiplies
the fibre loss.
""")

code(r'''
sens = []
for det in (1.0, 0.9, 0.8):
    eta40 = chsh.fibre_eta(L, detector_eff=det)
    row = dict(det=det, eta_40=eta40,
               win40_ideal=chsh.all_rounds_win(eta40, chsh.IDEAL_QUANTUM_WIN),
               win40_82=chsh.all_rounds_win(eta40, 0.82),
               dmax_ideal=chsh.max_separation_km(chsh.eta_threshold(chsh.IDEAL_QUANTUM_WIN), detector_eff=det),
               dmax_82=chsh.max_separation_km(chsh.eta_threshold(0.82), detector_eff=det),
               dmax_floor=chsh.max_separation_km(chsh.EBERHARD_FLOOR, detector_eff=det))
    sens.append(row)
R["detector_sensitivity"] = sens
D["dmax_82_det09"] = f"{sens[1]['dmax_82']:.1f} km"

# Where is the all-rounds win rate lowest? d(win)/d(eta) = 0 at eta = 0.25 / (p_q - 0.25).
# Beyond that distance both photons are usually lost, both desks play the classical rule,
# and the win rate drifts back UP toward (never above) 75%. This is why a longer route
# can score slightly higher than the 40 km link.
eta_worst = 0.25 / (0.82 - 0.25)
R["worst_distance_km_82"] = chsh.max_separation_km(eta_worst)
R["worst_win_82"] = chsh.all_rounds_win(eta_worst, 0.82)
D["worst_km"] = f"{R['worst_distance_km_82']:.0f} km"

# Fibre-loss sensitivity: 0.17 dB/km is the figure Ding & Jiang use; 0.1 dB/km is a
# hypothetical far-better fibre, included to show how much headroom better glass buys.
loss_rows = []
for loss in (0.2, 0.17, 0.1):
    loss_rows.append(dict(loss_db_per_km=loss,
        dmax_82=chsh.max_separation_km(chsh.eta_threshold(0.82), loss_db_per_km=loss),
        dmax_ideal=chsh.max_separation_km(chsh.eta_threshold(chsh.IDEAL_QUANTUM_WIN), loss_db_per_km=loss),
        dmax_floor=chsh.max_separation_km(chsh.EBERHARD_FLOOR, loss_db_per_km=loss)))
R["fibre_loss_sensitivity"] = loss_rows
D.update(dmax_82_017=f"{loss_rows[1]['dmax_82']:.1f} km", dmax_floor_017=f"{loss_rows[1]['dmax_floor']:.1f} km",
         dmax_82_010=f"{loss_rows[2]['dmax_82']:.1f} km", dmax_floor_010=f"{loss_rows[2]['dmax_floor']:.1f} km",
         loss_017="0.17 dB/km", loss_010="0.1 dB/km")
print("worst distance (82%):", R["worst_distance_km_82"], "km, win", R["worst_win_82"])
for r in loss_rows:
    print(r)
print(f"{'det':>4} {'eta40':>7} {'win40 ideal':>12} {'win40 82%':>10} {'dmax ideal':>11} {'dmax 82%':>9} {'dmax 2/3':>9}")
for r in sens:
    print(f"{r['det']:4.1f} {r['eta_40']:7.3f} {r['win40_ideal']:12.3f} {r['win40_82']:10.3f} "
          f"{r['dmax_ideal']:9.1f}km {r['dmax_82']:7.1f}km {r['dmax_floor']:7.1f}km")
''')

code(r'''
eta = np.linspace(0, 1, 401)
fig, ax = plt.subplots(figsize=(7.5, 4.6))
for (name, p_q), color, label in zip(P_LEVELS.items(), (BLUE, ORANGE),
                                     ("Ideal source (85.4% when both photons arrive)",
                                      "Startup-quality source (82% when both arrive)")):
    ax.plot(eta, chsh.all_rounds_win(eta, p_q), color=color, label=label)
    es = e2[name]["eta_star"]
    ax.plot([es], [0.75], "o", ms=7, color=color, mec="#fcfcfb", mew=2, zorder=5)
    xytext, ha = ((0.93, 0.70), "center") if name == "p82" else ((0.74, 0.80), "right")
    ax.annotate(f"break-even η = {es:.3f}", (es, 0.75), xytext=xytext,
                ha=ha, fontsize=9, color=INK2, arrowprops=dict(arrowstyle="-", color=INK2, lw=0.8))
ax.axhline(0.75, color=INK, lw=1.2, ls="--")
ax.text(0.02, 0.757, "Best classical strategy, no communication: 75%", fontsize=9, color=INK)
eta40 = e2["ideal"]["eta_40"]
ax.axvline(eta40, color=INK2, lw=1, ls=":")
ax.text(eta40 + 0.01, 0.56, f"Startup's 40 km link\nη = {eta40:.3f} per desk\n→ {pct(e2['ideal']['win_40'])} (ideal), "
        f"{pct(e2['p82']['win_40'])} (82% source)", fontsize=9, color=INK, va="bottom")
ax.set_xlim(0, 1); ax.set_ylim(0.5, 0.88)
ax.set_xlabel("Per-desk photon delivery efficiency η (fraction of photons that arrive and are detected)")
ax.set_ylabel("Win rate over ALL rounds")
ax.yaxis.set_major_formatter(matplotlib.ticker.PercentFormatter(1.0, decimals=0))
ax.grid(color=GRID, lw=0.6); ax.set_axisbelow(True)
leg = ax.legend(loc="lower left", frameon=True, fontsize=9, facecolor="#fcfcfb", edgecolor="none", framealpha=1)
leg.set_zorder(10)
ax.set_title("On its own 40 km link, the quantum strategy loses to the 75% classical rule", loc="left")
save(fig, "e2_win_vs_efficiency.png")
plt.show()
''')

md("""
**Reading E2.** *Under this unheralded fibre model* (midpoint source, independent loss, fixed
fallback answer, perfect detectors), only about one round in six on the 40 km link has both photons
arrive, and counting every round the modelled strategy wins well under 75%. For the modelled 82%
strategy to beat 75%, the desks must sit within a few kilometres; other strategies have other
limits (ideal source, Eberhard's tuned states, heralding: see below). The Monte
Carlo (which really drops photons) agrees with the formula to the third decimal, and its
coincidence-only win rate reproduces the "lab" number: an 82% *coincidence* rate is consistent with
this link, an 82% *all-rounds* rate is not. The startup's actual denominator and protocol are
unverified, which is why it is founder question 1.
""")

md("""
## E2b — Founder-rescue scenario: heralded delivery with quantum memories

The startup has **not** claimed quantum memories, but it is the obvious rescue argument. If each
desk stores its photon in a memory and a classical "herald" signal confirms both arrived *before*
the round, the desks know in advance whether to play quantum or classical. Lost pairs then cost
nothing: a round without a heralded pair simply uses the 75% classical rule.
""")

code(r'''
H_LEVELS = [0.05, 0.158, 0.5, 1.0]
# How much heralded supply does the link actually provide? Demand = the rounds needed for the
# claimed $50M, spread over one trading year (252 days x 6.5 h; our assumption, A18).
TRADING_SECONDS = 252 * 6.5 * 3600
rounds_needed = chsh.rounds_for_target(CASE["target_annual"], chsh.edge_per_round(0.82))
demand_per_s = rounds_needed / TRADING_SECONDS
supply_rows = [dict(route=name, km=km,
                    heralded_pairs_per_s=CASE["pair_rate"] * chsh.fibre_eta(km) ** 2,
                    h_max=chsh.heralded_supply_fraction(km, demand_per_s, CASE["pair_rate"]))
               for name, km in [("Startup 40 km link", 40.0), ("NYSE–Nasdaq", 56.0),
                                ("New York–London (direct fibre)", CASE["ny_london_km"])]]
heralded = [dict(h=h, win_82=chsh.heralded_win(h, 0.82), win_ideal=chsh.heralded_win(h, chsh.IDEAL_QUANTUM_WIN),
                 edge_82=chsh.edge_per_round(chsh.heralded_win(h, 0.82))) for h in H_LEVELS]
# Rate budget on the 40 km link: heralded pairs/s = generated pairs/s x both-arrive probability
herald_rate_40 = CASE["pair_rate"] * e2["p82"]["both_share_40"]
R["e2b"] = dict(table=heralded, heralded_pairs_per_s_40km=herald_rate_40,
                demand_rounds_per_s=demand_per_s, supply=supply_rows,
                memories_claimed=False)
D.update(demand_per_s=f"{demand_per_s:.2f}", trading_year="252 days × 6.5 hours", fibre_index="c/1.47",
         h_max_ny_lon=f"{supply_rows[2]['h_max']:.0e}",
         herald_rate=f"{herald_rate_40:.0f}",
         heralded_win_full=pct(chsh.heralded_win(1.0, 0.82)))
for r in heralded:
    print(f"h={r['h']:.3f}  win(82%)={r['win_82']:.4f}  win(ideal)={r['win_ideal']:.4f}  edge(82%)=${r['edge_82']:.2f}")
print("heralded pairs/s on 40 km:", herald_rate_40)
print(f"demand: {demand_per_s:.3f} rounds/s")
for r in supply_rows:
    print(f"{r['route']:32s} supply {r['heralded_pairs_per_s']:.3g} pairs/s -> h_max {r['h_max']:.3g}")
''')

md("""
**Reading E2b.** With heralding, any fraction of good rounds helps, so photon loss stops being
fatal: the win rate never drops below 75%. But the heralded fraction is capped by what the link
supplies. Even with perfect, lossless memories, the 40 km link covers the claimed volume, while direct
fibre across the Atlantic supplies essentially nothing (h ≈ 1e-108), so a transatlantic heralded
service would need repeaters or satellites that the startup has not claimed. Heralding changes
*which* product could work; it does not validate this one.
""")

md("""
## E3 — A classical cheater that scores 82% (the detection loophole)

If rounds can be discarded, a purely classical pair of desks can fake a quantum-looking score.
Both desks always answer 0 (losing only when x = y = 1); whenever desk A sees x = 1 it claims
"no photon" with probability 0.4375. This uses no entanglement and no communication — only the
right to drop rounds.
""")

code(r'''
all_w, det_w, kept = chsh.simulate_cheater(N_MC, rng)
exact = chsh.cheater_exact()
R["e3"] = dict(mc_all=all_w, mc_detected=det_w, mc_retained=kept,
               exact_all=exact[0], exact_detected=exact[1], exact_retained=exact[2], q=0.4375)
D.update(cheat_all=pct(exact[0], 0), cheat_det=pct(exact[1], 0), cheat_kept=pct(exact[2], 1))
R["e3"]
''')

md("""
**Reading E3.** A classical trick hits exactly 82% on "detected" rounds while keeping about 78%
of them. So an 82% figure alone proves nothing unless the startup also reports how many rounds
were attempted and how many were thrown away.
""")

md("""
## E4 — Frontier map (MAIN FIGURE)

Where on the map of *distance between desks* × *time allowed to decide* could entanglement ever
pay? We separate three causal states for one classical bit: **physically excluded** (window
< d/c: shorter than light needs), **route-dependent** (d/c ≤ window < 1.47·d/c: physics allows it,
but the modelled straight-line fibre route at c/1.47 is too slow; a faster route might not be,
hatched), and **classical arrives** (window ≥ 1.47·d/c, grey: one bit wins every round).
New York–London uses half the Hibernia round-trip benchmark (29.5 ms) as its route latency. Where no bit arrives on the
modelled route, the coloured bands show whether the modelled *unheralded* strategies can beat 75%.
""")

code(r'''
LANDMARKS = [("Carteret–Secaucus", 32.0), ("Startup 40 km test link", 40.0),
             ("NYSE–Nasdaq", 56.0), ("New York–London", CASE["ny_london_km"])]
c = chsh.SPEED_OF_LIGHT_KM_S

d = np.logspace(0, 4, 900)            # 1 km .. 10,000 km
w = np.logspace(-6, -1, 700)          # 1 us .. 100 ms
DD, WW = np.meshgrid(d, w)
region = chsh.frontier_region(DD, WW, p_demo=0.82)        # grey = bit arrives on modelled fibre route
causal = chsh.causal_status(DD, WW)
HIBERNIA_ONE_WAY_S = 58.95e-3 / 2       # derived from the 2015 round-trip benchmark, not a measured one-way service

colors = ["#d6d5cf", "#efa596", "#f6d27a", "#8ccf8c"]     # grey, red, yellow, green
fig, ax = plt.subplots(figsize=(10, 6.4))
ax.pcolormesh(d, w * 1e6, region, cmap=ListedColormap(colors), vmin=-0.5, vmax=3.5,
              shading="auto", rasterized=True)
ax.set_xscale("log"); ax.set_yscale("log")
# route-dependent band: hatched over whatever the loss model says
matplotlib.rcParams["hatch.color"] = "#5f5e5a"; matplotlib.rcParams["hatch.linewidth"] = 0.6
ax.contourf(d, w * 1e6, (causal == chsh.CAUSAL_ROUTE_DEPENDENT).astype(float), levels=[0.5, 1.5],
            colors="none", hatches=["////"])
ax.plot(d, d / c * 1e6, color=INK, lw=1.2)                                   # physical limit d/c
ax.plot(d, chsh.route_latency_s(d) * 1e6, color=INK, lw=1.0, ls="--")        # modelled fibre route
ax.set_xlim(1, 1e4); ax.set_ylim(1, 1e5)
# rotate the boundary label to match the line's on-screen slope
p1, p2 = ax.transData.transform([(100, 100 / c * 1e6), (1000, 1000 / c * 1e6)])
angle = math.degrees(math.atan2(p2[1] - p1[1], p2[0] - p1[0]))
ax.text(180, 180 / chsh.FIBRE_SPEED_KM_S * 1e6 * 1.35, "bit arrives on straight-line fibre (c/1.47)", rotation=angle,
        rotation_mode="anchor", fontsize=8.5, color=INK, ha="left", va="bottom")
ax.text(250, 250 / c * 1e6 * 0.62, "physical limit: light-travel time d/c", rotation=angle,
        rotation_mode="anchor", fontsize=8.5, color=INK, ha="left", va="top")
# New York-London on the benchmarked Hibernia route (derived one-way figure)
ax.plot([CASE["ny_london_km"]], [HIBERNIA_ONE_WAY_S * 1e6], "o", ms=6, color=INK, mec="#fcfcfb", mew=1.5, zorder=6)
ax.text(CASE["ny_london_km"] * 0.93, HIBERNIA_ONE_WAY_S * 1e6 * 1.25, "Hibernia ~29.5 ms\n(½ of 58.95 ms RTT)",
        fontsize=7.5, ha="right", va="bottom", color=INK)

# typical latency-arbitrage race (Aquilina, Budish & O'Neill 2022)
ax.axhspan(5, 10, color=BLUE, alpha=0.22, lw=0)
ax.text(90, 7.1, "typical latency-arbitrage race (5–10 µs)", fontsize=9, color="#104281",
        va="center", ha="left", fontweight="bold")

# landmark lines with labels inside the plot, in the grey area, staggered left/right
label_side = {"Carteret–Secaucus": ("right", 0.95), "Startup 40 km test link": ("left", 1.05),
              "NYSE–Nasdaq": ("left", 1.05), "New York–London": ("right", 0.95)}
for name, km in LANDMARKS:
    ax.axvline(km, color=INK, lw=1, ls="--" if "Startup" in name else "-", alpha=0.85)
    ha, fx = label_side[name]
    ax.text(km * fx, 1.2e4 if km < 1000 else 1.5e2, f"{name} (~{km:,.0f} km)", rotation=90,
            fontsize=8.5, ha=ha, va="center", color=INK)

# direct region labels (the legend repeats them with numbers)
ax.text(1.12, 4e3, "GREY: one classical bit arrives\non the modelled route,\nclassical wins 100%",
        fontsize=9.5, ha="left", va="center", color=INK)
ax.text(400, 22, "RED: no bit on the modelled route, and too many\nphotons lost for quantum to beat 75%",
        fontsize=10, ha="center", color="#7a1f17")
dmax82, dfloor = e2["p82"]["d_max_km"], e2["floor_d_max_km"]
ax.text(2.35, 1.75, "GREEN\n82% strategy\nbeats 75%", fontsize=8, ha="center", va="center", color="#0b4f0b")
ax.text(10.0, 1.75, "YELLOW\nnear-perfect\ntuned source", fontsize=8, ha="center", va="center", color="#6b4e00")


ax.set_xlabel("Distance between the two desks (km, log scale)")
ax.set_ylabel("Time allowed to make the decision (log scale)")
ax.set_yticks([1, 10, 100, 1e3, 1e4, 1e5])
ax.set_yticklabels(["1 µs", "10 µs", "100 µs", "1 ms", "10 ms", "100 ms"])
ax.set_xticks([1, 10, 100, 1e3, 1e4]); ax.set_xticklabels(["1", "10", "100", "1,000", "10,000"])
ax.spines["top"].set_visible(True); ax.spines["right"].set_visible(True)

legend = [Patch(color=colors[0], label="Grey: bit arrives on modelled fibre route, classical wins 100%"),
          Patch(facecolor="none", edgecolor="#5f5e5a", hatch="////", label="Hatched: route-dependent (physics allows a bit; modelled route too slow)"),
          Patch(color=colors[1], label="Red: photon loss too high, quantum cannot beat 75%"),
          Patch(color=colors[2], label=f"Yellow: only a near-perfect tuned source (2/3 floor, < {dfloor:.1f} km)"),
          Patch(color=colors[3], label=f"Green: modelled 82% strategy beats 75% (< {dmax82:.1f} km)"),
          Patch(color=BLUE, alpha=0.22, label="Typical latency-arbitrage race")]
ax.legend(handles=legend, loc="upper center", bbox_to_anchor=(0.5, -0.10), ncol=2,
          frameon=False, fontsize=8.5)
fig.suptitle("On every route we checked, photon loss or one classical bit beats the modelled quantum strategy\n"
             f"Unheralded fibre model: the 82% strategy beats 75% only below ~{dmax82:.1f} km and ~{dmax82 / c * 1e6:.0f} µs — the startup's 40 km link is red",
             x=0.08, y=0.985, ha="left", fontsize=12, fontweight="bold")
fig.text(0.08, -0.145,
         "Distances are approximate straight-line figures. Loss model: unheralded delivery, entangled source at the midpoint, 0.2 dB/km fibre, perfect "
         "detectors (generous to the startup),\nfixed fallback answer when a photon is missing. Grey uses a straight-line fibre route at c/1.47; "
         "hatched = physics allows a bit but that route is too slow. Yellow uses Eberhard's 2/3\nefficiency floor (best case, specially tuned states). "
         "Red includes long routes that fall back to exactly 75%. Heralded delivery with quantum memories is not shown (see E2b).",
         fontsize=8, color=INK2, ha="left")
save(fig, "main_frontier.png")
plt.show()

landmark_rows = []
for name, km in LANDMARKS:
    eta_l = chsh.fibre_eta(km)
    landmark_rows.append(dict(name=name, km=km, light_time_us=km / c * 1e6, eta=eta_l,
                              win_all_rounds_82=chsh.all_rounds_win(eta_l, 0.82),
                              region_at_7_5us=int(chsh.frontier_region(km, 7.5e-6)),
                              region_at_1ms=int(chsh.frontier_region(km, 1e-3)),
                              causal_at_20ms=int(chsh.causal_status(km, 20e-3,
                                  HIBERNIA_ONE_WAY_S if "London" in name else None))))
R["e4_landmarks"] = landmark_rows
R["ny_london_light_ms"] = CASE["ny_london_km"] / c * 1e3
R["hibernia_rtt_ms"] = 58.95
R["hibernia_one_way_ms"] = 58.95 / 2
D.update(ny_lon_light_ms=f"{R['ny_london_light_ms']:.1f} ms", hibernia_one_way=f"{R['hibernia_one_way_ms']:.1f} ms",
         nasdaq_win=pct(landmark_rows[2]["win_all_rounds_82"]),
         carteret_win=pct(landmark_rows[0]["win_all_rounds_82"]),
         nasdaq_light_us=f"{landmark_rows[2]['light_time_us']:.0f} µs",
         dmax82_round=f"{dmax82:.0f} km", green_us=f"{dmax82 / c * 1e6:.0f} µs")
for r in landmark_rows:
    print(r)

# Shared-spec state table: causal state name and loss region for each landmark and window.
# New York-London uses the Hibernia route latency; the metro routes use straight fibre at c/1.47.
STATE_WINDOWS = [("7.5 µs", 7.5e-6), ("1 ms", 1e-3), ("20 ms", 20e-3), ("100 ms", 100e-3)]
frontier_states = []
for name, km in LANDMARKS:
    rl = HIBERNIA_ONE_WAY_S if "London" in name else None
    for wlabel, wsec in STATE_WINDOWS:
        frontier_states.append(dict(
            landmark=name, km=km, window=wlabel, window_s=wsec,
            route_latency_s=float(chsh.route_latency_s(km, rl)),
            causal_state=chsh.CAUSAL_STATE_NAMES[int(chsh.causal_status(km, wsec, rl))],
            loss_region=chsh.REGION_NAMES[int(chsh.loss_region(km))],
            frontier_region=chsh.REGION_NAMES[int(chsh.frontier_region(km, wsec, route_latency=rl))]))
R["frontier_states"] = frontier_states
print(f"{'landmark':26s} {'window':>7s}  {'causal state':20s} {'loss':6s} frontier")
for r in frontier_states:
    print(f"{r['landmark']:26s} {r['window']:>7s}  {r['causal_state']:20s} {r['loss_region']:6s} {r['frontier_region']}")
''')

md("""
**Reading E4.** New York–London depends on the decision window. Above ~29.5 ms (half the Hibernia
round-trip benchmark) one bit arrives over existing cable and wins every round. Between ~18.6 ms
(light in vacuum) and ~29.5 ms it is route-dependent: a faster path could deliver the bit, the
benchmarked cable does not. Below ~18.6 ms no bit can arrive, but direct-fibre photon loss leaves
the modelled quantum strategy at 75%, no better than classical. Every metro route we checked
(32–56 km) is red whenever the bit cannot arrive. Under the unheralded model, the region where the
82% strategy wins is a few kilometres wide and, where physics rules out any bit, under ~19 µs tall.
""")

md("""
## E4b — Sensitivity: the photon source sits at one desk, not halfway

So far we put the entangled-photon source at the midpoint, so each photon crosses half the
distance. A real deployment might put the source inside one desk's building instead: that desk's
photon is (almost) never lost, but the other photon must cross the full distance. This section
checks whether that placement gives the startup more range or less.

*Model:* near desk η = 1, far desk η_far = det·10^(−0.2·d/10), same fixed fallback (no photon → answer 0).
Then win = η_far·p_q + (1 − η_far)·0.5, which beats 75% only if η_far > 0.25/(p_q − 0.5): 1/√2 for an ideal
maximally entangled source. With optimised partially entangled states the known asymmetric bound
(one perfect detector) is η_far > 1/2. We verify the first with a Monte Carlo that drops only the far
photon, and the second with a numerical optimiser over partially entangled states.
""")

code(r'''
e4b = {}
for name, p_q in P_LEVELS.items():
    e_star = chsh.endpoint_eta_threshold(p_q)
    e4b[name] = dict(p_q=p_q, eta_far_star=e_star, d_max_km=chsh.endpoint_max_separation_km(e_star),
                     midpoint_d_max_km=e2[name]["d_max_km"])
e4b["partial"] = dict(eta_far_star=chsh.ENDPOINT_PARTIAL_ETA_FLOOR,
                      d_max_km=chsh.endpoint_max_separation_km(chsh.ENDPOINT_PARTIAL_ETA_FLOOR),
                      midpoint_d_max_km=e2["floor_d_max_km"])

# Monte Carlo (singlet sampler, only the far photon is dropped) vs the closed form,
# at the ideal break-even distance and on the 40 km link.
mc_rows = []
for name, p_q in P_LEVELS.items():
    v = chsh.visibility_for_win(p_q)
    for d_km in (e4b[name]["d_max_km"], CASE["link_km"]):
        eta_f = float(chsh.endpoint_fibre_eta(d_km))
        mc = chsh.simulate_endpoint_lossy(N_MC, eta_f, rng, visibility=v)
        exact = chsh.endpoint_all_rounds_win(eta_f, p_q)
        mc_rows.append(dict(source=name, d_km=d_km, eta_far=eta_f, exact=exact, mc=mc, abs_error=abs(mc - exact)))
e4b["monte_carlo"] = mc_rows

# Partially entangled states cos(t)|HH> + sin(t)|VV>: optimise angles and B's fallback answer.
partial_rows = []
for t in (math.pi / 4, 0.5, 0.3, 0.15, 0.05):
    thr, params = chsh.endpoint_partial_eta_threshold(t, rng, starts=8)
    partial_rows.append(dict(theta=t, eta_far_star=round(thr, 6),
                             d_max_km=round(chsh.endpoint_max_separation_km(thr), 4)))
e4b["partial_numeric"] = partial_rows
R["e4b"] = e4b
R["endpoint_source_max_km_max_ent"] = e4b["ideal"]["d_max_km"]
R["endpoint_source_max_km_82"] = e4b["p82"]["d_max_km"]
R["endpoint_source_max_km_partial"] = e4b["partial"]["d_max_km"]
R["midpoint_favours_startup"] = all(e4b[k]["midpoint_d_max_km"] > e4b[k]["d_max_km"]
                                    for k in ("ideal", "p82", "partial"))
D.update(endpoint_source_max_km_max_ent=f"{R['endpoint_source_max_km_max_ent']:.1f} km",
         endpoint_source_max_km_82=f"{R['endpoint_source_max_km_82']:.1f} km",
         endpoint_source_max_km_partial=f"{R['endpoint_source_max_km_partial']:.1f} km",
         endpoint_eta_max_ent=f"{e4b['ideal']['eta_far_star']:.3f}",
         endpoint_eta_82=f"{e4b['p82']['eta_far_star']:.3f}",
         endpoint_eta_partial="1/2",
         endpoint_mc_err=f"{100 * max(r['abs_error'] for r in mc_rows):.2f} percentage points")

print(f"{'source':10s} {'eta_far*':>9s} {'endpoint d_max':>15s} {'midpoint d_max':>15s}")
for k in ("ideal", "p82", "partial"):
    print(f"{k:10s} {e4b[k]['eta_far_star']:9.4f} {e4b[k]['d_max_km']:13.2f}km {e4b[k]['midpoint_d_max_km']:13.2f}km")
for r in mc_rows:
    print(f"MC {r['source']:6s} d={r['d_km']:6.2f} km  exact={r['exact']:.4f}  mc={r['mc']:.4f}")
for r in partial_rows:
    print(f"partial theta={r['theta']:.3f}  eta_far*={r['eta_far_star']:.4f}  d_max={r['d_max_km']:.2f} km")
print("midpoint assumption favours the startup:", R["midpoint_favours_startup"])
''')

md("""
**Reading E4b.** The derivation, the Monte Carlo and the optimiser agree: with the source at one desk
the ideal maximally entangled strategy beats 75% only within about 7.5 km (82% source: about 5.4 km),
and even optimised partially entangled states stop at about 15.1 km, where the threshold approaches
1/2 only as the entanglement (and the advantage) shrinks to nothing. All three are shorter than the
midpoint figures (8.2, 5.7 and 17.6 km), so the midpoint assumption used everywhere else is the one
that favours the startup. The 40 km link stays red either way.
""")

md("""
## E5 — What if the trade's "signals" aren't 50/50?

The textbook game assumes each desk's signal is on half the time. Real trading signals are
rarely that balanced. Using the closed form of Ding & Jiang (Theorem 10), we compute how the
quantum edge changes when each desk's signal is on with probability p, and check the theorem
against a brute-force classical search and a numerical quantum optimiser.
""")

code(r'''
ps = np.linspace(0, 1, 1001)
cl = np.array([chsh.biased_classical(p) for p in ps])
qu = np.array([chsh.biased_quantum(p) for p in ps])
gap = qu - cl
lo, hi = 1 - 1 / math.sqrt(2), 1 / math.sqrt(2)

check_ps = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
brute_err = max(abs(chsh.classical_max(p) - chsh.biased_classical(p)) for p in check_ps)
numeric_err = max(abs(chsh.biased_quantum_numeric(p, rng) - chsh.biased_quantum(p)) for p in check_ps)
R["e5"] = dict(gap_at_half=chsh.biased_quantum(0.5) - chsh.biased_classical(0.5),
               advantage_lo=lo, advantage_hi=hi, max_gap=float(gap.max()),
               gap_at_0_35=chsh.biased_quantum(0.35) - chsh.biased_classical(0.35),
               # Rounded: optimiser noise at ~1e-13 differs across BLAS/CPU builds, and
               # results.json must be byte-identical on every machine.
               classical_bruteforce_max_err=round(brute_err, 9), quantum_numeric_max_err=round(numeric_err, 9))
D.update(gap_half=f"{100 * R['e5']['gap_at_half']:.1f} percentage points",
         adv_lo=f"{lo:.2f}", adv_hi=f"{hi:.2f}",
         adv_lo_pct=pct(lo, 0), adv_hi_pct=pct(hi, 0))

fig, ax = plt.subplots(figsize=(7.5, 4.2))
ax.fill_between(ps, 0, gap * 100, color=BLUE, alpha=0.18, lw=0)
ax.plot(ps, gap * 100, color=BLUE)
ax.axvspan(0, lo, color="#d6d5cf", alpha=0.5, lw=0); ax.axvspan(hi, 1, color="#d6d5cf", alpha=0.5, lw=0)
ax.text(lo / 2, 6, "no quantum\nadvantage", ha="center", fontsize=9, color=INK2)
ax.text((1 + hi) / 2, 6, "no quantum\nadvantage", ha="center", fontsize=9, color=INK2)
ax.annotate(f"{100 * R['e5']['gap_at_half']:.1f} points at p = 0.5", (0.5, gap.max() * 100),
            xytext=(0.5, 11.6), ha="center", fontsize=9, color=INK)
ax.set_xlim(0, 1); ax.set_ylim(0, 13)
ax.set_xlabel("Probability p that each desk's signal is 'on' (input = 1)")
ax.set_ylabel("Quantum win rate minus classical\n(percentage points)")
ax.grid(color=GRID, lw=0.6); ax.set_axisbelow(True)
ax.set_title(f"The edge exists only when signals fire {lo:.0%}–{hi:.0%} of the time", loc="left")
save(fig, "e5_biased_inputs.png")
plt.show()
R["e5"]
''')

md("""
**Reading E5.** The advantage is largest for perfectly balanced signals and vanishes completely
if a signal fires less than about 29% or more than about 71% of the time. The startup has not
named a trade, so we cannot say where a real signal would fall — which is one of our questions
for the founders.
""")

md("""
## E6 — Economics

We take the case's invented payoff (+$100 per win, −$100 per loss) at face value and ask how
many rounds a year it would take to earn the claimed $50M, and how that compares with the whole
global latency-arbitrage pie. Then we redo the sum with the all-rounds win rate from E2.
""")

code(r'''
edge_claim = chsh.edge_per_round(0.82)
rounds = chsh.rounds_for_target(CASE["target_annual"], edge_claim)
edge_all_82 = chsh.edge_per_round(e2["p82"]["win_40"])
edge_all_ideal = chsh.edge_per_round(e2["ideal"]["win_40"])
R["e6"] = dict(edge_claim=edge_claim, rounds_for_target=rounds,
               hours_if_rate_is_delivered_rounds=chsh.hours_to_generate(rounds),
               hours_if_rate_is_generated_pairs=chsh.hours_to_generate(rounds, usable_fraction=e2["p82"]["both_share_40"]),
               edge_all_rounds_82=edge_all_82, edge_all_rounds_ideal=edge_all_ideal,
               annual_loss_at_target_volume=edge_all_82 * rounds,
               share_of_global_pool=CASE["target_annual"] / CASE["global_hft_pool"],
               payoff_is_invented=True)
D.update(edge_claim=f"${edge_claim:.2f}", edge_claim_exact=f"${edge_claim:.3f}",
         rounds=f"{rounds / 1e6:.2f} million",
         hours_delivered=f"{R['e6']['hours_if_rate_is_delivered_rounds']:.1f} hours",
         hours_generated=f"{R['e6']['hours_if_rate_is_generated_pairs']:.1f} hours",
         edge_all_82=f"−${abs(edge_all_82):.2f}",
         annual_loss=f"${abs(R['e6']['annual_loss_at_target_volume']) / 1e6:.0f}M",
         share_pool=pct(R["e6"]["share_of_global_pool"]))
R["e6"]
''')

md("""
**Reading E6.** On the startup's own accounting the edge is about $14 a round, so $50M needs about
3.6 million rounds a year — roughly an hour of pair generation, so pair rate is not the
bottleneck. But $50M is 1% of the *entire* global equities latency-arbitrage pie, captured by a
game whose payoff no one has tied to a real trade. Counting every round on the 40 km link,
the edge turns negative: the same volume would *lose* money.
""")

md("""
## Hand re-derivation (independent of `src/chsh.py`)

Plain arithmetic, written out, to check the library against the brief's expected values.
""")

code(r'''
eta_h = 10 ** (-0.2 * 40 / 20)
q_h = math.cos(math.pi / 8) ** 2
checks = {
    "eta_40":        (eta_h, R["e2"]["ideal"]["eta_40"]),
    "win40_ideal":   (eta_h**2 * q_h + eta_h * (1 - eta_h) + 0.75 * (1 - eta_h) ** 2, R["e2"]["ideal"]["win_40"]),
    "eta_star_82":   (0.5 / 0.57, R["e2"]["p82"]["eta_star"]),
    "dmax_82":       (-100 * math.log10(0.5 / 0.57), R["e2"]["p82"]["d_max_km"]),
    "dmax_floor":    (-100 * math.log10(2 / 3), R["e2"]["floor_d_max_km"]),
    "z_82":          (0.07 / math.sqrt(0.1875 / 1000), R["z_82"]),
    "cheat_detect":  (1 - 0.25 * 0.5625 / 0.78125, R["e3"]["exact_detected"]),
    "edge":          (200 * 0.07 - 0.079, R["e6"]["edge_claim"]),
    "rounds":        (50e6 / 13.921, R["e6"]["rounds_for_target"]),
    "endpoint_ideal": (-50 * math.log10(1 / math.sqrt(2)), R["endpoint_source_max_km_max_ent"]),
    "endpoint_82":   (-50 * math.log10(0.25 / 0.32), R["endpoint_source_max_km_82"]),
    "endpoint_part": (-50 * math.log10(0.5), R["endpoint_source_max_km_partial"]),
}
for k, (hand, lib) in checks.items():
    assert math.isclose(hand, lib, rel_tol=1e-9, abs_tol=1e-12), k
    print(f"{k:14s} hand={hand:.6f}  library={lib:.6f}  OK")
R["hand_checks_passed"] = True
''')

md("""
## Save results

`results/results.json` holds every raw value (`values`) and the exact display strings the
written deliverables use (`display`). `scripts/render_deliverables.py` fills the memo from it and
`scripts/check_numbers.py` confirms every number in the memo is traceable to this file.
""")

code(r'''
def to_jsonable(o):
    if isinstance(o, dict):
        return {k: to_jsonable(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [to_jsonable(v) for v in o]
    if isinstance(o, (np.floating, np.integer)):
        return o.item()
    return o

out = {"seed": SEED, "n_monte_carlo": N_MC, "values": to_jsonable(R), "display": D}
(ROOT / "results" / "results.json").write_text(json.dumps(out, indent=2, ensure_ascii=False))
print(f"wrote results/results.json with {len(D)} display strings")
''')

nb = nbf.v4.new_notebook()
nb["cells"] = cells
nb["metadata"]["kernelspec"] = {"name": "python3", "display_name": "Python 3", "language": "python"}
nbf.write(nb, ROOT / "analysis.ipynb")
print("wrote analysis.ipynb")
