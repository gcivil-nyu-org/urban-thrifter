from django.contrib import admin
from .models import ResourcePost
# import json
from django.conf import settings



# Register your models here.
admin.site.register(ResourcePost)

class ResourcePostAdmin(admin.ModelAdmin):
    list_display = ('position_map', 'dropoff_location')

    def position_map(self, instance):
        if instance.dropoff_location is not None:
            return '<img src="http://maps.googleapis.com/maps/api/ \
                    staticmap?center=%(latitude)s,%(longitude)s& \
                    zoom=%(zoom)s&size=%(width)sx%(height)s& \
                    maptype=roadmap&markers=%(latitude)s,%(longitude)s& \
                    sensor=false&visual_refresh=true&scale=%(scale)s& \
                    key=%(key)s" \
                    width="%(width)s" height="%(height)s">' % {
                'latitude': instance.dropoff_location.latitude,
                'longitude': instance.dropoff_location.longitude,
                'key': getattr(settings, 'PLACES_MAPS_API_KEY'),
                'zoom': 9,
                'width': 100,
                'height': 100,
                'scale': 2,
                'map_id':'3215ae039708a60f'
            }
    position_map.allow_tags = True
