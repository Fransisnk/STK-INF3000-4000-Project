#!/usr/bin/env python
from flask import Flask
from flask_googlemaps import GoogleMaps
from flask_googlemaps import Map
from flask import render_template
from flask import request

app = Flask(__name__)
app.config['GOOGLEMAPS_KEY'] = "AIzaSyD1dtSQ7u68BiICJS_avC_EKhn9YztgQmk"
GoogleMaps(app)
marker_list =


@app.route("/")
def index():
    mymap = Map(identifier="bikemap", lat=59.927333, lng=10.749467, zoom=12, markers=[], style="height:700px; width:900px; margin=0;")
    sndmap = Map(
        identifier="sndmap",
        lat=37.4419,
        lng=-122.1419,
        markers=[
            {
                'icon': 'http://maps.google.com/mapfiles/ms/icons/green-dot.png',
                'lat': 37.4419,
                'lng': -122.1419,
                'infobox': "<b>Hello World</b>"
            },
            {
                'icon': 'http://maps.google.com/mapfiles/ms/icons/blue-dot.png',
                'lat': 37.4300,
                'lng': -122.1400,
                'infobox': "<b>Hello World from other place</b>"
            }
        ]
    )
    return render_template('index.html', mymap=mymap, sndmap=sndmap)


@app.route('/impressum')
def show_impressum():
    return '<h1>Impressum</h1><br>This has been created by Felix, Francis, Harjeet and Andrea.</br>'

def create_marker_list(list):
    pass


app.run(debug=True)


def getGPSFromJson(self, path, stationId):
    with open(path) as data_file:
        data = json.load(data_file)
    for station in data['stations']:
        if station['id'] == stationId:
            return ((station['center']['latitude'], station['center']['longitude']))