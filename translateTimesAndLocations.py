import ast
import math
from tiplocDictCreator import create_tiploc_dict

def convert_time_to_secs(time: str) -> int:
    hours = int(time[:2])
    mins = int(time[2:4])
    if len(time) == 6:
        has_half_min = 30
    else:
        has_half_min = 0

    return (3600 * hours) + (60 * mins) + has_half_min

def convert_sec_to_time(time: int) -> str:
    hours = math.floor(time / 3600)
    mins = math.floor((time - (hours * 3600))/60)

    if hours < 10:
        h_prefix = '0'
    else:
        h_prefix = ''
    if mins < 10:
        m_prefix = '0'
    else:
        m_prefix = ''

    return h_prefix + str(hours) + m_prefix + str(mins)


def return_value(inp: dict):
    if 'dep' in inp:
        return inp['dep']
    elif 'arr' in inp:
        return inp['arr']



def sub_in_tiploc(sorted_locations: list, tiploc_dict: dict) -> list:
    for l in sorted_locations:
        for t in tiploc_dict.keys():
            if l['location'] in tiploc_dict[t]:
                l['location'] = str(t)

    return sorted_locations


def produce_dict_with_times_and_locations(location_template_filename: str, tiploc_dict: dict):
    f = open(location_template_filename, "r")
    list_of_locations = ast.literal_eval(f.read())
    f.close()

    for l in list_of_locations:
        if 'dep' in l:
            l['dep'] = convert_time_to_secs(l['dep'])
        if 'arr' in l:
            l['arr'] = convert_time_to_secs(l['arr'])

    sorted_locations = sorted(list_of_locations, key=lambda x: return_value(x))
    origin = sorted_locations[0]['location']
    origin_time = convert_sec_to_time(sorted_locations[0]['dep'])
    dest = sorted_locations[-1]['location']
    dest_time = convert_sec_to_time(sorted_locations[-1]['arr'])
    locations_on_sim = sub_in_tiploc(sorted_locations, tiploc_dict)

    return [origin_time, origin,dest_time, dest, locations_on_sim]

#
# a = produce_dict_with_times_and_locations('1A01_locations.txt', create_tiploc_dict('swindon_locations.txt')[1])
#
# [print(x) for x in a]
