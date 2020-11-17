"""Unit tests."""
import datetime
import unittest

import numpy as np

from windrouter import utils


class TestUtilsMethods(unittest.TestCase):
    """Unit tests."""

    def test_conversions(self):
        """Test function."""
        mps = np.array([0, 10, 20, 30])
        knots = np.array([0, 19.43844492, 38.87688985, 58.31533477])

        self.assertTrue(np.allclose(utils.mps_to_knots(mps), knots))
        self.assertTrue(np.allclose(utils.knots_to_mps(knots), mps))

    def test_time_rounder(self):
        """Test function."""
        time = datetime.datetime(2012, 12, 31, 20, 44, 59, 1234)
        rounded = datetime.datetime(2012, 12, 31, 21, 0, 0, 0)
        new = utils.round_time(time, round_to=3600 * 3)
        self.assertEqual(new, rounded)
