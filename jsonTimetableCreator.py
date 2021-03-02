"""
Will create a TT for an individual train spec (so can create repeats if specified)
"""
import isodate
import re
import unittest

from tiplocDictCreator import pull_train_categories_out_of_xml, create_tiploc_dict
from translateTimesAndLocations import produce_dict_with_times_and_locations, convert_time_to_secs, convert_sec_to_time, produce_train_locations


FILE_WITH_CATEGORIES = 'templates/TrainCategories.xml'


# Parse uid pattern for next uid
def parse_uid_to_insert(uid_pattern: str, current_uid: str) -> str:
    out = ''
    # Group 1: uid, Group 2: uid[0], Group 3: uid[1], Group 4: uid[2:4], Group 5: rest of uid, Group 6: 1st increment,
    # Group 7: 2nd increment
    uid_regex = "^(([0-9\\*])([A-Z])([0-9]{2}|\\*\\*)([A-Z0-9]*))(?:((?:\\+|\\-)\\d+)((?:\\+|\\-)\\d+))?$"
    match_object = re.match(uid_regex, uid_pattern)
    if match_object is None:
        print('Bad uid pattern, pattern:' + uid_pattern + ' headcode: ' + current_uid)
        return ''
    first_incr = match_object.group(6)
    second_incr = match_object.group(7)
    if match_object.group(2) == '*':
        if first_incr is not None:
            out += str((int(current_uid[0]) + int(first_incr)) % 10)
        else:
            out += current_uid[0]
    else:
        out += match_object.group(2)

    out += match_object.group(3)

    if match_object.group(4) == '**':
        if second_incr is not None:
            out += f"{(int(current_uid[2:4]) + int(second_incr)) % 100:02d}"
        else:
            out += current_uid[2:4]
    else:
        out += match_object.group(4)

    if match_object.group(5) is not None:
        out += match_object.group(5)

    return out


# Adds activities if specified in a trip
def add_location_activities(location: dict, uid: str) -> dict:
    out = {}
    for activity_title in location['activities'].keys():
        out[str(activity_title)] = parse_uid_to_insert(location['activities'][activity_title], uid)

    return out


# Creates a trip within a TT, this translates as a location the train visits.
def create_trip(location: dict, time_increment, initial_offset, uid) -> dict:
    out = location.copy()
    if 'dep' in location:
        out['dep'] = convert_sec_to_time(location['dep'] + time_increment + initial_offset)
    if 'arr' in location:
        out['arr'] = convert_sec_to_time(location['arr'] + time_increment + initial_offset)

    # Add activities
    if 'activities' in location:
        out['activities'] = add_location_activities(location, uid)

    return out


# Parse time expressions written in the yaml TT def to seconds past midnight.
# Expression is either ISO duration or (hhmm - hhmm)
def parse_time_expression(frequency_expression) -> int:
    if not isinstance(frequency_expression, int):
        if 'PT' in frequency_expression:
            return int(isodate.parse_duration(frequency_expression).seconds)
        else:
            return convert_time_to_secs(frequency_expression[:4]) - convert_time_to_secs(frequency_expression[7:])
    else:
        return frequency_expression


# Will sub in any amendments listed in yaml TT spec for any locations.
def amend_locations(train_locations: list, config_dict: dict) -> list:
    if 'amended_locations' in config_dict:
        for tl in train_locations:
            for al in config_dict['amended_locations']:
                if tl['location'] == al['location']:
                    for prop in al.keys():
                        tl[str(prop)] = al[prop]

    if 'next_uid' in config_dict:
        for tl in train_locations:
            if 'activities' in tl:
                if 'trainBecomes' in tl['activities']:
                    tl['activities']['trainBecomes'] = config_dict['next_uid']

    return train_locations


