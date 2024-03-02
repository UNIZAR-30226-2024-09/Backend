from django.db import models

class Usuario(models.Model):
    correo = models.CharField(max_length=255, primary_key=True)
    nombre = models.CharField(max_length=255, null=False)
    sexo = models.CharField(max_length=255, blank=True)
    nacimiento = models.DateField(blank=True, null=True)
    contrasegna = models.CharField(max_length=255, null=False)
    pais = models.CharField(max_length=255, blank=True)

class Amigo(models.Model):
    micorreo1 = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='amigos1')
    micorreo2 = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='amigos2')

    class Meta:
        unique_together = ('micorreo1', 'micorreo2',)


class Playlist(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255, null=False)
    publica = models.BooleanField(null=False)


class Colabora(models.Model):
    miUsuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='playlists_colaboradas')
    miPlaylist = models.ForeignKey(Playlist, on_delete=models.CASCADE, related_name='colaboradores')

    class Meta:
        unique_together = ('miUsuario', 'miPlaylist',)


class Audio(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255, null=False)
    # Removed "audio" field as it's not defined in the schema.
    puntuacion = models.IntegerField(blank=True, null=True)


class Contiene(models.Model):
    miAudio = models.ForeignKey(Audio, on_delete=models.CASCADE, related_name='playlists_que_lo_contienen')
    miPlaylist = models.ForeignKey(Playlist, on_delete=models.CASCADE, related_name='audios_contenidos')

    class Meta:
        unique_together = ('miAudio', 'miPlaylist',)


class Historial(models.Model):
    id = models.AutoField(primary_key=True)
    miUsuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='historial_escucha')
    miAudio = models.ForeignKey(Audio, on_delete=models.CASCADE, related_name='veces_escuchado')


class Favorito(models.Model):
    miUsuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='audios_favoritos')
    miAudio = models.ForeignKey(Audio, on_delete=models.CASCADE, related_name='veces_marcado_favorito')

    class Meta:
        unique_together = ('miUsuario', 'miAudio',)


class Cola(models.Model):
    id = models.AutoField(primary_key=True)
    miUsuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    miAudio = models.ForeignKey(Audio, on_delete=models.CASCADE)


class Genero(models.Model):
    nombre = models.CharField(max_length=255, primary_key=True)


class Pertenecen(models.Model):
    id = models.AutoField(primary_key=True)
    miGenero = models.ForeignKey(Genero, on_delete=models.CASCADE)
    miAudio = models.ForeignKey(Audio, on_delete=models.CASCADE)


class Album(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255, null=False)


class Cancion(models.Model):
    id = models.AutoField(primary_key=True)
    letra = models.CharField(max_length=255, null=False)
    cantantes = models.CharField(max_length=255, null = False)
    miAlbum = models.ForeignKey(Album, on_delete=models.CASCADE)


class Podcast(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255, null=False)
    presentadores = models.CharField(max_length=255, null=False)


class Capitulo(models.Model):
    id = models.AutoField(primary_key=True)
    descripcion = models.CharField(max_length=255, blank=True)
    miPodcast = models.ForeignKey(Podcast, on_delete=models.CASCADE, related_name='capitulos')

