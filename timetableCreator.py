import isodate

from tiplocDictCreator import pull_train_categories_out_of_xml, create_tiploc_dict
from translateTimesAndLocations import produce_dict_with_times_and_locations, convert_time_to_secs, convert_sec_to_time
import re


def read_in_tt_template(timetable_template_location) -> str:
    f = open(timetable_template_location, "r")
    out = ''
    for fl in f:
        out += fl.rstrip()
    f.close()

    return out


def get_increments_from_pattern(uid_pattern: str):
    return [re.match(".{4}((?:\\+|\\-)\\d+)((?:\\+|\\-)\\d+)", uid_pattern).group(1), re.match(".{4}((?:\\+|\\-)\\d+)((?:\\+|\\-)\\d+)", uid_pattern).group(2)]


def parse_uid_to_insert(uid_pattern: str, current_uid: str) -> str:
    out = ''
    if len(uid_pattern) < 8:
        print('Bad uid pattern, pattern:' + uid_pattern + ' headcode: ' + current_uid)
        return ''
    if '*' not in uid_pattern:
        return uid_pattern[:-4]
    else:
        [first_incr, second_incr] = get_increments_from_pattern(uid_pattern)
        if '*' == uid_pattern[0]:
            out += str(int(current_uid[0]) + int(first_incr))
        else:
            out += uid_pattern[0]

        out += uid_pattern[1]

        if '*' == uid_pattern[2]:
            out += f"{int(current_uid[2:4]) + int(second_incr):02d}"
        else:
            out += uid_pattern[2:4]

        # out += uid_pattern[4:-4]
        return out
# headcode_template[:2] + f"{int(headcode_template[2:]) + (headcode_increment * i):02d}"


def add_location_activities(location: dict, uid: str, next_uid: str) -> str:
    out = '<Activities>'
    for activity in location['activities'].keys():
        f = open('templates/activities/' + str(activity) + 'Template.txt', "r")

        for fl in f:
            if next_uid is not None and 'trainBecomes' in str(activity):
                uid_to_insert = parse_uid_to_insert(next_uid, uid)
            else:
                uid_to_insert = parse_uid_to_insert(location['activities'][activity], uid)
            out += fl.rstrip().replace('${UID}', uid_to_insert)
        f.close()
    return out + '</Activities>'


def create_trip(location: dict, time_increment, initial_offset, uid, next_uid: str) -> str:
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
    # norm_bit = '<AutoLine>-1</AutoLine><AutoPath>-1</AutoPath><IsPassTime>-1</IsPassTime><DownDirection>-1</DownDirection><PrevPathEndDown>-1</PrevPathEndDown><NextPathStartDown>-1</NextPathStartDown>'

    # out += norm_bit

    # Need to add activities
    if 'activities' in location:
        out += add_location_activities(location, uid, next_uid)

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

def create_timetable_with_spec_entry(config_dict):

    tt_template = read_in_tt_template(config_dict['timetable_template_location'])
    [origin_time, origin, _entry_time, dest_time, dest, locations_on_sim] = produce_dict_with_times_and_locations(
        config_dict['train_json_tt_location'], create_tiploc_dict(config_dict['locations_on_sim'])[1])
    train_cat_dict = pull_train_categories_out_of_xml()[config_dict['train_category']]

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
        trips = ''.join([create_trip(l, time_increment, initial_offset, uid, config_dict['next_uid']) for l in locations_on_sim])
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
    # with open(headcode_template + '_timetables.xml', 'w') as f_to_write:
    #     for tt in list_of_timetables:
    #         print(tt, file=f_to_write)




#***************************************************************************************************************************************************************

def create_timetable_with_spec_entry_non_dict(headcode_template, headcode_increment, train_json_tt_location, locations_on_sim,
                                     timetable_template_location, entry_point, frequency, number_of, train_category, initial_offset, next_uid):



    tt_template = read_in_tt_template(timetable_template_location)
    [origin_time, origin, _entry_time, dest_time, dest, locations_on_sim] = produce_dict_with_times_and_locations(
        train_json_tt_location, create_tiploc_dict(locations_on_sim)[1])
    train_cat_dict = pull_train_categories_out_of_xml()[train_category]

    if _entry_time == '' and entry_point is not None:
        entry_time = convert_time_to_secs(input('Input Entry Time'))
    else:
        entry_time = _entry_time

    list_of_timetables = []
    for i in range(number_of):
        time_increment = frequency * i
        headcode = headcode_template[:2] + f"{int(headcode_template[2:]) + (headcode_increment * i):02d}"
        uid = headcode
        trips = ''.join([create_trip(l, time_increment, initial_offset, uid, next_uid) for l in locations_on_sim])
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
        description = convert_sec_to_time(int(OriginTime)) + ' ' + origin + ' - ' + dest + ' ' + train_category
        DestinationTime = str(convert_time_to_secs(dest_time) + time_increment + initial_offset)
        OperatorCode = 'GW'
        StartTraction = train_cat_dict['Electrification']
        SpeedClass = train_cat_dict['SpeedClass']
        Category = train_cat_dict['id']
        DwellTimes = ''
        if 'DwellTimes' in train_cat_dict:
            DwellTimes = '<Join>' + train_cat_dict['DwellTimes']['Join'] + '</Join><Divide>' +\
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
    # with open(headcode_template + '_timetables.xml', 'w') as f_to_write:
    #     for tt in list_of_timetables:
    #         print(tt, file=f_to_write)




