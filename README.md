VMSpider
================

Vasco Mouta


INSTRUCTIONS
------------

-In order to run this scraper, you need to go and install BeautifulSoup.  (e.g $ pip install BeautifulSoup)
-In order to run this scraper, you need to go and install requests.  (e.g $ pip install requests)
-In order to run this scraper, you need to go and install scrapy.  (e.g $ pip install scrapy)

-You may need to install pip (e.g mac:  $ sudo easy_install pip)

-Once you do, all you need to do is jump into your terminal or command line and navigate to ~/VMSpider/
$python vmspider
or
$python vmspider -h

- it should be able to be installed as lib with :
$pip install git+git://github.com/vmouta/VMSpider.git
NOTE: Never tried

- I looked around at scrape interesting but no time to make something nicer
$scrapy crawl linked 
NOTE:Not usable at the moment

Originally written/uploaded January 2016
---------------------------------------

This is a project that will go through and scrape public profile information off of linkedin. 
This is information that anyone can find and see from linkedIn's directory such as:

/// People
https://www.linkedin.com/directory/people-a
https://www.linkedin.com/directory/people-b-1/
https://www.linkedin.com/directory/people-b-1-1-34/

/// By Country
https://www.linkedin.com/directory/country_listing/
https://be.linkedin.com/directory/people-a

I used Scrapy, which is an open-source online library in python that helps you scrape websites.
http://scrapy.org/

