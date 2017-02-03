import unittest
import pandas as pd
import numpy as np
from io import StringIO
from datetime import datetime


from datacrunch import Datacrunch
from dataget import Dataget

class TestDataget(unittest.TestCase):
    def testGetYearFromHTML(self):

        getClass = Dataget()
        date = datetime.strptime('160416','%d%m%y')
        result = getClass.getYearHtmlFromDate(date)
        known = "https://www.yr.no/sted/Norge/Oslo/Oslo/Oslo/almanakk.html?dato=2016-04-16"

        self.assertEqual(known, result)

if __name__ == "__main__":
    a = TestDataget()
    a.testGetYearFromHTML()