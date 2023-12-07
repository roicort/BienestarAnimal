from rest_framework import serializers
from drf_dynamic_fields import DynamicFieldsMixin

from .models import AnimalCategoria, AnimalCaracteristica, Animal, PostulacionAdopcion, AnimalFavorito, Adopcion, ReportePerdido, ReporteCiudadanoPerdido
from asociaciones.serializers import PubAsociacionSerializer, CentroSerializer
from asociaciones.models import Centro
from base.serializers import HabilidadSerializer
from users.models import User
from rest_framework import routers

class AnimalCategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnimalCategoria
        fields = '__all__'


class AnimalCaracteristicaSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnimalCaracteristica
        fields = '__all__'


class AnimalFavoritoSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        if self.context['request'].user == instance.user:
            return super().to_representation(instance)
        else:
            return None

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.exclude(animal=None)
        return queryset

    class Meta:
        model = AnimalFavorito
        fields = ['user', 'animal', 'id']


class AnimalMinSerializer(DynamicFieldsMixin, serializers.ModelSerializer):
    
    categoria_nombre = serializers.SerializerMethodField('get_animal_category')

    def get_animal_category(self, instance):
        categoria = instance.categoria.id
        animale_categoria = AnimalCategoria.objects.filter(id=categoria)
        serializer = AnimalCategoriaSerializer(animale_categoria, many=True, context=self.context)
        return serializer.data[0]['nombre']

    class Meta:
        model = Animal
        fields = '__all__'


class MiPostulacionAdopcionListSerializer(serializers.ModelSerializer):
    animal_info = AnimalMinSerializer(source='animal', read_only=True)

    def get_centro_vinculado(self, obj):
        request = self.context.get('request', None)
        if obj.animal and obj.animal.centro:
            centro = Centro.objects.filter(id=obj.animal.centro.id)
            if obj.estatus_aceptacion_postulacion:
                return CentroSerializer(centro, many=True).data

    centro_info = serializers.SerializerMethodField('get_centro_vinculado')

    class Meta:
        model = PostulacionAdopcion
        fields = '__all__'


class StaffAnimalSerializer(DynamicFieldsMixin, serializers.ModelSerializer):

    animal_favorito = serializers.SerializerMethodField('get_animal_favorito')
    postulado_info = serializers.SerializerMethodField('get_postulado_info')
    asociacion_info = PubAsociacionSerializer(source='asociacion', read_only=True)
    categoria_info = AnimalCategoriaSerializer(source='categoria', read_only=True)
    habilidades_info = HabilidadSerializer(source='habilidades', read_only=True, many=True)
    inclusiones_info = AnimalCaracteristicaSerializer(source='inclusiones', read_only=True, many=True)

    def get_animal_favorito(self, instance):
        user = self.context['request'].user
        animales_favoritos = AnimalFavorito.objects.filter(user=user, animal=instance)
        serializer = AnimalFavoritoSerializer(animales_favoritos, many=True, context=self.context)
        return serializer.data

    def get_postulado_info(self, instance):
        user = self.context['request'].user
        postulaciones = PostulacionAdopcion.objects.filter(user=user, animal=instance)
        serializer = PostulacionAdopcionSerializer(postulaciones, many=True, context=self.context)
        return serializer.data

    class Meta:
        model = Animal
        fields = '__all__'


class AnimalSerializer(DynamicFieldsMixin, serializers.ModelSerializer):

    animal_favorito = serializers.SerializerMethodField('get_animal_favorito')
    postulado_info = serializers.SerializerMethodField('get_postulado_info')
    asociacion_info = PubAsociacionSerializer(source='asociacion', read_only=True)
    categoria_info = AnimalCategoriaSerializer(source='categoria', read_only=True)
    habilidades_info = HabilidadSerializer(source='habilidades', read_only=True, many=True)
    inclusiones_info = AnimalCaracteristicaSerializer(source='inclusiones', read_only=True, many=True)

    def get_animal_favorito(self, instance):
        user = self.context['request'].user
        animales_favoritos = AnimalFavorito.objects.filter(user=user, animal=instance)
        serializer = AnimalFavoritoSerializer(animales_favoritos, many=True, context=self.context)
        return serializer.data

    def get_postulado_info(self, instance):
        user = self.context['request'].user
        postulaciones = PostulacionAdopcion.objects.filter(user=user, animal=instance)
        serializer = PostulacionAdopcionSerializer(postulaciones, many=True, context=self.context)
        return serializer.data

    class Meta:
        model = Animal
        fields = '__all__'

class AdopcionSerializer(serializers.ModelSerializer):

    animal_info = AnimalMinSerializer(source='animal', read_only=True)
    asociacion_info = serializers.SerializerMethodField('get_asociacion_info')
    categoria_info = serializers.SerializerMethodField('get_animal_category')

    def get_animal_category(self, instance):
        categoria = instance.animal.categoria
        return AnimalCategoriaSerializer(categoria).data

    def get_asociacion_info(self, instance):
        asociacion = instance.animal.asociacion
        return PubAsociacionSerializer(asociacion).data

    class Meta:
        model = Adopcion
        fields = '__all__'


class ReportePerdidoSerializer(serializers.ModelSerializer):

    animal_info = AnimalMinSerializer(source='animal', read_only=True)
    asociacion_info = serializers.SerializerMethodField('get_asociacion_info')
    def get_asociacion_info(self, instance):
        asociacion = instance.animal.asociacion
        return PubAsociacionSerializer(asociacion).data

    class Meta:
        model = ReportePerdido
        fields = '__all__'

class ReporteCiudadanoPerdidoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReporteCiudadanoPerdido
        fields = '__all__'

class PostulacionAdopcionSerializer(serializers.ModelSerializer):
    animal_info = AnimalMinSerializer(source='animal', read_only=True)

    class Meta:
        model = PostulacionAdopcion
        fields = '__all__'
        read_only_fields = ['user', 'animal', 'fecha_postulacion', 'fecha_revision']


class PostulacionAdopcionListCreateSerializer(serializers.ModelSerializer):
    animal_info = AnimalMinSerializer(source='animal', read_only=True)

    class Meta:
        model = PostulacionAdopcion
        fields = '__all__'
        read_only_fields = ['centro_info']


class AnimalFavoritoCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnimalFavorito
        exclude = ['user']
        read_only_fields = ['__all__']
