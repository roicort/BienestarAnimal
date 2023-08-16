from django.contrib import admin
from base.admin import CustomGeoModelAdmin
from .models import *

# Register your models here.

@admin.register(Asociacion)
class AsociacionAdmin(CustomGeoModelAdmin):
    pass

@admin.register(Centro)
class SucursalAdmin(CustomGeoModelAdmin):
    pass

admin.site.register(VinculacionAsociacion)
