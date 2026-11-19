"""Assemble the static website into one deployable folder (default: _site/).

    _site/                 copy of site/ (pages, scripts, styles, fonts)
    _site/data/results.json  <- results/results.json   (the pages fetch it at load)
    _site/figures/*.png      <- figures/*.png
    _site/reports/*.pdf      <- reports/*.pdf           (missing PDFs are skipped with a warning)
    _site/.nojekyll

No templating and no build step for the pages themselves: this only copies files.
Usage: python scripts/build_site.py [--out DIR]
"""
from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PDFS = ("memo.pdf", "phase1.pdf", "one_page_brief.pdf")
# Files in site/ that are not part of the published page (Node helper for tests).
SKIP = {"parity_dump.js"}


def build(out: Path) -> list[str]:
    """Build the site into ``out``. Returns the list of warnings (missing optional files)."""
    warnings: list[str] = []
    out = out.resolve()
    protected = {ROOT} | {ROOT / d for d in ("site", "src", "results", "figures", "reports", "deliverables", "tests")}
    if out in protected or out in ROOT.parents:
        raise SystemExit(f"refusing to build into {out}")
    if out.exists():
        shutil.rmtree(out)
    shutil.copytree(ROOT / "site", out, ignore=lambda d, names: [n for n in names if n in SKIP])

    results = ROOT / "results" / "results.json"
    if not results.exists():
        raise SystemExit("results/results.json is missing: run the notebook first (scripts/package.sh)")
    (out / "data").mkdir()
    shutil.copy2(results, out / "data" / "results.json")

    (out / "figures").mkdir()
    for png in sorted((ROOT / "figures").glob("*.png")):
        shutil.copy2(png, out / "figures" / png.name)

    (out / "reports").mkdir()
    for name in PDFS:
        src = ROOT / "reports" / name
        if src.exists():
            shutil.copy2(src, out / "reports" / name)
        else:
            warnings.append(f"reports/{name} not found; skipped (run scripts/package.sh to build the PDFs)")

    (out / ".nojekyll").write_text("")
    return warnings


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--out", default=str(ROOT / "_site"), help="output directory (default: _site)")
    args = ap.parse_args(argv)
    out = Path(args.out)
    for w in build(out):
        print("warning: " + w, file=sys.stderr)
    n = sum(1 for p in out.resolve().rglob("*") if p.is_file())
    print(f"built {out} ({n} files)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
