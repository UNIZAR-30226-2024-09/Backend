from django.db import connection  # Assuming you're using Django

from .models import Usuario, Amigo, Playlist, Colabora, Contiene, Historial, Cancion, Podcast, Capitulo ,Cola, Genero, Pertenecen, Album, Artista, Cantan
from django.core.exceptions import ObjectDoesNotExist

#DAOs DE ARTISTA

def crearArtista(artistaVO): #Se crea el artista
    Artista.objects.create(nombre=artistaVO.nombre, descripcion=artistaVO.descripcion)

def conseguirArtistaPorId(artistaId): #Devuelve el artista dado su id
    try:
        return Artista.objects.get(pk=artistaId)
    except ObjectDoesNotExist:
        return None

def conseguirArtistaPorNombre(nombre): #Devuelve el artista dado su nombre
    try:
        return Artista.objects.get(nombre=nombre)
    except ObjectDoesNotExist:
        return None
    
def buscarArtista(nombre):
    try:
        nombre = nombre.lower()
        return Artista.objects.filter(nombre__istartswith=nombre)
    except ObjectDoesNotExist:
        return None



#DAOs DE USUARIO

# COMPROBADO
def conseguirUsuarioPorCorreo(correo): #Se busca el usuario por su correo
    try:
        return Usuario.objects.get(correo=correo)
    except ObjectDoesNotExist:
        return None

# COMPROBAD0
def comprobarContrasegna(correo, contrasegna): #se comprueba la contraseña del usuario (iniciar sesión)
    usuario = Usuario.objects.get(correo=correo)
    return usuario.contrasegna == contrasegna

# COMPROBADO
# EN LA API
def crearUsuario(usuarioVO): #Se crea el usuario sin amigos
    return Usuario.objects.create(
        correo=(usuarioVO.correo).lower(), #Se guarda en minusculas ya que en el correo electronico no importa la capitalizacion
        nombre=usuarioVO.nombre,
        contrasegna=usuarioVO.contrasegna,
        nacimiento=usuarioVO.nacimiento,
        sexo=usuarioVO.sexo,
        pais=usuarioVO.pais
    )

# COMPROBADO
def existeUsuario(correo): #Devuelve true si el usuario existe, false en caso contrario (?)
    try:
        usuario = Usuario.objects.get(correo=correo)
        return True
    except Usuario.DoesNotExist:
        return False    

# COMPROBADO
# EN LA API
def actualizarUsuario(usuarioVO): #Se actualiza el usuario, cambiado para simplificado proceso API
    usuario = Usuario.objects.get(pk=usuarioVO.correo)
    usuario.nombre = usuarioVO.nombre
    usuario.sexo = usuarioVO.sexo
    usuario.nacimiento = usuarioVO.nacimiento
    usuario.contrasegna = usuarioVO.contrasegna
    usuario.pais = usuarioVO.pais
    usuario.save()

# COMPROBADO
# EN LA API
def eliminarUsuario(correo): #Se elimina el usuario y todas sus relaciones
    usuario = Usuario.objects.get(pk=correo)
    usuario.delete()


# COMPROBADO
# EN LA API
def listarAmigos(correo): #Devuelve todos los amigos del usuario TODO: Revisar, no tengo claro si es correcto
    usuario = Usuario.objects.get(correo=correo)
    amigos1 = Amigo.objects.filter(micorreo1=usuario)
    amigos2 = Amigo.objects.filter(micorreo2=usuario)
    amigos = list(amigos1 | amigos2)
    return amigos

# COMPROBADO
# EN LA API
def agnadirAmigo(usuarioCorreo, amigoId): #Se crean las relaciones de amistad
    usuario = Usuario.objects.get(pk=usuarioCorreo)
    amigo = Usuario.objects.get(pk=amigoId)
    Amigo.objects.create(
        micorreo1=usuario,
        micorreo2=amigo
    )

