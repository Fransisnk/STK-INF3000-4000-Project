import numpy as np
import pandas as pd
import os
import json

class Datacrunch():
    def __init__(self):
        self.trippath = "res/trips"
        self.tripData = pd.read_csv("res/totTrip.csv", sep=",", parse_dates=['Start time', 'End time'])

    def tripMerge(self):
        """
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
                print("Could not concat new data with old, exception: " + e)

        self.tripData.to_csv("res/totTrip.csv", index=False)
        return self.tripData


if __name__ == "__main__":
    a = Datacrunch()
    print(a.tripMerge())
