"""Boat vectors"""
import numpy as np

from scipy.interpolate import interp2d

from .utils import knots_to_mps


def get_boat_profile(filepath):
    """Load polar from boat file."""
    polars = np.genfromtxt(filepath, delimiter=';')
    polars = np.nan_to_num(polars)

    ws = polars[0, 1:]
    wa = polars[1:, 0]
    values = polars[1:, 1:]

    # internally we use only meters per second
    ws = knots_to_mps(ws)
    values = knots_to_mps(values)

    f = interp2d(ws, wa, values, kind='linear')
    return {'func': f, 'polars': polars}


# def func_boat_speed(x, boat):
#     """Aux function for np.apply."""
#     tws = x[0]
#     twa = x[1]
#     twa = np.abs(twa)
#     if twa > 180:
#         twa = 360. - twa
#     return boat['func'](tws, twa)


def get_boat_speed(boat, tws, twa):
    """Boat speed for given TWS and TWA."""
    assert twa.shape == tws.shape, "Input shape mismatch"
    func = boat['func']

    # get rid of negative and above 180
    twa = np.abs(twa)
    twa[twa > 180] = 360. - twa[twa > 180]

    # init boat speed vector
    boat_speed = func(tws, twa)

    # unsort the result
    unsorted_idxs_tws = np.argsort(np.argsort(tws))
    unsorted_idxs_twa = np.argsort(np.argsort(twa))
    return boat_speed[unsorted_idxs_twa, unsorted_idxs_tws]
