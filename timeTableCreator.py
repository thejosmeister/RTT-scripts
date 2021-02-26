from tiplocDictCreator import pull_train_categories_out_of_xml, create_tiploc_dict
from translateTimesAndLocations import produce_dict_with_times_and_locations, convert_time_to_secs, convert_sec_to_time


def read_in_tt_template(timetable_template_location) -> str:
    f = open(timetable_template_location, "r")
    out = ''
    for fl in f:
        out += fl.rstrip()

    return out


def create_trip(location: dict, time_increment) -> str:
    out = '<Trip><Location>' + location['location'] + '</Location>'
    if 'dep' in location:
        out += '<DepPassTime>' + str(location['dep'] + time_increment) + '</DepPassTime>'
    if 'arr' in location:
        out += '<DepPassTime>' + str(location['arr'] + time_increment) + '</DepPassTime>'
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
    norm_bit = '<AutoLine>-1</AutoLine><AutoPath>-1</AutoPath><IsPassTime>-1</IsPassTime><DownDirection>-1</DownDirection><PrevPathEndDown>-1</PrevPathEndDown><NextPathStartDown>-1</NextPathStartDown>'

    out += norm_bit
    return out + '</Trip>'


def create_timetable_with_spec_entry(headcode_template, headcode_increment, location_list_location, tiploc_location,
                                     timetable_template_location, entry_point, frequency, number_of, train_category):
    output_str = ''
    tt_template = read_in_tt_template(timetable_template_location)
    [origin_time, origin, dest_time, dest, locations_on_sim] = produce_dict_with_times_and_locations(
        location_list_location, create_tiploc_dict(tiploc_location)[1])
    train_cat_dict = pull_train_categories_out_of_xml()[train_category]
    entry_time = convert_time_to_secs('0552.5')

    list_of_timetables = []
    for i in range(number_of):
        time_increment = frequency * i
        trips = ''.join([create_trip(l, time_increment) for l in locations_on_sim])
        headcode = headcode_template[:2] + f"{int(headcode_template[2:]) + (headcode_increment * i):02d}"
        uid = headcode
        AccelBrakeIndex = train_cat_dict['AccelBrakeIndex']
        DepartTime = str(entry_time + time_increment)
        description = str(origin_time) + origin + dest + train_category
        MaxSpeed = train_cat_dict['MaxSpeed']
        IsFreight = train_cat_dict['IsFreight']
        TrainLength = train_cat_dict['TrainLength']
        Electrification = 'D'
        OriginName = origin
        DestinationName = dest
        OriginTime = str(convert_time_to_secs(origin_time) + time_increment)
        DestinationTime = str(convert_time_to_secs(dest_time) + time_increment)
        OperatorCode = 'GW'
        StartTraction = 'D'
        Category = train_cat_dict['id']

        list_of_timetables.append(
            tt_template.replace('${ID}', headcode).replace('${UID}', uid).replace('${AccelBrakeIndex}', AccelBrakeIndex) \
            .replace('${DepartTime}', DepartTime).replace('${Description}', description).replace('${EntryPoint}',
                                                                                                 entry_point) \
            .replace('${MaxSpeed}', MaxSpeed).replace('${isFreight}', IsFreight).replace('${TrainLength}', TrainLength) \
            .replace('${Electrification}', Electrification).replace('${OriginName}', OriginName).replace(
                '${DestinationName}', DestinationName) \
            .replace('${OriginTime}', OriginTime).replace('${DestinationTime}', DestinationTime).replace(
                '${OperatorCode}', OperatorCode).replace('${StartTraction}', StartTraction) \
            .replace('${Category}', Category).replace('${Trips}', trips))

    with open('testfile.xml', 'w') as f_to_write:
        for tt in list_of_timetables:
            print(tt, file=f_to_write)


create_timetable_with_spec_entry('1A01', 2, '1A01_locations.txt', 'swindon_locations.txt', 'defaultTimatableWithEntryPoint.txt', 'EUPBAD', 3600, 10, 'IEP 800/3 - Bi Mode - 9 Car')
