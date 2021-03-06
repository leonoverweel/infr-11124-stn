import csv

import numpy as np
import geopandas
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import cartopy.crs as ccrs

from scores import get_scores


def get_station_data(alphas):
    longs = []
    lats = []
    scores = []

    station_scores = {station_id:score for station_id, score in get_scores(
        alpha_c=alphas['c'],
        alpha_d=alphas['d'],
        alpha_f=alphas['f'],
        alpha_p=alphas['p'],
        alpha_s=alphas['s']
    ).items() if score != -1}

    with open('data/stations.csv') as stations_file:
        station_reader = csv.reader(stations_file)
        next(station_reader, None)

        for station in station_reader:
            if station[0] not in station_scores:
                continue

            longs.append(float(station[2]))
            lats.append(float(station[3]))
            scores.append(station_scores[station[0]])

    return longs, lats, scores, station_scores


def plot_netherlands(ax):
    df = geopandas.read_file('data/ne_10m_admin_0_countries')
    poly = df.loc[df['ADMIN'] == 'Netherlands']['geometry'].values[0]
    ax.add_geometries(
        poly, 
        crs=ccrs.PlateCarree(), 
        facecolor='0.6',
    )


def plot_stations(ax, lats, longs, scores, max_score):
    cdict = {
        'red': (
            (0.0, 0, 0),
            (0.5, 1, 1),
            (1.0, 1, 1)),
        'green': (
            (0.0, 1, 1),
            (0.5, 1, 1),
            (1.0, 0, 0)),
        'blue':  (
            (0.0, 0, 0),
            (1.0, 0, 0))
    }
    cmap = colors.LinearSegmentedColormap('GnRd', cdict)

    ax.scatter(
        np.array(lats), 
        np.array(longs), 
        c=[(s / max_score) for s in scores],
        cmap=cmap,
        vmin=0,
        vmax=1,
        s=8,
        transform=ccrs.PlateCarree(), 
        zorder=2
    )

    # Amsterdam Centraal
    ax.scatter(np.array([4.90027761459351]), np.array([52.3788871765137]), s=20, c='k',
       transform=ccrs.PlateCarree(), zorder=3)


# Get data
save_data = True

alphas = {
    'c': 5,
    'd': 3,
    'f': 1,
    'p': 1,
    's': 2
}
max_score = sum(alphas.values())

longs, lats, scores, station_scores = get_station_data(alphas)

# Set up axes
plt.figure(figsize=(4,4.5))
ax = plt.axes(projection=ccrs.PlateCarree(), frameon=False)

# Plot stuff
plot_netherlands(ax)
plot_stations(ax, lats, longs, scores, max_score)

# Make figure pretty
plt.gca().outline_patch.set_visible(False)
plt.rcParams.update({'mathtext.default': 'regular'})
plt.title('$\\alpha_c = {c}; \\alpha_d = {d}; \\alpha_f = {f}; \\alpha_p = {p}; \\alpha_s = {s}$'.format_map(alphas),
          y=0.95)
plt.tight_layout()

ax.set_extent([3.3, 7.2, 50.7, 53.8], crs=ccrs.PlateCarree())
ax.set_aspect('auto')

# Save data
if save_data:

    # Save figure
    fig_key = 'c{c}-d{d}-f{f}-p{p}-s{s}'.format_map(alphas)
    plt.savefig('data/plots/' + fig_key + '.pdf')

    # Save ranking
    best_stations = sorted(station_scores, key=station_scores.get)
    with open('data/rankings/' + fig_key + '.txt', 'w') as outfile:
        outfile.write('Station,Score\n')
        for station_id in best_stations:
            outfile.write('{},{:.4f}\n'.format(station_id, station_scores[station_id] / max_score))

# Show figure
plt.show()
