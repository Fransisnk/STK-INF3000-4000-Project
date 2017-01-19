import numpy as np
import pandas as pd
import os

class Datacrunch():
    def __init__(self):
        self.trippath = "res/trips"

    def tripMerge(self):
        dfList = []
        for csvFile in os.listdir(self.trippath):
            dfList.append(pd.read_csv(self.trippath+"/"+csvFile, sep=",", parse_dates=['Start time', 'End time']))



if __name__ == "__main__":
    a = Datacrunch()
    a.tripMerge()