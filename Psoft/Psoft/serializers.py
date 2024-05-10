from rest_framework import serializers
from Musify import models

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Usuario
        fields = ['correo', 'nombre', 'sexo', 'nacimiento', 'contrasegna', 'pais']

class MensajeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Mensaje
        fields = ['id', 'miSala', 'miUsuario', 'texto', 'fecha']

#class AmigosSerializer(serializers.ModelSerializer):
#    class Meta:
#        model = models.Amigo
#        fields = ['micorreo1','micorreo2']
class EstadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Usuario
        fields = ['correo', 'ultima_cancion', 'ultima_minutos']

class SeguidoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Seguido
        fields = ['miUsuarioSeguido','seguido']

class SeguidorSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Seguidor
        fields = ['seguidor','miUsuarioSeguidor']

class PlaylistSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Playlist
        fields = ['id', 'nombre', 'publica']

class CancionSinAudioSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Cancion
        fields = ['id', 'nombre', 'miAlbum', 'puntuacion']

class CancionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Cancion
        fields = ['id', 'nombre', 'miAlbum', 'puntuacion', 'archivoMp3']

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
        fields = ['id', 'nombre']

class AlbumSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Album
        fields = ['id', 'nombre']

class ArtistaSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Artista
        fields = ['id', 'nombre', 'descripcion']

class PresentadorSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Artista
        fields = ['id', 'nombre', 'descripcion']

class GeneroSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Genero
        fields = ['nombre']

class SalaSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Sala
        fields = ['id', 'nombre']

