from django.db import connection  # Assuming you're using Django

from .models import Usuario, Amigo, Playlist, Colabora, Audio, Contiene, Historial, Favorito ,Cancion, Podcast, Capitulo ,Cola, Genero, Pertenecen, Album
"""
def get_user_by_id(user_id): #Se busca el usuario por su ID
    return Usuario.objects.get(pk=user_id)
"""
def get_user_by_correo(email): #Se busca el usuario por su correo
    return Usuario.objects.get(correo=email)

def create_user(user_vo): #Se crea el usuario sin amigos
    return Usuario.objects.create(
        correo=(user_vo.correo).lower(), #Se guarda en minusculas ya que en el correo electronico no importa la capitalizacion
        nombre=user_vo.nombre,
        contrasegna=user_vo.contrasegna
    )

def update_user(user_id, user_vo): #Se actualiza el usuario, requiere el ID
    user = Usuario.objects.get(pk=user_id)
    user.correo = user_vo.correo
    user.nombre = user_vo.nombre
    user.contrasegna = user_vo.contrasegna
    user.save()

def delete_user(user_id): #Se elimina el usuario y todas sus relaciones
    user = Usuario.objects.get(pk=user_id)
    user.delete()

def get_friends(user_email): #Devuelve todos los amigos del usuario TODO: Revisar, no tengo claro si es correcto
    user = Usuario.objects.get(correo=user_email)
    amigos = Amigo.objects.filter(micorreo1=user).all() | Amigo.objects.filter(micorreo2=user).all()
    return [amigo.micorreo1 if amigo.micorreo1 != user else amigo.micorreo2 for amigo in amigos]

def add_friend(user_id, friend_id): #Se crean las relaciones de amistad
    user = Usuario.objects.get(pk=user_id)
    friend = Usuario.objects.get(pk=friend_id)
    Amigo.objects.create(
        micorreo1=user,
        micorreo2=friend
    )

def remove_friend(user_id, friend_id): #Se eliminan las relaciones de amistad
    user = Usuario.objects.get(pk=user_id)
    friend = Usuario.objects.get(pk=friend_id)
    Amigo.objects.filter(micorreo1=user, micorreo2=friend).delete()
    Amigo.objects.filter(micorreo1=friend, micorreo2=user).delete()

def get_playlists(user_id): #Devuelve todas las playlists en las que el usuario colabora devueltas como VO
    user = Usuario.objects.get(pk=user_id)
    ids = Colabora.objects.filter(miUsuario=user)
    return [Colabora.objects.get(pk=id).miPlaylist for id in ids]

def create_playlist(user_id, playlist_vo): #Se crea sin colaboradores
    user = Usuario.objects.get(pk=user_id)
    playlist = Playlist.objects.create(
        nombre=playlist_vo.nombre,
        publica=playlist_vo.publica
    )
    Colabora.objects.create(
        miUsuario=user,
        miPlaylist=playlist
    )

def update_playlist_details(playlist_id, playlist_vo): # Solo se puede cambiar el nombre(TODO: se puede poner foto)
    playlist = Playlist.objects.get(pk=playlist_id)
    playlist.nombre = playlist_vo.nombre
    playlist.publica = playlist_vo.publica
    playlist.save()

def delete_playlist(playlist_id): # Hay que hacer que los colaboradores dejen de colaborar
    playlist = Playlist.objects.get(pk=playlist_id)
    playlist.delete()

def get_playlist_songs(playlist_id): # Asume que la playlist es de canciones solo, devuelve VO de Cancion
    playlist = Playlist.objects.get(pk=playlist_id)
    ids = Contiene.objects.filter(miPlaylist=playlist)
    return [Cancion.objects.get(pk=id).to_VO() for id in ids]

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

def get_user_history(user_id): #Devuelve el historial de escucha del usuario devuelto como VO
    user = Usuario.objects.get(pk=user_id)
    ids = Historial.objects.filter(miUsuario=user)
    return [Historial.objects.get(pk=id).miAudio for id in ids]

def add_song_to_history(user_id, song_id): #Se añade la cancion al historial
    user = Usuario.objects.get(pk=user_id)
    song = Audio.objects.get(pk=song_id)
    Historial.objects.create(
        miUsuario=user,
        miAudio=song
    )

def get_user_favorites(user_id): #Devuelve las canciones favoritas del usuario devueltas como VO
    user = Usuario.objects.get(pk=user_id)
    ids = Favorito.objects.filter(miUsuario=user)
    return [Favorito.objects.get(pk=id).miAudio for id in ids]

