"""
Isochrone class definition.
"""
import numpy as np
import datetime as dt
from typing import NamedTuple


class Isochrone(NamedTuple):
    """
    Isochrone data structure with typing.
            Parameters:
                count: isochrone counter
                start: tuple
                finish: tuple
                azi0: float
    """
    count: int
    start: tuple
    finish: tuple
    azi0: float
    lats1: np.ndarray
    lons1: np.ndarray
    lats2: np.ndarray
    lons2: np.ndarray
    azi12: np.ndarray
    s12: np.ndarray
    time1: dt.datetime
