from timetableCreator import create_timetable_with_spec_entry, create_tts_file
from translateTimesAndLocations import convert_sec_to_time, convert_time_to_secs
import yaml



def sub_in_defaults_etc(timetable, defaults, baseFilePaths):
    for default in defaults.keys():
        if default not in timetable:
            timetable[default] = defaults[default]

    for baseFilePath in baseFilePaths.keys():
        timetable[baseFilePath] = baseFilePaths[baseFilePath] + timetable[baseFilePath]

    return timetable

def build_list_of_tts(config_file_location: str, ouput_filename: str):
    with open(config_file_location, 'r') as stream:
        yaml_data = yaml.safe_load(stream)

    tt_list_for_file = []

    for timetable in yaml_data['timetables']:
        print('Building for ' + timetable['headcode_template'])
        tt_list_for_file.append(create_timetable_with_spec_entry(sub_in_defaults_etc(timetable, yaml_data['defaults'], yaml_data['baseFilePaths'])))

    create_tts_file(tt_list_for_file, ouput_filename)

build_list_of_tts('simsig_timetables/swindid_diversions_feb_21/swiDiversionsFeb21.yaml', 'testyamlconf.xml')

# Parse yaml


# Sub out defaults in each dict

# Input into create_timetable_with_spec_entry

# Put the big list in 1 file
