from rest_framework import serializers
from .models import *
from django.contrib.auth.models import Permission


#


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ['password', 'first_name', 'last_name', 'is_superuser', 'user_permissions', 'safe_delete',
                   'is_active']
        read_only_fields = ['last_login', 'username', 'date_joined', 'email', 'groups', 'is_staff']


class AdminUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # fields = ['url', 'username', 'email', 'groups']
        # fields = '__all__'
        exclude = ['password', 'first_name', 'last_name']


class GrupoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'


class PermisoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = '__all__'
