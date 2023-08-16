from apirest.urls import drf_router
from django.urls import path
from .viewsets import *

#

urlpatterns = []

drf_router.register(r'users/user', UserViewSet, basename='users-user')

urlpatterns += drf_router.urls
