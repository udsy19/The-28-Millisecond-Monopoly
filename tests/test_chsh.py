import unittest
from monopoly.chsh import (local_strategies, optimal_local_win_rate,
                           optimal_one_bit_strategy, one_sided_binomial_tail,
                           quantum_tsirelson_win_rate, wins)

class TestCHSH(unittest.TestCase):
    def test_complete_local_enumeration(self):
        strategies=local_strategies()
        self.assertEqual(len(strategies),16)
        self.assertEqual(max(s["win_rate"] for s in strategies),.75)
        self.assertEqual(optimal_local_win_rate(),.75)

    def test_quantum_ideal_not_confused_with_observed(self):
        self.assertAlmostEqual(quantum_tsirelson_win_rate(),.8535533905932737,places=12)

    def test_exact_one_bit_counterstrategy(self):
        for x in (0,1):
            for y in (0,1):
                a,b=optimal_one_bit_strategy(x,y)
                self.assertTrue(wins(x,y,a,b))

    def test_trial_denominator_sensitive_significance(self):
        self.assertAlmostEqual(one_sided_binomial_tail(1000,820),
                               7.496183309079151e-8,delta=1e-14)

    def test_biased_input_exact_classical(self):
        self.assertAlmostEqual(optimal_local_win_rate((.45,.45,.05,.05)),.95)
        with self.assertRaises(ValueError):
            optimal_local_win_rate((.2,.2,.2,.2))
