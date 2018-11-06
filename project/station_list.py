import csv
import xml.etree.ElementTree as ET

# http://webservices.ns.nl/ns-api-stations-v2 (requires basic auth)
tree = ET.parse('data/station-list.xml')

with open('data/stations.csv', 'w') as outfile:
    writer = csv.writer(outfile)
    writer.writerow(['Code', 'Name', 'Country', 'Latitude', 'Longitude'])

    for station in tree.getroot():
        code = station.find('Code').text
        name = station.find('Namen').find('Lang').text
        country = station.find('Land').text
        latitude = station.find('Lat').text
        longitude = station.find('Lon').text

        if country != 'NL':
            continue

        writer.writerow([code, name, country, latitude, longitude])
