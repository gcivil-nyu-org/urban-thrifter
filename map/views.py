import os
from django.shortcuts import render

# Create your views here.

def main_map(request):
    mapbox_access_token = 'pk.' + os.environ.get('MAPBOX_KEY')
    return render(request, 'main.html', { 'mapbox_access_token': mapbox_access_token} )
