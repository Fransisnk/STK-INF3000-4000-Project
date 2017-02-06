import numpy as np
import pandas as pd
import os
import json
from pymongo import MongoClient
from dataget import Dataget

class Datacrunch(Dataget):

    def __init__(self):

        Dataget.__init__(self)

        self.client = MongoClient()
        # MongoClient('localhost', 27017), MongoClient('mongodb://localhost:27017/')
        self.tripDb = self.client.tripDb
        self.trips = self.tripDb.trips
        self.stations = self.tripDb.stations

        self.trippath = "res/trips"
        # self.tripData = pd.read_csv("res/totTrip.csv", sep=",", parse_dates=['Start time', 'End time'])

    def updateDB(self):
        """
        Adds new trips to the database
        :return: None
        """
        for e in self.getMonthlyTrips():
            self.jsonToDB(e)

    def jsonToDB(self, dict):
        """
        Takes a monthly json file from OSLO bysykkel and adds the data to the database
        :param dict: dict file
        :return: None
        """
        data = dict["trips"]
        self.trips.insert_many(data)

    def getFromDB(self):
        print(self.trips.find_one())

    def tripMerge(self):
        """
        Maybe not usefull

        Combines all new bike-trips located in /res/trips to one pandas-dataframe with older csv.
        :return: pandas dataframe with all trips
        """
        dfList = []
        concatflag = False

        with open("res/parsedFiles.json", "r") as dataFile:

            data = json.load(dataFile)
            for csvFile in os.listdir(self.trippath):

                if csvFile not in data["ParsedMonthTrips"]:

                    concatflag = True
                    dfList.append(pd.read_csv(self.trippath+"/"+csvFile, sep=",",
                                              parse_dates=['Start time', 'End time']))
                    data["ParsedMonthTrips"].append(csvFile)

        with open("res/parsedFiles.json", "w") as outFile:
            json.dump(data, outFile)

        if concatflag:
            try:
                self.tripData = pd.concat([self.tripData]+dfList)
            except Exception as e:
                print("Could not concat new data with old, exception:")
                print(e)

        self.tripData.to_csv("res/totTrip.csv", index=False)
        return self.tripData

    def clearDB(self):
        self.trips.remove()

if __name__ == "__main__":
    a = Datacrunch()
    a.jsonToDB(a.unzip("temp/testzip.zip"))
    #a.updateDB()
    #a.jsonToDB()
    a.getFromDB()
