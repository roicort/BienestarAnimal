from apirest.urls import drf_router
from .viewsets import HabilidadViewSet
#

urlpatterns = []

drf_router.register(r'base/habilidad', HabilidadViewSet, basename='base-habilidad')

urlpatterns += drf_router.urls
