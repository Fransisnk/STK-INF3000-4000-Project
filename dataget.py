import json
from bs4 import BeautifulSoup as bs
import pandas as pd
from zipfile import ZipFile
from urllib.request import urlretrieve


class Dataget():
    def __init__(self):
        pass

    def getMonthlyTrips(self):
        """
        Checks for new json files in https://developer.oslobysykkel.no/data, downloads the zip-folder extracts the files
        and appends the to a list to be returned.
        :return: list with dict of trips
        """

        rooturl = "https://developer.oslobysykkel.no"
        rlist = []

        with open("temp/monthindex.html", "r") as html:
            soup = bs(html, "html.parser")

        for trip in soup.findAll("li", {"class": "report-list-item"}):
            content = bs(str(trip), "html.parser")
            month = content.find("h3").contents[0]

            # CsvUrl if needed
            # csvUrl = content.find("a", text="CSV")["href"]

            if not self.checkIfParsed("MonthData", month):
                jsonUrl = content.find("a", text="JSON")["href"]

                filehandle, _ = urlretrieve(rooturl+jsonUrl)
                zip_file_object = ZipFile(filehandle, 'r')

                first_file = zip_file_object.namelist()[0]
                file = zip_file_object.open(first_file)
                content = str(file.read())

                rlist.append(content)

                self.editParsed("MonthData", month)
                print(content)
            break
        return rlist

    def checkIfParsed(self, key, value):
        """
        Checks if value is in parsedFiles.json's key's element
        :param key: str key in the json file
        :param element: str vale in the list
        :return: True if in list else false
        """
        with open("res/parsedFiles.json", "r") as file:
            if value in json.load(file)[key]:
                return True
            else:
                return False

    def editParsed(self, key, value):
        """
        Appends value to parsedFiles.json's key's list
        :param key: str key in the json file
        :param element: value to ba appended in the list
        :return: none
        """
        with open("res/parsedFiles.json", "r") as file:
            data = json.load(file)

        data[key].append(value)
        with open("res/parsedFiles.json", "w") as file:
            json.dump(data, file)


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
    a = Dataget()
    print(a.getLocksFromJson('res/stations.json', 157))
    print(a.checkIfParsed("MonthData", "December 2016"))
    a.editParsed("MonthData", "December 2016")
    print(a.checkIfParsed("MonthData", "December 2016"))
