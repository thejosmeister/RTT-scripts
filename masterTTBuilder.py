from jsonTimetableListBuilder import build_list_of_tts
from xmlTimetableBuilder import build_xml_list_of_tts


def build_complete_tt(tt_name: str, locations_filename: str, xml_output_filename: str, overwrite_existing_trains: bool):
    build_list_of_tts('simsig_timetables/{}/{}.yaml'.format(tt_name, tt_name), tt_name, overwrite_existing_trains)
    build_xml_list_of_tts(tt_name, xml_output_filename, locations_filename)



def build_xml_tt_list_from_spec(tt_name: str, locations_filename: str, xml_output_filename: str,
                                overwrite_existing_trains: bool):

    build_list_of_tts('simsig_timetables/{}/{}.yaml'.format(tt_name, tt_name), tt_name, overwrite_existing_trains)
    build_xml_list_of_tts(tt_name, xml_output_filename, locations_filename)


build_xml_tt_list_from_spec('swindid_diversions_feb_21', 'swindon_locations.txt', 'ttlist.xml', True)
