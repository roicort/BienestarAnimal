from rest_framework import serializers
from .models import *
from django.contrib.auth.models import Permission
from drf_dynamic_fields import DynamicFieldsMixin

from asociaciones.models import VinculacionAsociacion
from asociaciones.serializers import UserVinculacionAsociacionSerializer

class PerfilGeneralSerializer(serializers.ModelSerializer):
    class Meta:
        model = PerfilGeneral
        fields = '__all__'
        read_only_fields = ['user']

class PerfilGeneralAsociadoSerializer(serializers.ModelSerializer):
    
    def get_asociaciones_vinculadas(self, obj):
        request = self.context.get('request', None)
        if request:
            vinculaciones = VinculacionAsociacion.objects.filter(user=request.user)
            return UserVinculacionAsociacionSerializer(vinculaciones, many=True).data
        return None

    vinculaciones_asociaciones = serializers.SerializerMethodField('get_asociaciones_vinculadas')

    class Meta:
        model = PerfilGeneral
        fields = '__all__'
        read_only_fields = ['user','vinculaciones_asociaciones']