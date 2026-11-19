import json
import tempfile
import unittest
from pathlib import Path
from monopoly.frontier import grid,classify
from monopoly.report import build

class TestReport(unittest.TestCase):
    def test_frontier_has_unverified_market_label(self):
        rows=grid()
        self.assertGreater(len(rows),100)
        self.assertTrue(all(r["commercial_viability_verified"] is False for r in rows))
        self.assertEqual(classify(5600,10)["region"],"no_direct_fibre_supply")
        self.assertEqual(classify(5600,40)["region"],"classical_one_bit_suffices")

    def test_exact_reproducible_bundle(self):
        with tempfile.TemporaryDirectory() as temp:
            a,b=Path(temp)/"a",Path(temp)/"b"
            self.assertEqual(build(a),build(b))
            for relative in ("metrics.json","figures/frontier.svg","figures/optical_loss.svg",
                             "figures/payoff_surgery.svg","tables/frontier.csv",
                             "tables/payoff_surgery.csv","EXECUTIVE_MEMO.md","RUN_MANIFEST.md"):
                self.assertTrue((a/relative).is_file(),relative)
                self.assertEqual((a/relative).read_bytes(),(b/relative).read_bytes())
            m=json.loads((a/"metrics.json").read_text())
            self.assertTrue(m["case_is_fictional"])
            self.assertIn("Reopening conditions",(a/"EXECUTIVE_MEMO.md").read_text())
