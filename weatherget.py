from bs4 import BeautifulSoup as bs
import pandas as pd
import io
import html5lib
import lxml

tempHtml = "temp/temp.html"

def getYrHtmlFromDate(date):
    return "https://www.yr.no/sted/Norge/Oslo/Oslo/Oslo/almanakk.html?dato="+date

def dataFromHtml(url):
    with open(url,"r") as html:
        soup = bs(html, "html.parser")

    soup = soup.findAll("table", {"class": "yr-table yr-table-hourly yr-popup-area"}, limit=1)

    pddf = pd.read_html(str(soup[0]),header=0)
    print(pddf)

dataFromHtml("temp/temp.html")