# COMPROBADO
# EN LA API
def eliminarAmigo(usuarioCorreo, amigoId): #Se eliminan las relaciones de amistad
    usuario = Usuario.objects.get(pk=usuarioCorreo)
    amigo = Usuario.objects.get(pk=amigoId)
    Amigo.objects.filter(micorreo1=usuario, micorreo2=amigo).delete()
    Amigo.objects.filter(micorreo1=amigo, micorreo2=usuario).delete()

# COMPROBADO
# EN LA API
def sonAmigos(usuarioCorreo, amigoCorreo): #Devuelve si dos usuarios son amigos
    return Amigo.objects.filter(micorreo1=usuarioCorreo, micorreo2=amigoCorreo).exists() or Amigo.objects.filter(micorreo1=amigoCorreo, micorreo2=usuarioCorreo).exists()

#DAOs DE PLAYLIST

'''# SIN COMPROBAR
def get_playlists(user_email): #Devuelve todas las playlists en las que el usuario colabora devueltas como VO
    user = Usuario.objects.get(pk=user_email)
    ids = Colabora.objects.filter(miUsuario=user)
    return [Colabora.objects.get(pk=id).miPlaylist for id in ids]'''

# COMPROBADO
#EN LA API
def crearPlaylist(usuarioCorreo, nombre, publica): #Se crea sin colaboradores
    usuario = Usuario.objects.get(pk=usuarioCorreo)
    playlist = Playlist.objects.create(
        nombre=nombre,
        publica=publica
    )
    Colabora.objects.create(
        miUsuario=usuario,
        miPlaylist=playlist
    )

# COMPROBADO
#EN LA API
def actualizarPlaylist(playlistId, nombre, publica): # Solo se puede cambiar el nombre(TODO: se puede poner foto)
    playlist = Playlist.objects.get(pk=playlistId)
    playlist.nombre = nombre
    playlist.publica = publica
    playlist.save()

'''def remove_playlist(playlist_id): # He intentado hacer que los colaboradores dejen de colaborar, pero NO SE SI ESTÁ BIEN
    playlist = Playlist.objects.get(pk=playlist_id)
    ids = Colabora.objects.filter(miUsuario=user)
    #Colabora.objects.get(pk=id).delete() for id in ids
    playlist.delete()'''

# COMPROBADO
#EN LA API
def listarPlaylistsUsuario(correo): #Devuelve todas las playlists del usuario devueltas como VO
    return Playlist.objects.filter(colaboradores__miUsuario__correo=correo)

# COMPROBADO
#EN LA API
def agnadirCancionPlaylist(playlistId, cancionId): #Se añade la cancion a la playlist
    playlist = Playlist.objects.get(pk=playlistId)
    song = Cancion.objects.get(pk=cancionId)
    Contiene.objects.create(
        miAudio=song,
        miPlaylist=playlist
    )

# COMPROBADO
#EN LA API
def eliminarCancionPlaylist(playlistId, cancionId): #Se elimina la cancion de la playlist
    playlist = Playlist.objects.get(pk=playlistId)
    song = Cancion.objects.get(pk=cancionId)
    Contiene.objects.filter(miAudio=song, miPlaylist=playlist).delete()

# COMPROBADO
#EN LA API
def listarCanciones(): #Devuelve todas las canciones
    return Cancion.objects.all()

# COMPROBADO
#EN LA API
def listarCancionesPlaylist(playlistId): #Devuelve las canciones de una playlist dado su id
    playlist = Playlist.objects.get(pk=playlistId)
    
    # Retrieve the Contiene objects related to the playlist
    contiene_objects = Contiene.objects.filter(miPlaylist=playlist)
    
    # Retrieve the miAudio attribute from each Contiene object
    canciones = [contiene.miAudio for contiene in contiene_objects]
    
    return canciones

'''def get_playlist_songs(playlist_id): # Asume que la playlist es de canciones solo, devuelve VO de Cancion
    playlist = Playlist.objects.get(pk=playlist_id)
    ids = Contiene.objects.filter(miPlaylist=playlist)
    return [Cancion.objects.get(pk=id).to_VO() for id in ids]'''

