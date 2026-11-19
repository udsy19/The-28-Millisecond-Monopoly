/* app.js - exhibit page: wires the sliders to model.js and draws the frontier map. No dependencies. */
(function () {
  "use strict";
  var M = window.CHSH;
  var F = window.Frontier;
  var C = M.SPEED_OF_LIGHT_KM_S;

  var D_MIN = F.D_MIN, D_MAX = F.D_MAX;   // km
  var W_MIN = F.W_MIN, W_MAX = F.W_MAX;   // s
  var REGION_NAMES = ["Grey", "Red", "Yellow", "Green"];
  var REGION_SW = ["sw-grey", "sw-red", "sw-yellow", "sw-green"];
  var REGION_TEXT = [
    "A single classical bit crosses between the desks inside the window, so classical wins every round. Entanglement adds nothing.",
    "No time for a message, but so many photons are lost that no quantum strategy beats 75% over all rounds.",
    "No time for a message; only an ideal source with near-perfect delivery (above the 2/3 floor) could beat 75%. Your source quality cannot.",
    "No time for a message and enough photons survive: quantum beats 75% at your source quality."
  ];
  var RACE_MID_S = 7.5e-6;   // midpoint of the 5-10 us race band

  // Case-file inputs; replaced by results.json values once it loads (same numbers).
  var P_CLAIM = 0.82;
  var PRESETS = {
    startup: { d: 40, det: 1.0, pq: P_CLAIM, w: 10e-6, mode: "plain" },
    nasdaq: { d: 56, det: 1.0, pq: P_CLAIM, w: 10e-6, mode: "plain" },
    london: { d: 5570, det: 1.0, pq: P_CLAIM, w: 30e-3, mode: "plain" },
    inside: { d: M.max_separation_km(M.eta_threshold(P_CLAIM)) / 2, det: 1.0, pq: P_CLAIM, w: RACE_MID_S, mode: "plain" }
  };
  var LANDMARKS = [
    { name: "Startup 40 km", km: 40, dash: true },
    { name: "NYSE–Nasdaq", km: 56 },
    { name: "NY–London", km: 5570 }
  ];
  var raceLabel = "";

  function $(id) { return document.getElementById(id); }
  var el = {
    dist: $("dist"), det: $("det"), pq: $("pq"), hf: $("hf"), win: $("win"), pb: $("pb"),
    distOut: $("dist-out"), detOut: $("det-out"), pqOut: $("pq-out"), hfOut: $("hf-out"),
    winOut: $("win-out"), pbOut: $("pb-out"), heraldCtl: $("herald-ctl"),
    verdict: $("verdict"), eta: $("r-eta"), etaSub: $("r-eta-sub"), winLabel: $("r-win-label"),
    winR: $("r-win"), winBar: $("r-win-bar"), winMark: $("r-win-mark"), edge: $("r-edge"),
    dmax: $("r-dmax"), dmaxSub: $("r-dmax-sub"), region: $("r-region"), regionSub: $("r-region-sub"),
    map: $("map"), mapSummary: $("map-summary")
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
      h: parseFloat(el.hf.value),
      w: fromLog(+el.win.value, W_MIN, W_MAX)
    };
  }

  function scalePos(x) { var lo = 0.5, hi = 0.9; return (100 * Math.max(0, Math.min(1, (x - lo) / (hi - lo)))) + "%"; }

  function update() {
    var s = state();
    var eta = M.fibre_eta(s.d, undefined, s.det);
    var etaStar = M.eta_threshold(s.pq);
    var winRate = s.herald ? M.heralded_win(s.h, s.pq) : M.all_rounds_win(eta, s.pq);
    var edge = M.edge_per_round(winRate);
    var dmax = M.max_separation_km(etaStar, undefined, s.det);
    var region = M.frontier_region(s.d, s.w, s.pq, s.det);
    var lightT = s.d / C;

    [el.dist, el.det, el.pq, el.hf, el.win].forEach(setFill);
    el.distOut.textContent = km(s.d);
    el.detOut.textContent = pct(s.det, 1);
    el.pqOut.textContent = s.pqIdeal ? pct(M.IDEAL_QUANTUM_WIN, 2) + " (ideal)" : pct(s.pq, 1);
    el.hfOut.textContent = pct(s.h, 1);
    el.winOut.textContent = dur(s.w);
    el.heraldCtl.classList.toggle("off", !s.herald);
    el.hf.disabled = !s.herald;
    $("hf-eta2").disabled = !s.herald;

    el.eta.textContent = pct(eta, 1);
    el.etaSub.textContent = "Both photons arrive in " + pct(eta * eta, 1) + " of rounds. Needed to beat 75%: " +
      (etaStar >= 1 ? "impossible at this quality" : pct(etaStar, 1) + " per desk") + ".";

    el.winLabel.textContent = s.herald ? "Win rate, heralded (all rounds)" : "Win rate over all rounds";
    el.winR.textContent = pct(winRate, 2);
    el.winBar.style.left = scalePos(winRate);

    el.edge.textContent = money(edge);
    el.edge.className = edge > 0 ? "" : "neg";

    if (s.herald) {
      el.dmax.textContent = s.h > 0 ? "No loss limit" : "None";
      el.dmaxSub.textContent = "With heralding, any stored pair helps, so fibre loss lowers the rate of good rounds instead of the win rate. Non-heralded limit at these settings: " + km(dmax) + ".";
    } else {
      el.dmax.textContent = dmax > 0 ? km(dmax) : "0 km";
      el.dmaxSub.textContent = dmax > 0
        ? "Light crosses that in " + dur(dmax / C) + ", so the window must be shorter than that too."
        : "The detectors alone already lose too many photons at this quality.";
    }

    el.region.innerHTML = '<span class="sw ' + REGION_SW[region] + '" aria-hidden="true"></span>' + REGION_NAMES[region];
    el.regionSub.textContent = REGION_TEXT[region] + " Light needs " + dur(lightT) + " to cross " + km(s.d) + ".";

    var v, tone;
    if (region === M.REGION_GREY) {
      v = "The " + dur(s.w) + " window is longer than the " + dur(lightT) + " light needs to cross " + km(s.d) +
        ". One classical message arrives in time and wins 100% of rounds, so the photons are irrelevant.";
      tone = "bad";
    } else if (winRate > M.CLASSICAL_MAX) {
      v = "No message can arrive in time and quantum wins " + pct(winRate, 1) + " of rounds, beating 75% by " +
        money(edge) + " per round" + (s.herald ? ", but only with quantum memories the startup has not claimed." : ".");
      tone = "good";
    } else {
      v = "No message can arrive in time, but with only " + pct(eta * eta, 1) + " of rounds getting both photons, the quantum strategy wins " +
        pct(winRate, 1) + ". Classical's 75% is better.";
      tone = "bad";
    }
    el.verdict.textContent = v;
    el.verdict.setAttribute("data-tone", tone);

    el.mapSummary.textContent = "At these settings green reaches " + (dmax > 0 ? km(dmax) + " and " + dur(dmax / C) : "nowhere") +
      ". Your point (" + km(s.d) + ", " + dur(s.w) + ") is " + REGION_NAMES[region].toLowerCase() + ".";

    F.draw(el.map, { pq: s.pq, det: s.det, marker: { d: s.d, w: s.w }, landmarks: LANDMARKS, raceLabel: raceLabel, key: "ex" });
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
    setMode(p.mode);
    document.querySelectorAll("[data-preset]").forEach(function (b) {
      b.setAttribute("aria-pressed", String(b.getAttribute("data-preset") === name));
    });
    update();
  }
  function clearPreset() {
    document.querySelectorAll("[data-preset]").forEach(function (b) { b.setAttribute("aria-pressed", "false"); });
  }

  [el.dist, el.det, el.pq, el.hf, el.win].forEach(function (inp) {
    inp.addEventListener("input", function () { clearPreset(); update(); });
  });
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

  el.hf.value = 0.158;
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
    LANDMARKS[0] = { name: "Startup " + d.display.link_km, km: inp.link_km, dash: true };
    if (nas) LANDMARKS[1].km = nas.km;
    LANDMARKS[2].km = inp.ny_london_km;
    raceLabel = d.display.race_window;
    var pressed = document.querySelector('[data-preset][aria-pressed="true"]');
    if (pressed) applyPreset(pressed.getAttribute("data-preset")); else update();
  });
})();
