"""Reproducible evidence bundle: calculations, SVG figures, tables and memo."""
from __future__ import annotations
import csv
import hashlib
import json
from pathlib import Path

from .chsh import optimal_local_win_rate, quantum_tsirelson_win_rate, one_sided_binomial_tail
from .config import Case, DEFAULT_CASE_PATH, REPOSITORY_ROOT
from .economics import comparison, payoff_surgery
from .frontier import DISTANCES_KM, DEADLINES_MS, grid
from .forensics import conditional_win_rate, required_filter_fraction, retained_fraction, simulate
from .lightcone import great_circle_km, ideal_fibre_ms, vacuum_min_ms, historical_one_way_equivalent_ms
from .photonics import attenuation_db, transmission_probability, upper_bound_received_pair_rate, source_rate_from_observed_at_distance


REGIONS = {
    "classical_one_bit_suffices": ("#21828a", "Classical bit arrives"),
    "no_direct_fibre_supply": ("#d16769", "Direct fibre insufficient"),
    "depends_on_fastest_classical_route": ("#d9aa5b", "Route-dependent"),
    "conditional_physics_candidate": ("#8f82ed", "Quantum physics candidate"),
}


def save_json(path: Path, value: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, sort_keys=True, indent=2) + "\n", encoding="utf-8")


def save_csv(path: Path, data: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(data[0]))
        writer.writeheader()
        writer.writerows(data)


def svg_wrap(body: str, width: int, height: int, label: str) -> str:
    return ('<svg xmlns="http://www.w3.org/2000/svg" role="img" aria-label="' + label +
            '" viewBox="0 0 ' + str(width) + ' ' + str(height) + '">' +
            '<rect width="100%" height="100%" fill="#0a1426"/>' +
            '<g font-family="system-ui,Arial,sans-serif">' + body + '</g></svg>\n')


