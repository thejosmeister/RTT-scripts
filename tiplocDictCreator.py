
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

# [e,l] = create_tiploc_dict('swindon_locations.txt')
#
# print(e)
# print(l)
