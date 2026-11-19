import json
import math
import tempfile
import unittest
from pathlib import Path

from monopoly.config import Case
from monopoly.operational import (
    OperatingScenario, annual_ceiling, build_operational_appendix,
    max_direct_distance_for_target, min_emitted_rate_for_target
)


class TestOperational(unittest.TestCase):
    def test_strongest_case_still_fails_over_atlantic_direct_fibre(self):
        scenario = OperatingScenario("atlantic", 5600, 20, 1000)
        result = annual_ceiling(scenario)
        self.assertEqual(result["classical_message_status"], "route_dependent")
        self.assertLess(result["ideal_direct_fibre_annual_pairs"], 1e-95)
        self.assertFalse(result["commercial_viability_verified"])
        self.assertTrue(result["economic_premium_unverified_if_route_dependent"])
        self.assertFalse(result["is_a_market_forecast"])

    def test_fast_classical_message_eliminates_quantum_game_premium(self):
        scenario = OperatingScenario("fast", 40, 100, 1000)
        result = annual_ceiling(scenario)
        self.assertEqual(result["classical_message_status"], "one_bit_available")
        self.assertEqual(result["nonnegative_conditional_value_ceiling_usd"], 0)
        self.assertGreater(result["ideal_direct_fibre_annual_pairs"], 1_000_000)

    def test_units_and_inverse(self):
        target = 50_000_000
        edge = 13.921
        max_d = max_direct_distance_for_target(1000, target, edge)
        self.assertAlmostEqual(max_d, 197.1753518, places=5)
        rate = min_emitted_rate_for_target(max_d, target, edge)
        self.assertAlmostEqual(rate, 1000, places=7)
        atlantic = min_emitted_rate_for_target(5600, target, edge)
        self.assertGreater(atlantic, 1e110)

    def test_capacity_saturates_buyer_and_accounts_for_fallback(self):
        s = OperatingScenario("short", 40, 0.01, 1000, annual_demand_rounds=25,
                              incremental_non_case_cost_per_round_usd=2)
        result = annual_ceiling(s)
        self.assertEqual(result["eligible_round_ceiling"], 25)
        self.assertAlmostEqual(result["incremental_game_value_before_fixed_cost_usd"],
                               25 * (13.921 - 2))
        self.assertEqual(result["classical_message_status"], "classical_physically_excluded")

    def test_fail_closed_inputs(self):
        for bad in (
            {"source_pair_rate_hz": -1},
            {"usable_pair_fraction": 1.2},
            {"route_multiplier": 0.5},
            {"distance_km": float("nan")},
        ):
            payload = dict(name="bad", distance_km=40, deadline_ms=1, source_pair_rate_hz=1000)
            payload.update(bad)
            with self.assertRaises(ValueError):
                OperatingScenario(**payload)
        self.assertIsNone(max_direct_distance_for_target(0.01, 50_000_000, 13.921))
        self.assertIsNone(min_emitted_rate_for_target(100, 50_000_000, 0))
        self.assertTrue(math.isinf(max_direct_distance_for_target(1, 0, 1)))

    def test_appendix_generated_and_reproducible(self):
        with tempfile.TemporaryDirectory() as d:
            summary = build_operational_appendix(d)
            saved = json.loads((Path(d) / "underwriting.json").read_text())
            self.assertEqual(summary, saved)
            self.assertEqual(len(summary["scenarios"]), 5)
            self.assertIn("fictional", (Path(d) / "OPERATIONS_APPENDIX.md").read_text())
            self.assertTrue((Path(d) / "tables" / "operational_scenarios.csv").exists())
