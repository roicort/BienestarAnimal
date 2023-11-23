from django.contrib.gis.db import models
from users.models import User
from django.contrib.auth.models import AbstractUser, Group
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.db.models import ProtectedError
from threadlocals.threadlocals import get_current_request

# Create your models here.

class AsociacionBaseAbstract(models.Model):
    """
    Abstract class base para modelo Asociacion
    """
    
    def upload_to(instance, filename):
        return f'asociacions/logo/{instance.nombre}/{filename}'
    
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField()
    logo = models.ImageField(max_length=255, null=True, blank=True, upload_to=upload_to)
    # TODO: Add a signal to delete the logo file when the asociacion is deleted
    domicilio = models.CharField(max_length=255, verbose_name="Domicilio, calle y número")
    colonia = models.CharField(max_length=255)
    codigo_postal = models.CharField(max_length=5)
    estado = models.CharField(max_length=255)
    municipio = models.CharField(max_length=255)
    esta_verificada = models.BooleanField(default=False)
    geom = models.PointField(srid=4326, null=True, blank=True)
    telefono = models.CharField(max_length=10, null=True, blank=True)

    class Meta:
        abstract = True

class Asociacion(AsociacionBaseAbstract):
    """
    Asociacion model
    """

    def __str__(self):
        return f"{self.nombre}"

    def save(self, *args, **kwargs):
        request = get_current_request()
        if request and request.user and request.user.is_authenticated:
            if request.user.is_staff:
                super(Asociacion, self).save(*args, **kwargs)
            else:
                self.esta_verificada = False
                super(Asociacion, self).save(*args, **kwargs)
        else:
            # Uncomment next line if you want to allow to create Asociacion objects from CLI without request
            # super(Asociacion, self).save(*args, **kwargs)
            # Comment next line and unncoment the previous one if you want to avoid creating Asociacion objects from CLI without request
            raise ProtectedError("No cuentas con permisos para realizar esta acción", self)

    class Meta:
        verbose_name = "Asociacion"
        verbose_name_plural = "Asociaciones"
        ordering = ['nombre']


class Centro(models.Model):
    """
    Centro model
    """
    asociacion = models.ForeignKey(Asociacion, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=255)
    domicilio = models.CharField(max_length=255, verbose_name="Domicilio, calle y número")
    colonia = models.CharField(max_length=255)
    codigo_postal = models.CharField(max_length=5)
    estado = models.CharField(max_length=255)
    municipio = models.CharField(max_length=255)
    geom = models.PointField(srid=4326, null=True, blank=True)

    def __str__(self):
        return f"{self.asociacion} ({self.nombre})"

    def save(self, *args, **kwargs):
        request = get_current_request()

        if request and request.user and request.user.is_authenticated:
            if request.user.is_staff:
                super(Centro, self).save(*args, **kwargs)
            else:
                request_user_vinculacionasociacion_rol = 'ninguno'
                try:
                    request_user_vinculacionasociacion_rol = VinculacionAsociacion.objects.get(user=request.user,
                                                                                         asociacion=self.asociacion).user_rol
                except Exception:
                    raise ProtectedError("Error recuperando autorización", self)
                #request_user_level = {'coordinador': 3, 'supervisor': 2, 'reclutador': 1, 'ninguno': 0}[
                #    request_user_vinculacionasociacion_rol]
                #if self.asociacion.esta_verificada:
                #    if request_user_level > 1:
                #        super(Centro, self).save(*args, **kwargs)
                #    else: raise ProtectedError("Tu nivel de usuario no permite esta acción. Nivel: "+str(request_user_level), self)
                #else: raise ProtectedError("La asociacion no está verificada", self)

                #Para tener una base solida de usuarios, se quita la validacion de niveles de acceso.
                super(Centro, self).save(*args, **kwargs) #!!!!!!!!!!!
        else:
            # Uncomment next line if you want to allow to create Centro objects from CLI without request
            # super(Centro, self).save(*args, **kwargs)
            # Comment next line and unncoment the previous one if you want to avoid creating Centro objects from CLI without request
            raise ProtectedError("No estas autenticado", self)

    class Meta:
        verbose_name = "Centro"
        verbose_name_plural = "Centros"
        ordering = ['nombre']


class VinculacionAsociacion(models.Model):
    """
    VinculacionAsociacion model
    """
    asociacion = models.ForeignKey(Asociacion, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    user_rol = models.CharField(max_length=30, default='reclutador', choices=(('', 'Rol de usuario'), ('coordinador', 'Coordinador'),('staff', 'Staff')))

    def __str__(self):
        return f"{self.asociacion} ({self.user} - {self.user_rol})"

    @receiver(post_save, sender=Asociacion)
    def crear_vinculacion_asociacion(sender, instance, created, **kwargs):
        if created:
            request = get_current_request()
            if request and request.user and request.user.is_authenticated and not request.user.is_staff:
                VinculacionAsociacion.objects.create(asociacion=instance, user=request.user, user_rol='staff')
                # TODO: Add a signal to delete the logo file when the asociacion is deleted
                # TODO: Set image path per asociacion

    def save(self, *args, **kwargs):
        request = get_current_request()
        self_obj = self
        if self.pk:
            self_obj = VinculacionAsociacion.objects.get(pk=self.pk)
            self.user = self_obj.user
            self.asociacion = self_obj.asociacion
        if request:
            if request.user.is_authenticated:
                if request.user.is_staff:
                    super(VinculacionAsociacion, self).save(*args, **kwargs)
                else:
                    request_user_vinculacionasociacion_rol = 'ninguno'
                    try:
                        request_user_vinculacionasociacion_rol = VinculacionAsociacion.objects.get(user=request.user,
                                                                                             asociacion=self.asociacion).user_rol
                    except Exception:
                        pass
                    request_user_level = {'coordinador': 2, 'staff': 1, 'ninguno': 0}[request_user_vinculacionasociacion_rol]
                    self_user_level = {'coordinador': 2, 'staff': 1}[self.user_rol]
                    if request_user_level < 2 and request.user == self.user:
                        self.user_rol = 'staff'
                        super(VinculacionAsociacion, self).save(*args, **kwargs)
                    elif request_user_level > 1 and request_user_level > self_user_level:
                        super(VinculacionAsociacion, self).save(*args, **kwargs)
                    else:
                        raise ProtectedError("No cuentas con permisos para realizar esta acción", self)
            else:
                raise ProtectedError("No cuentas con permisos para realizar esta acción", self)
        else:
            # Uncomment next line if you want to allow to create VinculacionAsociacion objects from CLI without request
            # super(VinculacionAsociacion, self).save(*args, **kwargs)
            # Comment next line and unncoment the previous one if you want to avoid creating VinculacionAsociacion objects from CLI without request
            raise ProtectedError("No cuentas con permisos para realizar esta acción", self)

    class Meta:
        verbose_name = "Vinculación a asociacion"
        verbose_name_plural = "Vinculaciones a asociaciones"
        ordering = ['id']
        unique_together = ('asociacion', 'user')
