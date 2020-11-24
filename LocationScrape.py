import requests
from bs4 import BeautifulSoup
import csv
import sys

pageurl = sys.argv[1]

# The page we want to find the list of services for a station
page = requests.get(pageurl)

#Parse this into html
soup = BeautifulSoup(page.content, 'html.parser')

locations = soup.find('div', class_='locationlist')

# print(locations.find_all('div',class_='location'))

dicts_of_locations = []

for a in locations.find_all('div',class_='location'):
    if a.find('a',{'class':'name'}) != None and a.find('div',{'class':'wtt'}) != None:
        location = {}
        location['location'] = a.find('a',{'class':'name'}).text
        if a.find('div', {'class':'wtt'}).find('div', {'class':'arr'}) != None:
            location['arr'] = a.find('div', {'class':'wtt'}).find('div', {'class':'arr'}).text
        if a.find('div', {'class':'wtt'}).find('div', {'class':'dep'}) != None:
            location['dep'] = a.find('div', {'class':'wtt'}).find('div', {'class':'dep'}).text
        dicts_of_locations.append(location)
        
import pprint
pp = pprint.PrettyPrinter(indent=4)
pp.pprint(dicts_of_locations)

with open('locations.csv', mode='w') as location_file:
    fieldnames = ['location','arr','dep']
    writer = csv.DictWriter(location_file, fieldnames=fieldnames)
    
    writer.writeheader()
    for row in dicts_of_locations:
        writer.writerow(row)
