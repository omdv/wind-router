import unittest
import numpy as np
from windrouter import router


class TestRouterMethods(unittest.TestCase):

    def test_gcr(self):
        # Default map coordinates - lat1, lat2, lon1, lon2
        lat1 = 43.2
        lat2 = 36
        lon1 = 6
        lon2 = 36
        path = router.get_gcr(lat1, lon1, lat2, lon2, n_points=5)
        result = [
            (34.3994404295813, 14.474857686655664),
            (36.79038628215888, 19.085104996424015),
            (39.172363837822566, 23.847188412824462),
            (41.544835910940314, 28.779609583049545),
            (43.90718903133833, 33.90333347332089)]
        np.testing.assert_allclose(path, result)


if __name__ == '__main__':
    unittest.main()
