from rest_framework import serializers
from .models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tarea
        fields = '__all__'

    def validate_titulo(self, value):
        # Validación personalizada para el campo 'titulo'
        if not value:
            raise serializers.ValidationError("El título no puede estar vacío.")
        return value

    def validate_descripcion(self, value):
        # Validación personalizada para el campo 'descripcion'
        if not value:
            raise serializers.ValidationError("La descripción no puede estar vacía.")
        return value

    def validate_estado(self, value):
        # Validación personalizada para el campo 'estado'
        choices = dict(Tarea.ESTADO_CHOICES)
        if value not in choices:
            raise serializers.ValidationError(f"El estado debe ser uno de los siguientes valores: {', '.join(choices.keys())}.")
        return value