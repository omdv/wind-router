import os

# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = True

# Secret key for session management. You can generate random strings here:
# https://randomkeygen.com/
SECRET_KEY = 'my precious'

# Default map coordinates - lat1, lon1, lat2, lon2
DEFAULT_MAP = [30, 0, 45, 40]
DEFAULT_ROUTE = [43.70313, 7.26608, 33.888630, 35.495480]
