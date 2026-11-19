/* app.js - exhibit page: wires the sliders to model.js and draws the frontier map. No dependencies. */
(function () {
  "use strict";
  var M = window.CHSH;
  var F = window.Frontier;
  var C = M.SPEED_OF_LIGHT_KM_S;

  var D_MIN = F.D_MIN, D_MAX = F.D_MAX;   // km
  var W_MIN = F.W_MIN, W_MAX = F.W_MAX;   // s
  var PR_MIN = 1, PR_MAX = 1e6;           // pairs/s (source rate, heralded mode)
  var REGION_NAMES = ["Grey", "Red", "Yellow", "Green"];
  var REGION_SW = ["sw-grey", "sw-red", "sw-yellow", "sw-green"];
  var REGION_TEXT = [
    "One classical bit arrives on the modelled route inside the window, so the one-bit rule wins every round. Entanglement adds nothing.",
    "No bit arrives on the modelled route, but so many photons are lost that the modelled unheralded strategies cannot beat 75% over all rounds.",
    "No bit arrives on the modelled route; only a near-perfect tuned source near the 2/3 floor could beat 75%. Your source quality cannot.",
    "No bit arrives on the modelled route and enough photons survive: the modelled unheralded strategy beats 75% at your source quality, under idealized assumptions."
  ];
  var CAUSAL_NAMES = ["Physically excluded", "Route-dependent", "Arrives on modelled route"];
  var RACE_MID_S = 7.5e-6;   // midpoint of the 5-10 us race band
  var HERALD_WARN_KM = 100;  // beyond this, stored entanglement is far from demonstrated

  // Case-file inputs; replaced by results.json values once it loads (same numbers).
  var P_CLAIM = 0.82, PAIR_RATE = 1000, DEMAND = 0.6090923888974801;
  var HIBERNIA_ONE_WAY_S = 58.95e-3 / 2;   // half the 2015 Hibernia round-trip benchmark
  var PRESETS = {
    startup: { d: 40, det: 1.0, pq: P_CLAIM, w: 10e-6, mode: "plain", route: null },
    nasdaq: { d: 56, det: 1.0, pq: P_CLAIM, w: 10e-6, mode: "plain", route: null },
    london: { d: 5570, det: 1.0, pq: P_CLAIM, w: 30e-3, mode: "plain", route: HIBERNIA_ONE_WAY_S },
    inside: { d: M.max_separation_km(M.eta_threshold(P_CLAIM)) / 2, det: 1.0, pq: P_CLAIM, w: RACE_MID_S, mode: "plain", route: null }
  };
  var LANDMARKS = [
    { name: "Startup 40 km", km: 40, dash: true },
    { name: "NYSE–Nasdaq", km: 56 },
    { name: "NY–London", km: 5570 }
  ];
  var raceLabel = "";
  var routeLatency = null;   // quoted one-way route latency (s); null = straight-line fibre
  var routeLabel = "";

  function $(id) { return document.getElementById(id); }
  var el = {
    dist: $("dist"), det: $("det"), pq: $("pq"), hf: $("hf"), win: $("win"), pb: $("pb"), pr: $("pr"), hypo: $("hypo"),
    distOut: $("dist-out"), detOut: $("det-out"), pqOut: $("pq-out"), hfOut: $("hf-out"), prOut: $("pr-out"),
    winOut: $("win-out"), pbOut: $("pb-out"), heraldCtl: $("herald-ctl"),
    verdict: $("verdict"), eta: $("r-eta"), etaSub: $("r-eta-sub"), winLabel: $("r-win-label"),
    winR: $("r-win"), winBar: $("r-win-bar"), winMark: $("r-win-mark"), edge: $("r-edge"),
    dmax: $("r-dmax"), dmaxSub: $("r-dmax-sub"), region: $("r-region"), regionSub: $("r-region-sub"),
    causal: $("r-causal"), causalSub: $("r-causal-sub"),
    map: $("map"), mapSummary: $("map-summary"),
    hSupply: $("h-supply"), hCap: $("h-cap"), hWarn: $("herald-warn")
  };

  // log sliders: integer 0..100000 mapped onto [lo, hi]
  function fromLog(v, lo, hi) { return lo * Math.pow(hi / lo, v / 100000); }
  function toLog(x, lo, hi) { return Math.round(100000 * Math.log(x / lo) / Math.log(hi / lo)); }

  function pct(x, dp) { return (100 * x).toFixed(dp === undefined ? 1 : dp) + "%"; }
  function km(x) {
    if (x >= 100) return Math.round(x).toLocaleString("en-US") + " km";
    if (x >= 10) return x.toFixed(1) + " km";
    return x.toFixed(2) + " km";
  }
  function dur(s) {
    if (s >= 1e-3) { var ms = s * 1e3; return (ms >= 10 ? ms.toFixed(1) : ms.toFixed(2)) + " ms"; }
    var us = s * 1e6; return (us >= 100 ? us.toFixed(0) : us >= 10 ? us.toFixed(1) : us.toFixed(2)) + " µs";
  }
  function money(x) {
    var s = Math.abs(x).toFixed(2);
    return (x < 0 ? "−$" : "+$") + s;
  }
  function sci(x) {
    if (x === 0) return "0";
    if (x >= 0.01) return x < 10 ? x.toFixed(3).replace(/\.?0+$/, "") : Math.round(x).toLocaleString("en-US");
    var e = Math.floor(Math.log10(x)), m = x / Math.pow(10, e);
    return m.toFixed(1) + "e" + e;
  }
  function rate(x) { return x >= 10 ? Math.round(x).toLocaleString("en-US") : sci(x); }

  function setFill(inp) {
    var lo = parseFloat(inp.min), hi = parseFloat(inp.max), v = parseFloat(inp.value);
    inp.style.setProperty("--fill", (100 * (v - lo) / (hi - lo)) + "%");
  }

  function state() {
    var pqRaw = parseFloat(el.pq.value);
    return {
      d: fromLog(+el.dist.value, D_MIN, D_MAX),
      det: parseFloat(el.det.value),
      pq: Math.min(pqRaw, M.IDEAL_QUANTUM_WIN),
      pqIdeal: pqRaw >= M.IDEAL_QUANTUM_WIN - 5e-4,
      herald: document.querySelector("input[name=mode]:checked").value === "herald",
      hChosen: parseFloat(el.hf.value),
      pairRate: fromLog(+el.pr.value, PR_MIN, PR_MAX),
      hypothetical: el.hypo.checked,
      w: fromLog(+el.win.value, W_MIN, W_MAX)
    };
  }

  function scalePos(x) { var lo = 0.5, hi = 0.9; return (100 * Math.max(0, Math.min(1, (x - lo) / (hi - lo)))) + "%"; }

  function update() {
    var s = state();
    var eta = M.fibre_eta(s.d, undefined, s.det);
    var etaStar = M.eta_threshold(s.pq);
    // heralded supply: h is capped at what the source rate and fibre loss can deliver
    var cap = M.heralded_supply_fraction(s.d, DEMAND, s.pairRate, s.det);
    var supplied = s.pairRate * Math.pow(eta, 2);
    if (!s.hypothetical && s.hChosen > cap) { el.hf.value = cap; s.hChosen = parseFloat(el.hf.value); }
    var h = s.hChosen;
    var winRate = s.herald ? M.heralded_win(h, s.pq) : M.all_rounds_win(eta, s.pq);
    var edge = M.edge_per_round(winRate);
    var dmax = M.max_separation_km(etaStar, undefined, s.det);
    var region = M.frontier_region(s.d, s.w, s.pq, s.det, routeLatency);
    var causal = M.causal_status(s.d, s.w, routeLatency);
    var lightT = s.d / C;
    var routeT = M.route_latency_s(s.d, routeLatency);

    [el.dist, el.det, el.pq, el.hf, el.win, el.pr].forEach(setFill);
    el.distOut.textContent = km(s.d);
    el.detOut.textContent = pct(s.det, 1);
    el.pqOut.textContent = s.pqIdeal ? pct(M.IDEAL_QUANTUM_WIN, 2) + " (ideal)" : pct(s.pq, 1);
    el.hfOut.textContent = pct(h, 1);
    el.prOut.textContent = rate(s.pairRate) + " pairs/s";
    el.winOut.textContent = dur(s.w);
    el.heraldCtl.classList.toggle("off", !s.herald);
    [el.hf, el.pr, el.hypo].forEach(function (x) { x.disabled = !s.herald; });
    $("hf-eta2").disabled = !s.herald;
    el.hSupply.textContent = rate(supplied) + " /s";
    el.hCap.textContent = cap >= 1 ? "100% (no cap)" : cap < 1e-3 ? sci(cap) : pct(cap, 1);

    var warn = [];
    if (s.herald && s.d > HERALD_WARN_KM) {
      warn.push("Over " + km(s.d) + " stored entanglement of this kind has not been demonstrated; this is a hypothetical rescue.");
    }
    if (s.herald && cap < 1e-6) {
      warn.push("Direct fibre over this distance supplies essentially no heralded pairs (cap " + sci(cap) +
        "). Repeaters or satellites would be needed, and the startup claims neither.");
    }
    if (s.herald && s.hypothetical && h > cap + 1e-12) {
      warn.push("Hypothetical supply (not validated): h = " + pct(h, 1) + " is above the " +
        (cap < 1e-3 ? sci(cap) : pct(cap, 1)) + " that " + rate(s.pairRate) + " pairs/s over this fibre can supply.");
    }
    el.hWarn.hidden = warn.length === 0;
    el.hWarn.innerHTML = warn.map(function (t) { return "<p>" + t + "</p>"; }).join("");

    el.eta.textContent = pct(eta, 1);
    el.etaSub.textContent = "Both photons arrive in " + pct(eta * eta, 1) + " of rounds. Needed to beat 75%: " +
      (etaStar >= 1 ? "impossible at this quality" : pct(etaStar, 1) + " per desk") + ".";

    el.winLabel.textContent = s.herald ? "Win rate, heralded (all rounds)" : "Win rate over all rounds";
    el.winR.textContent = pct(winRate, 2);
    el.winBar.style.left = scalePos(winRate);

    el.edge.textContent = money(edge);
    el.edge.className = edge > 0 ? "" : "neg";

    if (s.herald) {
      el.dmax.textContent = "Supply-limited";
      el.dmaxSub.textContent = "Heralding has no fixed distance cutoff: fibre loss lowers the supply of stored pairs (cap on h: " +
        (cap >= 1 ? "none here" : cap < 1e-3 ? sci(cap) : pct(cap, 1)) + "). Non-heralded limit at these settings: " + km(dmax) + ".";
    } else {
      el.dmax.textContent = dmax > 0 ? km(dmax) : "0 km";
      el.dmaxSub.textContent = dmax > 0
        ? "For the modelled unheralded strategy, under idealized assumptions. Light crosses that in " + dur(dmax / C) + "."
        : "The detectors alone already lose too many photons at this quality.";
    }

    el.causal.textContent = CAUSAL_NAMES[causal];
    el.causalSub.textContent = (causal === M.CAUSAL_EXCLUDED
      ? "The window is shorter than the " + dur(lightT) + " light needs in vacuum: no signal of any kind can arrive."
      : causal === M.CAUSAL_ROUTE_DEPENDENT
        ? "Physics allows a bit (light needs " + dur(lightT) + "), but the modelled route needs " + dur(routeT) + ". A faster route might deliver it."
        : "The bit arrives on the modelled route (" + dur(routeT) + ") inside the window.") +
      " Modelled route: " + (routeLatency === null ? "straight-line fibre at c/" + M.FIBRE_GROUP_INDEX + "." : routeLabel);

    el.region.innerHTML = '<span class="sw ' + REGION_SW[region] + '" aria-hidden="true"></span>' + REGION_NAMES[region];
    el.regionSub.textContent = REGION_TEXT[region];

    var v, tone;
    if (region === M.REGION_GREY) {
      v = "The " + dur(s.w) + " window is longer than the " + dur(routeT) + " the modelled route needs over " + km(s.d) +
        ". One classical message arrives in time and wins 100% of rounds, so the photons are irrelevant.";
      tone = "bad";
    } else {
      var pre = causal === M.CAUSAL_ROUTE_DEPENDENT
        ? "Physics would allow a bit, but the modelled route is too slow. "
        : "No signal can arrive in time. ";
      if (winRate > M.CLASSICAL_MAX) {
        v = pre + "Quantum wins " + pct(winRate, 1) + " of rounds, beating 75% by " + money(edge) + " per round" +
          (s.herald ? ", but only with stored entanglement the startup has not claimed or demonstrated at this distance." +
            (s.hypothetical && h > cap + 1e-12 ? " The pair supply behind this h is hypothetical (not validated)." : "") : ", under idealized assumptions.");
        tone = "good";
      } else if (s.herald) {
        v = pre + "With only " + pct(h, 1) + " of rounds heralded, quantum wins " + pct(winRate, 1) + ": no better than classical's 75%.";
        tone = "bad";
      } else {
        v = pre + "With only " + pct(eta * eta, 1) + " of rounds getting both photons, the quantum strategy wins " +
          pct(winRate, 1) + ". Classical's 75% is better.";
        tone = "bad";
      }
    }
    el.verdict.textContent = v;
    el.verdict.setAttribute("data-tone", tone);

    el.mapSummary.textContent = "At these settings green reaches " + (dmax > 0 ? km(dmax) : "nowhere") +
      " for the modelled unheralded strategy. Your point (" + km(s.d) + ", " + dur(s.w) + ") is " + REGION_NAMES[region].toLowerCase() +
      "; for the bit it is " + CAUSAL_NAMES[causal].toLowerCase() + ". Hatching marks windows where physics allows a bit but a straight-line fibre route is too slow.";

    F.draw(el.map, {
      pq: s.pq, det: s.det, marker: { d: s.d, w: s.w }, landmarks: LANDMARKS, raceLabel: raceLabel, key: "ex",
      points: [{ d: PRESETS.london.d, w: HIBERNIA_ONE_WAY_S, label: ["NY–LON " + dur(HIBERNIA_ONE_WAY_S), "FROM 2015 HIBERNIA ROUND TRIP"] }]
    });
  }

  function updateBias() {
    var p = parseFloat(el.pb.value);
    var cl = M.biased_classical(p), q = M.biased_quantum(p);
    setFill(el.pb);
    el.pbOut.textContent = pct(p, 0);
    $("b-cl").textContent = pct(cl, 1);
    $("b-q").textContent = pct(q, 1);
    $("b-gap").textContent = (100 * (q - cl)).toFixed(1) + " pts";
    $("b-note").textContent = q - cl < 1e-12
      ? "Quantum offers nothing at this bias: the signal is too lopsided."
      : "Quantum keeps an edge only while each signal fires between " + pct(1 - 1 / Math.SQRT2, 0) + " and " + pct(1 / Math.SQRT2, 0) + " of the time.";
  }

  // ---- wiring ------------------------------------------------------------------------
  function setMode(m) {
    document.querySelectorAll("input[name=mode]").forEach(function (r) { r.checked = r.value === m; });
  }
  function applyPreset(name) {
    var p = PRESETS[name];
    el.dist.value = toLog(p.d, D_MIN, D_MAX);
    el.det.value = p.det;
    el.pq.value = p.pq;
    el.win.value = toLog(p.w, W_MIN, W_MAX);
    routeLatency = p.route;
    setMode(p.mode);
    document.querySelectorAll("[data-preset]").forEach(function (b) {
      b.setAttribute("aria-pressed", String(b.getAttribute("data-preset") === name));
    });
    update();
  }
  function clearPreset() {
    document.querySelectorAll("[data-preset]").forEach(function (b) { b.setAttribute("aria-pressed", "false"); });
  }

  [el.det, el.pq, el.hf, el.win, el.pr].forEach(function (inp) {
    inp.addEventListener("input", function () { clearPreset(); update(); });
  });
  // moving the desks drops any quoted route latency: back to the straight-line fibre route
  el.dist.addEventListener("input", function () { clearPreset(); routeLatency = null; update(); });
  el.hypo.addEventListener("change", update);
  document.querySelectorAll("input[name=mode]").forEach(function (r) {
    r.addEventListener("change", function () { clearPreset(); update(); });
  });
  document.querySelectorAll("[data-preset]").forEach(function (b) {
    b.addEventListener("click", function () { applyPreset(b.getAttribute("data-preset")); });
  });
  $("hf-eta2").addEventListener("click", function () {
    var s = state();
    var eta = M.fibre_eta(s.d, undefined, s.det);
    el.hf.value = (eta * eta).toFixed(3);
    update();
  });
  el.pb.addEventListener("input", updateBias);

  var rt;
  window.addEventListener("resize", function () { clearTimeout(rt); rt = setTimeout(update, 60); });

  // static ticks on the win-rate scale
  $("r-win-mark-75").style.left = scalePos(M.CLASSICAL_MAX);
  el.winMark.style.left = scalePos(M.CLASSICAL_MAX);
  $("r-win-mark-ideal").style.left = scalePos(M.IDEAL_QUANTUM_WIN);
  $("r-win-lbl-ideal").style.left = scalePos(M.IDEAL_QUANTUM_WIN);
  $("c-kms").textContent = C.toLocaleString("en-US", { maximumFractionDigits: 3 });
  $("fibre-index").textContent = String(M.FIBRE_GROUP_INDEX);

  routeLabel = "half the 2015 Hibernia round-trip benchmark (" + dur(HIBERNIA_ONE_WAY_S) + "), derived, not a measured one-way service.";
  el.hf.value = 0.158;
  el.pr.value = toLog(PAIR_RATE, PR_MIN, PR_MAX);
  applyPreset("startup");
  updateBias();

  // once results.json is in, take the case-file inputs and labels from it
  window.Results.ready.then(function (d) {
    if (!d) return;
    var inp = d.values.inputs;
    var nas = d.values.e4_landmarks.filter(function (l) { return l.name === "NYSE–Nasdaq"; })[0];
    PRESETS.startup.d = inp.link_km;
    PRESETS.london.d = inp.ny_london_km;
    if (nas) PRESETS.nasdaq.d = nas.km;
    ["startup", "nasdaq", "london", "inside"].forEach(function (k) { PRESETS[k].pq = inp.p_quantum_claim; });
    PRESETS.inside.d = d.values.e2.p82.d_max_km / 2;
    if (typeof d.values.hibernia_one_way_ms === "number") {
      HIBERNIA_ONE_WAY_S = d.values.hibernia_one_way_ms / 1000;
      PRESETS.london.route = HIBERNIA_ONE_WAY_S;
      routeLabel = "half the 2015 Hibernia round-trip benchmark (" + d.display.hibernia_one_way + "), derived, not a measured one-way service.";
    }
    if (d.values.e2b && typeof d.values.e2b.demand_rounds_per_s === "number") DEMAND = d.values.e2b.demand_rounds_per_s;
    if (typeof inp.pair_rate === "number") { PAIR_RATE = inp.pair_rate; el.pr.value = toLog(PAIR_RATE, PR_MIN, PR_MAX); }
    LANDMARKS[0] = { name: "Startup " + d.display.link_km, km: inp.link_km, dash: true };
    if (nas) LANDMARKS[1].km = nas.km;
    LANDMARKS[2].km = inp.ny_london_km;
    raceLabel = d.display.race_window;
    var pressed = document.querySelector('[data-preset][aria-pressed="true"]');
    if (pressed) applyPreset(pressed.getAttribute("data-preset")); else update();
  });
})();
