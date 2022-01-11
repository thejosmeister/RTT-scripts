import requests
from bs4 import BeautifulSoup
import csv
import sys
import pandas as pd
import re
import numpy as np


def Parse_Rtt_Location_Page(start_time: str, end_time: str, location_page_link: str):
    """
    :param start_time: start of period to look for trains in format hhmm
    :param end_time: end of period to look for trains in format hhmm
    :param location_page_link: link to rtt location page
    :return: list of links to rtt train pages.
    """

    # sort link with times
    base_location_page_link = re.match('(.*/\\d{4}-\\d{2}-\\d{2}/)', location_page_link).group(1)
    link_to_get = base_location_page_link + start_time + '-' + end_time

    page = requests.get(link_to_get)

    soup = BeautifulSoup(page.content, 'html.parser')

    # This will find all the trains listed on the page
    trains = soup.find_all('a', class_='service')

    train_links = []

    for train in trains:
        train_link = train['href']
        if 'allox_id' in train_link:
            train_link = train_link.split('allox_id=')[0] + 'allox_id=0'
        train_links.append(train_link)

    page_header = soup.find_all('div', class_='header-text')
    location = page_header[0].find('h3').get_text().strip().split('\n')[0].strip()

    return [location, [f'https://www.realtimetrains.co.uk{t}' for t in train_links]]


# pageurl = sys.argv[1]
pageurls1 = Parse_Rtt_Location_Page('0000', '2400',
                                    'https://www.realtimetrains.co.uk/search/detailed/gb-nr:SEL/2021-12-01/0000-2359?stp=WVS&show=all&order=wtt')[
    1]
pageurls2 = Parse_Rtt_Location_Page('0000', '2400',
                                    'https://www.realtimetrains.co.uk/search/detailed/gb-nr:MRY/2021-12-01/0000-2359?stp=WVS&show=all&order=wtt')[
    1]

unique_ones = list(set(pageurls1) | set(pageurls2))
# filename = 'test_locations'
# The page we want to find the list of services for a station
trains = []

print(len(unique_ones))
for pageurl in unique_ones:
    print('getting ', pageurl)
    page = requests.get(pageurl)

    # Parse this into html
    soup = BeautifulSoup(page.content, 'html.parser')
    header = soup.find('div', class_='header')
    headcode = header.text[:4]
    uid = pageurl.split('gb-nr:')[1].split('/')[0]

    if headcode[0] not in '12':
        continue
    locations = soup.find('div', class_='locationlist')

    # print(locations.find_all('div',class_='location'))

    for a in locations.find_all('div', class_='location'):
        if a.find('a', {'class': 'name'}) is not None and a.find('div', {'class': 'wtt'}) is not None:
            location = a.find('a', {'class': 'name'}).text

            if a.find('div', {'class': 'wtt'}).find('div', {'class': 'dep'}) is not None:
                time = a.find('div', {'class': 'wtt'}).find('div', {'class': 'dep'}).text.replace('½', '.5')

                if time.strip() == '':
                    time = a.find('div', {'class': 'wtt'}).find('div', {'class': 'arr'}).text.replace('½', '.5')

            elif a.find('div', {'class': 'wtt'}).find('div', {'class': 'arr'}) is not None:
                time = a.find('div', {'class': 'wtt'}).find('div', {'class': 'arr'}).text.replace('½', '.5')

            # Departure Times
            if time != '':
                time = (int(time[0:2]) * 60) + int(time[2:4])
            else:
                time = np.nan

            trains.append({'headcode': uid, 'location': location, 'time': time})

tdf = pd.DataFrame(trains)

# tdf.to_csv('trainsat.csv')


tdf[tdf['headcode'] == 'L07265']

list_of_locations = tdf[tdf['headcode'] == 'G55976']['location'].tolist()

# list_of_locations.insert(0, 'headcode')

headcodes = tdf['headcode'].unique()

list_of_data = []

for hc in headcodes:
    data_for_hc = {'headcode': hc}
    for l in list_of_locations:
        time = np.nan
        for entr in trains:
            if entr['headcode'] == hc and entr['location'] == l:
                time = entr['time']

        data_for_hc[l] = time

    list_of_data.append(data_for_hc)

revised_df = pd.DataFrame(list_of_data)
revised_df.to_csv('trainsat.csv')

# cols = revised_df.columns.drop('headcode')

# def dt_fun(x):


#     return pd.to_datetime(x,format= '%H:%M:%S', errors='coerce')


# revised_df[cols] = revised_df[cols].apply(dt_fun)

a = revised_df.transpose()
a.columns = a.iloc[0]
a = a.drop(a.index[0])

a.insert(0, 'ID', range(0, len(a)))

# import matplotlib.pyplot as pl
# xticks=a.index.values[1:]
# x=[i for i in range(len(xticks))]
# # y=a
# # pl.plot(x,y)
# # pl.xticks(x,xticks)
# # pl.show()
b = a.reset_index()
b = b.rename(columns={"index": "lname"})
ax = b.plot(x='ID', y=b.columns[2:], figsize=(30, 20), xticks=b.index)
ax.set_xticklabels(b["lname"], rotation='vertical');
ax.legend(loc='center right')
# ax.set_xticklabels(a.C)
# a.plot(color=a.columns, figsize=(5, 3))