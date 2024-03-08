from django.shortcuts import render
from django.utils import timezone
from django.http import HttpResponse
from .models import Usuario, Amigo, Cancion, Podcast, Capitulo, Playlist, Colabora, Contiene, Historial, Favorito, Cola, Genero, Pertenecen, Album
from . import DAOs
from Psoft.serializers import UserSerializer
from rest_framework import viewsets


def home(request):
    text = "Home page"
    return HttpResponse(text, content_type='text/plain')
def test_are_friends(request):
    # Crear usuario
    user_vo = DAOs.get_user_by_correo("Paco@gmail.com")
    #DAOs.create_user(user_vo)
    # Crear amigo
    amigo_vo = DAOs.get_user_by_correo("PacoAmigo@gmail.com")
    #DAOs.create_user(amigo_vo)
    #DAOs.add_friend(user_vo.correo, amigo_vo.correo)
    if DAOs.are_friends(user_vo.correo,amigo_vo.correo) == True:
        friends = DAOs.get_friends(user_vo.correo)
        print("Amigos de Paco: ")
        for friend in friends:
            
            print(friend.correo + "\n")
    return HttpResponse(status=200)

def test_crear_playlist(request):
    # Crear usuario
    user_vo = DAOs.get_user_by_correo("Paco@gmail.com") #Esto en caso real se coge de la sesion
    # Crear playlist
    #DAOs.create_playlist(user_vo.correo, "Playlist de Paco", True)
    Playlists = DAOs.get_playlists_from_user(user_vo.correo)
    DAOs.update_playlist_details(Playlists[0].id, "Playlist Privada de Paco", False)
    #DAOs.create_song("Cancion de Paco")
    cancion = DAOs.get_song_by_id(2)
    #DAOs.add_song_to_playlist(Playlists[0].id,cancion.id)
    Canciones = DAOs.get_songs_from_playlist(1)
    if Canciones != None:
        for cancion in Canciones:
            print(cancion.nombre + "\n")
    return HttpResponse(status=200)

def test_queue_view(request):
    
    user = DAOs.get_user_by_correo("Paco@gmail.com")
    
    #DAOs.add_song_to_queue(user.correo, 2)
    queue = DAOs.get_queue_from_user(user.correo)
    # You can render these queue items in your template or just print them for testing
    for item in queue:
        print("Song:", item.nombre)
        print("Artist(s):", item.cantantes if item.cantantes else "N/A")
        print("Album:", item.miAlbum.nombre if item.miAlbum else "N/A")
        print()
    
    return HttpResponse(status=200)    

def test_password_view(request):
    user_vo = DAOs.get_user_by_correo("nerea@ejemplo.com")
    DAOs.check_user_password(user_vo, "nerea")
    if DAOs.check_user_password(user_vo, "nerea") == True:
        print("Contraseña correcta")
    else:
        print("Contraseña incorrecta")
    return HttpResponse(status=200)

# MAL
def test_add_song_to_history(request):
    user_vo = DAOs.get_user_by_correo("Paco@gmail.com")
    song_vo = DAOs.get_song_by_id(2)
    DAOs.add_song_to_history(user_vo.correo, song_vo.id)
    history = DAOs.get_user_history("Paco@gmail.com")
    if history != None:
        for song in history:
            print(song.nombre + "\n")
    else :
        print("No hay canciones en el historial")
    return HttpResponse(status=200)

# MAL
def test_remove_user(request):
    nuevo_usuario = Usuario(
        correo='ejemplo@gmail.com',
        nombre='ej',
        sexo='',
        nacimiento=timezone.now(),
        contrasegna='ej',
        pais=''
    )
    DAOs.create_user(nuevo_usuario)
    DAOs.remove_user(nuevo_usuario.correo)
    if DAOs.get_user_by_correo("ejemplo@gmail.com") == None:
        print("Usuario eliminado")
    else:
        print("Usuario no eliminado")
    return HttpResponse(status=200)


def test_add_friend(request):
    user_vo = DAOs.get_user_by_correo("Paco@gmail.com")
    nuevo_amigo = Usuario(
        correo='PacoAmigo2@gmail.com',
        nombre='PacoAmigo2',
        sexo='',
        nacimiento='',
        contrasegna='PacoAmigo2',
        pais=''
    )
    #DAOs.create_user(nuevo_amigo)
    nuevo_amigo = DAOs.get_user_by_correo("pacoamigo2@gmail.com")
    DAOs.add_friend(user_vo.correo, nuevo_amigo.correo)
    friends = DAOs.get_friends(user_vo.correo)
    print("Amigos de Paco: ")
    for friend in friends:
        print(friend.correo + "\n")
    return HttpResponse(status=200)

# EN PROCESO
def test_song(request):
    nueva_cancion = Cancion(
        letra='letra',
        cantantes='cantantes',
        miAlbum=None,
        puntuacion=None,
        nombre="Cancion de ejemplo"
    )
    #DAOs.create_song(nueva_cancion)
    #DAOs.add_song_to_playlist(1, DAOs.get_song_by_name("cancion2").id)
    Canciones = DAOs.get_songs_from_playlist(1)
    if Canciones != None:
        for cancion in Canciones:
            print(cancion.nombre + "\n")
            DAOs.add_song_rating(DAOs.get_song_by_name("cancion2").id, 5)
            print(DAOs.get_song_rating(DAOs.get_song_by_name("cancion2").id))
            #print(DAOs.get_song_album(DAOs.get_song_by_name("Cancion de ejemplo").id))
            print(DAOs.get_song_artists(DAOs.get_song_by_name("cancion2").id))
    return HttpResponse(status=200)     

