import numpy as np
import pygrib as pg
from scipy.interpolate import RegularGridInterpolator


def mps_to_knots(vals):
    """Meters per second to knots."""
    return vals * 3600 / 1852.0


def grib_to_wind_function(filepath):
    """Vectorized wind functions from grib file."""
    grbs = pg.open(filepath)

    u, _, _ = grbs[1].data()
    v, _, _ = grbs[2].data()

    tws = np.sqrt(u * u + v * v)
    twa = 180.0 / np.pi * np.arctan2(u, v) + 180.0

    lats_grid = np.linspace(-90, 90, 181)
    lons_grid = np.linspace(0, 360, 361)

    f_twa = RegularGridInterpolator(
        (lats_grid, lons_grid),
        np.flip(np.hstack((twa, twa[:, 0].reshape(181, 1))), axis=0),
    )

    f_tws = RegularGridInterpolator(
        (lats_grid, lons_grid),
        np.flip(np.hstack((tws, tws[:, 0].reshape(181, 1))), axis=0),
    )

    return f_twa, f_tws


def grib_to_wind_vectors(filepath, lat1, lat2, lon1, lon2):
    """Return u-v components for given rect."""
    grbs = pg.open(filepath)
    u, lats_u, lons_u = grbs[1].data(lat1, lat2, lon1, lon2)
    v, lats_v, lons_v = grbs[2].data(lat1, lat2, lon1, lon2)
    return u, v, lats_u, lons_u
