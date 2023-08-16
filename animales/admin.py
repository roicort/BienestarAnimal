from django.contrib import admin
from base.admin import CustomGeoModelAdmin
from .models import *
from django.contrib.auth.models import Group

# Register your models here.

@admin.register(Animal)
class AnimalAdmin(CustomGeoModelAdmin):
    pass

admin.site.register(Habilidad)
admin.site.register(AnimalCategoria)
admin.site.register(AnimalInclusion)
admin.site.register(PostulacionAdopcion)
admin.site.register(AnimalFavorito)

# admin.site.unregister(Group)
