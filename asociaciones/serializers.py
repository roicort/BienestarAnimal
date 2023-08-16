from rest_framework import serializers
from .models import *

#


class PubAsociacionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Asociacion
        fields = '__all__'
        read_only_fields = ['__all__']


class UserAsociacionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Asociacion
        fields = '__all__'
        read_only_fields = ['esta_verificada']


class StaffAsociacionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Asociacion
        fields = '__all__'


class CentroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Centro
        fields = '__all__'


class UserVinculacionAsociacionSerializer(serializers.ModelSerializer):
    asociacion_info = UserAsociacionSerializer(source='asociacion', read_only=True)
    class Meta:
        model = VinculacionAsociacion
        fields = '__all__'
        read_only_fields = ['esta_verificada']


class StaffVinculacionAsociacionSerializer(serializers.ModelSerializer):
    asociacion_info = UserAsociacionSerializer(source='asociacion', read_only=True)
    class Meta:
        model = VinculacionAsociacion
        fields = '__all__'
