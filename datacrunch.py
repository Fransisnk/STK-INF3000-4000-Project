import numpy as np
import pandas as pd
import os
import json
from pymongo import MongoClient
from dataget import Dataget
from datetime import datetime

class Datacrunch(Dataget):

    def __init__(self):

        Dataget.__init__(self)

        self.client = MongoClient()
        # MongoClient('localhost', 27017), MongoClient('mongodb://localhost:27017/')
        self.tripDb = self.client.tripDb
        self.trips = self.tripDb.trips
        self.stations = self.tripDb.stations
        self.weather = self.tripDb.weather

        self.trippath = "res/trips"
        # self.tripData = pd.read_csv("res/totTrip.csv", sep=",", parse_dates=['Start time', 'End time'])

    def updateDB(self):
        """
        Adds new trips to the database
        :return: None
        """
        for e in self.getMonthlyTrips():
            self.jsonToDB(e, self.trips)

    def jsonToDB(self, dict, db, remove=None):
        """
        Takes a monthly json file from OSLO bysykkel and adds the data to the database
        :param dict: dict file
        :return: None
        """
        db.insert_many(dict)
        if remove is not None:
            db.update({}, {"$unset": {remove: 1}}, multi=True)

    def getFromDB(self):
        print(self.trips.find_one())
        print(self.stations.find_one())

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

    def clearDB(self, db):
        db.remove()

    def jsonToDict(self, jsonPath):
        """
        Takes a path to a json file and returns a dict with the contents
        :param jsonPath: str path to file
        :return: dict with contents
        """
        with open(jsonPath) as data_file:
            data = json.load(data_file)
        return data

    def forStationinDb(self):
        for station in self.stations.find():
            print(station)

    def getFromAllStations(self, keys):
        """
        Takes a list of keys, loops trough the stations db, and returns a list with dictionaries with given keys
        :param keys: list with keys
        :return: list with dicts
        """
        rlist = []
        for station in self.stations.find():
            rdict = {}
            for key in keys:
                rdict[key] = station[key]
            rlist.append(rdict)
        return rlist

    def countFlow(self):

        for trip in self.trips.find():
            outgoing = trip["start_station_id"]
            ingoing = trip["end_station_id"]
            print(trip["start_time"])

if __name__ == "__main__":
    a = Datacrunch()
    a.jsonToDB(a.unzip("temp/testzip.zip")["trips"], a.trips)
    stations = a.jsonToDict("res/stations.json")
    a.jsonToDB(stations["stations"], a.stations, "bounds")
    #a.updateDB()
    #a.jsonToDB()
    #a.getFromDB()
    #a.getFromAllStations(["center", "id"])
    a.countFlow()
    a.clearDB(a.trips)
    a.clearDB(a.stations)
