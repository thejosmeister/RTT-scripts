import yaml
import isodate
import re
from tinydb import Query, TinyDB
from translateTimesAndLocations import convert_time_to_secs
import hashlib
from dbClient import *

# db = TinyDB('db/db.json')
# db.drop_tables()
# add_tt(db, {'uid': '1F99'})
# add_tt(db, {'uid': '1X99'})
# add_tt(db, {'uid': '2Z99'})
# add_tt(db, {'uid': '1F01'})
# add_tt(db, {'uid': '2X46'})
# add_tt_if_not_present(db, {'uid': '1F99'})
# add_tt_if_not_present(db, {'uid': '1A01'})
# put_tt_by_uid(db, '1F99', {'uid': '1F99', 'a': 'b'})
# add_tt(db, {'uid': '1F99'})
# patch_tt_by_uid(db, '1F99', {'VAL3': 12})
# print(get_tt_by_uid(db, '1A01'))
# print(db.all())
# print(return_uids_from_query(db, Query().uid == '1F01'))
# print(db.get(doc_id=1))

db = TrainTtDb('Swindon_A_&_B_IECC_-_SWINDID_130220')
TT = Query()
Location = Query()
results = db.db.search(TT.locations.any(Location.location == 'Didcot East Jn') & TT.locations.any(Location.location == 'Didcot North Jn') & TT.headcode.matches('^((0|4|5|6).)\\d{2}$'))

new_r = []
for r in results:
    time = [x for x in r['locations'] if x['location'] == 'Didcot East Jn' ][0]['dep']
    new_r.append({'headcode': r['headcode'], 'description': r['description'], 'time': time})

new_r = sorted(new_r, key=lambda x: float(x['time']))

[print(r['headcode'] + ' ' + r['description'] + ' ' + r['time']) for r in new_r]

print('***************************************************************************')


db = TrainTtDb('Swindon_February_2021')
TT = Query()
Location = Query()
results = db.db.search(TT.locations.any(Location.location == 'Didcot East Jn') & TT.locations.any(Location.location == 'Didcot North Jn') & TT.headcode.matches('^((0|4|5|6).)\\d{2}$'))

new_r = []
for r in results:
    time = [x for x in r['locations'] if x['location'] == 'Didcot East Jn' ][0]['dep']
    new_r.append({'headcode': r['headcode'], 'description': r['origin_time'] + ' ' + r['origin_name'] + ' - ' + r['destination_name'], 'time': time})

new_r = sorted(new_r, key=lambda x: float(x['time']))

[print(r['headcode'] + ' ' + r['description'] + ' ' + r['time']) for r in new_r]

# for r in results:
#     if 'entry_time' in r:
#         print(r['entry_time'] + ' entry time ' + r['headcode'])
#     else:
#         print(r['headcode'])
#         print(r['locations'][-1])

#
# TT = Query()
# Location = Query()
#
# result = db.search(TT.locations.any((Location.location == 'Challow') & (Location.dep.matches('08\\d{2}') )))
#
# for tt in result:
#     print( tt['headcode'] + str(tt['locations'][0]) )


