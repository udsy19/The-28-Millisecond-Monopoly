/* app.js - wires the sliders to model.js and draws the frontier map. No dependencies. */
(function () {
  "use strict";
  var M = window.CHSH;
  var C = M.SPEED_OF_LIGHT_KM_S;

  var D_MIN = 1, D_MAX = 1e4;          // km
  var W_MIN = 1e-6, W_MAX = 1e-1;      // s
  var REGION_COLORS = ["#d6d5cf", "#efa596", "#f6d27a", "#8ccf8c"];
  var REGION_NAMES = ["Grey", "Red", "Yellow", "Green"];
  var REGION_TEXT = [
    "A single classical bit crosses between the desks inside the window, so classical wins every round. Entanglement adds nothing.",
    "No time for a message, but so many photons are lost that no quantum strategy beats 75% over all rounds.",
    "No time for a message; only an ideal source with near-perfect delivery (above the 2/3 floor) could beat 75%. Your pₑ cannot.",
    "No time for a message and enough photons survive: quantum beats 75% at your pₑ."
  ];
  REGION_TEXT[2] = REGION_TEXT[2].replace("pₑ", "source quality");
  REGION_TEXT[3] = REGION_TEXT[3].replace("pₑ", "source quality");

  var LANDMARKS = [
    { name: "Startup 40 km", km: 40, dash: true },
    { name: "NYSE–Nasdaq", km: 56 },
    { name: "NY–London", km: 5570 }
  ];
  var PRESETS = {
    startup: { d: 40, det: 1.0, pq: 0.82, w: 10e-6, mode: "plain" },
    nasdaq: { d: 56, det: 1.0, pq: 0.82, w: 10e-6, mode: "plain" },
    london: { d: 5570, det: 1.0, pq: 0.82, w: 30e-3, mode: "plain" }
  };

  function $(id) { return document.getElementById(id); }
  var el = {
    dist: $("dist"), det: $("det"), pq: $("pq"), hf: $("hf"), win: $("win"), pb: $("pb"),
    distOut: $("dist-out"), detOut: $("det-out"), pqOut: $("pq-out"), hfOut: $("hf-out"),
    winOut: $("win-out"), pbOut: $("pb-out"), heraldCtl: $("herald-ctl"),
    verdict: $("verdict"), eta: $("r-eta"), etaSub: $("r-eta-sub"), winLabel: $("r-win-label"),
    winR: $("r-win"), winBar: $("r-win-bar"), winMark: $("r-win-mark"), edge: $("r-edge"),
    dmax: $("r-dmax"), dmaxSub: $("r-dmax-sub"), region: $("r-region"), regionSub: $("r-region-sub"),
    biasRead: $("bias-read"), map: $("map")
  };

  // log sliders: integer 0..1000 mapped onto [lo, hi]
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

  function update() {
    var s = state();
    var eta = M.fibre_eta(s.d, undefined, s.det);
    var etaStar = M.eta_threshold(s.pq);
    var winRate = s.herald ? M.heralded_win(s.h, s.pq) : M.all_rounds_win(eta, s.pq);
    var edge = M.edge_per_round(winRate);
    var dmax = M.max_separation_km(etaStar, undefined, s.det);
    var region = M.frontier_region(s.d, s.w, s.pq, s.det);
    var lightT = s.d / C;

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
    el.winR.className = winRate > M.CLASSICAL_MAX + 1e-12 ? "pos" : winRate < M.CLASSICAL_MAX - 1e-12 ? "neg" : "";
    // bar scale 50%..90%
    var lo = 0.5, hi = 0.9;
    el.winBar.style.width = (100 * Math.max(0, Math.min(1, (winRate - lo) / (hi - lo)))) + "%";
    el.winMark.style.left = (100 * (0.75 - lo) / (hi - lo)) + "%";

    el.edge.textContent = money(edge);
    el.edge.className = edge > 0 ? "pos" : "neg";

    if (s.herald) {
      el.dmax.textContent = s.h > 0 ? "No loss limit" : "None";
      el.dmaxSub.textContent = "With heralding, any stored pair helps, so fibre loss lowers the rate of good rounds instead of the win rate. Non-heralded limit at these settings: " + km(dmax) + ".";
    } else {
      el.dmax.textContent = dmax > 0 ? km(dmax) : "0 km";
      el.dmaxSub.textContent = dmax > 0
        ? "Light crosses that in " + dur(dmax / C) + ", so the window must be shorter than that too."
        : "The detectors alone already lose too many photons at this quality.";
    }

    el.region.textContent = REGION_NAMES[region];
    el.region.style.background = REGION_COLORS[region];
    el.regionSub.textContent = REGION_TEXT[region] + " Light needs " + dur(lightT) + " to cross " + km(s.d) + ".";

    var v;
    if (region === M.REGION_GREY) {
      v = "The " + dur(s.w) + " window is longer than the " + dur(lightT) + " light needs to cross " + km(s.d) +
        ". One classical message arrives in time and wins 100% of rounds, so the photons are irrelevant.";
    } else if (winRate > M.CLASSICAL_MAX) {
      v = "No message can arrive in time and quantum wins " + pct(winRate, 1) + " of rounds, beating 75% by " +
        money(edge) + " per round" + (s.herald ? ", but only with quantum memories the startup has not claimed." : ".");
    } else {
      v = "No message can arrive in time, but with only " + pct(eta * eta, 1) + " of rounds getting both photons, the quantum strategy wins " +
        pct(winRate, 1) + ". Classical's 75% is better.";
    }
    el.verdict.textContent = v;

    drawMap(s);
  }

  function updateBias() {
    var p = parseFloat(el.pb.value);
    var cl = M.biased_classical(p), q = M.biased_quantum(p);
    el.pbOut.textContent = pct(p, 0);
    el.biasRead.innerHTML = "Classical best: <strong>" + pct(cl, 1) + "</strong> &middot; Quantum best: <strong>" + pct(q, 1) +
      "</strong> &middot; Gap: <strong>" + (100 * (q - cl)).toFixed(1) + " points</strong>" +
      (q - cl < 1e-12 ? " (quantum offers nothing at this bias)" : "");
  }

  // ---- frontier map ------------------------------------------------------
  var mapCache = { key: "", img: null };

  function cssVar(name) { return getComputedStyle(document.documentElement).getPropertyValue(name).trim(); }

  function drawMap(s) {
    var cv = el.map;
    var dpr = window.devicePixelRatio || 1;
    var cw = cv.clientWidth, ch = cv.clientHeight;
    if (!cw || !ch) return;
    if (cv.width !== Math.round(cw * dpr) || cv.height !== Math.round(ch * dpr)) {
      cv.width = Math.round(cw * dpr); cv.height = Math.round(ch * dpr);
    }
    var ctx = cv.getContext("2d");
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    var narrow = cw < 520;
    var font = (narrow ? 10 : 12) + "px system-ui, -apple-system, sans-serif";
    var pad = { l: narrow ? 44 : 60, r: 10, t: 10, b: narrow ? 34 : 42 };
    var pw = cw - pad.l - pad.r, ph = ch - pad.t - pad.b;
    var ink = cssVar("--ink"), ink2 = cssVar("--ink-2"), bg = cssVar("--panel");

    function X(d) { return pad.l + pw * Math.log(d / D_MIN) / Math.log(D_MAX / D_MIN); }
    function Y(w) { return pad.t + ph * (1 - Math.log(w / W_MIN) / Math.log(W_MAX / W_MIN)); }

    ctx.fillStyle = bg; ctx.fillRect(0, 0, cw, ch);

    // region raster (cached per settings and size)
    var gw = Math.max(1, Math.round(pw * dpr)), gh = Math.max(1, Math.round(ph * dpr));
    var key = [s.pq, s.det, gw, gh].join("|");
    if (mapCache.key !== key) {
      var off = document.createElement("canvas");
      off.width = gw; off.height = gh;
      var octx = off.getContext("2d");
      var img = octx.createImageData(gw, gh);
      var rgb = REGION_COLORS.map(function (h) {
        return [parseInt(h.slice(1, 3), 16), parseInt(h.slice(3, 5), 16), parseInt(h.slice(5, 7), 16)];
      });
      var ds = new Float64Array(gw);
      for (var i = 0; i < gw; i++) ds[i] = D_MIN * Math.pow(D_MAX / D_MIN, (i + 0.5) / gw);
      for (var j = 0; j < gh; j++) {
        var w = W_MIN * Math.pow(W_MAX / W_MIN, 1 - (j + 0.5) / gh);
        for (var k = 0; k < gw; k++) {
          var c = rgb[M.frontier_region(ds[k], w, s.pq, s.det)];
          var o = 4 * (j * gw + k);
          img.data[o] = c[0]; img.data[o + 1] = c[1]; img.data[o + 2] = c[2]; img.data[o + 3] = 255;
        }
      }
      octx.putImageData(img, 0, 0);
      mapCache = { key: key, img: off };
    }
    ctx.imageSmoothingEnabled = false;
    ctx.drawImage(mapCache.img, pad.l, pad.t, pw, ph);

    ctx.save();
    ctx.beginPath(); ctx.rect(pad.l, pad.t, pw, ph); ctx.clip();

    // latency-arbitrage race band, 5-10 us
    ctx.fillStyle = "rgba(36, 89, 168, 0.22)";
    ctx.fillRect(pad.l, Y(10e-6), pw, Y(5e-6) - Y(10e-6));
    ctx.fillStyle = "#104281"; ctx.font = font; ctx.textBaseline = "middle"; ctx.textAlign = "left";
    ctx.fillText(narrow ? "5–10 µs races" : "typical latency-arbitrage race (5–10 µs)", pad.l + 6, Y(7.1e-6));

    // one-bit line
    ctx.strokeStyle = "#1d1d1b"; ctx.lineWidth = 1.4;
    ctx.beginPath(); ctx.moveTo(X(D_MIN), Y(D_MIN / C)); ctx.lineTo(X(D_MAX), Y(D_MAX / C)); ctx.stroke();

    // landmarks
    ctx.lineWidth = 1;
    LANDMARKS.forEach(function (lm, idx) {
      var x = X(lm.km);
      ctx.setLineDash(lm.dash ? [5, 4] : []);
      ctx.strokeStyle = "rgba(29,29,27,0.75)";
      ctx.beginPath(); ctx.moveTo(x, pad.t); ctx.lineTo(x, pad.t + ph); ctx.stroke();
      ctx.setLineDash([]);
      ctx.save();
      var left = idx === 0 || idx === LANDMARKS.length - 1;
      ctx.translate(x + (left ? -4 : 4), pad.t + 8);
      ctx.rotate(Math.PI / 2);
      ctx.fillStyle = "#1d1d1b"; ctx.font = font;
      ctx.textAlign = "left"; ctx.textBaseline = left ? "top" : "bottom";
      ctx.fillText(lm.name, 0, 0);
      ctx.restore();
    });

    // one-bit label along the line
    var a1 = [X(300), Y(300 / C)], a2 = [X(3000), Y(3000 / C)];
    var ang = Math.atan2(a2[1] - a1[1], a2[0] - a1[0]);
    ctx.save();
    ctx.translate(X(narrow ? 150 : 200), Y((narrow ? 150 : 200) / C) - 6);
    ctx.rotate(ang);
    ctx.fillStyle = "#1d1d1b"; ctx.font = font; ctx.textAlign = "left"; ctx.textBaseline = "bottom";
    ctx.fillText(narrow ? "light-travel time" : "one-bit line: light-travel time between desks", 0, 0);
    ctx.restore();

    // current-settings marker
    var mx = X(s.d), my = Y(s.w);
    ctx.lineWidth = 3; ctx.strokeStyle = "#ffffff";
    ctx.beginPath(); ctx.arc(mx, my, 8, 0, 2 * Math.PI); ctx.stroke();
    ctx.lineWidth = 2; ctx.strokeStyle = "#1d1d1b";
    ctx.beginPath(); ctx.arc(mx, my, 8, 0, 2 * Math.PI); ctx.stroke();
    ctx.fillStyle = "#1d1d1b";
    ctx.beginPath(); ctx.arc(mx, my, 2.2, 0, 2 * Math.PI); ctx.fill();
    ctx.restore();

    // frame + axes
    ctx.strokeStyle = ink2; ctx.lineWidth = 1;
    ctx.strokeRect(pad.l + 0.5, pad.t + 0.5, pw - 1, ph - 1);
    ctx.fillStyle = ink; ctx.font = font;
    ctx.textAlign = "center"; ctx.textBaseline = "top";
    [1, 10, 100, 1000, 10000].forEach(function (d) {
      var x = X(d);
      ctx.beginPath(); ctx.moveTo(x, pad.t + ph); ctx.lineTo(x, pad.t + ph + 4); ctx.stroke();
      ctx.textAlign = d === 1 ? "left" : d === 10000 ? "right" : "center";
      ctx.fillText(d.toLocaleString("en-US"), x, pad.t + ph + 6);
    });
    ctx.textAlign = "center";
    ctx.fillStyle = ink2;
    ctx.fillText("Distance between desks (km, log scale)", pad.l + pw / 2, pad.t + ph + (narrow ? 19 : 22));
    ctx.textAlign = "right"; ctx.textBaseline = "middle"; ctx.fillStyle = ink;
    [[1e-6, "1 µs"], [1e-5, "10 µs"], [1e-4, "100 µs"], [1e-3, "1 ms"], [1e-2, "10 ms"], [1e-1, "100 ms"]]
      .forEach(function (t) {
        var y = Y(t[0]);
        ctx.beginPath(); ctx.moveTo(pad.l - 4, y); ctx.lineTo(pad.l, y); ctx.stroke();
        ctx.textBaseline = t[0] === W_MIN ? "bottom" : t[0] === W_MAX ? "top" : "middle";
        ctx.fillText(t[1], pad.l - 6, y);
      });
  }

  // ---- wiring ------------------------------------------------------------
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
      b.classList.toggle("active", b.getAttribute("data-preset") === name);
    });
    update();
  }
  function clearPreset() {
    document.querySelectorAll("[data-preset]").forEach(function (b) { b.classList.remove("active"); });
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
  if (window.matchMedia) {
    var mq = window.matchMedia("(prefers-color-scheme: dark)");
    if (mq.addEventListener) mq.addEventListener("change", update);
  }

  el.hf.value = 0.158;
  applyPreset("startup");
  updateBias();
})();
