#TODO: Introduce VMG and gybing
"""Boat polars."""
import numpy as np

from scipy.interpolate import interp2d

from .utils import knots_to_mps


def boat_properties(filepath):
    """
    Load boat properties from boat file.

            Parameters:
                    filepath (string): Path to polars file

            Returns:
                    boat (dict): Dict with function and raw polars
    """
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


def boat_speed_function(boat, wind):
    """
    Vectorized boat speed function.

            Parameters:
                    boat (dict): Boat dict with wind function
                    wind (dict): Wind dict with TWA and TWS arrays

            Returns:
                    boat_speed (array): Array of boat speeds
    """
    twa = wind['twa']
    tws = wind['tws']

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