def create_json_timetables_with_spec_entry(config_dict: dict):
    """
    Creates json TTs for the number of trains specified in each line of a timetable spec.

    Currently handles the following config:
     - headcode_template: Is the UID for the train(s), format: <headcode><extra-chars>
     - headcode_increment: How much to increment headcode if multiple trains
     - train_json_tt_location: Path and name of train locations file
     - locations_on_sim: Path and name of sim locations file
     - timetable_template_location: the TT template filepath.
     - entry_point: Location code of entry point into sim (if one exists)
     - frequency: How often will the train repeat. (seconds)
     - number_of: How many repeats of this TT.
     - train_category: Train category description e.g. 'IEP 800/3 - Bi Mode - 9 Car'
     - initial_offset: How much later should the 1st train be than the specified time in the location list file. (secs past 00:00)
     - op_code: The operator code for the trains. e.g. 'GW'
     - next_uid: A pattern defining what the next uid/headcode is if the train becomes another. Format in readme.
     - amended_locations: List of changes we want to make at a location found in the locations file i.e. plat change
    :param config_dict: Map of config values.
    :return: A list of json objects that are train TTs.
    """

    train_locations = produce_train_locations(config_dict['train_json_tt_location'])
    if 'amended_locations' in config_dict or 'next_uid' in config_dict:
        train_locations = amend_locations(train_locations, config_dict)

    # Now we have quite a few bits.
    [original_o_time, origin, _entry_time, original_dest_time, dest, locations_on_sim] = produce_dict_with_times_and_locations(
        train_locations, create_tiploc_dict(config_dict['locations_on_sim'])[1])

    train_cat_dict = pull_train_categories_out_of_xml(FILE_WITH_CATEGORIES)[config_dict['train_category']]
    entry_point = config_dict['entry_point']
    frequency = parse_time_expression(config_dict['frequency'])
    initial_offset = parse_time_expression(config_dict['initial_offset'])

    # Can specify your own entry time but is easier to modify TT locations file.
    if _entry_time == '' and entry_point is not None:
        entry_time = convert_time_to_secs(input('Input Entry Time'))
    else:
        entry_time = _entry_time

    list_of_json_timetables = []

    for i in range(config_dict['number_of']):
        train_tt = {}
        # Work out time increment from last train.
        time_increment = frequency * i

        headcode = config_dict['headcode_template'][:2] + f"{int(config_dict['headcode_template'][2:4]) + (config_dict['headcode_increment'] * i):02d}"
        uid = headcode + config_dict['headcode_template'][4:]

        # Create the trips in the TT
        trips = [create_trip(l, time_increment, initial_offset, uid) for l in locations_on_sim]

        origin_time = convert_sec_to_time(convert_time_to_secs(original_o_time) + time_increment + initial_offset)
        destination_time = convert_sec_to_time(convert_time_to_secs(original_dest_time) + time_increment + initial_offset)
        # Sort all the parameters to plug in to template.
        if entry_point is not None:
            train_tt['entry_point'] = entry_point
            train_tt['entry_time'] = convert_sec_to_time(entry_time + time_increment + initial_offset)

        train_tt['headcode'] = headcode
        train_tt['uid'] = uid
        train_tt['max_speed'] = train_cat_dict['MaxSpeed']
        train_tt['accel_brake_index'] = train_cat_dict['AccelBrakeIndex']
        train_tt['is_freight'] = train_cat_dict['IsFreight']
        train_tt['train_length'] = train_cat_dict['TrainLength']
        train_tt['electrification'] = train_cat_dict['Electrification']
        train_tt['origin_name'] = origin
        train_tt['destination_name'] = dest
        train_tt['origin_time'] = origin_time
        train_tt['description'] = origin_time + ' ' + origin + ' - ' + dest + ' ' + config_dict['train_category']
        train_tt['destination_time'] = destination_time
        train_tt['operator_code'] = config_dict['op_code']
        train_tt['start_traction'] = train_cat_dict['Electrification']
        train_tt['speed_class'] = train_cat_dict['SpeedClass']
        train_tt['category'] = train_cat_dict['id']
        train_tt['tt_template'] = config_dict['timetable_template_location']
        train_tt['locations'] = trips
        if 'DwellTimes' in train_cat_dict:
            train_tt['dwell_times'] = {'join': train_cat_dict['DwellTimes']['Join'],
                                       'divide': train_cat_dict['DwellTimes']['Divide'],
                                       'crew_change': train_cat_dict['DwellTimes']['CrewChange']}

        list_of_json_timetables.append(train_tt)

    return list_of_json_timetables



# UTs
class TestTimetableCreator(unittest.TestCase):
    def test_parse_uid_to_insert(self):
        self.assertEqual(parse_uid_to_insert('1F99', '1F99'), '1F99', "Should be '1F99'")
        self.assertEqual(parse_uid_to_insert('1F9', '1F99'), '', "Should be ''")
        self.assertEqual(parse_uid_to_insert('1F99+0+0', '1F99'), '1F99', "Should be '1F99'")
        self.assertEqual(parse_uid_to_insert('1F**', '1F99'), '1F99', "Should be '1F99'")
        self.assertEqual(parse_uid_to_insert('1F**+0+1', '1F98'), '1F99', "Should be '1F99'")
        self.assertEqual(parse_uid_to_insert('1F**+0-1', '1F99'), '1F98', "Should be '1F98'")
        self.assertEqual(parse_uid_to_insert('1F**+0+1', '1F99'), '1F00', "Should be '1F99'")
        self.assertEqual(parse_uid_to_insert('1F**+0-1', '1F00'), '1F99', "Should be '1F99'")
        self.assertEqual(parse_uid_to_insert('*F99+1+1', '1F99'), '2F99', "Should be '2F99'")
        self.assertEqual(parse_uid_to_insert('*F99-1+1', '1F99'), '0F99', "Should be '0F99'")
        self.assertEqual(parse_uid_to_insert('*F99-1+1', '0F99'), '9F99', "Should be '9F99'")
        self.assertEqual(parse_uid_to_insert('*F88-1+1', '2F99'), '1F88', "Should be '1F88'")
        self.assertEqual(parse_uid_to_insert('*F**-1+1', '2F99'), '1F00', "Should be '1F00'")
        self.assertEqual(parse_uid_to_insert('*F**QQQ-1+1', '2F99'), '1F00QQQ', "Should be '1F00QQQ'")

    def test_create_trip(self):
        location = {'arr': 600, 'line': 'UM', 'location': 'SDON', 'plat': '1','activities': {'trainBecomes': '5G09+0+0'}}
        trip = {'arr': '0010', 'line': 'UM', 'location': 'SDON', 'plat': '1','activities': {'trainBecomes': '5G09'}}
        self.assertEqual(create_trip(location, 0, 0, '1L88'), trip)

        location = {'arr': 600, 'line': 'UM', 'location': 'SDON', 'plat': '1','activities': {'trainBecomes': '*G**+1+1'}}
        trip = {'arr': '0010', 'line': 'UM', 'location': 'SDON', 'plat': '1', 'activities': {'trainBecomes': '2G89'}}
        self.assertEqual(create_trip(location, 0, 0, '1L88'), trip)

        location = {'dep': 0, 'line': 'UM', 'location': 'SDON'}
        trip = {'dep': '0002', 'line': 'UM', 'location': 'SDON'}
        self.assertEqual(create_trip(location, 60, 60, '1L88'), trip)