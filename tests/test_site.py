"""Site integrity: the static website in site/ as assembled by scripts/build_site.py.

- every <... data-r="key"> used in site/*.html exists in results.json "display" (data-v paths in "values")
- every relative href/src (and CSS url()) resolves inside the assembled _site, including #fragments
- each page has one <h1>, one <main id="main"> and a skip link
- no result string from "display" is typed into the HTML outside a data-r slot
- site/model.js still exports its API, plus the causal-state and heralded-supply functions
- the causal-state spec (d/c and 1.47 d/c boundaries, quoted route latency) holds in model.js, and
  model.js matches src/chsh.py on those functions once the Python model implements the same spec
"""
import importlib.util
import json
import math
import re
import shutil
import subprocess
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit

import pytest

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "site"
PAGES = sorted(SITE.glob("*.html"))
RESULTS = json.loads((ROOT / "results" / "results.json").read_text())
DISPLAY, VALUES = RESULTS["display"], RESULTS["values"]
NODE = shutil.which("node")

sys.path.insert(0, str(ROOT))
from src import chsh  # noqa: E402


def load_build():
    spec = importlib.util.spec_from_file_location("build_site", ROOT / "scripts" / "build_site.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


class Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.refs, self.ids, self.data_r, self.data_v = [], set(), [], []
        self.h1 = 0
        self.main_ids = []
        self.skip = False
        self.text = []          # text outside data-r / data-v slots, script and style
        self._stack = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        for k in ("href", "src"):
            if a.get(k):
                self.refs.append(a[k])
        if "id" in a:
            self.ids.add(a["id"])
        if "data-r" in a:
            self.data_r.append(a["data-r"])
        if "data-v" in a:
            self.data_v.append(a["data-v"])
        if tag == "h1":
            self.h1 += 1
        if tag == "main":
            self.main_ids.append(a.get("id"))
        if tag == "a" and a.get("href") == "#main" and "skip" in (a.get("class") or ""):
            self.skip = True
        void = tag in {"meta", "link", "img", "input", "br", "hr", "col", "source", "path", "rect", "circle"}
        if not void:
            self._stack.append(tag in {"script", "style"} or "data-r" in a or "data-v" in a)

    def handle_endtag(self, tag):
        if self._stack:
            self._stack.pop()

    def handle_data(self, data):
        if not any(self._stack):
            self.text.append(data)


def parse(path):
    p = Page()
    p.feed(path.read_text(encoding="utf-8"))
    return p


PARSED = {p.name: parse(p) for p in PAGES}


@pytest.fixture(scope="module")
def built(tmp_path_factory):
    out = tmp_path_factory.mktemp("site") / "_site"
    warnings = load_build().build(out)
    return out, warnings


def test_pages_exist():
    assert {p.name for p in PAGES} >= {"index.html", "exhibit.html", "findings.html", "evidence.html", "reproduce.html"}


def test_build_layout(built):
    out, warnings = built
    assert (out / "data" / "results.json").read_text() == (ROOT / "results" / "results.json").read_text()
    assert (out / ".nojekyll").exists()
    for png in (ROOT / "figures").glob("*.png"):
        assert (out / "figures" / png.name).exists()
    assert (out / "fonts" / "GeistPixel-Square.woff2").exists() and (out / "fonts" / "OFL.txt").exists()
    # the only acceptable warnings are PDFs that have not been built yet
    assert all(w.startswith("reports/") and ".pdf" in w for w in warnings)


@pytest.mark.parametrize("page", [p.name for p in PAGES])
def test_data_r_keys_exist(page):
    missing = sorted({k for k in PARSED[page].data_r if k not in DISPLAY})
    assert not missing, f"{page}: data-r keys not in results.json display: {missing}"
    bad_v = []
    for path in PARSED[page].data_v:
        v = VALUES
        for part in path.split("."):
            v = v.get(part) if isinstance(v, dict) else None
        if not isinstance(v, (int, float)):
            bad_v.append(path)
    assert not bad_v, f"{page}: data-v paths not numeric in results.json values: {bad_v}"


def _resolve(out, page, ref, missing_pdfs):
    parts = urlsplit(ref)
    if parts.scheme or ref.startswith("//") or ref.startswith("mailto:"):
        return None
    target = (out / page).parent / parts.path if parts.path else out / page
    target = target.resolve()
    if out.resolve() not in target.parents and target != out.resolve():
        return f"{ref} escapes the site root"
    rel = target.relative_to(out.resolve()).as_posix()
    if not target.exists():
        if rel in missing_pdfs:
            return None          # warned about by build_site.py; the page shows a "not in this build" state
        return f"{ref} -> {rel} does not exist"
    if parts.fragment and target.suffix == ".html":
        ids = PARSED[target.name].ids if target.name in PARSED else set()
        if parts.fragment not in ids:
            return f"{ref}: no element with id={parts.fragment!r}"
    return None


@pytest.mark.parametrize("page", [p.name for p in PAGES])
def test_relative_links_resolve(built, page):
    out, warnings = built
    missing_pdfs = {w.split(" ")[0] for w in warnings}
    errors = [e for e in (_resolve(out, page, r, missing_pdfs) for r in PARSED[page].refs) if e]
    assert not errors, f"{page}: {errors}"


def test_css_urls_resolve(built):
    out, _ = built
    css = (SITE / "style.css").read_text()
    for url in re.findall(r"url\(\"?([^\")]+)\"?\)", css):
        if url.startswith("data:"):
            continue
        assert (out / url).exists(), f"style.css url({url}) missing from the build"


@pytest.mark.parametrize("page", [p.name for p in PAGES])
def test_page_structure(page):
    p = PARSED[page]
    assert p.h1 == 1, f"{page}: {p.h1} <h1> elements"
    assert p.main_ids == ["main"], f"{page}: expected one <main id='main'>"
    assert p.skip, f"{page}: no skip link to #main"


@pytest.mark.parametrize("page", [p.name for p in PAGES])
def test_no_hand_typed_results(page):
    """A result string that has a display key must come from data-r, not be typed into the page."""
    text = " ".join(PARSED[page].text)
    distinctive = [v for v in DISPLAY.values()
                   if re.search(r"\d", v) and re.search(r"[%$µ]|km|ms|hours|million|points", v) and len(v) >= 4]
    found = sorted({v for v in distinctive if re.search(r"(?<![\w.])" + re.escape(v) + r"(?![\w])", text)})
    assert not found, f"{page}: result strings typed into the HTML (use data-r): {found}"


# ---- model.js --------------------------------------------------------------------------------
ORIGINAL_API = ["fibre_eta", "all_rounds_win", "eta_threshold", "max_separation_km", "heralded_win",
                "edge_per_round", "biased_classical", "biased_quantum", "frontier_region",
                "SPEED_OF_LIGHT_KM_S", "FIBRE_LOSS_DB_PER_KM", "EBERHARD_FLOOR", "IDEAL_QUANTUM_WIN",
                "CLASSICAL_MAX", "REGION_GREY", "REGION_RED", "REGION_YELLOW", "REGION_GREEN"]
NEW_API = ["route_latency_s", "causal_status", "heralded_supply_fraction", "FIBRE_GROUP_INDEX",
           "FIBRE_SPEED_KM_S", "CAUSAL_EXCLUDED", "CAUSAL_ROUTE_DEPENDENT", "CAUSAL_ARRIVES"]

needs_node = pytest.mark.skipif(NODE is None, reason="node not on PATH")


def run_js(calls):
    proc = subprocess.run([NODE, str(SITE / "parity_dump.js")], input=json.dumps([[f, list(a)] for f, a in calls]),
                          capture_output=True, text=True, check=True, timeout=60)
    return json.loads(proc.stdout)


def js_exports():
    script = ("const C=require(process.argv[1]);const o={};for(const k of Object.keys(C))"
              "o[k]=typeof C[k]==='function'?'function':C[k];process.stdout.write(JSON.stringify(o))")
    proc = subprocess.run([NODE, "-e", script, str(SITE / "model.js")], capture_output=True, text=True,
                          check=True, timeout=60)
    return json.loads(proc.stdout)


@needs_node
def test_model_js_exports():
    ex = js_exports()
    missing = [k for k in ORIGINAL_API + NEW_API if k not in ex]
    assert not missing, f"model.js no longer exports {missing}"
    for k in ["fibre_eta", "all_rounds_win", "frontier_region", "causal_status", "route_latency_s",
              "heralded_supply_fraction"]:
        assert ex[k] == "function"
    assert (ex["CAUSAL_EXCLUDED"], ex["CAUSAL_ROUTE_DEPENDENT"], ex["CAUSAL_ARRIVES"]) == (0, 1, 2)
    assert ex["FIBRE_GROUP_INDEX"] == 1.47
    assert ex["FIBRE_SPEED_KM_S"] == ex["SPEED_OF_LIGHT_KM_S"] / 1.47


C = 299792.458
INDEX = 1.47
HIBERNIA_ONE_WAY = 58.95e-3 / 2


def spec_status(d, w, route=None):
    """The causal-state spec, written independently of both implementations."""
    light = d / C
    route_t = INDEX * d / C if route is None else max(route, light)
    if w < light:
        return 0
    if w >= route_t:
        return 2
    return 1


# (d_km, window_s, route_latency) including the exact boundaries window = d/c and window = 1.47 d/c
CAUSAL_CASES = []
for d in [0.5, 5.7, 40.0, 56.0, 100.0, 5570.0]:
    light, fibre = d / C, INDEX * d / C
    CAUSAL_CASES += [(d, math.nextafter(light, 0), None), (d, light, None), (d, 1.2 * light, None),
                     (d, math.nextafter(fibre, 0), None), (d, fibre, None), (d, 1.5 * light, None)]
CAUSAL_CASES += [(5570.0, 0.015, HIBERNIA_ONE_WAY), (5570.0, 5570.0 / C, HIBERNIA_ONE_WAY),
                 (5570.0, 0.020, HIBERNIA_ONE_WAY), (5570.0, math.nextafter(HIBERNIA_ONE_WAY, 0), HIBERNIA_ONE_WAY),
                 (5570.0, HIBERNIA_ONE_WAY, HIBERNIA_ONE_WAY), (5570.0, 0.035, HIBERNIA_ONE_WAY),
                 (100.0, 100.0 / C, 0.0), (100.0, math.nextafter(100.0 / C, 0), 0.0)]


@needs_node
def test_causal_spec_in_model_js():
    js = run_js([("causal_status", (d, w, r)) for d, w, r in CAUSAL_CASES])
    expected = [spec_status(d, w, r) for d, w, r in CAUSAL_CASES]
    bad = [(c, e, g) for c, e, g in zip(CAUSAL_CASES, expected, js) if e != g]
    assert not bad, f"{len(bad)} causal-status mismatches vs spec, first: {bad[:4]}"
    assert set(js) == {0, 1, 2}
    # a quoted route latency is never faster than light; New York-London at 20 ms is route-dependent
    lat, rd, grey20, grey35 = run_js([("route_latency_s", (100.0, 0.0)), ("causal_status", (5570.0, 0.020, HIBERNIA_ONE_WAY)),
                                      ("frontier_region", (5570.0, 0.020, 0.82, 1.0, HIBERNIA_ONE_WAY)),
                                      ("frontier_region", (5570.0, 0.035, 0.82, 1.0, HIBERNIA_ONE_WAY))])
    assert lat == 100.0 / C
    assert rd == 1 and grey20 != 0 and grey35 == 0


@needs_node
def test_heralded_supply_in_model_js():
    full, nyl, ratio = run_js([("heralded_supply_fraction", (40.0, VALUES["e2b"]["demand_rounds_per_s"])),
                               ("heralded_supply_fraction", (5570.0, VALUES["e2b"]["demand_rounds_per_s"])),
                               ("heralded_supply_fraction", (40.0, 1000.0))])
    assert full == 1.0
    assert nyl < 1e-100
    assert ratio == pytest.approx(chsh.fibre_eta(40.0) ** 2, rel=1e-12)
    for row in VALUES["e2b"]["supply"]:
        (got,) = run_js([("heralded_supply_fraction", (row["km"], VALUES["e2b"]["demand_rounds_per_s"]))])
        assert got == pytest.approx(row["h_max"], rel=1e-12)


python_on_spec = pytest.mark.skipif(
    getattr(chsh, "FIBRE_GROUP_INDEX", None) != INDEX,
    reason="src/chsh.py does not implement the 1.47 causal spec yet; re-run after the model change is merged")


@needs_node
@python_on_spec
def test_causal_parity_with_python():
    calls, py = [], []
    for d, w, r in CAUSAL_CASES:
        calls.append(("causal_status", (d, w, r)))
        py.append(int(chsh.causal_status(d, w, r)))
        calls.append(("route_latency_s", (d, r)))
        py.append(float(chsh.route_latency_s(d, r)))
        for p, det in [(0.82, 1.0), (chsh.IDEAL_QUANTUM_WIN, 0.9)]:
            calls.append(("frontier_region", (d, w, p, det, r)))
            py.append(int(chsh.frontier_region(d, w, p_demo=p, detector_eff=det, route_latency=r)))
    for d in [1.0, 40.0, 56.0, 100.0, 5570.0]:
        for dem, rate, det, mem in [(0.61, None, None, None), (VALUES["e2b"]["demand_rounds_per_s"], 500.0, 0.9, 0.5),
                                    (1000.0, None, 0.8, None)]:
            calls.append(("heralded_supply_fraction", (d, dem, rate, det, mem)))
            kw = {k: v for k, v in (("pair_rate", rate), ("detector_eff", det), ("memory_eff", mem)) if v is not None}
            py.append(chsh.heralded_supply_fraction(d, dem, **kw))
    js = run_js(calls)
    bad = [(c, p, g) for c, p, g in zip(calls, py, js)
           if not (p == g or (isinstance(p, float) and math.isclose(p, g, rel_tol=1e-12, abs_tol=0.0)))]
    assert not bad, f"{len(bad)} JS/Python mismatches, first: {bad[:4]}"
    assert chsh.CAUSAL_EXCLUDED == 0 and chsh.CAUSAL_ROUTE_DEPENDENT == 1 and chsh.CAUSAL_ARRIVES == 2
