#!/usr/bin/python
# Fetch LinkedIn countries

import re
import requests

from bs4 import BeautifulSoup

list_of_countries = None


# linkdin countries spider
def htmlFetch():
    url = 'https://www.linkedin.com/directory/country_listing/'
    response = requests.get(url)
    html = response.content
    return html


def countriesFetch():
    html = htmlFetch()
    soup = BeautifulSoup(html)
    table = soup.find('main', attrs={'id': 'layout-main'})
    global list_of_countries
    list_of_countries = {}
    for row in table.findAll('ul'):
        for cell in row.findAll('a', href=True):
            values = cell['title'].replace(' ', '').split('-')
            url = cell['href']
            code = re.split("^https://([a-z]{2,3})\.", url)[1]
            list_of_countries[code] = ([code, values[0], values[1], url])
    return list_of_countries


def countriesNameCode():
    t = tuple("%s - %s" %(x[0], x[1]) for x in (list_of_countries if list_of_countries != None else countriesFetch()).values())
    return t


def countryNames():
    t = tuple(x[1] for x in (list_of_countries if list_of_countries != None else countriesFetch()).values())
    return t


def countryCodes():
    t = tuple(x[0] for x in (list_of_countries if list_of_countries != None else countriesFetch()).values())
    return t


def countryUrlForCode(code):
    return (list_of_countries if list_of_countries != None else countriesFetch())[code][3]


if __name__ == "__main__":
    print(countriesFetch())
