import unittest

import numpy as np

from windrouter.boat import get_boat_profile, get_boat_speed
from windrouter.utils import knots_to_mps


class TestBoatMethods(unittest.TestCase):

    def test_vo70(self):
        boat_file = 'data/polar-VO70.csv'
        boat = get_boat_profile(boat_file)
        tws = knots_to_mps(np.array([0, 6, 10, 12, 9]))
        twa = np.array([0, 52, 75, 240, 110])
        res = knots_to_mps(np.array([0, 8.18, 12.43, 13.82, 12.025]))
        self.assertTrue(np.allclose(get_boat_speed(boat, tws, twa), res))

    def test_ita70(self):
        boat_file = 'data/polar-ITA70.csv'
        boat = get_boat_profile(boat_file)
        tws = knots_to_mps(np.array([0, 6, 12, 9, 20, 16]))
        twa = np.array([0, 52, 240, 110, 150, 180])
        res = knots_to_mps(np.array([0, 8.65, 16.32, 13.45, 18.26, 14.3]))
        self.assertTrue(np.allclose(get_boat_speed(boat, tws, twa), res))

if __name__ == '__main__':
    unittest.main()
