#!/usr/bin/python
# showmeboone spider

import csv

try:
    import http.cookiejar
    import urllib3
except ImportError:
    import cookielib
    import urllib2

import os
import urllib
import json
import unicodedata

from .person import Person
from .person import csvHeader
from vmspider import Fetcher

from bs4 import BeautifulSoup


test = False
debug = False
def printLine(str):
    if debug:
        print (str)


def unicodeHandle(stuff):
    return unicodedata.normalize('NFKD', stuff).encode('ascii','ignore')


class LinkedIn(Fetcher):

    def __init__(self, query=None, country=None, verbose=False, login="m8r-m1knwk@mailinator.com", password="qwert1", cookie_filename = "parser.cookies.txt"):
        '''Constructor'''
        global debug
        debug = verbose
        self.login = login
        self.password = password
        self.country = country
        self.query = query
        self.cookie_filename = cookie_filename
        self.loginUser(login, password)

    def __str__(self):
        return ("""LinkedIn:
            \tLogin: %s
            \tPassword: %s
            \tQuery: %s
            \tcountry=%s""" % (self.login, self.password, self.query, self.country if self.country else "All"))
    
    
    def loginUser(self, login, password):
        # Simulate browser with cookies enabled
        self.cj = cookielib.MozillaCookieJar(self.cookie_filename)
        if os.access(self.cookie_filename, os.F_OK):
            self.cj.load()
        self.opener = urllib2.build_opener(
                           urllib2.HTTPRedirectHandler(),
                           urllib2.HTTPHandler(debuglevel=0),
                           urllib2.HTTPSHandler(debuglevel=0),
                           urllib2.HTTPCookieProcessor(self.cj)
        )
        self.opener.addheaders = [ ('User-agent', ('Mozilla/4.0 (compatible; MSIE 6.0; ' 'Windows NT 5.2; .NET CLR 1.1.4322)'))]
              
        # Login
        self.loginPage()
        

    def loadPage(self, url, data=None):
        """ Utility function to load HTML from URLs for us with hack to continue despite 404 """
        printLine(url)
        # We'll print the url in case of infinite loop
        # print "Loading URL: %s" % url
        try:
            if data is not None:
                response = self.opener.open(url, data)
            else:
                response = self.opener.open(url)
            return ''.join([str(l) for l in response.readlines()])
        except Exception as e:
            # If URL doesn't load for ANY reason, try again...
            # Quick and dirty solution for 404 returns because of network problems
            # However, this could infinite loop if there's an actual problem
            return self.loadPage(url, data)

    def loadSoup(self, url, data=None):
        """ Combine loading of URL, HTML, and parsing with BeautifulSoup """
        html = self.loadPage(url)
        soup = BeautifulSoup(html)
        return soup
                        
    def loginPage(self):
        """ Handle login. This should populate our cookie jar."""
        html = self.loadPage("https://www.linkedin.com/")
        soup = BeautifulSoup(html)
        csrf = soup.find(id="loginCsrfParam-login")
        if csrf != None:
            login_data = urllib.urlencode({
                'session_key': self.login,
                'session_password': self.password,
                'loginCsrfParam': csrf['value'],
                }).encode('utf8')
            self.loadPage("https://www.linkedin.com/uas/login-submit", login_data)
            self.cj.save()
        return
    
    def loadTitle(self):
        soup = self.loadSoup("http://www.linkedin.com/nhome")
        return soup.find("title")
    
    def htmlFetch(self):
        baseUrl = "https://www.linkedin.com/"
        param = {"pt":"people"}
        if self.country != None:
            param["countryCode"] = self.country
        if self.query != None:
            param["keywords"] = self.query
        url = "".join([baseUrl, "vsearch/p?", urllib.urlencode(param)])
        printLine(url)
        if test:
            # For Testing
            try:
                with open('linkedin_html.txt', 'r') as myfile:
                    pageHtml=myfile.read().replace('\n', '')
            except:
                    print ("linkedin_html.txt - not found file with html for testing - try to generate")
                    pageHtml = self.loadPage(url)
                    f = open("linkedin_html.txt","w+")
                    f.write(pageHtml)
                    f.close()
        else:
            pageHtml = self.loadPage(url)
        return pageHtml

    def htmlFetchPerson(self, personUrl):
        if test:
            # For Testing
            try:
                with open('person_html.txt', 'r') as myfile:
                    html=myfile.read().replace('\n', '')
            except:
                print ("person_html.txt - not found file with html for testing - try to generate")
                html = self.loadPage(personUrl)
                f = open("person_html.txt","w+")
                f.write(html)
                f.close()
        else:
            html = self.loadPage(personUrl)
        return html

    def csv(self, outputFileName):
        ''' Build out put'''
        html = self.htmlFetch()
        soup = BeautifulSoup(html)
        code = soup.find('code', attrs={'id': 'voltron_srp_main-content'})
        if code != None:
            data = unicodeHandle(code.text)
            data = data.replace(":\u002d1,", ":\"\u002d1\",")
            jdata = json.loads(data)
            results = jdata["content"]["page"]["voltron_unified_search_json"]["search"]["results"]

            print(",".join(csvHeader()))
            list_persons_csv = []
            for person in results:
                personProfile = person.get("person", None)
                personProfile = personProfile.get("link_nprofile_view_headless", None) if personProfile != None else None
                if personProfile != None:
                    personHtml = self.htmlFetchPerson(personProfile)
                    personObject = Person(personHtml)
                    list_persons_csv.append(personObject.csv())
                    print(",".join(personObject.csv()))
        
            if outputFileName != None:
                with open(outputFileName, 'wb') as csvfile:
                    writer = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_ALL)
                    writer.writerow(csvHeader())
                    writer.writerows(list_persons_csv)
        else:
            print ("upss no content!!! - Probably something change or cookie old")






