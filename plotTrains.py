import ast
from translateTimesAndLocations import convert_time_to_secs
import dbClient
import matplotlib.pyplot as plt
import re

f = open('assorted_files/dist_from_rdg.txt', "r")
distances = ast.literal_eval(f.read())
f.close()

all_trains = dbClient.TrainTtDb('swindid_diversions_feb_21').get_all_in_db()

pairs_of_times_and_values = []

for train in all_trains:
    if re.match("^1(L|B|A|H|G)\\d{2}",train['headcode']):
        times = []
        mileages = []
        locations = train['locations']
        for location in locations:
            if location['location'] in distances:
                if 'arr' in location:
                    times.append(convert_time_to_secs(location['arr']))
                    mileages.append(distances[location['location']])
                if 'dep' in location:
                    times.append(convert_time_to_secs(location['dep']))
                    mileages.append(distances[location['location']])

        pairs_of_times_and_values.append([times, mileages, train['headcode']])

plt.style.use('fivethirtyeight')

for i in range(len(pairs_of_times_and_values)):
    plt.plot(pairs_of_times_and_values[i][0], pairs_of_times_and_values[i][1], label=pairs_of_times_and_values[i][2])

# plt.legend(loc=(1.04,0))
plt.show()