# COMPROBADO
def conseguirPlaylistPorNombre(playlistName): #Devuelve el playlist dado su nombre
    try:
        return Playlist.objects.get(nombre=playlistName)
    except ObjectDoesNotExist:
        return None
    
def buscarPlaylist(playlistNombre):
    try:
        playlistNombre = playlistNombre.lower()
        return Playlist.objects.filter(nombre__istartswith=playlistNombre)
    except ObjectDoesNotExist:
        return None


#DAOs DE CANCION

# COMPROBADO
#EN LA API
def crearCancion(cancionVO): #Se crea la cancion sin generos
    return Cancion.objects.create(
        nombre=cancionVO.nombre,
        #letra=song_vo.letra,
        #cantantes=song_vo.cantantes,
        miAlbum=cancionVO.miAlbum,
        puntuacion=cancionVO.puntuacion,
        numPuntuaciones=cancionVO.numPuntuaciones,
        archivo_mp3=cancionVO.archivo_mp3,
        foto=cancionVO.foto
    )
# devuelve el id de la playlist favoritos del usuario
def favoritoUsuario(correo):
    usuario = Usuario.objects.get(pk=correo)
    return Playlist.objects.get(colaboradores__miUsuario=usuario, nombre="Favoritos").id

def cancionFavorita(correo, cancionVO):
    usuario = Usuario.objects.get(pk=correo)
    playlist = Playlist.objects.get(colaboradores__miUsuario=usuario, nombre="Favoritos")
    cancion = Cancion.objects.get(pk=cancionVO.id)
    return Contiene.objects.filter(miAudio=cancion, miPlaylist=playlist).exists()
    

'''# SIN COMPROBAR (QUITAR QUIZÁS)
def get_user_favorites(usuarioCorreo): #Devuelve las canciones favoritas del usuario devueltas como VO
    user = Usuario.objects.get(pk=usuarioCorreo)
    ids = Favorito.objects.filter(miUsuario=user)
    return [Favorito.objects.get(pk=id).miAudio for id in ids]

# SIN COMPROBAR (QUITAR QUIZÁS)
def add_song_to_favorites(user_email, song_id): #Se añade la cancion a favoritos dado id
    user = Usuario.objects.get(pk=user_email)
    song = Cancion.objects.get(pk=song_id)
    Favorito.objects.create(
        miUsuario=user,
        miAudio=song
    )

# SIN COMPROBAR (QUITAR QUIZÁS)
def remove_song_from_favorites(user_email, song_id): #Se elimina la cancion de favoritos dado id
    user = Usuario.objects.get(pk=user_email)
    song = Cancion.objects.get(pk=song_id)
    Favorito.objects.filter(miUsuario=user, miAudio=song).delete()'''

# SIN COMPROBAR
def listarGenerosCancion(cancionId): #Devuelve los generos de una cancion dado su id
    cancion = Cancion.objects.get(pk=cancionId)
    ids = Pertenecen.objects.filter(miAudio=cancion)
    return [Pertenecen.objects.get(pk=id).miGenero for id in ids]

#COMPROBADO
def buscarCancion(cancionNombre):
    try:
        cancionNombre = cancionNombre.lower()
        return Cancion.objects.filter(nombre__istartswith=cancionNombre)
    except ObjectDoesNotExist:
        return None


# COMPROBADO
def conseguirCancionPorId(cancionId): #Devuelve la cancion dado su id
    try:
        return Cancion.objects.get(pk=cancionId)
    except ObjectDoesNotExist:
        return None

# EN PROCESO, está en la view q no saca nada por la terminal
def albumCancion(cancionId): #Devuelve el album de una cancion dado su id
    cancion = Cancion.objects.get(pk=cancionId)
    return cancion.miAlbum

# EN PROCESO, está en la view q no saca nada por la terminal
def artistasCancion(cancionId): #Devuelve los artistas de una cancion dado su id
    cancion = Cancion.objects.get(pk=cancionId)
    return cancion.cantantes

