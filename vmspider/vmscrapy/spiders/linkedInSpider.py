# linkedin spider
import sys

from scrapy.spider import BaseSpider
from scrapy.selector import Selector
from scrapy.http import Request

from vmspider.linkedin import countriesFetch

def striplist(l):
    l = [x.strip().replace('\t',"") for x in l]
    return [x for x in l if x != u'']

class LinkedInSpider(BaseSpider):
    name = "linkedin"
    allowed_domains = ["linkedin.com"]
    
    start_urls = ["https://www.linkedin.com/directory/people-%s" % s
              for s in "abcdefghijklmnopqrstuvwxyz"]

    #start_urls = ["https://www.linkedin.com/directory/people-a-1"]
    #start_urls = ["https://www.linkedin.com/in/aakriti-tambi-b593ba4a","https://www.linkedin.com/in/exobialegal"]

    def parse(self, response):
        # If you want to look at the HTML you are parsing, uncomment the next few lines and then look at the file
        
        """
        f = open("html.txt","w+")
        f.write(response.url)
        f.write("\n\n")
        f.write(response.body)
        f.close()
        """
        
        sel = Selector(response)
