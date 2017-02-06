import unittest
import pandas as pd
import numpy as np
from io import StringIO
from datetime import datetime
import json


from datacrunch import Datacrunch
from dataget import Dataget

class TestDataget(unittest.TestCase):

    testClass = Dataget()

    def testGetYearFromHTML(self):

        date = datetime.strptime('160416','%d%m%y')
        result = self.testClass.getYearHtmlFromDate(date)
        known = "https://www.yr.no/sted/Norge/Oslo/Oslo/Oslo/almanakk.html?dato=2016-04-16"

        self.assertEqual(known, result)

    def testGetPastWeather(self):
        # Change arg when switching to html

        result = self.testClass.getPastWeather("temp/temp.html")
        self.assertIsInstance(result, type(pd.DataFrame()))

    def testGetLocksFromJson(self):
        pass

    def testCheckIfParsed(self):

        self.assertTrue(self.testClass.checkIfParsed("TestData", "test"))
        self.assertFalse(self.testClass.checkIfParsed("TestDat", "test"))

    def testGetMonthlyTrips(self):

        result = self.testClass.getMonthlyTrips()
        self.assertIsInstance(result, type(list()))

        if len(result) != 0:
            for e in result:
                self.assertIsInstance(e, type(dict()))

    def testUnzip(self):
        # Git doesnt like zip, so download zip from bysykkel data
        result = self.testClass.unzip("temp/testzip.zip")
        self.assertIsInstance(result, type(dict()))

class TestDatacrunch(unittest.TestCase):

    def testJsonToDB(self):
        pass

    def testGetFromDB(self):
        pass

    def testTripMerge(self):
        pass



if __name__ == "__main__":
    a = TestDataget()
    a.testGetYearFromHTML()