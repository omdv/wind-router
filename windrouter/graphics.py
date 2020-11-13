import cartopy.crs as ccrs
import cartopy.feature as cf

from geovectorslib import geod

from matplotlib.figure import Figure

from .grib import grib_to_wind_vectors


def get_gcr_points(lat1, lon1, lat2, lon2, n_points=10):
    """Discretize gcr between two scalar coordinate points."""
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


def create_map(lat1, lon1, lat2, lon2, dpi):
    """Return map figure."""
    fig = Figure(
        figsize=(1200 / dpi, 400 / dpi),
        dpi=dpi)
    fig.set_constrained_layout_pads(
        w_pad=4. / dpi,
        h_pad=4. / dpi)
    ax = fig.add_subplot(111, projection=ccrs.PlateCarree())
    ax.set_extent([lon1, lon2, lat1, lat2], crs=ccrs.PlateCarree())
    ax.add_feature(cf.LAND)
    ax.add_feature(cf.OCEAN)
    ax.add_feature(cf.COASTLINE)
    ax.gridlines(draw_labels=True)
    return fig


def plot_barbs(fig, filepath, lat1, lon1, lat2, lon2):
    """Add barbs to the map figure."""
    u, v, lats, lons = grib_to_wind_vectors(filepath, lat1, lat2, lon1, lon2)

    ax = fig.get_axes()[0]
    ax.barbs(lons, lats, u, v, length=5,
             sizes=dict(emptybarb=0.25, spacing=0.2, height=0.5),
             linewidth=0.95)
    # ax.quiver(lons, lats, u, v)
    return fig


def plot_gcr(fig, lat1, lon1, lat2, lon2):
    """Add gcrs between provided points to the map figure."""
    path = get_gcr_points(lat1, lon1, lat2, lon2, n_points=10)
    lats = [x[0] for x in path]
    lons = [x[1] for x in path]

    ax = fig.get_axes()[0]
    ax.plot(lons, lats, 'r-', transform=ccrs.PlateCarree())
    return fig


def plot_isochrone(fig: dict, isochrone: dict) -> dict:
    """
    Add isochrone to the map figure.

    Input: dictionary from move_boat_direct
    """
    ax = fig.get_axes()[0]
    for p in isochrone['p2']:
        ax.plot(p[0], p[1], 'r-', transform=ccrs.PlateCarree())
