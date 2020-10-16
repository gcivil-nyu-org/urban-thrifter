import os
import requests
from django.shortcuts import render

# Create your views here.

def main_map(request):
    mapbox_access_token = 'pk.' + os.environ.get('MAPBOX_KEY')
    # mapbox_access_token = 'pk.eyJ1Ijoiamdpbm1iNyIsImEiOiJja2cybXpuNzAwMXFzMnFqdDFzbXBmNGszIn0.6UJeoJW2FwSS9LAOZN_QBw'

    # Drop-in Center API GET
    drop_in_center_URL = "https://data.cityofnewyork.us/resource/bmxf-3rd4.json"
    drop_in_center_r = requests.get(url = drop_in_center_URL)
    drop_in_centers = drop_in_center_r.json()
    # Information in JSON
    # [{'center_name': 'Living Room',
    #   'borough': 'Bronx',
    #   'address': '800 Barretto Street; Bronx, NY\n10474',
    #   'comments': 'Open 24 hours',
    #   'postcode': '10474',
    #   'latitude': '40.816615',
    #   'longitude': '-73.889883',
    #   'community_board': '202',
    #   'council_district': '17',
    #   'census_tract': '93',
    #   'bin': '2006002',
    #   'bbl': '2027400100',
    #   'nta': 'Hunts Point'},

    return render(request, 'map/main.html', { 'mapbox_access_token': mapbox_access_token, 'drop_in_centers': drop_in_centers } )
