import unittest

import numpy as np

from windrouter import graphics


class TestGraphicsMethods(unittest.TestCase):

    def test_gcr_function(self):
        # Default map coordinates - lat1, lat2, lon1, lon2
        lat1 = 43.2
        lat2 = 36
        lon1 = 6
        lon2 = 36
        path = graphics.get_gcr_points(lat1, lon1, lat2, lon2, n_points=5)
        result = [
            (43.2, 6),
            (42.41553092975164, 12.470738322155897),
            (41.27599859111937, 18.747045333026055),
            (39.80683285126772, 24.778772550035434),
            (38.037647067258405, 30.534417303276303),
            (36.00000000000163, 35.99999999999577)
        ]
        np.testing.assert_allclose(path, result)

if __name__ == '__main__':
    unittest.main()
