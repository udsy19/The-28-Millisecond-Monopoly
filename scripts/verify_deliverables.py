#!/usr/bin/env python3
"""Verify that generated evidence is complete and properly qualified."""
from pathlib import Path
import argparse
import json
parser=argparse.ArgumentParser()
parser.add_argument("--dir",default="artifacts")
root=Path(parser.parse_args().dir)
files=("metrics.json","EXECUTIVE_MEMO.md","RUN_MANIFEST.md",
       "tables/frontier.csv","tables/payoff_surgery.csv",
       "figures/frontier.svg","figures/optical_loss.svg","figures/payoff_surgery.svg")
missing=[name for name in files if not (root/name).is_file() or not (root/name).stat().st_size]
if missing:
    raise SystemExit("Missing/empty deliverables: "+", ".join(missing))
m=json.loads((root/"metrics.json").read_text())
required=(m["case_is_fictional"],
          m["economics"]["not_real_trading_profit"],
          m["optics"]["source_or_received_case_pair_rate_ambiguous"],
          m["forensics"]["loophole_counterexample_is_not_an_accusation"],
          m["chsh"]["p_value_is_invalid_if_only_coincidences_scored"],
          m["decision"].startswith("Do not fund"))
if not all(required):
    raise SystemExit("Scientific evidence/caveat gates failed")
print("All research outputs present and caveats preserved.")
