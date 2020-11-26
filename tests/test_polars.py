"""Test polar methods."""
import unittest

import numpy as np

from windrouter.polars import boat_properties, boat_speed_function
from windrouter.utils import knots_to_mps


class TestPolarMethods(unittest.TestCase):
    """Test Boat."""

    def test_vo70(self):
        """Test volvo70 polars."""
        boat_file = 'data/polar-VO70.csv'
        boat = boat_properties(boat_file)

        tws = knots_to_mps(np.array([0, 6, 10, 12, 9]))
        twa = np.array([0, 52, 75, 240, 110])
        wind = {'tws': tws, 'twa': twa}

        res = knots_to_mps(np.array([0, 8.18, 12.43, 13.82, 12.025]))
        self.assertTrue(np.allclose(boat_speed_function(boat, wind), res))

    def test_ita70(self):
        """Test ita volvo 70 polars."""
        boat_file = 'data/polar-ITA70.csv'
        boat = boat_properties(boat_file)

        tws = knots_to_mps(np.array([0, 6, 12, 9, 20, 16, 7.9, 7.9]))
        twa = np.array([0, 52, 240, 110, 150, 180, 181, 185])
        wind = {'tws': tws, 'twa': twa}

        calculated = boat_speed_function(boat, wind)
        expected = np.array([
            0,
            4.44994444,
            8.39573333,
            6.91927778,
            9.39375556,
            6.37396667,
            3.65040346,
            3.72513509])
        self.assertTrue(np.allclose(calculated, expected))
