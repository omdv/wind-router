"""Routing functions."""
from geovectorslib import geod

import numpy as np

from windrouter.polars import boat_speed_function
from windrouter.weather import wind_function


def move_boat_direct(start_coords,
                     hdgs,
                     boat,
                     winds,
                     start_time,
                     delta_time,
                     verbose=False):
    """
    Move boat forward from starting points, given headings and conditions.

            Parameters:
                start_coords (tuple) - tuple of arrays (lats, lons)
                hdgs (array) - headings
                boat (dict) - boat profile
                winds (dict) - wind functions
                start_time (datetime) - start time
                delta_time (float) - time to move in seconds

            Returns:
                gcr (dict) - dictionary of vectors
    """
    winds = wind_function(winds, start_coords, start_time)
    twa = winds['twa']
    tws = winds['tws']
    wind = {'tws': tws, 'twa': twa - hdgs}

    bs = boat_speed_function(boat, wind)

    if verbose:
        print('TWA: ', twa)
        print('TWS: ', tws)
        print('HDG: ', hdgs)
        print('WA:  ', twa - hdgs)
        print('BS:  ', bs)

    # distance in meters
    dist = delta_time * bs

    # move boat
    gcr = geod.direct(start_coords[0], start_coords[1], hdgs, dist)

    return {'azi1': hdgs,
            's12': dist,
            'p2': (gcr['lat2'], gcr['lon2']),
            't12': delta_time}


def calc_isochrone(start_coords,
                   end_coords,
                   boat,
                   winds,
                   start_time,
                   delta_time,
                   params,
                   verbose=False):
    """
    Get one isochrone with pruning.

            Parameters:
                start_coords (tuple) - tuple of arrays (lats, lons)
                end_coords (tuple) - tuple of arrays (lats, lons)
                boat (dict) - boat profile
                winds (dict) - wind functions
                start_time (datetime) - start time
                delta_time (float) - time to move in seconds
                params (dict) - isochrone calculation parameters

            Returns:
                gcr (dict) - dictionary of array of isochrones
    """
    # determine headings towards end point
    gcrs = geod.inverse(start_coords[0],
                        start_coords[1],
                        end_coords[0],
                        end_coords[1])

    # construct parameters for boat_direct call
    lats = np.repeat(start_coords[0], params['ROUTER_HDGS_SEGMENTS'] + 1)
    lons = np.repeat(start_coords[0], params['ROUTER_HDGS_SEGMENTS'] + 1)

    # vector of GCR heading +/- increments
    hdgs = np.repeat(gcrs['azi1'], params['ROUTER_HDGS_SEGMENTS'] + 1)
    delta_hdgs = np.linspace(
        -params['ROUTER_HDGS_SEGMENTS'] * params['ROUTER_HDGS_INCREMENTS_DEG'],
        +params['ROUTER_HDGS_SEGMENTS'] * params['ROUTER_HDGS_INCREMENTS_DEG'],
        params['ROUTER_HDGS_SEGMENTS'] + 1)
    delta_hdgs = np.tile(delta_hdgs, len(start_coords[0]))
    hdgs = hdgs - delta_hdgs

    # call boat direct with N_coords x (ROUTER_HDGS_SEGMENTS+1) vector
    iso = move_boat_direct((lats, lons),
                           hdgs,
                           boat,
                           winds,
                           start_time,
                           delta_time,
                           verbose=False)

    # hdgs = [10 * i for i in range(36)]
    # hours = 10
    # segments = 1
    # lat = start[0]
    # lon = start[1]
    # iso = move_boat_direct(
    #     lat * np.ones(len(hdgs)),
    #     lon * np.ones(len(hdgs)),
    #     hdgs, boat, gfs, hours, segments, True)
    print(iso)
    return None
