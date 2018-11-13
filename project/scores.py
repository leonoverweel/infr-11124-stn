import csv
from datetime import datetime, timedelta, time

from pprint import pprint

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
            'punctuality': [float(punctuality) if punctuality != 'None' else -1 
                for punctuality in option_data[7].split()]
        }

        # Filter on arriving between 8:00 and 9:00
        if option['arrive'] < time(hour=8) or option['arrive'] > time(hour=9):
            continue
        
        # Filter on travel time <= 2 hours
        if option['minutes'] > timedelta(minutes=120):
            continue

        stations[station_id].append(option)

scores = {}

for station_id in stations:
    scores[station_id] = {}

    # Crowd scores: the score for the most crowded leg of each option
    scores[station_id]['c'] = [max(option['crowd']) for option in stations[station_id]]

    # Duration scores: (minutes to get to ASD) / 120 for each option
    scores[station_id]['d'] = [option['minutes'].seconds / (60 * 120) 
        for option in stations[station_id]]

    break

pprint(scores)