# SIN COMPROBAR (QUITAR QUIZÁS)
def audioDeCancion(cancionId): #Devuelve el audio de una cancion dado su id(Con la api de spoty securamente no haga falta)
    return Cancion.objects.get(pk=cancionId).audio

# EN PROCESO
#EN LA API
def puntuarCancion(cancionId, puntuacion): #añade puntuación a una canción
    cancion = Cancion.objects.get(pk=cancionId)
    cancion.puntuacion = puntuacion
    cancion.save()

# EN PROCESO
def puntuacionCancion(cancionId): #Devuelve la puntuación de una canción
    cancion = Cancion.objects.get(pk=cancionId)
    return cancion.puntuacion

def numeroPuntuaciones(cancionId): #Devuelve el número de puntuaciones de una canción
    cancion = Cancion.objects.get(pk=cancionId)
    return cancion.pnumPuntuaciones

def aumentarNumeroPuntuaciones(cancionId, numeroPuntuaciones): #Aumenta el número de puntuaciones de una canción
    cancion = Cancion.objects.get(pk=cancionId)
    cancion.numPuntuaciones = numeroPuntuaciones
    cancion.save() 


#DAOs DE HISTORIAL

# COMPROBADO
#EN LA API
def listarHistorial(usuarioCorreo): #Devuelve el historial de escucha del usuario devuelto como VO
    usuario = Usuario.objects.get(pk=usuarioCorreo)
    historial = Historial.objects.filter(miUsuario=usuario)
    canciones = [Historial.objects.get(pk=historial_object.id).miAudio for historial_object in historial]
    return canciones

# COMPROBADO
#EN LA API
def agnadirCancionHistorial(usuarioCorreo, cancion): #Se añade la cancion al historial
    usuario = Usuario.objects.get(pk=usuarioCorreo)
    cancion = Cancion.objects.get(pk=cancion.id)
    Historial.objects.create(
        miUsuario=usuario,
        miAudio=cancion
    )

# COMPROBADO
def eliminarCancionHistorial(usuarioCorreo, cancionId): #Se elimina la cancion del historial
    usuario = Usuario.objects.get(pk=usuarioCorreo)
    cancion = Cancion.objects.get(pk=cancionId)
    Historial.objects.get(miUsuario=usuario, miAudio=cancion).delete()

#DAOs DE COLA

'''def get_user_queue(user_email): #Devuelve la cola de reproduccion del usuario devuelta como VO
    user = Usuario.objects.get(pk=user_email)
    ids = Cola.objects.filter(miUsuario=user)
    return [Cola.objects.get(pk=id).miAudio for id in ids]'''

# COMPROBADO
#EN LA API
def agnadirCancionCola(usuarioCorreo, cancionId): #Se añade la cancion a la cola de reproduccion
    usuario = Usuario.objects.get(pk=usuarioCorreo)
    cancion = Cancion.objects.get(pk=cancionId)
    Cola.objects.create(
        miUsuario=usuario,
        miAudio=cancion
    )

# COMPROBADO
#EN LA API
def eliminarCancionCola(usuarioCorreo, cancionId): #Se elimina la cancion de la cola de reproduccion
    usuario = Usuario.objects.get(pk=usuarioCorreo)
    cancion = Cancion.objects.get(pk=cancionId)
    Cola.objects.filter(miUsuario=usuario, miAudio=cancion).delete()


# lo hacemos? no se si dijimos si se podía o no añadir un episodio a la cola
# def add_episode_to_queue(user_email, episode_id)

# COMPROBADO
#EN LA API
def listarCola(usuarioCorreo): #Devuelve la cola de reproduccion del usuario devuelta como VO
    usuario = Usuario.objects.get(pk=usuarioCorreo)
    cola = Cola.objects.filter(miUsuario=usuario)
    canciones = [cola_object.miAudio for cola_object in cola]
    return canciones

#DAOs DE GENERO

