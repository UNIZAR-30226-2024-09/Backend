from django.db import connection  # Assuming you're using Django

from .models import Usuario,UsuarioManager , Seguido, Seguidor, Playlist, Colabora, Contiene, Historial, Cancion, Podcast, Capitulo ,Cola, Genero, PertenecenCancion, PertenecenPodcast, Album, Artista, Cantan, Presentador, Interpretan
from django.core.exceptions import ObjectDoesNotExist


#DAOs DE ESTADO

def guardarEstado(usuarioID,cancionVO,tiempo): #Se guarda el estado
    usuario = Usuario.objects.get(pk=usuarioID)
    usuario.ultima_cancion = cancionVO
    usuario.ultima_minutos = tiempo
    usuario.save()


#DAOs DE ARTISTA

def crearArtista(artistaVO): #Se crea el artista
    Artista.objects.create(nombre=artistaVO.nombre, foto=artistaVO.foto, descripcion=artistaVO.descripcion)

def crearPresentador(presentadorVO): #Se crea el artista
    Presentador.objects.create(nombre=presentadorVO.nombre, foto=presentadorVO.foto, descripcion=presentadorVO.descripcion)

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
    
def buscarPresentador(nombre):
    try:
        nombre = nombre.lower()
        return Presentador.objects.filter(nombre__istartswith=nombre)
    except ObjectDoesNotExist:
        return None

def listarArtistasFavoritos(correo):
    return Usuario.objects.get(pk=correo).artistas_favoritos.all()

def conseguirPresentadorPorId(presentadorId): #Devuelve el presentador dado su id
    try:
        return Presentador.objects.get(pk=presentadorId)
    except ObjectDoesNotExist:
        return None

#DAOs DE USUARIO

# COMPROBADO
def conseguirUsuarioPorCorreo(correo): #Se busca el usuario por su correo
    try:
        return Usuario.objects.get(correo=correo)
    except ObjectDoesNotExist:
        return None

def buscarUsuario(nombre):
    try:
        nombre = nombre.lower()
        return Usuario.objects.filter(nombre__istartswith=nombre)
    except ObjectDoesNotExist:
        return None

# COMPROBAD0
def comprobarContrasegna(correo, contrasegna): #se comprueba la contraseña del usuario (iniciar sesión)
    usuario = Usuario.objects.get(correo=correo)
    return usuario.contrasegna == contrasegna

# COMPROBADO
# EN LA API
def crearUsuario(usuarioVO): #Se crea el usuario sin amigos
    usuario = Usuario.objects.create_user(
        correo=usuarioVO.correo.lower(),
        nombre=usuarioVO.nombre,
        contrasegna=usuarioVO.contrasegna,
        nacimiento=usuarioVO.nacimiento,
        sexo=usuarioVO.sexo,
        pais=usuarioVO.pais
    )
    usuario.save()
    crearPlaylist(usuario.correo,"Favoritos",False)
    return usuario

# COMPROBADO
def existeUsuario(correo): #Devuelve true si el usuario existe, false en caso contrario (?)
    try:
        usuario = Usuario.objects.get(correo=correo)
        return True
    except Usuario.DoesNotExist:
        return False    

# COMPROBADO
# EN LA API
def actualizarUsuario(usuarioVO, usuarioNuevo): #Se actualiza el usuario
    usuarioVO.nombre = usuarioNuevo.nombre
    usuarioVO.contrasegna = usuarioNuevo.contrasegna
    usuarioVO.nacimiento = usuarioNuevo.nacimiento
    usuarioVO.sexo = usuarioNuevo.sexo
    usuarioVO.pais = usuarioNuevo.pais
    usuarioVO.save()

def agnadirGeneroFavorito(correo, generoVO): #Se añade un genero favorito al usuario
    usuario = Usuario.objects.get(pk=correo)
    if generoVO.tipo == "Cancion":
        usuario.generoFavoritoCancion = generoVO
    else:
        usuario.generoFavoritoPodcast = generoVO
    usuario.save()

