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
                count: int
                start: tuple
                finish: tuple
                gcr_azi: initial gcr heading
                lats1, lons1, azi1, s12: (M, N) arrays with history
                azi0, s0: (M, 1) vectors without history
                time1: current datetime
                elapsed: complete elapsed timedelta
    """
    count: int
    start: tuple
    finish: tuple
    gcr_azi: float
    lats1: np.ndarray
    lons1: np.ndarray
    azi12: np.ndarray
    s12: np.ndarray
    azi02: np.ndarray
    s02: np.ndarray
    time1: dt.datetime
    elapsed: dt.timedelta
