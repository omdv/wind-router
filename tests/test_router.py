"""Test routing methods."""
import datetime as dt
import numpy as np
import unittest
from geovectorslib import geod
from windrouter import polars, weather, router, isochrone


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
            lats, lons, hdgs,
            boat, winds,
            start_time, 3600,
            False
        )
        self.assertTrue(np.allclose(
            result['s12'],
            [15731.34902478, 21790.40986404, 25748.94679565, 115.94699562]))

    def test_pruning(self):
        """Test isochrone."""
        azi02 = np.array([
            328.36058953, 327.36058953, 326.36058953, 325.36058953,
            324.36058953, 323.36058953, 322.36058953, 321.36058953,
            320.36058953, 319.36058953, 318.36058953, 324.67390838,
            323.67390838, 322.67390838, 321.67390838, 320.67390838,
            319.67390838, 318.67390838, 317.67390838, 316.67390838,
            315.67390838, 314.67390838, 140.422624, 139.422624,
            138.422624, 137.422624, 136.422624, 135.422624,
            134.422624, 133.422624, 132.422624, 131.422624,
            130.422624, 134.98459562, 133.98459562, 132.98459562,
            131.98459562, 130.98459562, 129.98459562, 128.98459562,
            127.98459562, 126.98459562, 125.98459562, 124.98459562])
        s02 = np.array([
            5786.14040237,  6094.21347929,  6402.28655622,  6710.35963314,
            7018.43271006,  7326.50578698,  7634.57886391,  7942.65194083,
            8250.72501775,  8558.79809468,  8866.8711716, 18170.89052858,
            18612.98001084, 19055.0694931, 19497.15897536, 19939.24845762,
            20381.33793988, 20823.42742214, 21265.5169044, 21707.60638666,
            22149.69586892, 22591.78535118, 13866.17764187, 13866.17764187,
            13866.17764187, 13866.17764187, 13866.17764187, 13866.17764187,
            13866.17764187, 13866.17764187, 13866.17764187, 13866.17764187,
            13866.17764187, 12254.18219236, 12436.91285903, 12619.6435257,
            12802.37419236, 12985.10485903, 13167.8355257, 13350.56619236,
            13533.29685903, 13716.0275257, 13898.75819236, 14081.4888590])
        lats1 = np.array([
            10.04453567, 10.04639519, 10.04818812, 10.04991249,
            10.05156637, 10.05314787, 10.05465513, 10.05608633, 10.057439,
            10.05871356, 10.05990615, 20.13388726, 20.13542488, 20.136838,
            20.13812567, 20.13928413, 20.1403116, 20.14120591, 20.14196492,
            20.1425866, 20.14306897, 20.14341011, 29.903555, 29.90495923,
            29.9063924, 29.90785406, 29.90934377, 29.91086109, 29.91240555,
            29.91397667, 29.91557399, 29.91719702, 29.91884526, 39.921937,
            39.92216564, 39.92245896, 39.92281779, 39.92324271, 39.923734,
            39.92429289, 39.92491912, 39.92561337, 39.9263760, 39.927208])
        lats1 = np.array([lats1, lats1])
        lons1 = np.array([
            9.97231232,  9.97001641,  9.967647,  9.96520577, 9.96269441,
            9.96011468,  9.95746836,  9.95475732,  9.95198341,  9.94914859,
            9.9462548, 19.89951129, 19.89454634, 19.8894946, 19.88435916,
            19.87914318, 19.87384988, 19.86848252, 19.86304445, 19.8575391,
            19.85196976, 19.84634009, 30.091473, 30.09339168, 30.09528199,
            30.09714336, 30.09897522, 30.10077701, 30.10254819, 30.1042882,
            30.10599654, 30.10767267, 30.10931609, 40.10138309, 40.1046744,
            40.10798569, 40.11131511, 40.11466069, 40.11802042, 40.1213923,
            40.12477435, 40.12816448, 40.13156066, 40.13496081])
        lons1 = np.array([lons1, lons1])

        iso = isochrone.Isochrone(
            count=None,
            start=None,
            finish=None,
            gcr_azi=None,
            lats1=lats1,
            lons1=lons1,
            azi12=lats1,
            s12=lons1,
            azi02=azi02,
            s02=s02,
            time1=None,
            elapsed=None
        )

        lats1_exp = np.array([39.92720749, 20.14341011, 29.903555, 20.139284])
        lats1_exp = np.array([lats1_exp, lats1_exp])

        lons1_exp = np.array([40.13496081, 19.84634009, 30.091473, 19.879143])
        lons1_exp = np.array([lons1_exp, lons1_exp])

        azi02_exp = np.array([124.984596, 314.67391, 140.422624, 320.6739084])
        s02_exp = np.array([14081.4889, 22591.7854, 13866.1776, 19939.24846])

        bins = [120, 135, 140, 250, 300, 320, 340]
        calc = router.prune_isochrone(iso, 'azi02', 's02', bins, True)

        self.assertTrue(np.allclose(calc.lats1, lats1_exp))
        self.assertTrue(np.allclose(calc.lons1, lons1_exp))
        self.assertTrue(np.allclose(calc.azi02, azi02_exp))
        self.assertTrue(np.allclose(calc.s02, s02_exp))
        return None

    def test_recursive_isochrone_method(self):
        """Test isochrone."""
        start = (43.5, 7.2)
        finish = (33.8, 35.5)
        start_time = dt.datetime.strptime('2020111607', '%Y%m%d%H')

        gcr = geod.inverse([start[0]], [start[1]], [finish[0]], [finish[1]])

        iso = isochrone.Isochrone(
            count=0,
            start=start,
            finish=finish,
            gcr_azi=gcr['azi1'],
            lats1=np.array([[start[0]]]),
            lons1=np.array([[start[1]]]),
            azi12=np.array([[None]]),
            s12=np.array([[0]]),
            azi02=gcr['azi1'],
            s02=np.array([0]),
            time1=start_time,
            elapsed=dt.timedelta(seconds=0)
        )

        boat = polars.boat_properties('data/polar-ITA70.csv')
        model = '2020111600'
        winds = weather.read_wind_functions(model, 24)
        params = {
            'ROUTER_HDGS_SEGMENTS': 30,
            'ROUTER_HDGS_INCREMENTS_DEG': 1,
            'ISOCHRONE_EXPECTED_SPEED_KTS': 8,
            'ISOCHRONE_RESOLUTION_RAD': 1,
            'ISOCHRONE_PRUNE_SECTOR_DEG_HALF': 15,
            'ISOCHRONE_PRUNE_SEGMENTS': 5}

        delta_time_sec = 3600
        result = router.recursive_routing(
            iso, boat, winds,
            delta_time_sec, params,
            verbose=False)
        expected_s12 = np.array([
            [13235.5216, 12843.9842, 13150.357, 13541.8945, 13933.4320],
            [0., 0., 0., 0., 0.]])

        self.assertTrue(np.allclose(result.s12, expected_s12))
        self.assertTrue(
            result.time1,
            start_time+dt.timedelta(seconds=delta_time_sec))
        return None

    def test_recursive_routing(self):
        """Unit test."""

        start = (43.5, 7.2)
        finish = (33.8, 35.5)
        start_time = dt.datetime.strptime('2020111607', '%Y%m%d%H')

        gcr = geod.inverse([start[0]], [start[1]], [finish[0]], [finish[1]])

        iso = isochrone.Isochrone(
            count=0,
            start=start,
            finish=finish,
            gcr_azi=gcr['azi1'],
            lats1=np.array([[start[0]]]),
            lons1=np.array([[start[1]]]),
            azi12=np.array([[None]]),
            s12=np.array([[0]]),
            azi02=gcr['azi1'],
            s02=np.array([]),
            time1=start_time,
            elapsed=dt.timedelta(seconds=0)
        )

        boat = polars.boat_properties('data/polar-ITA70.csv')
        model = '2020111600'
        winds = weather.read_wind_functions(model, 24)
        params = {
            'ROUTER_HDGS_SEGMENTS': 30,
            'ROUTER_HDGS_INCREMENTS_DEG': 1,
            'ISOCHRONE_EXPECTED_SPEED_KTS': 8,
            'ISOCHRONE_RESOLUTION_RAD': 1,
            'ISOCHRONE_PRUNE_SECTOR_DEG_HALF': 15,
            'ISOCHRONE_PRUNE_SEGMENTS': 5}

        delta_time_sec = 3600

        for i in range(2):
            iso = router.recursive_routing(
                iso, boat, winds,
                delta_time_sec, params,
                verbose=False)

        expected_azi02 = np.array([
            100.45741406,
            113.20471345,
            95.06500765,
            117.72590944,
            106.25658986])
        expected_s02 = np.array([
            39090.76869898,
            42504.71278082,
            36630.65067096,
            43113.25351592,
            41573.10032953])
        self.assertTrue(np.allclose(iso.azi02, expected_azi02))
        self.assertTrue(np.allclose(iso.s02, expected_s02))
        return None

    def test_complete_routing(self):
        """Unit test."""

        start = (43.5, 7.2)
        finish = (33.8, 35.5)
        start_time = dt.datetime.strptime('2020111607', '%Y%m%d%H')
        delta_time = 3600
        steps = 10

        boat = polars.boat_properties('data/polar-ITA70.csv')
        model = '2020111600'
        winds = weather.read_wind_functions(model, 24)
        params = {
            'ROUTER_HDGS_SEGMENTS': 30,
            'ROUTER_HDGS_INCREMENTS_DEG': 1,
            'ISOCHRONE_EXPECTED_SPEED_KTS': 8,
            'ISOCHRONE_RESOLUTION_RAD': 1,
            'ISOCHRONE_PRUNE_SECTOR_DEG_HALF': 15,
            'ISOCHRONE_PRUNE_SEGMENTS': 5}

        iso = router.routing(
            start, finish,
            boat, winds,
            start_time, delta_time, steps,
            params
        )
        self.assertEqual(iso.s12.shape[0], 11)

        return None
