"""Check that every number in the written deliverables is traceable to results.json.

A number passes if it appears inside some display string in results.json, or in the
small allowlist below (citation details such as years, volume and page numbers, and
list markers). Sources sections are skipped. Exit code 1 lists anything untraceable.
Usage: python scripts/check_numbers.py [files...]   (default: deliverables/*.md)
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NUM = re.compile(r"(?<![\w.])[−-]?\d[\d,]*(?:\.\d+)?")

# Citation details and other non-result numerals (each with a reason).
ALLOW = {
    "2407.21723": "arXiv id", "11676104": "patent number (11676104B2)",
    "1986": "Mermin year", "1993": "Eberhard year", "2015": "Hibernia year",
    "2017": "Yin year", "2022": "Aquilina / Neumann year", "2024": "Craddock year",
    "2025": "Liu year", "137": "QJE volume", "47": "PRA volume", "640": "Nature volume",
    "343": "Nature page", "356": "Science volume", "1140": "Science page",
    "03": "challenge number", "16": "number of classical rules (E1)",
    "10": "Theorem 10 / 5-10 µs", "4995": "course code", "0": "answer bit 0",
}

display = json.loads((ROOT / "results" / "results.json").read_text())["display"]
known = set()
for v in display.values():
    for tok in NUM.findall(v):
        known.add(tok.replace("−", "-").lstrip("-"))
# fractions such as "5–10" also contribute their parts
known |= {t for v in display.values() for t in re.findall(r"\d+(?:\.\d+)?", v)}


def strip_sources(text):
    return re.split(r"^## Sources", text, flags=re.M)[0]


def check(path):
    bad = []
    text = strip_sources(path.read_text())
    for lineno, line in enumerate(text.splitlines(), 1):
        if line.lstrip().startswith("![") or line.lstrip().startswith("|---"):
            continue
        line = re.sub(r"^\s*\d+\.\s", "", line)        # numbered-list markers
        line = re.sub(r"`[^`]*`", "", line)            # code spans (file names)
        line = re.sub(r"\bE\d\b|\bA\d+\b|E2b", "", line)  # experiment / assumption labels
        line = re.sub(r"\b\d{1,2}:\d{2}\b", "", line)  # script timestamps
        for tok in NUM.findall(line):
            t = tok.replace("−", "-").lstrip("-").rstrip(",")
            if t in known or t in ALLOW or t.rstrip(",") in known:
                continue
            bad.append(f"{path.relative_to(ROOT)}:{lineno}: '{tok}'  in: {line.strip()[:90]}")
    return bad


files = [Path(f).resolve() for f in sys.argv[1:]] or sorted((ROOT / "deliverables").glob("*.md"))
problems = [b for f in files for b in check(f)]
for p in problems:
    print("UNTRACEABLE", p)
print(f"checked {len(files)} files: {len(problems)} untraceable numbers")
sys.exit(1 if problems else 0)
