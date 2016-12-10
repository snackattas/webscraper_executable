import os
import sys
import csv
import json
import base64
import requests
from BeautifulSoup import BeautifulSoup

file_destination = "inmates.csv"
url = 'http://www.showmeboone.com/sheriff/JailResidents/JailResidents.asp'

def removeFile():
    try:
        os.remove(file_destination)
        print("Past file {} removed\n".format(file_destination))
    except:
        print("No past file {} to remove\n".format(file_destination))


def webCrawler():
    try:
        response = requests.get(url)
        html = response.content
    except:
        print("HTTP error. crawler is not able to connect to {}".format(url))
        return False
    try:
        # Core web parsing logic lives here.
        soup = BeautifulSoup(html)
        table = soup.find('tbody', attrs={'class': 'stripe'})
        list_of_rows = []
        for row in table.findAll('tr'):
            list_of_cells = []
            for cell in row.findAll('td'):
                text = cell.text.replace('&nbsp;', '')
                list_of_cells.append(text)
            list_of_rows.append(list_of_cells)
        list_of_rows.append([sys.argv[1]])
    except:
        print("Parsing error. The format of the url must have changed: {}".format(url))
        return False
    print("Web crawler complete\n")
    return list_of_rows


def saveFile(list_of_rows):
    try:
        with open(file_destination, "wb") as outfile:
            writer = csv.writer(outfile)
            writer.writerows(list_of_rows)
            print("File {} created\n".format(file_destination))
            return True
    except:
        print("Unable to write content to file {}".format(file_destination))
        return False

if __name__ == "__main__":
    removeFile()
    list_of_rows = webCrawler()
    if not list_of_rows:
        exit()
    result = saveFile(list_of_rows)
