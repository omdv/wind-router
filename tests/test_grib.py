import unittest
import numpy as np
from windrouter import utils, grib


class TestUtilsMethods(unittest.TestCase):

    def test_grib_function(self):
        f_twa, f_tws = grib.grib_to_wind_function(
            'data/2019122212/2019122212f000')
        inputs = [
            [0, 0],
            [-40, 0],
            [16.5, 170],
            [-35.2211, 308.53805556],
            [-90, 360]]
        outputs = [4.61151, 26.38263, 21.605419, 32.230938, 11.184625]
        self.assertTrue(
            np.allclose(
                utils.mps_to_knots(f_tws(inputs)),
                outputs)
        )

    # def test_grib_vectors(self):
    #     u, v, lats, lons = utils.grib_to_wind_vectors(
    #         'data/2019122212/2019122212f000',
    #         20, 45, 0, 40)
    #     np.testing.assert_allclose(lats[0:10], [])


if __name__ == '__main__':
    unittest.main()
