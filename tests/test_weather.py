"""Testing Grib functions."""
import datetime as dt
import unittest
import warnings

import numpy as np

from windrouter import weather as wrt
from windrouter.utils import mps_to_knots


class TestWeatherMethods(unittest.TestCase):
    """Unit tests."""

    def test_grib_to_wind_function(self):
        """Test function."""
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", category=RuntimeWarning)
            gfs = wrt.grib_to_wind_function('data/2019122212/2019122212f000')
            tws = gfs['tws']
        coords = [
            [0, 0],
            [-40, 0],
            [16.5, 170],
            [-35.2211, 308.53805556],
            [-90, 360]]
        outputs = [4.61151, 26.38263, 21.605419, 32.230938, 11.184625]
        self.assertTrue(np.allclose(mps_to_knots(tws(coords)), outputs))

    def test_read_wind_functions(self):
        """Test function."""
        hours = 3
        wind = wrt.read_wind_functions('2020111600', hours)
        self.assertEqual(len(wind), hours // 3 + 2)

    def test_wind_function(self):
        """Test function."""
        model = '2020111600'
        winds = wrt.read_wind_functions(model, 24)

        time = dt.datetime.strptime('2020111607', '%Y%m%d%H')
        coords = [
            [0, 0],
            [-40, 0],
            [16.5, 170],
            [-35.2211, 308.53805556],
            [-90, 360]]

        winds = wrt.wind_function(winds, coords, time)
        twa = np.array([
            188.29806519,
            266.38195801,
            81.41789627,
            200.73077347,
            5.22937012])
        tws = np.array([
            4.43330574,
            5.18015099,
            7.99129558,
            6.28333179,
            7.24325514])
        self.assertTrue(np.allclose(twa, winds['twa']))
        self.assertTrue(np.allclose(tws, winds['tws']))
