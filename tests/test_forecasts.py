"""Test Forecasts GFS methods."""
import unittest

from windrouter import forecasts


class TestForecastsMethods(unittest.TestCase):
    """Unit tests."""

    def test_get_latest_gfs(self):
        """Unit tests."""
        date, hour = forecasts.get_latest_gfs_timestamp()
        self.assertEqual(len(date), 8)
        self.assertEqual(len(hour), 2)
