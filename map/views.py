import os
import requests
from django.shortcuts import render

# Create your views here.

def main_map(request):
    mapbox_access_token = 'pk.' + os.environ.get('MAPBOX_KEY')

    drop_in_center_URL = "https://data.cityofnewyork.us/resource/bmxf-3rd4.json"
    drop_in_center_r = requests.get(url = drop_in_center_URL)
    drop_in_centers = drop_in_center_r.json()

    # dropInCenter = []
    # for center in data:
    #     borough = center['borough']
    #     address = center['address']
    #     comments = center['comments']
    #     postcode = center['postcode']
    #     latitude = center['latitude']
    #     longitude = center['longitude']
    #
    # dropInCenters = []

    return render(request, 'map/main.html', { 'mapbox_access_token': mapbox_access_token, 'drop_in_centers': drop_in_centers } )




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
    #  {'center_name': 'Mainchance',
    #   'borough': 'Manhattan',
    #   'address': '120 E. 32nd Street; New York,\nNY 10016',
    #   'comments': 'Open 24 hours',
    #   'postcode': '1016',
    #   'latitude': '40.745377',
    #   'longitude': '-73.981306',
    #   'community_board': '105',
    #   'council_district': '2',
    #   'census_tract': '72',
    #   'bin': '1018469',
    #   'bbl': '1008870087',
    #   'nta': 'Murray Hill-Kips Bay'},
    #  {'center_name': 'Olivieri',
    #   'borough': 'Manhattan',
    #   'address': '257 West 30th Street; New\nYork, NY 10001',
    #   'comments': 'Open from 7:30 a.m.-8:30 p.m. This program remain open 24 hours during winter months',
    #   'postcode': '10001',
    #   'latitude': '40.749139',
    #   'longitude': '-73.994016',
    #   'community_board': '105',
    #   'council_district': '3',
    #   'census_tract': '101',
    #   'bin': '1014337',
    #   'bbl': '1007800009',
    #   'nta': 'Midtown-Midtown South'},
    #  {'center_name': 'Haven',
    #   'borough': 'Bronx',
    #   'address': '2640 Third Ave., Bronx, NY 10454',
    #   # comments<NONE>
    #   'postcode': '10454',
    #   'latitude': '40.812663',
    #   'longitude': '-73.924125',
    #   'community_board': '201',
    #   'council_district': '8',
    #   'census_tract': '41',
    #   'bin': '2000752',
    #   'bbl': '2023150030',
    #   'nta': 'Mott Haven-Port Morris'},
    #  {'center_name': 'Project Hospitality', 'borough': 'Staten Island', 'address': '150 Richmond Terrace; Staten\nIsland, NY 10301', 'comments': 'Open from 7:30 a.m.-8:30 p.m. This program remain open 24 hours during winter months', 'postcode': '10301', 'latitude': '40.645821', 'longitude': '-74.077908', 'community_board': '501', 'council_district': '49', 'census_tract': '7', 'bin': '5000104', 'bbl': '5000120001', 'nta': 'West New Brighton-New Brighton-St. George'},
    #  {'center_name': 'The Gathering Place', 'borough': 'Brooklyn', 'address': '2402 Atlantic Ave; Brooklyn,\nNY 11233', 'comments': 'Open from 7:30 a.m.-8:30 p.m. This program remain open 24 hours during winter months', 'postcode': '11233', 'latitude': '40.676015', 'longitude': '-73.905105', 'community_board': '316', 'council_district': '37', 'census_tract': '36502', 'bin': '3038666', 'bbl': '3014370008', 'nta': 'Ocean Hill'}]
