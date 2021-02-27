
def pull_tiploc_out_of_xml():
    entry_points = []
    locations = []
    f = open('SavedTimetable.xml', "r")
    for file_line in f:
        if 'EntryPoint' in file_line:
            entry_points.append(file_line.split('<EntryPoint>')[1].split('</EntryPoint>')[0])
        if 'Location' in file_line:
            locations.append(file_line.split('<Location>')[1].split('</Location>')[0])

    f.close()

    set_of_entry_points = set(entry_points)
    set_of_locations = set(locations)

    with open('swindon_locations.txt', mode='w') as emails_file:
        print('Entry Points: ', file=emails_file)
        for e in set_of_entry_points:
            print(e, file=emails_file)
        print(' ', file=emails_file)
        print('Locations: ', file=emails_file)
        for e in set_of_locations:
            print(e, file=emails_file)


def pull_train_categories_out_of_xml() -> dict:
    f = open('TrainCategories.xml', "r")
    categories_dict = {}
    _id = ''
    description = ''
    dwell_times = False
    for file_line in f:
        if '<TrainCategory' in file_line:
            _id = file_line.split('"')[1]
        elif 'Description' in file_line:
            description = file_line.split('<Description>')[1].split('</Description>')[0]
            categories_dict[description] = { 'id': _id }
        elif 'AccelBrakeIndex' in file_line:
            categories_dict[description]['AccelBrakeIndex'] = file_line.split('<AccelBrakeIndex>')[1].split('</AccelBrakeIndex>')[0]
        elif 'IsFreight' in file_line:
            categories_dict[description]['IsFreight'] = file_line.split('<IsFreight>')[1].split('</IsFreight>')[0]
        elif 'CanUseGoodsLines' in file_line:
            categories_dict[description]['CanUseGoodsLines'] = file_line.split('<CanUseGoodsLines>')[1].split('</CanUseGoodsLines>')[0]
        elif 'MaxSpeed' in file_line:
            categories_dict[description]['MaxSpeed'] = file_line.split('<MaxSpeed>')[1].split('</MaxSpeed>')[0]
        elif 'TrainLength' in file_line:
            categories_dict[description]['TrainLength'] = file_line.split('<TrainLength>')[1].split('</TrainLength>')[0]
        elif 'SpeedClass' in file_line:
            categories_dict[description]['SpeedClass'] = file_line.split('<SpeedClass>')[1].split('</SpeedClass>')[0]
        elif 'PowerToWeightCategory' in file_line:
            categories_dict[description]['PowerToWeightCategory'] = file_line.split('<PowerToWeightCategory>')[1].split('</PowerToWeightCategory>')[0]
        elif '<DwellTimes' in file_line:
            if 'DwellTimes/' not in file_line:
                categories_dict[description]['DwellTimes'] = {}
                dwell_times = True
                continue
        elif dwell_times is True:
            if 'Join' in file_line:
                categories_dict[description]['DwellTimes']['Join'] = file_line.split('<Join>')[1].split('</Join>')[0]
            elif 'Divide' in file_line:
                categories_dict[description]['DwellTimes']['Divide'] = file_line.split('<Divide>')[1].split('</Divide>')[0]
            elif 'CrewChange' in file_line:
                categories_dict[description]['DwellTimes']['CrewChange'] = file_line.split('<CrewChange>')[1].split('</CrewChange>')[0]
                dwell_times = False
        elif 'Electrification' in file_line:
            categories_dict[description]['Electrification'] = file_line.split('<Electrification>')[1].split('</Electrification>')[0]

    return categories_dict


def create_tiploc_dict(file_location: str) -> list:
    tiploc_locations = {}
    entry_points = {}
    is_entry_points = False
    is_locations = False
    f = open(file_location, "r")
    for file_line in f:
        if 'Entry Points' in file_line:
            is_entry_points = True
            is_locations = False
            continue
        elif 'Locations' in file_line:
            is_entry_points = False
            is_locations = True
            continue
        elif is_entry_points == True:
            code = file_line.rstrip().split(':')[0]
            names = file_line.rstrip().split(':')[1].split(',')
            entry_points[code] = names
        elif is_locations == True:
            code = file_line.rstrip().split(':')[0]
            names = file_line.rstrip().split(':')[1].split(',')
            tiploc_locations[code] = names

    return [entry_points, tiploc_locations]


d = pull_train_categories_out_of_xml()
print(d)

# [e,l] = create_tiploc_dict('swindon_locations.txt')
#
# print(e)
# print(l)
