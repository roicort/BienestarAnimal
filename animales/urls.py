from apirest.urls import drf_router
from .viewsets import *


urlpatterns = []

drf_router.register(r'animales/animal-categoria', AnimalCategoriaViewSet, basename='empleos-animal-categoria')
drf_router.register(r'animales/animal-inclusion', AnimalInclusionViewSet, basename='empleos-animal-inclusion')
drf_router.register(r'animales/animal', AnimalViewSet, basename='empleos-animal')
drf_router.register(r'animales/postulacion-adopcion', PostulacionAdopcionViewSet, basename='empleos-postulacion-animal')
drf_router.register(r'animales/mis-postulaciones', MisPostulacionesAnimalViewSet, basename='mis-postulacion-animal')
drf_router.register(r'animales/animal-favorito', AnimalFavoritoViewSet, basename='empleos-animal-favorita')

urlpatterns += drf_router.urls