# EN PROCESO
# EN LA API
def crearGenero(generoVO): #Crea y devuelve el genero como vo
    return Genero.objects.create(
        nombre=generoVO.nombre
    )

# EN PROCESO
def conseguirGeneroPorNombre(nombre):
    try:
        return Genero.objects.get(pk=nombre)
    except ObjectDoesNotExist:
        return None
    
# SIN COMPROBAR
def listarGeneros(): #Devuelve todos los generos
    return Genero.objects.all()

# SIN COMPROBAR, no se si esta bien el hecho de q haya puesto print aqui ?
def listarCancionesGenero(generoNombre): #Devuelve todas las canciones de un genero dado su nombre
    genero = Genero.objects.get(nombre=generoNombre)
    ids = Pertenecen.objects.filter(miGenero=genero)
    canciones = [pertenecen_object.miAudio for pertenecen_object in ids]
    return canciones

#DAOs DE ALBUM

# COMPROBADO
#EN LA API
def crearAlbum(albumVO): #Se crea el album sin canciones
    return Album.objects.create(
        nombre=albumVO.nombre
    )

# EN LA API
def actualizarAlbum(albumVO): #Se actualiza el album
    album = Album.objects.get(pk=albumVO.id)
    album.nombre = albumVO.nombre
    album.save()

# COMPROBADO
#EN LA API
def agnadirCancionAlbum(albumVO, cancionVO): #Se añade la cancion al album
    album = Album.objects.get(pk=albumVO.id)
    cancion = Cancion.objects.get(pk=cancionVO.id)
    cancion.miAlbum = album
    cancion.save()

# COMPROBADO
# EN LA API
def listarCancionesAlbum(albumVO): #Devuelve todas las canciones de un album
    album = Album.objects.get(pk=albumVO.id)
    return Cancion.objects.filter(miAlbum=album) #Devuelve todas las canciones??

# COMPROBADO
def conseguirAlbumPorId(albumId): #Devuelve el album dado su id
    try:
        return Album.objects.get(pk=albumId)
    except ObjectDoesNotExist:
        return None

# COMPROBADO
def conseguirAlbumPorNombre(albumNombre): #Devuelve el album dado su nombre
    try:
        return Album.objects.get(nombre=albumNombre)
    except ObjectDoesNotExist:
        return None
    
def buscarAlbum(albumNombre):
    try:
        albumNombre = albumNombre.lower()
        return Album.objects.filter(nombre__istartswith=albumNombre)
    except ObjectDoesNotExist:
        return None

#DAOs DE CAPITULO


# SIN COMPROBAR
#EN LA API
def crearCapitulo(capituloVO): #Se crea el capitulo
    return Capitulo.objects.create(
        nombre=capituloVO.nombre,
        descripcion=capituloVO.descripcion,
        miPodcast=capituloVO.miPodcast
    )

#EN LA API
def actualizarCapitulo(capituloId, nuevoNombre, nuevaDescripcion, nuevoPodcast): #Se actualiza el capitulo
    capitulo = Capitulo.objects.get(pk=capituloId)
    capitulo.nombre = nuevoNombre
    capitulo.descripcion = nuevaDescripcion
    capitulo.miPodcast = nuevoPodcast
    capitulo.save()

# SIN COMPROBAR
def conseguirCapituloPorId(capituloId): #Devuelve el capitulo dado su id
    try:
        return Capitulo.objects.get(pk=capituloId)
    except ObjectDoesNotExist:
        return None

# SIN COMPROBAR
def conseguirCapituloPorNombre(capituloNombre): #Devuelve el capitulo dado su nombre
    try:
        return Capitulo.objects.get(nombre=capituloNombre)
    except ObjectDoesNotExist:
        return None
    
def buscarCapitulo(capituloNombre):
    try:
        capituloNombre = capituloNombre.lower()
        return Capitulo.objects.filter(nombre__istartswith=capituloNombre)
    except ObjectDoesNotExist:
        return None

