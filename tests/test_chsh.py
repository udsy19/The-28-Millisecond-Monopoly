"""Expected-value checks. These numbers come from the task brief and were re-derived by
hand in the notebook; do not loosen a tolerance to make a test pass."""
import math
import sys
from pathlib import Path

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from src import chsh  # noqa: E402

D_LINK = 40.0


def test_classical_max():
    assert chsh.classical_max() == pytest.approx(0.75, abs=1e-12)
    assert len(chsh.deterministic_strategies()) == 16


def test_one_bit_strategy_wins_everything():
    assert chsh.one_bit_strategy_win_rate() == 1.0


def test_z_scores():
    assert chsh.z_score(0.82) == pytest.approx(5.1, abs=0.05)
    assert chsh.z_score(0.74) == pytest.approx(-0.7, abs=0.05)


def test_ideal_quantum_exact_and_monte_carlo():
    assert chsh.exact_quantum_win() == pytest.approx(0.8536, abs=1e-4)
    rng = np.random.default_rng(1)
    assert chsh.simulate_quantum(1_000_000, rng) == pytest.approx(0.8536, abs=0.002)


def test_noisy_source_hits_82():
    v = chsh.visibility_for_win(0.82)
    assert chsh.exact_quantum_win(v) == pytest.approx(0.82, abs=1e-12)


def test_eta_on_40km_link():
    assert chsh.fibre_eta(D_LINK) == pytest.approx(0.398, abs=5e-4)


def test_all_rounds_win_40km_ideal():
    eta = chsh.fibre_eta(D_LINK)
    assert chsh.all_rounds_win(eta, chsh.IDEAL_QUANTUM_WIN) == pytest.approx(0.646, abs=1.5e-3)
    assert eta**2 == pytest.approx(0.158, abs=1e-3)


def test_thresholds_and_separations():
    e_ideal = chsh.eta_threshold(chsh.IDEAL_QUANTUM_WIN)
    e_82 = chsh.eta_threshold(0.82)
    assert e_ideal == pytest.approx(0.828, abs=1e-3)
    assert chsh.max_separation_km(e_ideal) == pytest.approx(8.2, abs=0.05)
    assert e_82 == pytest.approx(0.877, abs=1e-3)
    assert chsh.max_separation_km(e_82) == pytest.approx(5.7, abs=0.05)
    assert chsh.max_separation_km(chsh.EBERHARD_FLOOR) == pytest.approx(17.6, abs=0.05)


def test_threshold_is_break_even():
    for p in (0.82, chsh.IDEAL_QUANTUM_WIN):
        assert chsh.all_rounds_win(chsh.eta_threshold(p), p) == pytest.approx(0.75, abs=1e-12)


def test_lossy_monte_carlo_matches_formula():
    rng = np.random.default_rng(2)
    eta = chsh.fibre_eta(D_LINK)
    all_w, coinc_w, both = chsh.simulate_lossy(1_000_000, eta, rng)
    assert all_w == pytest.approx(chsh.all_rounds_win(eta, chsh.IDEAL_QUANTUM_WIN), abs=0.002)
    assert coinc_w == pytest.approx(chsh.IDEAL_QUANTUM_WIN, abs=0.004)
    assert both == pytest.approx(eta**2, abs=0.002)


def test_cheater():
    assert chsh.cheater_exact() == pytest.approx((0.75, 0.82, 0.78125), abs=1e-12)
    rng = np.random.default_rng(3)
    all_w, det_w, kept = chsh.simulate_cheater(1_000_000, rng)
    assert all_w == pytest.approx(0.75, abs=0.002)
    assert det_w == pytest.approx(0.82, abs=0.002)
    assert kept == pytest.approx(0.78125, abs=0.002)


def test_biased_game():
    gap = chsh.biased_quantum(0.5) - chsh.biased_classical(0.5)
    assert gap == pytest.approx(0.1036, abs=1e-4)
    lo, hi = 1 - 1 / math.sqrt(2), 1 / math.sqrt(2)
    assert lo == pytest.approx(0.293, abs=1e-3) and hi == pytest.approx(0.707, abs=1e-3)
    for p in (0.1, 0.28, 0.75, 0.9):     # outside the window: no advantage
        assert chsh.biased_quantum(p) == chsh.biased_classical(p)
    for p in (0.31, 0.4, 0.6, 0.69):     # inside: strict advantage
        assert chsh.biased_quantum(p) > chsh.biased_classical(p)


