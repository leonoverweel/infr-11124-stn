import csv
from datetime import datetime, timedelta, time
from pprint import pprint

import numpy as np


CROWD_MAP = {
    'LOW': 0,
    'MEDIUM': 0.5,
    'HIGH': 1,
    'UNKNOWN': 0
}


def _calculate_score(c, alpha_c, d, alpha_d, f, alpha_f, p, alpha_p, s, alpha_s):
    return c * alpha_c \
        + d * alpha_d \
        + (1 - f) * alpha_f \
        + (1 - p) * alpha_p \
        + s * alpha_s


def get_scores(alpha_c, alpha_d, alpha_f, alpha_p, alpha_s):

    # Read in routes.csv
    stations = {}

    with open('data/routes.csv') as routes_file:
        routes_reader = csv.reader(routes_file)
        next(routes_reader)

        for option_data in routes_reader:
            station_id = option_data[0]
            if not station_id in stations:
                stations[station_id] = []
            
            subs = {
                'option_id': option_data[1],
                'depart': datetime.strptime(option_data[2], '%H:%M').time(),
                'arrive': datetime.strptime(option_data[3], '%H:%M').time(),
                'minutes': timedelta(minutes=int(option_data[4])),
                'legs': [tuple(leg.split('->')) for leg in option_data[5].split()],
                'crowd': [CROWD_MAP[crowd] for crowd in option_data[6].split()],
                'punctuality': [float(punctuality) / 100 if punctuality != 'None' else 1
                    for punctuality in option_data[7].split()]
            }

            # Filter on arriving between 8:00 and 9:00
            if subs['arrive'] < time(hour=8) or subs['arrive'] > time(hour=9):
                continue
            
            # Filter on travel time <= 2 hours
            if subs['minutes'] > timedelta(minutes=120):
                continue

            stations[station_id].append(subs)

    # Calculate max number of options and switches
    max_num_options = 0
    max_num_switches = 0
    for station_id in stations:
        if len(stations[station_id]) > max_num_options:
            max_num_options = len(stations[station_id])
        for subs in stations[station_id]:
            if len(subs['legs']) - 1 > max_num_switches:
                max_num_switches = len(subs['legs']) - 1

    # Calculate subscores
    sub_scores = {}

    for station_id in stations:
        sub_scores[station_id] = {}

        # Crowd scores: (crowd score for the most crowded leg) for each option
        sub_scores[station_id]['c'] = [max(subs['crowd']) for subs in stations[station_id]]

        # Duration scores: ((minutes to get to ASD) / 120) for each option
        sub_scores[station_id]['d'] = [subs['minutes'].seconds / (60 * 120) 
            for subs in stations[station_id]]
        
        # Flexibility score: (number of options) / (max number of options)
        sub_scores[station_id]['f'] = len(stations[station_id]) / max_num_options

        # Punctuality score: prod(punctuality of each leg) for each option
        sub_scores[station_id]['p'] = [np.prod(subs['punctuality'])
            for subs in stations[station_id]]

        # Switches score: (number of switches) / (max number of switches) for each option
        sub_scores[station_id]['s'] = [(len(subs['legs']) - 1) / max_num_switches
            for subs in stations[station_id]]

    # Calculate final scores per option
    scores = {}

    for station_id in sub_scores:
        subs = sub_scores[station_id]

        option_scores = [_calculate_score(
            subs['c'][i], alpha_c,
            subs['d'][i], alpha_d,
            subs['f'], alpha_f,
            subs['p'][i], alpha_p,
            subs['s'][i], alpha_s
        ) for i in range(len(subs['c']))]

        if len(option_scores) > 0:
            scores[station_id] = min(option_scores)
        else:
            scores[station_id] = -1

    return scores
