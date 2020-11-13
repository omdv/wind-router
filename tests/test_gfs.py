"""Test GFS methods."""
import unittest

import numpy as np

from windrouter import gfs


class TestGfsMethods(unittest.TestCase):

    def test_get_latest_gfs_date_hour(self):
        date, hour = gfs.get_latest_gfs_date_hour()
        self.assertEqual(len(date), 8)
        self.assertEqual(len(hour), 2)


if __name__ == '__main__':
    unittest.main()
