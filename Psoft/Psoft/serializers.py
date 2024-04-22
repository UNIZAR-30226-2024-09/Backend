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
        fields = ['id', 'nombre', 'miAlbum', 'puntuacion', 'archivoMp3', 'foto']

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
        fields = ['id', 'nombre', 'descripcion', 'miPodcast', 'archivoMp3']

class PodcastSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Podcast
        fields = ['id', 'nombre', 'presentadores', 'favorito', 'foto']

class AlbumSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Album
        fields = ['id', 'nombre', 'foto']

class ArtistaSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Artista
        fields = ['id', 'nombre', 'descripcion', 'foto']

class PresentadorSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Artista
        fields = ['id', 'nombre', 'descripcion', 'foto']


