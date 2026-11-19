/*
 * home.js - the hero instrument, the frontier map (section 04) and its route table.
 * Inputs (source quality, link length, route distances) come from data/results.json "values";
 * every derived number is computed live by model.js (a line-for-line port of src/chsh.py).
 */
(function () {
  "use strict";
  var M = window.CHSH;
  var C = M.SPEED_OF_LIGHT_KM_S;
  var RACE_MID_S = 7.5e-6;   // midpoint of the 5-10 us race band (E4 uses region_at_7_5us)
  var BLOCK_S = 0.1;         // an illustrative block-order window, slower than the Hibernia-derived 29.5 ms
  var CAUSAL = ["Physically excluded", "Route-dependent", "Arrives on modelled route"];
  var REGION = ["Grey", "Red", "Yellow", "Green"];
  var REGION_LONG = [
    "Grey: one classical bit arrives in time and wins every round",
    "Red: too many photons lost to beat the classical rule",
    "Yellow: only an ideal source near the efficiency floor could win",
    "Green: quantum beats the classical rule at this source quality"
  ];
  var SW = ["sw-grey", "sw-red", "sw-yellow", "sw-green"];

  function $(id) { return document.getElementById(id); }
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
  function money(x) { return (x < 0 ? "−$" : "+$") + Math.abs(x).toFixed(2); }
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }

  var data, V, D, S = {}, current = "startup";

  function scenarios() {
    var lm = {};
    V.e4_landmarks.forEach(function (l) { lm[l.name] = l; });
    var pq = V.inputs.p_quantum_claim;
    var halfGreen = V.e2.p82.d_max_km / 2;
    return {
      startup: { d: V.inputs.link_km, w: RACE_MID_S, wName: "race window",
        note: "The case file's own test link. The source sits at the midpoint, so each photon crosses " + km(V.inputs.link_km / 2) +
          " of fibre at " + D.fibre_loss + "." },
      nasdaq: { d: lm["NYSE–Nasdaq"].km, w: RACE_MID_S, wName: "race window",
        note: "The hedging route Ding & Jiang model. Past about " + D.worst_km + " both photons are usually lost and the desks drift back toward the classical rule, so it scores slightly above the 40 km link and still loses." },
      london: { d: V.inputs.ny_london_km, w: BLOCK_S, wName: "block-order window", route: V.hibernia_one_way_ms / 1000,
        note: "The startup's launch route; no decision window is stated. Slower than " + D.hibernia_one_way + " (half the 2015 Hibernia round-trip benchmark, not a measured one-way service) one bit arrives. Between " +
          D.ny_lon_light_ms + " and " + D.hibernia_one_way + " it is route-dependent; faster than " + D.ny_lon_light_ms + " no bit can arrive, but direct-fibre loss leaves quantum at " + D.classical_max + "." },
      inside: { d: halfGreen, w: RACE_MID_S, wName: "race window",
        note: "Half the " + D.dmax_82 + " break-even distance: the modelled " + D.p_claim + " unheralded strategy only exceeds the classical baseline below ~" + D.dmax_82 + ", under idealized assumptions. No route we checked is this close." },
      _pq: pq
    };
  }

  /* ---- instrument -------------------------------------------------------------------- */
  function compute(id) {
    var s = S[id], pq = S._pq;
    var eta = M.fibre_eta(s.d);
    var win = M.all_rounds_win(eta, pq);
    var region = M.frontier_region(s.d, s.w, pq, 1.0, s.route);
    var causal = M.causal_status(s.d, s.w, s.route);
    return { s: s, eta: eta, both: eta * eta, win: win, region: region, causal: causal, light: s.d / C,
      routeT: M.route_latency_s(s.d, s.route), edge: M.edge_per_round(win) };
  }

  function renderReadouts(r) {
    var grey = r.region === M.REGION_GREY;
    $("ro-main-label").textContent = grey ? "Win rate · one classical bit" : "Win rate · every round counted";
    $("ro-main").textContent = grey ? D.one_bit : pct(r.win, 1);
    $("ro-main-sub").textContent = grey
      ? "The modelled route needs " + dur(r.routeT) + "; the " + r.s.wName + " is longer, so desk A's bit arrives first. Entanglement, every round: " + pct(r.win, 1) + "."
      : (r.win > M.CLASSICAL_MAX
        ? "Beats the free classical rule (" + D.classical_max + ") by " + (100 * (r.win - M.CLASSICAL_MAX)).toFixed(1) + " points."
        : "Below the free classical rule (" + D.classical_max + "). A desk would switch the photons off.");
    // scale 50%..100%
    var lo = 0.5, hi = 1.0, v = grey ? 1.0 : r.win;
    $("scale-mark").style.left = (100 * (v - lo) / (hi - lo)) + "%";
    $("scale-mark").setAttribute("title", grey ? "one bit" : "this route, every round");

    $("ro-eta").textContent = pct(r.eta, 1);
    $("ro-both").textContent = pct(r.both, 1);
    $("ro-light").textContent = dur(r.light) + " / " + dur(r.s.w);
    $("ro-light-dt").textContent = "Light between desks / " + r.s.wName;
    $("ro-edge").textContent = grey ? "n/a" : money(r.edge);
    $("ro-causal").textContent = CAUSAL[r.causal];
    $("ro-region").innerHTML = '<span class="region-word"><span class="sw ' + SW[r.region] + '" aria-hidden="true"></span>' + REGION[r.region] + "</span>";
    var mc = $("ro-mc-row");
    if (current === "startup") {
      mc.hidden = false;
      $("ro-mc").textContent = pct(V.e2.p82.mc_all, 1);
    } else {
      mc.hidden = true;
    }
    $("scen-note").textContent = r.s.note;
    $("inst-status").textContent = labelOf(current) + ": " + $("ro-main-label").textContent + " " + $("ro-main").textContent + ". " + REGION_LONG[r.region] + ".";
  }

  function labelOf(id) {
    var el = document.querySelector('input[name="route"][value="' + id + '"]');
    return el ? el.parentNode.textContent.replace(/\s+/g, " ").trim() : id;
  }

  // SVG: source -> two desks; photon density along each arm = surviving fraction at that point.
  function renderDiagram(r, animate) {
    var host = $("inst-diagram");
    var W = Math.max(330, Math.min(560, host.clientWidth - 8));
    var H = 330;
    var cx = W / 2, deskW = W < 420 ? 96 : 116, ax = deskW / 2 + 4, bx = W - deskW / 2 - 4, deskY = 188;
    var grey = r.region === M.REGION_GREY;
    var fs = 11, fsS = 10;
    var o = [];
    o.push('<svg viewBox="0 0 ' + W + " " + H + '" width="' + W + '" height="' + H + '" role="img" aria-labelledby="dg-title">');
    o.push('<title id="dg-title">Entangled source between two desks ' + esc(km(r.s.d)) + " apart; each desk receives " + pct(r.eta, 1) +
      " of its photons; both photons arrive in " + pct(r.both, 1) + " of rounds.</title>");
    // header line
    o.push('<text x="' + cx + '" y="12" text-anchor="middle" class="dg-text" font-size="' + fsS + '" fill="var(--subtle)" letter-spacing="0.6">' +
      esc(km(r.s.d) + " apart · window " + dur(r.s.w)) + "</text>");
    // source
    o.push('<rect x="' + (cx - 62) + '" y="30" width="124" height="40" fill="var(--background)" stroke="var(--border-strong)"/>');
    o.push('<text x="' + cx + '" y="47" text-anchor="middle" class="dg-text" font-size="' + fs + '" fill="var(--foreground)">pair source</text>');
    o.push('<text x="' + cx + '" y="62" text-anchor="middle" class="dg-text" font-size="' + fsS + '" fill="var(--subtle)">p_q ' + esc(D.p_claim) + "</text>");
    // arms
    var arms = [[cx - 20, 70, ax, deskY - 22], [cx + 20, 70, bx, deskY - 22]];
    arms.forEach(function (a, i) {
      var d = "M" + a[0] + " " + a[1] + " C" + a[0] + " " + (a[1] + 60) + " " + a[2] + " " + (a[3] - 60) + " " + a[2] + " " + a[3];
      o.push('<path d="' + d + '" pathLength="1" fill="none" stroke="var(--border-strong)" class="dg-arm' + (animate ? " draw" : "") + '"/>');
      // photons along the arm
      var n = 9;
      for (var k = 1; k <= n; k++) {
        var t = k / (n + 1);
        var alive = Math.pow(10, -(M.FIBRE_LOSS_DB_PER_KM * (r.s.d / 2) * t) / 10);
        var p = bez(a, t);
        o.push('<circle cx="' + p[0].toFixed(1) + '" cy="' + p[1].toFixed(1) + '" r="2.6" fill="var(--foreground)" opacity="' +
          Math.max(0.06, alive).toFixed(3) + '" class="' + (animate ? "dg-fade" : "") + '"/>');
      }
      var m = bez(a, 0.5);
      var lx = i === 0 ? m[0] - 10 : m[0] + 10;
      o.push('<text x="' + lx.toFixed(1) + '" y="' + (m[1] - 4).toFixed(1) + '" text-anchor="' + (i === 0 ? "end" : "start") +
        '" class="dg-text" font-size="' + fsS + '" fill="var(--subtle)">' + esc(km(r.s.d / 2)) + "</text>");
    });
    // desks
    [["desk A", ax], ["desk B", bx]].forEach(function (dk) {
      o.push('<rect x="' + (dk[1] - deskW / 2) + '" y="' + (deskY - 22) + '" width="' + deskW + '" height="44" fill="var(--background)" stroke="var(--border-strong)"/>');
      o.push('<text x="' + dk[1] + '" y="' + (deskY - 5) + '" text-anchor="middle" class="dg-text" font-size="' + fs + '" fill="var(--foreground)">' + dk[0] + "</text>");
      o.push('<text x="' + dk[1] + '" y="' + (deskY + 11) + '" text-anchor="middle" class="dg-text" font-size="' + fsS + '" fill="var(--muted)">photon ' +
        esc(r.eta < 0.001 ? "<0.1%" : pct(r.eta, 1)) + "</text>");
    });
    // the classical bit, when it arrives in time
    var by = deskY + 34;
    if (grey) {
      o.push('<path d="M' + (ax + deskW / 2) + " " + deskY + " L" + (bx - deskW / 2 - 6) + " " + deskY + '" stroke="var(--foreground)" stroke-dasharray="3 3" fill="none"/>');
      o.push('<path d="M' + (bx - deskW / 2 - 6) + " " + (deskY - 4) + " L" + (bx - deskW / 2) + " " + deskY + " L" + (bx - deskW / 2 - 6) + " " + (deskY + 4) + 'Z" fill="var(--foreground)"/>');
      o.push('<text x="' + cx + '" y="' + (deskY - 8) + '" text-anchor="middle" class="dg-text" font-size="' + fsS + '" fill="var(--foreground)">1 bit · ' + esc(dur(r.light)) + "</text>");
    } else {
      o.push('<text x="' + cx + '" y="' + (deskY + 4) + '" text-anchor="middle" class="dg-text" font-size="' + fsS + '" fill="var(--subtle)">no time to talk</text>');
    }
    // 20 rounds, expected mix
    var N = 20, both = Math.round(N * r.both), none = Math.round(N * (1 - r.eta) * (1 - r.eta));
    if (both + none > N) none = N - both;
    var one = N - both - none;
    var cell = W < 420 ? 11 : 13, gap = 3, sw = N * cell + (N - 1) * gap, sx = cx - sw / 2, sy = by + 34;
    o.push('<text x="' + sx + '" y="' + (sy - 9) + '" class="dg-text" font-size="' + fsS + '" fill="var(--subtle)" letter-spacing="0.6">20 ROUNDS, EXPECTED MIX</text>');
    o.push('<text x="' + (sx + sw) + '" y="' + (sy - 9) + '" text-anchor="end" class="dg-text" font-size="' + fsS + '" fill="var(--foreground)">both ' + esc(pct(r.both, 1)) + "</text>");
    for (var i = 0; i < N; i++) {
      var x = sx + i * (cell + gap);
      var kind = i < both ? 2 : i < both + one ? 1 : 0;
      o.push('<rect x="' + (x + 0.5) + '" y="' + (sy + 0.5) + '" width="' + (cell - 1) + '" height="' + (cell - 1) + '" fill="' + (kind === 2 ? "var(--foreground)" : "none") + '" stroke="var(--muted)"/>');
      if (kind === 1) o.push('<path d="M' + x + " " + (sy + cell) + " L" + (x + cell) + " " + sy + " L" + (x + cell) + " " + (sy + cell) + 'Z" fill="var(--muted)"/>');
    }
    var ly = sy + cell + 18;
    o.push('<g class="dg-text" font-size="' + fsS + '" fill="var(--subtle)">' +
      '<rect x="' + sx + '" y="' + (ly - 8) + '" width="8" height="8" fill="var(--foreground)"/><text x="' + (sx + 12) + '" y="' + ly + '">both photons</text>' +
      '<rect x="' + (sx + 104) + '" y="' + (ly - 8) + '" width="8" height="8" fill="none" stroke="var(--muted)"/><path d="M' + (sx + 104) + " " + ly + " l8 -8 v8Z" + '" fill="var(--muted)"/><text x="' + (sx + 116) + '" y="' + ly + '">one</text>' +
      '<rect x="' + (sx + 152) + '" y="' + (ly - 8) + '" width="8" height="8" fill="none" stroke="var(--muted)"/><text x="' + (sx + 164) + '" y="' + ly + '">none</text></g>');
    o.push("</svg>");
    host.innerHTML = o.join("");
  }

  function bez(a, t) {
    // cubic with control points (x0, y0+60) and (x1, y1-60)
    var p0 = [a[0], a[1]], p1 = [a[0], a[1] + 60], p2 = [a[2], a[3] - 60], p3 = [a[2], a[3]];
    var u = 1 - t;
    return [0, 1].map(function (k) {
      return u * u * u * p0[k] + 3 * u * u * t * p1[k] + 3 * u * t * t * p2[k] + t * t * t * p3[k];
    });
  }

  function select(id, animate) {
    current = id;
    document.querySelectorAll('input[name="route"]').forEach(function (inp) {
      inp.parentNode.classList.toggle("is-on", inp.value === id);
    });
    var r = compute(id);
    renderReadouts(r);
    renderDiagram(r, animate);
  }

  /* ---- map + route table ---------------------------------------------------------------- */
  function drawMap() {
    var cv = $("home-map");
    if (!cv) return;
    window.Frontier.draw(cv, {
      pq: S._pq, det: 1.0, marker: null, raceLabel: D.race_window, key: "home",
      points: [{ d: V.inputs.ny_london_km, w: V.hibernia_one_way_ms / 1000, label: ["NY–LON " + D.hibernia_one_way, "FROM 2015 HIBERNIA ROUND TRIP"] }],
      landmarks: [
        { name: "Startup " + D.link_km, km: V.inputs.link_km, dash: true },
        { name: "NYSE–Nasdaq", km: S.nasdaq.d },
        { name: "NY–London", km: V.inputs.ny_london_km }
      ]
    });
  }

  function routeTable() {
    var tb = $("route-rows");
    if (!tb) return;
    var kmKey = { "Carteret–Secaucus": "carteret_km", "Startup 40 km test link": "link_km", "NYSE–Nasdaq": "nasdaq_km", "New York–London": "ny_lon_km" };
    tb.innerHTML = V.e4_landmarks.map(function (l) {
      var dist = kmKey[l.name] ? D[kmKey[l.name]] : km(l.km);
      return "<tr><td data-label=\"Route\">" + esc(l.name) + "</td>" +
        '<td class="num" data-label="Distance">' + esc(dist) + "</td>" +
        '<td class="num" data-label="Light time">' + esc(dur(l.light_time_us * 1e-6)) + "</td>" +
        '<td class="num" data-label="Every-round win">' + esc(pct(l.win_all_rounds_82, 1)) + "</td>" +
        '<td data-label="At the race window"><span class="region-word"><span class="sw ' + SW[l.region_at_7_5us] + '" aria-hidden="true"></span>' + REGION[l.region_at_7_5us] + "</span></td>" +
        '<td data-label="At a 1 ms window"><span class="region-word"><span class="sw ' + SW[l.region_at_1ms] + '" aria-hidden="true"></span>' + REGION[l.region_at_1ms] + "</span></td>" +
        '<td data-label="One bit at 20 ms">' + (typeof l.causal_at_20ms === "number" ? CAUSAL[l.causal_at_20ms] : "n/a") + "</td></tr>";
    }).join("");
  }

  function cheatStrip() {
    var g = $("cheat-strip");
    if (!g) return;
    var N = 32, kept = Math.round(N * V.e3.exact_retained), out = [];
    // spread the discarded rounds evenly through the strip
    var drop = {};
    for (var k = 0; k < N - kept; k++) drop[Math.floor((k + 0.5) * N / (N - kept))] = true;
    for (var i = 0; i < N; i++) {
      var x = (i % 16) * 21, y = 28 + Math.floor(i / 16) * 26;
      out.push('<rect x="' + (x + 0.5) + '" y="' + (y + 0.5) + '" width="15" height="15" fill="' + (drop[i] ? "none" : "var(--foreground)") +
        '" stroke="' + (drop[i] ? "var(--border-strong)" : "var(--foreground)") + '"' + (drop[i] ? ' stroke-dasharray="2 2"' : "") + "/>");
    }
    g.innerHTML = out.join("");
  }

  function failState() {
    var msg = '<div class="state" role="alert"><p class="label-mono">Results unavailable</p>' +
      "<p>The instrument reads its inputs from <code>data/results.json</code>, which did not load. " +
      "Build the site with <code>python scripts/build_site.py</code> and serve the output over HTTP.</p></div>";
    $("inst-diagram").innerHTML = msg;
    ["ro-main", "ro-eta", "ro-both", "ro-light", "ro-edge", "ro-region", "ro-causal"].forEach(function (id) {
      var e = $(id); if (e) { e.textContent = "n/a"; e.classList.add("r-missing"); }
    });
    var mb = $("home-map");
    if (mb) mb.parentNode.innerHTML = msg;
    var tb = $("route-rows");
    if (tb) tb.innerHTML = '<tr><td colspan="7" class="r-missing">Route values unavailable: results.json did not load.</td></tr>';
  }

  window.Results.ready.then(function (d) {
    if (!d) { failState(); return; }
    data = d; V = d.values; D = d.display;
    S = scenarios();
    document.querySelectorAll('input[name="route"]').forEach(function (inp) {
      inp.addEventListener("change", function () { if (inp.checked) select(inp.value, true); });
    });
    var ideal = (100 * (M.IDEAL_QUANTUM_WIN - 0.5) / 0.5) + "%";
    $("tick-ideal").style.left = ideal; $("lbl-ideal").style.left = ideal;
    cheatStrip();
    select("startup", false);
    drawMap();
    routeTable();
    var rt;
    window.addEventListener("resize", function () {
      clearTimeout(rt);
      rt = setTimeout(function () { renderDiagram(compute(current), false); drawMap(); }, 80);
    });
  });
})();
