"""Routing functions."""
from geovectorslib import geod

import numpy as np

from .polars import boat_speed_function


def move_boat_direct(lats, lons, hdgs,
                     boat, gfs,
                     hours, segments,
                     verbose=False):
    """
    Given boat configuration, starting point and route parameters determine
    the end point.

    lats, lons, hdgs - vectors of starting points and headings
    boat - boat profile
    gfs - interpolation functions for GFS
    hours, segments - number of hours per segment and number of segments
    """
    s12 = np.zeros(len(lats))

    p2 = (lats, lons)
    for i in range(segments):
        twa = gfs['twa'](p2)
        tws = gfs['tws'](p2)
        wind = {'tws': tws, 'twa': twa - hdgs}

        bs = boat_speed_function(boat, wind)

        if verbose:
            print('TWA: ', twa)
            print('TWS: ', tws)
            print('HDG: ', hdgs)
            print('WA:  ', twa - hdgs)
            print('BS:  ', bs)

        # distance in meters
        dist = (hours * 3600) * bs

        # move boat
        g = geod.direct(p2[0], p2[1], hdgs, dist)

        s12 += dist
        p2 = (g['lat2'], g['lon2'])

    return {'azi1': hdgs, 's12': dist, 'p2': p2, 't12': hours * segments}


def calc_isochrone(start, boat, gfs):
    """
    Estimate isochrones given a variety of headings.

    start - scalar start point
    boat - boat profile
    gfs - interpolation functions for interpolated GFS
    """
    hdgs = [10 * i for i in range(36)]
    hours = 10
    segments = 1
    lat = start[0]
    lon = start[1]
    iso = move_boat_direct(
        lat * np.ones(len(hdgs)),
        lon * np.ones(len(hdgs)),
        hdgs, boat, gfs, hours, segments, True)
    return iso