def agnadirArtistaFavorito(correo, artistaVO): #Se añade un artista favorito al usuario
    usuario = Usuario.objects.get(pk=correo)
    usuario.artistaFavorito = artistaVO
    usuario.save()

def agnadirPresentadorFavorito(correo, presentadorVO): #Se añade un presentador favorito al usuario
    usuario = Usuario.objects.get(pk=correo)
    usuario.presentadorFavorito = presentadorVO
    usuario.save()

def devolverArtistaFavorito(correo):
    usuario = Usuario.objects.get(pk=correo)
    return usuario.artistaFavorito

def devolverPresentadorFavorito(correo):
    usuario = Usuario.objects.get(pk=correo)
    return usuario.presentadorFavorito

def devolverGeneroFavoritoCancion(correo):
    usuario = Usuario.objects.get(pk=correo)
    return usuario.generoFavoritoCancion

def devolverGeneroFavoritoPodcast(correo):
    usuario = Usuario.objects.get(pk=correo)
    return usuario.generoFavoritoPodcast

'''def actualizarUsuarioNombre(usuarioVO, nombre):
    usuario = Usuario.objects.get(pk=usuarioVO.correo)
    usuario.nombre = nombre
    usuario.save()

def actualizarUsuarioSexo(usuarioVO, sexo):
    usuario = Usuario.objects.get(pk=usuarioVO.correo)
    usuario.sexo = sexo
    usuario.save()

def actualizarUsuarioNacimiento(usuarioVO, nacimiento):
    usuario = Usuario.objects.get(pk=usuarioVO.correo)
    usuario.nacimiento = nacimiento
    usuario.save()

def actualizarUsuarioContrasegna(usuarioVO, contrasegna):
    usuario = Usuario.objects.get(pk=usuarioVO.correo)
    usuario.contrasegna = contrasegna
    usuario.save()

def actualizarUsuarioPais(usuarioVO, pais):
    usuario = Usuario.objects.get(pk=usuarioVO.correo)
    usuario.pais = pais
    usuario.save()'''


# COMPROBADO
# EN LA API
def eliminarUsuario(correo): #Se elimina el usuario y todas sus relaciones
    usuario = Usuario.objects.get(pk=correo)
    usuario.delete()


# COMPROBADO
# EN LA API
#def listarAmigos(correo): #Devuelve todos los amigos del usuario TODO: Revisar, no tengo claro si es correcto
#    usuario = Usuario.objects.get(correo=correo)
#    amigos1 = Amigo.objects.filter(micorreo1=usuario)
#    amigos2 = Amigo.objects.filter(micorreo2=usuario)
#    amigos = list(amigos1 | amigos2)
#    return amigos

# SIN COMPROBAR
def listarSeguidos(usuarioVO): #Devuelve los usuarios a los que sigue
    seguidos = Seguido.objects.filter(miUsuarioSeguido=usuarioVO)
    return seguidos

# SIN COMPROBAR
def numeroSeguidos(usuarioVO): #Devuelve el número de usuarios a los que sigue
    return Seguido.objects.filter(miUsuarioSeguido=usuarioVO).count()

# SIN COMPROBAR
def agnadirSeguido(usuarioVO, usuarioSeguidoVO): #Se añade un seguido al usuario "correo"
    Seguido.objects.create(
        miUsuarioSeguido=usuarioVO,
        seguido=usuarioSeguidoVO
    )

# SIN COMPROBAR
def eliminarSeguido(usuarioVO, usuarioSeguidoVO): #Se elimina un seguido al usuario "correo"
    Seguido.objects.filter(miUsuarioSeguido=usuarioVO, seguido=usuarioSeguidoVO).delete()

# SIN COMPROBAR
def listarSeguidores(usuarioVO): #Devuelve los seguidores del usuario
    seguidores = Seguidor.objects.filter(miUsuarioSeguidor=usuarioVO)
    return seguidores

# SIN COMPROBAR
def numeroSeguidores(usuarioVO): #Devuelve el número de seguidores del usuario
    return Seguidor.objects.filter(miUsuarioSeguidor=usuarioVO).count()

