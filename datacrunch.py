import numpy as np
import pandas as pd
import os

class Datacrunch():
    def __init__(self):
        self.trippath = "res/trips"

    def tripMerge(self):
        # TODO: save the data to file, and check for new files to combine with saved file when running the function.
        """
        Combines all bike-trips located in /res/trips to one pandas-dataframe
        :return: pandas dataframe with all trips
        """
        dfList = []
        for csvFile in os.listdir(self.trippath):
            dfList.append(pd.read_csv(self.trippath+"/"+csvFile, sep=",",
                                      parse_dates=['Start time', 'End time']))

        tripCsv = pd.concat(dfList)
        tripCsv.to_csv("res/totTrip.csv")
        return pd.concat(dfList)


if __name__ == "__main__":
    a = Datacrunch()
    print(a.tripMerge())