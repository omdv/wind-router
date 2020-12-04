import datetime as dt
import time
from windrouter import polars, weather, router


if __name__ == "__main__":
    program_start = time.time()

    model = '2020111600'
    boatfile = 'data/polar-ITA70.csv'
    delta_time = 3600
    hours = 120

    fct_winds = weather.read_wind_functions(model, hours)
    r_la1, r_lo1, r_la2, r_lo2 = [43.5, 7.2, 33.8, 35.5]

    start = (r_la1, r_lo1)
    finish = (r_la2, r_lo2)
    start_time = dt.datetime.strptime('2020111607', '%Y%m%d%H')

    boat = polars.boat_properties(boatfile)
    params = {
        'ROUTER_HDGS_SEGMENTS': 180,
        'ROUTER_HDGS_INCREMENTS_DEG': 1,
        'ISOCHRONE_EXPECTED_SPEED_KTS': 8,
        'ISOCHRONE_PRUNE_SECTOR_DEG_HALF': 90,
        'ISOCHRONE_PRUNE_SEGMENTS': 180
    }

    iso = router.routing(
        start, finish,
        boat, fct_winds,
        start_time,
        delta_time, hours,
        params
    )
    print("Completed in {:4.4f} s".format(time.time() - program_start))