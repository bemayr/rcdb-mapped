import sys

import requests
import base64
import json
import geopy
from geopy.geocoders import Nominatim
import pickle
from random import randint
from time import sleep
from tqdm import tqdm

from scrape import to_base64, update_gist, create_gist_response_message


def from_base64(costers) -> str:
    return base64.urlsafe_b64decode(costers).decode('utf-8')


class LocNotFound(Exception):
    pass


def get_location(a: dict, geolocator: Nominatim) -> geopy.location.Location:

    sleep(randint(1, 2))
    location = geolocator.geocode(f'{a["city"]}, {a["region"]}, {a["country"]}')
    if location:
        return location

    sleep(randint(1, 2))
    location = geolocator.geocode(f'{a["city"]}, {a["country"]}')
    if location:
        return location

    sleep(randint(1, 2))
    location = geolocator.geocode(f'{a["city"]}')
    if location:
        return location

    print(f'GEO: nothing found {a}')
    raise LocNotFound("GEO: location not found")


def update_and_dump():
    f = open('coasters.json', 'rb')
    data = from_base64(f.read())
    d = json.loads(data)
    f.close()

    geolocator = Nominatim(user_agent="Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:65.0) Gecko/20100101 Firefox/65.0")

    updated = []

    for t in tqdm(d['features']):
        if t['geometry']['coordinates'][0] == 0:

            a = t['properties']

            while t['geometry']['coordinates'][0] == 0:
                try:
                    location = get_location(a, geolocator)
                    t['geometry']['coordinates'][0] = location.longitude
                    t['geometry']['coordinates'][1] = location.latitude
                except LocNotFound as lnf:
                    print(lnf)
                    break
                except:
                    print(sys.exc_info()[0])
                    continue

        updated.append(t)

    update_pack = {'type': 'FeatureCollection', 'features': updated}

    with open('data.json', 'w') as outfile:
        json.dump(update_pack, outfile)

    return update_pack


if __name__ == "__main__":
    # res = update_and_dump()
    # coasters = json.dumps(res)

    with open('data.json', 'r') as infile:
        coasters = json.load(infile)
    ready_to_update = to_base64(json.dumps(coasters))
    with open('dump_base64.pkl', 'wb') as du:
        pickle.dump(ready_to_update, du)

    response = update_gist(ready_to_update)
    print(create_gist_response_message(response))