def add_song_to_favorites(user_id, song_id): #Se añade la cancion a favoritos dado id
    user = Usuario.objects.get(pk=user_id)
    song = Audio.objects.get(pk=song_id)
    Favorito.objects.create(
        miUsuario=user,
        miAudio=song
    )

def remove_song_from_favorites(user_id, song_id): #Se elimina la cancion de favoritos dado id
    user = Usuario.objects.get(pk=user_id)
    song = Audio.objects.get(pk=song_id)
    Favorito.objects.filter(miUsuario=user, miAudio=song).delete()

def get_user_queue(user_id): #Devuelve la cola de reproduccion del usuario devuelta como VO
    user = Usuario.objects.get(pk=user_id)
    ids = Cola.objects.filter(miUsuario=user)
    return [Cola.objects.get(pk=id).miAudio for id in ids]

def add_song_to_queue(user_id, song_id): #Se añade la cancion a la cola de reproduccion
    user = Usuario.objects.get(pk=user_id)
    song = Audio.objects.get(pk=song_id)
    Cola.objects.create(
        miUsuario=user,
        miAudio=song
    )

def remove_song_from_queue(user_id, song_id): #Se elimina la cancion de la cola de reproduccion
    user = Usuario.objects.get(pk=user_id)
    song = Audio.objects.get(pk=song_id)
    Cola.objects.filter(miUsuario=user, miAudio=song).delete()

def get_genres(): #Devuelve todos los generos
    return Genero.objects.all()

def get_genre_songs(genre_name): #Devuelve todas las canciones de un genero dado su nombre
    genre = Genero.objects.get(nombre=genre_name)
    ids = Pertenecen.objects.filter(miGenero=genre)
    return [Pertenecen.objects.get(pk=id).miAudio for id in ids]

def get_album_songs(album_id): #Devuelve todas las canciones de un album dado su id
    album = Album.objects.get(pk=album_id)
    return Cancion.objects.filter(miAlbum=album)

def get_podcast_episodes(podcast_id): #Devuelve todos los capitulos de un podcast dado su id
    podcast = Podcast.objects.get(pk=podcast_id)
    return Capitulo.objects.filter(miPodcast=podcast)

def get_song_by_id(song_id): #Devuelve la cancion dado su id
    return Cancion.objects.get(pk=song_id)

def get_podcast_by_id(podcast_id): #Devuelve el podcast dado su id
    return Podcast.objects.get(pk=podcast_id)

def get_episode_by_id(episode_id): #Devuelve el capitulo dado su id
    return Capitulo.objects.get(pk=episode_id)

def get_album_by_id(album_id): #Devuelve el album dado su id
    return Album.objects.get(pk=album_id)

def get_song_genres(song_id): #Devuelve los generos de una cancion dado su id
    song = Cancion.objects.get(pk=song_id)
    ids = Pertenecen.objects.filter(miAudio=song)
    return [Pertenecen.objects.get(pk=id).miGenero for id in ids]

def get_song_album(song_id): #Devuelve el album de una cancion dado su id
    song = Cancion.objects.get(pk=song_id)
    return song.miAlbum

def get_song_artists(song_id): #Devuelve los artistas de una cancion dado su id
    song = Cancion.objects.get(pk=song_id)
    return song.cantantes

def get_song_audio(song_id): #Devuelve el audio de una cancion dado su id
    song = Cancion.objects.get(pk=song_id)
    return Audio.objects.get(pk=song.id)

def get_podcast_audio(podcast_id): #Devuelve el audio de un podcast dado su id
    podcast = Podcast.objects.get(pk=podcast_id)
    return Audio.objects.get(pk=podcast.id)

def get_episode_audio(episode_id): #Devuelve el audio de un capitulo dado su id
    episode = Capitulo.objects.get(pk=episode_id)
    return Audio.objects.get(pk=episode.id)

def get_audio_by_id(audio_id): #Devuelve el audio dado su id
    return Audio.objects.get(pk=audio_id)

def get_audio_name(audio_id): #Devuelve el nombre del audio dado su id
    audio = Audio.objects.get(pk=audio_id)
    return audio.nombre

def get_audio_score(audio_id): #Devuelve la puntuacion del audio dado su id
    audio = Audio.objects.get(pk=audio_id)
    return audio.puntuacion
    
def are_friends(user_email, friend_email): #Devuelve si dos usuarios son amigos
    return Amigo.objects.filter(micorreo1=user_email, micorreo2=friend_email).exists() or Amigo.objects.filter(micorreo1=friend_email, micorreo2=user_email).exists()