def frontier_figure(rows: list[dict]) -> str:
    parts = ['<text x="35" y="34" font-size="25" fill="#f4f6ff">THE CAUSAL × OPTICAL FRONTIER</text>',
             '<text x="35" y="58" font-size="13" fill="#a6b6d1">Idealized 1,000 source pairs/s; minimum 1 received pair/s; no repeaters</text>']
    columns = DISTANCES_KM
    deadlines = DEADLINES_MS
    x0, y0, dx, dy = 115, 90, 88, 33
    lookup = {(r["distance_km"], r["deadline_ms"]): r["region"] for r in rows}
    for j, deadline in enumerate(deadlines):
        parts.append('<text x="104" y="' + str(y0+j*dy+22) +
                     '" text-anchor="end" font-size="13" fill="#cdd8ec">' +
                     str(deadline) + '</text>')
        for i, distance in enumerate(columns):
            region = lookup[distance, deadline]
            parts.append('<rect x="' + str(x0+i*dx) + '" y="' + str(y0+j*dy) +
                         '" width="85" height="30" rx="3" fill="' + REGIONS[region][0] + '"/>')
    for i, distance in enumerate(columns):
        parts.append('<text x="' + str(x0+i*dx+42) + '" y="' + str(y0+len(deadlines)*dy+21) +
                     '" text-anchor="middle" font-size="12" fill="#cdd8ec">' + str(distance) + '</text>')
    yy = y0+len(deadlines)*dy+51
    for i, (_, (color, label)) in enumerate(REGIONS.items()):
        x, y = 48+(i%2)*420, yy+(i//2)*27
        parts += ['<rect x="'+str(x)+'" y="'+str(y-11)+'" width="14" height="14" fill="'+color+'"/>',
                  '<text x="'+str(x+22)+'" y="'+str(y)+'" font-size="13" fill="#dae4f7">'+label+'</text>']
    parts += [
        '<text x="510" y="'+str(yy+89)+'" text-anchor="middle" font-size="13" fill="#ced9ed">Distance / modelled optical path (km)</text>',
        '<text x="35" y="'+str(yy+110)+'" font-size="11" fill="#97aac5">Region is a physics sensitivity result, NOT verified profitable trading.</text>'
    ]
    return svg_wrap("".join(parts), 970, yy+125, "Causal versus fibre feasibility sensitivity grid")


def optical_figure() -> str:
    parts = ['<text x="35" y="37" font-size="25" fill="#f4f6ff">THE TRANSATLANTIC LOSS WALL</text>',
             '<text x="35" y="61" font-size="13" fill="#a6b6d1">Standard telecom-fibre illustration at 0.2 dB/km; no repeaters or loss correction</text>']
    x0, y0, width, height = 100, 95, 780, 300
    for decibels in (0, 200, 400, 600, 800, 1000, 1120):
        y = y0 + decibels / 1120 * height
        parts.append('<line x1="100" y1="'+str(y)+'" x2="880" y2="'+str(y)+'" stroke="#24364e"/>')
        parts.append('<text x="88" y="'+str(y+5)+'" text-anchor="end" font-size="13" fill="#b9c9df">'+str(decibels)+'</text>')
    for d in (0, 1000, 2000, 3000, 4000, 5000, 5600):
        x = x0 + d / 5600 * width
        parts.append('<text x="'+str(x)+'" y="421" text-anchor="middle" font-size="12" fill="#b9c9df">'+str(d)+'</text>')
    coords = []
    for d in range(0,5601,100):
        coords.append(str(round(x0+d/5600*width,2))+","+str(round(y0+attenuation_db(d)/1120*height,2)))
    parts.append('<polyline fill="none" stroke="#ebb56d" stroke-width="4" points="'+" ".join(coords)+'"/>')
    parts.append('<text x="490" y="461" text-anchor="middle" font-size="13" fill="#d5e0f0">Fibre distance (km)</text>')
    parts.append('<text x="600" y="488" font-size="13" fill="#ebb56d">5,600 km → 1,120 dB → transmission 10^-112</text>')
    return svg_wrap("".join(parts), 970, 510, "Optical attenuation rises linearly in dB and exponentially in transmission loss")


def payoff_figure() -> str:
    parts = ['<text x="35" y="37" font-size="25" fill="#f4f6ff">PAYOFF SURGERY: THE REFEREE CHANGES</text>',
             '<text x="35" y="61" font-size="13" fill="#a6b6d1">Model assumption: fixed 82% win rate for every setting, independent P(x=1)=P(y=1)=p</text>']
    x0, y0, width, height = 95, 90, 790, 305
    def y_value(edge):
        return y0 + (20-edge)/60*height
    zero_y = y_value(0)
    parts.append('<line x1="95" y1="'+str(zero_y)+'" x2="885" y2="'+str(zero_y)+'" stroke="#c7d2e6" stroke-dasharray="6 4"/>')
    pts = []
    for step in range(81):
        p = .10 + step*.005
        edge = payoff_surgery(p,p)["incremental_usd_per_round"]
        pts.append(str(round(x0+(p-.1)/.4*width,2))+","+str(round(y_value(edge),2)))
    parts.append('<polyline points="'+" ".join(pts)+'" fill="none" stroke="#a996ff" stroke-width="4"/>')
    for p in (.1,.2,.3,.4,.5):
        parts.append('<text x="'+str(x0+(p-.1)/.4*width)+'" y="423" text-anchor="middle" font-size="13" fill="#cbd8ec">'+str(round(p,2))+'</text>')
    parts += ['<text x="80" y="'+str(zero_y+4)+'" text-anchor="end" font-size="13" fill="#cbd8ec">$0</text>',
              '<text x="490" y="458" text-anchor="middle" font-size="13" fill="#cbd8ec">Input bias p</text>',
              '<text x="36" y="484" font-size="11" fill="#98abc6">Illustrative counterfactual, not a quantum optimum or an extrapolation justified by aggregate 82%.</text>']
    return svg_wrap("".join(parts), 970, 506, "Assumed fixed quantum edge falls as CHSH input settings become biased")


def analysis(case: Case = Case()) -> dict:
    geo = great_circle_km()
    q = required_filter_fraction(case.quantum_win_rate)
    return {
        "case_is_fictional": True,
        "chsh": {
            "optimal_local_uniform": optimal_local_win_rate(),
            "ideal_quantum_uniform": quantum_tsirelson_win_rate(),
            "reported_quantum": case.quantum_win_rate,
            "reported_classical": case.startup_classical_win_rate,
            "conditional_complete_trial_p_value": one_sided_binomial_tail(
                case.trials_per_protocol, round(case.trials_per_protocol*case.quantum_win_rate)),
            "p_value_is_invalid_if_only_coincidences_scored": True
        },
        "causality": {
            "geodesic_km": geo, "vacuum_floor_ms": vacuum_min_ms(geo),
            "ideal_straight_fibre_ms": ideal_fibre_ms(geo),
            "historic_half_rtt_ms_not_direct_measurement": historical_one_way_equivalent_ms(),
            "entanglement_cannot_signal_faster_than_light": True
        },
        "optics": {
            "attenuation_db_per_km": .2,
            "direct_fibre_5600km_loss_db": attenuation_db(5600),
            "direct_fibre_5600km_transmission": transmission_probability(5600),
            "best_case_5600km_rate_if_1000_emitted_per_s": upper_bound_received_pair_rate(1000,5600),
            "best_case_5600km_rate_if_1000_received_at_40km": upper_bound_received_pair_rate(
                source_rate_from_observed_at_distance(1000,40),5600),
            "source_or_received_case_pair_rate_ambiguous": True,
            "repeaters_and_satellites_not_modelled": True
        },
        "forensics": {
            "classical_filter_fraction": q,
            "analytical_reported_rate": conditional_win_rate(q),
            "analytical_retained_fraction": retained_fraction(q),
            "seeded_monte_carlo": simulate(100000,q,20261119).to_dict(),
            "loophole_counterexample_is_not_an_accusation": True
        },
        "economics": comparison(case),
        "decision": "Do not fund the proposed trading business on the case evidence; reopen after scientific, network and market gates."
    }


def memo(m:dict) -> str:
    p, c, f, e, q = m["causality"],m["chsh"],m["forensics"],m["economics"],m["optics"]
    return f"""# The 28-Millisecond Monopoly
## Investment committee memo — fictional quantum-trading case
**Decision:** Do not approve the proposed $3M investment at $25M pre-money on the current record. Reopen diligence on measurable milestones.

### The strongest claim
There is a real physics regime in which the two desks cannot exchange a classical message before their answer deadlines. The approximately {p['geodesic_km']:,.0f} km NY–London geodesic imposes a {p['vacuum_floor_ms']:.2f} ms vacuum signal floor and {p['ideal_straight_fibre_ms']:.2f} ms on an idealized equal-length fibre. This does **not** let entanglement carry signals faster than light: it enables pre-shared nonclassical correlations when both decisions are local.

### Reproducible findings
1. **Game-theoretic counterfactual.** Exhaustively searching all 16 deterministic local CHSH response tables gives a {c['optimal_local_uniform']:.0%} optimum versus the claimed {c['reported_quantum']:.0%}. Ideal quantum CHSH can reach {c['ideal_quantum_uniform']:.2%}. Once Alice's bit can reach Bob in time, a deterministic classical strategy wins every round.
2. **Infrastructure feasibility.** Direct unrepeated 5,600 km fibre at 0.2 dB/km implies {q['direct_fibre_5600km_loss_db']:,.0f} dB loss and {q['direct_fibre_5600km_transmission']:.1e} transmission. The case's 40 km, 1,000 pair/s claim does not establish an ocean-scale link; its rate measurement location is also unspecified. Satellite/repeater routes require distinct evidence.
3. **Adversarial falsification.** A perfectly local classical strategy with input-dependent no-click events can report {f['analytical_reported_rate']:.0%} wins after retaining {f['analytical_retained_fraction']:.3%} of issued rounds. This is a counterexample to naive post-selected interpretation, **not an allegation** about the fictional team.
4. **Valuation and demand.** Compared with the *optimal* classical baseline, not the startup's 74% demo, the incremental expected fictional referee-game payoff is only \${e['incremental_usd_per_round']:.3f} per round (after the quoted operating-cost difference). Reaching a claimed $50M in *incremental* benefit requires {e['rounds_for_claimed_opportunity']:,} rounds/year and an actual customer with the exact payoff/deadline structure. That customer has not been shown.

### Statistical caveat
A nominal one-sided binomial tail for 820 successes among 1,000 *complete, independently chosen, non-post-selected trials* is {c['conditional_complete_trial_p_value']:.3g}. If the startup counted only coincident detections, the calculation cannot certify a Bell violation. The case never clarifies which denominator is used.

### Reopening conditions — every condition is mandatory
- **Physics:** publish the trial-level event log, all detector no-clicks, choice RNG/timing, denominator and a valid finite-trial Bell analysis.
- **Operations:** independently validate metropolitan and transatlantic delivered entanglement rate, fidelity, storage/availability, cost, synchronization and classical route competition.
- **Markets:** identify a real order-coordination payoff function, transaction volume, failure costs and unavoidable sub-classical-latency deadline; test the best classical alternative.
- **Option, not endorsement:** investigate certified randomness or quantum-network verification as separate products; a reported 82% alone certifies neither secure keys nor device-independent randomness.

**Recommendation change rule:** consider a gated pilot when scientific, delivery and incremental unit-economics evidence all exist. A patent filing or a scientific advisory board is not commercial validation.

### Materials
Source and assumption register: docs/RESEARCH_SOURCES.md, docs/EVIDENCE_POLICY.md; tables and figure files generated next to this memo. This is a fictional academic exercise, not measured trading profit.
"""


def build(out_dir: str | Path="artifacts", case_path: str | Path=DEFAULT_CASE_PATH) -> dict:
    out = Path(out_dir)
    cp = Path(case_path)
    case = Case.from_json(cp)
    m = analysis(case)
    m["provenance"] = {
        "classification": "fictional_case_plus_explicit_model_assumptions",
        "reproduce": "python -m monopoly build --out artifacts",
        "seed": 20261119, "simulation_rounds": 100000,
        "input_sha256": {str(p.name): hashlib.sha256(p.read_bytes()).hexdigest()
                         for p in (cp, REPOSITORY_ROOT/"data"/"assumptions.json") if p.exists()}
    }
    save_json(out/"metrics.json",m)
    save_csv(out/"tables"/"frontier.csv",grid())
    surgery = []
    for step in range(10,51,2):
        row = payoff_surgery(step/100,step/100)
        row["weights"] = json.dumps(row["weights"])
        surgery.append(row)
    save_csv(out/"tables"/"payoff_surgery.csv",surgery)
    figures = out/"figures"
    figures.mkdir(parents=True,exist_ok=True)
    for name,content in (
        ("frontier.svg", frontier_figure(grid())),
        ("optical_loss.svg", optical_figure()),
        ("payoff_surgery.svg", payoff_figure())
    ):
        (figures/name).write_text(content,encoding="utf-8")
    (out/"EXECUTIVE_MEMO.md").write_text(memo(m),encoding="utf-8")
    (out/"RUN_MANIFEST.md").write_text(
        "# Reproducibility manifest\n\n- Python >=3.11; standard library only.\n"
        "- Inputs: data/case.json, data/assumptions.json (SHA-256 in metrics.json).\n"
        "- Deterministic seed 20261119; forensic simulation of 100,000 issued trials.\n"
        "- The 1,000-trial p-value is conditional on fair complete sampling.\n"
        "- All figures are conditional calculations, not measurements of a trading strategy.\n"
        "- Source references and study limitations: docs/RESEARCH_SOURCES.md.\n",encoding="utf-8")
    return m
