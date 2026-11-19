/*
 * frontier.js - draws the frontier map (desk separation x decision window) on a canvas.
 * Every cell is classified by CHSH.frontier_region from model.js; nothing is precomputed.
 * Dark-theme tones: grey = neutral surface, red = danger-tinted, yellow = warn-tinted, green = mint.
 * Shared by index.html (section 04) and exhibit.html.
 */
(function () {
  "use strict";
  var M = window.CHSH;
  var C = M.SPEED_OF_LIGHT_KM_S;
  var D_MIN = 1, D_MAX = 1e4;     // km
  var W_MIN = 1e-6, W_MAX = 1e-1; // s
  var cache = {};

  function cssVar(name) { return getComputedStyle(document.documentElement).getPropertyValue(name).trim(); }
  function hexRgb(h) {
    h = h.replace("#", "");
    return [parseInt(h.slice(0, 2), 16), parseInt(h.slice(2, 4), 16), parseInt(h.slice(4, 6), 16)];
  }

  /*
   * opts: { pq, det, marker: {d, w} | null, landmarks: [{name, km, dash}], points: [{d, w, label: [lines]}],
 *         raceLabel, key }. Regions use the default modelled route (straight-line fibre at c/1.468).
   */
  function draw(cv, opts) {
    var dpr = window.devicePixelRatio || 1;
    var cw = cv.clientWidth, ch = cv.clientHeight;
    if (!cw || !ch) return;
    if (cv.width !== Math.round(cw * dpr) || cv.height !== Math.round(ch * dpr)) {
      cv.width = Math.round(cw * dpr); cv.height = Math.round(ch * dpr);
    }
    var ctx = cv.getContext("2d");
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    var narrow = cw < 560;
    var mono = cssVar("--font-mono") || "monospace";
    var font = (narrow ? 10 : 11) + "px " + mono;
    var pad = { l: narrow ? 46 : 76, r: 8, t: 8, b: narrow ? 38 : 44 };
    var pw = cw - pad.l - pad.r, ph = ch - pad.t - pad.b;
    var fg = cssVar("--foreground"), axis = cssVar("--chart-axis"), muted = cssVar("--muted");
    var bg = cssVar("--background"), border = cssVar("--border-strong"), info = cssVar("--info");

    function X(d) { return pad.l + pw * Math.log(d / D_MIN) / Math.log(D_MAX / D_MIN); }
    function Y(w) { return pad.t + ph * (1 - Math.log(w / W_MIN) / Math.log(W_MAX / W_MIN)); }

    ctx.fillStyle = bg; ctx.fillRect(0, 0, cw, ch);

    // region raster, cached per (settings, size)
    var gw = Math.max(1, Math.round(pw * dpr)), gh = Math.max(1, Math.round(ph * dpr));
    var key = (opts.key || "") + "|" + [opts.pq, opts.det, gw, gh].join("|");
    var off = cache[key];
    if (!off) {
      off = document.createElement("canvas");
      off.width = gw; off.height = gh;
      var octx = off.getContext("2d");
      var img = octx.createImageData(gw, gh);
      var rgb = ["--map-grey", "--map-red", "--map-yellow", "--map-green"].map(function (n) { return hexRgb(cssVar(n)); });
      var ds = new Float64Array(gw);
      for (var i = 0; i < gw; i++) ds[i] = D_MIN * Math.pow(D_MAX / D_MIN, (i + 0.5) / gw);
      for (var j = 0; j < gh; j++) {
        var w = W_MIN * Math.pow(W_MAX / W_MIN, 1 - (j + 0.5) / gh);
        for (var k = 0; k < gw; k++) {
          var c = rgb[M.frontier_region(ds[k], w, opts.pq, opts.det)];
          var o = 4 * (j * gw + k);
          img.data[o] = c[0]; img.data[o + 1] = c[1]; img.data[o + 2] = c[2]; img.data[o + 3] = 255;
        }
      }
      octx.putImageData(img, 0, 0);
      cache = {}; cache[key] = off;
    }
    ctx.imageSmoothingEnabled = false;
    ctx.drawImage(off, pad.l, pad.t, pw, ph);

    ctx.save();
    ctx.beginPath(); ctx.rect(pad.l, pad.t, pw, ph); ctx.clip();
    ctx.font = font;

    // latency-arbitrage race band, 5-10 us (Aquilina, Budish & O'Neill)
    var y10 = Y(10e-6), y5 = Y(5e-6);
    ctx.fillStyle = "rgba(174, 198, 238, 0.10)";
    ctx.fillRect(pad.l, y10, pw, y5 - y10);
    ctx.strokeStyle = info; ctx.lineWidth = 1; ctx.setLineDash([3, 3]);
    ctx.beginPath(); ctx.moveTo(pad.l, y10 + 0.5); ctx.lineTo(pad.l + pw, y10 + 0.5);
    ctx.moveTo(pad.l, y5 - 0.5); ctx.lineTo(pad.l + pw, y5 - 0.5); ctx.stroke();
    ctx.setLineDash([]);
    ctx.fillStyle = info; ctx.textBaseline = "middle"; ctx.textAlign = "right";
    ctx.fillText(((opts.raceLabel || "") + (narrow ? " EQUITY RACES" : " EQUITY LATENCY RACES (CONTEXT, OTHER MARKET)")).trim(), pad.l + pw - 8, (y10 + y5) / 2);

    // route-dependent band: physics allows a bit (window > d/c) but the modelled straight-line
    // fibre route (d / (c/1.468)) is too slow. Hatched, between the two lines.
    var VF = M.FIBRE_SPEED_KM_S;
    var hatch = document.createElement("canvas");
    hatch.width = hatch.height = 6;
    var hc = hatch.getContext("2d");
    hc.strokeStyle = "rgba(244, 244, 245, 0.28)"; hc.lineWidth = 1;
    hc.beginPath(); hc.moveTo(0, 6); hc.lineTo(6, 0); hc.moveTo(-1, 1); hc.lineTo(1, -1); hc.moveTo(5, 7); hc.lineTo(7, 5); hc.stroke();
    ctx.fillStyle = ctx.createPattern(hatch, "repeat");
    ctx.beginPath();
    ctx.moveTo(X(D_MIN), Y(D_MIN / C)); ctx.lineTo(X(D_MAX), Y(D_MAX / C));
    ctx.lineTo(X(D_MAX), Y(D_MAX / VF)); ctx.lineTo(X(D_MIN), Y(D_MIN / VF)); ctx.closePath();
    ctx.fill();

    // the two lines: d/c (physical limit, solid) and the fibre route (dashed)
    ctx.strokeStyle = fg; ctx.lineWidth = 1;
    ctx.beginPath(); ctx.moveTo(X(D_MIN), Y(D_MIN / C)); ctx.lineTo(X(D_MAX), Y(D_MAX / C)); ctx.stroke();
    ctx.setLineDash([4, 3]);
    ctx.beginPath(); ctx.moveTo(X(D_MIN), Y(D_MIN / VF)); ctx.lineTo(X(D_MAX), Y(D_MAX / VF)); ctx.stroke();
    ctx.setLineDash([]);
    var a1 = [X(300), Y(300 / C)], a2 = [X(3000), Y(3000 / C)];
    var ang = Math.atan2(a2[1] - a1[1], a2[0] - a1[0]);
    var at = narrow ? 40 : 60;
    ctx.save();
    ctx.translate(X(at), Y(at / VF) - 5);
    ctx.rotate(ang);
    ctx.fillStyle = fg; ctx.textAlign = "left"; ctx.textBaseline = "bottom";
    ctx.fillText(narrow ? "BIT ARRIVES ON FIBRE ROUTE" : "ABOVE: ONE BIT ARRIVES ON A STRAIGHT FIBRE ROUTE (c/1.468)", 0, 0);
    ctx.restore();
    ctx.save();
    ctx.translate(X(at), Y(at / C) + 5);
    ctx.rotate(ang);
    ctx.fillStyle = muted; ctx.textAlign = "left"; ctx.textBaseline = "top";
    ctx.fillText(narrow ? "NO BIT CAN ARRIVE (d/c)" : "BELOW: NO SIGNAL CAN ARRIVE AT ALL (d/c)", 0, 0);
    ctx.restore();

    // routes
    (opts.landmarks || []).forEach(function (lm, idx, arr) {
      var x = Math.round(X(lm.km)) + 0.5;
      ctx.setLineDash(lm.dash ? [4, 3] : [1, 3]);
      ctx.strokeStyle = muted;
      ctx.beginPath(); ctx.moveTo(x, pad.t); ctx.lineTo(x, pad.t + ph); ctx.stroke();
      ctx.setLineDash([]);
      ctx.save();
      var left = idx === 0 || idx === arr.length - 1;
      ctx.translate(x + (left ? -5 : 5), pad.t + 8);
      ctx.rotate(Math.PI / 2);
      ctx.fillStyle = fg; ctx.textAlign = "left"; ctx.textBaseline = left ? "top" : "bottom";
      ctx.fillText(lm.name.toUpperCase(), 0, 0);
      ctx.restore();
    });

    // region labels (inside the plot, only where there is room)
    ctx.textBaseline = "middle"; ctx.textAlign = "left";
    ctx.fillStyle = muted;
    ctx.fillText("GREY · ONE BIT WINS", pad.l + 8, pad.t + 14);
    ctx.fillStyle = "#f0a3a3";
    ctx.textAlign = "right";
    ctx.fillText("RED · PHOTONS LOST", pad.l + pw - 8, Y(2e-6));

    // labelled points (e.g. New York-London at the Hibernia-derived one-way latency)
    (opts.points || []).forEach(function (pt) {
      var px = X(pt.d), py = Y(pt.w);
      ctx.fillStyle = fg; ctx.strokeStyle = bg; ctx.lineWidth = 2;
      ctx.beginPath(); ctx.moveTo(px, py - 5); ctx.lineTo(px + 5, py); ctx.lineTo(px, py + 5); ctx.lineTo(px - 5, py); ctx.closePath();
      ctx.stroke(); ctx.fill();
      ctx.textAlign = "right"; ctx.textBaseline = "middle";
      var lines = pt.label;
      ctx.fillStyle = bg;
      lines.forEach(function (ln, i) {
        var w = ctx.measureText(ln).width;
        ctx.fillRect(px - 10 - w - 3, py - 7 + i * 13 - 6 + 6, w + 6, 13);
      });
      ctx.fillStyle = fg;
      lines.forEach(function (ln, i) { ctx.fillText(ln, px - 10, py + i * 13); });
    });

    // current-settings marker
    if (opts.marker) {
      var mx = X(Math.max(D_MIN, Math.min(D_MAX, opts.marker.d))), my = Y(Math.max(W_MIN, Math.min(W_MAX, opts.marker.w)));
      ctx.lineWidth = 3; ctx.strokeStyle = bg;
      ctx.beginPath(); ctx.arc(mx, my, 8, 0, 2 * Math.PI); ctx.stroke();
      ctx.lineWidth = 1.5; ctx.strokeStyle = fg;
      ctx.beginPath(); ctx.arc(mx, my, 8, 0, 2 * Math.PI); ctx.stroke();
      ctx.fillStyle = fg;
      ctx.beginPath(); ctx.arc(mx, my, 2, 0, 2 * Math.PI); ctx.fill();
    }
    ctx.restore();

    // frame + axes (Mono 11px, --chart-axis)
    ctx.strokeStyle = border; ctx.lineWidth = 1;
    ctx.strokeRect(pad.l + 0.5, pad.t + 0.5, pw - 1, ph - 1);
    ctx.font = font; ctx.fillStyle = axis; ctx.strokeStyle = axis;
    ctx.textBaseline = "top";
    [1, 10, 100, 1000, 10000].forEach(function (d) {
      var x = Math.round(X(d)) + 0.5;
      ctx.beginPath(); ctx.moveTo(x, pad.t + ph); ctx.lineTo(x, pad.t + ph + 4); ctx.stroke();
      ctx.textAlign = d === 1 ? "left" : d === 10000 ? "right" : "center";
      ctx.fillText(d.toLocaleString("en-US"), x, pad.t + ph + 7);
    });
    ctx.textAlign = "center";
    ctx.fillText("DISTANCE BETWEEN DESKS (KM, LOG)", pad.l + pw / 2, pad.t + ph + (narrow ? 22 : 25));
    ctx.textAlign = "right";
    [[1e-6, "1 µs"], [1e-5, "10 µs"], [1e-4, "100 µs"], [1e-3, "1 ms"], [1e-2, "10 ms"], [1e-1, "100 ms"]]
      .forEach(function (t) {
        var y = Math.round(Y(t[0])) + 0.5;
        ctx.beginPath(); ctx.moveTo(pad.l - 4, y); ctx.lineTo(pad.l, y); ctx.stroke();
        ctx.textBaseline = t[0] === W_MIN ? "bottom" : t[0] === W_MAX ? "top" : "middle";
        ctx.fillText(t[1], pad.l - 7, y);
      });
    if (narrow) return;
    ctx.save();
    ctx.translate(10, pad.t + ph / 2);
    ctx.rotate(-Math.PI / 2);
    ctx.textAlign = "center"; ctx.textBaseline = "middle";
    ctx.fillText("TIME ALLOWED TO DECIDE (LOG)", 0, 0);
    ctx.restore();
  }

  window.Frontier = { draw: draw, D_MIN: D_MIN, D_MAX: D_MAX, W_MIN: W_MIN, W_MAX: W_MAX };
})();
