from django.contrib import admin
from base.admin import CustomGeoModelAdmin
from .models import *
from django.contrib.auth.models import Group

# Register your models here.

#admin.site.register(Animal)
admin.site.register(Habilidad)
admin.site.register(AnimalCategoria)
admin.site.register(AnimalInclusion)
#admin.site.register(PostulacionAdopcion)
admin.site.register(AnimalFavorito)
#admin.site.register(Adopcion)

###### Estos recursos son para poder exportar los datos ######

from import_export.admin import ImportExportModelAdmin
from import_export import resources
from daterange.filters import DateRangeFilter

###### Animales 

class AnimalResource(resources.ModelResource):
    class Meta:
        model = Animal

@admin.register(Animal)
class AnimalAdmin(ImportExportModelAdmin):

    list_display = ('nombre','id', 'categoria', 'sexo')
    search_fields = ('id', 'nombre')
    list_filter = ("categoria", 'asociacion', ("fecha_nacimiento", DateRangeFilter))
    change_list_template = "admin/daterange/change_list.html"

    resource_classes = [AnimalResource]

###### Adopciones 

class AdopcionResource(resources.ModelResource):
    class Meta:
        model = Adopcion

@admin.register(Adopcion)
class AdopcionAdmin(ImportExportModelAdmin):

    list_display = ('animal','asociacion')
    search_fields = ('id', 'animal')
    list_filter = ('asociacion', ("fecha_publicacion_inicio", DateRangeFilter))
    change_list_template = "admin/daterange/change_list.html"

    resource_classes = [AdopcionResource]

###### PostulacionAdopcion 

class PostulacionAdopcionResource(resources.ModelResource):
    class Meta:
        model = PostulacionAdopcion

@admin.register(PostulacionAdopcion)
class PostulacionAdopcionAdmin(ImportExportModelAdmin):

    list_display = ('animal','id')
    search_fields = ('id', 'animal')
    list_filter = ('estatus_aceptacion_postulacion', ("fecha_postulacion", DateRangeFilter))
    change_list_template = "admin/daterange/change_list.html"

    resource_classes = [PostulacionAdopcionResource]

###### ReportePerdido

class ReportePerdidoResource(resources.ModelResource):
    class Meta:
        model = ReportePerdido

@admin.register(ReportePerdido)
class ReportePerdidoAdmin(CustomGeoModelAdmin, ImportExportModelAdmin):

    list_display = ('animal','id')
    search_fields = ('id', 'animal')
    list_filter = ('estatus', ("fecha_reporte", DateRangeFilter))
    change_list_template = "admin/daterange/change_list.html"

    resource_classes = [ReportePerdidoResource]

####################################################################
