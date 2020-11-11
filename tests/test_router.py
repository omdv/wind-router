import unittest

import numpy as np

from windrouter import boat, grib, router


class TestRouterMethods(unittest.TestCase):

    def test_gcr_function(self):
        # Default map coordinates - lat1, lat2, lon1, lon2
        lat1 = 43.2
        lat2 = 36
        lon1 = 6
        lon2 = 36
        path = router.get_gcr(lat1, lon1, lat2, lon2, n_points=5)
        result = [
            (43.2, 6),
            (42.41553092975164, 12.470738322155897),
            (41.27599859111937, 18.747045333026055),
            (39.80683285126772, 24.778772550035434),
            (38.037647067258405, 30.534417303276303),
            (36.00000000000163, 35.99999999999577)
        ]
        np.testing.assert_allclose(path, result)

    def test_boat_direct(self):
        lats = [10, 20, 30]
        lons = [10, 20, 30]
        hdgs = [80, 90, 100]
        b = boat.get_boat_profile('data/polar-ITA70.csv')
        f_boat_speed = boat.get_boat_speed
        f_twa, f_tws = grib.grib_to_wind_function(
            'data/2019122212/2019122212f000')
        hours = 10
        segments = 2
        result = router.move_boat_direct(
            lats, lons, hdgs,
            b, f_boat_speed,
            f_twa, f_tws,
            hours, segments
        )
        self.assertTrue(np.allclose(
            result['s12'],
            [134284.01766855, 167862.22646772, 123965.49657972]))

if __name__ == '__main__':
    unittest.main()
