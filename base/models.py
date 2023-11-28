from django.contrib.gis.db import models
from django.utils.translation import gettext as _

# Create your models here.


class Habilidad(models.Model):
    nombre = models.CharField(max_length=60, unique=True)

    class Meta:
        verbose_name = "Habilidad"
        verbose_name_plural = "Habilidades"

    def __str__(self):
        return self.nombre

class TipoServicio(models.Model):
    nombre = models.CharField(max_length=60, unique=True)

    class Meta:
        verbose_name = "Tipo de Servicio"
        verbose_name_plural = "Tipos de Servicios"

    def __str__(self):
        return self.nombre

class Servicio(models.Model):
    tipo = models.ForeignKey(TipoServicio, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=60, unique=True)

    class Meta:
        verbose_name = "Servicio"
        verbose_name_plural = "Servicios"

    def __str__(self):
        return self.nombre