def test_biased_closed_form_matches_brute_force_and_optimiser():
    rng = np.random.default_rng(4)
    for p in (0.1, 0.3, 0.4, 0.5, 0.65, 0.8):
        assert chsh.classical_max(p) == pytest.approx(chsh.biased_classical(p), abs=1e-12)
        assert chsh.biased_quantum_numeric(p, rng) == pytest.approx(chsh.biased_quantum(p), abs=1e-6)


def test_economics():
    edge = chsh.edge_per_round(0.82)
    assert edge == pytest.approx(13.921, abs=1e-9)
    rounds = chsh.rounds_for_target(50e6, edge)
    assert rounds == pytest.approx(3.59e6, rel=2e-3)
    assert 50e6 / 5e9 == pytest.approx(0.010)


def test_all_rounds_edge_is_negative_on_40km():
    eta = chsh.fibre_eta(D_LINK)
    assert chsh.edge_per_round(chsh.all_rounds_win(eta, 0.82)) < 0


def test_frontier_regions():
    c = chsh.SPEED_OF_LIGHT_KM_S
    assert chsh.frontier_region(5570, 0.1) == chsh.REGION_GREY       # 100 ms window
    assert chsh.frontier_region(40, 1e-6) == chsh.REGION_RED          # test link, 1 us
    assert chsh.frontier_region(12, 1e-6) == chsh.REGION_YELLOW
    assert chsh.frontier_region(3, 1e-6) == chsh.REGION_GREEN
    assert chsh.frontier_region(3, 2 * 3 / c) == chsh.REGION_GREY


def test_heralded_never_below_classical():
    for h in (0.0, 0.158, 0.5, 1.0):
        assert chsh.heralded_win(h, 0.82) >= 0.75
    assert chsh.heralded_win(1.0, 0.82) == pytest.approx(0.82)
    assert chsh.heralded_win(0.0, 0.82) == pytest.approx(0.75)


def test_causal_status_three_states():
    c = chsh.SPEED_OF_LIGHT_KM_S
    hibernia_one_way = 58.95e-3 / 2
    # NY-London at a 20 ms deadline: physics allows a bit (> 18.6 ms) but the
    # benchmarked cable route does not deliver it (29.5 ms): route-dependent, not grey.
    assert chsh.causal_status(5570, 0.020, hibernia_one_way) == chsh.CAUSAL_ROUTE_DEPENDENT
    assert chsh.frontier_region(5570, 0.020, route_latency=hibernia_one_way) != chsh.REGION_GREY
    assert chsh.causal_status(5570, 0.015) == chsh.CAUSAL_EXCLUDED        # faster than light
    assert chsh.causal_status(5570, 0.035, hibernia_one_way) == chsh.CAUSAL_ARRIVES
    # default modelled route: straight-line fibre at c / 1.47
    d = 100.0
    assert chsh.causal_status(d, 1.2 * d / c) == chsh.CAUSAL_ROUTE_DEPENDENT
    assert chsh.causal_status(d, 1.5 * d / c) == chsh.CAUSAL_ARRIVES
    # a quoted route latency can never be faster than light
    assert chsh.route_latency_s(d, 0.0) == pytest.approx(d / c)


def test_heralded_supply_is_capped_by_the_link():
    # 1,000 pairs/s over 40 km easily covers well under one round per second ...
    assert chsh.heralded_supply_fraction(40, 0.61) == 1.0
    # ... but direct fibre across the Atlantic supplies essentially nothing.
    assert chsh.heralded_supply_fraction(5570, 0.61) < 1e-100
    # supply scales with the squared per-desk delivery
    eta = chsh.fibre_eta(40)
    assert chsh.heralded_supply_fraction(40, 1000.0) == pytest.approx(eta**2)


