from rest_framework import viewsets
from apirest.permissions import IsAdminOrReadOnly
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Habilidad
from .serializers import HabilidadSerializer

# Create your views here.


class HabilidadViewSet(viewsets.ModelViewSet):
    queryset = Habilidad.objects.all()
    serializer_class = HabilidadSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
