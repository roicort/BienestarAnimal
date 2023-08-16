from apirest.urls import drf_router
from .viewsets import *

#

urlpatterns = []

drf_router.register(r'perfiles/perfil-general', PerfilGeneralViewSet, basename='perfiles-perfil-general')

urlpatterns += drf_router.urls
