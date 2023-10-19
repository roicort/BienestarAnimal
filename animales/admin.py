from django.contrib import admin
from base.admin import CustomGeoModelAdmin
from .models import *
from django.contrib.auth.models import Group

# Register your models here.

@admin.register(ReportePerdido)
class ReportePerdidoAdmin(CustomGeoModelAdmin):
    pass

admin.site.register(Animal)
admin.site.register(Habilidad)
admin.site.register(AnimalCategoria)
admin.site.register(AnimalInclusion)
admin.site.register(PostulacionAdopcion)
admin.site.register(AnimalFavorito)
admin.site.register(Adopcion)

# admin.site.unregister(Group)
