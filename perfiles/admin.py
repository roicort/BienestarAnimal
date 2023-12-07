from django.contrib import admin
from .models import PerfilGeneral
from daterange.filters import DateRangeFilter

# from django.contrib.auth.models import Group

# Register your models here.

#admin.site.register(PerfilGeneral)

# admin.site.unregister(Group)


# class EstudioAdmin(admin.ModelAdmin):
#     pass
#
#
# admin.site.register(GradoAcademico, EstudioAdmin)
#
#
# class ExperienciaAdmin(admin.ModelAdmin):
#     pass
#
#
# admin.site.register(ExperienciaProfesional, ExperienciaAdmin)
#
#
# class IdiomaAdmin(admin.ModelAdmin):
#     pass
#
#
# admin.site.register(Idioma, IdiomaAdmin)
#
#
# class CertificacionAdmin(admin.ModelAdmin):
#     pass
#
#
# admin.site.register(Certificacion, CertificacionAdmin)

@admin.register(PerfilGeneral)
class PerfilGeneralAdmin(admin.ModelAdmin):
    list_display = ('user', 'nombres', 'apellidos', 'telefono')
    search_fields = ('user', 'nombres', 'apellidos', 'telefono')
    list_filter = ('genero', ("fecha_nacimiento", DateRangeFilter))
    change_list_template = "admin/daterange/change_list.html"
    pass