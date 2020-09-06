#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
from flask import Flask, render_template, request
from flask_googlemaps import GoogleMaps, Map
from dotenv import load_dotenv, find_dotenv
import pandas as pd
import requests
import os

load_dotenv(find_dotenv())

# require Flask-GoogleMaps (https://github.com/rochacbruno/Flask-GoogleMaps)

app = Flask(__name__)
api_key = os.getenv('GMAPS_API_KEY') # change this to your api key
# get api key from Google API Console (https://console.cloud.google.com/apis/)
GoogleMaps(app, key=api_key) # set api_key
devices_data = {} # dict to store data of devices
devices_location = {} # dict to store coordinates of devices
# use sqlalchemy or something to store things in database

@app.route('/', methods=['GET', 'POST'])
def index():
    
    station_status = requests.get("https://gbfs.divvybikes.com/gbfs/en/station_status.json").json()['data']['stations']
    station_info = requests.get("https://gbfs.divvybikes.com/gbfs/en/station_information.json").json()['data']['stations']

    ss = pd.DataFrame.from_dict(station_status)
    si = pd.DataFrame.from_dict(station_info)

    df = ss.merge(si, on='station_id')

    latitude_list = df['lat']
    longitude_list = df['lon']

    markers_data = [{'lat': row['lat'], 'lng': row['lon'], 'label': str(row['num_ebikes_available'])} for i, row in df.iterrows()]

    map = Map(
        identifier="divvymap",
        style="height:100%;width:100%;margin:0;",
        lat=41.881832,
        lng=-87.623177,
        markers=markers_data
    )

    return render_template('map.html', map=map) # render template

@app.route('/getdata', methods=['GET', 'POST'])
def getdata():
    json_data = requests.get.args('json')
    return json_data
    # you can use this to get request with strings and parse json
    # put data in database or something

if __name__ == '__main__':
    app.run() # run app