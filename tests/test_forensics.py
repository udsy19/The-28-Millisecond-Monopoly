import unittest
from monopoly.forensics import (required_filter_fraction,conditional_win_rate,
                                retained_fraction,simulate)
class TestForensics(unittest.TestCase):
    def test_exact_classical_82_percent_counterexample(self):
        q=required_filter_fraction(.82)
        self.assertAlmostEqual(q,.4375)
        self.assertAlmostEqual(conditional_win_rate(q),.82)
        self.assertAlmostEqual(retained_fraction(q),.78125)
    def test_monte_carlo_and_unconditional_bound(self):
        result=simulate(100000,.4375,20261119)
        self.assertLess(abs(result.observed_win_rate-.82),.012)
        self.assertLess(abs(result.unconditional_win_rate-.75),.008)
        self.assertLess(abs(result.retention_rate-.78125),.008)
    def test_no_filter(self):
        result=simulate(100000,0,20261119)
        self.assertEqual(result.observed_win_rate,result.unconditional_win_rate)
        with self.assertRaises(ValueError):
            required_filter_fraction(.7)
