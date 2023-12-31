from django.contrib.gis.db import models
from users.models import User
from asociaciones.models import Asociacion, Centro, VinculacionAsociacion
from base.models import Habilidad
from django.utils import timezone
from django.db.models import ProtectedError
from threadlocals.threadlocals import get_current_request
import django.utils 
from django.utils.html import mark_safe
from base.models import Servicio
from django.contrib import admin

# Create your models here.

def fecha_publicacion_fin():
    """
    Devuelve la fecha de publicación de un animal perdido
    """
    return (timezone.now() + timezone.timedelta(days=60)).date()


class AnimalCategoria(models.Model):
    """
    Categoría de animal

    Descripción: Define la categoría de un animal

    Ejemplo: Perro, Gato, Conejo, etc.

    Args:
        nombre (CharField): Nombre de la categoría
    """
    nombre = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.nombre

    class Meta:
        ordering = ['nombre']
        verbose_name = "Categoria de animal"
        verbose_name_plural = "Categorias de animales"

class AnimalCaracteristica(models.Model):
    """
    Característica de animal

    Descripción: Define una característica de un animal

    Ejemplo: Peludo, Orejas largas, etc.

    Args:
        nombre (CharField): Nombre de la característica
    """

    nombre = models.CharField(max_length=150, unique=True)

    def __str__(self):
        return self.nombre

    class Meta:
        ordering = ['id']

class Animal(models.Model):
    """Animal

    Descripción: Define un animal

    Attributes:
        nombre (CharField): Nombre del animal
        categoria (ForeignKey): Categoría del animal
        descripcion (TextField): Descripción del animal
        sexo (CharField): Sexo del animal
        fecha_recepcion (DateField): Fecha de recepción del animal
        fecha_nacimiento (DateField): Fecha de nacimiento del animal
        habilidades (ManyToManyField): Habilidades del animal
        caracteristicas (ManyToManyField): Características del animal
        foto (ImageField): Foto del animal
        señas_particulares (TextField): Señas particulares del animal
        talla (CharField): Talla del animal
        peso (IntegerField): Peso del animal
        altura_cruz (IntegerField): Altura a la cruz del animal
        longitud (IntegerField): Longitud del animal
        convivencia (ManyToManyField): Convivencia del animal
        sociable (BooleanField): Sociabilidad del animal
        apto_niños (BooleanField): Apto para niños del animal
        adiestramiento_observaciones (TextField): Observaciones de adiestramiento del animal
        servicios (ManyToManyField): Servicios del animal
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    asociacion = models.ForeignKey(Asociacion, on_delete=models.CASCADE)
    centro = models.ForeignKey(Centro, on_delete=models.CASCADE)

    nombre = models.CharField(max_length=140)
    categoria = models.ForeignKey(AnimalCategoria, related_name='categoria_animals', on_delete=models.PROTECT)
    descripcion = models.TextField()

    class Sexo(models.TextChoices):
        """
        Sexo de animal
        """
        macho = 'macho', 'Macho'
        hembra = 'hembra', 'Hembra'

    sexo = models.CharField(
        choices=Sexo.choices,
    )

    fecha_recepcion = models.DateField(auto_now_add=True)
    fecha_nacimiento = models.DateField(null=True, blank=True, default=django.utils.timezone.now)
    habilidades = models.ManyToManyField(Habilidad, blank=True)
    caracteristicas = models.ManyToManyField(AnimalCaracteristica, blank=True)
    foto = models.ImageField(max_length=255, null=True, blank=True)
    señas_particulares = models.TextField(null=True, blank=True)

    ###########################################################################

    class Talla(models.TextChoices):
        """
        Talla de animal
        """
        pequeno = 'pequeño', 'Pequeño'
        mediano = 'mediano', 'Mediano'
        grande = 'grande', 'Grande'

    talla = models.CharField(
        choices=Talla.choices,
    )

    peso = models.IntegerField(null=True, blank=True)

    altura_cruz = models.IntegerField(null=True, blank=True)

    longitud = models.IntegerField(null=True, blank=True)

    ###########################################################################

    convivencia = models.ManyToManyField(AnimalCategoria, related_name='convivencia_animals', blank=True)

    sociable = models.BooleanField(default=False)
    apto_niños = models.BooleanField(default=False)

    adiestramiento_observaciones = models.TextField(null=True, blank=True)

    ###########################################################################

    servicios = models.ManyToManyField(Servicio, through='Procedimiento')

    def __str__(self):
        return f"{self.nombre}"

    @property
    def FotoPreview(self):
        """
        Devuelve la foto del animal
        """
        if self.foto:
            return mark_safe('<img src="{}" style="max-width:200px; max-height:200px"/>'.format(self.foto.url))
        return ""

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
        ordering = ['nombre']
        verbose_name = "Animal"
        verbose_name_plural = "Animales"

class Procedimiento(models.Model):
    """
    Procedimiento (Modelo intermedio entre Animal y Servicio)

    Descripción: Define una relación entre un animal y un servicio

    Args:
        animal (ForeignKey): Animal al que se le aplica el procedimiento
        servicio (ForeignKey): Servicio que se le aplica al animal
        fecha_aplicacion (DateField): Fecha de aplicación del procedimiento
        asociacion (ForeignKey): Asociación que aplica el procedimiento
        centro (ForeignKey): Centro que aplica el procedimiento
        descripcion (TextField): Descripción del procedimiento
    """

    animal = models.ForeignKey(Animal, on_delete=models.CASCADE)
    servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE)
    fecha_aplicacion = models.DateField(default=django.utils.timezone.now)
    asociacion = models.ForeignKey(Asociacion, on_delete=models.CASCADE)
    centro = models.ForeignKey(Centro, on_delete=models.CASCADE)
    descripcion = models.TextField()

    def __str__(self):
        return f"[{self.servicio}] en [{self.fecha_aplicacion}] por [{self.asociacion}] a [{self.animal}]"

    class Meta:
        verbose_name = "Procedimiento"
        verbose_name_plural = "Procedimientos"

class ProcedimientoInline(admin.TabularInline):
    model = Procedimiento
    extra = 1  # Número de filas que se mostrarán.

class Adopcion(models.Model):

    animal = models.ForeignKey(Animal, on_delete=models.CASCADE)
    fecha_publicacion_inicio = models.DateField(auto_now_add=True)
    fecha_publicacion_fin = models.DateField(default=fecha_publicacion_fin)
    fecha_adopcion = models.DateField(null=True, editable=False)
    estatus_adopcion = models.BooleanField(null=True, default=False)  # None = pendiente, True = adoptado, False = no adoptado
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    adoptante = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='adoptante')  

    def __str__(self):
        return f"{self.animal} ({self.animal.asociacion})"

    def save(self, *args, **kwargs):
        self_obj = self
        if self.estatus_adopcion is True:
            self.fecha_adopcion = timezone.now().date()
            self.adoptante = self_obj.adoptante
        super(Adopcion, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Adopcion"
        verbose_name_plural = "Adopciones"

class PostulacionAdopcion(models.Model):
    """
    Postulación a adopción

    Descripción: Define una postulación a adopción

    Args:
        user (ForeignKey): Usuario que postula
        animal (ForeignKey): Animal al que se postula
        motivos (TextField): Motivos de la postulación
        fecha_postulacion (DateField): Fecha de postulación
        estatus_aceptacion_postulacion (BooleanField): Estatus de aceptación de la postulación
        fecha_evaluacion_postulacion (DateField): Fecha de evaluación de la postulación
        cuidados (TextField): Cuidados del animal
        espacio (TextField): Espacio del animal
        seguridad (BooleanField): Seguridad del animal
        techo (BooleanField): Techo del animal
        salida_calle (BooleanField): Salida a la calle del animal
        precauciones (TextField): Precauciones del animal
        destrozos (BooleanField): Destrozos del animal
        alimentacion (TextField): Alimentación del animal
        atencion_veterinaria (TextField): Atención veterinaria del animal
        enfermedades (BooleanField): Enfermedades del animal
        conservacion (TextField): Conservación del animal
        esterilizacion (BooleanField): Esterilización del animal
        consulta_seguimiento (BooleanField): Consulta de seguimiento del animal
        acuerdo (BooleanField): Acuerdo del animal
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE)

    motivos = models.TextField(null=True, blank=True)
    
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

