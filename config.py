import os

# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = True

# DPI properties
DPI = 96

# Secret key for session management. You can generate random strings here:
# https://randomkeygen.com/
SECRET_KEY = 'my precious'

# Defaults - self-explanatory
DEFAULT_MAP = [30, 0, 45, 40]
DEFAULT_ROUTE = [43.70313, 7.26608, 33.888630, 35.495480]
DEFAULT_BOAT = 'data/polar-ITA70.csv'
DEFAULT_GFS_DATE = '20201107'
DEFAULT_GFS_HOUR = '06'
DEFAULT_GFS_FCST = '000'
DEFAULT_GFS_RESOLUTION = '1p00'
DEFAULT_GFS_FILE = 'data/2019122212/2019122212f000'

# Isochrone routing parameters
ROUTER_HDGS_INCREMENTS_DEG = 0.1
ROUTER_HDGS_SEGMENTS = 1800
ROUTER_DELTA_TIME_HRS = 1