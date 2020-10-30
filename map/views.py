import os
import requests
from django.shortcuts import render
from django.apps import apps

# Create your views here.

def main_map(request):

    mapbox_access_token = "pk." + os.environ.get("MAPBOX_KEY")

    # All Personal Donations
    resource_post_model = apps.get_model(
        "donation", "ResourcePost"
    )  # getting model from donation app
    post_context = {"resource_posts": resource_post_model.objects.all()}

    # Shelter API GET
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
