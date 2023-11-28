from django.contrib import admin
from base.admin import CustomGeoModelAdmin
from .models import *
from django.contrib.auth.models import Group
from django import forms

# Register your models here.

admin.site.register(Habilidad)
admin.site.register(AnimalCategoria)
admin.site.register(AnimalCaracteristica)
#admin.site.register(Procedimiento)

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

    #form = AnimalAdminForm
    list_display = ('nombre','id', 'categoria', 'sexo', 'FotoPreview', 'centro')
    search_fields = ('id', 'nombre')
    list_filter = ("categoria", 'asociacion__nombre', 'sexo', 'apto_niños', 'talla', ("fecha_nacimiento", DateRangeFilter))
    read_only_fields = ('FotoPreview',)
    change_list_template = "admin/daterange/change_list.html"
    resource_classes = [AnimalResource]
    inlines = [ProcedimientoInline]

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

###### Procedimiento

class ProcedimientoResource(resources.ModelResource):
    class Meta:
        model = Procedimiento

@admin.register(Procedimiento)
class ProcedimientoAdmin(ImportExportModelAdmin):

    list_display = ('id', 'servicio', 'animal', 'fecha_aplicacion', 'centro')
    search_fields = ('id', 'servicio__nombre', 'animal')
    list_filter = ('servicio__nombre', 'animal', 'centro__nombre', ("fecha_aplicacion", DateRangeFilter))
    change_list_template = "admin/daterange/change_list.html"

    resource_classes = [ProcedimientoResource]


####################################################################
