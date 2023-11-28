from django.contrib.gis import admin
from .models import *

# Register your models here.

class CustomGeoModelAdmin(admin.GeoModelAdmin):
    default_lon = -100.31
    default_lat = 25.67
    default_zoom = 12
    scrollable = False
    wms_url = 'https://ows.terrestris.de/osm/service'
    wms_layer = 'OSM-WMS'

# Register your models here.

admin.site.register(TipoServicio)
admin.site.register(Servicio)




