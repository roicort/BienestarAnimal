from django.contrib.gis.db import models
from users.models import User
from asociaciones.models import Asociacion, Centro, VinculacionAsociacion
from base.models import Habilidad
from django.utils import timezone
from django.db.models import ProtectedError
from threadlocals.threadlocals import get_current_request


# Create your models here.


def fecha_publicacion_fin():
    return (timezone.now() + timezone.timedelta(days=60)).date()


class AnimalCategoria(models.Model):
    nombre = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.nombre

    class Meta:
        ordering = ['nombre']
        verbose_name = "Categoria de animal"
        verbose_name_plural = "Categorias de animales"


class AnimalInclusion(models.Model):
    nombre = models.CharField(max_length=150, unique=True)

    def __str__(self):
        return self.nombre

    class Meta:
        ordering = ['id']


class Animal(models.Model):

    nombre = models.CharField(max_length=140)
    categoria = models.ForeignKey(AnimalCategoria, on_delete=models.PROTECT)
    descripcion = models.TextField()
    sexo = models.CharField(max_length=32, choices=(
        ('macho', 'Macho'), ('hembra', 'Hembra')))
    edad = models.CharField(max_length=32, null=True, blank=True, verbose_name="Edad aproximada")
    habilidades = models.ManyToManyField(Habilidad, blank=True)
    apto_niños = models.BooleanField(default=False)
    inclusiones = models.ManyToManyField(AnimalInclusion, blank=True)
    fecha_publicacion_inicio = models.DateField(auto_now_add=True, editable=False)
    fecha_publicacion_fin = models.DateField(default=fecha_publicacion_fin, editable=False)
    asociacion = models.ForeignKey(Asociacion, on_delete=models.PROTECT)
    centro = models.ForeignKey(Centro, on_delete=models.PROTECT)
    foto = models.ImageField(max_length=255, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.nombre}"

    def save(self, *args, **kwargs):
        request = get_current_request()
        if request:
            if request.user.is_authenticated:
                if request.user.is_staff:
                    self.user = request.user if not self.user else self.user
                    super(Animal, self).save(*args, **kwargs)
                else:
                    tiene_vinculo_asociacion = VinculacionAsociacion.objects.filter(user=request.user, asociacion=self.asociacion).exists()
                    if tiene_vinculo_asociacion:
                        self.user = request.user
                        super(Animal, self).save(*args, **kwargs)
                    else:
                        raise ProtectedError("No tiene permisos para modificar este animal", self)
        else:
            raise ProtectedError("No tiene permisos para modificar este animal", self)

    class Meta:
        ordering = ['fecha_publicacion_inicio']
        verbose_name = "Animal"
        verbose_name_plural = "Animales"


class PostulacionAdopcion(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE)
    
    fecha_postulacion = models.DateField(auto_now_add=True)
    estatus_aceptacion_postulacion = models.BooleanField(null=True,
                                              default=None)  # None = pendiente, True = aceptada, False = rechazada
    fecha_evaluacion_postulacion = models.DateField(null=True, editable=False)

    cuidados = models.TextField(null=True, blank=True)
    espacio = models.TextField(null=True, blank=True)
    seguridad = models.BooleanField(null=True, blank=True)
    techo = models.BooleanField(null=True, blank=True)
    salida_calle = models.BooleanField(null=True, blank=True)
    precauciones = models.TextField(null=True, blank=True)
    destrozos = models.BooleanField(null=True, blank=True)
    alimentacion = models.TextField(null=True, blank=True)
    atencion_veterinaria = models.TextField(null=True, blank=True)
    enfermedades = models.BooleanField(null=True, blank=True)
    conservacion = models.TextField(null=True, blank=True)
    esterilizacion = models.BooleanField(null=True, blank=True)
    consulta_seguimiento = models.BooleanField(null=True, blank=True)
    acuerdo = models.BooleanField(null=True, blank=True)


    def __str__(self):
        return f"{self.user} ({self.animal}) ({self.fecha_postulacion})"

    def save(self, *args, **kwargs):
        self_obj = self
        if self.id:
            self_obj = PostulacionAdopcion.objects.get(id=self.id)
            self.user = self_obj.user
            self.animal = self_obj.animal
            self.fecha_postulacion = self_obj.fecha_postulacion
        if self.estatus_aceptacion_postulacion is not None:
            self.fecha_evaluacion_postulacion = timezone.now().date()
        super(PostulacionAdopcion, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Postulación a adopcion"
        verbose_name_plural = "Postulaciones a adopciones"
        unique_together = ('user', 'animal')


class AnimalFavorito(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='animales_favoritos')
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE, related_name='animales_favoritos')

    class Meta:
        verbose_name = "Animal favorito"
        verbose_name_plural = "Animales favoritos"
        unique_together = ['user', 'animal']

    def __str__(self):
        return f"{self.user} ({self.animal})"

    def save(self, *args, **kwargs):
        request = get_current_request()
        if request:
            self.user = request.user
            super(AnimalFavorito, self).save(*args, **kwargs)
        else:
            raise ProtectedError("No tiene permisos para modificar este objeto", self)

    def delete(self, *args, **kwargs):
        # Delete associated AnimalFavorito instances
        # Call the superclass's delete method to delete the Animal instance
        request = get_current_request()
        if request:
            self.user = request.user
            super(AnimalFavorito, self).delete(*args, **kwargs)