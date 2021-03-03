"""
For building up a list of train TTs to insert into a Simsig xml TT.
"""
from jsonTimetableCreator import create_json_timetables_with_spec_entry
from xmlTimetableCreator import convert_individual_json_tt_to_xml
from tinydb import TinyDB
from dbClient import *
import yaml


# Creates the file that we write the list of TTs to.
def create_xml_tt_list_file(list_of_tts: list, filename: str):
    with open(filename, 'w') as f_to_write:
        for tt in list_of_tts:
            print(tt, file=f_to_write)


def build_xml_list_of_tts(tt_name: str, output_filename: str, sim_locations_file: str):
    """
    Takes a db with json train TTs and creates an xml file with a list of all those TTs.
    This will not add any of the other stuff that goes into a Simsig xml TT.

    :param tt_name: Name of tt, used to find db file.
    :param output_filename: Name of xml file with TTs that is created.
    :param sim_locations_file: Name of file containing TIPLOC map on sim locations
    """

    tt_db = get_train_tt_db(tt_name)
    xml_tts = []

    for tt in get_all_in_db(tt_db):
        print('Building xml TT for ' + tt['uid'])
        xml_tts.append(convert_individual_json_tt_to_xml(tt, 'sim_location_files/' + sim_locations_file))

    create_xml_tt_list_file(xml_tts, output_filename)
