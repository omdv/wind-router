import unittest

import numpy as np

from windrouter import utils


class TestUtilsMethods(unittest.TestCase):

    def test_conversions(self):
        mps = np.array([0, 10, 20, 30])
        knots = np.array([0, 19.43844492, 38.87688985, 58.31533477])

        self.assertTrue(np.allclose(utils.mps_to_knots(mps), knots))
        self.assertTrue(np.allclose(utils.knots_to_mps(knots), mps))

if __name__ == '__main__':
    unittest.main()
