#!/usr/bin/python3

from bs4 import BeautifulSoup
import json
import urllib.request
import re

from config import urls

coo_matcher = re.compile(r'maps.here.com\/\?map=(-?\d{1,2}\.\d*),(-?\d{1,3}\.\d*),\d.*')


#
# Basic Coster content store
#
class Coaster:
    id = 0
    lat = 0.
    lng = 0.
    name = ''
    owner = ''
    city = ''
    region = ''
    country = ''
    status = ''
    type = ''
    main_material = ''
    drive_type = ''
    manufacturer = ''

    def __init__(self, id):
        super().__init__()
        self.id = id

    def __str__(self):
        return json.dumps(self.to_json(), cls=CoasterEncoder)

    def to_json(self):
        return {'type': 'Feature',
                'geometry': {'type': 'Point', 'coordinates': (float(self.lng), float(self.lat))},
                'properties': self.__dict__ }


#
# Helper to Convert Coaster to JSON
#
class CoasterEncoder(json.JSONEncoder):
    def default(self, o: Coaster):
        return o.to_json()


def item_url_builder(id: int) -> str:
    return f"{urls['coasters']['base']}/{id}.htm"


#
# parse for coster from rcdb
#
def parse_coaster(id) -> Coaster:
    with urllib.request.urlopen(item_url_builder(id)) as main:
        soup = BeautifulSoup(main, 'html.parser')

        # try to find Parks which is not a coaster
        if soup.find(id='feature').select('span.link_row')[0].getText().count('Parks nearby') > 0:
            return None

        coaster = Coaster(id)

        # extract lat & lng
        if len(soup.find_all(href=coo_matcher)) > 0:
            coor = coo_matcher.search(soup.find_all(href=coo_matcher).pop().get('href'))
            coaster.lat = coor.group(1)
            coaster.lng = coor.group(2)

        main_info = soup.find(id='feature')
        content = main_info.find_all('a')

        # set main info
        coaster.name = main_info.find('h1').text
        # try to find Amusement parks which are no coasters
        if coaster.name.count('Amusement') > 0:
            return None

        coaster.owner = content[0].text
        coaster.city = content[1].text
        coaster.region = content[2].text
        coaster.country = content[3].text

        # TODO extract status

        content = main_info.find('span').find_all('a')
        # set additional info
        coaster.type = content[0].text
        coaster.main_material = content[1].text
        coaster.drive_type = content[2].text

        content = main_info.select('div.scroll')
        if len(content) > 1:
            content = content[1].find_all('a')
            # set manufacturer
            coaster.manufacturer = content[0].text

        return coaster


def extract_coasters(ids: []) -> dict:
    return {'type': 'FeatureCollection', 'features': list(filter(lambda x: x is not None, [parse_coaster(i) for i in ids]))}


if __name__ == "__main__":
    # bad: 5537
    # good: 1823, 3111
    tmp = parse_coaster(3111)
    print(json.dumps(tmp, cls=CoasterEncoder, indent=4))
    print(tmp)
