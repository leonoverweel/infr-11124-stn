import csv
from datetime import datetime, timedelta, time
from pprint import pprint

import numpy as np

# Read in routes.csv
CROWD_MAP = {
    'LOW': 0,
    'MEDIUM': 0.5,
    'HIGH': 1,
    'UNKNOWN': 0
}
stations = {}

with open('data/routes.csv') as routes_file:
    routes_reader = csv.reader(routes_file)
    next(routes_reader)

    for option_data in routes_reader:
        station_id = option_data[0]
        if not station_id in stations:
            stations[station_id] = []
        
        option = {
            'option_id': option_data[1],
            'depart': datetime.strptime(option_data[2], '%H:%M').time(),
            'arrive': datetime.strptime(option_data[3], '%H:%M').time(),
            'minutes': timedelta(minutes=int(option_data[4])),
            'legs': [tuple(leg.split('->')) for leg in option_data[5].split()],
            'crowd': [CROWD_MAP[crowd] for crowd in option_data[6].split()],
            'punctuality': [float(punctuality) / 100 if punctuality != 'None' else -1 
                for punctuality in option_data[7].split()]
        }

        # Filter on arriving between 8:00 and 9:00
        if option['arrive'] < time(hour=8) or option['arrive'] > time(hour=9):
            continue
        
        # Filter on travel time <= 2 hours
        if option['minutes'] > timedelta(minutes=120):
            continue

        stations[station_id].append(option)


# Calculate max number of options and switches
max_num_options = 0
max_num_switches = 0
for station_id in stations:
    if len(stations[station_id]) > max_num_options:
        max_num_options = len(stations[station_id])
    for option in stations[station_id]:
        if len(option['legs']) - 1 > max_num_switches:
            max_num_switches = len(option['legs']) - 1


# Calculate scores
scores = {}

for station_id in stations:
    scores[station_id] = {}

    # Crowd scores: (crowd score for the most crowded leg) for each option
    scores[station_id]['c'] = [max(option['crowd']) for option in stations[station_id]]

    # Duration scores: ((minutes to get to ASD) / 120) for each option
    scores[station_id]['d'] = [option['minutes'].seconds / (60 * 120) 
        for option in stations[station_id]]
    
    # Flexibility score: (number of options) / (max number of options)
    scores[station_id]['f'] = len(stations[station_id]) / max_num_options

    # Punctuality score: prod(punctuality of each leg) for each option
    scores[station_id]['p'] = [np.prod(option['punctuality'])
        for option in stations[station_id]]

    # Switches score: (number of switches) / (max number of switches) for each option
    scores[station_id]['s'] = [(len(option['legs']) - 1) / max_num_switches
        for option in stations[station_id]]

pprint(scores['AH'])