import os
import requests
from django.shortcuts import render
from django.apps import apps

# Create your views here.


def main_map(request):
    resource_post_model = apps.get_model(
        "donation", "ResourcePost"
    )  # getting model from donation app
    post_context = {"resource_posts": resource_post_model.objects.all()}

    mapbox_access_token = "pk." + os.environ.get("MAPBOX_KEY")

    # Drop-in Center API GET
    drop_in_center_URL = "https://data.cityofnewyork.us/resource/bmxf-3rd4.json"
    drop_in_center_r = requests.get(url=drop_in_center_URL)
    drop_in_centers = drop_in_center_r.json()

    for center in drop_in_centers:
        new_address = ""
        for part in center["address"].split():
            new_address = new_address + " " + part
            if new_address[-1] == ";" or new_address[-2:] == ".,":
                center["address"] = new_address[:-1]
                break
                
    # Internet spots API GET
    internet_center_URL = "https://data.cityofnewyork.us/resource/yjub-udmw.json"
    internet_center_r = requests.get(url=internet_center_URL)
    internet_centers = internet_center_r.json()

    # [{"objectid":"10362",
    # "borough":"3",
    # "type":"Limited Free",
    # "provider":"ALTICEUSA",
    # "name":"Linden Park",
    # "location":"IN PARK PLAYGROUND AREA",
    # "latitude":"40.65838500000",
    # "longitude":"-73.88758299940",
    # "x":"1015440.52783000000",
    # "y":"179163.81002900000",
    # "location_t":"Outdoor",
    # "remarks":"3 free 10 min sessions",
    # "city":"Brooklyn",
    # "ssid":"GuestWiFi",
    # "activated":"9999-09-09T00:00:00.000",
    # "borocode":"3",
    # "boroname":"Brooklyn",
    # "ntacode":"BK82",
    # "ntaname":"East New York",
    # "coundist":"42.00000000000",
    # "zip":"11207",
    # "borocd":"305.00000000000",
    # "ct2010":"1104.00000000000",
    # "bctcb2010":"1104.00000000000",
    # "bin":"0E-11",
    # "bbl":"3043490001.00000000000",
    # "doitt_id":"217",
    # "location_lat_long":{"latitude":"40.658385","longitude":"-73.8875829994"},
    # ":@computed_region_efsh_h5xi":"17214",":@computed_region_f5dn_yrer":"45",":@computed_region_yeji_bk3q":"2",":@computed_region_92fq_4b7q":"25",":@computed_region_sbqj_enih":"47"}]

    return render(
        request,
        "map/main.html",
        {
            "mapbox_access_token": mapbox_access_token,
            "drop_in_centers": drop_in_centers,
            "post_context": post_context["resource_posts"],
            "internet_centers": internet_centers,
        },
    )
