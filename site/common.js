/*
 * common.js - shared by every page. No dependencies.
 *  1. Fetches data/results.json and fills every <span data-r="key"> from its "display" section
 *     (the exact strings the writing uses) and every <span data-v="a.b.c"> from "values".
 *     If the file cannot be loaded, every slot shows an explicit "unavailable" marker and the
 *     banner turns into an alert; nothing is left blank and nothing falls back to a typed number.
 *  2. Renders evidence labels (<span class="ev" data-kind="exact">) from one table, so the
 *     wording and glyph of each kind is defined once (QMint's EvidenceLabel grammar).
 *  3. Nav: hairline on scroll, mobile sheet. Copy buttons on code blocks. Missing-PDF state.
 * Other scripts wait on window.Results.ready (resolves to the parsed JSON, or null on failure).
 */
(function () {
  "use strict";

  /* ---- evidence labels: shape = origin, colour = tone (see style.css .ev) ------------ */
  var KINDS = {
    "exact": { label: "Exact", origin: "theory", tone: "info",
      title: "Closed-form value from the model (src/chsh.py, ported to model.js). No sampling." },
    "monte-carlo": { label: "Monte-Carlo", origin: "simulated", tone: "neutral",
      title: "Estimated by simulating rounds with photons actually dropped (fixed seed). A check on the exact value." },
    "claim": { label: "Case-file claim", origin: "claim", tone: "warn",
      title: "A number the startup or the case file asserts. Treated as a claim, not as a fact." },
    "published": { label: "Published source", origin: "measured", tone: "info",
      title: "A value taken from published work; see the source list on the Evidence page." },
    "assumption": { label: "Assumption", origin: "numeric", tone: "neutral",
      title: "A modelling choice. The assumptions table says whom each one favours." },
    "inference": { label: "Inference", origin: "numeric", tone: "warn",
      title: "Our reading of an ambiguous claim, derived from the model. Needs the raw logs to confirm." },
    "unproven": { label: "Unproven", origin: "none", tone: "warn",
      title: "A hypothesis worth testing, not a demonstrated result or market." }
  };

  function renderEvidence(root) {
    (root || document).querySelectorAll(".ev[data-kind]").forEach(function (el) {
      if (el.getAttribute("data-done")) return;
      var k = KINDS[el.getAttribute("data-kind")];
      if (!k) { el.textContent = el.getAttribute("data-kind"); return; }
      el.setAttribute("data-origin", k.origin);
      el.setAttribute("data-tone", k.tone);
      el.setAttribute("title", k.title);
      el.textContent = el.getAttribute("data-text") || k.label;
      var sr = document.createElement("span");
      sr.className = "sr-only";
      sr.textContent = ": " + k.title;
      el.appendChild(sr);
      el.setAttribute("data-done", "1");
    });
  }

  /* ---- results.json ------------------------------------------------------------------- */
  var URL = "data/results.json";

  function getPath(obj, path) {
    return path.split(".").reduce(function (o, k) { return o == null ? undefined : o[k]; }, obj);
  }

  function fill(data, root) {
    (root || document).querySelectorAll("[data-r]").forEach(function (el) {
      var key = el.getAttribute("data-r");
      var v = data.display[key];
      if (v === undefined) { markMissing(el, "missing key " + key); return; }
      el.textContent = v;
    });
    (root || document).querySelectorAll("[data-v]").forEach(function (el) {
      var v = getPath(data.values, el.getAttribute("data-v"));
      if (typeof v !== "number") { markMissing(el, "missing value"); return; }
      el.textContent = Number.isInteger(v) ? v.toLocaleString("en-US") : String(v);
    });
  }

  function markMissing(el, why) {
    el.textContent = "n/a";
    el.classList.add("r-missing");
    el.setAttribute("title", "Unavailable: " + why);
  }

  function fail(err) {
    document.querySelectorAll("[data-r], [data-v]").forEach(function (el) { markMissing(el, "results.json did not load"); });
    var b = document.querySelector(".banner");
    if (b) {
      b.classList.add("is-error");
      b.setAttribute("role", "alert");
      b.textContent = "Could not load " + URL + " (" + (err && err.message ? err.message : "network error") +
        "). Numbers on this page are unavailable. Build the site with scripts/build_site.py and serve it over HTTP.";
    }
    document.documentElement.classList.add("results-failed");
    return null;
  }

  var ready = fetch(URL, { cache: "no-cache" })
    .then(function (r) {
      if (!r.ok) throw new Error("HTTP " + r.status);
      return r.json();
    })
    .then(function (data) {
      if (!data || !data.display || !data.values) throw new Error("unexpected format");
      fill(data);
      document.documentElement.classList.add("results-ok");
      return data;
    })
    .catch(fail);

  window.Results = { ready: ready, fill: fill, renderEvidence: renderEvidence, kinds: KINDS };

  /* ---- nav ---------------------------------------------------------------------------- */
  function initNav() {
    var nav = document.querySelector(".nav");
    if (!nav) return;
    var onScroll = function () { nav.classList.toggle("is-scrolled", window.scrollY > 8); };
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
    var btn = nav.querySelector(".nav-toggle");
    var sheet = document.getElementById("nav-sheet");
    if (!btn || !sheet) return;
    function set(open) {
      btn.setAttribute("aria-expanded", String(open));
      btn.setAttribute("aria-label", open ? "Close menu" : "Open menu");
      sheet.hidden = !open;
      nav.classList.toggle("is-open", open);
      btn.querySelector(".i-open").style.display = open ? "none" : "";
      btn.querySelector(".i-close").style.display = open ? "" : "none";
    }
    btn.addEventListener("click", function () { set(btn.getAttribute("aria-expanded") !== "true"); });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && btn.getAttribute("aria-expanded") === "true") { set(false); btn.focus(); }
    });
    sheet.querySelectorAll("a").forEach(function (a) { a.addEventListener("click", function () { set(false); }); });
  }

  /* ---- copy buttons on code blocks ------------------------------------------------------ */
  function initCopy() {
    document.querySelectorAll("pre.code[data-copy]").forEach(function (pre) {
      var b = document.createElement("button");
      b.type = "button";
      b.className = "btn btn-ghost btn-sm copy-btn";
      b.textContent = "Copy";
      b.setAttribute("aria-label", "Copy command");
      b.addEventListener("click", function () {
        var text = pre.querySelector("code").textContent;
        var done = function () { b.textContent = "Copied"; setTimeout(function () { b.textContent = "Copy"; }, 1400); };
        if (navigator.clipboard) navigator.clipboard.writeText(text).then(done, function () { b.textContent = "Select and copy"; });
        else b.textContent = "Select and copy";
      });
      pre.appendChild(b);
    });
  }

  /* ---- PDFs that are not part of this build ---------------------------------------------- */
  function initPdfs() {
    document.querySelectorAll("a[data-pdf]").forEach(function (a) {
      fetch(a.getAttribute("href"), { method: "HEAD" }).then(function (r) {
        if (r.ok) return;
        var s = document.createElement("span");
        s.className = "is-missing";
        s.textContent = a.textContent.replace(/\s*↗\s*$/, "") + " (PDF not in this build; run scripts/package.sh)";
        a.replaceWith(s);
      }).catch(function () { /* offline: leave the link */ });
    });
  }

  function init() {
    renderEvidence();
    initNav();
    initCopy();
    initPdfs();
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init);
  else init();
})();
