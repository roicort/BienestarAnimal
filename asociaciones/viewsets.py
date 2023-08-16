from django.db.models import Q
from rest_framework import viewsets, exceptions
from rest_framework.parsers import MultiPartParser, JSONParser
from .models import Asociacion, Centro, VinculacionAsociacion
from .permissions import IsStaffOrVinculoAsociacion, IsStaffOrCoordinadorAsociacionOrReadOnly
from .serializers import StaffAsociacionSerializer, UserAsociacionSerializer, PubAsociacionSerializer, CentroSerializer, \
    StaffVinculacionAsociacionSerializer, UserVinculacionAsociacionSerializer
from django.http import HttpResponse, JsonResponse
from .models import VinculacionAsociacion


# Add your viewsets here


class AsociacionViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows asociaciones to be viewed only.
    """

    def get_serializer_class(self):
        if self.request.user.is_staff:
            return StaffAsociacionSerializer
        elif self.request.user.is_authenticated:
            return UserAsociacionSerializer
        else:
            return PubAsociacionSerializer

    queryset = Asociacion.objects.all()
    # permission_classes = [IsStaffOrCoordinadorAsociacionOrReadOnly]
    permission_classes = [IsStaffOrVinculoAsociacion]
    parser_classes = (MultiPartParser, JSONParser)


class CentroViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows asociaciones to be viewed only.
    """

    serializer_class = CentroSerializer
    queryset = Centro.objects.all()
    # permission_classes = [IsStaffOrCoordinadorAsociacionOrReadOnly]
    permission_classes = [IsStaffOrVinculoAsociacion]


class VinculacionAsociacionViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows asociaciones to be viewed only.
    """

    def get_serializer_class(self):
        if self.request.user.is_staff:
            return StaffVinculacionAsociacionSerializer
        elif self.request.user.is_authenticated:
            return UserVinculacionAsociacionSerializer
        else:
            raise exceptions.PermissionDenied('Forbidden')

    def get_queryset(self):
        if self.request.user.is_staff:
            return VinculacionAsociacion.objects.all()
        elif self.request.user.is_authenticated:
            asociaciones_coordinador = VinculacionAsociacion.objects.filter(user=self.request.user,
                                                                     user_rol='coordinador').values_list('asociacion',
                                                                                                         flat=True)
            asociaciones_supervisor = VinculacionAsociacion.objects.filter(user=self.request.user,
                                                                    user_rol='supervisor').values_list('asociacion',
                                                                                                       flat=True)
            return VinculacionAsociacion.objects.filter(
                Q(user=self.request.user) | Q(empresa__in=asociaciones_coordinador) | Q(empresa__in=asociaciones_supervisor))
        else:
            return HttpResponse('Unauthorized', status=401)

    permission_classes = [IsStaffOrVinculoAsociacion]

    filterset_fields = ['user']