# SIN COMPROBAR
def agnadirSeguidor(usuarioVO, usuarioSeguidorVO): #Se añade un seguidor al usuario "correo"
    Seguidor.objects.create(
        miUsuarioSeguidor=usuarioVO,
        seguidor=usuarioSeguidorVO
    )

# SIN COMPROBAR
def eliminarSeguidor(usuarioVO, usuarioSeguidorVO): #Se elimina un seguidor al usuario "correo"
    Seguidor.objects.filter(miUsuarioSeguidor=usuarioVO, seguidor=usuarioSeguidorVO).delete()

# COMPROBADO
# EN LA API
#def agnadirAmigo(usuarioCorreo, amigoId): #Se crean las relaciones de amistad
#    usuario = Usuario.objects.get(pk=usuarioCorreo)
#    amigo = Usuario.objects.get(pk=amigoId)
#    Amigo.objects.create(
#        micorreo1=usuario,
#        micorreo2=amigo
#    )

# COMPROBADO
# EN LA API
#def eliminarAmigo(usuarioCorreo, amigoId): #Se eliminan las relaciones de amistad
#    usuario = Usuario.objects.get(pk=usuarioCorreo)
#    amigo = Usuario.objects.get(pk=amigoId)
#    Amigo.objects.filter(micorreo1=usuario, micorreo2=amigo).delete()
#    Amigo.objects.filter(micorreo1=amigo, micorreo2=usuario).delete()

# COMPROBADO
# EN LA API
#def sonAmigos(usuarioCorreo, amigoCorreo): #Devuelve si dos usuarios son amigos
#    return Amigo.objects.filter(micorreo1=usuarioCorreo, micorreo2=amigoCorreo).exists() or Amigo.objects.filter(micorreo1=amigoCorreo, micorreo2=usuarioCorreo).exists()

def siguiendo(usuarioVO, amigoVO): #Devuelve si un usuario sigue a otro
    return Seguido.objects.filter(miUsuarioSeguido=usuarioVO, seguido=amigoVO).exists()

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

def crearPlaylistGeneral(nombre):
    return Playlist.objects.create(
        nombre=nombre,
        publica=True
    )

def agnadirColaborador(playlistVO, usuarioCorreo):
    usuario = Usuario.objects.get(pk=usuarioCorreo)
    Colabora.objects.create(
        miUsuario=usuario,
        miPlaylist=playlistVO
    )
# COMPROBADO
#EN LA API
def actualizarPlaylist(playlist, nombre, publica):
    playlist.nombre = nombre
    playlist.publica = publica
    playlist.save()

