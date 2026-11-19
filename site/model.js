/*
 * model.js - browser/Node port of the pure functions in src/chsh.py.
 * Kept line-for-line close to the Python so tests/test_parity.py can check
 * agreement to 1e-12. UMD wrapper: window.CHSH in the browser, require() in Node.
 */
(function (root, factory) {
  if (typeof module === "object" && module.exports) {
    module.exports = factory();
  } else {
    root.CHSH = factory();
  }
})(typeof self !== "undefined" ? self : this, function () {
  "use strict";

  var SPEED_OF_LIGHT_KM_S = 299792.458;   // vacuum: the earliest any signal can arrive
  var FIBRE_GROUP_INDEX = 1.47;            // standard single-mode fibre at 1550 nm
  var FIBRE_SPEED_KM_S = SPEED_OF_LIGHT_KM_S / FIBRE_GROUP_INDEX;   // ~204,000 km/s
  var FIBRE_LOSS_DB_PER_KM = 0.2;          // telecom fibre at 1550 nm
  var EBERHARD_FLOOR = 2.0 / 3.0;          // lowest efficiency any CHSH-type test tolerates
  var IDEAL_QUANTUM_WIN = Math.pow(Math.cos(Math.PI / 8), 2);  // Tsirelson, ~0.8536
  var CLASSICAL_MAX = 0.75;

  var REGION_GREY = 0, REGION_RED = 1, REGION_YELLOW = 2, REGION_GREEN = 3;
  // Causal status of one classical bit sent from desk A to desk B after the inputs arrive.
  var CAUSAL_EXCLUDED = 0, CAUSAL_ROUTE_DEPENDENT = 1, CAUSAL_ARRIVES = 2;

  function def(v, d) { return v === undefined ? d : v; }

  /* E2: win rate over ALL rounds when each desk gets its photon with probability eta. */
  function all_rounds_win(eta, p_q) {
    return Math.pow(eta, 2) * p_q + 2 * eta * (1 - eta) * 0.5 + Math.pow(1 - eta, 2) * CLASSICAL_MAX;
  }

  /* Efficiency at which all_rounds_win equals 0.75. */
  function eta_threshold(p_q) {
    return 0.5 / (p_q - 0.25);
  }

  /* Per-desk efficiency with the source at the midpoint (each arm is d/2 km). */
  function fibre_eta(d_km, loss_db_per_km, detector_eff) {
    loss_db_per_km = def(loss_db_per_km, FIBRE_LOSS_DB_PER_KM);
    detector_eff = def(detector_eff, 1.0);
    var arm_loss_db = loss_db_per_km * d_km / 2;
    return detector_eff * Math.pow(10, -arm_loss_db / 10);
  }

  /* Largest separation whose fibre efficiency still reaches eta_needed (0 if detectors alone fail). */
  function max_separation_km(eta_needed, loss_db_per_km, detector_eff) {
    loss_db_per_km = def(loss_db_per_km, FIBRE_LOSS_DB_PER_KM);
    detector_eff = def(detector_eff, 1.0);
    if (eta_needed >= detector_eff) return 0.0;
    return -20.0 / loss_db_per_km * Math.log10(eta_needed / detector_eff);
  }

  /* E2b: largest heralded fraction h the link can actually supply (perfect memories at best). */
  function heralded_supply_fraction(d_km, rounds_per_s, pair_rate, detector_eff, memory_eff) {
    pair_rate = def(pair_rate, 1000.0);
    detector_eff = def(detector_eff, 1.0);
    memory_eff = def(memory_eff, 1.0);
    var per_desk = fibre_eta(d_km, undefined, detector_eff) * memory_eff;
    var supply = pair_rate * Math.pow(per_desk, 2);
    return Math.min(1.0, supply / rounds_per_s);
  }

  /* E2b: heralded delivery (quantum memories). Founder-rescue scenario, not claimed. */
  function heralded_win(h, p_q) {
    return h * p_q + (1 - h) * CLASSICAL_MAX;
  }

  /* E6: extra dollars per round. The +/-$100 payoff is invented by the case file. */
  function edge_per_round(p_quantum, p_classical, payoff, cost_quantum, cost_classical) {
    p_classical = def(p_classical, 0.75);
    payoff = def(payoff, 100.0);
    cost_quantum = def(cost_quantum, 0.08);
    cost_classical = def(cost_classical, 0.001);
    return 2 * payoff * (p_quantum - p_classical) - (cost_quantum - cost_classical);
  }

  /* E5: biased inputs (Ding & Jiang, Theorem 10). */
  function biased_classical(p) {
    return p <= 0.5 ? 1 - Math.pow(p, 2) : -Math.pow(p, 2) + 2 * p;
  }

  function biased_quantum(p) {
    var lo = 1 - 1 / Math.sqrt(2), hi = 1 / Math.sqrt(2);
    if (lo <= p && p <= hi) return (1 - 2 * p * (1 - p)) / Math.sqrt(2) + 0.5;
    return biased_classical(p);
  }

  /* E4: one-way latency of the modelled classical route. Default: straight-line fibre,
     FIBRE_GROUP_INDEX * d / c (written this way so the boundary window = 1.47 d/c is exact).
     A quoted route_latency (seconds) replaces it, but nothing is faster than light (d/c). */
  function route_latency_s(d_km, route_latency) {
    var modelled = (route_latency === undefined || route_latency === null)
      ? FIBRE_GROUP_INDEX * d_km / SPEED_OF_LIGHT_KM_S : route_latency;
    return Math.max(modelled, d_km / SPEED_OF_LIGHT_KM_S);
  }

  /* E4: can one classical bit reach the other desk within the window?
     EXCLUDED: window < d/c.  ROUTE_DEPENDENT: d/c <= window < route latency.
     ARRIVES: window >= route latency (default 1.47 d/c). */
  function causal_status(d_km, window_s, route_latency) {
    if (window_s < d_km / SPEED_OF_LIGHT_KM_S) return CAUSAL_EXCLUDED;
    if (window_s >= route_latency_s(d_km, route_latency)) return CAUSAL_ARRIVES;
    return CAUSAL_ROUTE_DEPENDENT;
  }

  /* E4: classify a (separation, decision window) point. Scalar version.
     Grey = the bit arrives on the modelled route; otherwise the unheralded photon-loss model decides. */
  function frontier_region(d_km, window_s, p_demo, detector_eff, route_latency) {
    p_demo = def(p_demo, 0.82);
    detector_eff = def(detector_eff, 1.0);
    var eta = fibre_eta(d_km, undefined, detector_eff);
    var region = REGION_RED;
    if (eta > EBERHARD_FLOOR) region = REGION_YELLOW;
    if (eta > eta_threshold(p_demo)) region = REGION_GREEN;
    if (causal_status(d_km, window_s, route_latency) === CAUSAL_ARRIVES) region = REGION_GREY;
    return region;
  }

  return {
    SPEED_OF_LIGHT_KM_S: SPEED_OF_LIGHT_KM_S,
    FIBRE_GROUP_INDEX: FIBRE_GROUP_INDEX,
    FIBRE_SPEED_KM_S: FIBRE_SPEED_KM_S,
    FIBRE_LOSS_DB_PER_KM: FIBRE_LOSS_DB_PER_KM,
    EBERHARD_FLOOR: EBERHARD_FLOOR,
    IDEAL_QUANTUM_WIN: IDEAL_QUANTUM_WIN,
    CLASSICAL_MAX: CLASSICAL_MAX,
    REGION_GREY: REGION_GREY, REGION_RED: REGION_RED,
    REGION_YELLOW: REGION_YELLOW, REGION_GREEN: REGION_GREEN,
    CAUSAL_EXCLUDED: CAUSAL_EXCLUDED, CAUSAL_ROUTE_DEPENDENT: CAUSAL_ROUTE_DEPENDENT,
    CAUSAL_ARRIVES: CAUSAL_ARRIVES,
    fibre_eta: fibre_eta,
    all_rounds_win: all_rounds_win,
    eta_threshold: eta_threshold,
    max_separation_km: max_separation_km,
    heralded_supply_fraction: heralded_supply_fraction,
    heralded_win: heralded_win,
    edge_per_round: edge_per_round,
    biased_classical: biased_classical,
    biased_quantum: biased_quantum,
    route_latency_s: route_latency_s,
    causal_status: causal_status,
    frontier_region: frontier_region
  };
});
