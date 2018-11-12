import csv

from cartopy.io import shapereader
import numpy as np
import geopandas
import matplotlib.pyplot as plt
import cartopy.crs as ccrs


def plot_netherlands(ax):
    df = geopandas.read_file('data/ne_10m_admin_0_countries')
    poly = df.loc[df['ADMIN'] == 'Netherlands']['geometry'].values[0]

    ax.add_geometries(
        poly, 
        crs=ccrs.PlateCarree(), 
        facecolor='0.8'
    )


def plot_stations(ax):
    longs = []
    lats = []

    with open('data/stations.csv') as stations_file:
        station_reader = csv.reader(stations_file)
        next(station_reader, None)

        for station in station_reader:
            longs.append(float(station[2]))
            lats.append(float(station[3]))

    ax.scatter(
        np.array(lats), 
        np.array(longs), 
        c='k',
        s=10,
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