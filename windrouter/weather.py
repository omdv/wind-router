"""Weather functions."""
import numpy as np
import datetime as dt

import pygrib as pg

from scipy.interpolate import RegularGridInterpolator

from .utils import round_time


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

    return {'twa': f_twa, 'tws': f_tws}


def grib_to_wind_vectors(filepath, lat1, lon1, lat2, lon2):
    """Return u-v components for given rect for visualization."""
    grbs = pg.open(filepath)
    u, lats_u, lons_u = grbs[1].data(lat1, lat2, lon1, lon2)
    v, lats_v, lons_v = grbs[2].data(lat1, lat2, lon1, lon2)
    return u, v, lats_u, lons_u


def read_wind_vectors(model, hours_ahead, lat1, lon1, lat2, lon2):
    """Return wind vectors for given number of hours.

            Parameters:
                    model (dict): available forecast wind functions
                    hours_ahead (int): number of hours looking ahead
                    lats, lons: rectange defining forecast area

            Returns:
                    wind_vectors (dict):
                        model: model timestamp
                        hour: function for given forecast hour
    """
    wind_vectors = {}
    wind_vectors['model'] = model

    for i in range(hours_ahead + 1):
        if (i % 3 == 0):
            filename = 'data/{}/{}f{:03d}'.format(model, model, i)
            wind_vectors[i] = grib_to_wind_vectors(
                filename, lat1, lon1, lat2, lon2)

    return wind_vectors


def read_wind_functions(model, hours_ahead):
    """
    Read wind functions.

            Parameters:
                    model (dict): available forecast wind functions

            Returns:
                    wind_functions (dict):
                        model: model timestamp
                        model+hour: function for given forecast hour
    """
    wind_functions = {}
    wind_functions['model'] = model

    for i in range(hours_ahead + 1):
        if (i % 3 == 0):
            filename = 'data/{}/{}f{:03d}'.format(model, model, i)
            wind_functions[i] = grib_to_wind_function(filename)
    return wind_functions


def wind_function(winds, coordinate, time):
    """
    Vectorized TWA and TWS function from forecast.

            Parameters:
                    winds (dict): available forecast wind functions
                    coordinate (array): array of tuples (lats, lons)
                    time (datetime): time to forecast

            Returns:
                    forecast (dict):
                        twa (array): array of TWA
                        tws (array): array of TWS
    """
    model_time = dt.datetime.strptime(winds['model'], "%Y%m%d%H")
    rounded_time = round_time(time, 3600 * 3)

    timedelta = rounded_time - model_time
    forecast = int(timedelta.seconds / 3600)

    wind = winds[forecast]
    twa = wind['twa'](coordinate)
    tws = wind['tws'](coordinate)
    return {'twa': twa, 'tws': tws}
