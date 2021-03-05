"""
For building up a list of train TTs to insert into a Simsig xml TT.
"""
from jsonTimetableCreator import create_json_timetables_with_spec_entry
from dbClient import *
import yaml


# Subs in the defined defaults in the yaml tt spec.
def sub_in_defaults_etc(timetable, defaults, baseFilePaths):
    for default in defaults.keys():
        if default not in timetable:
            timetable[default] = defaults[default]

    for baseFilePath in baseFilePaths.keys():
        timetable[baseFilePath] = baseFilePaths[baseFilePath] + timetable[baseFilePath]

    return timetable


def build_list_of_tts(config_file_location: str, tt_name: str, overwrite_old_tts: bool):
    """
    Will take a yaml file containing a spec for multiple TTs and create json TTs for each one and then store them in.

    :param config_file_location: Filepath for yaml config.
    :param tt_name: Name of TT that will indicate where json TTs will be stored.
    :param overwrite_old_tts: Do we want to overwrite any TTs already present in the db.
    """
    with open(config_file_location, 'r') as stream:
        yaml_data = yaml.safe_load(stream)

    json_tt_list_for_file = []

    for timetable in yaml_data['timetables']:
        print('Building json TT for ' + timetable['headcode_template'])
        for tt in create_json_timetables_with_spec_entry(sub_in_defaults_etc(timetable, yaml_data['tt_defaults'], yaml_data['baseFilePaths'])):
            json_tt_list_for_file.append(tt)

    tt_db = TrainTtDb(tt_name)

    if overwrite_old_tts is True:
        for tt in json_tt_list_for_file:
            tt_db.add_tt(tt)
    else:
        for tt in json_tt_list_for_file:
            tt_db.add_tt_if_not_present(tt)