'''def actualizarPlaylistNombre(playlistVO, nombre):
    playlist = Playlist.objects.get(pk=playlistVO.id)
    playlist.nombre = nombre
    playlist.save()

def actualizarPlaylistPublica(playlistVO, publica):
    playlist = Playlist.objects.get(pk=playlistVO.id)
    playlist.publica = publica
    playlist.save()

    def remove_playlist(playlist_id): # He intentado hacer que los colaboradores dejen de colaborar, pero NO SE SI ESTÁ BIEN
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
    canciones = Cancion.objects.all()
    for cancion in canciones:
        cancion.archivoMp3 = None
    return canciones

def listarPocasCanciones(): #Devuelve 5 canciones aleatorias
    canciones = Cancion.objects.all().order_by('?')[:5]
    for cancion in canciones:
        cancion.archivoMp3 = None
    return canciones

def listarPocosPodcasts(): #Devuelve 5 podcasts aleatorios
    podcasts = Podcast.objects.all().order_by('?')[:5]
    for podcast in podcasts:
        podcast.archivoMp3 = None
    return podcasts

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
def conseguirPlaylistPorNombre(playlistName): #Devuelve la playlist dado su nombre
    try:
        return Playlist.objects.get(nombre=playlistName)
    except ObjectDoesNotExist:
        return None
    
def conseguirPlaylistPorId(playlistId): #Devuelve la playlist dado su id
    try:
        return Playlist.objects.get(pk=playlistId)
    except ObjectDoesNotExist:
        return None

def buscarPlaylist(playlistNombre):
    try:
        playlistNombre = playlistNombre.lower()
        return Playlist.objects.filter(nombre__istartswith=playlistNombre)
    except ObjectDoesNotExist:
        return None

def eliminarPlaylist(playlistId):
    playlist = Playlist.objects.get(pk=playlistId)
    playlist.delete()
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
        #archivoMp3=cancionVO.archivoMp3,
        #foto=cancionVO.foto
    )

def actualizarCancion(cancionVO, nombre, miAlbum, archivoMp3, foto): #Se actualiza la cancion
    cancionVO.nombre = nombre
    cancionVO.miAlbum = miAlbum
    cancionVO.archivoMp3 = archivoMp3
    cancionVO.foto = foto
    cancionVO.save()

def eliminarCancion(cancionVO):
    if cancionVO.miAlbum:
        cancionVO.miAlbum = None
    if PertenecenCancion.objects.filter(miCancion=cancionVO).exists():
        PertenecenCancion.objects.filter(miCancion=cancionVO).delete()
    if Cantan.objects.filter(miCancion=cancionVO).exists():
        Cantan.objects.filter(miCancion=cancionVO).delete()
    if Contiene.objects.filter(miAudio=cancionVO).exists():
        Contiene.objects.filter(miAudio=cancionVO).delete()
    if Historial.objects.filter(miAudio=cancionVO).exists():
        Historial.objects.filter(miAudio=cancionVO).delete()
    if Cola.objects.filter(miAudio=cancionVO).exists():
        Cola.objects.filter(miAudio=cancionVO).delete()
    if Usuario.objects.filter(ultima_cancion=cancionVO).exists():
        Usuario.objects.filter(ultima_cancion=cancionVO).update(ultima_cancion=None)
    cancionVO.delete()

def eliminarCapitulo(capituloVO):
    if Cola.objects.filter(miAudio=capituloVO).exists():
        Cola.objects.filter(miAudio=capituloVO).delete()
    if Contiene.objects.filter(miAudio=capituloVO).exists():
        Contiene.objects.filter(miAudio=capituloVO).delete()
    if Historial.objects.filter(miAudio=capituloVO).exists():
        Historial.objects.filter(miAudio=capituloVO).delete()
    if Usuario.objects.filter(ultima_cancion=capituloVO).exists():
        Usuario.objects.filter(ultima_cancion=capituloVO).update(ultima_cancion=None)
    capituloVO.delete()

def eliminarPodcast(podcastVO):
    if Capitulo.objects.filter(miPodcast=podcastVO).exists():
        Capitulo.objects.filter(miPodcast=podcastVO).delete()
    if PertenecenPodcast.objects.filter(miPodcast=podcastVO).exists():
        PertenecenPodcast.objects.filter(miPodcast=podcastVO).delete()
    if Interpretan.objects.filter(miPodcast=podcastVO).exists():
        Interpretan.objects.filter(miPodcast=podcastVO).delete()
    podcastVO.delete()

def eliminarCapitulo(capituloVO):
    capituloVO.delete()

def eliminarPodcast(podcastVO):
    podcastVO.delete()

# devuelve el id de la playlist favoritos del usuario
def favoritoUsuario(correo):
    usuario = Usuario.objects.get(pk=correo)
    return Playlist.objects.get(colaboradores__miUsuario=usuario, nombre="Favoritos").id

def cancionFavorita(correo, cancionVO):
    usuario = Usuario.objects.get(pk=correo)
    playlist = Playlist.objects.get(colaboradores__miUsuario=usuario, nombre="Favoritos")
    return Contiene.objects.filter(miAudio=cancionVO, miPlaylist=playlist).exists()
    
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
def listarGenerosCancion(cancion): #Devuelve los generos de una cancion dado su id¡
    ids = PertenecenCancion.objects.filter(miCancion=cancion.id)
    generos = [pertenecenObject.miGenero for pertenecenObject in ids]
    return generos

def listarGenerosPodcast(podcast): #Devuelve los generos de un podcast dado su id
    ids = PertenecenPodcast.objects.filter(miPodcast=podcast.id)
    generos = [pertenecenObject.miGenero for pertenecenObject in ids]
    return generos

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

def listarArtistasCancion(cancionVO): #Devuelve los artistas de una cancion dado su id
    ids = Cantan.objects.filter(miCancion=cancionVO.id)
    artistas = [cantanObject.miArtista for cantanObject in ids]
    return artistas

def listarPresentadoresPodcast(podcastVO): #Devuelve los presentadores de un podcast dado su id
    ids = Interpretan.objects.filter(miPodcast=podcastVO.id)
    presentadores = [interpretanObject.miPresentador for interpretanObject in ids]
    return presentadores

#Funciona
def audioDeCancion(cancionId):
    cancion = Cancion.objects.get(pk=cancionId)
    audio = cancion.archivoMp3
    return audio

# SIN COMPROBAR
#EN LA API
def puntuarCancion(cancionId, puntuacion): #añade puntuación a una canción
    correo = Usuario.objects.get(pk=correo)
    cancion = Cancion.objects.get(pk=cancionId)
    cancion.puntuacion = puntuacion
    cancion.save()
    puntuaCancion = puntuaCancion.objects.create (
        miUsuario = correo,
        miCancion = cancion,
        puntuacion = puntuacion
    )
    puntuaCancion.save()


# SIN COMPROBAR
def puntuacionCancion(cancionId): #Devuelve la puntuación de una canción
    cancion = Cancion.objects.get(pk=cancionId)
    return cancion.puntuacion

# SIN COMPROBAR
def numeroPuntuaciones(cancionId): #Devuelve el número de puntuaciones de una canción
    cancion = Cancion.objects.get(pk=cancionId)
    return cancion.pnumPuntuaciones

# SIN COMPROBAR
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
    
def eliminarUltimaCancionHistorial(usuarioCorreo):
    usuario = Usuario.objects.get(pk=usuarioCorreo)
    historial = Historial.objects.filter(miUsuario=usuario)
    historial.order_by('id')
    historial[0].delete()

def numeroCancionesHistorial(usuarioCorreo): #Devuelve el número de canciones en el historial
    usuario = Usuario.objects.get(pk=usuarioCorreo)
    return Historial.objects.filter(miUsuario=usuario).count()
#DAOs DE COLA

'''def get_user_queue(user_email): #Devuelve la cola de reproduccion del usuario devuelta como VO
    user = Usuario.objects.get(pk=user_email)
    ids = Cola.objects.filter(miUsuario=user)
    return [Cola.objects.get(pk=id).miAudio for id in ids]'''

# COMPROBADO
#EN LA API
def agnadirCancionCola(usuarioCorreo, cancionVO): #Se añade la cancion a la cola de reproduccion
    usuario = Usuario.objects.get(pk=usuarioCorreo)
    cancion = Cancion.objects.get(pk=cancionVO.id)
    Cola.objects.create(
        miUsuario=usuario,
        miAudio=cancion
    )

def comprobarCancionCola(usuarioCorreo, cancion):
    usuario = Usuario.objects.get(pk=usuarioCorreo)
    return Cola.objects.filter(miUsuario=usuario, miAudio=cancion).exists()

# COMPROBADO
#EN LA API
def eliminarCancionCola(usuarioCorreo, cancionId): #Se elimina la cancion de la cola de reproduccion
    usuario = Usuario.objects.get(pk=usuarioCorreo)
    cancion = Cancion.objects.get(pk=cancionId)
    Cola.objects.filter(miUsuario=usuario, miAudio=cancion).delete()


# SIN COMPROBAR
def agnadirCapituloCola(usuarioCorreo, capituloId):
    usuario = Usuario.objects.get(pk=usuarioCorreo)
    capitulo = Capitulo.objects.get(pk=capituloId)
    Cola.objects.create(
        miUsuario=usuario,
        miAudio=capitulo
    )

# SIN COMPROBAR
def eliminarCapituloCola(usuarioCorreo, capituloId): #Se elimina la cancion de la cola de reproduccion
    usuario = Usuario.objects.get(pk=usuarioCorreo)
    capitulo = Capitulo.objects.get(pk=capituloId)
    Cola.objects.filter(miUsuario=usuario, miAudio=capitulo).delete()

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
        nombre=generoVO.nombre,
        tipo=generoVO.tipo
    )

# EN PROCESO
def conseguirGeneroPorNombre(nombre):
    try:
        return Genero.objects.get(pk=nombre)
    except ObjectDoesNotExist:
        return None
    
# SIN COMPROBAR
def listarGenerosCanciones(): #Devuelve todos los generos de las canciones
    generos = Genero.objects.filter(tipo="Cancion")
    return generos

def listarGenerosPodcasts(): #Devuelve todos los generos de los podcasts
    generos = Genero.objects.filter(tipo="Podcast")
    return generos

def listarPresentadores(): #Devuelve todos los presentadores
    return Presentador.objects.all()

def listarArtistas(): #Devuelve todos los artistas
    return Artista.objects.all()

def listarCancionesArtista(artistaVO): #Devuelve todas las canciones de un artista dado su id
    ids = Cantan.objects.filter(miArtista=artistaVO.id)
    canciones = [canta_object.miCancion for canta_object in ids]
    return canciones

def listarPodcastsPresentador(presentadorVO): #Devuelve todos los podcasts de un presentador dado su id
    ids = Interpretan.objects.filter(miPresentador=presentadorVO.id)
    podcasts = [interpretan_object.miPodcast for interpretan_object in ids]
    return podcasts

# SIN COMPROBAR, no se si esta bien el hecho de q haya puesto print aqui ?
def listarCancionesGenero(genero): #Devuelve todas las canciones de un genero dado su nombre
    ids = PertenecenCancion.objects.filter(miGenero=genero)
    canciones = [pertenecen_object.miCancion for pertenecen_object in ids]
    return canciones

def listarPodcastsGenero(genero): #Devuelve todos los podcasts de un genero dado su nombre
    ids = PertenecenPodcast.objects.filter(miGenero=genero)
    podcasts = [pertenecen_object.miPodcast for pertenecen_object in ids]
    return podcasts


def listarGenerosFavoritos(correo): #Devuelve los generos favoritos del usuario
    return Usuario.objects.get(pk=correo).generos_favoritos.all()

#DAOs DE ALBUM

# COMPROBADO
#EN LA API
def crearAlbum(albumVO): #Se crea el album sin canciones
    return Album.objects.create(
        nombre=albumVO.nombre,
    )

# EN LA API
def actualizarAlbum(albumVO, nombre, foto): #Se actualiza el album
    album = Album.objects.get(pk=albumVO.id)
    album.nombre = nombre
    album.foto = foto
    album.save()

'''def actualizarAlbumNombre(albumVO, nombre):
    album = Album.objects.get(pk=albumVO.id)
    album.nombre = nombre
    album.save()

