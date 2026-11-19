import unittest
from monopoly.config import Case
from monopoly.economics import comparison,payoff_surgery,independent_bit_probabilities
class TestEconomics(unittest.TestCase):
    def test_rational_optimal_baseline(self):
        m=comparison(Case())
        self.assertAlmostEqual(m["quantum_net_usd"],63.92)
        self.assertAlmostEqual(m["optimal_classical_net_usd"],49.999)
        self.assertAlmostEqual(m["startup_classical_net_usd"],47.999)
        self.assertAlmostEqual(m["incremental_usd_per_round"],13.921)
        self.assertEqual(m["rounds_for_claimed_opportunity"],3591696)
        self.assertAlmostEqual(m["equity_post_money_fraction"],3/28)
    def test_biased_referee_changes_economics(self):
        self.assertAlmostEqual(sum(independent_bit_probabilities(.2,.7)),1)
        self.assertGreater(payoff_surgery(.5,.5)["incremental_usd_per_round"],0)
        self.assertLess(payoff_surgery(.1,.1)["incremental_usd_per_round"],0)
        self.assertTrue(payoff_surgery(.3,.3)["is_hypothesis_not_observation"])
