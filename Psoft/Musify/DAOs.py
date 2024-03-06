from django.db import connection  # Assuming you're using Django

from .models import Usuario, Amigo, Playlist, Colabora, Contiene, Historial, Favorito ,Cancion, Podcast, Capitulo ,Cola, Genero, Pertenecen, Album

#DAOs DE USUARIO

"""
def get_user_by_id(user_email): #Se busca el usuario por su ID
    return Usuario.objects.get(pk=user_email)
"""

def get_user_by_correo(email): #Se busca el usuario por su correo
    return Usuario.objects.get(correo=email)

def check_user_password(user_email, password): #se comprueba la contraseña del usuario (iniciar sesión)
    user = Usuario.objects.get(pk=user_email)
    return user.contrasegna == password

def create_user(user_vo): #Se crea el usuario sin amigos
    return Usuario.objects.create(
        correo=(user_vo.correo).lower(), #Se guarda en minusculas ya que en el correo electronico no importa la capitalizacion
        nombre=user_vo.nombre,
        contrasegna=user_vo.contrasegna
    )

def update_user(user_email, user_vo): #Se actualiza el usuario, requiere el ID
    user = Usuario.objects.get(pk=user_email)
    user.correo = user_vo.correo
    user.nombre = user_vo.nombre
    user.contrasegna = user_vo.contrasegna
    user.save()

def remove_user(user_email): #Se elimina el usuario y todas sus relaciones
    user = Usuario.objects.get(pk=user_email)
    user.delete()

def get_friends(user_email): #Devuelve todos los amigos del usuario TODO: Revisar, no tengo claro si es correcto
    user = Usuario.objects.get(correo=user_email)
    amigos = Amigo.objects.filter(micorreo1=user).all() | Amigo.objects.filter(micorreo2=user).all()
    return [amigo.micorreo1 if amigo.micorreo1 != user else amigo.micorreo2 for amigo in amigos]

def add_friend(user_email, friend_id): #Se crean las relaciones de amistad
    user = Usuario.objects.get(pk=user_email)
    friend = Usuario.objects.get(pk=friend_id)
    Amigo.objects.create(
        micorreo1=user,
        micorreo2=friend
    )

def remove_friend(user_email, friend_id): #Se eliminan las relaciones de amistad
    user = Usuario.objects.get(pk=user_email)
    friend = Usuario.objects.get(pk=friend_id)
    Amigo.objects.filter(micorreo1=user, micorreo2=friend).delete()
    Amigo.objects.filter(micorreo1=friend, micorreo2=user).delete()

def are_friends(user_email, friend_email): #Devuelve si dos usuarios son amigos
    return Amigo.objects.filter(micorreo1=user_email, micorreo2=friend_email).exists() or Amigo.objects.filter(micorreo1=friend_email, micorreo2=user_email).exists()

#DAOs DE PLAYLIST

def get_playlists(user_email): #Devuelve todas las playlists en las que el usuario colabora devueltas como VO
    user = Usuario.objects.get(pk=user_email)
    ids = Colabora.objects.filter(miUsuario=user)
    return [Colabora.objects.get(pk=id).miPlaylist for id in ids]

def create_playlist(user_email, nombre, publica): #Se crea sin colaboradores
    user = Usuario.objects.get(pk=user_email)
    playlist = Playlist.objects.create(
        nombre=nombre,
        publica=publica
    )
    Colabora.objects.create(
        miUsuario=user,
        miPlaylist=playlist
    )

def update_playlist_details(playlist_id, nombre,publica): # Solo se puede cambiar el nombre(TODO: se puede poner foto)
    playlist = Playlist.objects.get(pk=playlist_id)
    playlist.nombre = nombre
    playlist.publica = publica
    playlist.save()

'''def remove_playlist(playlist_id): # He intentado hacer que los colaboradores dejen de colaborar, pero NO SE SI ESTÁ BIEN
    playlist = Playlist.objects.get(pk=playlist_id)
    ids = Colabora.objects.filter(miUsuario=user)
    #Colabora.objects.get(pk=id).delete() for id in ids
    playlist.delete()'''




def get_playlists_from_user(user_email): #Devuelve todas las playlists del usuario devueltas como VO
    return Playlist.objects.filter(colaboradores__miUsuario__correo=user_email)

def add_song_to_playlist(playlist_id, song_id): #Se añade la cancion a la playlist
    playlist = Playlist.objects.get(pk=playlist_id)
    song = Cancion.objects.get(pk=song_id)
    Contiene.objects.create(
        miAudio=song,
        miPlaylist=playlist
    )