def actualizarAlbumFoto(albumVO, foto):
    album = Album.objects.get(pk=albumVO.id)
    album.foto = foto
    album.save()'''

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
        miPodcast=capituloVO.miPodcast,
        #archivoMp3=capituloVO.archivoMp3
    )

#EN LA API
def actualizarCapitulo(capitulo, nombre, descripcion, miPodcast): #Se actualiza el capitulo
    capitulo.nombre = nombre
    capitulo.descripcion = descripcion
    capitulo.miPodcast = miPodcast
    capitulo.save()

'''def actualizarCapituloNombre(capituloVO, nombre):
    capitulo = Capitulo.objects.get(pk=capituloVO.id)
    capitulo.nombre = nombre
    capitulo.save()

def actualizarCapituloDescripcion(capituloVO, descripcion):
    capitulo = Capitulo.objects.get(pk=capituloVO.id)
    capitulo.descripcion = descripcion
    capitulo.save()

def actualizarCapituloPodcast(capituloVO, podcast):
    capitulo = Capitulo.objects.get(pk=capituloVO.id)
    capitulo.miPodcast = podcast
    capitulo.save()

def actualizarCapituloArchivoMp3(capituloVO, archivoMp3):
    capitulo = Capitulo.objects.get(pk=capituloVO.id)
    capitulo.archivoMp3 = archivoMp3
    capitulo.save()'''

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

def editarTipoGenero(generoVO, tipo):
    genero = Genero.objects.get(pk=generoVO.nombre)
    genero.tipo = tipo
    genero.save()

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
        puntuacion=podcastVO.puntuacion,
        numPuntuaciones=podcastVO.numPuntuaciones,
        #foto=podcastVO.foto
    )

# SIN COMPROBAR
def puntuacionPodcast(podcastId): #Devuelve la puntuación de un podcast dado su id
    podcast = Podcast.objects.get(pk=podcastId)
    return podcast.puntuacion

# SIN COMPROBAR
def puntuarPodcast(podcastId, puntuacion): #añade puntuación a un podcast
    podcast = Podcast.objects.get(pk=podcastId)
    podcast.puntuacion = puntuacion
    podcast.save()
    puntuaPodcast = puntuaPodcast.objects.create (
        miUsuario = correo,
        miPodcast = podcast,
        puntuacion = puntuacion
    )
    puntuaPodcast.save()

# SIN COMPROBAR
def numeroPuntuacionesPodcast(podcastId): #Devuelve el número de puntuaciones de una canción
    podcast = Podcast.objects.get(pk=podcastId)
    return podcast.numPuntuaciones

# SIN COMPROBAR
def aumentarNumeroPuntuacionesPodcast(podcastId, numeroPuntuaciones): #Aumenta el número de puntuaciones de una canción
    podcast = Podcast.objects.get(pk=podcastId)
    podcast.numPuntuaciones = numeroPuntuaciones
    podcast.save() 

# COMPROBADO
# EN LA API
def actualizarPodcast(podcastVO): #Se actualiza el podcast
    podcast = Podcast.objects.get(pk=podcastVO.id)
    podcast.nombre = podcastVO.nombre
    podcast.save()

def actualizarPodcastNombre(podcastVO, nombre):
    podcast = Podcast.objects.get(pk=podcastVO.id)
    podcast.nombre = nombre
    podcast.save()

def actualizarPodcastFoto(podcastVO, foto):
    podcast = Podcast.objects.get(pk=podcastVO.id)
    podcast.foto = foto
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
def crearPertenecenCancion(miGeneroVO, miAudioVO):
    return PertenecenCancion.objects.create(
        miGenero=miGeneroVO,
        miCancion=miAudioVO
    )

def crearPertenecenPodcast(miGeneroVO, miAudioVO):
    return PertenecenPodcast.objects.create(
        miGenero=miGeneroVO,
        miPodcast=miAudioVO
    )

def crearCantan(cancionVO, artistaVO):
    return Cantan.objects.create(
        miCancion=cancionVO,
        miArtista=artistaVO
    )


def crearInterpretan(podcastVO, presentadorVO):
    return Interpretan.objects.create(
        miPodcast=podcastVO,
        miPresentador=presentadorVO
    )

#DAOs para recomendar

#def recomendar():
#    with connection.cursor() as cursor:
#        cursor.execute("SELECT * FROM Musify_cancion ORDER BY puntuacion DESC LIMIT 5")
#        return cursor.fetchall()

#def generosCancionesMejorPuntuadasPorUsuario(usuarioId):
#    generos_destacados = PuntuaCancion.objects.filter(miUsuario=usuarioId, puntuacion__in=[4, 5]).values_list('miCancion__genero__nombre', flat=True).distinct()
    
    # Convertir el resultado a una lista para poder devolverla
#    generos_destacados = list(generos_destacados)
    
#    return generos_destacados

