from django.db.models import Q
from rest_framework import viewsets, exceptions
from .models import AnimalCategoria, AnimalCaracteristica, Animal, PostulacionAdopcion, AnimalFavorito, ReportePerdido, Adopcion, ReporteCiudadanoPerdido
from .serializers import AnimalCategoriaSerializer, AnimalCaracteristicaSerializer, \
    StaffAnimalSerializer, AnimalSerializer, PostulacionAdopcionSerializer, PostulacionAdopcionListCreateSerializer, \
    AnimalFavoritoSerializer, AnimalFavoritoCreateSerializer, MiPostulacionAdopcionListSerializer, AdopcionSerializer, ReportePerdidoSerializer, ReporteCiudadanoPerdidoSerializer
from rest_framework import permissions
#from django.http import HttpResponse
from asociaciones.models import VinculacionAsociacion
from .permissions import IsStaffOrVinculacionAsociacionOrReadOnly
#from django.contrib.auth.models import User
from rest_framework import filters
#from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

class AnimalCategoriaViewSet(viewsets.ModelViewSet):
    queryset = AnimalCategoria.objects.all()
    serializer_class = AnimalCategoriaSerializer
    read_only_fields = ['__all__']

class AnimalCaracteristicaViewSet(viewsets.ModelViewSet):
    queryset = AnimalCaracteristica.objects.all()
    serializer_class = AnimalCaracteristicaSerializer
    read_only_fields = ['__all__']

class AnimalViewSet(viewsets.ModelViewSet):
    def get_serializer_class(self):
        if self.request.user.is_staff:
            return StaffAnimalSerializer
        else:
            return AnimalSerializer

    queryset = Animal.objects.all()
    permission_classes = [IsStaffOrVinculacionAsociacionOrReadOnly]
    filter_backends = [filters.SearchFilter,DjangoFilterBackend,filters.OrderingFilter]
    filterset_fields = ['categoria', 'asociacion']
    search_fields = ['nombre', 'descripcion']
    ordering_fields = ['fecha_nacimiento']


class AdopcionViewSet(viewsets.ModelViewSet):
    
    serializer_class = AdopcionSerializer
    queryset = Adopcion.objects.all()
    permission_classes = [IsStaffOrVinculacionAsociacionOrReadOnly]
    filter_backends = [filters.SearchFilter, DjangoFilterBackend,filters.OrderingFilter]
    search_fields = ['animal__nombre', 'animal__descripcion', 'animal__categoria__nombre', 'animal__asociacion__nombre']
    filterset_fields = ['animal__asociacion', 'animal__centro', 'animal__categoria']
    ordering_fields = ['fecha_publicacion_inicio']

class ReportePerdidoViewSet(viewsets.ModelViewSet):

    serializer_class = ReportePerdidoSerializer
    reportes_perdidos = ReportePerdido.objects.all()
    #queryset = Animal.objects.filter(id__in=reportes_perdidos.values_list('animal', flat=True))
    queryset = ReportePerdido.objects.all()
    permission_classes = [IsStaffOrVinculacionAsociacionOrReadOnly]
    filter_backends = [filters.SearchFilter,DjangoFilterBackend,filters.OrderingFilter]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class ReporteCiudadanoPerdidoViewSet(viewsets.ModelViewSet):

    serializer_class = ReporteCiudadanoPerdidoSerializer
    reportes_perdidos = ReportePerdido.objects.all()
    #queryset = Animal.objects.filter(id__in=reportes_perdidos.values_list('animal', flat=True))
    queryset = ReporteCiudadanoPerdido.objects.all()
    permission_classes = [IsStaffOrVinculacionAsociacionOrReadOnly]
    filter_backends = [filters.SearchFilter,DjangoFilterBackend,filters.OrderingFilter]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class PostulacionAdopcionViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        if self.request.user.is_staff:
            return PostulacionAdopcion.objects.all()
        elif self.request.user.is_authenticated:
            asociaciones_vinculadas = list(VinculacionAsociacion.objects.filter(user=self.request.user).values_list('asociacion', flat=True).distinct())
            animales_vinculados = list(PostulacionAdopcion.objects.filter(animal__asociacion__in=asociaciones_vinculadas).values_list('animal', flat=True).distinct())
            return PostulacionAdopcion.objects.filter(Q(animal__in=animales_vinculados))
        else:
            raise exceptions.PermissionDenied()

    def get_serializer_class(self):
        usuario_vinculado = VinculacionAsociacion.objects.filter(user=self.request.user).exists()
        if self.request.user.is_authenticated:
            if self.action == 'list' or self.action == 'create':
                return PostulacionAdopcionListCreateSerializer
            elif (self.action == 'retrieve' or self.action == 'update' or
                  self.action == 'partial_update' or self.action == 'destroy') \
                    and (usuario_vinculado or self.request.user.is_staff):
                print("self.action", self.action, "usuario_vinculado", usuario_vinculado, "self.request.user.is_staff",
                      self.request.user.is_staff)
                print('PostulacionAdopcionSerializer',PostulacionAdopcionSerializer)
                return PostulacionAdopcionSerializer
            else:
                raise exceptions.PermissionDenied()
        else:
            print("no autenticado")
            raise exceptions.PermissionDenied()

    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class MisPostulacionesAnimalViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        if self.request.user.is_authenticated:
            return PostulacionAdopcion.objects.filter(Q(user=self.request.user))
        else:
            raise exceptions.PermissionDenied()

    serializer_class = MiPostulacionAdopcionListSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        usuario_vinculado = VinculacionAsociacion.objects.filter(user=self.request.user).exists()
        if self.request.user.is_authenticated:
            if self.action == 'list' or self.action == 'create':
                return PostulacionAdopcionListCreateSerializer
            elif (self.action == 'retrieve' or self.action == 'update' or
                  self.action == 'partial_update' or self.action == 'destroy') \
                    and (usuario_vinculado or self.request.user.is_staff):
                print("self.action", self.action, "usuario_vinculado", usuario_vinculado, "self.request.user.is_staff",
                      self.request.user.is_staff)
                print('PostulacionAdopcionSerializer',PostulacionAdopcionSerializer)
                return PostulacionAdopcionSerializer
            else:
                raise exceptions.PermissionDenied()
        else:
            print("no autenticado")
            raise exceptions.PermissionDenied()

    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class AnimalFavoritoViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        if self.request.user.is_authenticated:
            query = AnimalFavorito.objects.filter(user=self.request.user)
            return query
        else:
            raise exceptions.PermissionDenied()

    def get_serializer_class(self):
        #return AnimalFavoritoSerializer
        if self.request.user.is_authenticated:
            if self.action == 'create':
                return AnimalFavoritoCreateSerializer
            elif self.action == 'list' or self.action == 'retrieve' or self.action == 'destroy' or self.action == 'update' or self.action == 'partial_update':
                return AnimalFavoritoSerializer
            else:
                raise exceptions.PermissionDenied()
        else:
            raise exceptions.PermissionDenied()
    
    filterset_fields = ['animal']
    permission_classes = [permissions.IsAuthenticated]
    #permission_classes = [permissions.AllowAny]