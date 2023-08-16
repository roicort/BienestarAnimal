from rest_framework import serializers
from .models import Habilidad

# Create your serializers here.

class HabilidadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habilidad
        fields = '__all__'



