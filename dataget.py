import re
import json
from pprint import pprint
from pymongo import MongoClient
from bs4 import BeautifulSoup as bs
import pandas as pd

MongoClient("localhost", 27017)


class dataget():
    def __init__(self):
        pass

    def fromHtml(self, url):
        pass

    def fromCsv(self, path):
        pass

    def getLocksFromJson(self, path, stationId):
        """
        Gets n locks from bike station by ID-nr
        :param path: str path to .json file with bike-lock information
        :param stationId: StationID to get from
        :return: If found str n locks, else None
        """
        with open(path) as data_file:
            data = json.load(data_file)
        for station in data['stations']:
            if station['id'] == stationId:
                return station['number_of_locks']
        return None

    def getGPSFromJson(self, path, stationId):
        pass

    def getYrHtmlFromDate(self, date):
        # TODO: Convert datetime to YYYY-MM-DD str
        """
        Takes an datetime object and returns url to yr for given day.
            url in the form Oslo/Oslo/Oslo/almanakk.html?dato=YYYY-MM-DD
        :param date: Datetime object
        :return: Str, url to given day
        """
        return "https://www.yr.no/sted/Norge/Oslo/Oslo/Oslo/almanakk.html?dato=" + date

    def dataFromHtml(self, url):
        # TODO: Data needs cleanup, index can be Datetime
        """
        Takes an url to yr, parses the html and makes an pandas data frame with the usefull information.
        :param url: Str, link to yr for a earlier date
        :return: pandas data frame with weather information
        """
        with open(url, "r") as html:
            soup = bs(html, "html.parser")

        soup = soup.findAll("table", {"class": "yr-table yr-table-hourly yr-popup-area"}, limit=1)

        pddf = pd.read_html(str(soup[0]), header=0)[0]
        pddf = pddf.drop(pddf.columns[[9, 10]], axis=1)

        pddf.columns = ["Time", "Weather", "T Measured", "T Max", "T Min", "Rain/Snow", "Wind Mean", "Wind Strongest",
                        "Humidity"]

        return pddf

if __name__ == "__main__":
    a = dataget()
    print(a.getLocksFromJson('res/stations.json', 157))
    print(a.dataFromHtml("temp/temp.html"))
