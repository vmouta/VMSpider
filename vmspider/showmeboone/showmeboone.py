# showmeboone spider

import csv
import requests
from BeautifulSoup import BeautifulSoup
from vmspider import Fetcher

class ShowMeBoone(Fetcher):

    def __init__(self, query=None, country=None):
        '''Constructor'''
        self.query = query

    def __str__(self):
        return ("Query: %s\ncountry=%s" % (self.query, self.country if self.country else "All"))


def htmlFetch():
    url = 'http://www.showmeboone.com/sheriff/JailResidents/JailResidents.asp'
    response = requests.get(url)
    html = response.content
    soup = BeautifulSoup(html)
    table = soup.find('tbody', attrs={'id': 'mrc_main_table'})
    list_of_rows = []
    for row in table.findAll('tr'):
        list_of_cells = []
        for cell in row.findAll('td'):
            text = cell.text.replace('&nbsp;', '')
            list_of_cells.append(text)
        list_of_rows.append(list_of_cells)
    outfile = open("./inmates.csv", "wb")
    writer = csv.writer(outfile)
    writer.writerow(["Last", "First", "Middle", "Gender", "Race", "Age", "City", "State"])
    writer.writerows(list_of_rows)

if __name__ == "__main__":
    print(htmlFetch())