# SIN COMPROBAR
def podcastCapitulo(capituloId): #Devuelve el podcast de un episodio dado su id
    episode = Capitulo.objects.get(pk=capituloId)
    return episode.miPodcast

#DAOs DE PODCAST

# COMPORBADO
# EN LA API
def crearPodcast(podcastVO): #Se crea el podcast
    return Podcast.objects.create(
        nombre=podcastVO.nombre,
        presentadores=podcastVO.presentadores,
        puntuacion=podcastVO.puntuacion,
        numPuntuaciones=podcastVO.numPuntuaciones
    )


def puntuacionPodcast(podcastId): #Devuelve la puntuación de un podcast dado su id
    podcast = Podcast.objects.get(pk=podcastId)
    return podcast.puntuacion

def puntuarPodcast(podcastId, puntuacion): #añade puntuación a un podcast
    podcast = Podcast.objects.get(pk=podcastId)
    podcast.puntuacion = puntuacion
    podcast.save()

def numeroPuntuacionesPodcast(podcastId): #Devuelve el número de puntuaciones de una canción
    podcast = Podcast.objects.get(pk=podcastId)
    return podcast.numPuntuaciones

def aumentarNumeroPuntuacionesPodcast(podcastId, numeroPuntuaciones): #Aumenta el número de puntuaciones de una canción
    podcast = Podcast.objects.get(pk=podcastId)
    podcast.numPuntuaciones = numeroPuntuaciones
    podcast.save() 

# COMPROBADO
# EN LA API
def actualizarPodcast(podcastVO): #Se actualiza el podcast
    podcast = Podcast.objects.get(pk=podcastVO.id)
    podcast.nombre = podcastVO.nombre
    podcast.presentadores = podcastVO.presentadores
    podcast.save()

# SIN COMPROBAR
def listarCapitulosPodcast(podcastVO): #Devuelve todos los capitulos de un podcast dado su id
    podcast = Podcast.objects.get(pk=podcastVO.id)
    return Capitulo.objects.filter(miPodcast=podcast)

def listarPodcasts(): #Devuelve todos los podcasts
    return Podcast.objects.all()

# SIN COMPROBAR
def conseguirPodcastPorId(podcastId): #Devuelve el podcast dado su id
    try:
        return Podcast.objects.get(pk=podcastId)
    except ObjectDoesNotExist:
        return None

# SIN COMPROBAR
# NO SE SI ESTÁ BIEN
def conseguirPodcastPorNombre(podcastNombre): #Devuelve el podcast dado su nombre
    try:
        return Podcast.objects.get(nombre=podcastNombre)
    except ObjectDoesNotExist:
        return None

def buscarPodcast(podcastNombre):
    try:
        podcastNombre = podcastNombre.lower()
        return Podcast.objects.filter(nombre__istartswith=podcastNombre)
    except ObjectDoesNotExist:
        return None


# SIN COMPROBAR
def listarGenerosPodcast(podcastId): #Devuelve los generos de un podcast dado su id
    podcast = Podcast.object.get(pk=podcastId)
    ids = Pertenecen.objects.filter(miAudio=podcast)
    return [Pertenecen.objects.get(pk=id).miGenero for id in ids]

# SIN COMPROBAR
# MIRAR SI ESTÁ BIEN
def presentadoresPodcast(podcastId): #Devuelve los presentadores de un podcast dado su id
    podcast = Podcast.objects.get(pk=podcastId)
    return podcast.presentadores



'''def get_episode_audio(episode_id): #Devuelve el audio de un capitulo dado su id
    episode = Capitulo.objects.get(pk=episode_id)
    return Audio.objects.get(pk=episode.id)
'''

# DAOs de pertenecer

# SIN COMPROBAR
# EN LA API
def crearPertenecen(miGeneroVO, miAudioVO):
    return Pertenecen.objects.create(
        miGenero=miGeneroVO,
        miAudio=miAudioVO
    )

def crearCantan(cancionVO, artistaVO):
    return Cantan.objects.create(
        miCancion=cancionVO,
        miArtista=artistaVO
    )