class ReportePerdido(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE, null=True, blank=True)

    estatus = models.BooleanField(null=True, default=False)  # None = Desconocido, True = Encontrado, False = Perdido
    descripcion_hechos = models.TextField(null=True, blank=True)
    llamar_a = models.CharField(max_length=140, null=True, blank=True)
    fecha_reporte = models.DateField(auto_now_add=True)
    geom = models.PointField(null=True, blank=True)
    fecha_encontrado = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.user} ({self.animal})"

    def save(self, *args, **kwargs):
        if self.estatus is True:
            self.fecha_encontrado = timezone.now().date()
        super(ReportePerdido, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Reporte animal perdido"
        verbose_name_plural = "Reportes animales perdidos"
        unique_together = ('user', 'animal')

class ReporteCiudadanoPerdido(models.Model):
    
        user = models.ForeignKey(User, on_delete=models.CASCADE)
        
        nombre = models.CharField(max_length=32)
        foto = models.ImageField(max_length=255, null=True, blank=True)
        categoria = models.ForeignKey(AnimalCategoria, related_name='categoria_animals_ciudadano', on_delete=models.PROTECT)
        señas_particulares = models.TextField(null=True, blank=True)
        estatus = models.BooleanField(null=True, default=False)  # None = Desconocido, True = Encontrado, False = Perdido
        descripcion_hechos = models.TextField(null=True, blank=True)
        llamar_a = models.CharField(max_length=140, null=True, blank=True)
        fecha_reporte = models.DateField(auto_now_add=True)
        geom = models.PointField(null=True, blank=True)
        fecha_encontrado = models.DateField(null=True, blank=True)
    
        def __str__(self):
            return f"{self.user} ({self.animal})"
    
        def save(self, *args, **kwargs):
            if self.estatus is True:
                self.fecha_encontrado = timezone.now().date()
            super(ReporteCiudadanoPerdido, self).save(*args, **kwargs)
    
        class Meta:
            verbose_name = "Reporte animal perdido ciudadano "
            verbose_name_plural = "Reportes animales perdidos ciudadano"

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
