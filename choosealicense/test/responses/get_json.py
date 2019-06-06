#!/usr/bin/env python
# -*- coding: utf-8 -*-

from os import path
import json
import requests

ROOT = path.dirname(path.abspath(__file__))


def get_license_list():
    response = requests.get(
        'https://api.github.com/licenses',
        headers={'accept': 'application/vnd.github.drax-preview+json'})
    with open(path.join(ROOT, 'licenses.json'), 'w') as f:
        json.dump(response.json(), f, indent=4)
    print("Get the license list.")


def get_individual_license():
    with open(path.join(ROOT, 'licenses.json')) as f:
        response = json.loads(f.read())
    all_the_licenses = [l["key"] for l in response]
    for license in all_the_licenses:
        response = requests.get(
            'https://api.github.com/licenses/{0}'.format(license),
            headers={'accept': 'application/vnd.github.drax-preview+json'})
        with open(path.join(ROOT, 'licenses/{0}.json'.format(license)),
                  'w') as f:
            json.dump(response.json(), f, indent=4)
        print("Get the license: {0}.".format(license))


def get_not_found():
    response = requests.get(
        'https://api.github.com/licenses/invalid',
        headers={'accept': 'application/vnd.github.drax-preview+json'})
    with open(path.join(ROOT, 'not_found.json'), 'w') as f:
        json.dump(response.json(), f, indent=4)
    print("Get the invalid response.")


if __name__ == "__main__":
    get_license_list()
    get_individual_license()
    get_not_found()
