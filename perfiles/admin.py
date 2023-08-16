from django.contrib import admin
from .models import *
# from django.contrib.auth.models import Group

# Register your models here.

admin.site.register(PerfilGeneral)

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
