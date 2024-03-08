from rest_framework import serializers
from Musify.models import Usuario

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['correo', 'nombre', 'sexo', 'nacimiento', 'contrasegna', 'pais']
