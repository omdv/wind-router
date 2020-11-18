"""Test routing methods."""
import datetime as dt
import numpy as np
import unittest

from windrouter import polars, weather, router


class TestRouterMethods(unittest.TestCase):
    """Unittest class."""

    def test_boat_direct(self):
        """Testing boat direct method."""
        lats = [0, 0, -40, 0]
        lons = [0, 0, 0, 0]
        hdgs = [33, 123, 353, 188]

        boat = polars.boat_properties('data/polar-ITA70.csv')

        model = '2020111600'
        winds = weather.read_wind_functions(model, 24)
        start_time = dt.datetime.strptime('2020111607', '%Y%m%d%H')

        result = router.move_boat_direct(
            (lats, lons),
            hdgs,
            boat, winds,
            start_time, 3600,
            False
        )
        self.assertTrue(np.allclose(
            result['s12'],
            [16111.32450562, 21790.40986404, 25748.94679565, 115.94699562]))

    def test_isochrone(self):
        """Test isochrone."""
        p1 = ([10, 20, 30, 40], [40, 30, 20, 10])
        p2 = ([40, 30, 20, 10], [10, 20, 30, 40])
        params = {
            'ROUTER_HDGS_INCREMENTS_DEG': 0.5,
            'ROUTER_HDGS_SEGMENTS': 10,
            'ROUTER_DELTA_TIME_HRS': 1}

        boat = polars.boat_properties('data/polar-ITA70.csv')

        model = '2020111600'
        winds = weather.read_wind_functions(model, 24)
        start_time = dt.datetime.strptime('2020111607', '%Y%m%d%H')

        router.calc_isochrone(
            p1, p2,
            boat, winds, start_time, 3600, params, verbose=False)
