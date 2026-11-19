import unittest
from monopoly.lightcone import (great_circle_km,vacuum_min_ms,ideal_fibre_ms,
                                historical_one_way_equivalent_ms,classical_status)

class TestLightcone(unittest.TestCase):
    def test_speeds_of_light(self):
        d=great_circle_km()
        self.assertTrue(5500<d<5650)
        self.assertTrue(18<vacuum_min_ms(d)<19)
        self.assertTrue(27<ideal_fibre_ms(d)<28)
        self.assertAlmostEqual(historical_one_way_equivalent_ms(),29.475)
    def test_critical_intermediate_regime(self):
        self.assertEqual(classical_status(5600,1),"classical_physically_excluded")
        self.assertEqual(classical_status(5600,25),"route_dependent")
        self.assertEqual(classical_status(5600,40),"one_bit_available")
        with self.assertRaises(ValueError):
            vacuum_min_ms(-2)