def remove_song_from_playlist(playlist_id, song_id): #Se elimina la cancion de la playlist
    playlist = Playlist.objects.get(pk=playlist_id)
    song = Cancion.objects.get(pk=song_id)
    Contiene.objects.filter(miAudio=song, miPlaylist=playlist).delete()

def get_songs_from_playlist(playlist_id): #Devuelve las canciones de una playlist dado su id
    playlist = Playlist.objects.get(pk=playlist_id)
    
    # Retrieve the Contiene objects related to the playlist
    contiene_objects = Contiene.objects.filter(miPlaylist=playlist)
    
    # Retrieve the miAudio attribute from each Contiene object
    songs = [contiene.miAudio for contiene in contiene_objects]
    
    return songs

def get_playlist_by_name(playlist_name): #devuelve una playlist dado su nombre
    return Playlist.objects.get(nombre=playlist_name)

def set_playlist_public(playlist_id, publica): #hace pública o privada una playlist
    playlist = Playlist.objects.get(pk=playlist_id)
    playlist.publica = publica
    playlist.save()

#DAOs DE CANCION

def get_playlist_songs(playlist_id): # Asume que la playlist es de canciones solo, devuelve VO de Cancion
    playlist = Playlist.objects.get(pk=playlist_id)
    ids = Contiene.objects.filter(miPlaylist=playlist)
    return [Cancion.objects.get(pk=id).to_VO() for id in ids]

def create_song(nombre): #Se crea la cancion sin generos
    return Cancion.objects.create(
        nombre=nombre,
    )

def get_user_favorites(user_email): #Devuelve las canciones favoritas del usuario devueltas como VO
    user = Usuario.objects.get(pk=user_email)
    ids = Favorito.objects.filter(miUsuario=user)
    return [Favorito.objects.get(pk=id).miAudio for id in ids]

def add_song_to_favorites(user_email, song_id): #Se añade la cancion a favoritos dado id
    user = Usuario.objects.get(pk=user_email)
    song = Cancion.objects.get(pk=song_id)
    Favorito.objects.create(
        miUsuario=user,
        miAudio=song
    )

def remove_song_from_favorites(user_email, song_id): #Se elimina la cancion de favoritos dado id
    user = Usuario.objects.get(pk=user_email)
    song = Cancion.objects.get(pk=song_id)
    Favorito.objects.filter(miUsuario=user, miAudio=song).delete()

def get_song_genres(song_id): #Devuelve los generos de una cancion dado su id
    song = Cancion.objects.get(pk=song_id)
    ids = Pertenecen.objects.filter(miAudio=song)
    return [Pertenecen.objects.get(pk=id).miGenero for id in ids]

# NO SE SI ESTÁ BIEN
def get_song_by_name(song_name): #Devuelve la cancion dado su nombre
    return Cancion.objects.get(nombre=song_name)

def get_song_by_id(song_id): #Devuelve la cancion dado su id
    return Cancion.objects.get(pk=song_id)

def get_song_album(song_id): #Devuelve el album de una cancion dado su id
    song = Cancion.objects.get(pk=song_id)
    return song.miAlbum


def get_song_artists(song_id): #Devuelve los artistas de una cancion dado su id
    song = Cancion.objects.get(pk=song_id)
    return song.cantantes

def get_song_audio(song_id): #Devuelve el audio de una cancion dado su id(Con la api de spoty securamente no haga falta)
    return Cancion.objects.get(pk=song_id).audio

def add_song_rating(song_id, rating): #añade puntuación a una canción
    song = Cancion.objects.get(pk=song_id)
    song.puntuacion = rating
    song.save()

#DAOs DE HISTORIAL

def get_user_history(user_email): #Devuelve el historial de escucha del usuario devuelto como VO
    user = Usuario.objects.get(pk=user_email)
    ids = Historial.objects.filter(miUsuario=user)
    return [Historial.objects.get(pk=id).miAudio for id in ids]

def add_song_to_history(user_email, song_id): #Se añade la cancion al historial
    user = Usuario.objects.get(pk=user_email)
    song = Cancion.objects.get(pk=song_id)
    Historial.objects.create(
        miUsuario=user,
        miAudio=song
    )

