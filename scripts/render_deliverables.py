"""Fill deliverables/templates/*.md with display strings from results/results.json.

Writing never types a number by hand: each {{key}} is replaced by results["display"][key].
An unknown key is an error, so a typo cannot silently leave a gap.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
display = json.loads((ROOT / "results" / "results.json").read_text())["display"]

missing = []
for tmpl in sorted((ROOT / "deliverables" / "templates").glob("*.md")):
    def sub(m):
        key = m.group(1)
        if key not in display:
            missing.append(f"{tmpl.name}: {key}")
            return m.group(0)
        return display[key]
    out = re.sub(r"\{\{(\w+)\}\}", sub, tmpl.read_text())
    (ROOT / "deliverables" / tmpl.name).write_text(out)
    print("rendered deliverables/" + tmpl.name)

if missing:
    sys.exit("missing display keys: " + ", ".join(missing))
