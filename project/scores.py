import csv
from datetime import datetime, timedelta

from pprint import pprint

CROWD_MAP = {
    'LOW': 0,
    'MEDIUM': 0.5,
    'HIGH': 1,
    'UNKNOWN': 0.5
}
stations = {}

with open('data/routes.csv') as routes_file:
    routes_reader = csv.reader(routes_file)
    next(routes_reader)

    for option in routes_reader:
        station = option[0]
        if not station in stations:
            stations[station] = []
        
        stations[station].append({
            'option_id': option[1],
            'depart': datetime.strptime(option[2], '%H:%M').time(),
            'arrive': datetime.strptime(option[3], '%H:%M').time(),
            'minutes': timedelta(minutes=int(option[4])),
            'legs': [tuple(leg.split('->')) for leg in option[5].split()],
            'crowd': [CROWD_MAP[crowd] for crowd in option[6].split()],
            'punctuality': [float(punctuality) if punctuality != 'None' else -1 
                for punctuality in option[7].split()]
        })

pprint(stations['AH'])
