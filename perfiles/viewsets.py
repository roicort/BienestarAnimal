from rest_framework import viewsets
from django.db.models import Q
from rest_framework.parsers import MultiPartParser
from rest_framework import exceptions
from rest_framework.permissions import IsAuthenticated
from asociaciones.models import VinculacionAsociacion
from asociaciones.serializers import PubAsociacionSerializer
from animales.models import PostulacionAdopcion
from .models import PerfilGeneral
from .serializers import PerfilGeneralSerializer, PerfilGeneralAsociadoSerializer

# Create your views here.

class PerfilGeneralViewSet(viewsets.ModelViewSet):

    def get_queryset(self):
        if self.request.user.is_staff:
            return PerfilGeneral.objects.all()
        elif self.request.user.is_authenticated:
            asociaciones_vinculadas = list(VinculacionAsociacion.objects.filter(user=self.request.user).values_list('asociacion', flat=True))
            usuarios_postulaciones_asociaciones_vinculadas = list(PostulacionAdopcion.objects.filter(animal__asociacion__in=asociaciones_vinculadas).values_list('user', flat=True))
            return PerfilGeneral.objects.filter(Q(user=self.request.user) | Q(user__in=usuarios_postulaciones_asociaciones_vinculadas))
        else:
            raise exceptions.PermissionDenied('Forbidden')

    def get_serializer_class(self):
        if self.request.user.is_staff:
            return PerfilGeneralSerializer
        elif self.request.user.is_authenticated:
            return PerfilGeneralAsociadoSerializer

    # serializer_class = PerfilGeneralSerializer
    permission_classes = [IsAuthenticated]