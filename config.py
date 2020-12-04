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
DEFAULT_ROUTE = [43.5, 7.2, 33.8, 35.5]
DEFAULT_BOAT = 'data/polar-ITA70.csv'
DEFAULT_GFS_DATETIME = '2020111607'
DEFAULT_GFS_HOUR = '06'
DEFAULT_GFS_FCST = '000'
DEFAULT_GFS_RESOLUTION = '1p00'
DEFAULT_GFS_FILE = 'data/2019122212/2019122212f000'
DEFAULT_GFS_MODEL = '2020111600'

# Isochrone routing parameters
ROUTER_HDGS_SEGMENTS = 180
ROUTER_HDGS_INCREMENTS_DEG = 1
ISOCHRONE_EXPECTED_SPEED_KTS = 8
ISOCHRONE_PRUNE_SECTOR_DEG_HALF = 90
ISOCHRONE_PRUNE_SEGMENTS = 180