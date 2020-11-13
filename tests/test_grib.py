import unittest
import warnings

import numpy as np

from windrouter.grib import grib_to_wind_function
from windrouter.utils import mps_to_knots


class TestGribMethods(unittest.TestCase):

    def test_grib_function(self):
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", category=RuntimeWarning)
            gfs = grib_to_wind_function('data/2019122212/2019122212f000')
            twa = gfs['twa']
            tws = gfs['tws']
        inputs = [
            [0, 0],
            [-40, 0],
            [16.5, 170],
            [-35.2211, 308.53805556],
            [-90, 360]]
        outputs = [4.61151, 26.38263, 21.605419, 32.230938, 11.184625]
        self.assertTrue(np.allclose(mps_to_knots(tws(inputs)), outputs))


if __name__ == '__main__':
    unittest.main()
