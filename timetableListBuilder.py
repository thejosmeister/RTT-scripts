"""
For building up a list of train TTs to insert into a Simsig xml TT.
"""
from jsonTimetableCreator import create_json_timetables_with_spec_entry
from xmlTimetableCreator import convert_individual_json_tt_to_xml
from tinydb import TinyDB
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
def create_tts_file(list_of_tts: list, filename: str):
    with open(filename, 'w') as f_to_write:
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

    json_tt_list_for_file = []
    xml_tts = []

    for timetable in yaml_data['timetables']:
        print('Building json TT for ' + timetable['headcode_template'])
        for tt in create_json_timetables_with_spec_entry(sub_in_defaults_etc(timetable, yaml_data['defaults'], yaml_data['baseFilePaths'])):
            json_tt_list_for_file.append(tt)

    db = TinyDB('db/db.json')
    db.insert_multiple(json_tt_list_for_file)

    for tt in json_tt_list_for_file:
        print('Building xml TT for ' + tt['uid'])
        xml_tts.append(convert_individual_json_tt_to_xml(tt, 'sim_location_files/swindon_locations.txt'))

    create_tts_file(xml_tts, ouput_filename)


build_list_of_tts('simsig_timetables/swindid_diversions_feb_21/swiDiversionsFeb21.yaml', 'testyamlconf.xml')
