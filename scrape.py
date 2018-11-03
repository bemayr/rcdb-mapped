#!/usr/bin/python3

import requests
from bs4 import BeautifulSoup

from config import urls, gist
from coaster_parser import extract_coasters, CoasterEncoder


# functions
def get_max_page_number() -> int:
    return int(max([pagelink.get_text()
            for pagelink
            in BeautifulSoup(requests.get(urls["coasters"]["index"]).content, "html.parser").find(id="rfoot").find_all("a")
            if pagelink.get_text().isnumeric()]))


def get_coaster_ids(max_page_number) -> [int]:
    return [entry.find_all("a")[1].get("href")[1:].split(".")[0]
            for page_number
            in range(1, max_page_number)
            for entry
            in BeautifulSoup(requests.get(urls["coasters"]["page"] + str(page_number)).content, "html.parser").select("#report tbody")[0].find_all("tr")]


def read_gist_token() -> str:
    with open('GIST_TOKEN', 'r') as token_file:
        return token_file.read().rstrip()


def update_gist(coasters):
    return requests.patch(f'{gist["url"]}{gist["id"]}', headers={"Authorization": f'token {read_gist_token()}'},
                          data=gist["template"] % coasters)


def create_gist_response_message(response) -> str:
    return f'Yay, the coasters have been updated successfully! ({response.url})' if response.ok else f'Oh noooo, something unexpected happened: {response.status_code}, {response.reason}'


def main():
    print("Counting all the coasters...")
    max_page_number = get_max_page_number()
    coaster_ids = get_coaster_ids(max_page_number)
    print("Riding all the coasters to get the necessary information...")
    coasters = extract_coasters(coaster_ids)  # replace with David's code
    # coasters to JSON via `json.dumps(coasters, cls=CoasterEncoder)`
    # or via `print(coaster)`
    print("Storing the data in the cloud")
    response = update_gist(coasters)
    print(create_gist_response_message(response))


if __name__ == "__main__":
    main()
