import unittest
import warnings

import numpy as np

from windrouter import grib


class TestGribMethods(unittest.TestCase):

    def test_grib_function(self):
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", category=RuntimeWarning)
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
                grib.mps_to_knots(f_tws(inputs)),
                outputs)
        )

    def test_gfs_download(self):
        date = "20201107"
        hour = "06"
        resolution = "1p00"
        forecast = "003"

        self.assertEqual(grib.download_gfs_forecast(
            date, hour, forecast, resolution),
            "https://www.ftp.ncep.noaa.gov/data/nccf/com/gfs/prod/" +
            "gfs.20201105/06/gfs.t06z.pgrb2b.1p00.f003")

    # def test_grib_vectors(self):
    #     u, v, lats, lons = utils.grib_to_wind_vectors(
    #         'data/2019122212/2019122212f000',
    #         20, 45, 0, 40)
    #     np.testing.assert_allclose(lats[0:10], [])


if __name__ == '__main__':
    unittest.main()
