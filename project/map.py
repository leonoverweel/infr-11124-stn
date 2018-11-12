from cartopy.io import shapereader
import numpy as np
import geopandas
import matplotlib.pyplot as plt

import cartopy.crs as ccrs

plt.figure(figsize=(4,4.5))

df = geopandas.read_file('data/ne_10m_admin_0_countries')
poly = df.loc[df['ADMIN'] == 'Netherlands']['geometry'].values[0]

ax = plt.axes(projection=ccrs.PlateCarree(), frameon=False)
plt.gca().outline_patch.set_visible(False)

ax.add_geometries(
    poly, 
    crs=ccrs.PlateCarree(), 
    facecolor='0.9'
)

ax.set_extent([3.1, 7.5, 50.6, 53.7], crs=ccrs.PlateCarree())
ax.set_aspect('auto')

plt.tight_layout()
plt.savefig('data/test.pdf')
plt.show()