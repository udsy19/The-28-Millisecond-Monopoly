import unittest
from monopoly.photonics import (attenuation_db, transmission_probability,
                                upper_bound_received_pair_rate,source_rate_from_observed_at_distance,
                                arrival_probability_in_window)
class TestPhotonics(unittest.TestCase):
    def test_fibre_loss_order_of_magnitude(self):
        self.assertEqual(attenuation_db(5600),1120)
        self.assertAlmostEqual(transmission_probability(5600),1e-112,delta=1e-125)
        self.assertAlmostEqual(transmission_probability(40),10**(-.8),places=12)
    def test_two_interpretations_of_1000_per_second(self):
        self.assertAlmostEqual(upper_bound_received_pair_rate(1000,40),158.48931924611142)
        self.assertAlmostEqual(source_rate_from_observed_at_distance(1000,40),6309.573444801934)
    def test_poisson_event(self):
        self.assertAlmostEqual(arrival_probability_in_window(1,1),.6321205588285577)
