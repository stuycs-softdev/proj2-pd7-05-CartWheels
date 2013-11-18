import urllib2
import json
from models import Cart

carts = Cart()
carts.remove_all()
host = 'http://data.cityofnewyork.us/resource/xfyi-uyt5.json'
for i in range(0, 7000, 1000):
    query = 'permit_type_description=MOBILE+FOOD+UNIT&$offset=%d' % i
    request = host + '?' + query
    data = urllib2.urlopen(host + '?' + query) 

    results = json.loads(data.read())
    data.close()
    for r in results:
        if not r.has_key('longitude_wgs84'):
            r['longitude_wgs84'] = 'UNKNOWN'
        if not r.has_key('latitude_wgs84'):
            r['latitude_wgs84'] = 'UNKNOWN'
        if not r.has_key('street'):
            r['street'] = 'UNKNOWN'
        if not r.has_key('address'):
            r['address'] = 'UNKNOWN'
        if not r.has_key('zip_code'):
            r['zip_code'] = 'UNKNOWN'
        if not r.has_key('borough'):
            r['borough'] = 'UNKNOWN'
        if not r.has_key('license_permit_holder'):
            r['license_permit_holder'] = 'UNKNOWN'
    
        carts.insert(lat=r['latitude_wgs84'], lng=r['longitude_wgs84'], 
                street=r['street'], address=r['address'],
                zip_code=r['zip_code'], borough=r['borough'], 
                owner=r['license_permit_holder'])


out = [c for c in carts.find()]
print len(out)
