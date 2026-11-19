"""Executable CLI for all reproducible experiments."""
import argparse
import json
from .chsh import optimal_local_win_rate,quantum_tsirelson_win_rate
from .config import DEFAULT_CASE_PATH
from .forensics import simulate,required_filter_fraction
from .report import build


def main(argv=None):
    parser=argparse.ArgumentParser(description="The 28-Millisecond Monopoly")
    sub=parser.add_subparsers(dest="command",required=True)
    run=sub.add_parser("build",help="Generate research artifacts and memo")
    run.add_argument("--out",default="artifacts")
    run.add_argument("--case",default=str(DEFAULT_CASE_PATH))
    audit=sub.add_parser("audit",help="Simulate the classical detection loophole")
    audit.add_argument("--rounds",type=int,default=100000)
    audit.add_argument("--seed",type=int,default=20261119)
    sub.add_parser("limits",help="Print exact CHSH limits")
    args=parser.parse_args(argv)
    if args.command=="build":
        m=build(args.out,args.case)
        print(json.dumps({"directory":args.out,"decision":m["decision"],
                          "incremental_toy_usd_per_round":m["economics"]["incremental_usd_per_round"]},indent=2))
    elif args.command=="audit":
        print(json.dumps(simulate(args.rounds,required_filter_fraction(.82),args.seed).to_dict(),indent=2))
    else:
        print(json.dumps({"classical_no_communication":optimal_local_win_rate(),
                          "ideal_quantum":quantum_tsirelson_win_rate(),
                          "classical_after_one_bit_delivery":1.0},indent=2))
    return 0