def test_update_user(request):
    user_vo = DAOs.get_user_by_correo("Paco@gmail.com")
    print("datos anteriores de " + "\n" + user_vo.correo + "\n"  + user_vo.nombre + "\n" + user_vo.sexo + "\n" + str(user_vo.nacimiento) + "\n" + user_vo.contrasegna + "\n" + user_vo.pais + "\n")
    usuario_actualizado = Usuario(
        correo = "Paco@gmail.com",
        nombre='paco',
        sexo='M',
        nacimiento=timezone.now(),
        contrasegna='Paquito',
        pais='Espana'
    )
    DAOs.update_user(user_vo.correo, usuario_actualizado)
    user_vo = DAOs.get_user_by_correo("Paco@gmail.com")
    print("datos actuales de " + "\n" + user_vo.correo + "\n"  + user_vo.nombre + "\n" + user_vo.sexo + "\n" + str(user_vo.nacimiento) + "\n" + user_vo.contrasegna + "\n" + user_vo.pais + "\n")
    return HttpResponse(status=200)

def test_remove_friend(request):
    user_vo = DAOs.get_user_by_correo("Paco@gmail.com")
    nuevo_amigo = DAOs.get_user_by_correo("pacoamigo2@gmail.com")
    DAOs.remove_friend(user_vo.correo, nuevo_amigo.correo)
    return HttpResponse(status=200)

def test_get_genre_songs(request):
    DAOs.create_genre('pop')
    song_vo=DAOs.get_song_by_id(7)
    pertenecen_vo = Pertenecen(
        miGenero='pop',
        miAudio=song_vo.id
    )
    songs=DAOs.get_genre_songs('pop')
    for song in songs:
        print(song.nombre + "\n")
    return HttpResponse(status=200)

def test_remove_song_from_playlist(request):
    user_vo = DAOs.get_user_by_correo("Paco@gmail.com")
    Playlists = DAOs.get_playlists_from_user(user_vo.correo)
    cancion = DAOs.get_song_by_id(2)
    Canciones = DAOs.get_songs_from_playlist(1)
    print("Canciones de la playlist antes de eliminar una cancion: ")
    if Canciones != None:
        for cancion in Canciones:
            print(cancion.nombre + "\n")
    DAOs.remove_song_from_playlist(Playlists[0].id,cancion.id)
    print("Canciones de la playlist despues de eliminar una cancion: ")
    Canciones = DAOs.get_songs_from_playlist(1)
    if Canciones != None:
        for cancion in Canciones:
            print(cancion.nombre + "\n")
    return HttpResponse(status=200)

# MAL, INTENTAR CUANDO SE CONSIGA EL ADD SONG TO HISTORY
def test_remove_song_from_history(request):
    user_vo = DAOs.get_user_by_correo("Paco@gmail.com")
    historial = DAOs.get_user_history(user_vo.correo)
    print("Canciones del historial antes de eliminar una cancion: ")
    if historial != None:
        for cancion in historial:
            print(cancion.nombre + "\n")
    DAOs.remove_song_from_history(user_vo.correo, 7)
    historial = DAOs.get_user_history(user_vo.correo)
    print("Canciones del historial despues de eliminar una cancion: ")
    if historial != None:
        for cancion in historial:
            print(cancion.nombre + "\n")
    return HttpResponse(status=200)

# HAY QUE PROBARLO
def test_remove_song_from_queue(request):
    user_vo = DAOs.get_user_by_correo("PacoPaco@gmail.com")
    song_vo = DAOs.get_song_by_id(2)
    print("Canciones de la cola antes de eliminar una cancion: ")
    queue = DAOs.get_queue_from_user(user_vo.correo)
    if queue != None:
        for cancion in queue:
            print(cancion.nombre + "\n")
    DAOs.remove_song_from_queue(user_vo.correo, song_vo.id)
    print("Canciones de la cola despues de eliminar una cancion: ")
    queue = DAOs.get_queue_from_user(user_vo.correo)
    if queue != None:
        for cancion in queue:
            print(cancion.nombre + "\n")
    return HttpResponse(status=200)

# HAY QUE PROBARLO
def test_album(request):
    album_vo = Album(
        nombre='album de Paco'
    )
    DAOs.create_album(album_vo)
    album_vo = DAOs.get_album_by_name("album de Paco")
    print("Canciones del album antes de añadir: ")
    canciones = DAOs.get_album_songs(album_vo)
    if canciones != None:
        for cancion in canciones:
            print(cancion.nombre + "\n")
    album_vo = DAOs.get_album_by_id(1)
    cancion = DAOs.get_song_by_id(2)
    DAOs.add_song_to_album(album_vo, cancion)
    print("Canciones del album despues de añadir: ")
    canciones = DAOs.get_album_songs(album_vo)
    if canciones != None:
        for cancion in canciones:
            print(cancion.nombre + "\n")
    return HttpResponse(status=200)




#TEST API
class UserViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UserSerializer