def remove_song_from_history(user_email, song_id): #Se elimina la cancion del historial
    user = Usuario.objects.get(pk=user_email)
    song = Cancion.objects.get(pk=song_id)
    Historial.objects.get(miUsuario=user, miAudio=song).delete()

#DAOs DE COLA

def get_user_queue(user_email): #Devuelve la cola de reproduccion del usuario devuelta como VO
    user = Usuario.objects.get(pk=user_email)
    ids = Cola.objects.filter(miUsuario=user)
    return [Cola.objects.get(pk=id).miAudio for id in ids]

def add_song_to_queue(user_email, song_id): #Se añade la cancion a la cola de reproduccion
    user = Usuario.objects.get(pk=user_email)
    song = Cancion.objects.get(pk=song_id)
    Cola.objects.create(
        miUsuario=user,
        miAudio=song
    )

def remove_song_from_queue(user_email, song_id): #Se elimina la cancion de la cola de reproduccion
    user = Usuario.objects.get(pk=user_email)
    song = Cancion.objects.get(pk=song_id)
    Cola.objects.filter(miUsuario=user, miAudio=song).delete()

def add_song_to_queue(user_email, song_id): #Se añade la cancion a la cola de reproduccion
    user = Usuario.objects.get(pk=user_email)
    song = Cancion.objects.get(pk=song_id)
    Cola.objects.create(
        miUsuario=user,
        miAudio=song
    )

# lo hacemos? no se si dijimos si se podía o no añadir un episodio a la cola
# def add_episode_to_queue(user_email, episode_id)

def get_queue_from_user(user_email): #Devuelve la cola de reproduccion del usuario devuelta como VO
    user = Usuario.objects.get(pk=user_email)
    cola = Cola.objects.filter(miUsuario=user)
    songs = [cola_object.miAudio for cola_object in cola]
    return songs

#DAOs DE GENERO
    
def get_genres(): #Devuelve todos los generos
    return Genero.objects.all()

def get_genre_songs(genre_name): #Devuelve todas las canciones de un genero dado su nombre
    genre = Genero.objects.get(nombre=genre_name)
    ids = Pertenecen.objects.filter(miGenero=genre)
    return [Pertenecen.objects.get(pk=id).miAudio for id in ids]

#DAOs DE ALBUM

def get_album_songs(album_id): #Devuelve todas las canciones de un album dado su id
    album = Album.objects.get(pk=album_id)
    return Cancion.objects.filter(miAlbum=album)

def get_album_by_id(album_id): #Devuelve el album dado su id
    return Album.objects.get(pk=album_id)

def get_album_by_name(album_name): #Devuelve el album dado su nombre
    return Album.objects.get(nombre=album_name)

#DAOs DE CAPITULO

#MIRAR SI ESTÁ BIEN
def create_episode(nombre, descripcion): #Se crea el capitulo
    return Capitulo.objects.create(
        nombre=nombre,
        descripcion=descripcion
    )

def get_episode_by_id(episode_id): #Devuelve el capitulo dado su id
    return Capitulo.objects.get(pk=episode_id)

def get_episode_podcast(episode_id): #Devuelve el podcast de un episodio dado su id
    episode = Capitulo.objects.get(pk=episode_id)
    return episode.miPodcast

#DAOs DE PODCAST

def get_podcast_episodes(podcast_id): #Devuelve todos los capitulos de un podcast dado su id
    podcast = Podcast.objects.get(pk=podcast_id)
    return Capitulo.objects.filter(miPodcast=podcast)

def get_podcast_by_id(podcast_id): #Devuelve el podcast dado su id
    return Podcast.objects.get(pk=podcast_id)

# NO SE SI ESTÁ BIEN
def get_podcast_by_name(podcast_name): #Devuelve el podcast dado su nombre
    return Podcast.objects.get(nombre=podcast_name)

def get_podcast_genres(podcast_id): #Devuelve los generos de un podcast dado su id
    podcast = Podcast.object.get(pk=podcast_id)
    ids = Pertenecen.objects.filter(miAudio=podcast)
    return [Pertenecen.objects.get(pk=id).miGenero for id in ids]

# MIRAR SI ESTÁ BIEN
def get_podcast_hosts(podcast_id): #Devuelve los presentadores de un podcast dado su id
    podcast = Podcast.objects.get(pk=podcast_id)
    return podcast.presentadores



'''def get_episode_audio(episode_id): #Devuelve el audio de un capitulo dado su id
    episode = Capitulo.objects.get(pk=episode_id)
    return Audio.objects.get(pk=episode.id)
'''




