import requests
from bs4 import BeautifulSoup
import csv
import sys

# pageurl = sys.argv[1]
pageurl = 'https://www.realtimetrains.co.uk/train/03483/2021-02-20/detailed'
filename = '5Z74_locations'
# The page we want to find the list of services for a station
page = requests.get(pageurl)

# Parse this into html
soup = BeautifulSoup(page.content, 'html.parser')

locations = soup.find('div', class_='locationlist')

# print(locations.find_all('div',class_='location'))

dicts_of_locations = []

for a in locations.find_all('div', class_='location'):
    if a.find('a', {'class': 'name'}) is not None and a.find('div', {'class': 'wtt'}) is not None:
        location = {'location': a.find('a', {'class': 'name'}).text}
        if a.find('div', {'class': 'wtt'}).find('div', {'class': 'arr'}) is not None:
            arrTime = a.find('div', {'class': 'wtt'}).find('div', {'class': 'arr'}).text
            if len(arrTime) == 4:
                location['arr'] = arrTime
            elif len(arrTime) == 5:
                location['arr'] = arrTime[:4] + '.5'
        if a.find('div', {'class': 'wtt'}).find('div', {'class': 'dep'}) is not None:
            depTime = a.find('div', {'class': 'wtt'}).find('div', {'class': 'dep'}).text
            if len(depTime) == 4:
                location['dep'] = depTime
            elif len(depTime) == 5:
                location['dep'] = depTime[:4] + '.5'
        dicts_of_locations.append(location)

import pprint

pp = pprint.PrettyPrinter(indent=4)

pp.pprint(dicts_of_locations)

# with open('1F05_locations.csv', mode='w') as location_file:
#     fieldnames = ['location', 'arr', 'dep']
#     writer = csv.DictWriter(location_file, fieldnames=fieldnames)
#
#     writer.writeheader()
#     for row in dicts_of_locations:
#         writer.writerow(row)

with open(filename + '.txt', 'w') as f_to_write:
    f_to_write.write(pp.pformat(dicts_of_locations))
