"""Python-browser parity: site/model.js must reproduce src/chsh.py.

Runs node on site/parity_dump.js with a grid of inputs and compares every value to the
Python reference to 1e-12 relative (frontier regions must match exactly). Skipped when
node is not installed.
"""
import itertools
import json
import math
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from src import chsh  # noqa: E402

NODE = shutil.which("node")
pytestmark = pytest.mark.skipif(NODE is None, reason="node not on PATH")

DISTANCES = [0.5, 1.0, 5.7, 8.17, 17.6, 32.0, 40.0, 56.0, 100.0, 1000.0, 5570.0, 10000.0]
DETECTORS = [1.0, 0.9, 0.8]
P_Q = [0.75, 0.80, 0.82, chsh.IDEAL_QUANTUM_WIN]
ETAS = [0.0, 0.1, 0.3981071705534972, 0.5, 2 / 3, 0.8284271247461902, 0.877, 0.95, 1.0]
HERALD = [0.0, 0.05, 0.158, 0.5, 1.0]
P_BIAS = [round(0.1 * k, 1) for k in range(1, 10)] + [1 - 1 / math.sqrt(2), 1 / math.sqrt(2)]
WINDOWS = [1e-6, 7.5e-6, 1e-5, 1.9e-5, 5e-5, 1e-4, 1e-3, 1e-2, 1e-1]
REL = 1e-12


def run_js(calls):
    proc = subprocess.run([NODE, str(ROOT / "site" / "parity_dump.js")],
                          input=json.dumps([[f, list(a)] for f, a, _ in calls]),
                          capture_output=True, text=True, check=True, timeout=60)
    return json.loads(proc.stdout)


def build_cases():
    """(js function name, js args, python value) triples. None = use the JS default."""
    cases = []
    for d, det in itertools.product(DISTANCES, DETECTORS):
        cases.append(("fibre_eta", (d, None, det), chsh.fibre_eta(d, detector_eff=det)))
    for eta, p in itertools.product(ETAS, P_Q):
        cases.append(("all_rounds_win", (eta, p), chsh.all_rounds_win(eta, p)))
    for p in P_Q:
        cases.append(("eta_threshold", (p,), chsh.eta_threshold(p)))
    for need, det in itertools.product(
            [chsh.EBERHARD_FLOOR] + [chsh.eta_threshold(p) for p in P_Q] + [0.5], DETECTORS):
        cases.append(("max_separation_km", (need, None, det),
                      chsh.max_separation_km(need, detector_eff=det)))
    for h, p in itertools.product(HERALD, P_Q):
        cases.append(("heralded_win", (h, p), chsh.heralded_win(h, p)))
    for w in [0.6412853266935348, 0.75, 0.82, chsh.IDEAL_QUANTUM_WIN, 0.5]:
        cases.append(("edge_per_round", (w,), chsh.edge_per_round(w)))
    for p in P_BIAS:
        cases.append(("biased_classical", (p,), chsh.biased_classical(p)))
        cases.append(("biased_quantum", (p,), chsh.biased_quantum(p)))
    for d, w, det, p in itertools.product(DISTANCES, WINDOWS, DETECTORS, [0.82, chsh.IDEAL_QUANTUM_WIN]):
        cases.append(("frontier_region", (d, w, p, det),
                      int(chsh.frontier_region(d, w, p_demo=p, detector_eff=det))))
    return cases


def test_js_matches_python():
    cases = build_cases()
    js = run_js(cases)
    assert len(js) == len(cases)
    bad = []
    for (fn, args, py), got in zip(cases, js):
        if fn == "frontier_region":
            if got != py:
                bad.append((fn, args, py, got))
        elif not (got == py or math.isclose(got, py, rel_tol=REL, abs_tol=0.0)):
            bad.append((fn, args, py, got))
    assert not bad, f"{len(bad)} mismatches, first: {bad[:5]}"
    # the grid must exercise all four frontier regions
    regions = {py for fn, _, py in cases if fn == "frontier_region"}
    assert regions == {0, 1, 2, 3}


def test_js_constants():
    script = ("const C=require(process.argv[1]);process.stdout.write(JSON.stringify("
              "[C.SPEED_OF_LIGHT_KM_S,C.FIBRE_LOSS_DB_PER_KM,C.EBERHARD_FLOOR,C.IDEAL_QUANTUM_WIN,C.CLASSICAL_MAX]))")
    proc = subprocess.run([NODE, "-e", script, str(ROOT / "site" / "model.js")],
                          capture_output=True, text=True, check=True, timeout=60)
    c, loss, floor, ideal, cmax = json.loads(proc.stdout)
    assert c == chsh.SPEED_OF_LIGHT_KM_S
    assert loss == chsh.FIBRE_LOSS_DB_PER_KM
    assert floor == chsh.EBERHARD_FLOOR
    assert math.isclose(ideal, chsh.IDEAL_QUANTUM_WIN, rel_tol=REL)
    assert cmax == chsh.CLASSICAL_MAX


def test_js_anchors():
    eta40, win40, dmax82 = run_js([
        ("fibre_eta", (40.0,), None),
        ("all_rounds_win", (0.3981071705534972, chsh.IDEAL_QUANTUM_WIN), None),
        ("max_separation_km", (chsh.eta_threshold(0.82),), None),
    ])
    assert eta40 == pytest.approx(0.398, abs=5e-4)
    assert win40 == pytest.approx(0.646, abs=1e-3)
    assert dmax82 == pytest.approx(5.7, abs=0.05)
