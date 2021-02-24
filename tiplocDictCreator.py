
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



pull_tiploc_out_of_xml()

