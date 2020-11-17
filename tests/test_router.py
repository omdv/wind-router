"""Test routing methods."""
import unittest

import numpy as np

from windrouter import polars, weather, router


class TestRouterMethods(unittest.TestCase):
    """Unittest class."""

    def test_boat_direct(self):
        """Testing boat direct method."""
        lats = [0, 0, -40, 0]
        lons = [0, 0, 0, 0]
        hdgs = [33, 123, 353, 0]
        boat = polars.boat_properties('data/polar-ITA70.csv')
        gfs = weather.grib_to_wind_function('data/2019122212/2019122212f000')
        hours = 1
        segments = 1
        result = router.move_boat_direct(
            lats, lons, hdgs,
            boat, gfs,
            hours, segments,
            False
        )
        self.assertTrue(np.allclose(
            result['s12'],
            [19444.93, 22.315, 30032.68, 17574.56]))
