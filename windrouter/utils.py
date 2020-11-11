def mps_to_knots(vals):
    """Meters/second to knots."""
    return vals * 3600.0 / 1852.0


def knots_to_mps(vals):
    """Knots to meters/second"""
    return vals * 1852.0 / 3600.0
