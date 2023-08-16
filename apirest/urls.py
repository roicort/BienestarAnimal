from django.urls import include, path
from rest_framework import routers
drf_router = routers.DefaultRouter()

urlpatterns = [
    path(r'users/', include('users.urls')),
    path(r'base/', include('base.urls')),
    path(r'animales/', include('animales.urls')),
    path(r'perfiles/', include('perfiles.urls')),
    path(r'asociaciones/', include('asociaciones.urls')),
]

urlpatterns += drf_router.urls
