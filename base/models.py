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
