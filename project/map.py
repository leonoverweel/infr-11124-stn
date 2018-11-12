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
        facecolor='0.9'
    )

# Set up axes
plt.figure(figsize=(4,4.5))
ax = plt.axes(projection=ccrs.PlateCarree(), frameon=False)

# Plot stuff
plot_netherlands(ax)

# Make figure pretty
plt.gca().outline_patch.set_visible(False)
plt.tight_layout()

ax.set_extent([3.1, 7.5, 50.6, 53.7], crs=ccrs.PlateCarree())
ax.set_aspect('auto')

# Save figure
plt.savefig('data/test.pdf')
plt.show()