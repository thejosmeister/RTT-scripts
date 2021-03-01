"""
Will create a TT for an individual train spec (so can create repeats if specified)
"""
import isodate
import re
import unittest

from tiplocDictCreator import pull_train_categories_out_of_xml, create_tiploc_dict
from translateTimesAndLocations import produce_dict_with_times_and_locations, convert_time_to_secs, convert_sec_to_time, produce_train_locations


# Reads in TT template file which will be the bare bones of a TT for an individual train.
def read_in_tt_template(timetable_template_location) -> str:
    f = open(timetable_template_location, "r")
    out = ''
    for fl in f:
        out += fl.rstrip()
    f.close()

    return out


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


# Adds activities if specified in a location
def add_location_activities(location: dict, uid: str) -> str:
    out = '<Activities>'
    for activity in location['activities'].keys():
        f = open('templates/activities/' + str(activity) + 'Template.txt', "r")

        for fl in f:
            uid_to_insert = parse_uid_to_insert(location['activities'][activity], uid)
            out += fl.rstrip().replace('${UID}', uid_to_insert)
        f.close()

    return out + '</Activities>'


def create_trip(location: dict, time_increment, initial_offset, uid) -> str:
    out = '<Trip><Location>' + location['location'] + '</Location>'
    if 'dep' in location:
        out += '<DepPassTime>' + str(location['dep'] + time_increment + initial_offset) + '</DepPassTime>'
        if 'arr' not in location and 'isOrigin' not in location:
            out += '<IsPassTime>-1</IsPassTime>'
    if 'arr' in location:
        out += '<ArrTime>' + str(location['arr'] + time_increment + initial_offset) + '</ArrTime>'
    if 'plat' in location:
        out += '<Platform>' + location['plat'] + '</Platform>'
    if 'line' in location:
        out += '<Line>' + location['line'] + '</Line>'
    if 'path' in location:
        out += '<Path>' + location['path'] + '</Path>'
    if 'pth allow' in location:
        out += '<PathAllowance>' + location['pth allow'] + '</PathAllowance>'
    if 'eng allow' in location:
        out += '<EngAllowance>' + location['eng allow'] + '</EngAllowance>'
    if 'pth allow' in location:
        out += '<PathAllowance>' + location['pth allow'] + '</PathAllowance>'

    # Add activities
    if 'activities' in location:
        out += add_location_activities(location, uid)

    return out + '</Trip>'


def create_tts_file(list_of_lists_of_tts: list, filename: str):
    with open(filename, 'w') as f_to_write:
        for list_of_tts in list_of_lists_of_tts:
            for tt in list_of_tts:
                print(tt, file=f_to_write)


def parse_time_expression(frequency_expression) -> int:
    if not isinstance(frequency_expression, int):
        if 'PT' in frequency_expression:
            return int(isodate.parse_duration(frequency_expression).seconds)
        else:
            return convert_time_to_secs(frequency_expression[:4]) - convert_time_to_secs(frequency_expression[7:])
    else:
        return frequency_expression


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


def create_timetable_with_spec_entry(config_dict):

    tt_template = read_in_tt_template(config_dict['timetable_template_location'])

    train_locations = produce_train_locations(config_dict['train_json_tt_location'])
    if 'amended_locations' in config_dict or 'next_uid' in config_dict:
        train_locations = amend_locations(train_locations, config_dict)

    [origin_time, origin, _entry_time, dest_time, dest, locations_on_sim] = produce_dict_with_times_and_locations(
        train_locations, create_tiploc_dict(config_dict['locations_on_sim'])[1])

    train_cat_dict = pull_train_categories_out_of_xml('templates/TrainCategories.xml')[config_dict['train_category']]

    entry_point = config_dict['entry_point']
    frequency = parse_time_expression(config_dict['frequency'])
    initial_offset = parse_time_expression(config_dict['initial_offset'])

    if _entry_time == '' and entry_point is not None:
        entry_time = convert_time_to_secs(input('Input Entry Time'))
    else:
        entry_time = _entry_time

    list_of_timetables = []

    for i in range(config_dict['number_of']):
        time_increment = frequency * i
        headcode = config_dict['headcode_template'][:2] + f"{int(config_dict['headcode_template'][2:]) + (config_dict['headcode_increment'] * i):02d}"
        uid = headcode
        trips = ''.join([create_trip(l, time_increment, initial_offset, uid) for l in locations_on_sim])
        AccelBrakeIndex = train_cat_dict['AccelBrakeIndex']
        if entry_point is not None:
            DepartTime = str(entry_time + time_increment + initial_offset)
        else:
            DepartTime = ''
        MaxSpeed = train_cat_dict['MaxSpeed']
        IsFreight = train_cat_dict['IsFreight']
        TrainLength = train_cat_dict['TrainLength']
        Electrification = train_cat_dict['Electrification']
        OriginName = origin
        DestinationName = dest
        OriginTime = str(convert_time_to_secs(origin_time) + time_increment + initial_offset)
        description = convert_sec_to_time(int(OriginTime)) + ' ' + origin + ' - ' + dest + ' ' + config_dict['train_category']
        DestinationTime = str(convert_time_to_secs(dest_time) + time_increment + initial_offset)
        OperatorCode = config_dict['op_code']
        StartTraction = train_cat_dict['Electrification']
        SpeedClass = train_cat_dict['SpeedClass']
        Category = train_cat_dict['id']
        DwellTimes = ''
        if 'DwellTimes' in train_cat_dict:
            DwellTimes = '<Join>' + train_cat_dict['DwellTimes']['Join'] + '</Join><Divide>' + \
                         train_cat_dict['DwellTimes']['Divide'] + '</Divide><CrewChange>' + train_cat_dict['DwellTimes']['CrewChange'] + '</CrewChange>'


        tt_string = tt_template.replace('${ID}', headcode).replace('${UID}', uid).replace('${AccelBrakeIndex}', AccelBrakeIndex) \
            .replace('${Description}', description) \
            .replace('${MaxSpeed}', MaxSpeed).replace('${isFreight}', IsFreight).replace('${TrainLength}', TrainLength) \
            .replace('${Electrification}', Electrification).replace('${OriginName}', OriginName).replace(
            '${DestinationName}', DestinationName) \
            .replace('${OriginTime}', OriginTime).replace('${DestinationTime}', DestinationTime).replace(
            '${OperatorCode}', OperatorCode).replace('${StartTraction}', StartTraction).replace('${SpeedClass}', SpeedClass) \
            .replace('${Category}', Category).replace('${Trips}', trips).replace('${DwellTimes}', DwellTimes)

        if entry_point is None:
            list_of_timetables.append(tt_string)
        else:
            list_of_timetables.append(tt_string.replace('${EntryPoint}', entry_point).replace('${DepartTime}', DepartTime))


    return list_of_timetables


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
