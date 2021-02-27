from timetableCreator import create_timetable_with_spec_entry, create_tts_file
from translateTimesAndLocations import convert_sec_to_time, convert_time_to_secs

tt_list_for_file = []

# The 1Axx
tt_list_for_file.append(create_timetable_with_spec_entry('1A01', 3, 'SWI_KEY_locations/1A01_KEY_locations.txt', 'swindon_locations.txt', 'templates/timetables/defaultTimetableWithEntryPoint.txt', 'EUPBAD', 3600, 2, 'IEP 800/3 - Bi Mode - 9 Car', 0, None))
tt_list_for_file.append(create_timetable_with_spec_entry('1A12', 2, 'SWI_KEY_locations/1A01_KEY_locations.txt', 'swindon_locations.txt', 'templates/timetables/defaultTimetableWithEntryPoint.txt', 'EUPBAD', 3600, 11, 'IEP 800/3 - Bi Mode - 9 Car', 7200, None))
tt_list_for_file.append(create_timetable_with_spec_entry('1A33', 2, 'SWI_KEY_locations/1A01_KEY_locations.txt', 'swindon_locations.txt', 'templates/timetables/defaultTimetableWithEntryPoint.txt', 'EUPBAD', 3600, 3, 'IEP 800/3 - Bi Mode - 9 Car', int(13.5*3600), None))
tt_list_for_file.append(create_timetable_with_spec_entry('1A40', 2, 'SWI_KEY_locations/1A01_KEY_locations.txt', 'swindon_locations.txt', 'templates/timetables/defaultTimetableWithEntryPoint.txt', 'EUPBAD', 3600, 1, 'IEP 800/3 - Bi Mode - 9 Car', int(17*3600) + 15*60, None))

# 1Hxx
tt_list_for_file.append(create_timetable_with_spec_entry('1H02', 2, 'SWI_KEY_locations/1H02_KEY_locations.txt', 'swindon_locations.txt', 'templates/timetables/defaultTimetableWithEntryPoint.txt', 'EDNMAIN', 3600, 11, 'IEP 800/0 - Bi Mode -10 Car', 0, None))
tt_list_for_file.append(create_timetable_with_spec_entry('1H25', 3, 'SWI_KEY_locations/1H02_KEY_locations.txt', 'swindon_locations.txt', 'templates/timetables/defaultTimetableWithEntryPoint.txt', 'EDNMAIN', 3600, 3, 'IEP 800/0 - Bi Mode -10 Car', 11*3600 - 3*60, None))
tt_list_for_file.append(create_timetable_with_spec_entry('1H33', 3, 'SWI_KEY_locations/1H02_KEY_locations.txt', 'swindon_locations.txt', 'templates/timetables/defaultTimetableWithEntryPoint.txt', 'EDNMAIN', 3600, 1, 'IEP 800/0 - Bi Mode -10 Car', 14*3600, None))
tt_list_for_file.append(create_timetable_with_spec_entry('1U36', 1, 'SWI_KEY_locations/1H02_KEY_locations.txt', 'swindon_locations.txt', 'templates/timetables/defaultTimetableWithEntryPoint.txt', 'EDNMAIN', 3600, 2, 'IEP 800/0 - Bi Mode -10 Car', 15*3600 + 33*60, None))

# 1Lxx swansea
tt_list_for_file.append(create_timetable_with_spec_entry('1L01', 4, 'SWI_KEY_locations/1L01_KEY_locations.txt', 'swindon_locations.txt', 'templates/timetables/defaultTimetableWithEntryPoint.txt', 'EUPBAD', 3600, 1, 'IEP 800/3 - Bi Mode - 9 Car', 0, None))
tt_list_for_file.append(create_timetable_with_spec_entry('1L04', 4, 'SWI_KEY_locations/1L04_KEY_locations.txt', 'swindon_locations.txt', 'templates/timetables/defaultTimetableWithEntryPoint.txt', 'EUPBAD', 3660, 2, 'IEP 800/3 - Bi Mode - 9 Car', 0, None))
tt_list_for_file.append(create_timetable_with_spec_entry('1L10', 4, 'SWI_KEY_locations/1L04_KEY_locations.txt', 'swindon_locations.txt', 'templates/timetables/defaultTimetableWithEntryPoint.txt', 'EUPBAD', 3600, 13, 'IEP 800/3 - Bi Mode - 9 Car', 2*3600 + 60, None))

