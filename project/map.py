import csv

from cartopy.io import shapereader
import numpy as np
import geopandas
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import cartopy.crs as ccrs


def plot_netherlands(ax):
    df = geopandas.read_file('data/ne_10m_admin_0_countries')
    poly = df.loc[df['ADMIN'] == 'Netherlands']['geometry'].values[0]

    ax.add_geometries(
        poly, 
        crs=ccrs.PlateCarree(), 
        facecolor='0.6',
    )


def plot_stations(ax):
    longs = []
    lats = []
    scores = []

    with open('data/stations.csv') as stations_file:
        station_reader = csv.reader(stations_file)
        next(station_reader, None)

        for station in station_reader:
            longs.append(float(station[2]))
            lats.append(float(station[3]))
            scores.append(np.random.rand())

    cdict = {
        'red': (
            (0.0, 1, 1),
            (0.5, 1, 1),
            (1.0, 0, 0)),
        'green': (
            (0.0, 0, 0),
            (0.5, 1, 1),
            (1.0, 1, 1)),
        'blue':  (
            (0.0, 0, 0),
            (1.0, 0, 0))
    }
    cmap = colors.LinearSegmentedColormap('GnRd', cdict)

    ax.scatter(
        np.array(lats), 
        np.array(longs), 
        c=scores,
        cmap=cmap,
        vmin=0,
        vmax=1,
        s=20,
        transform=ccrs.PlateCarree(), 
        zorder=2
    )


# Set up axes
plt.figure(figsize=(4,4.5))
ax = plt.axes(projection=ccrs.PlateCarree(), frameon=False)

# Plot stuff
plot_netherlands(ax)
plot_stations(ax)

# Make figure pretty
plt.gca().outline_patch.set_visible(False)
plt.tight_layout()

ax.set_extent([3.1, 7.5, 50.6, 53.7], crs=ccrs.PlateCarree())
ax.set_aspect('auto')

# Save figure
plt.savefig('data/test.pdf')
plt.show()