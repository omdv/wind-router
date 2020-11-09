import unittest

import numpy as np

from windrouter import boat


class TestBoatMethods(unittest.TestCase):

    def test_boat_function(self):
        b = boat.get_boat_data('VO70')
        tws = np.array([0, 6, 10, 12, 9])
        twa = np.array([0, 52, 75, 240, 110])
        res = np.array([0, 8.18, 12.43, 13.82, 12.025])
        self.assertTrue(np.allclose(boat.get_boat_speed(b, tws, twa), res))


if __name__ == '__main__':
    unittest.main()
