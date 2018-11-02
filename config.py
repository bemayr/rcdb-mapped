#!/usr/bin/python3

urls = {
    "coasters": {
        "index": "https://rcdb.com/r.htm?ot=2",
        "page": "https://rcdb.com/r.htm?ot=2&page="
    }
}
gist = {
    "id": "6cea555f0723b1438b4a9aff14cc912b",
    "url": "https://api.github.com/gists/",
    "template": """{
        "description": "rcdb clone",
        "public": "true",
        "files": {
            "coasters.json": {
                "content": "%s"
            }
        }
    }"""
}
