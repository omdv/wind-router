"""Utility functions."""
import datetime


def mps_to_knots(vals):
    """Meters/second to knots."""
    return vals * 3600.0 / 1852.0


def knots_to_mps(vals):
    """Knot to meters/second."""
    return vals * 1852.0 / 3600.0


def round_time(dt=None, round_to=60):
    """
    Round a datetime object to any time lapse in seconds.

    ref: /questions/3463930/how-to-round-the-minute-of-a-datetime-object
    dt : datetime.datetime object, default now.
    round_to : Closest number of seconds to round to, default 1 minute.
    Author: Thierry Husson 2012 - Use it as you want but don't blame me.
    """
    if dt is None:
        dt = datetime.datetime.now()
    seconds = (dt.replace(tzinfo=None) - dt.min).seconds
    rounding = (seconds + round_to / 2) // round_to * round_to
    return dt + datetime.timedelta(0, rounding - seconds, - dt.microsecond)
