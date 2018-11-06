import csv
import json

with open('data/routes-raw.json') as infile:
    data = json.load(infile)

    with open('data/routes.csv', 'w') as outfile:
        writer = csv.writer(outfile)
        writer.writerow([
            'Station', 'Option ID', 'Depart', 'Arrive', 'Minutes', 'Legs', 'Crowd', 'Punctuality'
        ])

        for route in data:
            try:
                station = route['vertreklocatie']['id'].upper()
            except:
                continue
            
            for option_id, option in enumerate(route['reismogelijkheden']):
                try:
                    writer.writerow([
                        station,  # Station name
                        option_id,   # Option ID
                        option['vertrektijd'][-5:],  # Departure time
                        option['aankomsttijd'][-5:],  # Arrival time
                        option['reistijd']['uren'] * 60 + option['reistijd']['minuten'],  # Duration
                        ' '.join(['{}->{}'.format(
                            leg['stops'][0]['locatie']['id'],
                            leg['stops'][-1]['locatie']['id'],
                        ).upper() for leg in option['reisdelen']]), ## Legs
                        ' '.join([leg['crowdForecast'] for leg in option['reisdelen']]),
                        ' '.join([str(leg['punctuality']) for leg in option['reisdelen']]),
                    ])
                except:
                    print('Unable to parse', station, option_id)
