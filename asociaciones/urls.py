from apirest.urls import drf_router
from django.urls import path
from .viewsets import *

urlpatterns = []

drf_router.register(r'asociaciones/asociacion', AsociacionViewSet, basename='asociaciones-empresa')
drf_router.register(r'asociaciones/centro', CentroViewSet, basename='asociaciones-sucursal')
drf_router.register(r'asociaciones/vinculacion-asociacion', VinculacionAsociacionViewSet, basename='asociaciones-vinculacion-asociacion')

urlpatterns += drf_router.urls
