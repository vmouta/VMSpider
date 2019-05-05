#!/usr/bin/python
# Person class

import unicodedata

from bs4 import BeautifulSoup

def unicodeHandle(stuff):
    return unicodedata.normalize('NFKD', stuff).encode('ascii','ignore')

class Person:

    def __init__(self, personHtml):
        '''Constructor'''
        self.firstName = ""
        self.lastName = ""
        self.location = ""
        self.country = ""
        self.industry = ""
        self.company = ""
        self.position = ""
        self.parseHtml(personHtml)

    def __str__(self):
        return """Person:
                \tfirstName:%s
                \tlastName:%s
                \tlocation:%s
                \tcountry:%s
                \tcompany:%s
                \tposition:%s
                \tindustry:%s""" % (self.firstName, self.lastName, self.location, self.country, self.company, self.position, self.industry)
           
    def parseHtml(self, personHtml):
        personSoup = BeautifulSoup(personHtml)
        
        #name
        fullNameContainer = personSoup.find('div', attrs={'id': 'name-container'})
        self.parseName(fullNameContainer)
        
        #headline
        headlineContainer = personSoup.find('div', attrs={'id': 'headline-container'})
        self.parseHeadline(headlineContainer)
        
        #Location
        locationContainer = personSoup.find('div', attrs={'id': 'location-container'})
        self.parseLocation(locationContainer)
    
        #current
        current = personSoup.find('tr', attrs={'id': 'overview-summary-current'})
        self.parseCurrent(current)
    
    def parseName(self, current):
        fullName = unicodeHandle(current.find('span', attrs={'class': 'full-name'}).text)
        nameComponents = fullName.split(" ")
        self.firstName = nameComponents[0]
        self.lastName = nameComponents[1]
    
    def parseHeadline(self, current):
        headline = unicodeHandle(current.find('p', attrs={'class': 'title'}).text)
        headlineComponents = headline.split(" at ")
        self.position = headlineComponents[0]
    
    def parseCurrent(self, current):
        if current != None:
            curentProperties = current.find('td').findAll('a')
            if curentProperties != None:
                for property in curentProperties:
                    if property["name"] == "company":
                        self.company = unicodeHandle(", ".join([self.company, property.text]) if self.company != "" else property.text)

    def parseLocation(self, location):
        if location != None:
            locationProperties = location.findAll('a')
            if locationProperties != None:
                for property in locationProperties:
                    if property["name"] == "location":
                        splitLocation = unicodeHandle(property.text).split(", ")
                        if len(splitLocation) > 1:
                            self.location = splitLocation[0]
                            self.country = splitLocation[1]
                        else:
                            self.country = splitLocation[0]
                    elif property["name"] == "industry":
                        self.industry = unicodeHandle(property.text)

    def csv(self):
        return [self.firstName, self.lastName, self.location, self.country, self.company, self.position, self.industry]


def csvHeader():
    return ["firstName", "lastName", "location", "country", "company", "position", "industry"]
