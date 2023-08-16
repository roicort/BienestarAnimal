from django.db import models
from animales.models import Habilidad, AnimalCategoria
from users.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from django.db.models import ProtectedError

# Create your models here.


class PerfilGeneral(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    nombres = models.CharField(max_length=255)
    apellidos = models.CharField(max_length=255)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    telefono = models.CharField(max_length=255)

    motivos = models.TextField(null=True, blank=True)

    tiene_animales = models.BooleanField(default=False)
    animales_descripcion = models.TextField(null=True, blank=True)

    personas_hogar = models.IntegerField(null=True, blank=True)
    situacion_familiar = models.CharField(max_length=32, choices=(('solor', 'Solo'), ('familia', 'Familia'), ('roomies', 'Roomies'), ('pareja','Pareja')))
    hogar_menores = models.BooleanField(null=True, blank=True)

    domicilio = models.CharField(max_length=255)
    ciudad = models.CharField(max_length=100, null=True, blank=True)
    codigo_postal = models.CharField(max_length=100, null=True, blank=True)
    municipio = models.CharField(max_length=100, null=True, blank=True)
    estado = models.CharField(max_length=100, null=True, blank=True)

    # Seccion de datos para fines estadisticos
    genero = models.CharField(max_length=100, null=True, blank=True, choices=[('Masculino', 'Masculino'), ('Femenino', 'Femenino'), ('Otro', 'Otro')])
    fecha_nacimiento = models.DateField(null=True, blank=True)
    capacidad_diferente = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Perfil de usuario"
        verbose_name_plural = "Perfiles de usuarios"

    def __str__(self):
        return f"{self.nombre} {self.apellidos}" if self.nombre and self.apellidos else self.user.email

    @property
    def nombre_completo(self):
        return f"{self.nombre} {self.apellidos}" if self.nombre and self.apellidos else self.user.email

    @receiver(post_save, sender=User)
    def crear_perfil_usuario(sender, instance, created, **kwargs):
        if created:
            PerfilGeneral.objects.create(user=instance)

    @receiver(post_delete, sender='perfiles.PerfilGeneral')
    def eliminar_perfil_usuario(sender, instance, **kwargs):
        if not instance.user.safe_delete:
            raise ProtectedError('No se pueden eliminar perfiles de manera independiente', instance)

