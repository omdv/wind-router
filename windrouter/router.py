"""Routing functions"""
from geovectorslib import geod

import numpy as np


def get_gcr(lat1, lon1, lat2, lon2, n_points=10):
    """Calculate gcr between two points."""
    points = [(lat1, lon1)]

    inv = geod.inverse([lat1], [lon1], [lat2], [lon2])
    dist = inv['s12'] / (n_points)

    for i in range(n_points):
        dir = geod.direct(lat1, lon1, inv['azi1'], dist)
        points.append((dir['lat2'][0], dir['lon2'][0]))
        lat1 = dir['lat2'][0]
        lon1 = dir['lon2'][0]
        inv = geod.inverse([lat1], [lon1], [lat2], [lon2])

    return points


def move_boat_direct(lats, lons, hdgs,
                     boat, f_boat_speed,
                     f_tws, f_twa,
                     hours, segments,
                     verbose=False):
    """
    Given boat configuration, starting point and route parameters determine
    the end point

    lats, lons, hdgs - vectors of starting points and headings
    boat, f_boat_speed - boat profile and boat speed function
    f_tws, f_twa - functions for interpolated grib2 tws and twa
    hours, segments - number of hours per segment and number of segments
    """
    s12 = np.zeros(len(lats))
    print(lats, lons, hdgs)

    p2 = (lats, lons)
    for i in range(segments):
        twa = f_twa(p2)
        tws = f_tws(p2)
        sp = f_boat_speed(boat, twa - hdgs, tws)

        if verbose:
            print('TWA:{:4.3f}, WS:{:4.3f}, HDG:{:4.3f},\
                WA: {:4.3f}, BS: {:4.3f})'
                  .format(twa, tws, hdgs, twa - hdgs, sp))

        # distance in meters
        dist = (hours * 3600) * sp

        # move boat
        g = geod.direct(*p2, hdgs, dist)

        s12 += dist
        p2 = (g['lat2'], g['lon2'])

    return {'azi1': hdgs, 's12': dist, 'p2': p2, 't12': hours * segments}
