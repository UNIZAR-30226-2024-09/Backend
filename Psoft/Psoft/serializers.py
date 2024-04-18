from rest_framework import serializers
from Musify import models

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Usuario
        fields = ['correo', 'nombre', 'sexo', 'nacimiento', 'contrasegna', 'pais']

class AmigosSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Amigo
        fields = ['micorreo1','micorreo2']

class PlaylistSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Playlist
        fields = ['id', 'nombre', 'publica']

class CancionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Cancion
        fields = ['id', 'nombre', 'cantantes', 'miAlbum', 'puntuacion', 'archivo_mp3', 'foto', 'favorito']

# este, de momento, no se usa así que igual se podrá quitar
class HistorialSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Historial
        fields = ['miUsuario', 'miAudio']

# este, de momento, no se usa así que igual se podrá quitar
class ColaSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Cola
        fields = ['miUsuario', 'miAudio']

class CapituloSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Capitulo
        fields = ['id', 'nombre', 'descripcion', 'miPodcast']

class PodcastSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Podcast
        fields = ['id', 'nombre', 'presentadores', 'favorito']

class AlbumSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Album
        fields = ['id', 'nombre']

class ArtistaSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Artista
        fields = ['id', 'nombre', 'descripcion']