# 1Bxx

# 1Lxx cnm

# 1Gxx

# 1Txx
tt_list_for_file.append(create_timetable_with_spec_entry('1T99', 4, 'SWI_KEY_locations/1T99_KEY_locations.txt', 'swindon_locations.txt', 'templates/timetables/defaultTimetableWithEntryPoint.txt', 'EUPMAIN', 3600, 1, 'IEP 800/3 - Bi Mode - 9 Car', 0, None))
tt_list_for_file.append(create_timetable_with_spec_entry('3T01', 4, 'SWI_KEY_locations/3T01_KEY_locations.txt', 'swindon_locations.txt', 'templates/timetables/defaultTimetableNoEP.txt', None, 3600, 1, 'IEP 800/3 - Bi Mode - 9 Car', 0, None))
tt_list_for_file.append(create_timetable_with_spec_entry('3T00', 0, 'SWI_KEY_locations/3T00_KEY_locations.txt', 'swindon_locations.txt', 'templates/timetables/defaultTimetableWithEntryPoint.txt','EUPBAD', 3600, 1, 'IEP 800/0 - Bi Mode - 5 Car', 0, None))
tt_list_for_file.append(create_timetable_with_spec_entry('1T00', 4, 'SWI_KEY_locations/1T00_KEY_locations.txt', 'swindon_locations.txt', 'templates/timetables/defaultTimetableNoEP.txt', None, 7200, 1, 'IEP 800/0 - Bi Mode - 5 Car', 0, None))
# 1T04 - 1T24
tt_list_for_file.append(create_timetable_with_spec_entry('1T04', 4, 'SWI_KEY_locations/1T00_KEY_locations.txt', 'swindon_locations.txt', 'templates/timetables/defaultTimetableNoEP.txt', None, 7200, 6, 'IEP 800/0 - Bi Mode - 5 Car', 3600 + 49*60, None))
# 1T02 - 1T26
tt_list_for_file.append(create_timetable_with_spec_entry('1T02', 4, 'SWI_KEY_locations/1T00_KEY_locations.txt', 'swindon_locations.txt', 'templates/timetables/defaultTimetableNoEP.txt', None, 7200, 7, 'IEP 800/3 - Bi Mode - 9 Car', 49*60, None))
# 1T01 - 1T25
tt_list_for_file.append(create_timetable_with_spec_entry('1T01', 4, 'SWI_KEY_locations/1T01_KEY_locations.txt', 'swindon_locations.txt', 'templates/timetables/defaultTimetableWithEntryPoint.txt', 'EUPMAIN', 7200, 7, 'IEP 800/3 - Bi Mode - 9 Car', 0, None))
# 1T03 - 1T23
tt_list_for_file.append(create_timetable_with_spec_entry('1T03', 4, 'SWI_KEY_locations/1T01_KEY_locations.txt', 'swindon_locations.txt', 'templates/timetables/defaultTimetableWithEntryPoint.txt', 'EUPMAIN', 7200, 6, 'IEP 800/0 - Bi Mode - 5 Car', 3600, None))
# 1t27 arr swi 2114 -> 1g31 dep swi 2132,
tt_list_for_file.append(create_timetable_with_spec_entry('1T27', 4, 'SWI_KEY_locations/1T01_KEY_locations.txt', 'swindon_locations.txt', 'templates/timetables/defaultTimetableWithEntryPoint.txt', 'EUPMAIN', 7200, 1, 'IEP 800/3 - Bi Mode - 9 Car', 13*3600, '1G31+0+0'))
# CREATE 1G31

