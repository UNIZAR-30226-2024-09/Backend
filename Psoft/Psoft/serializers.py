from rest_framework import serializers
from Musify import models

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Usuario
        fields = ['correo', 'nombre', 'sexo', 'nacimiento', 'contrasegna', 'pais']

class FriendsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Amigo
        fields = ['micorreo1', 'micorreo2']

class SongsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Cancion
    fields = ['nombre', 'cantantes', 'miAlbum']