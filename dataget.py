import re
import json
from pprint import pprint
from pymongo import MongoClient

MongoClient("localhost", 27017)


class dataget():
    def __init__(self):
        pass

    def fromHtml(self, url):
        pass

    def fromCsv(self, path):
        pass

    def getLocksFromJson(self, path, stationId):
        with open(path) as data_file:
            data = json.load(data_file)
        for station in data['stations']:
            if station['id'] == stationId:
                return station['number_of_locks']
        return None

    def getGPSFromJson(self, path, stationId):
        pass

''' here you can test the shit:
a = dataget()
print(a.getLocksFromJson('res/stations.json', 157))
'''

a = dataget()
print(a.getLocksFromJson('res/stations.json', 158))