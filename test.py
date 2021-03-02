import yaml
import isodate
import re
from tinydb import Query, TinyDB
from translateTimesAndLocations import convert_time_to_secs

db = TinyDB('db/db.json')

TT = Query()
Location = Query()

result = db.search(TT.locations.any((Location.location == 'Challow') & (Location.dep.matches('08\\d{2}') )))

for tt in result:
    print( tt['headcode'] + str(tt['locations'][0]) )

