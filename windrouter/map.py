import cartopy.crs as ccrs
import cartopy.feature as cf
from matplotlib.figure import Figure
import random

from .grib import grib_to_wind_vectors
from .router import get_gcr

# (lat1, lon1, lat2, lon2, n_points=10):


def create_map(lat1, lon1, lat2, lon2, dpi=96):
    """Return map figure."""
    fig = Figure(
        figsize=(1200/dpi, 400/dpi),
        dpi=dpi)
    fig.set_constrained_layout_pads(
        w_pad=4./dpi,
        h_pad=4./dpi)
    ax = fig.add_subplot(111, projection=ccrs.PlateCarree())
    ax.set_extent([lon1, lon2, lat1, lat2], crs=ccrs.PlateCarree())
    ax.add_feature(cf.LAND)
    ax.add_feature(cf.OCEAN)
    ax.add_feature(cf.COASTLINE)
    ax.gridlines(draw_labels=True)
    return fig


def add_barbs(fig, filepath, lat1, lon1, lat2, lon2):
    """Add barbs to the map figure."""
    u, v, lats, lons = grib_to_wind_vectors(filepath, lat1, lat2, lon1, lon2)

    ax = fig.get_axes()[0]
    ax.barbs(lons, lats, u, v, length=5,
             sizes=dict(emptybarb=0.25, spacing=0.2, height=0.5),
             linewidth=0.95)
    # ax.quiver(lons, lats, u, v)
    return fig


def add_route(fig, lat1, lon1, lat2, lon2):
    """Add router between two provided points."""
    path = get_gcr(lat1, lon1, lat2, lon2, n_points=10)
    lats = [x[0] for x in path]
    lons = [x[1] for x in path]

    ax = fig.get_axes()[0]
    ax.plot(lons, lats, 'r-', transform=ccrs.PlateCarree())
    return fig


def create_figure(dpi=96):
    """Demo x-y plot for testing."""
    fig = Figure(figsize=(800/dpi, 600/dpi), dpi=dpi)
    axis = fig.add_subplot(1, 1, 1)
    xs = range(100)
    ys = [random.randint(1, 50) for x in xs]
    axis.plot(xs, ys)
    return fig
