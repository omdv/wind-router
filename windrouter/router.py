"""Routing functions."""
from geovectorslib import geod

import numpy as np

from windrouter.isochrone import Isochrone
from windrouter.polars import boat_speed_function
from windrouter.weather import wind_function
from scipy.stats import binned_statistic


def move_boat_direct(lats, lons, hdgs, boat, winds,
                     start_time, delta_time, verbose=False):
    """
    Move boat forward from starting points, given headings and conditions.

            Parameters:
                lats, lons - array of starting lats and lons
                hdgs (array) - headings
                boat (dict) - boat profile
                winds (dict) - wind functions
                start_time (datetime) - start time
                delta_time (float) - time to move in seconds

            Returns:
                gcr (dict) - dictionary of vectors
    """
    winds = wind_function(winds, (lats, lons), start_time)
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
    gcr = geod.direct(lats, lons, hdgs, dist)

    return {'azi1': hdgs,
            's12': dist,
            'lats2': gcr['lat2'],
            'lons2': gcr['lon2'],
            't12': delta_time}


def prune_isochrone(iso: Isochrone, x, y, bins, trim=True):
    """
    Binned statistic.

            Parameters:
                iso: isochrone dictionary
                x: values to binarize
                y: values to apply max to
                bins: bins edges, dimension is n_bins + 1
                trim: whether return just one of max values
            Returns:
                pruned isochrone dictionary with max values in each bin
    """
    idxs = []
    result = {}

    bin_stat, bin_edges, bin_number = binned_statistic(
        iso[x], iso[y], statistic='max', bins=bins)

    if trim:
        for i in range(len(bin_edges)-1):
            try:
                idxs.append(np.where(iso[y] == bin_stat[i])[0][0])
            except IndexError:
                pass
        idxs = list(set(idxs))
    else:
        for i in range(len(bin_edges)-1):
            idxs.append(np.where(iso[y] == bin_stat[i])[0])
        idxs = list(set([item for subl in idxs for item in subl]))

    for k in iso.keys():
        if isinstance(iso[k], (list, np.ndarray)):
            result[k] = iso[k][idxs]
        else:
            result[k] = iso[k]
    return result


def recursive_routing(iso,
                      boat,
                      winds,
                      delta_time,
                      params,
                      verbose=False):
    """
    Progress one isochrone with pruning.

            Parameters:
                iso (Isochrone) - starting isochrone
                start_point (tuple) - starting point of the route
                end_point (tuple) - end point of the route
                x1_coords (tuple) - tuple of arrays (lats, lons)
                x2_coords (tuple) - tuple of arrays (lats, lons)
                boat (dict) - boat profile
                winds (dict) - wind functions
                start_time (datetime) - start time
                delta_time (float) - time to move in seconds
                params (dict) - isochrone calculation parameters

            Returns:
                iso (Isochrone) - next isochrone
    """
    # # determine headings towards end point
    # gcrs = geod.inverse(x1_coords[0],
    #                     x1_coords[1],
    #                     x2_coords[0],
    #                     x2_coords[1])

    # construct parameters for boat_direct call
    lats = np.repeat(iso.lats1, params['ROUTER_HDGS_SEGMENTS'] + 1)
    lons = np.repeat(iso.lons1, params['ROUTER_HDGS_SEGMENTS'] + 1)

    # vector of GCR heading +/- increments
    hdgs = np.repeat(iso.azi0, params['ROUTER_HDGS_SEGMENTS'] + 1)
    delta_hdgs = np.linspace(
        -params['ROUTER_HDGS_SEGMENTS'] * params['ROUTER_HDGS_INCREMENTS_DEG'],
        +params['ROUTER_HDGS_SEGMENTS'] * params['ROUTER_HDGS_INCREMENTS_DEG'],
        params['ROUTER_HDGS_SEGMENTS'] + 1)
    delta_hdgs = np.tile(delta_hdgs, len(iso.lats1))
    hdgs = hdgs - delta_hdgs

    # call boat direct with N_coords x (ROUTER_HDGS_SEGMENTS+1) vector
    move = move_boat_direct(lats, lons, hdgs,
                            boat, winds,
                            iso.time1, delta_time,
                            verbose=True)

    print(move)

    # # pruning the new isochrone
    # # determine gcrs from X0 to Xi
    # start_lats = np.repeat(start_point[0], len(iso['lats2']))
    # start_lons = np.repeat(start_point[1], len(iso['lons2']))
    # gcrs = geod.inverse(start_lats, start_lons, iso['lats2'], iso['lons2'])
    
    # # determine bins - isochrone pruning segments
    # c_coeff = np.pi / (60 * 180)
    # gcr_x0 = geod.inverse(
    #     start_point[0], start_point[1],
    #     end_point[0], end_point[1])
    
    # iso['azi0'] = gcrs['azi1']
    # iso['s0'] = gcrs['s12']
    # bins = []
    
    # iso2 = prune_isochrone(iso, 'azi0', 's0',)
    # print(iso2)

    # hdgs = [10 * i for i in range(36)]
    # hours = 10
    # segments = 1
    # lat = start[0]
    # lon = start[1]
    # iso = move_boat_direct(
    #     lat * np.ones(len(hdgs)),
    #     lon * np.ones(len(hdgs)),
    #     hdgs, boat, gfs, hours, segments, True)
    # print(iso)
    return None
