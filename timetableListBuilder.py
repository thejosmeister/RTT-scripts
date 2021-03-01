"""
For building up a list of train TTs to insert into a Simsig xml TT.
"""
from timetableCreator import create_timetable_with_spec_entry
import yaml


# Subs in the defined defaults in the yaml tt spec.
def sub_in_defaults_etc(timetable, defaults, baseFilePaths):
    for default in defaults.keys():
        if default not in timetable:
            timetable[default] = defaults[default]

    for baseFilePath in baseFilePaths.keys():
        timetable[baseFilePath] = baseFilePaths[baseFilePath] + timetable[baseFilePath]

    return timetable


# Creates the file that we write the list of TTs to.
def create_tts_file(list_of_lists_of_tts: list, filename: str):
    with open(filename, 'w') as f_to_write:
        for list_of_tts in list_of_lists_of_tts:
            for tt in list_of_tts:
                print(tt, file=f_to_write)


def build_list_of_tts(config_file_location: str, ouput_filename: str):
    """
    Will take a yaml file containing a spec for multiple TTs and create an xml file with a list of all those TTs.
    This will not add any of the other stuff that goes into a Simsig xml TT.

    :param config_file_location: Filepath for yaml config.
    :param ouput_filename: Name of xml file with TTs that is created.
    """
    with open(config_file_location, 'r') as stream:
        yaml_data = yaml.safe_load(stream)

    tt_list_for_file = []

    for timetable in yaml_data['timetables']:
        print('Building for ' + timetable['headcode_template'])
        tt_list_for_file.append(create_timetable_with_spec_entry(sub_in_defaults_etc(timetable, yaml_data['defaults'], yaml_data['baseFilePaths'])))

    create_tts_file(tt_list_for_file, ouput_filename)


build_list_of_tts('simsig_timetables/swindid_diversions_feb_21/swiDiversionsFeb21.yaml', 'testyamlconf.xml')
