from django.db import models

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils import timezone
from django.conf import settings
import uuid
from django.contrib.admin.models import LogEntry as BaseLogEntry
from django.contrib.admin.models import DELETION, LogEntry, ADDITION, CHANGE

class Sala(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255, null=False)

class Mensaje(models.Model):
    id = models.AutoField(primary_key=True)
    miSala = models.ForeignKey(Sala, on_delete=models.CASCADE)
    miUsuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    texto = models.CharField(max_length=10000, null=False)
    fecha = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['fecha']

class CustomToken(models.Model):
    key = models.CharField(max_length=40, primary_key=True, default=uuid.uuid4)
    usuario = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='custom_token', on_delete=models.CASCADE)
    created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.key


class UsuarioManager(BaseUserManager):
    def create_user(self, correo, nombre, contrasegna, **extra_fields):
        if not correo:
            raise ValueError('El correo electrónico es obligatorio')
        email = self.normalize_email(correo)
        usuario = self.model(correo=email, nombre=nombre,contrasegna = contrasegna, **extra_fields)
        usuario.set_password(contrasegna)
        usuario.save(using=self._db)
        return usuario

    def create_superuser(self, correo, nombre, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(correo, nombre, password, **extra_fields)

class Usuario(AbstractBaseUser):
    correo = models.CharField(max_length=255, primary_key=True, unique=True)
    nombre = models.CharField(max_length=255, null=False)
    sexo = models.CharField(max_length=255, blank=True)
    nacimiento = models.DateField(blank=True, null=True)
    contrasegna = models.CharField(max_length=255, null=False)
    pais = models.CharField(max_length=255, blank=True)
    ultima_cancion = models.ForeignKey('Cancion', on_delete=models.SET_NULL, related_name='ultima_cancion', null=True)
    ultima_minutos = models.IntegerField(default=0)
    #generos_favoritos = models.ManyToManyField('Genero', related_name='generos_favoritos')
    #artistas_favoritos = models.ManyToManyField('Artista', related_name='artistas_favoritos')


    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    # para el correo de verificación
    is_email_verified = models.BooleanField(default=False)

    objects = UsuarioManager()

    USERNAME_FIELD = 'correo'
    REQUIRED_FIELDS = ['nombre']

    def __str__(self):
        return self.correo

    def has_perm(self, perm, obj=None):
        return self.is_staff

    def has_module_perms(self, app_label):
        return self.is_staff


#class Amigo(models.Model):
#    micorreo1 = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='amigos1')
#    micorreo2 = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='amigos2')
#    class Meta:
#        unique_together = ('micorreo1', 'micorreo2',)

class Seguido(models.Model):
    miUsuarioSeguido = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='miUsuarioSeguido')
    seguido = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='seguido')
    class Meta:
        unique_together = ('miUsuarioSeguido', 'seguido')

class Seguidor(models.Model):
    miUsuarioSeguidor = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='miUsuarioSeguidor')
    seguidor = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='seguidor')
    class Meta:
        unique_together = ('miUsuarioSeguidor', 'seguidor')

class Playlist(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255, null=False)
    publica = models.BooleanField(null=False)


class Album(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255, null=False)
    foto = models.BinaryField(default=b'\x00')


class Presentador(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255, null=False)
    foto = models.BinaryField(default=b'\x00')
    descripcion = models.CharField(max_length=500, null=True)

class Artista(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255, null=False)
    foto = models.BinaryField(default=b'\x00')
    descripcion = models.CharField(max_length=500, null=True)

class Cancion(models.Model):
    id = models.AutoField(primary_key=True)
    miAlbum = models.ForeignKey(Album, on_delete=models.CASCADE,null = True)
    puntuacion = models.IntegerField(blank=True, null=True)
    numPuntuaciones = models.IntegerField(blank=True, null=True)
    nombre = models.CharField(max_length=255, null=False)
    archivoMp3 = models.BinaryField(default=b'\x00')
    foto = models.BinaryField(default=b'\x00')


class Colabora(models.Model):
    miUsuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='playlists_colaboradas')
    miPlaylist = models.ForeignKey(Playlist, on_delete=models.CASCADE, related_name='colaboradores')

    class Meta:
        unique_together = ('miUsuario', 'miPlaylist',)

class Contiene(models.Model):
    miAudio = models.ForeignKey(Cancion, on_delete=models.CASCADE, related_name='playlists_que_lo_contienen')
    miPlaylist = models.ForeignKey(Playlist, on_delete=models.CASCADE, related_name='audios_contenidos')

    class Meta:
        unique_together = ('miAudio', 'miPlaylist',)


class Historial(models.Model):
    id = models.AutoField(primary_key=True)
    miUsuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='historial_escucha')
    miAudio = models.ForeignKey(Cancion, on_delete=models.CASCADE, related_name='veces_escuchado')


class Cola(models.Model):
    id = models.AutoField(primary_key=True)
    miUsuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    miAudio = models.ForeignKey(Cancion, on_delete=models.CASCADE)


class Genero(models.Model):
    nombre = models.CharField(max_length=255, primary_key=True)


class Pertenecen(models.Model):
    miGenero = models.ForeignKey(Genero, on_delete=models.CASCADE)
    miAudio = models.ForeignKey(Cancion, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=255, null=False)

    class Meta:
        unique_together = ('miGenero', 'miAudio', 'tipo',)

class Podcast(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255, null=False)
    puntuacion = models.IntegerField(blank=True, null=True)
    numPuntuaciones = models.IntegerField(blank=True, null=True)
    foto = models.BinaryField(default=b'\x00')

class Capitulo(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255, null=False)
    descripcion = models.CharField(max_length=255, blank=True)
    miPodcast = models.ForeignKey(Podcast, on_delete=models.CASCADE, related_name='capitulos')
    archivoMp3 = models.BinaryField(default=b'\x00')

class Cantan(models.Model):
    id = models.AutoField(primary_key=True)
    miArtista = models.ForeignKey(Artista, on_delete=models.CASCADE)
    miCancion = models.ForeignKey(Cancion, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('miArtista', 'miCancion',)

class Interpretan(models.Model):
    id = models.AutoField(primary_key=True)
    miPresentador = models.ForeignKey(Presentador, on_delete=models.CASCADE)
    miPodcast = models.ForeignKey(Podcast, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('miPresentador', 'miPodcast',)

#class PuntuaCancion(models.Model):
#    id = models.AutoField(primary_key=True)
#    miUsuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
#    miCancion = models.ForeignKey(Cancion, on_delete=models.CASCADE)
#    puntuacion = models.IntegerField(null=False)

#class PuntuaPodcast(models.Model):
#    id = models.AutoField(primary_key=True)
#    miUsuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
#    miPodcast = models.ForeignKey(Podcast, on_delete=models.CASCADE)
#    puntuacion = models.IntegerField(null=False)

