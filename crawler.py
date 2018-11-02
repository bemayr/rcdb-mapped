from bs4 import BeautifulSoup
import urllib.request
import re


coo_matcher = re.compile(r'maps.here.com\/\?map=(\-?\d{1,2}\.\d*),(\-?\d{1,3}\.\d*),\d.*')

#
# Basic Coster content store
#
class NewCoster:
    lat = 0
    lng = 0
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


#
# parse for coster from rcdb
#
def parse_coster(url) -> NewCoster:

    with urllib.request.urlopen(url) as main:
        soup = BeautifulSoup(main, 'html.parser')
        coster = NewCoster()

        # extract lat & lng
        if len(soup.find_all(href=coo_matcher)) > 0:
            coor = coo_matcher.search(soup.find_all(href=coo_matcher).pop().get('href'))
            coster.lat = coor.group(1)
            coster.lng = coor.group(2)

        main_info = soup.find(id='feature')
        content = main_info.find_all('a')

        # set main info
        coster.name = main_info.find('h1').text
        coster.owner = content[0].text
        coster.city = content[1].text
        coster.region = content[2].text
        coster.country = content[3].text

        # TODO extract status

        content = main_info.find('span').find_all('a')

        # set additional info
        coster.type = content[0].text
        coster.main_material = content[1].text
        coster.drive_type = content[2].text

        content = main_info.select('div.scroll')[1].find_all('a')

        # set manufacturer
        coster.manufacturer = content[0].text

        return coster