def test_causal_boundaries_shared_spec():
    """Shared spec with site/model.js: excluded if w < d/c; arrives if w >= 1.47 d/c."""
    c = chsh.SPEED_OF_LIGHT_KM_S
    assert chsh.FIBRE_GROUP_INDEX == 1.47
    for d in (1.0, 32.0, 40.0, 56.0, 5570.0):
        assert chsh.causal_status(d, d / c) == chsh.CAUSAL_ROUTE_DEPENDENT
        assert chsh.causal_status(d, np.nextafter(d / c, 0)) == chsh.CAUSAL_EXCLUDED
        assert chsh.causal_status(d, 1.47 * d / c) == chsh.CAUSAL_ARRIVES
        assert chsh.causal_status(d, np.nextafter(1.47 * d / c, 0)) == chsh.CAUSAL_ROUTE_DEPENDENT
    # with a route-latency override the same inclusive/exclusive rule applies
    hib = 58.95e-3 / 2
    assert chsh.causal_status(5570, hib, hib) == chsh.CAUSAL_ARRIVES
    assert chsh.causal_status(5570, np.nextafter(hib, 0), hib) == chsh.CAUSAL_ROUTE_DEPENDENT
    assert chsh.causal_status(5570, 5570 / c, hib) == chsh.CAUSAL_ROUTE_DEPENDENT
    assert chsh.CAUSAL_STATE_NAMES == {0: "physically_excluded", 1: "route_dependent",
                                       2: "classical_arrives"}


def test_loss_region_matches_frontier_when_no_bit():
    for d in (3.0, 12.0, 40.0, 5570.0):
        assert chsh.loss_region(d) == chsh.frontier_region(d, 1e-9)
    assert chsh.REGION_NAMES[int(chsh.loss_region(40.0))] == "red"


def test_endpoint_source_thresholds():
    ideal = chsh.IDEAL_QUANTUM_WIN
    assert chsh.endpoint_eta_threshold(ideal) == pytest.approx(1 / math.sqrt(2), abs=1e-12)
    assert chsh.endpoint_eta_threshold(0.82) == pytest.approx(0.78125, abs=1e-12)
    for p in (0.82, ideal):
        assert chsh.endpoint_all_rounds_win(chsh.endpoint_eta_threshold(p), p) == pytest.approx(0.75, abs=1e-12)
    assert chsh.endpoint_max_separation_km(chsh.endpoint_eta_threshold(ideal)) == pytest.approx(7.5, abs=0.05)
    assert chsh.endpoint_max_separation_km(chsh.endpoint_eta_threshold(0.82)) == pytest.approx(5.4, abs=0.05)
    assert chsh.endpoint_max_separation_km(chsh.ENDPOINT_PARTIAL_ETA_FLOOR) == pytest.approx(15.1, abs=0.05)
    assert chsh.endpoint_fibre_eta(15.0515) == pytest.approx(0.5, abs=1e-5)
    # the midpoint source tolerates more distance than the endpoint source in every case
    assert chsh.max_separation_km(chsh.eta_threshold(ideal)) > chsh.endpoint_max_separation_km(1 / math.sqrt(2))
    assert chsh.max_separation_km(chsh.eta_threshold(0.82)) > chsh.endpoint_max_separation_km(0.78125)
    assert chsh.max_separation_km(chsh.EBERHARD_FLOOR) > chsh.endpoint_max_separation_km(0.5)
    # eta_near = 1 reduces to the closed form; eta_near = eta_far = eta matches the midpoint model
    assert chsh.endpoint_all_rounds_win(0.6, 0.82) == pytest.approx(0.6 * 0.82 + 0.4 * 0.5)
    assert chsh.endpoint_all_rounds_win(0.4, 0.82, eta_near=0.4) == pytest.approx(chsh.all_rounds_win(0.4, 0.82))


def test_endpoint_monte_carlo_matches_formula():
    rng = np.random.default_rng(5)
    for d in (7.5, 40.0):
        eta = chsh.endpoint_fibre_eta(d)
        mc = chsh.simulate_endpoint_lossy(1_000_000, eta, rng)
        assert mc == pytest.approx(chsh.endpoint_all_rounds_win(eta, chsh.IDEAL_QUANTUM_WIN), abs=0.002)


def test_endpoint_partial_state_threshold_numeric():
    rng = np.random.default_rng(6)
    # maximally entangled: optimising angles and fallbacks cannot beat 1/sqrt(2)
    thr, _ = chsh.endpoint_partial_eta_threshold(math.pi / 4, rng, starts=6)
    assert thr == pytest.approx(1 / math.sqrt(2), abs=1e-4)
    # weakly entangled states approach the asymmetric 1/2 floor from above
    thr, params = chsh.endpoint_partial_eta_threshold(0.05, rng, starts=6)
    assert 0.5 < thr < 0.502
    q, f = chsh.endpoint_partial_terms(0.05, params)
    assert thr * q + (1 - thr) * f == pytest.approx(0.75, abs=1e-9)