# 3t38 arr swi 2156 -> 1t28 dep swi 2202,
tt_list_for_file.append(create_timetable_with_spec_entry('3T38', 0, 'SWI_KEY_locations/3T00_KEY_locations.txt', 'swindon_locations.txt', 'templates/timetables/defaultTimetableWithEntryPoint.txt','EUPBAD', 3600, 1, 'IEP 800/0 - Bi Mode - 5 Car', convert_time_to_secs('2156') - convert_time_to_secs('0738'), '1T28+0+0'))
tt_list_for_file.append(create_timetable_with_spec_entry('1T28', 4, 'SWI_KEY_locations/1T00_KEY_locations.txt', 'swindon_locations.txt', 'templates/timetables/defaultTimetableNoEP.txt', None, 7200, 1, 'IEP 800/0 - Bi Mode - 5 Car', 13*3600 + 49*60 + 17*60, None))

# 1t29 arr swi p1 2235 -> 5t04
# 1t31 arr swi p1 2320 -> 5t05

# 1Fxx pompey harbours
# 2b62 -> 1f05
tt_list_for_file.append(create_timetable_with_spec_entry('2B62', 0, 'SWI_KEY_locations/2B62_KEY_locations.txt', 'swindon_locations.txt', 'templates/timetables/defaultTimetableWithEntryPoint.txt','EUPKEMB', 3600, 1, 'Cl 165/3', 0, None))
# 5f07 -> 1f07
tt_list_for_file.append(create_timetable_with_spec_entry('5F07', 0, 'SWI_KEY_locations/5F07_KEY_locations.txt', 'swindon_locations.txt', 'templates/timetables/defaultTimetableWithEntryPoint.txt','EUPBAD', 3600, 1, 'Cl 165/3', 0, None))
# 1f to pompey 1f05 to 1f19
tt_list_for_file.append(create_timetable_with_spec_entry('1F05', 2, 'SWI_KEY_locations/1F05_KEY_locations.txt', 'swindon_locations.txt', 'templates/timetables/defaultTimetableNoEP.txt', None, 3600, 8, 'Cl 165/3', 0, None))
# 1f to pompey 1f21 to 1f23 at 21 past the hour
tt_list_for_file.append(create_timetable_with_spec_entry('1F21', 2, 'SWI_KEY_locations/1F05_KEY_locations.txt', 'swindon_locations.txt', 'templates/timetables/defaultTimetableNoEP.txt', None, 3600, 2, 'Cl 165/3', 8*3600 - 3*60, None))
# 1f to pompey 1f25 to 1f33 at 24 past the hour
tt_list_for_file.append(create_timetable_with_spec_entry('1F25', 2, 'SWI_KEY_locations/1F05_KEY_locations.txt', 'swindon_locations.txt', 'templates/timetables/defaultTimetableNoEP.txt', None, 3600, 5, 'Cl 165/3', 10*3600, None))

# 1f coming up from pompey
# 1f06 to 1f30
tt_list_for_file.append(create_timetable_with_spec_entry('1F06', 2, 'SWI_KEY_locations/1F06_KEY_locations.txt', 'swindon_locations.txt', 'templates/timetables/defaultTimetableWithEntryPoint.txt','EDNTROW', 3600, 13, 'Cl 165/3', 0, None))
# 1f32 arr swi 2152 -> 5f32 dep 2207
tt_list_for_file.append(create_timetable_with_spec_entry('1F32', 0, 'SWI_KEY_locations/1F06_KEY_locations.txt', 'swindon_locations.txt', 'templates/timetables/defaultTimetableWithEntryPoint.txt','EDNTROW', convert_time_to_secs('2152') - convert_time_to_secs('0854'), 1, 'Cl 165/3', 0, '5F32+0+0'))
tt_list_for_file.append(create_timetable_with_spec_entry('5F32', 0, 'SWI_KEY_locations/5F32_KEY_locations.txt', 'swindon_locations.txt', 'templates/timetables/defaultTimetableNoEP.txt', None, 3600, 1, 'Cl 165/3', 0, None))



create_tts_file(tt_list_for_file, 'biglist.xml')
